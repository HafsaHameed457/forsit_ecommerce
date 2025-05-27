USE ECommerceDB;


INSERT INTO category (id, name, description, created_at, updated_at)
VALUES 
    (UUID(), 'Electronics', 'Gadgets and electronic devices', NOW(), NOW()),
    (UUID(), 'Clothing', 'Apparel and fashion items', NOW(), NOW()),
    (UUID(), 'Home & Kitchen', 'Household and cooking items', NOW(), NOW()),
    (UUID(), 'Books', 'Fiction and non-fiction literature', NOW(), NOW()),
    (UUID(), 'Sports', 'Sports equipment and accessories', NOW(), NOW());


INSERT INTO products (id, name, description, cost_price, category_id, created_at, updated_at, remaining_items)
SELECT 
    UUID(),
    'iPhone 14',
    'Latest Apple smartphone',
    999.99,
    (SELECT id FROM category WHERE name = 'Electronics' LIMIT 1),
    NOW(),
    NOW(),
    100
UNION ALL
SELECT 
    UUID(),
    'Loose Top',
    'Cotton round-neck top baggy clothes',
    20.00,
    (SELECT id FROM category WHERE name = 'Clothing' LIMIT 1),
    NOW(),
    NOW(),
    250
UNION ALL
SELECT 
    UUID(),
    'Kite Runner',
    'Bestselling novel by Khaled Hosseini',
    12.99,
    (SELECT id FROM category WHERE name = 'Books' LIMIT 1),
    NOW(),
    NOW(),
    150;


INSERT INTO inventory (id, change_amount, reason, product_id, created_at)
SELECT 
    UUID(),
    250,
    'Initial stock',
    id,
    NOW()
FROM products 
WHERE name = 'Loose Top';


INSERT INTO inventory (id, change_amount, reason, product_id, created_at)
SELECT 
    UUID(),
    150,
    'Initial stock',
    id,
    NOW()
FROM products 
WHERE name = 'Kite Runner';

SET @product_id = (SELECT id FROM products WHERE name = 'Loose Top' LIMIT 1);
SET @cost_price = (SELECT cost_price FROM products WHERE name = 'Loose Top' LIMIT 1);
SET @selling_price = @cost_price * 1.2; -- 20% markup
SET @quantity = 50;
SET @order_id = UUID();


INSERT INTO orders (id, sale_date, total_amount, created_at, updated_at)
VALUES (@order_id, NOW(), @selling_price * @quantity, NOW(), NOW());


INSERT INTO sale_items (id, order_id, product_id, quantity, selling_price, created_at, updated_at)
VALUES (UUID(), @order_id, @product_id, @quantity, @selling_price, NOW(), NOW());


UPDATE products 
SET remaining_items = remaining_items - @quantity,
    updated_at = NOW()
WHERE id = @product_id;


INSERT INTO inventory (id, change_amount, reason, product_id, created_at)
VALUES (UUID(), -@quantity, 'Sale order', @product_id, NOW());


SELECT * FROM category;
SELECT * FROM products;
SELECT * FROM inventory WHERE product_id = @product_id;
SELECT * FROM orders;
SELECT * FROM sale_items WHERE order_id = @order_id;