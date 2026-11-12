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


## fct_satis (satış satırı başına 1 satır, resmi tatil bayrağıyla)
| Sütun | Anlamı | Tip |
|---|---|---|
| fatura_no | Fatura numarası | metin |
| urun_kodu | Ürün kodu | metin |
| urun_adi | Ürün adı (küçük harf) | metin |
| musteri_id | Müşteri numarası | tam sayı |
| ulke | Ülke | metin |
| adet | Satılan adet | tam sayı |
| birim_fiyat | Birim fiyat (£) | ondalık |
| satir_tutari | adet x birim_fiyat (£) | ondalık |
| satis_zamani | Satış tarih ve saati | zaman damgası |
| satis_tarihi | Satış günü | tarih |
| tatil_gunu_mu | Satış günü UK resmi tatiliyse 1, değilse 0 | 0 / 1 |

## dim_musteri (müşteri başına 1 satır, tüm dönem)
| Sütun | Anlamı | Tip |
|---|---|---|
| musteri_id | Müşteri numarası | tam sayı |
| ulke | Müşterinin ülkesi | metin |
| ilk_alisveris | Müşterinin ilk alışveriş günü | tarih |
| son_alisveris | Müşterinin son alışveriş günü | tarih |
| toplam_fatura | Tüm dönemdeki farklı fatura sayısı | tam sayı |
| toplam_harcama | Tüm dönemdeki toplam harcama (£) | ondalık |

Not: Bu tablo 9 Eylül 2011 sonrasını da içerdiği için churn modelinde özellik olarak kullanılmaz (veri sızıntısı olur). Model özellikleri `mart_musteri_rfm` tablosundan alınır.

## mart_segment_ozet (segment başına 1 satır)
| Sütun | Anlamı | Tip |
|---|---|---|
| segment | Sampiyon, Potansiyel, Risk Altinda, Kaybedilmis | metin |
| musteri_sayisi | Segmentteki müşteri sayısı | tam sayı |
| churn_yuzde | Segmentte kesme tarihinden sonraki 90 günde alışveriş yapmayanların yüzdesi | ondalık |
| ortalama_harcama | Segmentteki müşteri başına ortalama harcama (£, kesme tarihine kadar) | ondalık |
| toplam_harcama | Segmentin toplam harcaması (£) | ondalık |
| risk_altindaki_harcama | Churn eden müşterilerin toplam harcaması (£) | ondalık |

## mart_musteri_rfm için ek not
r_skor, f_skor ve m_skor `ntile(4)` ile hesaplanır. Eşit değerlerde sıralama müşteri numarasına göre sabitlenmiştir; böylece her `dbt run` aynı sonucu verir.
