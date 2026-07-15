CREATE TABLE wards (
    ward_id SERIAL PRIMARY KEY,
    ward_name VARCHAR(100) NOT NULL,
    ward_code VARCHAR(20) NOT NULL UNIQUE,
    ward_type VARCHAR(50) NOT NULL,
    department_id INT NOT NULL,
    total_beds INT NOT NULL CHECK (total_beds > 0),
    occupied_beds INT DEFAULT 0 CHECK (occupied_beds >= 0),
    floor_number INT NOT NULL CHECK (floor_number >= 0),
    nurse_station VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Active'
        CHECK (status IN ('Active','Inactive','Maintenance')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ward_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);