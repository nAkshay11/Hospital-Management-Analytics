CREATE TABLE beds (
    bed_id SERIAL PRIMARY KEY,
    bed_code VARCHAR(20) UNIQUE NOT NULL,
    ward_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    bed_number VARCHAR(20) NOT NULL,
    bed_type VARCHAR(30)
        CHECK (bed_type IN ('General','ICU','Emergency','Private','Semi-Private')),
    availability_status VARCHAR(20)
        DEFAULT 'Available'
        CHECK (availability_status IN ('Available','Occupied','Maintenance','Reserved')),
    daily_charge NUMERIC(10,2)
        CHECK (daily_charge >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bed_ward
        FOREIGN KEY (ward_id)
        REFERENCES wards(ward_id)
);