# 23. Cloudflare Worker, Access ve GitHub

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A Worker, Access ve GitHub tetikleme; B Actions sınırları, çıktı depolama ve Python ortamı); sentezi ben yazdım. Ham notlar `arastirma/notlar/23/` içinde. Etiketler: **[B]** tam metin okundu, **[D]** resmi belge okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı. Sahibe yazılacak kurulum rehberi (`KURULUM.md`) ayrı bir belge olacak; bu belge o rehberin dayanağı.

## Kısa sonuç

**1. Mimari kaynaklı sınırlara sığıyor.** Telefon, Access ile korunan bir Worker'a istek gönderir; Worker Cloudflare Access JWT'sini doğrular, sonra GitHub'a `workflow_dispatch` çağrısı yapar. GitHub anahtarı Worker secret'ında kalır, tarayıcıya hiç gitmez [D ve H].

**2. Worker ücretsiz plan yeterli.** Günde 100 000 istek, istek başına 10 ms CPU, istek başına 50 alt istek; en çok 64 ortam değişkeni ve secret toplam [D]. Tek kullanıcılı tetikleyici için fazlasıyla yeterli.

**3. Kare çıktısı için Actions artifact yetmiyor; Cloudflare R2 ya da GitHub Releases seçilmeli.** 30 ile 100 kare × 2 ile 6 MB = 60 ile 600 MB bir koşuda. Ücretsiz planda artifact + paket depolama toplamda 500 MB [D]. R2: 10 GB ay ücretsiz, çıkış ücretsiz [D]. GitHub Releases: dosya başına 2 GiB, toplam sınırı yok [D].

**4. Herkese açık depo seçilirse standart çalıştırıcı 4 vCPU ve 16 GB, ücretsiz ve sınırsız; gizli depoda 2 vCPU ve 8 GB, aylık 12 dolarlık hak.** [D]. Fastscapelib 13. konudaki ölçümüme göre herkese açık depoda 4 milyon düğümlü koşuyu sığdırır [H].

## 1. Cloudflare Worker ve Access (A kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| Worker ücretsiz plan | 100 000 istek/gün (aşımda Error 1027), 10 ms CPU/istek (aşımda Error 1102), 50 alt istek/istek, 64 ortam değişkeni + secret, 5 KB değer, 64 MiB boyut | [D] |
| Secret | `wrangler secret put`; değer panoda ve Wrangler'da gizli; yeni sürüm hemen dağıtılır; yerelde `.dev.vars` | [D] |
| CORS | Worker `Access-Control-Allow-Origin`'i çağıranın origin'ine ayarlar, `Vary: Origin` ekler, OPTIONS ön denetimini yanıtlar | [D] |
| Access JWT | başlık `Cf-Access-Jwt-Assertion` (tarayıcıda `CF_Authorization` çerezi de var); anahtarlar `https://<takım>.cloudflareaccess.com/cdn-cgi/access/certs`; `iss` = takım alan adı, `aud` = uygulama AUD etiketi | [D] |
| Access ücretsiz plan | 50 kullanıcı (resmi fiyat sayfası sayıyı içermiyordu); tek seferlik PIN e-posta ile (10 dakika geçerli); GitHub kimlik sağlayıcı | [Ö ve D] |
| Service token | başlık adları indirilen sayfada yok | [Y] |
| Pages Functions ve Worker | Pages Functions Worker'lar üzerinde çalışır, Pages projesinin parçası; tek amaçlı tetikleyici için düz Worker daha basit | [D, kısa metin] |
| Dağıtım | `wrangler deploy`; GitHub Actions'tan dağıtım için gereken API token ayrıca doğrulanmadı | [Y] |

## 2. GitHub'ı tetikleme (A kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| `workflow_dispatch` | `POST /repos/{o}/{r}/actions/workflows/{id}/dispatches`, gövde `ref` (+ `inputs`), başarıda 204 (koşu kimliği dönmez) | [D] |
| `repository_dispatch` | `POST /repos/{o}/{r}/dispatches`, `event_type` + `client_payload`, 204 | [D] |
| Yetki | ince ayarlı kişisel erişim jetonu (fine-grained PAT): Actions yazma; tek depoya sınırlı | [D] |
| Koşu durumu | `GET /actions/runs`, `/actions/runs/{id}` (`status`, `conclusion`, `logs_url`, `artifacts_url`); loglar `logs_url` ile 302 zip; artifact `archive_download_url` (`/zip`) | [D] |
| Jeton ömrü | PAT 1 ile 366 gün (belirtilmezse varsayılan 30 gün, org politikası engelleyebilir) | [D] |
| Hız sınırı | PAT 5000 istek/saat; GitHub App installation token en az 5000/saat (12 500'e kadar ölçeklenir); `GITHUB_TOKEN` 1000/saat/depo; ikincil: 80 içerik isteği/dk, 500/saat; dispatch'in bu sayıma girip girmediği bulunamadı | [D ve Y] |

**Koşu kimliği sorunu [H].** `workflow_dispatch` koşu kimliğini döndürmediği için telefon "hangi koşu benimki" bilgisini sonradan `GET /actions/runs` ile bulmalı (en yeni koşu ya da `inputs` içine koyulan benzersiz bir etiketle eşleştirme). Bu bir çıkarım; belgede çözüm verilmemiş.

## 3. Güvenlik tasarımı (A kolu ve çıkarım)

- Anahtar Worker secret'ında kalır, tarayıcıya gitmez [D].
- Worker her istekte JWT'yi doğrular: imza, `iss`, `aud`, `exp` [D].
- Günlük koşu sınırı için ücretsiz plan limitleri tek başına yeterli değil; sayaç KV ya da Durable Object ile yazılmalı. Durable Object'in ücretsiz plandaki durumu doğrulanmadı; Worker rate-limiting bağlantı sayfası bulunamadı (indirilen sayfa yanlıştı) [Y].
- KV ücretsiz planda günde 1000 yazma, 1 GB depolama, 25 MiB değer [D, B kolu]: günlük sayaç için yeterli ama başka kullanım için sınırlı [H].
- Önerilen sıra [H]: Access ile giriş, Worker JWT'yi doğrular, günlük koşu sayısını kontrol eder, ancak sonra GitHub çağrısı yapar.

## 4. Actions çalıştırıcıları, depolama ve Python ortamı (B kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| Çalıştırıcı, herkese açık depo | `ubuntu-latest` 4 vCPU, 16 GB RAM, 14 GB SSD; ücretsiz, sınırsız | [D] |
| Çalıştırıcı, gizli depo | 2 vCPU, 8 GB RAM (7 GB değil), 14 GB SSD | [D] |
| Ücretsiz plan hakkı | aylık 12 dolarlık Actions işlem payı (2000 dakika değil); Linux 2 çekirdek dakikası 0,006 dolar, yani yaklaşık 2000 dakika (B kolunun türetmesi) | [D ve H] |
| Süre sınırları | iş 6 saat, iş akışı 35 gün, eşzamanlı iş (Ücretsiz) 20 | [D] |
| Artifact | ücretsiz planda depolama 500 MB (paketlerle ortak); varsayılan saklama 90 gün ve dosya başına boyut sınırı bulunamadı | [D ve Y] |
| GitHub Releases | dosya başına 2 GiB, toplam sınır yok, en çok 1000 dosya | [D] |
| GitHub Pages | site 1 GB, aylık 100 GB yumuşak bant genişliği | [D] |
| Git LFS | Ücretsiz 10 GiB depolama ve 10 GiB/ay bant genişliği | [D] |
| `actions/cache` | depo başına 10 GB, 7 gün kullanılmazsa silinir; teslimat için uygun değil | [D] |
| Cloudflare Pages | dosya başına 25 MiB, 20 000 dosya, ayda 500 derleme | [D] |
| Cloudflare R2 | 10 GB ay ücretsiz, çıkış ücretsiz, 1 milyon sınıf A ve 10 milyon sınıf B işlem ücretsiz | [D] |
| Workers KV | 1 GB depolama, 25 MiB değer, 1000 yazma/gün | [D] |
| `setup-python` | `cache: pip`, bağımlılık dosyası özetine göre anahtarlı | [D] |
| Fastscapelib | 0.3.0, CPython 3.10 ile 3.13 için Linux x86_64 (manylinux) tekerlek hazır, kaynak dağıtımı da var, cp314 yok; conda-forge'da da 0.3.0 | [D] |
| goSPL | 2026.7.14, yalnızca kaynak dağıtımı (Python ≥ 3.11), ağır bağımlılıklar (petsc4py, mpi4py, vtk); kaynaktan derleme beklenir, conda-forge muhtemelen daha hızlı; kurulum süresi ölçülmedi | [D ve Y] |

**Kare çıktısı kararı (B kolunun önerisi, benim eklememle) [H].** 30 ile 100 kare × 2 ile 6 MB = 60 ile 600 MB bir koşuda; artifact ücretsiz planda sığmaz. R2 en uygun (10 GB ücretsiz, çıkış ücretsiz); kare dosyaları 21. belgedeki 16 bit PNG ölçümüne göre 1 milyon hücre için yaklaşık 1,5 MB. Alternatif GitHub Releases (herkese açık depoda). Sahibin R2 ve Cloudflare hesabı zaten gerekeceği için R2 tutarlı.

**Herkese açık mı gizli mi [H].** Herkese açık depoda kod, veri ve çıktılar herkese açık olur; gizli depoda yalnızca 2 çekirdek ve 8 GB kalır ve aylık yaklaşık 2000 dakikayla sınırlıdır. 13. belgedeki ölçüm (4 çekirdek, 15 GB) gizli depoya doğrudan uymaz: 1 milyon düğüm bir adımı muhtemelen daha yavaş koşar. Bu karar sahibe ait.

## 5. Aracın varsayılan değerleri

| Parametre | Öneri | Etiket |
|---|---|---|
| Kimlik | Cloudflare Access (tek kullanıcı, OTP PIN ya da GitHub kimlik sağlayıcı) | [D ve Ö] |
| Tetikleyici | Worker + fine-grained PAT (Actions yazma, tek depo) | [D] |
| Jeton ömrü | PAT en çok 366 gün; yenileme hatırlatması | [D] |
| Koşu durumu | `GET /actions/runs/{id}`; kimlik `inputs` etiketiyle eşlenir | [D ve H] |
| Günlük sınır | KV sayacı (günde 1000 yazma sınırı içinde) | [D ve H] |
| Çıktı depolama | R2 (kare dosyaları), küçük özetler için Release | [D ve H] |
| Python ortamı | `setup-python` + pip önbelleği; Fastscapelib tekerlekle | [D] |
| Çalıştırıcı | herkese açık depo ise 4 vCPU, 16 GB; gizli ise 2 vCPU, 8 GB | [D] |
| Bildirim | koşu sonunda Worker'dan Web Push (22. belge) ya da yoklama | [H] |

## 6. Kaynaklar arası çelişkiler

- Gizli depoda RAM: 8 GB (resmi belge) ile 7 GB (promptumdaki).
- Ücretsiz Actions hakkı: 12 dolarlık işlem payı (resmi) ile 2000 dakika (promptumdaki); ikisi yaklaşık aynı.
- Access ücretsiz kullanıcı sayısı 50 yalnızca arama özetinde.

## 7. Bulunamayanlar ve doğrulanamayanlar

- Access ücretsiz plan 50 kullanıcı sınırının resmi doğrulaması; service token başlık adları.
- GitHub App installation token ömrü (genelde 1 saat, doğrulanmadı); dispatch'in içerik oluşturma ikincil limitine girip girmediği.
- Worker rate-limiting bağlantısı ve Durable Object'in ücretsiz plandaki durumu.
- Artifact varsayılan saklama süresi ve dosya başına boyut sınırı; büyük çalıştırıcı fiyatları; CI ortamında ölçülmüş kurulum süreleri; goSPL için conda kurulum süresi.
- `wrangler deploy` için gereken API token kapsamı.
- docs.github.com ve developers.cloudflare.com WebFetch'te DNS hatası verdi; curl ile erişildi, bot koruması atlatılmadı.

## 8. Promptumdaki hatalar (düzeltildi)

- Gizli depoda RAM 8 GB (7 GB değil).
- Ücretsiz plan "2000 dakika" yerine aylık 12 dolarlık işlem payı.
- Artifact "saklama 90 gün" ifadesi indirilen metinde yok.
- Access ücretsiz "50 kullanıcı" resmi sayfada doğrulanamadı.

## Başlıca kaynaklar

- Cloudflare Workers sınırları, Secrets, Access JWT doğrulama, R2/Pages/KV fiyatlandırması (developers.cloudflare.com)
- GitHub REST API: Actions iş akışları, dispatches, runs; GitHub Actions hosted runners, billing, artifacts, releases, Pages, LFS (docs.github.com)
- PyPI: fastscapelib 0.3.0 tekerlek listesi; goSPL
- Tam liste ve her bilginin kaynağı `arastirma/notlar/23/` içinde.
