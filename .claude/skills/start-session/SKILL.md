---
name: start-session
description: Oturumu başlatır. Vadesi gelen kelimeleri, seriyi ve bugünün planını gösterir. "başlayalım", "bugün ne yapıyoruz" denince kullan.
---
1. `python3 tools/srs.py brief` ve `python3 tools/srs.py due` çalıştır; `data/profile.md` ve `data/mistakes.md` oku.
2. Kısa özet ver: seri, due kelime sayısı, son sık hata.
3. Bugünün planını öner (kullanıcının süresine göre), varsayılan akış:
   - 10-15 dk `/review` (due kelimeler)
   - 30-40 dk `/learn-words` (yeni metin + kelimeler)
   - 15-20 dk `/speak`
   - kalan süre: `/work-english` (işten gerçek içerik)
4. Kullanıcıya hangisiyle başlayacağını sor, o skill'e geç.
