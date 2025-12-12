/**
 * ===== SISTEMA DE GESTIÓN AVANZADA - JAVASCRIPT =====
 * Funcionalidades y animaciones para todos los paneles
 * Colores: Azul Francia, Naranja, Negro
 */

class GestionAvanzada {
    constructor() {
        this.init();
    }

    init() {
        this.setupAnimations();
        this.setupInteractions();
        this.createParticles();
        this.initCounters();
        console.log('🚀 Sistema de Gestión Avanzada inicializado');
    }

    // Configurar animaciones de entrada
    setupAnimations() {
        // Animar tarjetas al cargar
        const cards = document.querySelectorAll('.contratista-card, .empleado-card, .proveedor-card, .propietario-card, .contrato-card, .propiedad-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Animar estadísticas
        const statsCards = document.querySelectorAll('.stats-card, .stats-empleados, .stats-proveedores, .stats-propietarios, .stats-contratos, .stats-propiedades');
        statsCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.8)';
            setTimeout(() => {
                card.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, index * 150);
        });
    }

    // Configurar interacciones
    setupInteractions() {
        // Efecto hover mejorado para tarjetas
        const cards = document.querySelectorAll('.contratista-card, .empleado-card, .proveedor-card, .propietario-card, .contrato-card, .propiedad-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.addHoverEffect(card);
            });
            
            card.addEventListener('mouseleave', () => {
                this.removeHoverEffect(card);
            });
        });

        // Botones con efectos de ripple
        const buttons = document.querySelectorAll('.btn-francia, .floating-action');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e, button);
            });
        });

        // Tooltips dinámicos
        this.setupTooltips();
    }

    // Agregar efecto hover
    addHoverEffect(element) {
        element.style.transform = 'translateY(-8px) scale(1.02)';
        element.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        
        // Agregar partículas al hover
        this.createHoverParticles(element);
    }

    // Remover efecto hover
    removeHoverEffect(element) {
        element.style.transform = 'translateY(0) scale(1)';
        element.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
    }

    // Crear efecto ripple en botones
    createRippleEffect(event, button) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Crear partículas de fondo
    createParticles() {
        const heroSections = document.querySelectorAll('.contratistas-hero, .empleados-hero, .proveedores-hero, .propietarios-hero, .contratos-hero, .propiedades-hero');
        
        heroSections.forEach(hero => {
            const particlesContainer = document.createElement('div');
            particlesContainer.className = 'particles-bg';
            hero.appendChild(particlesContainer);
            
            for (let i = 0; i < 15; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 8 + 's';
                particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
                particlesContainer.appendChild(particle);
            }
        });
    }

    // Crear partículas en hover
    createHoverParticles(element) {
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: #FF6600;
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                left: ${Math.random() * element.offsetWidth}px;
                top: ${Math.random() * element.offsetHeight}px;
                animation: hover-particle 1s ease-out forwards;
            `;
            
            element.style.position = 'relative';
            element.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 1000);
        }
    }

    // Inicializar contadores animados
    initCounters() {
        const counters = document.querySelectorAll('.stats-card h3, .stats-empleados h3, .stats-proveedores h3, .stats-propietarios h3, .stats-contratos h3, .stats-propiedades h3');
        
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }

    // Animar contador
    animateCounter(element) {
        const target = parseInt(element.textContent) || parseFloat(element.textContent) || 0;
        const isFloat = element.textContent.includes('.');
        let current = 0;
        const increment = target / 50;
        const duration = 2000;
        const stepTime = duration / 50;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            if (isFloat) {
                element.textContent = current.toFixed(1);
            } else {
                element.textContent = Math.floor(current);
            }
        }, stepTime);
    }

    // Configurar tooltips
    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target);
            });
            
            element.addEventListener('mouseleave', (e) => {
                this.hideTooltip(e.target);
            });
        });
    }

    // Mostrar tooltip
    showTooltip(element) {
        const tooltip = document.createElement('div');
        const text = element.getAttribute('data-tooltip');
        
        tooltip.className = 'custom-tooltip-popup';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            white-space: nowrap;
            z-index: 10000;
            pointer-events: none;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        
        setTimeout(() => {
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';
        }, 10);
        
        element._tooltip = tooltip;
    }

    // Ocultar tooltip
    hideTooltip(element) {
        if (element._tooltip) {
            element._tooltip.style.opacity = '0';
            element._tooltip.style.transform = 'translateY(10px)';
            setTimeout(() => {
                if (element._tooltip) {
                    element._tooltip.remove();
                    delete element._tooltip;
                }
            }, 300);
        }
    }

    // Mostrar notificación
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'} me-2"></i>
                ${message}
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'linear-gradient(45deg, #28a745, #20c997)' : 
                        type === 'error' ? 'linear-gradient(45deg, #dc3545, #c82333)' : 
                        'linear-gradient(45deg, #002395, #FF6600)'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 10000;
            transform: translateX(100%);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 400);
        }, 3000);
    }

    // Filtrar elementos
    filterElements(searchTerm, containerSelector) {
        const container = document.querySelector(containerSelector);
        const elements = container.querySelectorAll('.contratista-card, .empleado-card, .proveedor-card, .propietario-card, .contrato-card, .propiedad-card');
        
        elements.forEach(element => {
            const text = element.textContent.toLowerCase();
            const matches = text.includes(searchTerm.toLowerCase());
            
            element.style.transition = 'all 0.4s ease';
            if (matches) {
                element.style.opacity = '1';
                element.style.transform = 'scale(1)';
                element.style.display = 'block';
            } else {
                element.style.opacity = '0';
                element.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    if (element.style.opacity === '0') {
                        element.style.display = 'none';
                    }
                }, 400);
            }
        });
    }
}

// Agregar estilos CSS dinámicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes hover-particle {
        0% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-20px) scale(0);
        }
    }
    
    .notification {
        font-weight: 600;
        border-left: 4px solid rgba(255,255,255,0.5);
    }
    
    .custom-tooltip-popup {
        font-family: 'Inter', sans-serif;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
`;
document.head.appendChild(style);

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.gestionAvanzada = new GestionAvanzada();
});

// Funciones globales para uso en templates
window.showNotification = function(message, type = 'success') {
    if (window.gestionAvanzada) {
        window.gestionAvanzada.showNotification(message, type);
    }
};

window.filterElements = function(searchTerm, containerSelector = '.container-fluid') {
    if (window.gestionAvanzada) {
        window.gestionAvanzada.filterElements(searchTerm, containerSelector);
    }
};