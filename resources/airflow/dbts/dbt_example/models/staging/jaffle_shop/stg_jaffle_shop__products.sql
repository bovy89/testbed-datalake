select
    _id as product_id,
    name as product_name,
    price as price_euro,
    quantity,
    manufacturer as vendor
from {{ source('jaffle_shop','jaffle_shop__products') }}
