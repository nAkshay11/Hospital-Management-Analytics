import sys
import os
import random
from datetime import datetime
from faker import Faker
from datetime import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_SHIFTS = 50000
BATCH_SIZE = 5000


def generate_staff_shifts():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating staff shifts...")

    cursor.execute("SELECT doctor_id, department_id FROM doctors")
    doctors = cursor.fetchall()

    cursor.execute("SELECT nurse_id, department_id FROM nurses")
    nurses = cursor.fetchall()

    shift_details = {
        "Morning": (time(6, 0), time(14, 0)),
        "Evening": (time(14, 0), time(22, 0)),
        "Night": (time(22, 0), time(6, 0))
    }

    attendance = [
        "Scheduled",
        "Present",
        "Absent",
        "Leave"
    ]

    shifts = []

    for i in range(1, TOTAL_SHIFTS + 1):

        if random.choice([True, False]):
            staff_type = "Doctor"
            staff_id, department_id = random.choice(doctors)
        else:
            staff_type = "Nurse"
            staff_id, department_id = random.choice(nurses)

        shift_name = random.choice(list(shift_details.keys()))

        start_time, end_time = shift_details[shift_name]

        row = (
            f"SFT{i:07d}",
            staff_type,
            staff_id,
            department_id,
            fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            shift_name,
            start_time,
            end_time,
            random.choice(attendance),
            datetime.now(),
            datetime.now()
        )

        shifts.append(row)

    print(f"Generated {len(shifts)} staff shifts")
    query = """
    INSERT INTO staff_shifts
    (
        shift_code,
        staff_type,
        staff_id,
        department_id,
        shift_date,
        shift_name,
        start_time,
        end_time,
        attendance_status,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(shifts, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} staff shifts)"
        )

        batch_number += 1

    print(f"\n✅ {len(shifts)} Staff Shifts Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_staff_shifts()