---
name: learn-words
description: Yeni kelimeleri kartla değil metin içinde öğretir. Paragraf okuma, aktif yazma ve konuşmaya hazırlık yapar. "yeni kelime", "metinle çalış" denince kullan.
---
Seviyeye uygun (`data/profile.md`) çalış. Konu kullanıcının ilgisinden veya işinden seçilsin; sormadıysa 1 soru sor.

**Adım 1 - Metin:** 120-200 kelimelik özgün bir metin yaz, 6-8 hedef kelimeyi **kalın** kullan. Tanım verme, önce kullanıcı anlamaya çalışsın.
**Adım 2 - Anlama:** 3 soru (1 ana fikir, 2 detay), cevapları kullanıcı İngilizce yazsın. Sonra kelime anlamlarını Türkçe/İngilizce ver, tahmin ettirerek.
**Adım 3 - Aktif kullanım:** Cloze (boşluk doldurma) 5 cümle, sonra kullanıcı her kelime ile **kendi cümlesini** yazsın. Düzelt (bkz. CLAUDE.md hata kuralı).
**Adım 4 - Konuşmaya köprü:** Kullanıcı bu kelimelerle 1 dakikalık bir anlatım yazsın/yazıya dökmeden söylesin; devamı `/speak`.
**Adım 5 - Kaydet:** Öğrenilen kelimeleri ekle:
`python3 tools/srs.py add "<kelime>" -m "<anlam>" -e "<örnek>" -t "<konu>"`
Sonunda `python3 tools/srs.py log -n "learn-words: <konu>"`.

Bir seferde en fazla 8 yeni kelime. Önceki metinlerde geçen kelimeleri yeni metne de yedirerek tekrarla.
