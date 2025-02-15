import autogen

config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4"],
        },
    )
llm_config = {"config_list": config_list, "cache_seed": 42}

class ResearchManager:

    print_callback_function = None
    user_proxy = None

    #coder = None
    #pm = None

    engineer = None
    scientist = None
    planner = None
    executor = None
    critic = None

    groupchat = None
    manager = None

    # Constructor method with instance variables name and age
    def __init__(self, print_callback_function):
        self.print_callback_function = print_callback_function

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
        )
        self.engineer = autogen.AssistantAgent(
            name="Engineer",
            llm_config=llm_config,
            system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        """,
        )
        self.scientist = autogen.AssistantAgent(
            name="Scientist",
            llm_config=llm_config,
            system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
        )
        self.planner = autogen.AssistantAgent(
            name="Planner",
            system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
        The plan may involve an engineer who can write code and a scientist who doesn't write code.
        Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
        """,
            llm_config=llm_config,
        )
        self.executor = autogen.UserProxyAgent(
            name="Executor",
            system_message="Executor. Execute the code written by the engineer and report the result.",
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "paper",
                "use_docker": False,
            },
            # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        )
        self.critic = autogen.AssistantAgent(
            name="Critic",
            system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
            llm_config=llm_config,
        )
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.engineer, self.scientist, self.planner, self.executor, self.critic], messages=[], max_round=50
        )
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=llm_config)

        '''
        self.user_proxy = autogen.UserProxyAgent(
            name="User_proxy",
            system_message="A human admin.",
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": "groupchat",
                "use_docker": False,
            },
            # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
            human_input_mode="TERMINATE",
        )
        self.coder = autogen.AssistantAgent(
            name="Coder",
            llm_config=llm_config,
        )
        self.pm = autogen.AssistantAgent(
            name="Product_manager",
            system_message="Creative in software product ideas.",
            llm_config=llm_config,
        )
        self.groupchat = autogen.GroupChat(agents=[self.user_proxy, self.coder, self.pm], messages=[], max_round=12)
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=llm_config)
        '''

        # Register print function for the agents
        self.user_proxy.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_callback_function,
            config={"callback": None},
        )

        self.engineer.register_reply([autogen.Agent, None],reply_func=self.print_callback_function,config={"callback": None},)
        self.scientist.register_reply([autogen.Agent, None],reply_func=self.print_callback_function,config={"callback": None},)
        self.planner.register_reply([autogen.Agent, None],reply_func=self.print_callback_function,config={"callback": None},)
        self.executor.register_reply([autogen.Agent, None],reply_func=self.print_callback_function,config={"callback": None},)
        self.critic.register_reply([autogen.Agent, None],reply_func=self.print_callback_function,config={"callback": None},)

        '''
        self.coder.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_callback_function,
            config={"callback": None},
        )

        self.pm.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_callback_function,
            config={"callback": None},
        )
        '''

        print('ResearchManager initialized')

    def run(self, input):
        print('ResearchManager run: '+ input)
        result = self.user_proxy.initiate_chat(self.manager, message=input)
        return result
