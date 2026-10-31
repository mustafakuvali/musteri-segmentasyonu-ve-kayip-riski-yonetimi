import duckdb

sorgu = """
select
    count(*)                                                   as toplam_satir,
    count(distinct customer_id)                                as farkli_musteri,
    sum(case when customer_id is null then 1 else 0 end)       as musterisi_bos_satir,
    sum(case when invoice like 'C%' then 1 else 0 end)         as iptal_satir,
    sum(case when try_cast(quantity as integer) <= 0 then 1 else 0 end)    as adedi_sifir_ya_da_eksi,
    sum(case when try_cast(unit_price as double) <= 0 then 1 else 0 end)   as fiyati_sifir_ya_da_eksi,
    count(distinct invoice)                                    as farkli_fatura
from read_csv('data/online_retail_ii.csv', header=true, all_varchar=true)
"""

print(duckdb.sql(sorgu).df().T)