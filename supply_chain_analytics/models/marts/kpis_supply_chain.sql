with fct_orders as (
    select * from {{ ref('fct_orders') }}
),

kpis as (
    select
        -- Volume
        count(order_id) as total_orders,
        sum(num_of_item) as total_items_delivered,
        round(sum(order_revenue), 2) as total_revenue,

        -- On-Time Delivery
        countif(is_on_time = true) as orders_on_time,
        round(
            countif(is_on_time = true) / count(order_id) * 100, 2
        ) as on_time_delivery_rate,

        -- Lead Time
        round(avg(lead_time_days), 1) as avg_lead_time_days,
        round(avg(processing_time_days), 1) as avg_processing_time_days,
        round(avg(shipping_time_days), 1) as avg_shipping_time_days,
        min(lead_time_days) as min_lead_time_days,
        max(lead_time_days) as max_lead_time_days,

        -- Revenue
        round(avg(order_revenue), 2) as avg_order_value,
        round(avg(num_of_item), 1) as avg_items_per_order

    from fct_orders
    where lead_time_days is not null
      and lead_time_days >= 0
)

select * from kpis