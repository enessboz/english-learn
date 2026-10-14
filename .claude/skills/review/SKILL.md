---
name: review
description: Vadesi gelen kelimeleri tekrar ettirir (aralıklı tekrar). Önce hatırlat, sonra bağlamda sor. "tekrar", "due", "ne unuttum" denince kullan.
---
1. `python3 tools/srs.py due` ile listeyi al. Boşsa kullanıcıya söyle ve `/learn-words` öner.
2. Her kelime için kart gibi düz sorma; sırayla karıştır:
   - Yeni bir cümlede boşluk doldurma
   - "Bu kelimeyi kullanarak bir cümle yaz"
   - Türkçe anlamı verip İngilizcesini sor
   Kelimeyi önce kullanıcı hatırlamaya çalışsın, ipucunu sonra ver.
3. Sonuç: doğru -> `python3 tools/srs.py grade "<kelime>" pass`, yanlış/ipucuyla -> `fail`.
4. Sonda 3-5 cümlelik mini metin yaz, bu oturumun kelimelerini içine yerleştir (bağlamla pekiştir).
5. `srs.py log -n "review"`; kaç tanesi kaldı, yarın kaç tane gelecek söyle.
