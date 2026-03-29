// public/sw.js

const CACHE_NAME = "traintrackr-v1";

// List of assets to cache
const ASSETS_TO_CACHE = [
  "/",
  "/index.html",
  "/icon.png",
  "/index.css",
  // Vite JS/CSS assets will be dynamically cached later
];

// Install event: cache static assets
self.addEventListener("install", (event) => {
  console.log("Service Worker: Installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate event: clean old caches
self.addEventListener("activate", (event) => {
  console.log("Service Worker: Activated");
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch event: serve cached assets first, then network
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedRes) => {
      return (
        cachedRes ||
        fetch(event.request)
          .then((response) => {
            // Dynamically cache new requests
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response.clone());
              return response;
            });
          })
          .catch(() => {
            // fallback for offline
            if (event.request.destination === "document") {
              return caches.match("/index.html");
            }
          })
      );
    })
  );
});