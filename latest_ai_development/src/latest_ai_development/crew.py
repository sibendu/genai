from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_core.callbacks import BaseCallbackHandler
from crewai_tools import SerperDevTool

# Uncomment the following line to use an example of a custom tool
# from latest_ai_development.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopment():
	"""LatestAiDevelopment crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	researcher_callback = None
	reporting_analyst_callback = None

	# Constructor method with instance variables name and age
	def __init__(self, researcher_callback, reporting_analyst_callback):
		self.researcher_callback = researcher_callback
		self.reporting_analyst_callback = reporting_analyst_callback
		print('agent_step_callback_functions are set')

	@agent
	def researcher(self) -> Agent:
		print(self.researcher_callback)
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			step_callback=self.researcher_callback,
			#callbacks=[final_callback_function],
      		#tools=[SerperDevTool(), Salesforcetoo, SAPtool]
		)

	@agent
	def reporting_analyst(self) -> Agent:
		print(self.researcher_callback)
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			step_callback=self.reporting_analyst_callback,
			#callbacks=[final_callback_function],
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			#callback=task_callback_function,
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			#callback=task_callback_function,
			output_file='output/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
