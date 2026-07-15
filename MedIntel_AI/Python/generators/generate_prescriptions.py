import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_PRESCRIPTIONS = 100000
BATCH_SIZE = 5000


def generate_prescriptions():

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT medicine_id FROM medicines")
    medicine_ids = [row[0] for row in cursor.fetchall()]

    print("✅ PostgreSQL Connected Successfully")
    print("Generating prescriptions...")

    dosages = [
        "250 mg",
        "500 mg",
        "650 mg",
        "1 Tablet",
        "2 Tablets",
        "5 ml",
        "10 ml",
        "1 Capsule",
        "2 Capsules"
    ]

    frequencies = [
        "Once Daily",
        "Twice Daily",
        "Three Times Daily",
        "Before Food",
        "After Food",
        "Morning",
        "Night",
        "SOS"
    ]

    instructions = [
        "Take after food.",
        "Take before food.",
        "Drink plenty of water.",
        "Complete full course.",
        "Take at bedtime.",
        "Avoid alcohol.",
        "Use as directed by physician.",
        "Finish antibiotic course."
    ]

    prescriptions = []

    for i in range(1, TOTAL_PRESCRIPTIONS + 1):

        row = (
            f"PRE{i:07d}",
            random.randint(1, 100000),
            random.randint(1, 500),
            random.choice(medicine_ids),
            random.choice(dosages),
            random.choice(frequencies),
            random.randint(1, 30),
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            random.choice(instructions),
            datetime.now(),
            datetime.now()
        )

        prescriptions.append(row)

    print(f"Generated {len(prescriptions)} prescriptions")
    query = """
    INSERT INTO prescriptions
    (
        prescription_code,
        patient_id,
        doctor_id,
        medicine_id,
        dosage,
        frequency,
        duration_days,
        prescription_date,
        instructions,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(prescriptions, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} prescriptions)"
        )

        batch_number += 1

    print(f"\n✅ {TOTAL_PRESCRIPTIONS} Prescriptions Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_prescriptions()