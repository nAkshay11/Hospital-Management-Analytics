CREATE TABLE admissions (
    admission_id SERIAL PRIMARY KEY,
    admission_code VARCHAR(20) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    ward_id INT NOT NULL,
    bed_id INT NOT NULL,
    admission_date TIMESTAMP NOT NULL,
    admission_type VARCHAR(30)
        CHECK (admission_type IN ('Emergency','Planned','Transfer')),
    admission_reason VARCHAR(250),
    admission_status VARCHAR(20)
        DEFAULT 'Admitted'
        CHECK (admission_status IN ('Admitted','Discharged','Transferred','Cancelled')),
    estimated_discharge_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_admission_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_admission_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    CONSTRAINT fk_admission_ward
        FOREIGN KEY (ward_id)
        REFERENCES wards(ward_id),

    CONSTRAINT fk_admission_bed
        FOREIGN KEY (bed_id)
        REFERENCES beds(bed_id)
);