/**
 * Dark Mode Toggle (Phase 104)
 * Persists theme preference to localStorage
 * Default: Dark mode
 */

(function() {
  const THEME_KEY = 'echopilot-theme';
  
  // Get saved theme or default to dark
  function getTheme() {
    return localStorage.getItem(THEME_KEY) || 'dark';
  }
  
  // Set theme and persist
  function setTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
    applyTheme(theme);
  }
  
  // Apply theme to body
  function applyTheme(theme) {
    if (theme === 'light') {
      document.body.classList.add('light-mode');
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    } else {
      document.body.classList.remove('light-mode');
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
    }
    
    // Update toggle button if exists
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
      toggleBtn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    }
  }
  
  // Toggle between themes
  function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }
  
  // Apply saved theme immediately (before page renders)
  applyTheme(getTheme());
  
  // Expose global functions
  window.EchoPilotTheme = {
    get: getTheme,
    set: setTheme,
    toggle: toggleTheme
  };
  
  // Auto-initialize toggle button when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initToggleButton);
  } else {
    initToggleButton();
  }
  
  function initToggleButton() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
      applyTheme(getTheme());  // Update button state
    }
  }
})();
