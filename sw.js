const IMAGE_CACHE = 'lebska-images-v1';
const IMAGE_MAX_AGE = 7 * 24 * 60 * 60 * 1000; // 7 days in ms

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const isImage = req.destination === 'image' ||
    /\.(webp|jpg|jpeg|png|gif|svg)(\?.*)?$/.test(url.pathname);

  if (!isImage) return;

  event.respondWith(
    caches.open(IMAGE_CACHE).then(cache =>
      cache.match(req).then(cached => {
        if (cached) {
          const cachedDate = cached.headers.get('sw-cached-at');
          if (cachedDate && Date.now() - Number(cachedDate) < IMAGE_MAX_AGE) {
            return cached;
          }
        }
        return fetch(req).then(response => {
          if (!response.ok) return response;
          const clone = response.clone();
          const headers = new Headers(clone.headers);
          headers.set('sw-cached-at', String(Date.now()));
          clone.blob().then(body => {
            cache.put(req, new Response(body, { status: clone.status, statusText: clone.statusText, headers }));
          });
          return response;
        }).catch(() => cached || new Response('', { status: 503 }));
      })
    )
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== IMAGE_CACHE).map(k => caches.delete(k)))
    )
  );
});
