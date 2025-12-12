// TRADUCTOR ESPECÍFICO PARA PANEL DE ADMINISTRACIÓN DJANGO
// Se ejecuta automáticamente en /admin/

(function() {
    'use strict';
    
    // Verificar si estamos en el panel de administración
    if (!window.location.pathname.includes('/admin/')) {
        return;
    }
    
    class AdminTranslator {
        constructor() {
            this.currentLanguage = localStorage.getItem('lumaLanguage') || 'es';
            this.init();
        }
        
        init() {
            // Esperar a que el DOM esté completamente cargado
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.translateAdmin());
            } else {
                this.translateAdmin();
            }
            
            // Observar cambios dinámicos
            this.setupObserver();
            
            // Escuchar cambios de idioma
            document.addEventListener('changeLanguage', (e) => {
                this.currentLanguage = e.detail.language;
                setTimeout(() => this.translateAdmin(), 100);
            });
        }
        
        setupObserver() {
            const observer = new MutationObserver(() => {
                this.translateAdmin();
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        translateAdmin() {
            // Traducir elementos específicos del admin de Django
            this.translateHeader();
            this.translateNavigation();
            this.translateTables();
            this.translateForms();
            this.translateButtons();
            this.translateMessages();
            this.translateBreadcrumbs();
            this.translateModules();
        }
        
        translateHeader() {
            // Traducir header del admin
            const branding = document.querySelector('#branding h1');
            if (branding) {
                this.translateText(branding);
            }
            
            // Traducir herramientas de usuario
            document.querySelectorAll('#user-tools a').forEach(link => {
                this.translateText(link);
            });
        }
        
        translateNavigation() {
            // Traducir navegación lateral
            document.querySelectorAll('#nav-sidebar .app-label').forEach(label => {
                this.translateText(label);
            });
            
            document.querySelectorAll('#nav-sidebar .model-label').forEach(label => {
                this.translateText(label);
            });
        }
        
        translateTables() {
            // Traducir encabezados de tablas
            document.querySelectorAll('th').forEach(th => {
                this.translateText(th);
            });
            
            // Traducir contenido de celdas comunes
            document.querySelectorAll('td').forEach(td => {
                if (td.children.length === 0) {
                    this.translateText(td);
                }
            });
        }
        
        translateForms() {
            // Traducir labels de formularios
            document.querySelectorAll('label').forEach(label => {
                this.translateText(label);
            });
            
            // Traducir textos de ayuda
            document.querySelectorAll('.help').forEach(help => {
                this.translateText(help);
            });
            
            // Traducir placeholders
            document.querySelectorAll('input[placeholder]').forEach(input => {
                const translation = this.getTranslation(input.placeholder.toLowerCase());
                if (translation) {
                    input.placeholder = translation;
                }
            });
        }
        
        translateButtons() {
            // Traducir botones
            document.querySelectorAll('input[type="submit"], button').forEach(btn => {
                const text = btn.value || btn.textContent;
                if (text) {
                    const translation = this.getTranslation(text.toLowerCase());
                    if (translation) {
                        if (btn.value) {
                            btn.value = translation;
                        } else {
                            btn.textContent = translation;
                        }
                    }
                }
            });
            
            // Traducir enlaces de acción
            document.querySelectorAll('.addlink, .changelink, .deletelink').forEach(link => {
                this.translateText(link);
            });
        }
        
        translateMessages() {
            // Traducir mensajes del sistema
            document.querySelectorAll('.messagelist li').forEach(msg => {
                this.translateText(msg);
            });
            
            document.querySelectorAll('.errornote, .warningnote').forEach(note => {
                this.translateText(note);
            });
        }
        
        translateBreadcrumbs() {
            // Traducir breadcrumbs
            document.querySelectorAll('.breadcrumbs a').forEach(crumb => {
                this.translateText(crumb);
            });
        }
        
        translateModules() {
            // Traducir módulos de la página principal
            document.querySelectorAll('.module caption').forEach(caption => {
                this.translateText(caption);
            });
            
            document.querySelectorAll('.app-list .section h2').forEach(h2 => {
                this.translateText(h2);
            });
        }
        
        translateText(element) {
            if (!element || !element.textContent) return;
            
            const text = element.textContent.trim().toLowerCase();
            const translation = this.getTranslation(text);
            
            if (translation && translation !== text) {
                element.textContent = translation;
            }
        }
        
        getTranslation(text) {
            const translations = {
                // Textos del header
                'sistema gestión paraguay - administración': {
                    'en': 'PARAGUAY MANAGEMENT SYSTEM - Administration',
                    'ru': 'СИСТЕМА УПРАВЛЕНИЯ ПАРАГВАЙ - Администрирование',
                    'ja': 'パラグアイ管理システム - 管理',
                    'it': 'SISTEMA GESTIONE PARAGUAY - Amministrazione',
                    'fr': 'SYSTÈME GESTION PARAGUAY - Administration'
                },
                'bienvenidos': {
                    'en': 'Welcome', 'ru': 'Добро пожаловать', 'ja': 'ようこそ', 'it': 'Benvenuti', 'fr': 'Bienvenue'
                },
                'ver el sitio': {
                    'en': 'View Site', 'ru': 'Посмотреть сайт', 'ja': 'サイトを見る', 'it': 'Vedi Sito', 'fr': 'Voir le Site'
                },
                'cambiar contraseña': {
                    'en': 'Change Password', 'ru': 'Изменить пароль', 'ja': 'パスワード変更', 'it': 'Cambia Password', 'fr': 'Changer Mot de Passe'
                },
                'cerrar sesión': {
                    'en': 'Logout', 'ru': 'Выйти', 'ja': 'ログアウト', 'it': 'Disconnetti', 'fr': 'Déconnexion'
                },
                'cambiar tema': {
                    'en': 'Change Theme', 'ru': 'Изменить тему', 'ja': 'テーマ変更', 'it': 'Cambia Tema', 'fr': 'Changer Thème'
                },
                'panel de administración profesional': {
                    'en': 'Professional Administration Panel',
                    'ru': 'Профессиональная панель администрирования',
                    'ja': 'プロフェッショナル管理パネル',
                    'it': 'Pannello Amministrazione Professionale',
                    'fr': 'Panneau Administration Professionnel'
                },
                'autenticación y autorización': {
                    'en': 'Authentication and Authorization',
                    'ru': 'Аутентификация и авторизация',
                    'ja': '認証と認可',
                    'it': 'Autenticazione e Autorizzazione',
                    'fr': 'Authentification et Autorisation'
                },
                'grupos': {
                    'en': 'Groups', 'ru': 'Группы', 'ja': 'グループ', 'it': 'Gruppi', 'fr': 'Groupes'
                },
                'gestion': {
                    'en': 'Management', 'ru': 'Управление', 'ja': '管理', 'it': 'Gestione', 'fr': 'Gestion'
                },
                'añadir': {
                    'en': 'Add', 'ru': 'Добавить', 'ja': '追加', 'it': 'Aggiungi', 'fr': 'Ajouter'
                },
                'modificar': {
                    'en': 'Modify', 'ru': 'Изменить', 'ja': '変更', 'it': 'Modifica', 'fr': 'Modifier'
                },
                'carritos': {
                    'en': 'Carts', 'ru': 'Корзины', 'ja': 'カート', 'it': 'Carrelli', 'fr': 'Paniers'
                },
                'categorías': {
                    'en': 'Categories', 'ru': 'Категории', 'ja': 'カテゴリー', 'it': 'Categorie', 'fr': 'Catégories'
                },
                'contratistas': {
                    'en': 'Contractors', 'ru': 'Подрядчики', 'ja': '請負業者', 'it': 'Appaltatori', 'fr': 'Entrepreneurs'
                },
                'contratos de contratistas': {
                    'en': 'Contractor Contracts',
                    'ru': 'Контракты подрядчиков',
                    'ja': '請負業者契約',
                    'it': 'Contratti Appaltatori',
                    'fr': 'Contrats Entrepreneurs'
                },
                'empleados': {
                    'en': 'Employees', 'ru': 'Сотрудники', 'ja': '従業員', 'it': 'Dipendenti', 'fr': 'Employés'
                },
                'evaluaciones de proveedores': {
                    'en': 'Supplier Evaluations',
                    'ru': 'Оценки поставщиков',
                    'ja': 'サプライヤー評価',
                    'it': 'Valutazioni Fornitori',
                    'fr': 'Évaluations Fournisseurs'
                },
                'herramientas': {
                    'en': 'Tools', 'ru': 'Инструменты', 'ja': 'ツール', 'it': 'Strumenti', 'fr': 'Outils'
                },
                'items de pedido': {
                    'en': 'Order Items', 'ru': 'Элементы заказа', 'ja': '注文アイテム', 'it': 'Articoli Ordine', 'fr': 'Articles Commande'
                },
                'items del carrito': {
                    'en': 'Cart Items', 'ru': 'Элементы корзины', 'ja': 'カートアイテム', 'it': 'Articoli Carrello', 'fr': 'Articles Panier'
                },
                'maquinarias': {
                    'en': 'Machinery', 'ru': 'Оборудование', 'ja': '機械', 'it': 'Macchinari', 'fr': 'Machines'
                },
                'materiales': {
                    'en': 'Materials', 'ru': 'Материалы', 'ja': '材料', 'it': 'Materiali', 'fr': 'Matériaux'
                },
                'notificaciones': {
                    'en': 'Notifications', 'ru': 'Уведомления', 'ja': '通知', 'it': 'Notifiche', 'fr': 'Notifications'
                },
                'obras': {
                    'en': 'Projects', 'ru': 'Проекты', 'ja': 'プロジェクト', 'it': 'Progetti', 'fr': 'Projets'
                },
                'pedidos': {
                    'en': 'Orders', 'ru': 'Заказы', 'ja': '注文', 'it': 'Ordini', 'fr': 'Commandes'
                },
                'presupuestos': {
                    'en': 'Budgets', 'ru': 'Бюджеты', 'ja': '予算', 'it': 'Budget', 'fr': 'Budgets'
                },
                'productos': {
                    'en': 'Products', 'ru': 'Продукты', 'ja': '製品', 'it': 'Prodotti', 'fr': 'Produits'
                },
                'productos de proveedores': {
                    'en': 'Supplier Products',
                    'ru': 'Продукты поставщиков',
                    'ja': 'サプライヤー製品',
                    'it': 'Prodotti Fornitori',
                    'fr': 'Produits Fournisseurs'
                },
                'propiedades': {
                    'en': 'Properties', 'ru': 'Свойства', 'ja': 'プロパティ', 'it': 'Proprietà', 'fr': 'Propriétés'
                },
                'propietarios': {
                    'en': 'Owners', 'ru': 'Владельцы', 'ja': '所有者', 'it': 'Proprietari', 'fr': 'Propriétaires'
                },
                'proveedores': {
                    'en': 'Suppliers', 'ru': 'Поставщики', 'ja': 'サプライヤー', 'it': 'Fornitori', 'fr': 'Fournisseurs'
                },
                'tiendas': {
                    'en': 'Stores', 'ru': 'Магазины', 'ja': '店舗', 'it': 'Negozi', 'fr': 'Magasins'
                },
                'usuarios': {
                    'en': 'Users', 'ru': 'Пользователи', 'ja': 'ユーザー', 'it': 'Utenti', 'fr': 'Utilisateurs'
                },
                'acciones recientes': {
                    'en': 'Recent Actions', 'ru': 'Недавние действия', 'ja': '最近のアクション', 'it': 'Azioni Recenti', 'fr': 'Actions Récentes'
                },
                'mis acciones': {
                    'en': 'My Actions', 'ru': 'Мои действия', 'ja': '私のアクション', 'it': 'Le Mie Azioni', 'fr': 'Mes Actions'
                },
                'ninguno disponible': {
                    'en': 'None Available', 'ru': 'Нет доступных', 'ja': '利用不可', 'it': 'Nessuno Disponibile', 'fr': 'Aucun Disponible'
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
    
    // Inicializar el traductor del admin
    new AdminTranslator();
    
})();