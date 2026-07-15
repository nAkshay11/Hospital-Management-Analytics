CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    patient_code VARCHAR(20) UNIQUE NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10)
        CHECK (gender IN ('Male','Female','Other')),
    date_of_birth DATE NOT NULL,
    blood_group VARCHAR(5),
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(15),
    insurance_status VARCHAR(20)
        CHECK (insurance_status IN ('Insured','Not Insured')),
    marital_status VARCHAR(20),
    nationality VARCHAR(50) DEFAULT 'Indian',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);