class NewsLLMAgent:
    def __init__(self):
        self.enabled = False 

    def enhance_article(self, article):
        return {
            **article,
            "enhanced": False
        }

    def categorize_articles(self, articles):
        return {
            "general": articles
        }
