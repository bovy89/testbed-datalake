select
    _id as order_id,
    customerId as customer_id,
    totalPrice,
    date as order_date,
    productsList,
    status as order_status
from {{ source('jaffle_shop','jaffle_shop__orders') }}
