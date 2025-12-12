// TRADUCTOR ESPECÍFICO PARA PÁGINA DE INICIO
// Traduce todo el contenido de la página principal

(function() {
    'use strict';
    
    class HomeTranslator {
        constructor() {
            this.currentLanguage = localStorage.getItem('lumaLanguage') || 'es';
            this.init();
        }
        
        init() {
            // Esperar a que el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.translateHome());
            } else {
                this.translateHome();
            }
            
            // Escuchar cambios de idioma
            document.addEventListener('changeLanguage', (e) => {
                this.currentLanguage = e.detail.language;
                setTimeout(() => this.translateHome(), 100);
            });
            
            // Observar cambios dinámicos
            this.setupObserver();
        }
        
        setupObserver() {
            const observer = new MutationObserver(() => {
                this.translateHome();
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        translateHome() {
            // Traducir todos los elementos de la página de inicio
            this.translateAllElements();
        }
        
        translateAllElements() {
            // Traducir TODOS los elementos de texto
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            
            const textNodes = [];
            let node;
            
            while (node = walker.nextNode()) {
                if (node.nodeValue.trim()) {
                    textNodes.push(node);
                }
            }
            
            textNodes.forEach(textNode => {
                const text = textNode.nodeValue.trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    textNode.nodeValue = translation;
                }
            });
            
            // Traducir placeholders y atributos
            this.translateAttributes();
        }
        
        translateAttributes() {
            // Traducir placeholders
            document.querySelectorAll('[placeholder]').forEach(element => {
                const placeholder = element.placeholder.toLowerCase();
                const translation = this.getTranslation(placeholder);
                if (translation) {
                    element.placeholder = translation;
                }
            });
            
            // Traducir títulos
            document.querySelectorAll('[title]').forEach(element => {
                const title = element.title.toLowerCase();
                const translation = this.getTranslation(title);
                if (translation) {
                    element.title = translation;
                }
            });
            
            // Traducir alt text
            document.querySelectorAll('[alt]').forEach(element => {
                const alt = element.alt.toLowerCase();
                const translation = this.getTranslation(alt);
                if (translation) {
                    element.alt = translation;
                }
            });
        }
        
        getTranslation(text) {
            // Usar las mismas traducciones que el auto-traductor principal
            if (window.AutoTranslator && window.AutoTranslator.prototype.getTranslation) {
                return window.AutoTranslator.prototype.getTranslation.call(this, text);
            }
            
            // Traducciones locales como respaldo
            const translations = {
                'sistema de gestión en presupuestos': {
                    'en': 'BUDGET MANAGEMENT SYSTEM',
                    'ru': 'СИСТЕМА УПРАВЛЕНИЯ БЮДЖЕТОМ',
                    'ja': '予算管理システム',
                    'it': 'SISTEMA GESTIONE BUDGET',
                    'fr': 'SYSTÈME GESTION BUDGETS'
                },
                'para obras civiles': {
                    'en': 'FOR CIVIL WORKS',
                    'ru': 'ДЛЯ ГРАЖДАНСКИХ РАБОТ',
                    'ja': '土木工事用',
                    'it': 'PER LAVORI CIVILI',
                    'fr': 'POUR TRAVAUX CIVILS'
                },
                'plataforma profesional para la gestión de obras civiles y presupuestos en paraguay': {
                    'en': 'Professional platform for civil works and budget management in Paraguay',
                    'ru': 'Профессиональная платформа для управления гражданскими работами и бюджетом в Парагвае',
                    'ja': 'パラグアイの土木工事と予算管理のためのプロフェッショナルプラットフォーム',
                    'it': 'Piattaforma professionale per la gestione di lavori civili e budget in Paraguay',
                    'fr': 'Plateforme professionnelle pour la gestion des travaux civils et budgets au Paraguay'
                }
            };
            
            const cleanText = text.toLowerCase().trim();
            const translationObj = translations[cleanText];
            
            if (translationObj && translationObj[this.currentLanguage]) {
                return translationObj[this.currentLanguage];
            }
            
            return null;
        }
    }
    
    // Inicializar solo si no estamos en el admin
    if (!window.location.pathname.includes('/admin/')) {
        new HomeTranslator();
    }
    
})();