async function registerUser() {
    const url = 'http://127.0.0.1:8000/register';
    const data = new URLSearchParams({
        username: 'jelila',
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
