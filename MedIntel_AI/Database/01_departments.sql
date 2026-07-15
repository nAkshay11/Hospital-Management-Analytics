CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(10) NOT NULL UNIQUE,
    floor_number INT NOT NULL CHECK (floor_number >= 0),
    description TEXT,
    contact_number VARCHAR(15),
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Active'
        CHECK (status IN ('Active','Inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);