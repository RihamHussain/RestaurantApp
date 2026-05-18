document.addEventListener('DOMContentLoaded', function() {
    updateNavbar();
});

function updateNavbar() {
    const token = localStorage.getItem('access_token');
    const loggedOutDiv = document.getElementById('auth-links-logged-out');
    const loggedInDiv = document.getElementById('auth-links-logged-in');
    const usernameSpan = document.getElementById('display-username');
    const adminLink = document.getElementById('admin-only-link');
    const adminCard = document.getElementById('admin-card'); // The card in the middle of the home page

    if (token) {
        if (loggedOutDiv) loggedOutDiv.classList.add('d-none');
        if (loggedInDiv) loggedInDiv.classList.remove('d-none');

        try {
            // Robust JWT decoding
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const payload = JSON.parse(window.atob(base64));
            
            if (usernameSpan) usernameSpan.innerText = payload.sub;

            // Check if user is admin
            if (payload.role === 'admin') {
                if (adminLink) adminLink.classList.remove('d-none');
                if (adminCard) adminCard.classList.remove('d-none');
            }
        } catch (e) {
            console.error("Token decoding failed", e);
            logout();
        }
    } else {
        if (loggedOutDiv) loggedOutDiv.classList.remove('d-none');
        if (loggedInDiv) loggedInDiv.classList.add('d-none');
        if (adminLink) adminLink.classList.add('d-none');
        if (adminCard) adminCard.classList.add('d-none');
    }
}

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/auth/login';
}