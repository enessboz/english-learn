---
name: gate-test
description: Chapter kapı testi. 4 beceriyi (konuşma, yazma, okuma, dinleme) test eder; geçerse sonraki chapter'a açar. "chapter testi", "kapıya hazırım", "bölümü geçeyim" denince kullan.
---
1. `python3 tools/chapter.py status` çalıştır. Otomatik şartlar (gün ve kelime) tamam değilse testi yapma; eksiği söyle ve nasıl tamamlanacağını planla.
2. `data/curriculum.json`'daki mevcut chapter'ın `gate` kriterlerini oku. Testler yeni içerikle yapılır (daha önce görülmemiş metin/senaryo), chapter kelimelerinin bir kısmını içersin.
3. Dört testi sırayla uygula, her biri için puan ver (0-100):
   - **Okuma:** gate'te belirtilen uzunlukta özgün metin + 8-10 soru. Puan = doğru yüzdesi. Geçme: 80.
   - **Yazma:** belirtilen kelime sayısı ve konu. Rubrik (her biri 25): görev, gramer, kelime, düzen. Geçme: 70.
   - **Konuşma:** öğrenci belirtilen sürede (yazıyla veya sesli söyleyip yazıya dökerek) anlatır; bir de 3 soruluk sohbet. Rubrik: akıcılık, doğruluk, kelime, görev. Geçme: 70.
   - **Dinleme:** öğrenci seçtiğimiz klibi dinler, transkripti yapıştırır (veya sen transkripti olan bir kaynak seçersin), 5-7 soruya hafızadan cevap verir. Geçme: 70.
4. Sonuç: her beceri için puan + 1-2 satır neden. Hataları `data/mistakes.md`'ye ekle.
5. Kaydet: `python3 tools/chapter.py gate pass -s "speaking=..,writing=..,reading=..,listening=.."` (hepsi geçtiyse) veya `gate fail -s "..."`. Kalırsan: zayıf beceri için 3 günlük plan yaz, 3 gün sonra yalnızca kalan becerileri tekrar test et.
6. Geçtiyse kutla, yeni chapter'ın can-do listesini ve ilk haftasını anlat, `python3 tools/chapter.py html` ile haritayı güncelle. Puanları şişirme; sınırdaysa dürüstçe kal.
