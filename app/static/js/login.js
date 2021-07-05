window.addEventListener('load', () => {
    let storage = window.sessionStorage;
    let loginButton = document.getElementById('login');
    let username = document.getElementById('username');
    let password = document.getElementById('password');

    loginButton.addEventListener('click', (event) => {
        event.preventDefault();
        data = {
            username: username.value,
            password: password.value
        };
        
        fetch('/login', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => {
            if (response.status == 200){
                return response.json();
            } else {
                alert('Usuário ou senha incorretos!')
            }
        }).then(json => {
            storage.setItem('jwt', json.access_token);
            window.location.replace('/url-list');
        }).catch(error => {
            console.error('Error:', error);
        });
    });
});
