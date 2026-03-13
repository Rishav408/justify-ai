// Theme Management System

class ThemeManager {
    constructor() {
        this.themeKey = 'justify-ai-theme';
        this.currentTheme = this.getSavedTheme() || 'light';
    }

    init() {
        // Apply saved theme on page load
        this.applyTheme(this.currentTheme);
        
        // Set up event listener for theme toggle button
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggle());
            this.updateToggleIcon();
        }
    }

    toggle() {
        // Switch between light and dark themes
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        this.saveTheme(this.currentTheme);
        this.updateToggleIcon();
    }

    applyTheme(theme) {
        // Apply theme to document root
        document.documentElement.setAttribute('data-theme', theme);
    }

    saveTheme(theme) {
        // Persist theme preference in localStorage
        localStorage.setItem(this.themeKey, theme);
    }

    getSavedTheme() {
        // Retrieve saved theme from localStorage
        return localStorage.getItem(this.themeKey);
    }

    updateToggleIcon() {
        // Update the icon based on current theme
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        const sunIcon = themeToggle.querySelector('.sun-icon');
        const moonIcon = themeToggle.querySelector('.moon-icon');

        if (this.currentTheme === 'dark') {
            // Show sun icon in dark mode (to switch to light)
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        } else {
            // Show moon icon in light mode (to switch to dark)
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        }
    }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const themeManager = new ThemeManager();
    themeManager.init();
});
