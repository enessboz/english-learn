---
name: speak
description: Konuşma pratiği. Rol yapma/sohbet yapar, hataları sonda toplu düzeltir. Yeni ve due kelimeleri konuşmaya yedirir.
---
1. `python3 tools/srs.py due --limit 8` ile kelimeleri al (yoksa son öğrenilenler).
2. Bir senaryo seç (kafe, mülakat, toplantı, tartışma, müşteri görüşmesi; kullanıcı iş ister ise gerçek iş senaryosu).
3. Sohbet et: kısa, doğal repliklerle. Konuşma sırasında düzeltme için akışı **bölme**. Hedef kelimeleri kullanıcıyı kullanmaya yönlendirecek sorular sor.
4. 8-10 turdan sonra bitir ve geri bildirim ver:
   - Hata tablosu: söylediğin -> doğrusu -> neden (en fazla 5 madde)
   - Daha doğal alternatifler (2-3)
   - Kullanılan hedef kelimeler: kullandıysa `srs.py grade <kelime> pass`
5. Tekrarlayan hataları `data/mistakes.md`'ye ekle. `srs.py log -n "speak: <senaryo>"`.
Not: Ses girişi yoksa kullanıcı yazılı konuşsun, "sesli söyle, sonra yaz" şeklinde telaffuz tavsiyesi ver.
