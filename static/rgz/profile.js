document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profile-form');
    const deleteBtn = document.getElementById('delete-btn');
    const photoContainer = document.getElementById('profile-photo-container');

    
    loadProfile();

    
    profileForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(profileForm);

        try {
            const response = await fetch('/api/profile', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                return alert(errorData.error || 'Ошибка');
            }

            const data = await response.json();
            alert('Профиль успешно обновлён');

            
            const photoInput = document.getElementById('photo-input');
            if (photoInput && photoInput.files[0]) {
                const user_id = data.user_id || data.profile?.user_id;
                if (user_id) showProfilePhoto(user_id);
            }

        } catch (err) {
            console.error(err);
            alert('Ошибка соединения с сервером');
        }
    });

    
    deleteBtn.addEventListener('click', async () => {
        if (!confirm('Удалить аккаунт?')) return;

        try {
            const response = await fetch('/api/profile', { method: 'DELETE' });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                return alert(errorData.error || 'Ошибка');
            }

            alert('Аккаунт удалён');
            window.location.href = '/rgz/';

        } catch (err) {
            console.error(err);
            alert('Ошибка');
        }
    });

    
    function showProfilePhoto(user_id) {
        photoContainer.innerHTML = '';
        const img = document.createElement('img');
        img.src = `/static/uploads/${user_id}.jpg?${Date.now()}`; 
        img.alt = 'Фото профиля';
        img.style.maxWidth = '200px';
        img.style.display = 'block';
        img.style.marginBottom = '10px';
        photoContainer.appendChild(img);
    }

    
    async function loadProfile() {
        try {
            const response = await fetch('/api/profile');
            if (!response.ok) return;
            const data = await response.json();
            const profile = data.profile;
            if (!profile) return;

            for (const key of ['full_name','age','gender','about','contact']) {
                const input = profileForm.querySelector(`[name="${key}"]`);
                if(input) input.value = profile[key] || '';
            }
            profileForm.querySelector('input[name="is_hidden"]').checked = profile.is_hidden || false;

            if (profile.has_photo) showProfilePhoto(profile.user_id);

        } catch (err) {
            console.error(err);
        }
    }
});
