SELECT
    oi.id AS order_item_id,
    oi.order_id,
    oi.product_id,
    p.name AS product_name,
    p.category,
    p.brand,
    p.department,
    oi.sale_price,
    oi.status,
    u.country,
    u.state,
    oi.created_at
FROM {{ source('thelook_ecommerce', 'order_items') }} oi
LEFT JOIN {{ source('thelook_ecommerce', 'products') }} p ON oi.product_id = p.id
LEFT JOIN {{ source('thelook_ecommerce', 'orders') }} o ON oi.order_id = o.order_id
LEFT JOIN {{ source('thelook_ecommerce', 'users') }} u ON o.user_id = u.id