/* ==========================================================================
   File: modal-carousel.js
   Purpose: Modal carousel for artwork mockups on the edit listing page
   Sections:
   [MC.1] Carousel Setup and Accessibility
   [MC.2] Form Action Helpers
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('carousel-modal');
    if (!modal) return;

    const imgEl = modal.querySelector('#carousel-img');
    const prevBtn = modal.querySelector('.carousel-nav.left');
    const nextBtn = modal.querySelector('.carousel-nav.right');
    const closeBtn = modal.querySelector('.carousel-close');
    const counterEl = modal.querySelector('#carousel-counter');

    const focusSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    let focusableEls = [];
    let currentIndex = 0;
    let touchStartX = 0;
    let lastFocus = null;

    const thumbEls = Array.from(document.querySelectorAll('.mockup-grid .mockup-thumb'));
    const mainImg = document.querySelector('.hero-image img');
    const images = mainImg ? [mainImg.src, ...thumbEls.map(el => el.src)] : thumbEls.map(el => el.src);

    function update() {
        imgEl.src = images[currentIndex];
        imgEl.alt = `Mockup Preview ${currentIndex + 1}`;
        if (counterEl) counterEl.textContent = `${currentIndex + 1} / ${images.length}`;
        thumbEls.forEach(t => t.classList.remove('current'));
        if (thumbEls[currentIndex]) {
            thumbEls[currentIndex].classList.add('current');
        }
    }

    function open(index = 0, triggerEl = null) {
        lastFocus = triggerEl || document.activeElement;
        currentIndex = index;
        update();
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        focusableEls = modal.querySelectorAll(focusSelector);
        closeBtn.focus();
    }

    function close() {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        if (lastFocus) {
            lastFocus.focus();
        }
    }

    function next() { if (currentIndex < images.length - 1) { currentIndex++; update(); } }
    function prev() { if (currentIndex > 0) { currentIndex--; update(); } }

    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);
    closeBtn.addEventListener('click', close);

    modal.addEventListener('click', e => { if (e.target === modal) close(); });
    modal.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
    modal.addEventListener('touchend', e => {
        const diff = e.changedTouches[0].clientX - touchStartX;
        if (diff > 50) prev();
        if (diff < -50) next();
    });

    document.addEventListener('keydown', e => {
        if (!modal.classList.contains('active')) return;
        if (e.key === 'Escape') { close(); }
        else if (e.key === 'ArrowRight') { next(); }
        else if (e.key === 'ArrowLeft') { prev(); }
        else if (e.key === 'Tab') {
            const first = focusableEls[0];
            const last = focusableEls[focusableEls.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault(); last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault(); first.focus();
            }
        }
    });

    if (mainImg) {
        mainImg.addEventListener('click', () => open(0, mainImg));
        mainImg.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(0, mainImg);
            }
        });
    }
    thumbEls.forEach((thumb, idx) => {
        const index = idx + 1;
        thumb.addEventListener('click', () => open(index, thumb));
        thumb.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(index, thumb);
            }
        });
    });

    // === [MC.2] Form Action Helpers ===
    function toggleActionBtns() {
        const txt = document.querySelector('textarea[name="images"]');
        const disabled = !(txt && txt.value.trim());
        document.querySelectorAll('.require-images').forEach(btn => { btn.disabled = disabled; });
    }
    const imagesTextarea = document.querySelector('textarea[name="images"]');
    if (imagesTextarea) imagesTextarea.addEventListener('input', toggleActionBtns);
    toggleActionBtns();

    document.querySelectorAll('.lock-form').forEach(f => {
        f.addEventListener('submit', () => {
            const r = prompt('Reason for lock/unlock? (optional)');
            if (r !== null) f.querySelector('input[name="reason"]').value = r;
        });
    });

    const deleteBtn = document.querySelector('.delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', e => {
            if (!confirm('Delete this artwork and all files?')) {
                e.preventDefault();
            }
        });
    }
});
