from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatGoogleGenerativeAI(model="models/chat-bison-001", google_api_key="AIzaSyDFKJGHipveJt_s_ZDOrnn1PdJj2VlQAQ")

prompt = PromptTemplate(
    input_variables=["title", "description"],
    template="Summarize this news article briefly:\n\nTitle: {title}\n\nDescription: {description}"
)

summarizer_chain = LLMChain(llm=llm, prompt=prompt)

class NewsLLMAgent:
    def enhance(self, article: dict) -> dict:
        title = article.get("title", "")
        description = article.get("description", "")
        if not title and not description:
            article["summary"] = "No summary available"
            return article
        try:
            summary = summarizer_chain.run(title=title, description=description)
            article["summary"] = summary.strip()
        except Exception as e:
            article["summary"] = "LLM summarization failed"
        return article
