import os

try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

api_key = os.getenv("GEMINI_API_KEY", "")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key) if api_key else None
    prompt = PromptTemplate(
        input_variables=["title", "description"],
        template="Summarize this news article briefly:\n\nTitle: {title}\n\nDescription: {description}"
    )
    summarizer_chain = prompt | llm if llm else None
except Exception:
    summarizer_chain = None

class NewsLLMAgent:
    def enhance(self, article: dict) -> dict:
        title = article.get("title", "")
        description = article.get("description", "")
        if not title and not description:
            article["summary"] = "No summary available"
            return article
        if not summarizer_chain:
            article["summary"] = description or "No summary available"
            return article
        try:
            if hasattr(summarizer_chain, "invoke"):
                result = summarizer_chain.invoke({"title": title, "description": description})
                summary = result.content if hasattr(result, "content") else str(result)
            else:
                summary = summarizer_chain.run(title=title, description=description)
            article["summary"] = summary.strip()
        except Exception:
            article["summary"] = description or "LLM summarization failed"
        return article

