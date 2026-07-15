CREATE TABLE medicines (
    medicine_id SERIAL PRIMARY KEY,
    medicine_code VARCHAR(20) UNIQUE NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    manufacturer VARCHAR(100),
    dosage_form VARCHAR(50),
    strength VARCHAR(50),
    unit_price NUMERIC(10,2)
        CHECK (unit_price >= 0),
    supplier_id INT NOT NULL,
    storage_condition VARCHAR(100),
    expiry_date DATE,
    status VARCHAR(20)
        DEFAULT 'Active'
        CHECK (status IN ('Active','Discontinued')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_medicine_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);