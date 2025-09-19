from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import BASE_DIR, UPDATES_DIR

from app.api.v1.print import router as print_router
from app.api.v1.mapping import router as mapping_router
from app.api.v1.client import router as client_router
from app.api.v1.orders import router as orders_router
from app.api.v1.import_ import router as import_router

app = FastAPI(title="Huandan Server")

# 挂载静态与更新包目录
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/updates", StaticFiles(directory=str(UPDATES_DIR)), name="updates")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 页面
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("orders/list.html", {"request": request})

@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return templates.TemplateResponse("orders/list.html", {"request": request})

@app.get("/orders/print", response_class=HTMLResponse)
def print_board(request: Request):
    return templates.TemplateResponse("orders/print_board.html", {"request": request})

@app.get("/settings/clients", response_class=HTMLResponse)
def settings_clients(request: Request):
    return templates.TemplateResponse("settings/clients.html", {"request": request})

# API
app.include_router(mapping_router, prefix="/api/v1", tags=["mapping"])
app.include_router(print_router,   prefix="/api/v1", tags=["print"])
app.include_router(client_router,  prefix="/api/v1", tags=["client"])
app.include_router(orders_router,  prefix="/api/v1", tags=["orders"])
app.include_router(import_router,  prefix="/api/v1", tags=["import"])

