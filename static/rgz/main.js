document.addEventListener('DOMContentLoaded', function() {
    console.log('index.js загружен'); 
    
    const logoutBtn = document.getElementById('logout-btn');
    
    if (logoutBtn) {
        console.log('Кнопка выхода найдена');
        
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            console.log('Клик по кнопке выхода');
            
            try {
                const response = await fetch('/api/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                const data = await response.json();
                console.log('Ответ от API:', data);
                
                if (response.ok) {
                    alert('Вы успешно вышли из системы');
                    window.location.href = '/rgz/';
                } else {
                    alert(data.error || 'Ошибка при выходе');
                }
            } catch (error) {
                console.error('Ошибка при выходе:', error);
                alert('Ошибка соединения с сервером');
            }
        });
    } else {
        console.log('Кнопка выхода не найдена (возможно, пользователь не авторизован)');
    }
});