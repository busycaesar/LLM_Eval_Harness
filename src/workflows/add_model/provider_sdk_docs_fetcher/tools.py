import re
from ddgs import DDGS

WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Search the web and return up to 5 result summaries. Use this to discover "
            "documentation pages, official SDK repos, and code examples relevant to the request."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
    },
}

WEB_FETCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_fetch",
        "description": (
            "Fetch a URL and return the page's extracted text content (HTML tags stripped, "
            "capped at 10000 chars). Use this to read a specific documentation page you've "
            "identified from a search result."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Absolute URL to fetch"},
            },
            "required": ["url"],
        },
    },
}

def web_search(query: str) -> list | dict:
    try:
        with DDGS() as ddgs:
            return [
                {"title": r.get("title"), "url": r.get("href"), "snippet": r.get("body")}
                for r in ddgs.text(query, max_results=5)
            ]
    except Exception as e:
        return {"error": f"web_search failed: {type(e).__name__}: {e}"}

def web_fetch(url: str) -> str | dict:
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"error": f"web_fetch failed for {url}: {type(e).__name__}: {e}"}
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:10000]