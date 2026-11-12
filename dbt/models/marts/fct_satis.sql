with tatiller as (
    select distinct tatil_tarihi
    from {{ ref('stg_tatil') }}
)

select
    s.fatura_no,
    s.urun_kodu,
    s.urun_adi,
    s.musteri_id,
    s.ulke,
    s.adet,
    s.birim_fiyat,
    s.satir_tutari,
    s.satis_zamani,
    cast(s.satis_zamani as date)                           as satis_tarihi,
    case when t.tatil_tarihi is not null then 1 else 0 end as tatil_gunu_mu
from {{ ref('stg_satis') }} s
left join tatiller t
    on cast(s.satis_zamani as date) = t.tatil_tarihi