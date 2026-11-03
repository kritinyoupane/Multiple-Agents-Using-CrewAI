import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from crewai import Crew, Process

from agents import build_agents
from task import build_tasks
from tools import build_tool

DEFAULT_URL = 'https://sui.io/sui-agent-typhoon#tracks-prizes'
DEFAULT_TOPIC = 'SUI AI hackathon'
OUTPUT_DIR = Path('output')


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'blog-post'


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def main():
    parser = argparse.ArgumentParser(description='Generate a blog post from a website.')
    parser.add_argument('--url', default=DEFAULT_URL, help='website the agents may search')
    parser.add_argument('--topic', default=DEFAULT_TOPIC, help='topic of the blog post')
    parser.add_argument(
        '--out',
        help='output markdown file (default: output/<topic-slug>.md)',
    )
    args = parser.parse_args()

    load_dotenv()

    if not args.topic.strip():
        sys.exit('Error: --topic must not be empty.')
    if not is_valid_url(args.url):
        sys.exit(f'Error: "{args.url}" is not a valid http(s) URL.')
    if not os.getenv('OPENAI_API_KEY'):
        sys.exit(
            'Error: OPENAI_API_KEY is not set. Copy .env.example to .env '
            'and add your key.'
        )

    output_file = Path(args.out) if args.out else OUTPUT_DIR / f'{slugify(args.topic)}.md'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        tool = build_tool(args.url)
        blog_researcher, blog_writer = build_agents(tool)
        research_task, writer_task = build_tasks(
            blog_researcher, blog_writer, tool, str(output_file)
        )

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
    except KeyboardInterrupt:
        sys.exit('\nInterrupted.')
    except Exception as exc:
        sys.exit(f'Error: the crew failed ({type(exc).__name__}): {exc}')

    print(result)
    print(f'\nSaved to {output_file}')


if __name__ == '__main__':
    main()
