select
    _id as payment_id,
    orderId as order_id,
    paymentMethod as payment_method,
    status as payment_status,
    amount,
    date as payment_date

from {{ source('stripe','stripe__payments') }}
