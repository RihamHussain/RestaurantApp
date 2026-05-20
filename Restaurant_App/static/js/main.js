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
        // ASK THE SERVER FOR USER INFO (Since we can't read cookies directly)
        const response = await fetch('/auth/me', { credentials: 'include' });

        
        if (response.ok) {
            const user = await response.json(); // user = {username, role, ...}
            
            if (loggedOutDiv) loggedOutDiv.classList.add('d-none');
            if (loggedInDiv) loggedInDiv.classList.remove('d-none');
            if (usernameSpan) usernameSpan.innerText = user.username;

            // Check if user is admin
            if (user.role === 'admin') {
                if (adminLink) adminLink.classList.remove('d-none');
                if (adminCard) adminCard.classList.remove('d-none');
            }
        } else {
            // Not logged in or session expired
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

// Global logout function
async function logout() {
    await fetch('/auth/logout', { method: 'POST' });
    window.location.href = '/auth/login';
}