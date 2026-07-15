import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data
from utils.random_data import random_name, random_city, random_phone, random_address

TOTAL_SUPPLIERS = 500


COMPANIES = [
    "Sun Pharma",
    "Cipla",
    "Dr. Reddy's",
    "Apollo Pharma",
    "Mankind Pharma",
    "Lupin",
    "Alkem",
    "Torrent Pharma",
    "Zydus",
    "Abbott"
]


def random_gst():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=15))


def generate_suppliers():

    connection = get_connection()
    cursor = connection.cursor()

    suppliers = []

    for i in range(1, TOTAL_SUPPLIERS + 1):

        city, state = random_city()

        suppliers.append(
            (
                f"SUP{i:04}",
                random.choice(COMPANIES) + f" {i}",
                random_name(),
                random_phone(),
                f"supplier{i}@medintel.com",
                random_address(),
                city,
                state,
                random_gst(),
                "Active"
            )
        )

    query = """
    INSERT INTO suppliers
    (
        supplier_code,
        supplier_name,
        contact_person,
        phone,
        email,
        address,
        city,
        state,
        gst_number,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(suppliers, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"Batch {batch_no} inserted ({len(batch)} suppliers)")

        batch_no += 1

    print(f"\n✅ {TOTAL_SUPPLIERS} Suppliers Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_suppliers()