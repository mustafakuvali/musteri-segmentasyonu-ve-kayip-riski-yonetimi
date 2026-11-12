select *
from (
    select
        (select sum(musteri_sayisi) from {{ ref('mart_segment_ozet') }}) as segment_toplam,
        (select count(*) from {{ ref('mart_musteri_rfm') }})            as rfm_toplam
) t
where segment_toplam != rfm_toplam