async function registerUser() {
    const url = 'http://127.0.0.1:8000/register';
    const data = new URLSearchParams({
        username: 'newuser',
        password: 'newpass',
        confirm_password: 'newpass'
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

async function loginUser() {
    const url = 'http://127.0.0.1:8000/login';
    const data = new URLSearchParams({
        username: 'newuser',
        password: 'newpass'
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

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvbW90YWRlIiwiZXhwIjoxNzE2NzM0NzE4fQ.eS_T8sYbcysQ2c3ld6ndhSwsdoh7_cCptMoz_miP-JI";  // Replace with the actual token obtained from login
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

