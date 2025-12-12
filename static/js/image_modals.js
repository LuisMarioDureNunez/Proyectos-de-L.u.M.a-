/**
 * ===== SISTEMA DE MODALES DE IMÁGENES PROFESIONAL =====
 * Funcionalidad similar a Facebook para mostrar imágenes en modales
 * Autor: L.u.M.a System
 * Versión: 2.0
 */

class ImageModalSystem {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createModalStyles();
        console.log('🖼️ Sistema de Modales de Imágenes inicializado');
    }

    // Configurar event listeners
    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            // Imágenes de perfil clickeables
            this.setupProfileImageClicks();
            
            // Logos de empresa clickeables
            this.setupCompanyLogoClicks();
            
            // Efectos de hover
            this.setupHoverEffects();
            
            // Partículas en modales
            this.setupModalParticles();
        });
    }

    // Configurar clicks en imágenes de perfil
    setupProfileImageClicks() {
        const profileImages = document.querySelectorAll('[id*="profileImage"], .profile-avatar, .user-avatar-grande');
        
        profileImages.forEach(img => {
            // Click simple para mostrar modal
            img.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.showProfileModal(img);
            });

            // Doble click para cambiar imagen
            img.addEventListener('dblclick', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.triggerFileInput('avatarInput');
            });

            // Agregar cursor pointer
            img.style.cursor = 'pointer';
        });
    }

    // Configurar clicks en logos de empresa
    setupCompanyLogoClicks() {
        const companyLogos = document.querySelectorAll('[id*="companyLogo"], .company-logo, .logo-grande');
        
        companyLogos.forEach(logo => {
            // Click simple para mostrar modal
            logo.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.showCompanyModal(logo);
            });

            // Doble click para cambiar logo
            logo.addEventListener('dblclick', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.triggerFileInput('logoInput');
            });

            // Agregar cursor pointer
            logo.style.cursor = 'pointer';
        });
    }

    // Mostrar modal de imagen de perfil
    showProfileModal(imgElement) {
        const modalId = 'profileImageModal';
        let modal = document.getElementById(modalId);
        
        if (!modal) {
            modal = this.createProfileModal();
        }

        const modalImg = modal.querySelector('#profileModalImage, .modal-image');
        if (modalImg && imgElement) {
            modalImg.src = imgElement.src || imgElement.style.backgroundImage?.replace(/url\(["']?([^"']*)["']?\)/, '$1');
        }

        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();

        // Crear partículas cuando se abre
        modal.addEventListener('shown.bs.modal', () => {
            this.createModalParticles(modalId);
        });
    }

    // Mostrar modal de logo de empresa
    showCompanyModal(logoElement) {
        const modalId = 'companyLogoModal';
        let modal = document.getElementById(modalId);
        
        if (!modal) {
            modal = this.createCompanyModal();
        }

        const modalImg = modal.querySelector('#companyModalImage, .modal-image');
        if (modalImg && logoElement) {
            modalImg.src = logoElement.src || logoElement.style.backgroundImage?.replace(/url\(["']?([^"']*)["']?\)/, '$1');
        }

        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();

        // Crear partículas cuando se abre
        modal.addEventListener('shown.bs.modal', () => {
            this.createModalParticles(modalId);
        });
    }

    // Crear modal de perfil dinámicamente
    createProfileModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade profile-modal';
        modal.id = 'profileImageModal';
        modal.tabIndex = -1;
        modal.innerHTML = `
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-particles"></div>
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-user-circle me-2 text-warning"></i>Mi Foto de Perfil
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center p-5">
                        <img id="profileModalImage" src="" alt="Foto de Perfil" 
                             class="img-fluid modal-image" 
                             style="max-height: 70vh; border-radius: 20px; box-shadow: 0 20px 60px rgba(255,255,255,0.3);">
                        <div class="mt-4">
                            <button class="btn btn-primary me-2" onclick="document.getElementById('avatarInput')?.click()">
                                <i class="fas fa-camera me-2"></i>Cambiar Foto
                            </button>
                            <button class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times me-2"></i>Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    // Crear modal de empresa dinámicamente
    createCompanyModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade profile-modal';
        modal.id = 'companyLogoModal';
        modal.tabIndex = -1;
        modal.innerHTML = `
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-particles"></div>
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-building me-2 text-warning"></i>Logo de Empresa
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center p-5">
                        <img id="companyModalImage" src="" alt="Logo Empresa" 
                             class="img-fluid modal-image" 
                             style="max-height: 70vh; border-radius: 20px; box-shadow: 0 20px 60px rgba(255,255,255,0.3);">
                        <div class="mt-4">
                            <button class="btn btn-primary me-2" onclick="document.getElementById('logoInput')?.click()">
                                <i class="fas fa-upload me-2"></i>Cambiar Logo
                            </button>
                            <button class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times me-2"></i>Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    // Crear partículas en modales
    createModalParticles(modalId) {
        const modal = document.getElementById(modalId);
        const particlesContainer = modal?.querySelector('.modal-particles');
        
        if (particlesContainer) {
            particlesContainer.innerHTML = '';
            
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'modal-particle';
                particle.style.cssText = `
                    position: absolute;
                    width: ${Math.random() * 6 + 2}px;
                    height: ${Math.random() * 6 + 2}px;
                    background: ${this.getRandomColor()};
                    border-radius: 50%;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation: modalParticleFloat ${Math.random() * 6 + 4}s infinite ease-in-out;
                    animation-delay: ${Math.random() * 4}s;
                    opacity: ${Math.random() * 0.6 + 0.2};
                `;
                particlesContainer.appendChild(particle);
            }
        }
    }

    // Obtener color aleatorio para partículas
    getRandomColor() {
        const colors = [
            'rgba(255, 215, 0, 0.6)',
            'rgba(0, 35, 149, 0.6)', 
            'rgba(255, 102, 0, 0.6)',
            'rgba(64, 224, 208, 0.6)',
            'rgba(255, 255, 255, 0.4)'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    // Configurar efectos de hover
    setupHoverEffects() {
        const clickableImages = document.querySelectorAll('.clickable-image, .profile-avatar, .company-logo, .user-avatar-grande, .logo-grande');
        
        clickableImages.forEach(img => {
            img.addEventListener('mouseenter', () => {
                img.style.transform = 'scale(1.05)';
                img.style.transition = 'all 0.3s ease';
                img.style.boxShadow = '0 15px 40px rgba(0,0,0,0.4)';
            });

            img.addEventListener('mouseleave', () => {
                img.style.transform = 'scale(1)';
                img.style.boxShadow = '';
            });
        });
    }

    // Activar input de archivo
    triggerFileInput(inputId) {
        const input = document.getElementById(inputId);
        if (input) {
            input.click();
        }
    }

    // Configurar partículas en modales
    setupModalParticles() {
        // Agregar event listeners para crear partículas cuando se abren modales
        document.addEventListener('shown.bs.modal', (e) => {
            const modalId = e.target.id;
            if (modalId.includes('Modal')) {
                setTimeout(() => {
                    this.createModalParticles(modalId);
                }, 100);
            }
        });
    }

    // Crear estilos CSS dinámicamente
    createModalStyles() {
        if (document.getElementById('imageModalStyles')) return;

        const style = document.createElement('style');
        style.id = 'imageModalStyles';
        style.textContent = `
            @keyframes modalParticleFloat {
                0%, 100% { 
                    transform: translateY(0px) translateX(0px) rotate(0deg);
                }
                25% { 
                    transform: translateY(-30px) translateX(20px) rotate(90deg);
                }
                50% { 
                    transform: translateY(0px) translateX(40px) rotate(180deg);
                }
                75% { 
                    transform: translateY(30px) translateX(20px) rotate(270deg);
                }
            }

            .modal-particles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
                overflow: hidden;
            }

            .modal-image {
                transition: all 0.3s ease;
                cursor: zoom-in;
            }

            .modal-image:hover {
                transform: scale(1.02);
            }

            .profile-modal .modal-content {
                background: linear-gradient(135deg, rgba(0,35,149,0.95) 0%, rgba(0,0,0,0.95) 100%);
                backdrop-filter: blur(20px);
                border: 2px solid rgba(255,255,255,0.2);
                box-shadow: 0 25px 80px rgba(0,0,0,0.8);
                border-radius: 20px;
            }

            .profile-modal .modal-header {
                background: linear-gradient(90deg, rgba(255,215,0,0.2) 0%, transparent 100%);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }

            .profile-modal .modal-title {
                font-family: 'Orbitron', sans-serif;
                font-weight: 700;
                text-shadow: 0 2px 10px rgba(0,0,0,0.5);
                background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .clickable-image {
                position: relative;
                overflow: hidden;
            }

            .clickable-image::before {
                content: '🔍';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 2rem;
                opacity: 0;
                transition: all 0.3s ease;
                z-index: 2;
                text-shadow: 0 2px 10px rgba(0,0,0,0.8);
            }

            .clickable-image::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                opacity: 0;
                transition: all 0.3s ease;
                z-index: 1;
            }

            .clickable-image:hover::before {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1.2);
            }

            .clickable-image:hover::after {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }

    // Mostrar notificación
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 10000;
            min-width: 300px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: slideInRight 0.5s ease;
        `;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-check-circle me-2"></i>
                ${message}
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOutRight 0.5s ease';
                setTimeout(() => notification.remove(), 500);
            }
        }, 3000);
    }
}

// Funciones globales para compatibilidad
window.showProfileModal = function() {
    const userImage = document.querySelector('#userDropdown img, .user-avatar-grande, .profile-avatar');
    if (userImage && window.imageModalSystem) {
        window.imageModalSystem.showProfileModal(userImage);
    }
};

window.showLogoModal = function() {
    const logoImage = document.querySelector('.logo-grande, .company-logo');
    if (logoImage && window.imageModalSystem) {
        window.imageModalSystem.showCompanyModal(logoImage);
    }
};

// Inicializar sistema cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.imageModalSystem = new ImageModalSystem();
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ImageModalSystem;
}