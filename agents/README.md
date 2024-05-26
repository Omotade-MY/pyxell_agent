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

1. create an instance of the class  `BrowserAgent`
2. call the `.execute` method and pass in your text e.g **Go to any football platform and get me the last english premiership scores.**
3. The final from the should be a list of string.


