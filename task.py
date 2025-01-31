from crewai import Task
from tools import tool
from agents import blog_researcher, blog_writer

research_task = Task(
    description=(
        "Identify the {topic}."
        "get detailed information about the website"
    ),
    expected_output = "A comprehensive 3 paragraphs long report",
    tools=[tool],
    agent = blog_researcher,
)

writer_task = Task(
    description=(
        "get the info from the website{topic}."
    ),
    expected_output = "Summarize the info from website",
    tools=[tool],
    agent = blog_writer,
    output_file = 'new-blog-plost.md'
)

