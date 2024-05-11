// Получаем кэш сайта
self.addEventListener("install", e => {
	e.waitUntil(
		caches.open("static").then(cache => {
			return cache.addAll(["/", 
				"./static/css/main.css", 
				"./static/images/mysite.png",]);
		})
	);
});

self.addEventListener("fetch", e => {
	e.respondWith(
		caches.match(e.request).then(response => {
			return response || fetch(e.request);
		})
	);
});