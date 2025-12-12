/* ========================================
   BASE SCRIPTS - Sistema L.u.M.a
   JavaScript profesional optimizado
   ======================================== */

$(document).ready(function(){
    // ===== CREAR PARTÍCULAS DINÁMICAS =====
    function createParticles() {
        const container = $('#particles-container');
        for (let i = 0; i < 20; i++) {
            const particle = $('<div class="particle"></div>');
            const size = Math.random() * 15 + 5;
            particle.css({
                width: size + 'px',
                height: size + 'px',
                left: Math.random() * 100 + '%',
                top: Math.random() * 100 + '%',
                animationDelay: Math.random() * 8 + 's'
            });
            container.append(particle);
        }
    }

    // ===== ANIMACIONES GSAP AVANZADAS =====
    function initProfessionalAnimations() {
        if (typeof gsap === 'undefined') return;
        
        gsap.from('.navbar-premium', {
            duration: 1,
            y: -100,
            opacity: 0,
            ease: "power4.out"
        });

        gsap.from('.card-premium', {
            duration: 1,
            y: 80,
            opacity: 0,
            stagger: 0.15,
            ease: "back.out(1.7)",
            delay: 0.3
        });

        gsap.from('.content-card', {
            duration: 1.2,
            scale: 0.8,
            opacity: 0,
            ease: "power3.out",
            delay: 0.5
        });
    }

    // ===== SMOOTH SCROLLING =====
    $('a[href*="#"]').on('click', function(e) {
        const href = $(this).attr('href');
        if (href && href.includes('#')) {
            e.preventDefault();
            const target = $(href.split('#')[1] ? '#' + href.split('#')[1] : 'body');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 800);
            }
        }
    });

    // ===== AUTO-CLOSE ALERTS =====
    setTimeout(function(){
        $('.alert').fadeOut('slow', function() {
            $(this).alert('close');
        });
    }, 6000);

    // ===== HIGHLIGHT ACTIVE SIDEBAR =====
    $('.sidebar-nav .nav-link').each(function(){
        if($(this).attr('href') === window.location.pathname){
            $(this).addClass('active');
        }
    });

    // ===== EFECTO HOVER 3D PARA TARJETAS =====
    $('.card-premium').on('mousemove', function(e) {
        if (typeof gsap === 'undefined') return;
        
        const card = $(this);
        const cardWidth = card.width();
        const cardHeight = card.height();
        const centerX = card.offset().left + cardWidth / 2;
        const centerY = card.offset().top + cardHeight / 2;
        const mouseX = e.pageX - centerX;
        const mouseY = e.pageY - centerY;
        const rotateY = (mouseX / cardWidth) * 15;
        const rotateX = -(mouseY / cardHeight) * 15;
        
        gsap.to(card, {
            duration: 0.3,
            rotationY: rotateY,
            rotationX: rotateX,
            transformPerspective: 800,
            ease: "power2.out"
        });
    });

    $('.card-premium').on('mouseleave', function() {
        if (typeof gsap === 'undefined') return;
        
        gsap.to($(this), {
            duration: 0.5,
            rotationY: 0,
            rotationX: 0,
            ease: "elastic.out(1, 0.5)"
        });
    });

    // ===== INICIALIZAR TODO =====
    createParticles();
    initProfessionalAnimations();

    console.log('🎯 Sistema L.u.M.a cargado correctamente!');
});

// ===== FUNCIONES GLOBALES =====

// Mostrar modal de imagen de perfil
function showProfileModal() {
    const userImage = document.querySelector('#userDropdown img');
    const modalImage = document.getElementById('navbarModalImage');
    
    if (userImage && modalImage) {
        modalImage.src = userImage.src;
        const modal = new bootstrap.Modal(document.getElementById('navbarProfileModal'));
        modal.show();
    }
}

// Mostrar modal del logo
function showLogoModal() {
    const logoImage = document.querySelector('.logo-grande');
    const modalImage = document.getElementById('navbarLogoModalImage');
    
    if (logoImage && modalImage) {
        modalImage.src = logoImage.src;
        const modal = new bootstrap.Modal(document.getElementById('navbarLogoModal'));
        modal.show();
    }
}

// ===== PWA SERVICE WORKER =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('✅ Service Worker registrado:', registration.scope);
            })
            .catch(function(error) {
                console.log('❌ Error registrando Service Worker:', error);
            });
    });
}

// ===== PWA INSTALL PROMPT =====
let deferredPrompt;
const installButton = document.getElementById('pwaInstallButton');

window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    
    setTimeout(() => {
        if (installButton) {
            installButton.classList.add('show');
        }
    }, 3000);
});

if (installButton) {
    installButton.addEventListener('click', function() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            
            deferredPrompt.userChoice.then(function(choiceResult) {
                if (choiceResult.outcome === 'accepted') {
                    console.log('🎉 Usuario instaló la PWA');
                }
                deferredPrompt = null;
                installButton.classList.remove('show');
            });
        }
    });
}

// ===== DETECTAR CONEXIÓN OFFLINE/ONLINE =====
window.addEventListener('online', function() {
    console.log('🌐 Conexión restaurada');
});

window.addEventListener('offline', function() {
    console.log('📡 Sin conexión - Modo offline');
});
