import sys
import os
import random
from datetime import datetime, timedelta

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_TREATMENTS = 50000
BATCH_SIZE = 5000


def generate_treatments():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating treatments...")

    cursor.execute("""
        SELECT diagnosis_id
        FROM diagnoses
    """)

    diagnosis_ids = [row[0] for row in cursor.fetchall()]

    treatment_data = [
        ("Medication Therapy", "Medication"),
        ("Physiotherapy", "Therapy"),
        ("Surgery", "Surgical"),
        ("Chemotherapy", "Cancer Care"),
        ("Radiotherapy", "Cancer Care"),
        ("Dialysis", "Renal Care"),
        ("ICU Monitoring", "Critical Care"),
        ("Vaccination", "Preventive"),
        ("Wound Dressing", "Nursing"),
        ("Cardiac Rehabilitation", "Rehabilitation")
    ]

    statuses = [
        "Planned",
        "Ongoing",
        "Completed",
        "Cancelled"
    ]

    treatments = []

    for i, diagnosis_id in enumerate(diagnosis_ids, start=1):

        treatment_name, treatment_type = random.choice(treatment_data)

        start = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        end = start + timedelta(days=random.randint(1, 20))

        row = (
            f"TRT{i:07d}",
            diagnosis_id,
            treatment_name,
            treatment_type,
            start,
            end,
            round(random.uniform(1000, 50000), 2),
            random.choice(statuses),
            datetime.now(),
            datetime.now()
        )

        treatments.append(row)

    print(f"Generated {len(treatments)} treatments")
    query = """
    INSERT INTO treatments
    (
        treatment_code,
        diagnosis_id,
        treatment_name,
        treatment_type,
        treatment_start,
        treatment_end,
        treatment_cost,
        treatment_status,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(treatments, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} treatments)"
        )

        batch_number += 1

    print(f"\n✅ {len(treatments)} Treatments Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_treatments()