from crewai import Agent
from tools import tool

blog_researcher = Agent(
    role = 'Blog Researcher from Website',
    goal = 'get the relevant content for the topic {topic} from Website',
    verbose = True,
    memory = True,
    backstory = (
        "Expert in understanding data in website"
    ),
    tools = [tool],
    allow_delegation = True
)

blog_writer = Agent(
    role = 'Blog Writer',
    goal = 'Narrate compelling story about the video {topic} from Yt channel',
    verbose = True,
    memory = True,
    backstory = (
        "Expert in simplifying complex topics."
    ),
    tools = [tool],
    allow_delegation = True 
)