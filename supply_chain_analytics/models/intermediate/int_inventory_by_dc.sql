with inventory as (
    select * from {{ ref('stg_inventory_items') }}
),

distribution_centers as (
    select * from {{ ref('stg_distribution_centers') }}
),

final as (
    select
        dc.distribution_center_id,
        dc.distribution_center_name,
        dc.latitude,
        dc.longitude,
        i.product_category,
        i.product_brand,
        count(i.inventory_item_id) as total_items,
        countif(i.sold_at is not null) as sold_items,
        countif(i.sold_at is null) as available_items,
        round(
            countif(i.sold_at is not null) / count(i.inventory_item_id) * 100, 2
        ) as sell_through_rate,
        round(avg(i.cost), 2) as avg_cost,
        round(avg(i.product_retail_price), 2) as avg_retail_price
    from inventory i
    left join distribution_centers dc
        on i.distribution_center_id = dc.distribution_center_id
    group by 1,2,3,4,5,6
)

select * from final