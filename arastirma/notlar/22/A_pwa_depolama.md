# PWA on phones, status 2026: storage, offline, updates, background work

Status: DONE (first full pass). Labels: [D] official doc, [B] full text read, [O] search/summary only, [K] user/bug report (not Apple/Google statement).

## Corrections to the brief
- Brief: Safari "origin quota ~60% of total origin quota". WebKit 2023 post [B] says the origin quota is up to 60% of total DISK for browser apps (15% for other apps); overall quota is 80% of disk (browser apps) / 20% (other apps). The 60% is of disk, not of another quota.
- web.dev/articles/storage-for-the-web [O] says Safari "appears to allow about 1GB" and states this is unverified. Superseded by the WebKit 2023 post. Do not use 1GB.
- The 7-day rule is real [B] (WebKit ITP post), but home-screen web apps have their own days-of-use counter (see 1).

## 1. iOS Safari PWA (Add to Home Screen)
- Manifest with display standalone/fullscreen makes the site open as a Home Screen web app, outside Safari. [B] webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ ("that site becomes a Home Screen web app")
- Web Push for Home Screen web apps: iOS/iPadOS 16.4+. Permission request must follow direct user interaction (e.g., a subscribe tap). Uses Apple Push service; standard W3C Push API. [B] webkit.org/blog/13878
- Notification API: iOS 16.4+ with partial_implementation flag (MDN compat, BCD, Notification.json) [D-data]. Safari desktop 7+.
- Badging API: works for Home Screen web apps in 16.4+. [B] webkit.org/blog/13878
- Manifest id: supported in 16.4+. [B] webkit.org/blog/13878
- ITP 7-day cap: script-writable storage (IndexedDB, Cache, localStorage, etc.) deleted after 7 days of Safari use without user interaction on the site. Home Screen web apps are not part of Safari; they have their own counter, reset by use; WebKit does not expect their data to be deleted this way. [B] webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ (section "7-Day Cap on All Script-Writeable Storage"; the post date is not confirmed in the fetched text)
- Home Screen web app has its own storage container, separate from Safari tab storage. [O] web.dev/articles/storage-for-the-web (older, non-official; WebKit 2023 post [B] confirms same quota for standalone apps).

## 2. Storage quota (Cache API, IndexedDB, OPFS)
- Safari 17.0+ / iOS 17+ [B] webkit.org/blog/14403/updates-to-storage-policy/:
  - Origin quota: up to 60% of total disk (browser apps), 15% (other apps).
  - Overall quota: up to 80% of disk (browser), 20% (other apps). Reaching it causes eviction.
  - Standalone Home Screen web app: "has the same origin quota and overall quota as when it is opened in a browser app" [B] (same post).
  - Cross-origin frame quota: 10% of main frame origin quota. [B]
  - Eviction: LRU by origin; origins with an active page or in persistent mode are excluded. Default is best-effort. [B]
  - Errors: quota errors are thrown as QuotaExceededError; quota can change over time, so handle errors. [B]
- Persistence: navigator.storage.persist() / persisted() [B] WebKit post: WebKit grants based on heuristics such as "opened as a Home Screen Web App". BCD: StorageManager.persist/persisted Safari 15.2 (safari_ios mirror) [D-data: MDN BCD StorageManager.json]; estimate() Safari 17 [D-data].
- Chrome: up to 80% of total disk for browsers; an origin up to 60% of total disk; incognito ~5%. [O] web.dev (older; not re-verified against Chrome's own docs - Chrome docs not fetched).
- Firefox (older web.dev statement): 50% of free disk; eTLD+1 group up to 2GB. [O]
- Cache API: BCD Safari 11.1; iOS mirror. [D-data] api_Cache.json
- OPFS (getDirectory): BCD Safari 15.2; iOS mirror. [D-data] StorageManager.json
- web.dev recommends Cache Storage for app resources, OPFS for file content, IndexedDB for other data. [O] web.dev (not a Google-official policy but a Google article)

## 3. Offline work, service worker strategies, cache budget
- Stale-while-revalidate: serve cache immediately, fetch network to update cache. Workbox StaleWhileRevalidate "will always make a revalidation request, regardless of the age of the cached response." [B] developer.chrome.com/docs/workbox/modules/workbox-strategies
- Expiration: Workbox ExpirationPlugin supports maxEntries and maxAgeSeconds per cache. [B] workbox-strategies / workbox-expiration docs (example maxEntries: 10).
- Cache budget (30 frames x 2 MB = 60 MB): quota is not the binding limit on iOS (origin quota = 60% of disk per WebKit). The binding limit is memory during decode and playback, see 7. Practical: store frames as one compressed file or limited number, use ExpirationPlugin with maxEntries to bound cache size, and show frames via <img>/decoding=async rather than large canvas buffers. (Design suggestion, not sourced.)

## 4. Update flow (new version prompt, skipWaiting)
- New SW: browser downloads the worker in background; if byte-different, installs; new worker waits until old one controls zero clients. [B] web.dev/articles/service-worker-lifecycle
- Update check triggers: navigation to in-scope page, functional events (push, sync) unless checked within 24h. [B] same
- self.skipWaiting() makes the new worker activate right after install; call it after user interaction (e.g., postMessage from "Update now" button) to avoid breaking an open session. [B] same
- clients.claim() takes control of uncontrolled pages; can break pages that loaded without the worker. [B] same
- Default: browsers ignore HTTP cache on SW script update check (Chrome 68+). [B] same
- Recommended UX (suggestion): on updatefound / waiting state show "new version" toast; on tap, postMessage SKIP_WAITING and reload on controllerchange.

## 5. Web Share, File System Access, downloads
- Web Share (navigator.share): Safari 12.1; iOS mirror (supported on iOS). [D-data] Navigator.json. canShare Safari 14.
- File System Access pickers (showOpenFilePicker, showSaveFilePicker, showDirectoryPicker): Chrome 86; Safari false; iOS mirror (not supported on iOS). [D-data] Window.json.
- FileSystemHandle: Chrome 86, Safari 15.2 (for OPFS), Chrome Android 109. [D-data]
- Downloads on iOS: use <a download> with blob URL or Web Share file sharing (share files via navigator.share with files). Sharing file types: not verified in this pass. [pending verification]

## 6. Background sync and push
- Background Sync (SyncManager): Chrome 49, Firefox false, Safari false, iOS mirror (no). [D-data] api_SyncManager.json. MDN: "Limited availability" [O] MDN Background_Synchronization_API.
- Periodic Background Sync (PeriodicSyncManager): Chrome 80, Safari false, iOS mirror (no). [D-data] api_PeriodicSyncManager.json.
- Therefore on iOS, a page or SW cannot wake up itself after a long GitHub Actions run. Push is the only background-wake option, and only for Home Screen web apps 16.4+ with user permission. [B] webkit.org/blog/13878
- Push alternative design (suggestion): the Action's last step calls your own server, which sends a Web Push to the subscribed Home Screen app when the run finishes. Requires a push-capable server and subscription stored once; the app must be installed to Home Screen and permission granted.
- Badge: setAppBadge works from push handler in Home Screen app. [B] webkit.org/blog/13878

## 7. Memory limits in mobile browsers (iOS Safari)
- Apple publishes no numeric per-tab memory limit. Behavior: exceeding the process budget causes the system to kill the web content process and reload the tab (jetsam). [O] WebSearch summary of developer.apple.com forum 766309, WebKit bugs (summary only).
- WebKit Bugzilla 312727 [K] "Jetsam on some De Correspondent articles - works fine in Chrome and Firefox": reporter says Safari tab crashes and reloads on iPhone 13 and iPhone 16 Pro when scrolling a long article; the same page works on Android Chrome/Firefox including a 2013 Moto X with 2GB RAM. Bug report text fetched [B]; the page is a user report, not Apple's statement. A WebKit maintainer's confirmation of jetsam is mentioned in a search summary [O], not verified in the fetched text.
- Canvas/WebGL and image bitmaps are common triggers in search summaries [O]; esri guide not accessible (DNS error on community.esri.com; "ERİŞİLEMEDİ").
- Practical: avoid large canvas backing stores, avoid resizing canvases repeatedly, decode images on demand, release object URLs (URL.revokeObjectURL), and handle "page reloaded" by restoring state from IndexedDB or localStorage on load (state loss on reload is the failure mode for a mobile PWA, not quota).
- Apple's own WebKit iOS quota (sec 2) is generous; the real constraint for PNG frames is decoded-bitmap memory.

## Access log
- webkit.org/blog/14403/updates-to-storage-policy/ : fetched, full text. [B]
- webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ : fetched, text read (first ~5000 chars of 8644). [B]
- webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ : fetched, ITP section read. [B]
- web.dev/articles/storage-for-the-web : fetched, read. [O]
- web.dev/articles/service-worker-lifecycle : fetched, read. [B]
- developer.chrome.com/docs/workbox/caching-strategies-overview and /modules/workbox-strategies : fetched, read. [B]
- developer.mozilla.org StorageManager/persist, StorageManager/estimate, Background_Synchronization_API, ServiceWorkerRegistration/update : fetched. [O]
- MDN browser-compat-data JSON (raw.githubusercontent.com): SyncManager, PeriodicSyncManager, StorageManager, FileSystemHandle, Cache, Navigator, Window, Notification. [D-data] Fetched OK. Navigator/share.json and Window/showOpenFilePicker.json returned 404 (paths differ); values taken from parent files instead.
- bugs.webkit.org/show_bug.cgi?id=312727 : fetched, text read. [K]
- developer.apple.com/documentation/webkit/webkit-features-in-safari-15-1 : ERİŞİLEMEDİ (empty text).
- community.esri.com/... (memory guide): ERİŞİLEMEDİ (DNS ENOTFOUND in WebFetch).
- developer.apple.com/forums/thread/766309 and WebKit bugs 291677, 279637, 256366, 261685, 277848, 222097 : not fetched; only seen in search results [O].

## Open items
- Chrome's own storage docs not fetched (web.dev used instead).
- Share of files (downloads) on iOS: not verified.
- Date of the ITP post and the Apple forum threads: not confirmed from text.
