from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings, BASE_DIR
from .core.db import init_db
from .api import auth, planners, history

app=FastAPI(title=settings.app_name,version="1.0.0",description="Budget-aware GenAI recommendation assistant")
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_origin,"http://localhost:8000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=BASE_DIR/"static"),name="static")
templates=Jinja2Templates(directory=BASE_DIR/"templates")
app.include_router(auth.router,prefix="/api")
app.include_router(planners.router,prefix="/api")
app.include_router(history.router,prefix="/api")

@app.on_event("startup")
def startup(): init_db()

@app.get("/",response_class=HTMLResponse)
def index(request:Request): return templates.TemplateResponse("index.html",{"request":request})
@app.get("/login",response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse("login.html",{"request":request})
@app.get("/register",response_class=HTMLResponse)
def register_page(request:Request): return templates.TemplateResponse("register.html",{"request":request})
@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request): return templates.TemplateResponse("dashboard.html",{"request":request})
@app.get("/planner/{kind}",response_class=HTMLResponse)
def planner_page(request:Request,kind:str):
    if kind not in {"home","party","jewelry"}: return templates.TemplateResponse("404.html",{"request":request},status_code=404)
    return templates.TemplateResponse(f"{kind}.html",{"request":request})
@app.get("/startup")
def startup_status(): return {"status":"ok","gemini_configured":bool(settings.gemini_api_key)}
@app.get("/recommendations-details")
def details(): return {"message":"Use the planner endpoints to generate recommendations."}

if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
