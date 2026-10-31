import pandas as pd

print("Excel okunuyor, 1-2 dakika surebilir...")
sayfalar = pd.read_excel("data/online_retail_II.xlsx", sheet_name=None)
df = pd.concat(sayfalar.values(), ignore_index=True)

df.columns = ["invoice", "stock_code", "description", "quantity",
              "invoice_date", "unit_price", "customer_id", "country"]

df.to_csv("data/online_retail_ii.csv", index=False)

print("Bitti!")
print("Satir sayisi:", len(df))
print("Ilk tarih:", df["invoice_date"].min())
print("Son tarih:", df["invoice_date"].max())
