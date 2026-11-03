# Multiple Agents Using CrewAI

A small multi-agent pipeline built with [CrewAI](https://github.com/crewAIInc/crewAI) that turns a website into a blog post.

Two agents work in sequence:

1. **Blog Researcher** searches a single website (via `WebsiteSearchTool`) and writes a short report of the facts it finds about a topic.
2. **Blog Writer** takes that report and writes a markdown blog post with a title, headings and a call to action.

The result is saved to `blog-post.md`. The defaults target the [Sui Agent Typhoon hackathon page](https://sui.io/sui-agent-typhoon#tracks-prizes), but any URL and topic work.

## Built with

- [`crewai`](https://pypi.org/project/crewai/): the framework for defining agents, tasks and the crew that runs them.
- [`crewai-tools`](https://pypi.org/project/crewai-tools/): ready-made tools for agents. This project uses `WebsiteSearchTool` to search a single website.
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): loads `OPENAI_API_KEY` from `.env`.

## Project structure

| File | Purpose |
| --- | --- |
| `crew.py` | Entry point: parses CLI args, builds the crew and runs it |
| `agents.py` | Defines the researcher and writer agents |
| `task.py` | Defines the research and writing tasks (the writer receives the research as context) |
| `tools.py` | Builds the `WebsiteSearchTool` restricted to one URL |
| `blog-post.md` | Sample output from an earlier run |
| `output/` | Generated posts (created on first run) |

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env` and set `OPENAI_API_KEY`. CrewAI uses OpenAI by default, and `WebsiteSearchTool` also uses it for embeddings.

## Usage

Run with the defaults:

```bash
python crew.py
```

Or point it at any website and topic:

```bash
python crew.py --url https://example.com/some-page --topic "Example topic"
```

The final post is printed to the terminal and saved to `output/<topic-slug>.md` (for example `output/sui-ai-hackathon.md`), so different topics don't overwrite each other. Use `--out path/to/file.md` to choose the file yourself.

The script exits with a clear message if the topic is empty, the URL isn't a valid http(s) URL, `OPENAI_API_KEY` is missing, or the crew fails.

## Customizing

- **Tone, length, audience:** edit the `writer_task` description in `task.py`.
- **Agent behavior:** edit the roles, goals and backstories in `agents.py`.
- **Memory and telemetry:** `memory` and `share_crew` are off. Enable them in `crew.py` if you need them (`share_crew=True` sends data to CrewAI).
- **Different LLM:** set the `llm` argument on the agents; see the CrewAI docs for supported providers.

## Ideas for improvement

- Add a reviewer agent that fact-checks the draft against the source page.
- Add a general web search tool (for example `SerperDevTool`) alongside the website tool.
- Pin dependency versions in `requirements.txt` once you have a working setup (`pip freeze`).
- Detect pages that load but return little content, and stop instead of padding.
