document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');

    if (!resultsContainer) return;

    resultsContainer.addEventListener('click', async (e) => {
        if (!e.target.classList.contains('delete-btn')) return;

        const card = e.target.closest('.profile-card');
        const userId = card.dataset.userId;

        if (!confirm('Вы действительно хотите удалить этого пользователя из лайков?')) return;

        try {
            const response = await fetch(`/api/unlike/${userId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (response.ok) {
                card.remove();
            } else {
                alert(data.error || 'Ошибка при удалении лайка');
            }
        } catch (err) {
            console.error(err);
            alert('Ошибка соединения с сервером');
        }
    });
});
