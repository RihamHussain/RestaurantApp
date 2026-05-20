document.addEventListener('DOMContentLoaded', function() {
    updateNavbar();
});

async function updateNavbar() {
    const loggedOutDiv = document.getElementById('auth-links-logged-out');
    const loggedInDiv = document.getElementById('auth-links-logged-in');
    const usernameSpan = document.getElementById('display-username');
    const adminLink = document.getElementById('admin-only-link');
    const adminCard = document.getElementById('admin-card');

    try {
        const response = await fetch('/auth/me', { credentials: 'include' });
        
        if (response.ok) {
            const user = await response.json();
            
            if (loggedOutDiv) loggedOutDiv.classList.add('d-none');
            if (loggedInDiv) loggedInDiv.classList.remove('d-none');
            if (usernameSpan) usernameSpan.innerText = user.username;

            // Include is_superadmin in the visual UI check
            if (user.role === 'admin' || user.is_superadmin) {
                if (adminLink) adminLink.classList.remove('d-none');
                if (adminCard) adminCard.classList.remove('d-none');
            }
        } else {
            showLoggedOutUI();
        }
    } catch (e) {
        console.error("Auth check failed", e);
        showLoggedOutUI();
    }
}

function showLoggedOutUI() {
    document.getElementById('auth-links-logged-out')?.classList.remove('d-none');
    document.getElementById('auth-links-logged-in')?.classList.add('d-none');
    document.getElementById('admin-only-link')?.classList.add('d-none');
    document.getElementById('admin-card')?.classList.add('d-none');
}

async function logout() {
    await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
    window.location.href = '/auth/login';
}