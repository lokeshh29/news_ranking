import aiohttp
from typing import List, Dict, Optional

class NewsService:
    def __init__(self):
        self.api_key = "b43960956c7072d1e72ae1120f769830"
        self.base_url = "https://gnews.io/api/v4"

    async def get_trending_news(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        params = {
            "token": self.api_key,
            "lang": "en",
            "country": "us",
            "max": min(limit, 100),
            "sortby": "publishedAt"
        }
        if category and category != "general":
            url = f"{self.base_url}/search"
            params["q"] = category
        else:
            url = f"{self.base_url}/top-headlines"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("articles", [])[:limit]
                return []
