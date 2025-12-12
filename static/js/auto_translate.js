// AUTO-TRADUCTOR UNIVERSAL PARA TODO EL SISTEMA L.u.M.a
// Se ejecuta automáticamente y traduce TODO el contenido

(function() {
    'use strict';
    
    // Configuración de traducciones automáticas
    const AUTO_TRANSLATIONS = {
        // Textos comunes del sistema
        'crear': { 'en': 'Create', 'ru': 'Создать', 'ja': '作成', 'it': 'Crea', 'fr': 'Créer' },
        'editar': { 'en': 'Edit', 'ru': 'Редактировать', 'ja': '編集', 'it': 'Modifica', 'fr': 'Modifier' },
        'eliminar': { 'en': 'Delete', 'ru': 'Удалить', 'ja': '削除', 'it': 'Elimina', 'fr': 'Supprimer' },
        'guardar': { 'en': 'Save', 'ru': 'Сохранить', 'ja': '保存', 'it': 'Salva', 'fr': 'Sauvegarder' },
        'cancelar': { 'en': 'Cancel', 'ru': 'Отменить', 'ja': 'キャンセル', 'it': 'Annulla', 'fr': 'Annuler' },
        'buscar': { 'en': 'Search', 'ru': 'Поиск', 'ja': '検索', 'it': 'Cerca', 'fr': 'Rechercher' },
        'filtrar': { 'en': 'Filter', 'ru': 'Фильтр', 'ja': 'フィルター', 'it': 'Filtra', 'fr': 'Filtrer' },
        'nombre': { 'en': 'Name', 'ru': 'Имя', 'ja': '名前', 'it': 'Nome', 'fr': 'Nom' },
        'descripcion': { 'en': 'Description', 'ru': 'Описание', 'ja': '説明', 'it': 'Descrizione', 'fr': 'Description' },
        'precio': { 'en': 'Price', 'ru': 'Цена', 'ja': '価格', 'it': 'Prezzo', 'fr': 'Prix' },
        'cantidad': { 'en': 'Quantity', 'ru': 'Количество', 'ja': '数量', 'it': 'Quantità', 'fr': 'Quantité' },
        'fecha': { 'en': 'Date', 'ru': 'Дата', 'ja': '日付', 'it': 'Data', 'fr': 'Date' },
        'estado': { 'en': 'Status', 'ru': 'Статус', 'ja': '状態', 'it': 'Stato', 'fr': 'État' },
        'activo': { 'en': 'Active', 'ru': 'Активный', 'ja': 'アクティブ', 'it': 'Attivo', 'fr': 'Actif' },
        'inactivo': { 'en': 'Inactive', 'ru': 'Неактивный', 'ja': '非アクティブ', 'it': 'Inattivo', 'fr': 'Inactif' },
        'total': { 'en': 'Total', 'ru': 'Итого', 'ja': '合計', 'it': 'Totale', 'fr': 'Total' },
        'acciones': { 'en': 'Actions', 'ru': 'Действия', 'ja': 'アクション', 'it': 'Azioni', 'fr': 'Actions' },
        'detalles': { 'en': 'Details', 'ru': 'Подробности', 'ja': '詳細', 'it': 'Dettagli', 'fr': 'Détails' },
        'telefono': { 'en': 'Phone', 'ru': 'Телефон', 'ja': '電話', 'it': 'Telefono', 'fr': 'Téléphone' },
        'email': { 'en': 'Email', 'ru': 'Электронная почта', 'ja': 'メール', 'it': 'Email', 'fr': 'Email' },
        'direccion': { 'en': 'Address', 'ru': 'Адрес', 'ja': '住所', 'it': 'Indirizzo', 'fr': 'Adresse' },
        'ciudad': { 'en': 'City', 'ru': 'Город', 'ja': '市', 'it': 'Città', 'fr': 'Ville' },
        'departamento': { 'en': 'Department', 'ru': 'Отдел', 'ja': '部門', 'it': 'Dipartimento', 'fr': 'Département' },
        'especialidad': { 'en': 'Specialty', 'ru': 'Специальность', 'ja': '専門', 'it': 'Specialità', 'fr': 'Spécialité' },
        'experiencia': { 'en': 'Experience', 'ru': 'Опыт', 'ja': '経験', 'it': 'Esperienza', 'fr': 'Expérience' },
        'calificacion': { 'en': 'Rating', 'ru': 'Рейтинг', 'ja': '評価', 'it': 'Valutazione', 'fr': 'Évaluation' },
        'disponible': { 'en': 'Available', 'ru': 'Доступно', 'ja': '利用可能', 'it': 'Disponibile', 'fr': 'Disponible' },
        'ocupado': { 'en': 'Busy', 'ru': 'Занят', 'ja': '忙しい', 'it': 'Occupato', 'fr': 'Occupé' },
        'salario': { 'en': 'Salary', 'ru': 'Зарплата', 'ja': '給料', 'it': 'Stipendio', 'fr': 'Salaire' },
        'cargo': { 'en': 'Position', 'ru': 'Должность', 'ja': 'ポジション', 'it': 'Posizione', 'fr': 'Poste' },
        'proyecto': { 'en': 'Project', 'ru': 'Проект', 'ja': 'プロジェクト', 'it': 'Progetto', 'fr': 'Projet' },
        'cliente': { 'en': 'Client', 'ru': 'Клиент', 'ja': 'クライアント', 'it': 'Cliente', 'fr': 'Client' },
        'ubicacion': { 'en': 'Location', 'ru': 'Местоположение', 'ja': '場所', 'it': 'Posizione', 'fr': 'Emplacement' },
        'presupuesto': { 'en': 'Budget', 'ru': 'Бюджет', 'ja': '予算', 'it': 'Budget', 'fr': 'Budget' },
        'progreso': { 'en': 'Progress', 'ru': 'Прогресс', 'ja': '進捗', 'it': 'Progresso', 'fr': 'Progrès' },
        'completado': { 'en': 'Completed', 'ru': 'Завершено', 'ja': '完了', 'it': 'Completato', 'fr': 'Terminé' },
        'en proceso': { 'en': 'In Progress', 'ru': 'В Процессе', 'ja': '進行中', 'it': 'In Corso', 'fr': 'En Cours' },
        'pendiente': { 'en': 'Pending', 'ru': 'Ожидание', 'ja': '保留中', 'it': 'In Attesa', 'fr': 'En Attente' },
        'cancelado': { 'en': 'Cancelled', 'ru': 'Отменено', 'ja': 'キャンセル済み', 'it': 'Annullato', 'fr': 'Annulé' },
        
        // Textos específicos del panel de administración
        'administración': { 'en': 'Administration', 'ru': 'Администрирование', 'ja': '管理', 'it': 'Amministrazione', 'fr': 'Administration' },
        'configuración': { 'en': 'Settings', 'ru': 'Настройки', 'ja': '設定', 'it': 'Impostazioni', 'fr': 'Paramètres' },
        'usuarios': { 'en': 'Users', 'ru': 'Пользователи', 'ja': 'ユーザー', 'it': 'Utenti', 'fr': 'Utilisateurs' },
        'permisos': { 'en': 'Permissions', 'ru': 'Разрешения', 'ja': '権限', 'it': 'Permessi', 'fr': 'Permissions' },
        'grupos': { 'en': 'Groups', 'ru': 'Группы', 'ja': 'グループ', 'it': 'Gruppi', 'fr': 'Groupes' },
        'sesiones': { 'en': 'Sessions', 'ru': 'Сессии', 'ja': 'セッション', 'it': 'Sessioni', 'fr': 'Sessions' },
        'logs': { 'en': 'Logs', 'ru': 'Журналы', 'ja': 'ログ', 'it': 'Log', 'fr': 'Journaux' },
        'backup': { 'en': 'Backup', 'ru': 'Резервная копия', 'ja': 'バックアップ', 'it': 'Backup', 'fr': 'Sauvegarde' },
        'restaurar': { 'en': 'Restore', 'ru': 'Восстановить', 'ja': '復元', 'it': 'Ripristina', 'fr': 'Restaurer' },
        'exportar': { 'en': 'Export', 'ru': 'Экспорт', 'ja': 'エクスポート', 'it': 'Esporta', 'fr': 'Exporter' },
        'importar': { 'en': 'Import', 'ru': 'Импорт', 'ja': 'インポート', 'it': 'Importa', 'fr': 'Importer' },
        
        // Textos de formularios
        'requerido': { 'en': 'Required', 'ru': 'Обязательно', 'ja': '必須', 'it': 'Richiesto', 'fr': 'Requis' },
        'opcional': { 'en': 'Optional', 'ru': 'Необязательно', 'ja': 'オプション', 'it': 'Opzionale', 'fr': 'Optionnel' },
        'seleccionar': { 'en': 'Select', 'ru': 'Выбрать', 'ja': '選択', 'it': 'Seleziona', 'fr': 'Sélectionner' },
        'cargar archivo': { 'en': 'Upload File', 'ru': 'Загрузить файл', 'ja': 'ファイルアップロード', 'it': 'Carica File', 'fr': 'Télécharger Fichier' },
        'enviar': { 'en': 'Submit', 'ru': 'Отправить', 'ja': '送信', 'it': 'Invia', 'fr': 'Envoyer' },
        'resetear': { 'en': 'Reset', 'ru': 'Сбросить', 'ja': 'リセット', 'it': 'Reset', 'fr': 'Réinitialiser' },
        
        // Mensajes del sistema
        'éxito': { 'en': 'Success', 'ru': 'Успех', 'ja': '成功', 'it': 'Successo', 'fr': 'Succès' },
        'error': { 'en': 'Error', 'ru': 'Ошибка', 'ja': 'エラー', 'it': 'Errore', 'fr': 'Erreur' },
        'advertencia': { 'en': 'Warning', 'ru': 'Предупреждение', 'ja': '警告', 'it': 'Avviso', 'fr': 'Avertissement' },
        'información': { 'en': 'Information', 'ru': 'Информация', 'ja': '情報', 'it': 'Informazione', 'fr': 'Information' },
        'confirmación': { 'en': 'Confirmation', 'ru': 'Подтверждение', 'ja': '確認', 'it': 'Conferma', 'fr': 'Confirmation' },
        
        // Navegación
        'anterior': { 'en': 'Previous', 'ru': 'Предыдущий', 'ja': '前へ', 'it': 'Precedente', 'fr': 'Précédent' },
        'siguiente': { 'en': 'Next', 'ru': 'Следующий', 'ja': '次へ', 'it': 'Successivo', 'fr': 'Suivant' },
        'primera': { 'en': 'First', 'ru': 'Первая', 'ja': '最初', 'it': 'Prima', 'fr': 'Première' },
        'última': { 'en': 'Last', 'ru': 'Последняя', 'ja': '最後', 'it': 'Ultima', 'fr': 'Dernière' },
        'página': { 'en': 'Page', 'ru': 'Страница', 'ja': 'ページ', 'it': 'Pagina', 'fr': 'Page' },
        'de': { 'en': 'of', 'ru': 'из', 'ja': 'の', 'it': 'di', 'fr': 'de' },
        'resultados': { 'en': 'Results', 'ru': 'Результаты', 'ja': '結果', 'it': 'Risultati', 'fr': 'Résultats' },
        'mostrando': { 'en': 'Showing', 'ru': 'Показано', 'ja': '表示中', 'it': 'Mostrando', 'fr': 'Affichage' },
        
        // PANEL DE ADMINISTRACIÓN DJANGO
        'sistema gestión paraguay': { 'en': 'PARAGUAY MANAGEMENT SYSTEM', 'ru': 'СИСТЕМА УПРАВЛЕНИЯ ПАРАГВАЙ', 'ja': 'パラグアイ管理システム', 'it': 'SISTEMA GESTIONE PARAGUAY', 'fr': 'SYSTÈME GESTION PARAGUAY' },
        'administración': { 'en': 'Administration', 'ru': 'Администрирование', 'ja': '管理', 'it': 'Amministrazione', 'fr': 'Administration' },
        'bienvenidos': { 'en': 'Welcome', 'ru': 'Добро пожаловать', 'ja': 'ようこそ', 'it': 'Benvenuti', 'fr': 'Bienvenue' },
        'ver el sitio': { 'en': 'View Site', 'ru': 'Посмотреть сайт', 'ja': 'サイトを見る', 'it': 'Vedi Sito', 'fr': 'Voir le Site' },
        'cambiar contraseña': { 'en': 'Change Password', 'ru': 'Изменить пароль', 'ja': 'パスワード変更', 'it': 'Cambia Password', 'fr': 'Changer Mot de Passe' },
        'cerrar sesión': { 'en': 'Logout', 'ru': 'Выйти', 'ja': 'ログアウト', 'it': 'Disconnetti', 'fr': 'Déconnexion' },
        'cambiar tema': { 'en': 'Change Theme', 'ru': 'Изменить тему', 'ja': 'テーマ変更', 'it': 'Cambia Tema', 'fr': 'Changer Thème' },
        'tema actual': { 'en': 'Current Theme', 'ru': 'Текущая тема', 'ja': '現在のテーマ', 'it': 'Tema Attuale', 'fr': 'Thème Actuel' },
        'automático': { 'en': 'Automatic', 'ru': 'Автоматический', 'ja': '自動', 'it': 'Automatico', 'fr': 'Automatique' },
        'panel de administración profesional': { 'en': 'Professional Administration Panel', 'ru': 'Профессиональная панель администрирования', 'ja': 'プロフェッショナル管理パネル', 'it': 'Pannello Amministrazione Professionale', 'fr': 'Panneau Administration Professionnel' },
        'autenticación y autorización': { 'en': 'Authentication and Authorization', 'ru': 'Аутентификация и авторизация', 'ja': '認証と認可', 'it': 'Autenticazione e Autorizzazione', 'fr': 'Authentification et Autorisation' },
        'nombre del modelo': { 'en': 'Model Name', 'ru': 'Название модели', 'ja': 'モデル名', 'it': 'Nome Modello', 'fr': 'Nom du Modèle' },
        'añadir vínculo': { 'en': 'Add Link', 'ru': 'Добавить ссылку', 'ja': 'リンク追加', 'it': 'Aggiungi Link', 'fr': 'Ajouter Lien' },
        'cambiar o ver el enlace de la lista': { 'en': 'Change or View List Link', 'ru': 'Изменить или просмотреть ссылку списка', 'ja': 'リストリンクの変更または表示', 'it': 'Cambia o Vedi Link Lista', 'fr': 'Changer ou Voir Lien Liste' },
        'grupos': { 'en': 'Groups', 'ru': 'Группы', 'ja': 'グループ', 'it': 'Gruppi', 'fr': 'Groupes' },
        'añadir': { 'en': 'Add', 'ru': 'Добавить', 'ja': '追加', 'it': 'Aggiungi', 'fr': 'Ajouter' },
        'modificar': { 'en': 'Modify', 'ru': 'Изменить', 'ja': '変更', 'it': 'Modifica', 'fr': 'Modifier' },
        'gestion': { 'en': 'Management', 'ru': 'Управление', 'ja': '管理', 'it': 'Gestione', 'fr': 'Gestion' },
        'carritos': { 'en': 'Carts', 'ru': 'Корзины', 'ja': 'カート', 'it': 'Carrelli', 'fr': 'Paniers' },
        'categorías': { 'en': 'Categories', 'ru': 'Категории', 'ja': 'カテゴリー', 'it': 'Categorie', 'fr': 'Catégories' },
        'contratos de contratistas': { 'en': 'Contractor Contracts', 'ru': 'Контракты подрядчиков', 'ja': '請負業者契約', 'it': 'Contratti Appaltatori', 'fr': 'Contrats Entrepreneurs' },
        'evaluaciones de proveedores': { 'en': 'Supplier Evaluations', 'ru': 'Оценки поставщиков', 'ja': 'サプライヤー評価', 'it': 'Valutazioni Fornitori', 'fr': 'Évaluations Fournisseurs' },
        'items de pedido': { 'en': 'Order Items', 'ru': 'Элементы заказа', 'ja': '注文アイテム', 'it': 'Articoli Ordine', 'fr': 'Articles Commande' },
        'items del carrito': { 'en': 'Cart Items', 'ru': 'Элементы корзины', 'ja': 'カートアイテム', 'it': 'Articoli Carrello', 'fr': 'Articles Panier' },
        'notificaciones': { 'en': 'Notifications', 'ru': 'Уведомления', 'ja': '通知', 'it': 'Notifiche', 'fr': 'Notifications' },
        'pedidos': { 'en': 'Orders', 'ru': 'Заказы', 'ja': '注文', 'it': 'Ordini', 'fr': 'Commandes' },
        'productos': { 'en': 'Products', 'ru': 'Продукты', 'ja': '製品', 'it': 'Prodotti', 'fr': 'Produits' },
        'productos de proveedores': { 'en': 'Supplier Products', 'ru': 'Продукты поставщиков', 'ja': 'サプライヤー製品', 'it': 'Prodotti Fornitori', 'fr': 'Produits Fournisseurs' },
        'tiendas': { 'en': 'Stores', 'ru': 'Магазины', 'ja': '店舗', 'it': 'Negozi', 'fr': 'Magasins' },
        'acciones recientes': { 'en': 'Recent Actions', 'ru': 'Недавние действия', 'ja': '最近のアクション', 'it': 'Azioni Recenti', 'fr': 'Actions Récentes' },
        'mis acciones': { 'en': 'My Actions', 'ru': 'Мои действия', 'ja': '私のアクション', 'it': 'Le Mie Azioni', 'fr': 'Mes Actions' },
        'ninguno disponible': { 'en': 'None Available', 'ru': 'Нет доступных', 'ja': '利用不可', 'it': 'Nessuno Disponibile', 'fr': 'Aucun Disponible' },
        
        // PÁGINA DE INICIO Y VISTAS GENERALES
        'plataforma profesional para la gestión de obras civiles y presupuestos en paraguay': {
            'en': 'Professional platform for civil works and budget management in Paraguay',
            'ru': 'Профессиональная платформа для управления гражданскими работами и бюджетом в Парагвае',
            'ja': 'パラグアイの土木工事と予算管理のためのプロフェッショナルプラットフォーム',
            'it': 'Piattaforma professionale per la gestione di lavori civili e budget in Paraguay',
            'fr': 'Plateforme professionnelle pour la gestion des travaux civils et budgets au Paraguay'
        },
        'ir al dashboard': {
            'en': 'GO TO DASHBOARD', 'ru': 'ПЕРЕЙТИ К ПАНЕЛИ', 'ja': 'ダッシュボードへ', 'it': 'VAI AL DASHBOARD', 'fr': 'ALLER AU TABLEAU DE BORD'
        },
        'características principales': {
            'en': 'MAIN FEATURES', 'ru': 'ОСНОВНЫЕ ФУНКЦИИ', 'ja': '主要機能', 'it': 'CARATTERISTICHE PRINCIPALI', 'fr': 'CARACTÉRISTIQUES PRINCIPALES'
        },
        'gestión de obras': {
            'en': 'Project Management', 'ru': 'Управление проектами', 'ja': 'プロジェクト管理', 'it': 'Gestione Progetti', 'fr': 'Gestion de Projets'
        },
        'administra todas tus obras civiles desde la planificación hasta la finalización con control total del progreso': {
            'en': 'Manage all your civil works from planning to completion with full progress control',
            'ru': 'Управляйте всеми вашими гражданскими работами от планирования до завершения с полным контролем прогресса',
            'ja': '計画から完成まで、すべての土木工事を進捗の完全な制御で管理',
            'it': 'Gestisci tutti i tuoi lavori civili dalla pianificazione al completamento con controllo totale del progresso',
            'fr': 'Gérez tous vos travaux civils de la planification à l\'achèvement avec un contrôle total du progrès'
        },
        'presupuestos profesionales': {
            'en': 'Professional Budgets', 'ru': 'Профессиональные бюджеты', 'ja': 'プロフェッショナル予算', 'it': 'Budget Professionali', 'fr': 'Budgets Professionnels'
        },
        'genera presupuestos detallados con cálculos automáticos, iva y formato paraguayo': {
            'en': 'Generate detailed budgets with automatic calculations, VAT and Paraguayan format',
            'ru': 'Создавайте детальные бюджеты с автоматическими расчетами, НДС и парагвайским форматом',
            'ja': '自動計算、VAT、パラグアイ形式で詳細な予算を作成',
            'it': 'Genera budget dettagliati con calcoli automatici, IVA e formato paraguaiano',
            'fr': 'Générez des budgets détaillés avec calculs automatiques, TVA et format paraguayen'
        },
        'control de materiales': {
            'en': 'Materials Control', 'ru': 'Контроль материалов', 'ja': '材料管理', 'it': 'Controllo Materiali', 'fr': 'Contrôle Matériaux'
        },
        'gestiona tu inventario de materiales con alertas de stock bajo y valorización automática': {
            'en': 'Manage your materials inventory with low stock alerts and automatic valuation',
            'ru': 'Управляйте своим инвентарем материалов с оповещениями о низких запасах и автоматической оценкой',
            'ja': '低在庫アラートと自動評価で材料在庫を管理',
            'it': 'Gestisci il tuo inventario materiali con avvisi di stock basso e valutazione automatica',
            'fr': 'Gérez votre inventaire de matériaux avec alertes de stock bas et évaluation automatique'
        },
        'gestión de maquinarias': {
            'en': 'Machinery Management', 'ru': 'Управление оборудованием', 'ja': '機械管理', 'it': 'Gestione Macchinari', 'fr': 'Gestion Machines'
        },
        'controla maquinarias pesadas con estados, mantenimiento y disponibilidad en tiempo real': {
            'en': 'Control heavy machinery with status, maintenance and real-time availability',
            'ru': 'Контролируйте тяжелую технику с состоянием, обслуживанием и доступностью в реальном времени',
            'ja': '状態、メンテナンス、リアルタイムの可用性で重機を制御',
            'it': 'Controlla macchinari pesanti con stato, manutenzione e disponibilità in tempo reale',
            'fr': 'Contrôlez les machines lourdes avec statut, maintenance et disponibilité en temps réel'
        },
        'control de herramientas': {
            'en': 'Tools Control', 'ru': 'Контроль инструментов', 'ja': 'ツール管理', 'it': 'Controllo Strumenti', 'fr': 'Contrôle Outils'
        },
        'administra herramientas con seguimiento de cantidad, estado y asignación a obras': {
            'en': 'Manage tools with quantity tracking, status and assignment to projects',
            'ru': 'Управляйте инструментами с отслеживанием количества, состоянием и назначением на проекты',
            'ja': '数量追跡、状態、プロジェクトへの割り当てでツールを管理',
            'it': 'Gestisci strumenti con tracciamento quantità, stato e assegnazione ai progetti',
            'fr': 'Gérez les outils avec suivi de quantité, statut et affectation aux projets'
        },
        'reportes avanzados': {
            'en': 'Advanced Reports', 'ru': 'Расширенные отчеты', 'ja': '高度なレポート', 'it': 'Report Avanzati', 'fr': 'Rapports Avancés'
        },
        'obtén estadísticas detalladas y exporta reportes en excel con datos completos': {
            'en': 'Get detailed statistics and export Excel reports with complete data',
            'ru': 'Получайте подробную статистику и экспортируйте отчеты Excel с полными данными',
            'ja': '詳細な統計を取得し、完全なデータでExcelレポートをエクスポート',
            'it': 'Ottieni statistiche dettagliate ed esporta report Excel con dati completi',
            'fr': 'Obtenez des statistiques détaillées et exportez des rapports Excel avec données complètes'
        },
        'sistema de roles': {
            'en': 'Role System', 'ru': 'Система ролей', 'ja': 'ロールシステム', 'it': 'Sistema Ruoli', 'fr': 'Système de Rôles'
        },
        'permisos completos para administradores, constructores, vendedores y clientes': {
            'en': 'Complete permissions for administrators, builders, sellers and clients',
            'ru': 'Полные разрешения для администраторов, строителей, продавцов и клиентов',
            'ja': '管理者、建設業者、販売者、顧客のための完全な権限',
            'it': 'Permessi completi per amministratori, costruttori, venditori e clienti',
            'fr': 'Permissions complètes pour administrateurs, constructeurs, vendeurs et clients'
        },
        'diseño responsive': {
            'en': 'Responsive Design', 'ru': 'Адаптивный дизайн', 'ja': 'レスポンシブデザイン', 'it': 'Design Responsive', 'fr': 'Design Responsive'
        },
        'accede desde cualquier dispositivo: pc, tablet o móvil con diseño adaptativo': {
            'en': 'Access from any device: PC, tablet or mobile with adaptive design',
            'ru': 'Доступ с любого устройства: ПК, планшет или мобильный с адаптивным дизайном',
            'ja': 'アダプティブデザインでPC、タブレット、モバイルのどのデバイスからでもアクセス',
            'it': 'Accedi da qualsiasi dispositivo: PC, tablet o mobile con design adattivo',
            'fr': 'Accédez depuis n\'importe quel appareil: PC, tablette ou mobile avec design adaptatif'
        },
        'seguridad total': {
            'en': 'Total Security', 'ru': 'Полная безопасность', 'ja': '完全なセキュリティ', 'it': 'Sicurezza Totale', 'fr': 'Sécurité Totale'
        },
        'sistema seguro con autenticación, encriptación y respaldo de datos': {
            'en': 'Secure system with authentication, encryption and data backup',
            'ru': 'Безопасная система с аутентификацией, шифрованием и резервным копированием данных',
            'ja': '認証、暗号化、データバックアップを備えた安全なシステム',
            'it': 'Sistema sicuro con autenticazione, crittografia e backup dei dati',
            'fr': 'Système sécurisé avec authentification, cryptage et sauvegarde des données'
        },
        'enlaces rápidos': {
            'en': 'Quick Links', 'ru': 'Быстрые ссылки', 'ja': 'クイックリンク', 'it': 'Link Rapidi', 'fr': 'Liens Rapides'
        },
        'iniciar sesión': {
            'en': 'Login', 'ru': 'Войти', 'ja': 'ログイン', 'it': 'Accedi', 'fr': 'Connexion'
        },
        'contacto': {
            'en': 'Contact', 'ru': 'Контакт', 'ja': '連絡先', 'it': 'Contatto', 'fr': 'Contact'
        },
        'fundador y creador': {
            'en': 'Founder and Creator', 'ru': 'Основатель и создатель', 'ja': '创設者兼作成者', 'it': 'Fondatore e Creatore', 'fr': 'Fondateur et Créateur'
        },
        'todos los derechos reservados': {
            'en': 'All Rights Reserved', 'ru': 'Все права защищены', 'ja': '全ての権利保護', 'it': 'Tutti i Diritti Riservati', 'fr': 'Tous Droits Réservés'
        },
        'hecho con': {
            'en': 'Made with', 'ru': 'Сделано с', 'ja': '作成', 'it': 'Fatto con', 'fr': 'Fait avec'
        },
        'en paraguay': {
            'en': 'in Paraguay', 'ru': 'в Парагвае', 'ja': 'パラグアイで', 'it': 'in Paraguay', 'fr': 'au Paraguay'
        },
        'gestión de maquinarias': {
            'en': 'Machinery Management', 'ru': 'Управление оборудованием', 'ja': '機械管理', 'it': 'Gestione Macchinari', 'fr': 'Gestion Machines'
        },
        'buscar maquinarias': {
            'en': 'Search machinery', 'ru': 'Поиск оборудования', 'ja': '機械を検索', 'it': 'Cerca macchinari', 'fr': 'Rechercher machines'
        },
        'todos los estados': {
            'en': 'All statuses', 'ru': 'Все статусы', 'ja': 'すべてのステータス', 'it': 'Tutti gli stati', 'fr': 'Tous les statuts'
        },
        'lista de maquinarias': {
            'en': 'Machinery List', 'ru': 'Список оборудования', 'ja': '機械リスト', 'it': 'Lista Macchinari', 'fr': 'Liste Machines'
        },
        'costo alquiler/día': {
            'en': 'Rental Cost/Day', 'ru': 'Стоимость аренды/день', 'ja': 'レンタル料金/日', 'it': 'Costo Noleggio/Giorno', 'fr': 'Coût Location/Jour'
        },
        'fecha creación': {
            'en': 'Creation Date', 'ru': 'Дата создания', 'ja': '作成日', 'it': 'Data Creazione', 'fr': 'Date Création'
        },
        'dashboard super': {
            'en': 'SUPER DASHBOARD', 'ru': 'СУПЕР ПАНЕЛЬ', 'ja': 'スーパーダッシュボード', 'it': 'SUPER DASHBOARD', 'fr': 'SUPER TABLEAU DE BORD'
        },
        'sistema de gestión en tiempo real - paraguay': {
            'en': 'Real-Time Management System - Paraguay', 'ru': 'Система управления в реальном времени - Парагвай', 'ja': 'リアルタイム管理システム - パラグアイ', 'it': 'Sistema Gestione Tempo Reale - Paraguay', 'fr': 'Système Gestion Temps Réel - Paraguay'
        },
        'ingresos': {
            'en': 'Revenue', 'ru': 'Доходы', 'ja': '収益', 'it': 'Ricavi', 'fr': 'Revenus'
        },
        'análisis visual avanzado': {
            'en': 'Advanced Visual Analysis', 'ru': 'Расширенный визуальный анализ', 'ja': '高度なビジュアル分析', 'it': 'Analisi Visiva Avanzata', 'fr': 'Analyse Visuelle Avancée'
        },
        'obras activas': {
            'en': 'Active Projects', 'ru': 'Активные проекты', 'ja': 'アクティブプロジェクト', 'it': 'Progetti Attivi', 'fr': 'Projets Actifs'
        },
        'presupuestos recientes': {
            'en': 'Recent Budgets', 'ru': 'Недавние бюджеты', 'ja': '最近の予算', 'it': 'Budget Recenti', 'fr': 'Budgets Récents'
        },
        'actividad en tiempo real': {
            'en': 'Real-Time Activity', 'ru': 'Активность в реальном времени', 'ja': 'リアルタイムアクティビティ', 'it': 'Attività Tempo Reale', 'fr': 'Activité Temps Réel'
        },
        'acciones rápidas': {
            'en': 'Quick Actions', 'ru': 'Быстрые действия', 'ja': 'クイックアクション', 'it': 'Azioni Rapide', 'fr': 'Actions Rapides'
        },
        'nueva obra': {
            'en': 'New Project', 'ru': 'Новый проект', 'ja': '新しいプロジェクト', 'it': 'Nuovo Progetto', 'fr': 'Nouveau Projet'
        },
        'nuevo material': {
            'en': 'New Material', 'ru': 'Новый материал', 'ja': '新しい材料', 'it': 'Nuovo Materiale', 'fr': 'Nouveau Matériau'
        },
        'ver obras': {
            'en': 'View Projects', 'ru': 'Просмотр проектов', 'ja': 'プロジェクトを見る', 'it': 'Vedi Progetti', 'fr': 'Voir Projets'
        },
        'todos los enlaces del sistema': {
            'en': 'All System Links', 'ru': 'Все ссылки системы', 'ja': 'すべてのシステムリンク', 'it': 'Tutti i Link Sistema', 'fr': 'Tous les Liens Système'
        },
        'dashboards': {
            'en': 'Dashboards', 'ru': 'Панели управления', 'ja': 'ダッシュボード', 'it': 'Dashboard', 'fr': 'Tableaux de Bord'
        },
        'dashboard principal': {
            'en': 'Main Dashboard', 'ru': 'Главная панель', 'ja': 'メインダッシュボード', 'it': 'Dashboard Principale', 'fr': 'Tableau de Bord Principal'
        },
        'dashboard increíble': {
            'en': 'Amazing Dashboard', 'ru': 'Невероятная панель', 'ja': '素晴らしいダッシュボード', 'it': 'Dashboard Incredibile', 'fr': 'Tableau de Bord Incroyable'
        },
        'dashboard paraguay': {
            'en': 'Paraguay Dashboard', 'ru': 'Панель Парагвай', 'ja': 'パラグアイダッシュボード', 'it': 'Dashboard Paraguay', 'fr': 'Tableau de Bord Paraguay'
        },
        'lista obras': {
            'en': 'Project List', 'ru': 'Список проектов', 'ja': 'プロジェクトリスト', 'it': 'Lista Progetti', 'fr': 'Liste Projets'
        },
        'obras finalizadas': {
            'en': 'Completed Projects', 'ru': 'Завершенные проекты', 'ja': '完了したプロジェクト', 'it': 'Progetti Completati', 'fr': 'Projets Terminés'
        },
        'lista presupuestos': {
            'en': 'Budget List', 'ru': 'Список бюджетов', 'ja': '予算リスト', 'it': 'Lista Budget', 'fr': 'Liste Budgets'
        },
        'nuevo presupuesto': {
            'en': 'New Budget', 'ru': 'Новый бюджет', 'ja': '新しい予算', 'it': 'Nuovo Budget', 'fr': 'Nouveau Budget'
        },
        'solicitar presupuesto': {
            'en': 'Request Budget', 'ru': 'Запросить бюджет', 'ja': '予算をリクエスト', 'it': 'Richiedi Budget', 'fr': 'Demander Budget'
        },
        'presupuesto avanzado': {
            'en': 'Advanced Budget', 'ru': 'Расширенный бюджет', 'ja': '高度な予算', 'it': 'Budget Avanzato', 'fr': 'Budget Avancé'
        },
        'lista materiales': {
            'en': 'Materials List', 'ru': 'Список материалов', 'ja': '材料リスト', 'it': 'Lista Materiali', 'fr': 'Liste Matériaux'
        },
        'lista maquinarias': {
            'en': 'Machinery List', 'ru': 'Список оборудования', 'ja': '機械リスト', 'it': 'Lista Macchinari', 'fr': 'Liste Machines'
        },
        'nueva maquinaria': {
            'en': 'New Machinery', 'ru': 'Новое оборудование', 'ja': '新しい機械', 'it': 'Nuovo Macchinario', 'fr': 'Nouvelle Machine'
        },
        'lista herramientas': {
            'en': 'Tools List', 'ru': 'Список инструментов', 'ja': 'ツールリスト', 'it': 'Lista Strumenti', 'fr': 'Liste Outils'
        },
        'nueva herramienta': {
            'en': 'New Tool', 'ru': 'Новый инструмент', 'ja': '新しいツール', 'it': 'Nuovo Strumento', 'fr': 'Nouvel Outil'
        },
        'gestión usuarios': {
            'en': 'User Management', 'ru': 'Управление пользователями', 'ja': 'ユーザー管理', 'it': 'Gestione Utenti', 'fr': 'Gestion Utilisateurs'
        },
        'reportes avanzados': {
            'en': 'Advanced Reports', 'ru': 'Расширенные отчеты', 'ja': '高度なレポート', 'it': 'Report Avanzati', 'fr': 'Rapports Avancés'
        },
        'reporte completo': {
            'en': 'Complete Report', 'ru': 'Полный отчет', 'ja': '完全なレポート', 'it': 'Report Completo', 'fr': 'Rapport Complet'
        }
    };
    
    class AutoTranslator {
        constructor() {
            this.currentLanguage = localStorage.getItem('lumaLanguage') || 'es';
            this.init();
        }
        
        init() {
            this.setupObserver();
            this.translateExistingContent();
            
            // Escuchar cambios de idioma
            document.addEventListener('changeLanguage', (e) => {
                this.currentLanguage = e.detail.language;
                setTimeout(() => this.translateExistingContent(), 100);
            });
        }
        
        setupObserver() {
            // Observer para contenido dinámico
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach((node) => {
                            if (node.nodeType === Node.ELEMENT_NODE) {
                                this.translateElement(node);
                            }
                        });
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        translateExistingContent() {
            // Traducir elementos con data-translate primero
            document.querySelectorAll('[data-translate]').forEach(element => {
                const key = element.dataset.translate;
                const translation = this.getTranslation(key);
                if (translation && translation !== key) {
                    element.textContent = translation;
                }
            });
            
            // Traducir todo el contenido existente
            this.translateTables();
            this.translateButtons();
            this.translateForms();
            this.translateLabels();
            this.translatePlaceholders();
            this.translateAdminContent();
            this.translateGenericText();
        }
        
        translateElement(element) {
            // Traducir un elemento específico y sus hijos
            this.translateElementText(element);
            element.querySelectorAll('*').forEach(child => {
                this.translateElementText(child);
            });
        }
        
        translateElementText(element) {
            if (element.children.length === 0 && element.textContent.trim()) {
                const text = element.textContent.trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    element.textContent = translation;
                }
            }
        }
        
        translateTables() {
            // Traducir encabezados de tablas
            document.querySelectorAll('th, .table-header').forEach(th => {
                const text = th.textContent.trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    th.textContent = translation;
                }
            });
        }
        
        translateButtons() {
            // Traducir botones
            document.querySelectorAll('button, .btn, input[type="submit"], input[type="button"]').forEach(btn => {
                const text = (btn.textContent || btn.value || '').trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    if (btn.textContent) {
                        btn.textContent = translation;
                    } else if (btn.value) {
                        btn.value = translation;
                    }
                }
            });
        }
        
        translateForms() {
            // Traducir labels de formularios
            document.querySelectorAll('label').forEach(label => {
                const text = label.textContent.trim().toLowerCase().replace(':', '');
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    label.textContent = translation + (label.textContent.includes(':') ? ':' : '');
                }
            });
        }
        
        translateLabels() {
            // Traducir etiquetas y títulos
            document.querySelectorAll('h1, h2, h3, h4, h5, h6, .title, .label').forEach(element => {
                const text = element.textContent.trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    element.textContent = translation;
                }
            });
        }
        
        translatePlaceholders() {
            // Traducir placeholders
            document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(input => {
                const placeholder = input.placeholder.toLowerCase();
                const translation = this.getTranslation(placeholder);
                if (translation && translation !== placeholder) {
                    input.placeholder = translation;
                }
            });
        }
        
        translateAdminContent() {
            // Traducir contenido específico del panel de administración Django
            const adminSelectors = [
                '.admin-panel', '.django-admin', '#admin-content', 
                '#header', '#branding', '#user-tools', '#nav-sidebar',
                '.module', '.app-list', '.model-list', '.addlink', '.changelink',
                'h1', 'h2', 'h3', '.breadcrumbs', '.object-tools',
                'caption', 'th', 'td', '.form-row label', '.help'
            ];
            
            adminSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(element => {
                    if (element.children.length === 0 && element.textContent.trim()) {
                        const text = element.textContent.trim().toLowerCase();
                        const translation = this.getTranslation(text);
                        if (translation && translation !== text) {
                            element.textContent = translation;
                        }
                    }
                });
            });
            
            // Traducir enlaces específicos del admin
            document.querySelectorAll('a').forEach(link => {
                const text = link.textContent.trim().toLowerCase();
                const translation = this.getTranslation(text);
                if (translation && translation !== text) {
                    link.textContent = translation;
                }
            });
        }
        
        translateGenericText() {
            // Traducir texto genérico en elementos comunes
            const selectors = [
                '.card-title', '.card-text', '.alert', '.badge', '.chip',
                '.menu-item', '.nav-item', '.dropdown-item', '.list-item',
                '.status', '.tag', '.category', '.type', '.role',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div',
                '.feature-title', '.feature-description', '.footer-text'
            ];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(element => {
                    if (element.children.length === 0 && element.textContent.trim()) {
                        const text = element.textContent.trim().toLowerCase();
                        const translation = this.getTranslation(text);
                        if (translation && translation !== text) {
                            element.textContent = translation;
                        }
                    }
                });
            });
            
            // Traducir textos largos específicos
            this.translateLongTexts();
        },
        
        translateLongTexts() {
            // Traducir textos largos y descripciones
            document.querySelectorAll('*').forEach(element => {
                if (element.children.length === 0 && element.textContent.trim().length > 10) {
                    const text = element.textContent.trim().toLowerCase();
                    const translation = this.getTranslation(text);
                    if (translation && translation !== text) {
                        element.textContent = translation;
                    }
                }
            });
        }
        
        getTranslation(text) {
            const cleanText = text.toLowerCase().trim();
            const translations = AUTO_TRANSLATIONS[cleanText];
            
            if (translations && translations[this.currentLanguage]) {
                return translations[this.currentLanguage];
            }
            
            return null;
        }
    }
    
    // Inicializar el auto-traductor cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new AutoTranslator();
        });
    } else {
        new AutoTranslator();
    }
    
    // Hacer disponible globalmente
    window.AutoTranslator = AutoTranslator;
    
})();