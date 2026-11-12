select
    segment,
    count(*)                                                       as musteri_sayisi,
    round(avg(churn_flag) * 100, 1)                                as churn_yuzde,
    round(avg(monetary), 2)                                        as ortalama_harcama,
    round(sum(monetary), 2)                                        as toplam_harcama,
    round(sum(case when churn_flag = 1 then monetary else 0 end), 2) as risk_altindaki_harcama
from {{ ref('mart_musteri_rfm') }}
group by segment