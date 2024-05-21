# API Server
It should be note that the API server is built using FastAPI as such requires a python environment to run

```bash
pip install -r requirements.txt
```

## Making API calls
#### Sign up a new User

**Bash**\
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/register?username={yourUserName}&password={password}&confirm_password={password}' \
  -H 'accept: application/json' \
  -d ''
```

**Javascript**\
In JavaScript, you can use the fetch API to make an HTTP POST request. Here’s an example:

```javascript
const url = 'http://127.0.0.1:8000/register';
const data = {
    username: '{yourUserName}',
    password: '{password}',
    confirm_password: '{password}'
};

const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data)
});
```

**Python** \
in Python using the requests library.

```python
import requests

url = 'http://127.0.0.1:8000/register'
data = {
    'username': '{yourUserName}',
    'password': '{password}',
    'confirm_password': '{password}'
}
headers = {'accept': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.status_code)
```


#### Sign in for existing User
**Bash**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username={yourUserName}&password={password}&scope=&client_id=&client_secret='
  ```

**Python**\
```python
import requests

url = 'http://127.0.0.1:8000/login'
data = {
    'grant_type': '',
    'username': 'yourUserName',
    'password': '{password}',
    'scope': '',
    'client_id': '',
    'client_secret': ''
}

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, data=data, headers=headers)

print(response.status_code)
print(response.json())  # Assuming the response is in JSON format

```


**Javascript**\
```javascript
const url = 'http://127.0.0.1:8000/login';
const data = new URLSearchParams({
    'grant_type': '',
    'username': 'yourUserName',
    'password': '{password}',
    'scope': '',
    'client_id': '',
    'client_secret': ''
});

const headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
};

fetch(url, {
    method: 'POST',
    headers: headers,
    body: data
});
```


