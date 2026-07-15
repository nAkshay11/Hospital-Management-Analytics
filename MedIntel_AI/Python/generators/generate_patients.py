import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.random_data import (
    random_name,
    random_gender,
    random_phone,
    random_city,
    random_blood_group,
    random_marital_status,
    random_insurance,
    random_dob,
    random_pincode,
    random_address,
    NATIONALITY
)

from utils.batch_insert import chunk_data

TOTAL_PATIENTS = 100000


def generate_patients():

    connection = get_connection()
    cursor = connection.cursor()

    patients = []

    used_phone = set()

    print("Generating patients...")

    for i in range(1, TOTAL_PATIENTS + 1):

        city, state = random_city()

        phone = random_phone()

        while phone in used_phone:
            phone = random_phone()

        used_phone.add(phone)

        email = f"patient{i}@medintel.com"

        patients.append(
            (
                f"PAT{i:06}",
                random_name(),
                random_gender(),
                random_dob(),
                random_blood_group(),
                phone,
                email,
                random_address(),
                city,
                state,
                random_pincode(),
                random_name(),
                random_phone(),
                random_insurance(),
                random_marital_status(),
                NATIONALITY,
            )
        )

    print(f"Generated {len(patients)} patients")

    query = """
    INSERT INTO patients
    (
        patient_code,
        patient_name,
        gender,
        date_of_birth,
        blood_group,
        phone,
        email,
        address,
        city,
        state,
        pincode,
        emergency_contact_name,
        emergency_contact_phone,
        insurance_status,
        marital_status,
        nationality
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(patients, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"Batch {batch_no} inserted ({len(batch)} records)")

        batch_no += 1

    print(f"\n✅ {TOTAL_PATIENTS} Patients Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_patients()