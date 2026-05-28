with order_logistics as (
    select * from {{ ref('int_order_logistics') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

final as (
    select
        ol.order_id,
        ol.user_id,
        u.first_name,
        u.last_name,
        u.state,
        u.city,
        u.country,
        ol.status,
        ol.created_at,
        ol.shipped_at,
        ol.delivered_at,
        ol.num_of_item,
        ol.lead_time_days,
        ol.processing_time_days,
        ol.shipping_time_days,
        ol.is_on_time,
        ol.order_revenue
    from order_logistics ol
    left join users u
        on ol.user_id = u.user_id
)

select * from final