from crewai import Agent


def build_agents(tool):
    blog_researcher = Agent(
        role='Blog Researcher',
        goal='Gather accurate, relevant content about {topic} from the website',
        verbose=True,
        memory=False,
        backstory=(
            "You are a careful researcher who extracts facts from web pages. "
            "You only report information that is actually found on the page "
            "and never invent details."
        ),
        tools=[tool],
        allow_delegation=False,
    )

    blog_writer = Agent(
        role='Blog Writer',
        goal='Write a compelling, easy-to-read blog post about {topic}',
        verbose=True,
        memory=False,
        backstory=(
            "You are an expert at simplifying complex topics for a general "
            "audience. You write only from the research you are given."
        ),
        allow_delegation=False,
    )

    return blog_researcher, blog_writer
