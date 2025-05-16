use ECommerceDB;
-- Add data to category table 
INSERT INTO category (id, name, description)
VALUES 
    (UUID(), 'Electronics', 'Gadgets and electronic devices'),
    (UUID(), 'Clothing', 'Apparel and fashion items'),
    (UUID(), 'Home & Kitchen', 'Household and cooking items'),
    (UUID(), 'Books', 'Fiction and non-fiction literature'),
    (UUID(), 'Sports', 'Sports equipment and accessories');

-- Add data to products table 

INSERT INTO products (id, name, description, cost_price, category_id)
VALUES 
    (UUID(), 'iPhone 14', 'Latest Apple smartphone', 999.99, (SELECT id FROM category WHERE name = 'Electronics' LIMIT 1)),
    (UUID(), 'Loose Top', 'Cotton round-neck top baggy clothes', 20.00, (SELECT id FROM category WHERE name = 'Clothing' LIMIT 1)),
    (UUID(), 'Kite runner', 'Electric kitchen blender', 49.99, (SELECT id FROM category WHERE name = 'Books' LIMIT 1));
    

-- Add data to inventory table for products
    
INSERT INTO inventory (id, remaining_items, product_id)
SELECT 
    UUID(),                         
    250,               
    p.id
FROM products p
WHERE p.name = 'Loose Top';


INSERT INTO inventory (id, remaining_items, product_id)
SELECT 
    UUID(),                         
    250,               
    p.id
FROM products p
WHERE p.name = 'Kite runner';

-- Add data to inventory_history table for products to keep record
INSERT INTO inventory_history (id, change_amount, reason, product_id, changed_at)
SELECT 
    UUID(),          
    250,
    'Initial stock',
    i.product_id,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY
FROM inventory i
JOIN products p ON i.product_id = p.id
WHERE p.name = 'Loose Top';

INSERT INTO inventory_history (id, change_amount, reason, product_id, changed_at)
SELECT 
    UUID(),          
    250,
    'Initial stock',
    i.product_id,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY
FROM inventory i
JOIN products p ON i.product_id = p.id
WHERE p.name = 'Kite runner';

-- Take order for loose shirts
SELECT @pid:=id, @price:=cost_price 
FROM products 
WHERE name = 'Loose Top' 
LIMIT 1;

SET @new_order_id = UUID();
INSERT INTO orders (id, sale_date, total_amount)
VALUES (@new_order_id, NOW(), @price * 50 * 1.2);

SELECT * from inventory;

-- Add data to sales items table for loose shirts
INSERT INTO sale_items (id, order_id, product_id, quantity, selling_price)
VALUES (UUID(), @new_order_id, @pid, 50, @price * 1.2);

Select @pid;

UPDATE inventory 
SET remaining_items = remaining_items - 50
WHERE product_id = (SELECT id FROM products WHERE name = 'Loose Top');









