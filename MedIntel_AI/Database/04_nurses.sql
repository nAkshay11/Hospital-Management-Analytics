CREATE TABLE nurses (
    nurse_id SERIAL PRIMARY KEY,
    nurse_code VARCHAR(20) UNIQUE NOT NULL,
    nurse_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10)
        CHECK (gender IN ('Male','Female','Other')),
    department_id INT NOT NULL,
    qualification VARCHAR(100),
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,
    experience_years INT
        CHECK (experience_years >= 0),
    shift_type VARCHAR(20)
        CHECK (shift_type IN ('Morning','Evening','Night')),
    joining_date DATE,
    status VARCHAR(20)
        DEFAULT 'Active'
        CHECK (status IN ('Active','Inactive','On Leave')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_nurse_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);