with satis as (
    select
        date_trunc('month', cast(satis_zamani as date)) as ay,
        count(distinct fatura_no)                       as fatura_sayisi,
        count(distinct musteri_id)                      as musteri_sayisi,
        round(sum(satir_tutari), 2)                     as ciro
    from {{ ref('stg_satis') }}
    group by 1
),

tatil as (
    select
        date_trunc('month', tatil_tarihi) as ay,
        count(*)                          as tatil_gun_sayisi
    from {{ ref('stg_tatil') }}
    group by 1
)

select
    s.ay,
    s.fatura_sayisi,
    s.musteri_sayisi,
    s.ciro,
    coalesce(t.tatil_gun_sayisi, 0) as tatil_gun_sayisi
from satis s
left join tatil t on s.ay = t.ay
order by s.ay