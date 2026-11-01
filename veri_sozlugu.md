# Veri Sözlüğü

## mart_musteri_rfm (müşteri başına 1 satır)
| Sütun | Anlamı | Tip |
|---|---|---|
| musteri_id | Müşteri numarası (anonim) | tam sayı |
| recency_gun | Kesme tarihinden önceki son alışverişin kaç gün önce olduğu | tam sayı |
| frequency | Kesme tarihine kadarki farklı fatura sayısı | tam sayı |
| monetary | Kesme tarihine kadarki toplam harcama (£) | ondalık |
| ulke | Müşterinin ülkesi | metin |
| r_skor | Recency puanı (1-4, 4 = en yeni alışveriş) | tam sayı |
| f_skor | Frequency puanı (1-4, 4 = en sık) | tam sayı |
| m_skor | Monetary puanı (1-4, 4 = en çok harcayan) | tam sayı |
| segment | Sampiyon, Potansiyel, Risk Altinda, Kaybedilmis | metin |
| churn_flag | 1 = kesme tarihinden sonraki 90 günde alışveriş yok, 0 = var | 0 / 1 |

Segment kuralı: r ve f skoru 3-4 ise Sampiyon; sadece r 3-4 ise Potansiyel;
sadece f 3-4 ise Risk Altinda; diğerleri Kaybedilmis.

## mart_aylik_satis (ay başına 1 satır)
| Sütun | Anlamı | Tip |
|---|---|---|
| ay | Ayın ilk günü | tarih |
| fatura_sayisi | O aydaki farklı fatura sayısı | tam sayı |
| musteri_sayisi | O ay alışveriş yapan farklı müşteri sayısı | tam sayı |
| ciro | O aydaki toplam satış tutarı (£) | ondalık |
| tatil_gun_sayisi | O aydaki UK resmi tatil günü sayısı | tam sayı |

## stg_satis (temizlenmiş satış satırları)
| Sütun | Anlamı | Tip |
|---|---|---|
| fatura_no | Fatura numarası | metin |
| urun_kodu | Ürün kodu | metin |
| urun_adi | Ürün adı (küçük harf) | metin |
| adet | Satılan adet | tam sayı |
| satis_zamani | Satış tarih ve saati | zaman damgası |
| birim_fiyat | Birim fiyat (£) | ondalık |
| musteri_id | Müşteri numarası | tam sayı |
| ulke | Ülke | metin |
| satir_tutari | adet x birim_fiyat | ondalık |

## stg_tatil (UK resmi tatilleri)
| Sütun | Anlamı | Tip |
|---|---|---|
| tatil_tarihi | Tatil günü | tarih |
| tatil_adi | Tatilin adı | metin |