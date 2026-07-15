CREATE TABLE patient_feedback (
    feedback_id SERIAL PRIMARY KEY,
    feedback_code VARCHAR(20) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT,
    department_id INT,
    rating INT
        CHECK (rating BETWEEN 1 AND 5),
    recommendation VARCHAR(10)
        CHECK (recommendation IN ('Yes','No')),
    service_type VARCHAR(50),
    feedback_comments TEXT,
    feedback_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_feedback_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_feedback_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    CONSTRAINT fk_feedback_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);