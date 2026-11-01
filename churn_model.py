"""
Churn tahmin modeli
Girdi : data/mart_musteri_rfm.parquet  (dbt martından export_mart.py ile üretilen)
Çıktı : data/churn_tahminleri.csv      (Power BI'a alınacak risk skorları)

Kurulum:  pip install pandas pyarrow scikit-learn matplotlib
Çalıştır: python churn_model.py   (proje klasörünün kökünden)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (roc_auc_score, average_precision_score, classification_report,
                             confusion_matrix, RocCurveDisplay)

RS = 42

# 1) Veri ----------------------------------------------------------------
df = pd.read_parquet("data/mart_musteri_rfm.parquet")
print("Müşteri sayısı:", len(df))
print("Churn oranı   :", round(df["churn_flag"].mean(), 3))

# 2) Özellikler ----------------------------------------------------------
# segment ve *_skor kolonları kullanılmıyor: zaten R/F/M'den türetilmiş (tekrar bilgi).
X = pd.DataFrame({
    "recency_gun": df["recency_gun"],
    "frequency":   df["frequency"],
    "log_monetary": np.log1p(df["monetary"].clip(lower=0)),
    "ort_fatura_tutari": df["monetary"] / df["frequency"],
    "uk_mi": (df["ulke"] == "United Kingdom").astype(int),
})
y = df["churn_flag"]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=RS)

# 3) Modeller ------------------------------------------------------------
modeller = {
    "Lojistik Regresyon": Pipeline([("scaler", StandardScaler()),
                                    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))]),
    "Random Forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                            class_weight="balanced", random_state=RS, n_jobs=-1),
    "Gradient Boosting": HistGradientBoostingClassifier(random_state=RS),
}

sonuc = {}
for ad, m in modeller.items():
    m.fit(X_tr, y_tr)
    p = m.predict_proba(X_te)[:, 1]
    sonuc[ad] = {"model": m, "proba": p,
                 "ROC-AUC": roc_auc_score(y_te, p),
                 "PR-AUC": average_precision_score(y_te, p)}
    print(f"{ad:20s} ROC-AUC={sonuc[ad]['ROC-AUC']:.3f}  PR-AUC={sonuc[ad]['PR-AUC']:.3f}")

# Baseline: sadece recency ile ne kadar tahmin edilebiliyor?
print("Baseline (sadece recency) ROC-AUC:", round(roc_auc_score(y_te, X_te["recency_gun"]), 3))

# 4) En iyi model için detaylı değerlendirme ----------------------------
en_iyi = max(sonuc, key=lambda k: sonuc[k]["ROC-AUC"])
print("\nEn iyi model:", en_iyi)
p = sonuc[en_iyi]["proba"]
tahmin = (p >= 0.5).astype(int)
print(classification_report(y_te, tahmin, target_names=["Kaldı", "Churn"]))
print("Karışıklık matrisi:\n", confusion_matrix(y_te, tahmin))

fig, ax = plt.subplots(figsize=(6, 5))
for ad, s in sonuc.items():
    RocCurveDisplay.from_predictions(y_te, s["proba"], name=ad, ax=ax)
ax.plot([0, 1], [0, 1], "k--", alpha=0.4)
ax.set_title("ROC Eğrileri")
fig.savefig("data/roc_egrileri.png", dpi=150, bbox_inches="tight")

# Özellik önemi (permütasyon)
pi = permutation_importance(sonuc[en_iyi]["model"], X_te, y_te, scoring="roc_auc",
                            n_repeats=10, random_state=RS)
onem = pd.Series(pi.importances_mean, index=X.columns).sort_values(ascending=False)
print("\nÖzellik önemi (ROC-AUC düşüşü):\n", onem.round(4))

# 5) Tüm müşteriler için risk skoru (Power BI için) ---------------------
# cross_val_predict: her müşterinin skoru, onu görmemiş bir modelden gelir (dürüst skor)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RS)
oof = cross_val_predict(modeller[en_iyi], X, y, cv=cv, method="predict_proba")[:, 1]

cikti = df[["musteri_id", "segment", "churn_flag"]].copy()
cikti["churn_olasiligi"] = oof.round(4)
cikti["risk_grubu"] = pd.cut(oof, bins=[-0.01, 0.33, 0.66, 1.0], labels=["Düşük", "Orta", "Yüksek"])
cikti.to_csv("data/churn_tahminleri.csv", index=False)
print("\nYazıldı: data/churn_tahminleri.csv")
print(cikti.groupby("segment")["churn_olasiligi"].mean().round(3))

