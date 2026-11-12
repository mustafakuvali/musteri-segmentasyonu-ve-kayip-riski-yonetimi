select *
from {{ ref('mart_musteri_rfm') }}
where recency_gun < 0
   or frequency < 1
   or monetary <= 0