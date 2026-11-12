import os
import duckdb

klasor = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
con = duckdb.connect(klasor + "/dbt/retail.duckdb", read_only=True)

for tablo in ["mart_musteri_rfm", "mart_aylik_satis", "mart_segment_ozet"]:
    con.sql(f"copy (select * from {tablo}) to '{klasor}/data/{tablo}.parquet' (format parquet)")
    print("Yazildi:", tablo)