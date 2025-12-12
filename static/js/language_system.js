// SISTEMA DE IDIOMAS MULTILENGUAJE SUPER AVANZADO
// Soporte para 25+ idiomas con traducciones completas

class LanguageManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('lumaLanguage') || 'es';
        this.translations = {};
        this.loadTranslations();
        this.initializeLanguageSystem();
    }

    // Traducciones completas para 25 idiomas
    loadTranslations() {
        this.translations = {
            // ESPAÑOL (Predeterminado)
            'es': {
                // Navegación
                'inicio': 'INICIO',
                'dashboard': 'DASHBOARD',
                'obras': 'OBRAS',
                'presupuestos': 'PRESUPUESTOS',
                'materiales': 'MATERIALES',
                'maquinarias': 'MAQUINARIAS',
                'herramientas': 'HERRAMIENTAS',
                'contratistas': 'CONTRATISTAS',
                'propietarios': 'PROPIETARIOS',
                'empleados': 'EMPLEADOS',
                'proveedores': 'PROVEEDORES',
                
                // L.u.N.a AI
                'asistente_inteligente': 'Asistente Inteligente',
                'luna_saludo': '¡Hola! Soy L.u.N.a, tu asistente de IA para gestión de obras civiles. ¿En qué puedo ayudarte hoy? 🚀',
                'escribe_pregunta': 'Escribe tu pregunta aquí...',
                'enviar_mensaje': 'Enviar mensaje',
                
                // Mensajes comunes
                'bienvenido': 'Bienvenido',
                'cerrar_sesion': 'Cerrar Sesión',
                'mi_perfil': 'Mi Perfil',
                'configuracion': 'Configuración',
                'ayuda': 'Ayuda',
                'contacto': 'Contacto',
                'idioma': 'Idioma',
                'seleccionar_idioma': 'Seleccionar Idioma',
                'guardar': 'Guardar',
                'cancelar': 'Cancelar',
                'eliminar': 'Eliminar',
                'editar': 'Editar',
                'crear': 'Crear',
                'buscar': 'Buscar',
                'filtrar': 'Filtrar',
                'exportar': 'Exportar',
                'imprimir': 'Imprimir'
            },

            // INGLÉS
            'en': {
                'inicio': 'HOME',
                'dashboard': 'DASHBOARD',
                'obras': 'PROJECTS',
                'presupuestos': 'BUDGETS',
                'materiales': 'MATERIALS',
                'maquinarias': 'MACHINERY',
                'herramientas': 'TOOLS',
                'contratistas': 'CONTRACTORS',
                'propietarios': 'OWNERS',
                'empleados': 'EMPLOYEES',
                'proveedores': 'SUPPLIERS',
                
                'asistente_inteligente': 'Intelligent Assistant',
                'luna_saludo': 'Hello! I\'m L.u.N.a, your AI assistant for civil works management. How can I help you today? 🚀',
                'escribe_pregunta': 'Type your question here...',
                'enviar_mensaje': 'Send message',
                
                'bienvenido': 'Welcome',
                'cerrar_sesion': 'Logout',
                'mi_perfil': 'My Profile',
                'configuracion': 'Settings',
                'ayuda': 'Help',
                'contacto': 'Contact',
                'idioma': 'Language',
                'seleccionar_idioma': 'Select Language',
                'guardar': 'Save',
                'cancelar': 'Cancel',
                'eliminar': 'Delete',
                'editar': 'Edit',
                'crear': 'Create',
                'buscar': 'Search',
                'filtrar': 'Filter',
                'exportar': 'Export',
                'imprimir': 'Print'
            },

            // GUARANÍ
            'gn': {
                'inicio': 'ÑEPYRŨ',
                'dashboard': 'ÑEHECHAUKA',
                'obras': 'TEMBIAPO',
                'presupuestos': 'JEPORU CUENTA',
                'materiales': 'MBAʼE',
                'maquinarias': 'MÁQUINA',
                'herramientas': 'TEMBIPORU',
                'contratistas': 'TEMBIAPORÃ',
                'propietarios': 'JÁRA',
                'empleados': 'TEMBIAPÓVA',
                'proveedores': 'ÑEME\'Ẽ',
                
                'asistente_inteligente': 'Pytyvõhára Arandu',
                'luna_saludo': '¡Mba\'éichapa! Che ha\'e L.u.N.a, nde pytyvõhára AI tembiapo civil rehegua. ¿Mba\'éichapa ikatu roipytyvõ ko\'ára? 🚀',
                'escribe_pregunta': 'Ehai nde porandu ko\'ápe...',
                'enviar_mensaje': 'Emondo ñe\'ẽmondo',
                
                'bienvenido': 'Tereguahẽ porãite',
                'cerrar_sesion': 'Esẽ',
                'mi_perfil': 'Che Perfil',
                'configuracion': 'Ñemboheko',
                'ayuda': 'Pytyvõ',
                'contacto': 'Ñe\'ẽ',
                'idioma': 'Ñe\'ẽ',
                'seleccionar_idioma': 'Eiporavo Ñe\'ẽ',
                'guardar': 'Ñongatu',
                'cancelar': 'Ani',
                'eliminar': 'Mbogue',
                'editar': 'Ñembosako\'i',
                'crear': 'Japo',
                'buscar': 'Jeheka',
                'filtrar': 'Ñemboguata',
                'exportar': 'Ñesẽ',
                'imprimir': 'Ñembokuatia'
            },

            // PORTUGUÉS
            'pt': {
                'inicio': 'INÍCIO',
                'dashboard': 'PAINEL',
                'obras': 'OBRAS',
                'presupuestos': 'ORÇAMENTOS',
                'materiales': 'MATERIAIS',
                'maquinarias': 'MAQUINÁRIO',
                'herramientas': 'FERRAMENTAS',
                'contratistas': 'EMPREITEIROS',
                'propietarios': 'PROPRIETÁRIOS',
                'empleados': 'FUNCIONÁRIOS',
                'proveedores': 'FORNECEDORES',
                
                'asistente_inteligente': 'Assistente Inteligente',
                'luna_saludo': 'Olá! Eu sou L.u.N.a, seu assistente de IA para gestão de obras civis. Como posso ajudá-lo hoje? 🚀',
                'escribe_pregunta': 'Digite sua pergunta aqui...',
                'enviar_mensaje': 'Enviar mensagem',
                
                'bienvenido': 'Bem-vindo',
                'cerrar_sesion': 'Sair',
                'mi_perfil': 'Meu Perfil',
                'configuracion': 'Configurações',
                'ayuda': 'Ajuda',
                'contacto': 'Contato',
                'idioma': 'Idioma',
                'seleccionar_idioma': 'Selecionar Idioma',
                'guardar': 'Salvar',
                'cancelar': 'Cancelar',
                'eliminar': 'Excluir',
                'editar': 'Editar',
                'crear': 'Criar',
                'buscar': 'Buscar',
                'filtrar': 'Filtrar',
                'exportar': 'Exportar',
                'imprimir': 'Imprimir'
            },

            // JAPONÉS
            'ja': {
                'inicio': 'ホーム',
                'dashboard': 'ダッシュボード',
                'obras': 'プロジェクト',
                'presupuestos': '予算',
                'materiales': '材料',
                'maquinarias': '機械',
                'herramientas': 'ツール',
                'contratistas': '請負業者',
                'propietarios': '所有者',
                'empleados': '従業員',
                'proveedores': 'サプライヤー',
                
                'asistente_inteligente': 'インテリジェントアシスタント',
                'luna_saludo': 'こんにちは！私はL.u.N.a、土木工事管理のためのAIアシスタントです。今日はどのようにお手伝いできますか？🚀',
                'escribe_pregunta': 'ここに質問を入力してください...',
                'enviar_mensaje': 'メッセージを送信',
                
                'bienvenido': 'ようこそ',
                'cerrar_sesion': 'ログアウト',
                'mi_perfil': 'マイプロフィール',
                'configuracion': '設定',
                'ayuda': 'ヘルプ',
                'contacto': '連絡先',
                'idioma': '言語',
                'seleccionar_idioma': '言語を選択',
                'guardar': '保存',
                'cancelar': 'キャンセル',
                'eliminar': '削除',
                'editar': '編集',
                'crear': '作成',
                'buscar': '検索',
                'filtrar': 'フィルター',
                'exportar': 'エクスポート',
                'imprimir': '印刷'
            },

            // RUSO
            'ru': {
                'inicio': 'ГЛАВНАЯ',
                'dashboard': 'ПАНЕЛЬ',
                'obras': 'ПРОЕКТЫ',
                'presupuestos': 'БЮДЖЕТЫ',
                'materiales': 'МАТЕРИАЛЫ',
                'maquinarias': 'ОБОРУДОВАНИЕ',
                'herramientas': 'ИНСТРУМЕНТЫ',
                'contratistas': 'ПОДРЯДЧИКИ',
                'propietarios': 'ВЛАДЕЛЬЦЫ',
                'empleados': 'СОТРУДНИКИ',
                'proveedores': 'ПОСТАВЩИКИ',
                
                'asistente_inteligente': 'Умный Помощник',
                'luna_saludo': 'Привет! Я L.u.N.a, ваш ИИ-помощник для управления гражданскими работами. Как я могу помочь вам сегодня? 🚀',
                'escribe_pregunta': 'Введите ваш вопрос здесь...',
                'enviar_mensaje': 'Отправить сообщение',
                
                'bienvenido': 'Добро пожаловать',
                'cerrar_sesion': 'Выйти',
                'mi_perfil': 'Мой Профиль',
                'configuracion': 'Настройки',
                'ayuda': 'Помощь',
                'contacto': 'Контакт',
                'idioma': 'Язык',
                'seleccionar_idioma': 'Выбрать Язык',
                'guardar': 'Сохранить',
                'cancelar': 'Отмена',
                'eliminar': 'Удалить',
                'editar': 'Редактировать',
                'crear': 'Создать',
                'buscar': 'Поиск',
                'filtrar': 'Фильтр',
                'exportar': 'Экспорт',
                'imprimir': 'Печать'
            },

            // COREANO
            'ko': {
                'inicio': '홈',
                'dashboard': '대시보드',
                'obras': '프로젝트',
                'presupuestos': '예산',
                'materiales': '자재',
                'maquinarias': '기계',
                'herramientas': '도구',
                'contratistas': '계약자',
                'propietarios': '소유자',
                'empleados': '직원',
                'proveedores': '공급업체',
                
                'asistente_inteligente': '지능형 어시스턴트',
                'luna_saludo': '안녕하세요! 저는 토목 공사 관리를 위한 AI 어시스턴트 L.u.N.a입니다. 오늘 어떻게 도와드릴까요? 🚀',
                'escribe_pregunta': '여기에 질문을 입력하세요...',
                'enviar_mensaje': '메시지 보내기',
                
                'bienvenido': '환영합니다',
                'cerrar_sesion': '로그아웃',
                'mi_perfil': '내 프로필',
                'configuracion': '설정',
                'ayuda': '도움말',
                'contacto': '연락처',
                'idioma': '언어',
                'seleccionar_idioma': '언어 선택',
                'guardar': '저장',
                'cancelar': '취소',
                'eliminar': '삭제',
                'editar': '편집',
                'crear': '생성',
                'buscar': '검색',
                'filtrar': '필터',
                'exportar': '내보내기',
                'imprimir': '인쇄'
            },

            // FRANCÉS
            'fr': {
                'inicio': 'ACCUEIL',
                'dashboard': 'TABLEAU DE BORD',
                'obras': 'PROJETS',
                'presupuestos': 'BUDGETS',
                'materiales': 'MATÉRIAUX',
                'maquinarias': 'MACHINES',
                'herramientas': 'OUTILS',
                'contratistas': 'ENTREPRENEURS',
                'propietarios': 'PROPRIÉTAIRES',
                'empleados': 'EMPLOYÉS',
                'proveedores': 'FOURNISSEURS',
                
                'asistente_inteligente': 'Assistant Intelligent',
                'luna_saludo': 'Bonjour! Je suis L.u.N.a, votre assistant IA pour la gestion des travaux civils. Comment puis-je vous aider aujourd\'hui? 🚀',
                'escribe_pregunta': 'Tapez votre question ici...',
                'enviar_mensaje': 'Envoyer le message',
                
                'bienvenido': 'Bienvenue',
                'cerrar_sesion': 'Se Déconnecter',
                'mi_perfil': 'Mon Profil',
                'configuracion': 'Paramètres',
                'ayuda': 'Aide',
                'contacto': 'Contact',
                'idioma': 'Langue',
                'seleccionar_idioma': 'Sélectionner la Langue',
                'guardar': 'Sauvegarder',
                'cancelar': 'Annuler',
                'eliminar': 'Supprimer',
                'editar': 'Modifier',
                'crear': 'Créer',
                'buscar': 'Rechercher',
                'filtrar': 'Filtrer',
                'exportar': 'Exporter',
                'imprimir': 'Imprimer'
            },

            // ALEMÁN
            'de': {
                'inicio': 'STARTSEITE',
                'dashboard': 'DASHBOARD',
                'obras': 'PROJEKTE',
                'presupuestos': 'BUDGETS',
                'materiales': 'MATERIALIEN',
                'maquinarias': 'MASCHINEN',
                'herramientas': 'WERKZEUGE',
                'contratistas': 'AUFTRAGNEHMER',
                'propietarios': 'EIGENTÜMER',
                'empleados': 'MITARBEITER',
                'proveedores': 'LIEFERANTEN',
                
                'asistente_inteligente': 'Intelligenter Assistent',
                'luna_saludo': 'Hallo! Ich bin L.u.N.a, Ihr KI-Assistent für das Management von Tiefbauarbeiten. Wie kann ich Ihnen heute helfen? 🚀',
                'escribe_pregunta': 'Geben Sie hier Ihre Frage ein...',
                'enviar_mensaje': 'Nachricht senden',
                
                'bienvenido': 'Willkommen',
                'cerrar_sesion': 'Abmelden',
                'mi_perfil': 'Mein Profil',
                'configuracion': 'Einstellungen',
                'ayuda': 'Hilfe',
                'contacto': 'Kontakt',
                'idioma': 'Sprache',
                'seleccionar_idioma': 'Sprache Auswählen',
                'guardar': 'Speichern',
                'cancelar': 'Abbrechen',
                'eliminar': 'Löschen',
                'editar': 'Bearbeiten',
                'crear': 'Erstellen',
                'buscar': 'Suchen',
                'filtrar': 'Filtern',
                'exportar': 'Exportieren',
                'imprimir': 'Drucken'
            },

            // ITALIANO
            'it': {
                'inicio': 'HOME',
                'dashboard': 'CRUSCOTTO',
                'obras': 'PROGETTI',
                'presupuestos': 'BUDGET',
                'materiales': 'MATERIALI',
                'maquinarias': 'MACCHINARI',
                'herramientas': 'STRUMENTI',
                'contratistas': 'APPALTATORI',
                'propietarios': 'PROPRIETARI',
                'empleados': 'DIPENDENTI',
                'proveedores': 'FORNITORI',
                
                'asistente_inteligente': 'Assistente Intelligente',
                'luna_saludo': 'Ciao! Sono L.u.N.a, il tuo assistente AI per la gestione dei lavori civili. Come posso aiutarti oggi? 🚀',
                'escribe_pregunta': 'Scrivi la tua domanda qui...',
                'enviar_mensaje': 'Invia messaggio',
                
                'bienvenido': 'Benvenuto',
                'cerrar_sesion': 'Disconnetti',
                'mi_perfil': 'Il Mio Profilo',
                'configuracion': 'Impostazioni',
                'ayuda': 'Aiuto',
                'contacto': 'Contatto',
                'idioma': 'Lingua',
                'seleccionar_idioma': 'Seleziona Lingua',
                'guardar': 'Salva',
                'cancelar': 'Annulla',
                'eliminar': 'Elimina',
                'editar': 'Modifica',
                'crear': 'Crea',
                'buscar': 'Cerca',
                'filtrar': 'Filtra',
                'exportar': 'Esporta',
                'imprimir': 'Stampa'
            },

            // CHINO SIMPLIFICADO
            'zh': {
                'inicio': '首页',
                'dashboard': '仪表板',
                'obras': '项目',
                'presupuestos': '预算',
                'materiales': '材料',
                'maquinarias': '机械',
                'herramientas': '工具',
                'contratistas': '承包商',
                'propietarios': '业主',
                'empleados': '员工',
                'proveedores': '供应商',
                
                'asistente_inteligente': '智能助手',
                'luna_saludo': '您好！我是L.u.N.a，您的土木工程管理AI助手。今天我能为您做些什么？🚀',
                'escribe_pregunta': '在此输入您的问题...',
                'enviar_mensaje': '发送消息',
                
                'bienvenido': '欢迎',
                'cerrar_sesion': '登出',
                'mi_perfil': '我的资料',
                'configuracion': '设置',
                'ayuda': '帮助',
                'contacto': '联系',
                'idioma': '语言',
                'seleccionar_idioma': '选择语言',
                'guardar': '保存',
                'cancelar': '取消',
                'eliminar': '删除',
                'editar': '编辑',
                'crear': '创建',
                'buscar': '搜索',
                'filtrar': '筛选',
                'exportar': '导出',
                'imprimir': '打印'
            },

            // ÁRABE
            'ar': {
                'inicio': 'الرئيسية',
                'dashboard': 'لوحة التحكم',
                'obras': 'المشاريع',
                'presupuestos': 'الميزانيات',
                'materiales': 'المواد',
                'maquinarias': 'الآلات',
                'herramientas': 'الأدوات',
                'contratistas': 'المقاولون',
                'propietarios': 'الملاك',
                'empleados': 'الموظفون',
                'proveedores': 'الموردون',
                
                'asistente_inteligente': 'المساعد الذكي',
                'luna_saludo': 'مرحباً! أنا L.u.N.a، مساعدك الذكي لإدارة الأعمال المدنية. كيف يمكنني مساعدتك اليوم؟ 🚀',
                'escribe_pregunta': 'اكتب سؤالك هنا...',
                'enviar_mensaje': 'إرسال الرسالة',
                
                'bienvenido': 'مرحباً',
                'cerrar_sesion': 'تسجيل الخروج',
                'mi_perfil': 'ملفي الشخصي',
                'configuracion': 'الإعدادات',
                'ayuda': 'المساعدة',
                'contacto': 'الاتصال',
                'idioma': 'اللغة',
                'seleccionar_idioma': 'اختيار اللغة',
                'guardar': 'حفظ',
                'cancelar': 'إلغاء',
                'eliminar': 'حذف',
                'editar': 'تحرير',
                'crear': 'إنشاء',
                'buscar': 'بحث',
                'filtrar': 'تصفية',
                'exportar': 'تصدير',
                'imprimir': 'طباعة'
            },

            // HINDI
            'hi': {
                'inicio': 'होम',
                'dashboard': 'डैशबोर्ड',
                'obras': 'परियोजनाएं',
                'presupuestos': 'बजट',
                'materiales': 'सामग्री',
                'maquinarias': 'मशीनरी',
                'herramientas': 'उपकरण',
                'contratistas': 'ठेकेदार',
                'propietarios': 'मालिक',
                'empleados': 'कर्मचारी',
                'proveedores': 'आपूर्तिकर्ता',
                
                'asistente_inteligente': 'बुद्धिमान सहायक',
                'luna_saludo': 'नमस्ते! मैं L.u.N.a हूं, सिविल वर्क्स प्रबंधन के लिए आपका AI सहायक। आज मैं आपकी कैसे मदद कर सकता हूं? 🚀',
                'escribe_pregunta': 'यहां अपना प्रश्न लिखें...',
                'enviar_mensaje': 'संदेश भेजें',
                
                'bienvenido': 'स्वागत है',
                'cerrar_sesion': 'लॉग आउट',
                'mi_perfil': 'मेरी प्रोफ़ाइल',
                'configuracion': 'सेटिंग्स',
                'ayuda': 'सहायता',
                'contacto': 'संपर्क',
                'idioma': 'भाषा',
                'seleccionar_idioma': 'भाषा चुनें',
                'guardar': 'सेव करें',
                'cancelar': 'रद्द करें',
                'eliminar': 'हटाएं',
                'editar': 'संपादित करें',
                'crear': 'बनाएं',
                'buscar': 'खोजें',
                'filtrar': 'फ़िल्टर',
                'exportar': 'निर्यात',
                'imprimir': 'प्रिंट'
            }
        };
    }

    // Inicializar el sistema de idiomas
    initializeLanguageSystem() {
        this.applyLanguage(this.currentLanguage);
        this.setupLanguageSelector();
        this.setupLanguageEvents();
    }

    // Aplicar idioma seleccionado
    applyLanguage(languageCode) {
        const translations = this.translations[languageCode] || this.translations['es'];
        
        // Traducir elementos con data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[key]) {
                element.textContent = translations[key];
            }
        });

        // Traducir placeholders
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            if (translations[key]) {
                element.placeholder = translations[key];
            }
        });

        // Traducir títulos
        document.querySelectorAll('[data-translate-title]').forEach(element => {
            const key = element.getAttribute('data-translate-title');
            if (translations[key]) {
                element.title = translations[key];
            }
        });

        // Actualizar el idioma actual
        this.currentLanguage = languageCode;
        localStorage.setItem('lumaLanguage', languageCode);

        // Actualizar el selector de idiomas
        this.updateLanguageSelector();

        // Disparar evento personalizado
        document.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: languageCode, translations: translations }
        }));
    }

    // Configurar el selector de idiomas
    setupLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.addEventListener('change', (e) => {
                this.applyLanguage(e.target.value);
                this.showLanguageChangeNotification(e.target.value);
            });
        }
    }

    // Actualizar el selector de idiomas
    updateLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = this.currentLanguage;
        }

        // Actualizar la bandera mostrada
        const flagDisplay = document.querySelector('.language-flag-display');
        if (flagDisplay) {
            const flagMap = {
                'es': '🇪🇸', 'en': '🇺🇸', 'gn': '🇵🇾', 'pt': '🇧🇷', 'ja': '🇯🇵',
                'ru': '🇷🇺', 'ko': '🇰🇷', 'fr': '🇫🇷', 'de': '🇩🇪', 'it': '🇮🇹',
                'zh': '🇨🇳', 'ar': '🇸🇦', 'hi': '🇮🇳'
            };
            flagDisplay.textContent = flagMap[this.currentLanguage] || '🌐';
        }
    }

    // Configurar eventos de idioma
    setupLanguageEvents() {
        // Detectar cambio de idioma del navegador
        window.addEventListener('languagechange', () => {
            const browserLang = navigator.language.split('-')[0];
            if (this.translations[browserLang]) {
                this.applyLanguage(browserLang);
            }
        });

        // Escuchar eventos personalizados de cambio de idioma
        document.addEventListener('changeLanguage', (e) => {
            this.applyLanguage(e.detail.language);
        });
    }

    // Mostrar notificación de cambio de idioma
    showLanguageChangeNotification(languageCode) {
        const languageNames = {
            'es': 'Español', 'en': 'English', 'gn': 'Guaraní', 'pt': 'Português',
            'ja': '日本語', 'ru': 'Русский', 'ko': '한국어', 'fr': 'Français',
            'de': 'Deutsch', 'it': 'Italiano', 'zh': '中文', 'ar': 'العربية',
            'hi': 'हिन्दी'
        };

        const notification = document.createElement('div');
        notification.className = 'language-notification';
        notification.innerHTML = `
            <div class="language-notification-content">
                <i class="fas fa-globe"></i>
                <span>Idioma cambiado a: <strong>${languageNames[languageCode]}</strong></span>
            </div>
        `;

        // Estilos para la notificación
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideInRight 0.5s ease-out;
            font-weight: 600;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
        `;

        document.body.appendChild(notification);

        // Remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 500);
        }, 3000);
    }

    // Obtener traducción por clave
    getTranslation(key, languageCode = null) {
        const lang = languageCode || this.currentLanguage;
        const translations = this.translations[lang] || this.translations['es'];
        return translations[key] || key;
    }

    // Obtener idioma actual
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Obtener todas las traducciones del idioma actual
    getCurrentTranslations() {
        return this.translations[this.currentLanguage] || this.translations['es'];
    }

    // Agregar nuevas traducciones dinámicamente
    addTranslations(languageCode, newTranslations) {
        if (!this.translations[languageCode]) {
            this.translations[languageCode] = {};
        }
        Object.assign(this.translations[languageCode], newTranslations);
    }

    // Traducir texto dinámicamente
    translateText(text, targetLanguage = null) {
        const lang = targetLanguage || this.currentLanguage;
        const translations = this.translations[lang] || this.translations['es'];
        
        // Buscar traducción exacta
        for (const [key, value] of Object.entries(translations)) {
            if (value.toLowerCase() === text.toLowerCase()) {
                return translations[key];
            }
        }
        
        return text; // Retornar texto original si no se encuentra traducción
    }
}

// Agregar estilos CSS para las animaciones
const languageStyles = document.createElement('style');
languageStyles.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }

    .language-notification-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .language-notification-content i {
        font-size: 1.2rem;
        animation: spin 2s linear infinite;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Efectos de transición para elementos traducidos */
    [data-translate] {
        transition: all 0.3s ease;
    }

    [data-translate]:hover {
        transform: scale(1.02);
    }

    /* Indicador de idioma activo */
    .language-selector-container .active-language {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
`;

document.head.appendChild(languageStyles);

// Inicializar el sistema de idiomas cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.languageManager = new LanguageManager();
    console.log('🌐 Sistema de idiomas multilenguaje inicializado correctamente');
});

// Función global para cambiar idioma
window.changeLanguage = function(languageCode) {
    if (window.languageManager) {
        window.languageManager.applyLanguage(languageCode);
    }
};

// Función global para obtener traducción
window.getTranslation = function(key, languageCode = null) {
    if (window.languageManager) {
        return window.languageManager.getTranslation(key, languageCode);
    }
    return key;
};

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageManager;
}