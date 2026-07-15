CREATE TABLE insurance_claims (
    claim_id SERIAL PRIMARY KEY,
    claim_number VARCHAR(30) UNIQUE NOT NULL,
    bill_id INT NOT NULL,
    insurance_provider VARCHAR(100),
    claim_amount NUMERIC(12,2)
        CHECK (claim_amount >= 0),
    approved_amount NUMERIC(12,2)
        CHECK (approved_amount >= 0),
    claim_status VARCHAR(20)
        CHECK (claim_status IN ('Submitted','Under Review','Approved','Rejected')),
    claim_submission_date DATE,
    claim_approval_date DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_claim_bill
        FOREIGN KEY (bill_id)
        REFERENCES billing(bill_id)
);