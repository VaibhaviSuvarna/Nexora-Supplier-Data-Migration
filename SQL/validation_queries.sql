-- Total suppliers
SELECT COUNT(*) AS total_suppliers
FROM suppliers;


-- Check duplicate GST numbers
SELECT
    gst_number,
    COUNT(*) AS supplier_count
FROM suppliers
GROUP BY gst_number
HAVING COUNT(*) > 1;


-- Check migrated suppliers
SELECT *
FROM suppliers
WHERE supplier_name IN (
    'CloudServe Solutions',
    'NextGen Solutions'
);


-- Supplier count by city
SELECT
    city,
    COUNT(*) AS supplier_count
FROM suppliers
GROUP BY city
ORDER BY supplier_count DESC;


-- Supplier count by status
SELECT
    status,
    COUNT(*) AS supplier_count
FROM suppliers
GROUP BY status;