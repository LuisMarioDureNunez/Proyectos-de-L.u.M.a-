class SistemaGestion {
    constructor() {
        this.init();
    }

    init() {
        this.initEventListeners();
        this.initTooltips();
        this.initAutoDismiss();
        this.initDynamicForms();
        this.initSearch();
    }

    initEventListeners() {
        // Confirmación para acciones destructivas
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-confirm]')) {
                const message = e.target.closest('[data-confirm]').getAttribute('data-confirm');
                if (!confirm(message)) {
                    e.preventDefault();
                }
            }
        });

        // Auto-submit en filtros
        document.addEventListener('change', (e) => {
            if (e.target.closest('[data-auto-submit]')) {
                e.target.closest('form').submit();
            }
        });

        // Toggle sidebar en móviles
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-toggle-sidebar]')) {
                document.querySelector('.sidebar').classList.toggle('d-none');
            }
        });
    }

    initTooltips() {
        // Inicializar tooltips de Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initAutoDismiss() {
        // Auto-dismiss alerts después de 5 segundos
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    }

    initDynamicForms() {
        // Dynamic form fields para items de presupuesto
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-add-item]')) {
                this.addFormItem(e);
            }
            if (e.target.closest('[data-remove-item]')) {
                this.removeFormItem(e);
            }
        });

        // Cálculo automático de totales
        document.addEventListener('input', (e) => {
            if (e.target.name && (e.target.name.includes('cantidad') || e.target.name.includes('precio_unitario'))) {
                this.calcularTotalItem(e.target);
            }
        });
    }

    addFormItem(e) {
        e.preventDefault();
        const container = e.target.closest('[data-items-container]');
        const template = container.querySelector('[data-item-template]');
        const newItem = template.cloneNode(true);
        newItem.classList.remove('d-none');
        newItem.removeAttribute('data-item-template');
        
        // Actualizar índices
        const index = container.querySelectorAll('[data-item]').length;
        newItem.querySelectorAll('[name]').forEach(input => {
            const name = input.getAttribute('name').replace('-0-', `-${index}-`);
            input.setAttribute('name', name);
            input.value = '';
        });
        
        container.appendChild(newItem);
        this.actualizarContadoresItems(container);
    }

    removeFormItem(e) {
        e.preventDefault();
        const item = e.target.closest('[data-item]');
        if (item && item.parentElement.querySelectorAll('[data-item]').length > 1) {
            item.remove();
            this.actualizarContadoresItems(item.parentElement);
        }
    }

    actualizarContadoresItems(container) {
        const items = container.querySelectorAll('[data-item]');
        items.forEach((item, index) => {
            item.querySelectorAll('[name]').forEach(input => {
                const name = input.getAttribute('name').replace(/-(\d+)-/, `-${index}-`);
                input.setAttribute('name', name);
            });
        });
    }

    calcularTotalItem(input) {
        const item = input.closest('[data-item]');
        const cantidad = parseFloat(item.querySelector('[name*="cantidad"]').value) || 0;
        const precio = parseFloat(item.querySelector('[name*="precio_unitario"]').value) || 0;
        const total = cantidad * precio;
        
        const totalInput = item.querySelector('[name*="total"]');
        if (totalInput) {
            totalInput.value = total.toFixed(2);
        }
        
        this.calcularTotalGeneral();
    }

    calcularTotalGeneral() {
        let totalGeneral = 0;
        document.querySelectorAll('[name*="total"]').forEach(input => {
            totalGeneral += parseFloat(input.value) || 0;
        });
        
        const totalGeneralElement = document.querySelector('#total-general');
        if (totalGeneralElement) {
            totalGeneralElement.textContent = totalGeneral.toFixed(2);
        }
    }

    initSearch() {
        // Búsqueda en tiempo real
        const searchInputs = document.querySelectorAll('[data-real-time-search]');
        searchInputs.forEach(input => {
            input.addEventListener('input', this.debounce(() => {
                this.realTimeSearch(input);
            }, 300));
        });
    }

    realTimeSearch(input) {
        const searchUrl = input.getAttribute('data-search-url');
        const target = input.getAttribute('data-target');
        const query = input.value;

        if (query.length < 2) {
            this.clearSearchResults(target);
            return;
        }

        fetch(`${searchUrl}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => this.displaySearchResults(data, target))
            .catch(error => console.error('Error en búsqueda:', error));
    }

    displaySearchResults(data, target) {
        const container = document.querySelector(target);
        if (!container) return;

        container.innerHTML = '';
        
        if (data.resultados && data.resultados.length > 0) {
            data.resultados.forEach(item => {
                const element = this.createSearchResultElement(item);
                container.appendChild(element);
            });
        } else {
            container.innerHTML = '<div class="text-muted p-2">No se encontraron resultados</div>';
        }
    }

    createSearchResultElement(item) {
        const div = document.createElement('div');
        div.className = 'search-result-item p-2 border-bottom';
        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${item.nombre}</strong>
                    ${item.precio ? `<br><small class="text-success">$${item.precio}</small>` : ''}
                </div>
                <button type="button" class="btn btn-sm btn-outline-primary" 
                        onclick="sistemaGestion.selectSearchItem(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                    Seleccionar
                </button>
            </div>
        `;
        return div;
    }

    selectSearchItem(item) {
        // Implementar según el contexto
        console.log('Item seleccionado:', item);
    }

    clearSearchResults(target) {
        const container = document.querySelector(target);
        if (container) {
            container.innerHTML = '';
        }
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Utilidades para notificaciones
    mostrarNotificacion(mensaje, tipo = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[tipo] || 'alert-info';

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.messages-container') || document.body;
        container.appendChild(alertDiv);

        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Cargar datos asíncronos
    cargarDatos(url, callback) {
        fetch(url)
            .then(response => response.json())
            .then(data => callback(data))
            .catch(error => console.error('Error cargando datos:', error));
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.sistemaGestion = new SistemaGestion();
});