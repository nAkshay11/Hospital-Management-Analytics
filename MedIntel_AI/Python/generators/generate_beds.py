import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

TOTAL_BEDS = 2000

BED_TYPES = [
    "General",
    "ICU",
    "Semi-Private",
    "Private",
    "Emergency"
]

STATUS = [
    "Available",
    "Occupied",
    "Maintenance"
]


def generate_beds():

    connection = get_connection()
    cursor = connection.cursor()

    beds = []

    for i in range(1, TOTAL_BEDS + 1):

        ward_id = random.randint(1, 12)

        room_number = f"R{ward_id:02}{random.randint(1,60):03}"

        bed_number = f"B{random.randint(1,6):02}"

        bed_type = random.choice(BED_TYPES)

        if bed_type == "General":
            charge = random.randint(1000, 2500)

        elif bed_type == "Semi-Private":
            charge = random.randint(2500, 4000)

        elif bed_type == "Private":
            charge = random.randint(4000, 7000)

        elif bed_type == "ICU":
            charge = random.randint(7000, 12000)

        else:
            charge = random.randint(5000, 9000)

        beds.append(
            (
                f"BED{i:05}",
                ward_id,
                room_number,
                bed_number,
                bed_type,
                random.choice(STATUS),
                charge
            )
        )

    query = """
    INSERT INTO beds
    (
        bed_code,
        ward_id,
        room_number,
        bed_number,
        bed_type,
        availability_status,
        daily_charge
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(beds, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"Batch {batch_no} inserted ({len(batch)} beds)")

        batch_no += 1

    print(f"\n✅ {TOTAL_BEDS} Beds Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_beds()