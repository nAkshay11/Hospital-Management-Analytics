CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    payment_code VARCHAR(20) UNIQUE NOT NULL,
    bill_id INT NOT NULL,
    payment_method VARCHAR(30)
        CHECK (payment_method IN ('Cash','Credit Card','Debit Card','UPI','Net Banking','Insurance')),
    payment_amount NUMERIC(12,2)
        CHECK (payment_amount >= 0),
    payment_status VARCHAR(20)
        DEFAULT 'Completed'
        CHECK (payment_status IN ('Pending','Completed','Failed','Refunded')),
    transaction_reference VARCHAR(100) UNIQUE,
    payment_gateway VARCHAR(50),
    payment_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payment_bill
        FOREIGN KEY (bill_id)
        REFERENCES billing(bill_id)
);