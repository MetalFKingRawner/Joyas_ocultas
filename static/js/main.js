// Menú móvil
const menuToggle = document.getElementById('menuToggle');
const mainNav = document.getElementById('mainNav');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        mainNav.classList.toggle('jo-nav-open');
    });
}

// Animación de aparición al hacer scroll
const revealElements = document.querySelectorAll('.jo-reveal');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('jo-visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });

revealElements.forEach(el => observer.observe(el));