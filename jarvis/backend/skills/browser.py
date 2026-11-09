import requests
from backend.skills.base import Skill
from backend.llm.factory import create_llm
from backend.core.logger import get_logger


class BrowserSkill(Skill):

    name = "browser"

    description = "Searches the web or fetches online information."

    def __init__(self):
        self.logger = get_logger("BrowserSkill")
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = create_llm()
        return self._llm

    def execute(self, **kwargs) -> str:
        query = kwargs.get("query", "").strip()
        if not query:
            return "Please provide a query to search."

        # Try DuckDuckGo Instant Answer API
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1",
            }
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                answer = data.get("Answer")
                abstract = data.get("AbstractText")
                if answer:
                    return str(answer)
                if abstract:
                    return str(abstract)
        except Exception as e:
            self.logger.warning(f"DuckDuckGo search failed: {e}")

        # Fallback to LLM with search intent
        try:
            prompt = f"Please provide a helpful and factual answer to this web search request: {query}"
            return self.llm.generate(prompt)
        except Exception as e:
            self.logger.error(f"LLM fallback failed: {e}")
            return f"I could not retrieve information for '{query}' at the moment."
