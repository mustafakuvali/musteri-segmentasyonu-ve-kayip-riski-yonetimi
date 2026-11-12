select *
from {{ ref('fct_satis') }}
where satir_tutari <= 0