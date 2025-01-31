from crewai_tools import WebsiteSearchTool


# Example of limiting the search to the content of a specific website, 
# so now agents can only search within that website
tool = WebsiteSearchTool(website='https://sui.io/sui-agent-typhoon#tracks-prizes')

# from crewai.tools import tool

# @tool("Tool Name")
# def dex_tool(searchterm: str) -> str:
#     """Tool description for clarity."""
#     # Tool logic here
#     return "Tool output"