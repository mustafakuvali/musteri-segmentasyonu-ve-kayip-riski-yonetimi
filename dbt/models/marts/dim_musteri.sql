select
    musteri_id,
    max(ulke)                         as ulke,
    min(satis_tarihi)                 as ilk_alisveris,
    max(satis_tarihi)                 as son_alisveris,
    count(distinct fatura_no)         as toplam_fatura,
    round(sum(satir_tutari), 2)       as toplam_harcama
from {{ ref('fct_satis') }}
group by musteri_id