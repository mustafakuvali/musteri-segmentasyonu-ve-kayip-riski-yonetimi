with ham as (

    select *
    from read_csv('../data/online_retail_ii.csv', header=true, all_varchar=true)

),

temiz as (

    select
        invoice                                          as fatura_no,
        stock_code                                       as urun_kodu,
        trim(lower(description))                         as urun_adi,
        try_cast(quantity as integer)                    as adet,
        try_cast(invoice_date as timestamp)              as satis_zamani,
        try_cast(unit_price as double)                   as birim_fiyat,
        cast(try_cast(customer_id as double) as integer) as musteri_id,
        country                                          as ulke
    from ham

)

select
    *,
    adet * birim_fiyat                                   as satir_tutari
from temiz
where musteri_id is not null
  and fatura_no not like 'C%'
  and adet > 0
  and birim_fiyat > 0