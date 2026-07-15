import sys
import os
import random
from datetime import datetime, timedelta

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_DISCHARGES = 50000
BATCH_SIZE = 5000


def chunk_data(data, chunk_size=BATCH_SIZE):
    """
    Split list into smaller batches.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def generate_discharges():

    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating discharges...")

    discharge_types = [
        "Recovered",
        "Transferred",
        "Against Medical Advice",
        "Deceased"
    ]

    discharge_summaries = [
        "Patient recovered successfully.",
        "Condition improved and discharged.",
        "Transferred to another hospital.",
        "Discharged after surgery.",
        "Patient requested discharge.",
        "Recovered after medication.",
        "Treatment completed successfully.",
        "Patient discharged with medications.",
        "Follow-up advised after discharge.",
        "Patient expired during treatment."
    ]

    rows = []

    for i in range(1, TOTAL_DISCHARGES + 1):

        discharge_date = fake.date_time_between(
            start_date="-1y",
            end_date="now"
        )

        follow_up_required = random.choice([True, False])

        if follow_up_required:
            follow_up_date = (
                discharge_date +
                timedelta(days=random.randint(7, 30))
            ).date()
        else:
            follow_up_date = None

        rows.append(
            (
                f"DIS{i:07d}",
                i,                              # admission_id (unique)
                discharge_date,
                random.choice(discharge_types),
                random.choice(discharge_summaries),
                follow_up_required,
                follow_up_date,
                datetime.now(),
                datetime.now()
            )
        )

    print(f"Generated {len(rows)} discharges")

    query = """
    INSERT INTO discharges
    (
        discharge_code,
        admission_id,
        discharge_date,
        discharge_type,
        discharge_summary,
        follow_up_required,
        follow_up_date,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(rows, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} discharges)"
        )

        batch_number += 1

    print(f"\n✅ {TOTAL_DISCHARGES} Discharges Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_discharges()