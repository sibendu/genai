from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from crewai_enterprise_content_marketing_ideas.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool


@CrewBase
class CrewaiEnterpriseContentMarketingCrew:
    """CrewaiEnterpriseContentMarketing crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    researcher_callback = None
    content_generator_callback = None

    # Constructor method with instance variables name and age
    def __init__(self, researcher_callback, content_generator_callback):
        self.researcher_callback = researcher_callback
        self.content_generator_callback = content_generator_callback
        print('agent_step_callback_functions are set')

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            #tools=[SerperDevTool()],
            verbose=True,
            step_callback=self.researcher_callback,
        )

    @agent
    def content_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_generator"],
            verbose=True,
            step_callback=self.content_generator_callback,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_generation_task"], output_file="report.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiEnterpriseContentMarketing crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
