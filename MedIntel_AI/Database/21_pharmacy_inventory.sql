CREATE TABLE pharmacy_inventory (
    inventory_id SERIAL PRIMARY KEY,
    inventory_code VARCHAR(20) UNIQUE NOT NULL,
    medicine_id INT NOT NULL,
    batch_number VARCHAR(50),
    quantity_in_stock INT
        CHECK (quantity_in_stock >= 0),
    reorder_level INT
        CHECK (reorder_level >= 0),
    expiry_date DATE,
    purchase_price NUMERIC(10,2)
        CHECK (purchase_price >= 0),
    selling_price NUMERIC(10,2)
        CHECK (selling_price >= 0),
    last_restock_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_medicine
        FOREIGN KEY (medicine_id)
        REFERENCES medicines(medicine_id)
);