CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    appointment_code VARCHAR(20) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    department_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    consultation_type VARCHAR(30)
        CHECK (consultation_type IN ('In-Person','Video','Follow-Up')),
    appointment_status VARCHAR(20)
        DEFAULT 'Scheduled'
        CHECK (appointment_status IN ('Scheduled','Completed','Cancelled','No-Show')),
    booking_channel VARCHAR(30)
        CHECK (booking_channel IN ('Online','Phone','Walk-In','Referral')),
    reason_for_visit VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    CONSTRAINT fk_appointment_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);