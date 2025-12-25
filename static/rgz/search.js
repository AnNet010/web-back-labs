document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    let currentOffset = 0;
    let currentName = '';
    let currentAge = '';

    
    async function performSearch() {
        const params = new URLSearchParams();
        if (currentName) params.append('name', currentName);
        if (currentAge) params.append('age', currentAge);
        params.append('offset', currentOffset);

        try {
            const response = await fetch(`/api/search?${params.toString()}`);
            const data = await response.json();

            resultsContainer.innerHTML = '';

            
            if (response.ok && data.results.length > 0) {
                data.results.forEach(profile => {
                    const card = document.createElement('div');
                    card.className = 'profile-card';

                    const btnText = profile.liked ? '✓ Лайк отправлен' : '❤ Лайк';
                    const disabled = profile.liked ? 'disabled' : '';

                    const photoUrl = `/static/uploads/${profile.user_id}.jpg`;

                    card.innerHTML = `
                        <img src="${photoUrl}" alt="Фото профиля"
                             onerror="this.src='/static/default_user.png';"
                             class="profile-photo">
                        <div class="profile-info">
                            <div class="profile-name">${profile.full_name}</div>
                            <div class="profile-details">
                                <span>Возраст: ${profile.age}</span>
                                <span>Пол: ${profile.gender}</span>
                            </div>
                            <div class="profile-about">${profile.about || 'Нет информации о себе'}</div>
                            <button class="like-btn" data-user-id="${profile.user_id}" ${disabled}>${btnText}</button>
                        </div>
                    `;
                    resultsContainer.appendChild(card);
                });
            } else {
                resultsContainer.innerHTML = '<p>Анкеты не найдены</p>';
            }

            
            const navContainer = document.createElement('div');
            navContainer.className = 'nav-buttons';

            if (currentOffset > 0) {
                const prevBtn = document.createElement('button');
                prevBtn.className = 'prev-btn';
                prevBtn.textContent = '← Назад';
                navContainer.appendChild(prevBtn);
            }

            if (data.results.length === 3) {
                const nextBtn = document.createElement('button');
                nextBtn.className = 'next-btn';
                nextBtn.textContent = 'Следующие →';
                navContainer.appendChild(nextBtn);
            }

            if (navContainer.children.length > 0) {
                resultsContainer.appendChild(navContainer);
            }

        } catch (err) {
            console.error(err);
            resultsContainer.innerHTML = '<p>Ошибка соединения с сервером</p>';
        }
    }

    
    searchForm.addEventListener('submit', async e => {
        e.preventDefault();
        currentOffset = 0;
        currentName = document.querySelector('input[name="name"]').value;
        currentAge = document.querySelector('input[name="age"]').value;
        await performSearch();
    });

    
    resultsContainer.addEventListener('click', async e => {
        if (e.target.classList.contains('next-btn')) {
            currentOffset += 3;
            await performSearch();
        } else if (e.target.classList.contains('prev-btn')) {
            currentOffset = Math.max(0, currentOffset - 3);
            await performSearch();
        } else if (e.target.classList.contains('like-btn')) {
            const toUserId = e.target.dataset.userId;
            try {
                const res = await fetch('/api/like', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ to_user_id: toUserId })
                });
                const data = await res.json();
                if (res.ok) {
                    e.target.textContent = data.match ? '💚 Совпадение!' : '✓ Лайк отправлен';
                    e.target.disabled = true;
                } else {
                    alert(data.error || 'Ошибка при отправке лайка');
                }
            } catch (err) {
                console.error(err);
                alert('Ошибка соединения с сервером');
            }
        }
    });
});
