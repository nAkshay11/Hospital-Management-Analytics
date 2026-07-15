CREATE TABLE lab_tests (
    lab_test_id SERIAL PRIMARY KEY,
    test_code VARCHAR(20) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    test_name VARCHAR(150),
    test_category VARCHAR(100),
    test_date TIMESTAMP,
    result_status VARCHAR(20)
        CHECK (result_status IN ('Pending','Completed','Cancelled')),
    result_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_lab_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_lab_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id)
);