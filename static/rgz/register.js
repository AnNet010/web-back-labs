document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.querySelector('form');
    const photoCheckbox = document.getElementById('add-photo-checkbox');
    const photoBlock = document.getElementById('photo-block');
    const photoInput = document.getElementById('photo-input');

    photoCheckbox.addEventListener('change', () => {
        photoBlock.style.display = photoCheckbox.checked ? 'block' : 'none';
    });

    registerForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        
        const formData = new FormData(registerForm);

        
        formData.set('has_photo', photoCheckbox.checked);

        
        if (photoCheckbox.checked && photoInput.files.length > 0) {
            formData.set('photo', photoInput.files[0]);
        }

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                alert('Регистрация прошла успешно');
                window.location.href = '/rgz/login';
            } else {
                alert(data.error || 'Ошибка регистрации');
            }
        } catch (err) {
            console.error(err);
            alert('Ошибка соединения с сервером');
        }
    });
});
