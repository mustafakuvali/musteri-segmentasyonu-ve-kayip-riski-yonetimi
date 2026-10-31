select
    cast(date as date)   as tatil_tarihi,
    trim(title)          as tatil_adi
from read_csv('../data/uk_bank_holidays.csv', header=true, all_varchar=true)