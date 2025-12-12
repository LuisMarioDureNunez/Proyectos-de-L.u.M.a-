// MEJORAS INTERACTIVAS PARA LA TIENDA

document.addEventListener('DOMContentLoaded', function() {
    // Animación para las cards al cargar
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Efecto de confirmación para eliminar
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Mostrar/ocultar contraseña en login
    const passwordInput = document.getElementById('id_password');
    if (passwordInput) {
        const togglePassword = document.createElement('button');
        togglePassword.type = 'button';
        togglePassword.innerHTML = '<i class="fas fa-eye"></i>';
        togglePassword.className = 'btn btn-outline-secondary position-absolute';
        togglePassword.style.right = '10px';
        togglePassword.style.top = '50%';
        togglePassword.style.transform = 'translateY(-50%)';
        togglePassword.style.zIndex = '5';
        
        passwordInput.parentNode.style.position = 'relative';
        passwordInput.parentNode.appendChild(togglePassword);
        
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
    }

    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Efecto de carga para botones
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Procesando...';
            setTimeout(() => {
                this.innerHTML = this.getAttribute('data-original-text') || this.innerHTML;
            }, 2000);
        });
    });
});

// Función para mostrar notificaciones toast
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}-circle me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}