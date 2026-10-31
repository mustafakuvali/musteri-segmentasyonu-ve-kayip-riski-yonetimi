with ayar as (
    select date '2011-09-09' as kesme_tarihi
),

gecmis as (
    select s.*
    from {{ ref('stg_satis') }} s, ayar a
    where cast(s.satis_zamani as date) <= a.kesme_tarihi
),

gelecek as (
    select distinct s.musteri_id
    from {{ ref('stg_satis') }} s, ayar a
    where cast(s.satis_zamani as date) > a.kesme_tarihi
      and cast(s.satis_zamani as date) <= a.kesme_tarihi + 90
),

rfm as (
    select
        g.musteri_id,
        date_diff('day', cast(max(g.satis_zamani) as date),
                  (select kesme_tarihi from ayar))   as recency_gun,
        count(distinct g.fatura_no)                  as frequency,
        round(sum(g.satir_tutari), 2)                as monetary,
        max(g.ulke)                                  as ulke
    from gecmis g
    group by g.musteri_id
),

skorlu as (
    select
        *,
        ntile(4) over (order by recency_gun desc) as r_skor,
        ntile(4) over (order by frequency asc)    as f_skor,
        ntile(4) over (order by monetary asc)     as m_skor
    from rfm
)

select
    s.*,
    case
        when s.r_skor >= 3 and s.f_skor >= 3 then 'Sampiyon'
        when s.r_skor >= 3                   then 'Potansiyel'
        when s.f_skor >= 3                   then 'Risk Altinda'
        else                                      'Kaybedilmis'
    end as segment,
    case when gk.musteri_id is null then 1 else 0 end as churn_flag
from skorlu s
left join gelecek gk on s.musteri_id = gk.musteri_id