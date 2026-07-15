CREATE TABLE emergency_visits (
    emergency_visit_id SERIAL PRIMARY KEY,
    emergency_code VARCHAR(20) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT,
    arrival_time TIMESTAMP NOT NULL,
    triage_time TIMESTAMP,
    treatment_start_time TIMESTAMP,
    severity_level VARCHAR(20)
        CHECK (severity_level IN ('Critical','High','Moderate','Low')),
    waiting_minutes INT
        CHECK (waiting_minutes >= 0),
    arrival_mode VARCHAR(30)
        CHECK (arrival_mode IN ('Ambulance','Walk-In','Referral','Police')),
    outcome VARCHAR(40)
        CHECK (outcome IN ('Discharged','Admitted','Transferred','Deceased')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_emergency_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_emergency_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id)
);