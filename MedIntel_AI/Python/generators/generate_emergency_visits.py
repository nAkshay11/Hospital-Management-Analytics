import sys
import os
import random
from datetime import datetime, timedelta

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_VISITS = 50000
BATCH_SIZE = 5000


def generate_emergency_visits():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating emergency visits...")

    cursor.execute("""
        SELECT patient_id FROM patients
    """)
    patient_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT doctor_id FROM doctors
    """)
    doctor_ids = [row[0] for row in cursor.fetchall()]

    severity_levels = [
        "Critical",
        "High",
        "Moderate",
        "Low"
    ]

    arrival_modes = [
        "Ambulance",
        "Walk-In",
        "Referral",
        "Police"
    ]

    outcomes = [
        "Discharged",
        "Admitted",
        "Transferred",
        "Deceased"
    ]

    visits = []

    for i in range(1, TOTAL_VISITS + 1):

        arrival = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        waiting = random.randint(5, 120)

        triage = arrival + timedelta(minutes=random.randint(2, 15))

        treatment = triage + timedelta(minutes=waiting)

        row = (
            f"ER{i:07d}",
            random.choice(patient_ids),
            random.choice(doctor_ids),
            arrival,
            triage,
            treatment,
            random.choice(severity_levels),
            waiting,
            random.choice(arrival_modes),
            random.choice(outcomes),
            datetime.now(),
            datetime.now()
        )

        visits.append(row)

    print(f"Generated {len(visits)} emergency visits")
    query = """
    INSERT INTO emergency_visits
    (
        emergency_code,
        patient_id,
        doctor_id,
        arrival_time,
        triage_time,
        treatment_start_time,
        severity_level,
        waiting_minutes,
        arrival_mode,
        outcome,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(visits, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} emergency visits)"
        )

        batch_number += 1

    print(f"\n✅ {len(visits)} Emergency Visits Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_emergency_visits()