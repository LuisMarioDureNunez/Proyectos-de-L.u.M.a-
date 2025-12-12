// Service Worker para L.u.M.a PWA
const CACHE_NAME = 'luma-pwa-v1.0.0';
const OFFLINE_URL = '/offline/';

// Archivos esenciales para cachear
const ESSENTIAL_FILES = [
  '/',
  '/dashboard/',
  '/static/css/styles.css',
  '/static/js/scripts.js',
  '/static/images/logo.jpeg',
  '/static/images/gifluma.gif',
  '/static/manifest.json',
  OFFLINE_URL
];

// Instalación del Service Worker
self.addEventListener('install', event => {
  console.log('🚀 L.u.M.a Service Worker instalando...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 Cacheando archivos esenciales de L.u.M.a');
        return cache.addAll(ESSENTIAL_FILES);
      })
      .then(() => {
        console.log('✅ L.u.M.a PWA instalada correctamente');
        self.skipWaiting();
      })
      .catch(error => {
        console.error('❌ Error instalando L.u.M.a PWA:', error);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', event => {
  console.log('🔄 L.u.M.a Service Worker activando...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ L.u.M.a Service Worker activado');
      return self.clients.claim();
    })
  );
});

// Interceptar peticiones de red
self.addEventListener('fetch', event => {
  // Solo manejar peticiones GET
  if (event.request.method !== 'GET') return;
  
  // Estrategia: Cache First para recursos estáticos
  if (event.request.url.includes('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(event.request).then(response => {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseClone);
            });
            return response;
          });
        })
        .catch(() => {
          console.log('📡 Recurso no disponible offline:', event.request.url);
        })
    );
    return;
  }
  
  // Estrategia: Network First para páginas HTML
  if (event.request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          return caches.match(event.request)
            .then(response => {
              return response || caches.match(OFFLINE_URL);
            });
        })
    );
    return;
  }
  
  // Para otras peticiones, intentar red primero
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        return caches.match(event.request);
      })
  );
});

// Manejar mensajes del cliente
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Notificaciones push (opcional)
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body || 'Nueva actualización de L.u.M.a',
      icon: '/static/images/logo.jpeg',
      badge: '/static/images/gifluma.gif',
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: data.primaryKey || 1
      },
      actions: [
        {
          action: 'explore',
          title: 'Ver en L.u.M.a',
          icon: '/static/images/logo.jpeg'
        },
        {
          action: 'close',
          title: 'Cerrar',
          icon: '/static/images/logo.jpeg'
        }
      ]
    };
    
    event.waitUntil(
      self.registration.showNotification('L.u.M.a - Sistema Paraguay', options)
    );
  }
});

// Manejar clics en notificaciones
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/dashboard/')
    );
  }
});

console.log('🇵🇾 L.u.M.a Service Worker cargado - Hecho en Paraguay');