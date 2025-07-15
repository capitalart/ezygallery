/* ==========================================================================
   File: script.js
   Purpose: Handles interactive logic for the menu and theme toggling.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const bodyTag = document.body;
    const htmlTag = document.documentElement;

    // === [ THEME TOGGLE LOGIC ] ===
    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    const userIcon = document.getElementById("userIcon");
    const userAuthLink = document.getElementById("userAuthLink");

    const icons = {
        sun: 'static/icons/svg/light/sun-light.svg',
        moon: 'static/icons/svg/light/moon-light.svg',
        user: 'static/icons/svg/light/user-circle-light.svg',
        userChecked: 'static/icons/svg/light/user-circle-check-light.svg'
    };

    const setTheme = (isDark) => {
        htmlTag.classList.toggle('dark', isDark);
        if (themeIcon) themeIcon.src = isDark ? icons.sun : icons.moon;
        localStorage.setItem('darkMode', isDark);
    };

    const savedThemeIsDark = localStorage.getItem('darkMode') === 'true';
    setTheme(savedThemeIsDark);

    const toggleTheme = () => {
        const isCurrentlyDark = htmlTag.classList.contains('dark');
        setTheme(!isCurrentlyDark);
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    
    let isLoggedIn = false;
    const toggleLogin = (e) => {
        e.preventDefault();
        isLoggedIn = !isLoggedIn;
        if (userIcon) userIcon.src = isLoggedIn ? icons.userChecked : icons.user;
    };

    if (userAuthLink) userAuthLink.addEventListener('click', toggleLogin);


    // === [ OVERLAY MENU LOGIC ] ===
    const menuToggle = document.getElementById("menuToggle");
    const overlayMenu = document.getElementById("overlayMenu");
    const overlayClose = document.getElementById("overlayClose");

    let focusableElements = [];
    const focusableSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

    const openMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.add("is-active");
        overlayMenu.setAttribute('aria-hidden', 'false');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'true');
        htmlTag.classList.add('overlay-open');
        bodyTag.style.overflow = 'hidden';
        focusableElements = overlayMenu.querySelectorAll(focusableSelector);
        if (overlayClose) overlayClose.focus();
    };

    const closeMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.remove("is-active");
        overlayMenu.setAttribute('aria-hidden', 'true');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
        htmlTag.classList.remove('overlay-open');
        bodyTag.style.overflow = '';
        if (menuToggle) menuToggle.focus();
    };

    if (menuToggle) menuToggle.addEventListener("click", openMenu);
    if (overlayClose) overlayClose.addEventListener("click", closeMenu);

    if (overlayMenu) {
        overlayMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
        overlayMenu.addEventListener('click', (event) => {
            const content = overlayMenu.querySelector('.overlay-content');
            if (!content.contains(event.target)) {
                closeMenu();
            }
        });
    }

    const handleTabTrap = (event) => {
        if (!overlayMenu.classList.contains('is-active')) return;
        const first = focusableElements[0];
        const last = focusableElements[focusableElements.length - 1];
        if (event.key === 'Tab') {
            if (event.shiftKey) {
                if (document.activeElement === first) {
                    event.preventDefault();
                    last.focus();
                }
            } else {
                if (document.activeElement === last) {
                    event.preventDefault();
                    first.focus();
                }
            }
        }
    };

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlayMenu.classList.contains('is-active')) {
            closeMenu();
        }
        handleTabTrap(event);
    });
});
