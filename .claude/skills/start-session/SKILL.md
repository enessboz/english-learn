---
name: start-session
description: Öğretmen modu. Günün dersini hazırlar ve baştan sona yürütür. "başlayalım", "bugün ne yapıyoruz", "derse başla" denince kullan.
---
Sen öğretmensin, kullanıcı öğrenci. Ne yapılacağını sen belirle, öğrenciye menü sunma. Önce hazırlan:

1. `python3 tools/chapter.py status`, `python3 tools/srs.py brief`, `python3 tools/srs.py due` çalıştır; `data/curriculum.json` (mevcut chapter), `data/profile.md`, `data/mistakes.md` oku.
2. Kısa karşılama (3-4 satır): chapter, kaçıncı gün, kelime ilerlemesi, due kelime sayısı, dünkü en sık hata. Seri koptuysa suçlamadan söyle.
3. Öğrenciye süresini sor (tam gün ~2.5 saat veya kısa gün ~1 saat). Cevaba göre `daily_plan` / `short_day_plan` blok sırasını uygula ve zamanı bloklara böl.
4. Dersi sırayla yürüt, her blokta ilgili skill'in talimatını izle:
   - Tekrar -> `/review`
   - Mini ders: chapter'ın o günkü gramer maddesi. 10 dk anlat (Türkçe, 3-4 örnek), 10 dk alıştırma yaptır. Her gün bir madde; konuyu bir önceki dersle bağla.
   - Okuma + kelime -> `/learn-words` (chapter temasıyla, kelime sayısı günlük en fazla 8-10)
   - Yazma -> `/work-english` veya chapter temasında kısa yazma görevi
   - Dinleme: önerilen kaynaklardan (curriculum.resources) seviyeye uygun 3-5 dk klip seç, adını ve ne arayacağını ver. Öğrenci dinlesin, sonra transkripti veya kendi özetini yapıştırsın; sen 3-5 soru sor.
   - Konuşma -> `/speak`
5. Her blok bitince çok kısa ilerleme notu ver ("2/6 blok tamam"). Ders sonunda: `python3 tools/srs.py log -n "lesson"`, bugünün özeti, yarına ödev (1 küçük görev) ve kapıya kalan şartlar.
6. Kapı şartları (gün ve kelime) tamamsa "kapıya hazırsın" de ve `/gate-test` öner.
7. Haftada bir `python3 tools/chapter.py html` çalıştırıp haritayı güncelle (`/roadmap`).
