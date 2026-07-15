import sys
import os
import random
from datetime import datetime, timedelta

from faker import Faker
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_ADMISSIONS = 50000
BATCH_SIZE = 5000


def chunk_data(data, chunk_size=BATCH_SIZE):
    """
    Split data into smaller batches.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def generate_admissions():

    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating admissions...")

    admission_types = [
        "Emergency",
        "Planned",
        "Transfer"
    ]

    admission_status = [
        "Admitted",
        "Discharged",
        "Transferred",
        "Cancelled"
    ]

    admission_reasons = [
        "Fever",
        "Diabetes",
        "Hypertension",
        "Accident",
        "Heart Disease",
        "Pregnancy",
        "Fracture",
        "Asthma",
        "Cancer",
        "Kidney Stone",
        "Migraine",
        "Covid-19",
        "Pneumonia",
        "Surgery",
        "Chest Pain"
    ]

    rows = []

    for i in range(1, TOTAL_ADMISSIONS + 1):

        admission_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        discharge_date = (
            admission_date +
            timedelta(days=random.randint(1, 15))
        ).date()

        rows.append(

            (
                f"ADM{i:07d}",

                random.randint(1, 100000),     # patient_id

                random.randint(1, 500),        # doctor_id

                random.randint(1, 12),         # ward_id

                random.randint(1, 2000),       # bed_id

                admission_date,

                random.choice(admission_types),

                random.choice(admission_reasons),

                random.choice(admission_status),

                discharge_date,

                datetime.now(),

                datetime.now()

            )

        )

    print(f"Generated {len(rows)} admissions")

    query = """
    INSERT INTO admissions
    (
        admission_code,
        patient_id,
        doctor_id,
        ward_id,
        bed_id,
        admission_date,
        admission_type,
        admission_reason,
        admission_status,
        estimated_discharge_date,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(rows, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} admissions)"
        )

        batch_number += 1

    print(f"\n✅ {TOTAL_ADMISSIONS} Admissions Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_admissions()