document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    
    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const login = document.querySelector('input[name="login"]').value;
        const password = document.querySelector('input[name="password"]').value;

        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                login,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = '/rgz/'; 
        } else {
            alert(data.error || 'Что-то пошло не так');
        }
    });
});