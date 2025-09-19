import logging
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import crud, models
from .database import SessionLocal, engine, Base
from fastapi import HTTPException
from .logging_config import logger
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

logger = logging.getLogger("app_logger")  # Assure que le logger est configuré (via logging_config.py)
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host  # récupère l’IP du client

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        log_line = f"{client_ip} - {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms"
        logger.info(log_line)

        return response

app.add_middleware(
    ServerErrorMiddleware,
    handler=lambda request, exc: logger.error(f"Erreur serveur: {exc}")
)
app.add_middleware(LoggingMiddleware)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.client.host} connecté à /users")
    users = crud.get_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

@app.get("/users/new", response_class=HTMLResponse)
def new_user_form(request: Request):
    logger.info(f"{request.client.host} connecté à /users/new")
    return templates.TemplateResponse("user_form.html", {"request": request, "form_action": "/users/new"})

@app.post("/users/new")
def create_user(fullname: str = Form(...), studylevel: str = Form(...), age: int = Form(...), db: Session = Depends(get_db)):
    user_data = {"fullname": fullname, "studylevel": studylevel, "age": age}
    crud.create_user(db, user_data)
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/delete", response_class=HTMLResponse)
def delete_user_hub(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.client.host} connecté à /users/delete")
    users = crud.get_users(db)
    return templates.TemplateResponse("users_delete_hub.html", {"request": request, "users": users})

@app.get("/users/delete/{user_uuid}", response_class=HTMLResponse)
def confirm_delete_user(request: Request, user_uuid: str, db: Session = Depends(get_db)):
    logger.info(f"{request.client.host} connecté à /users/delete/{user_uuid}")
    user = crud.get_user(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_delete_confirm.html", {"request": request, "user": user})

@app.post("/users/delete/{user_uuid}")
def delete_user(user_uuid: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_uuid)
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/edit", response_class=HTMLResponse)
def edit_user_hub(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.client.host} connecté à /users/edit")
    users = crud.get_users(db)
    return templates.TemplateResponse("users_edit_hub.html", {"request": request, "users": users})

@app.get("/users/edit/{user_uuid}", response_class=HTMLResponse)
def edit_user_form(request: Request, user_uuid: str, db: Session = Depends(get_db)):
    logger.info(f"{request.client.host} connecté à /users/edit/{user_uuid}")
    user = crud.get_user(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_edit_form.html", {"request": request, "user": user, "form_action": f"/users/edit/{user_uuid}"})

@app.post("/users/edit/{user_uuid}")
def update_user(user_uuid: str, fullname: str = Form(...), studylevel: str = Form(...), age: int = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = {"fullname": fullname, "studylevel": studylevel, "age": age}
    crud.update_user(db, user_uuid, updated_data)
    return RedirectResponse(url="/users", status_code=303)
