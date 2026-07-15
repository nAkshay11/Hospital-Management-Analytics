import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_BILLS = 50000
BATCH_SIZE = 5000


def generate_billing():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating billing records...")

    cursor.execute("""
        SELECT admission_id, patient_id
        FROM admissions
    """)

    admissions = cursor.fetchall()

    payment_status = [
        "Pending",
        "Partial",
        "Paid"
    ]

    bills = []

    for i, (admission_id, patient_id) in enumerate(admissions, start=1):

        total = round(random.uniform(500, 50000), 2)

        tax = round(total * 0.05, 2)

        discount = round(random.uniform(0, total * 0.15), 2)

        net = round(total + tax - discount, 2)

        row = (
            f"BILL{i:07d}",
            patient_id,
            admission_id,
            total,
            tax,
            discount,
            net,
            random.choice(payment_status),
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            datetime.now(),
            datetime.now()
        )

        bills.append(row)

    print(f"Generated {len(bills)} billing records")
    query = """
    INSERT INTO billing
    (
        bill_number,
        patient_id,
        admission_id,
        total_amount,
        tax_amount,
        discount_amount,
        net_amount,
        payment_status,
        billing_date,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(bills, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} bills)"
        )

        batch_number += 1

    print(f"\n✅ {len(bills)} Billing Records Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_billing()