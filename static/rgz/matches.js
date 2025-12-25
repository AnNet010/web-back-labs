document.addEventListener('DOMContentLoaded', async () => {
    const resultsContainer = document.getElementById('results-container');

    async function loadLikes() {
        try {
            const response = await fetch('/api/my_likes');
            const data = await response.json();

            if (!response.ok) {
                resultsContainer.innerHTML = `<div class="no-results"><p>${data.error || 'Ошибка при загрузке лайков'}</p></div>`;
                return;
            }

            if (data.results && data.results.length > 0) {
                resultsContainer.innerHTML = '';

                const counter = document.createElement('p');
                counter.innerHTML = `<strong>Найдено лайков: ${data.results.length}</strong>`;
                resultsContainer.appendChild(counter);

                data.results.forEach(profile => {
                    const card = document.createElement('div');
                    card.className = 'profile-card';
                    card.dataset.userId = profile.user_id;

                    card.innerHTML = `
                        <div style="flex-grow: 1;">
                            <div style="margin-bottom: 10px;">
                                <strong style="font-size: 1.2em; color: #1e3a8a;">${profile.full_name}</strong>
                                <span style="background: #e0e7ff; padding: 4px 10px; border-radius: 15px; float: right;">
                                    ${profile.age} лет
                                </span>
                            </div>
                            <div style="color: #6b7280; margin-bottom: 10px;">
                                Пол: ${profile.gender}
                            </div>
                            <div>
                                ${profile.about || '<em>Нет информации о себе</em>'}
                            </div>
                        </div>
                        <button class="delete-btn" style="
                            margin-left: 10px;
                            padding: 6px 12px;
                            background: #ef4444;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            cursor: pointer;
                        ">Удалить</button>
                    `;

                    resultsContainer.appendChild(card);
                });

            } else {
                resultsContainer.innerHTML = '<div class="no-results"><p>Вы ещё не ставили лайки</p></div>';
            }
        } catch (error) {
            console.error(error);
            resultsContainer.innerHTML = '<div class="no-results"><p>Ошибка соединения с сервером</p></div>';
        }
    }

    resultsContainer.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const card = e.target.closest('.profile-card');
            const toUserId = card.dataset.userId;

            if (!confirm('Вы уверены, что хотите удалить этот лайк?')) return;

            try {
                const res = await fetch('/api/unlike', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to_user_id: toUserId})
                });
                const data = await res.json();

                if (res.ok) {
                    card.remove();

                    if (resultsContainer.querySelectorAll('.profile-card').length === 0) {
                        resultsContainer.innerHTML = '<p>Вы пока никому не ставили лайки.</p>';
                    }
                } else {
                    alert(data.error || 'Ошибка при удалении лайка');
                }
            } catch (err) {
                console.error(err);
                alert('Ошибка соединения с сервером');
            }
        }
    });

    loadLikes();
});
