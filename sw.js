const CACHE_NAME = 'mtv-cache-v1';
const urlsToCache = [
  '/',
  '/retro_tv_ultimate.html',
  '/manifest.json',
  '/magnets/en.json',
  '/magnets/fr.json',
  'https://cdn.skypack.dev/webtorrent@latest'
];

// Install event - cache essential files
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching essential files');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('Service Worker: Clearing old cache');
            return caches.delete(cache);
          }
        })
      );
    })
    .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache when offline, update cache when online
self.addEventListener('fetch', event => {
  console.log('Service Worker: Fetching ', event.request.url);
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        if (response) {
          console.log('Service Worker: Serving from cache:', event.request.url);
          return response;
        }
        
        // For magnet JSON files, try network first, then cache
        if (event.request.url.includes('/magnets/')) {
          return fetch(event.request)
            .then(response => {
              // Clone the response before caching
              const responseClone = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseClone);
                });
              return response;
            })
            .catch(() => {
              console.log('Service Worker: Network failed for magnets, trying cache fallback');
              return caches.match(event.request);
            });
        }
        
        // For other requests, fetch and cache
        return fetch(event.request)
          .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response before caching
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseClone);
              });
            
            return response;
          })
          .catch(() => {
            // If it's a request for an image, serve a placeholder
            if (event.request.url.match(/\.(jpg|jpeg|png|gif|webp|svg)$/)) {
              return new Response(
                '<svg width="192" height="192" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#333"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="#999">Offline</text></svg>',
                { headers: { 'Content-Type': 'image/svg+xml' } }
              );
            }
          });
      })
  );
});

// Background sync for updating magnet data (optional future feature)
self.addEventListener('sync', event => {
  if (event.tag === 'update-magnets') {
    event.waitUntil(updateMagnets());
  }
});

// Push notifications for new content (optional future feature)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New MTV content available!',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Explore new content',
        icon: '/images/checkmark.png'
      },
      {
        action: 'close',
        title: 'Close notification',
        icon: '/images/xmark.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('MTV Resurrection', options)
  );
});

// Helper function to update magnet data
async function updateMagnets() {
  try {
    const cache = await caches.open(CACHE_NAME);
    await cache.add('/magnets/en.json');
    await cache.add('/magnets/fr.json');
    console.log('Service Worker: Updated magnet data');
  } catch (error) {
    console.error('Service Worker: Failed to update magnets:', error);
  }
}
