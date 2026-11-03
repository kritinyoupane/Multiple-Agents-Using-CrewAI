from crewai import Task

OUTPUT_FILE = 'blog-post.md'


def build_tasks(blog_researcher, blog_writer, tool):
    research_task = Task(
        description=(
            "Identify the key facts about {topic}. "
            "Get detailed information from the website, including dates, "
            "prizes, tracks and any other relevant details."
        ),
        expected_output="A comprehensive 3 paragraph report of the findings",
        tools=[tool],
        agent=blog_researcher,
    )

    writer_task = Task(
        description=(
            "Using the research on {topic}, write an engaging blog post with "
            "a title, short intro, clear headings and a closing call to action."
        ),
        expected_output=(
            "A blog post in markdown. Do not wrap the output in a code fence."
        ),
        agent=blog_writer,
        context=[research_task],
        output_file=OUTPUT_FILE,
    )

    return research_task, writer_task
