// Sistema de Modo Oscuro/Claro
class ThemeSwitcher {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createToggleButton();
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle-btn';
        button.innerHTML = this.currentTheme === 'dark' ? '☀️' : '🌙';
        button.onclick = () => this.toggleTheme();
        
        // Agregar estilos
        const style = document.createElement('style');
        style.textContent = `
            .theme-toggle-btn {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
                transition: all 0.3s;
                z-index: 1000;
            }
            .theme-toggle-btn:hover {
                transform: scale(1.1) rotate(15deg);
                box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            }
            
            /* Tema Oscuro */
            body.dark-theme {
                background-color: #1a202c;
                color: #e2e8f0;
            }
            body.dark-theme .card {
                background-color: #2d3748;
                color: #e2e8f0;
                border-color: #4a5568;
            }
            body.dark-theme .card-header {
                background-color: #374151 !important;
                color: #e2e8f0;
                border-bottom-color: #4a5568;
            }
            body.dark-theme .table {
                color: #e2e8f0;
            }
            body.dark-theme .table-striped tbody tr:nth-of-type(odd) {
                background-color: #374151;
            }
            body.dark-theme .table-hover tbody tr:hover {
                background-color: #4a5568;
            }
            body.dark-theme .form-control {
                background-color: #374151;
                border-color: #4a5568;
                color: #e2e8f0;
            }
            body.dark-theme .form-select {
                background-color: #374151;
                border-color: #4a5568;
                color: #e2e8f0;
            }
            body.dark-theme .btn-outline-primary {
                color: #60a5fa;
                border-color: #60a5fa;
            }
            body.dark-theme .btn-outline-primary:hover {
                background-color: #60a5fa;
                color: white;
            }
            body.dark-theme .text-muted {
                color: #9ca3af !important;
            }
            body.dark-theme .bg-light {
                background-color: #374151 !important;
            }
            body.dark-theme .border {
                border-color: #4a5568 !important;
            }
            
            /* Transición suave */
            body, .card, .card-header, .table, .form-control, .form-select {
                transition: background-color 0.3s, color 0.3s, border-color 0.3s;
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(button);
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
    }

    applyTheme(theme) {
        const button = document.getElementById('theme-toggle');
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            if (button) button.innerHTML = '☀️';
        } else {
            document.body.classList.remove('dark-theme');
            if (button) button.innerHTML = '🌙';
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ThemeSwitcher();
});