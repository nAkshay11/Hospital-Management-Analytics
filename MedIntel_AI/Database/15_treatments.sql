CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,
    treatment_code VARCHAR(20) UNIQUE NOT NULL,
    diagnosis_id INT NOT NULL,
    treatment_name VARCHAR(200),
    treatment_type VARCHAR(100),
    treatment_start TIMESTAMP,
    treatment_end TIMESTAMP,
    treatment_cost NUMERIC(12,2)
        CHECK (treatment_cost >= 0),
    treatment_status VARCHAR(20)
        CHECK (treatment_status IN ('Planned','Ongoing','Completed','Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_treatment_diagnosis
        FOREIGN KEY (diagnosis_id)
        REFERENCES diagnoses(diagnosis_id)
);