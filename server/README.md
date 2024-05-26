# API Server
It should be note that the API server is built using FastAPI as such requires a python environment to run

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --reload
```

## Making API calls
#### Sign up a new User

**Javascript**\
In JavaScript, you can use the fetch API to make an HTTP POST request. Here’s an example:

```javascript
async function registerUser() {
    const url = 'http://127.0.0.1:8000/register';
    const data = new URLSearchParams({
        username: 'yourUserName',
        password: 'salam',
        confirm_password: 'salam'
    });

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data
    });

    const result = await response.json();
    console.log(response.status, result);
}

registerUser();

```

**Python** \
in Python using the requests library.

```python
import requests

import requests

url = 'http://127.0.0.1:8000/register'
data = {
    'username': 'Your Username',
    'password': 'salam',
    'confirm_password': 'salam'
}

response = requests.post(url, data=data)
print(response.status_code, response.json())

```


#### Sign in for existing User

**Python**\
```python
import requests

url = 'http://127.0.0.1:8000/login'
data = {
    'username': 'your User name',
    'password': 'salam'
}

response = requests.post(url, data=data)
print(response.status_code, response.json())
token = response.json().get('token')

```

```javascript

async function loginUser() {
    const url = 'http://127.0.0.1:8000/login';
    const data = new URLSearchParams({
        username: 'Your User Name',
        password: 'salam'
    });

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data
    });

    const result = await response.json();
    console.log(response.status, result);
    return result.token;
}

loginUser().then(token => console.log(token));
```


## Sending Request to chat endpoint
```javascript
const token = 'oken_here';  // Replace with the actual token obtained from login
const prompt = "Extract the prices of all commodities on the africaexchange website";
const url = "http://127.0.0.1:8000/chat/";

const data = new URLSearchParams({
  'prompt': prompt
});

fetch(url, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: data
})
.then(response => {
  console.log('Status:', response.status);
  return response.json();
})
.then(data => {
  console.log('Response:', data);
})
.catch(error => {
  console.error('Error:', error);
});
```


