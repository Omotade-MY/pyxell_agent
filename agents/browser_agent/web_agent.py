import os
import openai
from dotenv import load_dotenv, find_dotenv
from lavague.core import ActionEngine
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import PythonEngine
from lavague.core import WorldModel
from lavague.core.agents import WebAgent
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
import logging
# Configure the logging
# logging.basicConfig(level=logging.DEBUG,  # Set the logging level
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
#                     handlers=[
#                         logging.FileHandler("agent.log"),  # Log to a file
#                         logging.StreamHandler()  # Also log to console
#                     ])
# logger = logging.getLogger(__name__)
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
            >>> generate_prompt("Go to any football platform and get me the latest english premiership result.")
            {
                "url": "https://huggingface.co/login",
                "modified_user_task_prompt": "Navigate to Hugging Face and log in with my credentials. Go to my profile and get the name of the latest model I uploaded."
            }
        """
        from textwrap import dedent

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=LavagueInput)

        query = PromptTemplate(template = dedent("""  
        You are an excellent assistant. You have provided with a prompt for the user.
        Your task:
        - Understand the request of the user
        - Generate a breakdown and step by step instruction on how to execute the task.
        - Provide relevant information needed such as links to a website, details to fill a form
        - You output should adhere strictly to this format
                                        

        You should answer these thought questions:
        1. Does this the task require Login?
        2. Has the user provided Login Credentials?
        3. Does the task require other information and has the user provided them?

        ** Follow these guidelines based on the user's request**:
        - If the task requires logging into a website then you should provide the relavant website and link. The user must provide you with login details.
        - For data extraction from a website: Provide the correct URL and a detailed data extraction prompt. You can aswell scrape the page screenshots 
        - For retrieving information from a profile (e.g., latest model on Hugging Face): Provide the URL and a step-by-step breakdown.
        

        Your task is to give a detailed step by step process to accomplish the task.


        Example Prompts and ```EXPECTED OUTPUT FORMAT```:

        User Prompt:
        " What is the latest model I uploaded? You have my login  credentials username:{{to be provided by user}} and password:{{should be provided by user}}"

            Expected Output:
            {{
                "url": "https://huggingface.co/login",
                "task": "Navigate to Hugging Face and log in with my credentials. Go to my profile and get the name of the latest model I uploaded."
            }}
        User Prompt:
        "Schedule a zoom meeting for me today (26th May 2024) by 5pm. Here are my login details\n email:myemail@example.com \npassword:MySecurePass"

            Expected Output:
            {{
                "url": "https://zoom.us/",
                "task": "Go to Zoom, navigate to the Login page, and create an account for me."
            }}


        REMEBER THAT YOU ARE ONLY MODIFYING USER PROMPT AND NOT PERFORMING THE TASK.

        User Prompt:

        ```{task}```

        ENSURE THAT YOU ADHERE TO ```EXPECTED OUTPUT FORMAT```  AND URL MUST BE ACCURATE. 

        LASTLY ENSURE THE OUTPUT KEYS ARE **url** and **task**. RETURN ONLY THE JSONOUTPU AND NOTHING MORE


        """),
                            
        input_variables=["task"],
        )
        # Choose the LLM to use
        llm = ChatOpenAI(model="gpt-4o")
        new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

        chain = query | llm | new_parser
        response = chain.invoke({"task": task}) 
        print(response)
        
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
        output = agent.run(modified_user_task["task"])
        
        return output
    


if __name__ == "__main__":
    #task_1 worked
    task_1 = "Go on Hugging Face platform, log in with my credentials username:chukypedro15@gmail.com and password:k2%H_h5E@pK7Kgf, and navigate to my profile to get the name of the latest model I uploaded."
    #task_2 worked
    task_2 = "https://relevanceai.com/pricing/", "Extract the pricing info"
    #agent = BrowserAgent()
    #output = agent.execute(task=task_2)
        