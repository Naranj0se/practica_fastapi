from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from src.routers.book_router import book_router
from src.utils.http_error_handler import HTTPErrorHandler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="Mi primera API",
    description="Api de prueba para aprender FastAPI",
    version="1.0",
)


# Middleware manejador de errores
# app.add_middleware(HTTPErrorHandler)
@app.middleware("http")
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    try:
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content={"message": content}, status_code=status_code)


# Configuración de la carpeta de archivos estáticos y plantillas

static_path = os.path.join(os.path.dirname(__file__), "static")
templates_path = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

# Rutas

def common_params(start_date: str = None, end_date: str = None):
    return {"start_date": start_date, "end_date": end_date}

@app.get("/", tags=["home"])
def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Hola Mundo!"}
    )

@app.get("/users", tags=["users"])
def get_users(commons: dict = Depends(common_params)):
    return f"Obteniendo usuarios desde {commons["start_date"]} hasta {commons["end_date"]}"

@app.get("/customers", tags=["customers"])
def get_customers(commons: dict = Depends(common_params)):
    return f"Obteniendo clientes desde {commons["start_date"]} hasta {commons["end_date"]}"


app.include_router(prefix="/books", router=book_router)
