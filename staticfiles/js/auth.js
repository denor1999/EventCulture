document.addEventListener('DOMContentLoaded', function() {
    
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const closeLogin = document.getElementById('closeLogin');
    const closeRegister = document.getElementById('closeRegister');

    function openModal(modal) {
        modal.style.display = 'block';
    }

    function closeModal(modal) {
        modal.style.display = 'none';
    }

    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            openModal(loginModal);
        });
    }

    if (registerBtn) {
        registerBtn.addEventListener('click', function() {
            openModal(registerModal);
        });
    }

    if (closeLogin) {
        closeLogin.addEventListener('click', function() {
            closeModal(loginModal);
        });
    }

    if (closeRegister) {
        closeRegister.addEventListener('click', function() {
            closeModal(registerModal);
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === loginModal) {
            closeModal(loginModal);
        }
        if (event.target === registerModal) {
            closeModal(registerModal);
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (loginModal.style.display === 'block') {
                closeModal(loginModal);
            }
            if (registerModal.style.display === 'block') {
                closeModal(registerModal);
            }
        }
    });

});