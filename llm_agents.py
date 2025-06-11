import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class NewsLLMAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            self.enabled = True
        else:
            self.model = None
            self.enabled = False

    def enhance_article(self, article):
        if not self.enabled:
            return {**article, "enhanced": False}

        try:
            summary = self._generate_summary(article)
            topics = self._generate_topics(article)
            return {
                **article,
                "enhanced_summary": summary,
                "key_topics": topics,
                "enhanced": True,
            }
        except:
            return {**article, "enhanced": False}

    def categorize_articles(self, articles):
        if not self.enabled:
            return {"general": articles}

        result = {}
        for art in articles:
            try:
                cat = self._generate_category(art)
            except:
                cat = "general"

            if cat not in result:
                result[cat] = []
            result[cat].append(art)
        return result

    def _article_as_text(self, art):
        title = art.get("title", "")
        desc = art.get("description", "")
        content = (art.get("content", "") or "")[:500]
        return f"Title:\n{title}\n\nDescription:\n{desc}\n\nContent:\n{content}"

    def _generate_summary(self, art):
        prompt = (
            "Write a short 2–3 sentence summary.\n\n"
            + self._article_as_text(art)
            + "\n\nSummary:"
        )
        return self._ask_gemini(prompt)

    def _generate_topics(self, art):
        prompt = (
            "Extract 3 to 5 topics. Return JSON: {\"topics\": [\"topic1\", \"topic2\"]}.\n\n"
            + self._article_as_text(art)
            + "\n\nJSON only:"
        )
        raw = self._ask_gemini(prompt)
        return self._safe_json(raw).get("topics", [])

    def _generate_category(self, art):
        prompt = (
            "Choose one category: business, entertainment, health, science, sports, technology, general. "
            "Return JSON: {\"category\": \"...\"}.\n\n"
            + self._article_as_text(art)
            + "\n\nJSON only:"
        )
        raw = self._ask_gemini(prompt)
        return self._safe_json(raw).get("category", "general")

    def _ask_gemini(self, prompt):
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1].strip()
        return text

    def _safe_json(self, txt):
        try:
            return json.loads(txt)
        except:
            return {}
