CREATE TABLE staff_shifts (
    shift_id SERIAL PRIMARY KEY,
    shift_code VARCHAR(20) UNIQUE NOT NULL,
    staff_type VARCHAR(20)
        CHECK (staff_type IN ('Doctor','Nurse')),
    staff_id INT NOT NULL,
    department_id INT NOT NULL,
    shift_date DATE NOT NULL,
    shift_name VARCHAR(20)
        CHECK (shift_name IN ('Morning','Evening','Night')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    attendance_status VARCHAR(20)
        DEFAULT 'Scheduled'
        CHECK (attendance_status IN ('Scheduled','Present','Absent','Leave')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_shift_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);