import sys
import os
import random
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.random_data import random_name

SPECIALIZATIONS = {
    1: "Cardiologist",
    2: "Neurologist",
    3: "Orthopedic Surgeon",
    4: "Pediatrician",
    5: "Emergency Physician",
    6: "Radiologist",
    7: "Oncologist",
    8: "ENT Specialist",
    9: "Dermatologist",
    10: "Critical Care Specialist"
}

QUALIFICATIONS = [
    "MBBS",
    "MBBS, MD",
    "MBBS, MS",
    "MBBS, DM",
    "MBBS, MCh"
]

EMPLOYMENT_TYPES = [
    "Full-Time",
    "Part-Time",
    "Visiting"
]

STATUS = [
    "Active",
    "Active",
    "Active",
    "On Leave"
]


def random_phone():
    return "9" + "".join(random.choices("0123456789", k=9))


def random_joining_date():
    start = date(2015, 1, 1)
    end = date(2026, 1, 1)

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))


def generate_doctors():

    connection = get_connection()
    cursor = connection.cursor()

    doctors = []

    for i in range(1, 501):

        department = random.randint(1, 10)

        doctors.append((
            f"DOC{i:04}",
            "Dr. " + random_name(),
            random.choice(["Male", "Female"]),
            SPECIALIZATIONS[department],
            department,
            random.choice(QUALIFICATIONS),
            random_phone(),
            f"doctor{i}@medintel.com",
            random.randint(1, 25),
            random.randint(400, 2500),
            random_joining_date(),
            random.choice(EMPLOYMENT_TYPES),
            random.choice(STATUS)
        ))

    query = """
    INSERT INTO doctors
    (
        doctor_code,
        doctor_name,
        gender,
        specialization,
        department_id,
        qualification,
        phone,
        email,
        experience_years,
        consultation_fee,
        joining_date,
        employment_type,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.executemany(query, doctors)

    connection.commit()

    print(f"✅ {len(doctors)} Doctors Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_doctors()