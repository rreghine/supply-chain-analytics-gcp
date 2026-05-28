with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

final as (
    select
        o.order_id,
        o.user_id,
        o.status,
        o.created_at,
        o.shipped_at,
        o.delivered_at,
        o.num_of_item,
        date_diff(o.delivered_at, o.created_at, day) as lead_time_days,
        date_diff(o.shipped_at, o.created_at, day) as processing_time_days,
        date_diff(o.delivered_at, o.shipped_at, day) as shipping_time_days,
        case
            when o.delivered_at <= timestamp_add(o.created_at, interval 5 day)
            then true
            else false
        end as is_on_time,
        sum(oi.sale_price) as order_revenue
    from orders o
    left join order_items oi
        on o.order_id = oi.order_id
    where o.status = 'Complete'
    group by 1,2,3,4,5,6,7,8,9,10,11
)

select * from final