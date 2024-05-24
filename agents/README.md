### Installing Oython Dependencies

1. create a python virtual environment using conda or virtuenv 
2. cd into `agent` directory and Install poetry 
 -  `pip install poetry` 

```bash
poetry lock
poetry install
```

#### Virtual Env

```bash
poetry shell
```


#### To test the browser_agent

1. Install npm and node
2. Install packages in package.json `npm install`
3. navigate to browser_agent and test the agent.
   - cd to browser agent directory
   - create  a .env file and place your openai apikey in the .env file.
   - run `node web_agent.js ` to interact with the agent.


