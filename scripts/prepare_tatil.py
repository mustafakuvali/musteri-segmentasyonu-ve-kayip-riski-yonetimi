import csv
import os
import requests

klasor = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hedef = os.path.join(klasor, "data", "uk_bank_holidays.csv")

veri = requests.get("https://www.gov.uk/bank-holidays.json").json()
olaylar = veri["england-and-wales"]["events"]

with open(hedef, "w", newline="", encoding="utf-8") as f:
    yazici = csv.writer(f)
    yazici.writerow(["date", "title"])
    for o in olaylar:
        yazici.writerow([o["date"], o["title"]])

print("Bitti! Tatil sayisi:", len(olaylar))
print("Kaydedildi:", hedef)