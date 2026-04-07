// static/js/theme.js
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const root = document.documentElement;

    // Check localStorage for saved theme, default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    root.setAttribute('data-theme', currentTheme);
    updateIcon(currentTheme);

    if(toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            let targetTheme = 'light';
            if (root.getAttribute('data-theme') === 'light') {
                targetTheme = 'dark';
            }
            
            root.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
            updateIcon(targetTheme);
        });
    }

    function updateIcon(theme) {
        if(!toggleBtn) return;
        if (theme === 'dark') {
            toggleBtn.innerHTML = '<i class="bi bi-sun-fill"></i>';
        } else {
            toggleBtn.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
        }
    }
});
