/**
 * base.js - Shared Utilities
 */

function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');
    if (input.type === "password") {
        input.type = "text";
        icon.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        input.type = "password";
        icon.classList.replace('bi-eye-slash', 'bi-eye');
    }
}

function showAlert(elementId, message, type = 'danger') {
    const alertBox = document.getElementById(elementId);
    if (!alertBox) return;
    alertBox.className = `alert alert-${type}`;
    alertBox.innerText = message;
    alertBox.classList.remove('d-none');
}

document.addEventListener('DOMContentLoaded', () => {
    const yearSpan = document.getElementById('year');
    if (yearSpan) yearSpan.textContent = new Date().getFullYear();
});

async function logout() {
    await fetch('/auth/logout', { method: 'POST' });
    window.location.href = '/auth/login';
}