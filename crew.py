import argparse

from dotenv import load_dotenv
from crewai import Crew, Process

from agents import build_agents
from task import build_tasks
from tools import build_tool

DEFAULT_URL = 'https://sui.io/sui-agent-typhoon#tracks-prizes'
DEFAULT_TOPIC = 'SUI AI hackathon'


def main():
    parser = argparse.ArgumentParser(description='Generate a blog post from a website.')
    parser.add_argument('--url', default=DEFAULT_URL, help='website the agents may search')
    parser.add_argument('--topic', default=DEFAULT_TOPIC, help='topic of the blog post')
    args = parser.parse_args()

    load_dotenv()

    tool = build_tool(args.url)
    blog_researcher, blog_writer = build_agents(tool)
    research_task, writer_task = build_tasks(blog_researcher, blog_writer, tool)

    crew = Crew(
        agents=[blog_researcher, blog_writer],
        tasks=[research_task, writer_task],
        process=Process.sequential,
        memory=False,
        cache=True,
        max_rpm=100,
        share_crew=False,
    )

    result = crew.kickoff(inputs={'topic': args.topic})
    print(result)


if __name__ == '__main__':
    main()
