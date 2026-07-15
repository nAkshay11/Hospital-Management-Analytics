CREATE TABLE discharges (
    discharge_id SERIAL PRIMARY KEY,
    discharge_code VARCHAR(20) UNIQUE NOT NULL,
    admission_id INT NOT NULL UNIQUE,
    discharge_date TIMESTAMP NOT NULL,
    discharge_type VARCHAR(30)
        CHECK (discharge_type IN ('Recovered','Transferred','Against Medical Advice','Deceased')),
    discharge_summary TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_discharge_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);