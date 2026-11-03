from crewai_tools import WebsiteSearchTool


def build_tool(url: str) -> WebsiteSearchTool:
    """Limit the search to the content of a specific website,
    so the agents can only search within that website."""
    return WebsiteSearchTool(website=url)
