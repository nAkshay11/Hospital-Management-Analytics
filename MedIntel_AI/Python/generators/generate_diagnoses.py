import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_DIAGNOSES = 50000
BATCH_SIZE = 5000


def generate_diagnoses():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating diagnoses...")

    cursor.execute("""
        SELECT admission_id, doctor_id
        FROM admissions
    """)

    admissions = cursor.fetchall()

    diagnosis_data = [
        ("Hypertension", "Cardiology", "I10"),
        ("Diabetes Mellitus", "Endocrinology", "E11"),
        ("Pneumonia", "Respiratory", "J18"),
        ("Migraine", "Neurology", "G43"),
        ("Asthma", "Respiratory", "J45"),
        ("Fracture", "Orthopedics", "S52"),
        ("Appendicitis", "General Surgery", "K35"),
        ("COVID-19", "Infectious Disease", "U07.1"),
        ("Kidney Stone", "Urology", "N20"),
        ("Gastritis", "Gastroenterology", "K29")
    ]

    severity_levels = [
        "Low",
        "Moderate",
        "High",
        "Critical"
    ]

    notes_list = [
        "Patient stable.",
        "Requires observation.",
        "Medication started.",
        "Further investigations advised.",
        "Condition improving.",
        "Specialist consultation recommended."
    ]

    diagnoses = []

    for i, (admission_id, doctor_id) in enumerate(admissions, start=1):

        name, category, icd = random.choice(diagnosis_data)

        row = (
            f"DGN{i:07d}",
            admission_id,
            doctor_id,
            name,
            category,
            icd,
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            random.choice(severity_levels),
            random.choice(notes_list),
            datetime.now(),
            datetime.now()
        )

        diagnoses.append(row)

    print(f"Generated {len(diagnoses)} diagnoses")
    query = """
    INSERT INTO diagnoses
    (
        diagnosis_code,
        admission_id,
        doctor_id,
        diagnosis_name,
        diagnosis_category,
        icd_code,
        diagnosis_date,
        severity,
        notes,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(diagnoses, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} diagnoses)"
        )

        batch_number += 1

    print(f"\n✅ {len(diagnoses)} Diagnoses Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_diagnoses()