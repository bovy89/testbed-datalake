select
    _id as customer_id,
    first_name,
    last_name,
    contact
from {{ source('jaffle_shop','jaffle_shop__customers') }}
