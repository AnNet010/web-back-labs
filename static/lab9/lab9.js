document.addEventListener('DOMContentLoaded', function() {
    const giftBoxes = document.querySelectorAll('.gift-box');
    const modal = document.getElementById('congratulation-modal');
    const overlay = document.getElementById('modal-overlay');
    const errorMessage = document.getElementById('error-message');
    const openedCountElement = document.getElementById('opened-count');
    const remainingCountElement = document.getElementById('remaining-count');
    
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 3000);
    }
    
    function openModal(congratulation, giftImage) {
        document.getElementById('congratulation-text').textContent = congratulation;
        document.getElementById('gift-image').src = giftImage;
        modal.style.display = 'block';
        overlay.style.display = 'block';
    }
    
    window.closeModal = function() {
        modal.style.display = 'none';
        overlay.style.display = 'none';
    };
    
    overlay.addEventListener('click', closeModal);
    
    giftBoxes.forEach(box => {
        box.addEventListener('click', function() {
            const boxId = this.dataset.boxId;
            
            if (this.classList.contains('opened')) {
                showError('Эта коробка уже открыта!');
                return;
            }
            
            fetch('/lab9/open_box', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    box_id: parseInt(boxId)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                if (data.success) {
                    this.classList.add('opened');
                    openedCountElement.textContent = data.opened;
                    remainingCountElement.textContent = data.remaining;
                    openModal(data.congratulation, data.gift);
                    this.querySelector('img').style.opacity = '0.5';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Произошла ошибка при открытии коробки');
            });
        });
    });
    
    window.callSanta = function() {
        fetch('/lab9/santa', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                showError('Произошла ошибка');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Произошла ошибка');
        });
    };
    
    window.resetGame = function() {
        fetch('/lab9/reset', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else if (data.error) {
                showError(data.error);
            } else {
                showError('Произошла ошибка при сбросе игры');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Произошла ошибка при сбросе игры');
        });
    };
});