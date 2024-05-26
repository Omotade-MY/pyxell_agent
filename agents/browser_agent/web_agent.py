import os
import openai
from dotenv import load_dotenv, find_dotenv
from lavague.core import ActionEngine
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import PythonEngine
from lavague.core import WorldModel
from lavague.core.agents import WebAgent
from langchain_openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
import logging
# Configure the logging
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
                    handlers=[
                        logging.FileHandler("agent.log"),  # Log to a file
                        logging.StreamHandler()  # Also log to console
                    ])
logger = logging.getLogger(__name__)
_ = load_dotenv(find_dotenv())
# Load OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class LavagueInput(BaseModel):
    url: str = Field(description="the base url of the platform")
    task: str = Field(description="the task from the user")

class BrowserAgent:
    
    selenium_driver = SeleniumDriver(headless=True)
    action_engine = ActionEngine(selenium_driver)
    python_engine = PythonEngine()
    world_model = WorldModel()
    
    def __generate_prompt(self, task):
        """
        Generates a prompt for the given query.

        Args:
            query (str): The query for which the prompt is generated.

        Returns:
            dict: The generated prompt in the format specified.

        Example:
            >>> generate_prompt("Go to any football platform and get me the last english premiership scores.")
            {
                "url": "https://huggingface.co/login",
                "modified_user_task_prompt": "Navigate to Hugging Face and log in with my credentials. Go to my profile and get the name of the latest model I uploaded."
            }
        """
        from textwrap import dedent

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=LavagueInput)

        query = PromptTemplate(template = dedent("""  
        You are provided with the user task prompt, and your output should be a modified breakdown of the user task prompt.
        Your output should be in this format and modified user task prompt.


        1. Follow these guidelines based on the user's request:
        - For account creation: Provide steps and site links.
        - For data extraction from a website: Provide the URL and a detailed data extraction prompt.
        - For retrieving information from a profile (e.g., latest model on Hugging Face): Provide the URL and a step-by-step breakdown.
        - For other platform data requests (e.g., stock prices from Yahoo Finance): Log in if necessary, navigate to the relevant section, and extract the specified information. Provide the URL and a detailed breakdown.



        Example Prompts and ```EXPECTED OUTPUT FORMAT```:

        User Prompt:
        "Go on Hugging Face platform, log in with my credentials username:chukypedro15@gmail.com and password:k2%H_h5E@pK7Kgf, and navigate to my profile to get the name of the latest model I uploaded."

            Expected Output:
            {{
                "url": "https://huggingface.co/login",
                "modified_task": "Navigate to Hugging Face and log in with my credentials. Go to my profile and get the name of the latest model I uploaded."
            }}
        User Prompt:
        "Go to Zoom and create an account for me."

            Expected Output:
            {{
                "url": "https://zoom.us/",
                "modified_task": "Go to Zoom, navigate to the Sign-Up page, and create an account for me."
            }}


        REMEBER THAT YOU ARE ONLY MODIFYING USER PROMPT AND NOT PERFORMING THE TASK.

        User Prompt:

        ```{task}```

        ENSURE THAT YOU ADHERE TO ```EXPECTED OUTPUT FORMAT```  AND URL MUST BE ACCURATE. 

        LASTLY ENSURE THE OUTPUT KEYS ARE **url** and **modified_task**. RETURN ONLY THE JSONOUTPU AND NOTHING MORE


        """),
                            
        input_variables=["task"],
        )
        # Choose the LLM to use
        llm = OpenAI()
        new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

        chain = query | llm | new_parser
        response = chain.invoke({"task": task}) 
        
        return response

    def execute(self, task):
        """
        Executes a task by generating a modified user task prompt, creating a WebAgent,
        navigating to the URL specified in the modified user task prompt, and running the 
        modified task using the WebAgent.
        
        :param task: A dictionary containing the user task prompt and the URL to navigate to.
        :type task: dict
        
        :return: The output of running the modified task using the WebAgent.
        :rtype: Any
        """
        
        modified_user_task = self.__generate_prompt(task)
        
        agent = WebAgent(self.world_model, self.action_engine, self.python_engine)
        agent.get(modified_user_task["url"])
        output = agent.run(modified_user_task["modified_task"])
        
        return output
        