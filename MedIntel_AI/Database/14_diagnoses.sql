CREATE TABLE diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    diagnosis_code VARCHAR(20) UNIQUE NOT NULL,
    admission_id INT NOT NULL,
    doctor_id INT NOT NULL,
    diagnosis_name VARCHAR(200) NOT NULL,
    diagnosis_category VARCHAR(100),
    icd_code VARCHAR(20),
    diagnosis_date TIMESTAMP NOT NULL,
    severity VARCHAR(20)
        CHECK (severity IN ('Low','Moderate','High','Critical')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_diag_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id),

    CONSTRAINT fk_diag_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id)
);