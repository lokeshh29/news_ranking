import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime

class NewsService:
    def __init__(self):
        self.api_key = "b43960956c7072d1e72ae1120f769830"
        self.base_url = "https://gnews.io/api/v4"

    async def get_trending_news(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Fetch trending news articles"""
        params = {
            "token": self.api_key,
            "lang": "en",
            "country": "us",
            "max": min(limit, 100),
            "sortby": "publishedAt"
        }
        if category and category.lower() != "general":
            params["category"] = category

        url = f"{self.base_url}/top-headlines"
        return await self._fetch_articles(url, params, limit)

    async def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """Search news articles by keyword"""
        params = {
            "q": query,
            "token": self.api_key,
            "lang": "en",
            "country": "us",
            "max": min(limit, 100),
            "sortby": "relevance"
        }

        url = f"{self.base_url}/search"
        return await self._fetch_articles(url, params, limit)

    async def _fetch_articles(self, url: str, params: Dict, limit: int) -> List[Dict]:
        """Generic method to fetch and process articles"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        return [
                            self._process_article(a) for a in articles[:limit]
                            if self._process_article(a)
                        ]
                    elif response.status == 401:
                        raise Exception("Invalid API key")
                    elif response.status == 429:
                        raise Exception("API rate limit exceeded")
                    else:
                        error = await response.text()
                        raise Exception(f"GNews error {response.status}: {error}")
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Fetch error: {str(e)}")

    def _process_article(self, article: Dict) -> Optional[Dict]:
        """Clean and format a single article"""
        try:
            if not article.get("title") or not article.get("description"):
                return None

            published_at = article.get("publishedAt")
            if published_at:
                try:
                    dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    published_at = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                except:
                    published_at = "Unknown"

            return {
                "title": article.get("title", "").strip(),
                "description": article.get("description", "").strip(),
                "url": article.get("url", ""),
                "image": article.get("image"),
                "publishedAt": published_at,
                "source": {
                    "name": article.get("source", {}).get("name", "Unknown Source"),
                    "url": article.get("source", {}).get("url", "")
                },
                "content": article.get("content", "")
            }
        except Exception as e:
            print(f"Article processing error: {e}")
            return None
