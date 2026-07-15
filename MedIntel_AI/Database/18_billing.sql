CREATE TABLE billing (
    bill_id SERIAL PRIMARY KEY,
    bill_number VARCHAR(30) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    admission_id INT,
    total_amount NUMERIC(12,2)
        CHECK (total_amount >= 0),
    tax_amount NUMERIC(12,2)
        DEFAULT 0 CHECK (tax_amount >= 0),
    discount_amount NUMERIC(12,2)
        DEFAULT 0 CHECK (discount_amount >= 0),
    net_amount NUMERIC(12,2)
        CHECK (net_amount >= 0),
    payment_status VARCHAR(20)
        CHECK (payment_status IN ('Pending','Partial','Paid')),
    billing_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bill_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_bill_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);