CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor_code VARCHAR(20) UNIQUE NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10)
        CHECK (gender IN ('Male','Female','Other')),
    specialization VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    qualification VARCHAR(100),
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,
    experience_years INT
        CHECK (experience_years >= 0),
    consultation_fee NUMERIC(10,2)
        CHECK (consultation_fee >= 0),
    joining_date DATE,
    employment_type VARCHAR(20)
        DEFAULT 'Full-Time'
        CHECK (employment_type IN ('Full-Time','Part-Time','Visiting')),
    status VARCHAR(20)
        DEFAULT 'Active'
        CHECK (status IN ('Active','Inactive','On Leave')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_doctor_department
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);