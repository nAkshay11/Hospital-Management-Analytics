import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_FEEDBACK = 50000
BATCH_SIZE = 5000


def generate_patient_feedback():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating patient feedback...")

    cursor.execute("SELECT patient_id FROM patients")
    patient_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT doctor_id FROM doctors")
    doctor_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT department_id FROM departments")
    department_ids = [row[0] for row in cursor.fetchall()]

    service_types = [
        "Consultation",
        "Emergency",
        "Surgery",
        "Lab",
        "Pharmacy",
        "Inpatient",
        "Outpatient"
    ]

    comments = [
        "Excellent service.",
        "Doctor explained everything clearly.",
        "Friendly staff.",
        "Waiting time was high.",
        "Very satisfied.",
        "Clean hospital environment.",
        "Good nursing care.",
        "Treatment was effective.",
        "Highly recommended.",
        "Overall good experience."
    ]

    feedback = []

    for i in range(1, TOTAL_FEEDBACK + 1):

        row = (
            f"FDB{i:07d}",
            random.choice(patient_ids),
            random.choice(doctor_ids),
            random.choice(department_ids),
            random.randint(1, 5),
            random.choice(["Yes", "No"]),
            random.choice(service_types),
            random.choice(comments),
            fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            datetime.now(),
            datetime.now()
        )

        feedback.append(row)

    print(f"Generated {len(feedback)} feedback records")
    query = """
    INSERT INTO patient_feedback
    (
        feedback_code,
        patient_id,
        doctor_id,
        department_id,
        rating,
        recommendation,
        service_type,
        feedback_comments,
        feedback_date,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(feedback, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} feedback records)"
        )

        batch_number += 1

    print(f"\n✅ {len(feedback)} Patient Feedback Records Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_patient_feedback()