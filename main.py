from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional
from news_service import NewsService
from llm_agents import NewsLLMAgent  

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

news_service = NewsService()
llm_agent = NewsLLMAgent() 

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/news")
async def get_news(category: Optional[str] = "general", limit: int = 10):
    if limit not in [3, 5, 10]:
        limit = 10
    try:
        raw_news = await news_service.get_trending_news(category=category, limit=limit)
        
        enhanced_news = [llm_agent.enhance(article) for article in raw_news]

        return {
            "articles": enhanced_news,
            "category": category,
            "count": len(enhanced_news)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {e}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "trending-news-api"}
