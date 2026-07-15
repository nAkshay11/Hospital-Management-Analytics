import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_PAYMENTS = 50000
BATCH_SIZE = 5000


def generate_payments():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating payments...")

    cursor.execute("""
        SELECT bill_id, net_amount
        FROM billing
    """)

    bills = cursor.fetchall()

    payment_methods = [
        "Cash",
        "Credit Card",
        "Debit Card",
        "UPI"
    ]

    payment_statuses = [
        "Pending",
        "Completed",
        "Failed",
        "Refunded"
    ]

    gateways = [
        "Razorpay",
        "Paytm",
        "PhonePe",
        "Google Pay",
        "Cash Counter",
        "HDFC Gateway",
        "ICICI Gateway"
    ]

    payments = []

    for i, (bill_id, net_amount) in enumerate(bills, start=1):

        row = (
            f"PAY{i:07d}",
            bill_id,
            random.choice(payment_methods),
            round(float(net_amount), 2),
            random.choice(payment_statuses),
            f"TXN{i:09d}",
            random.choice(gateways),
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            datetime.now(),
            datetime.now()
        )

        payments.append(row)

    print(f"Generated {len(payments)} payments")
    query = """
    INSERT INTO payments
    (
        payment_code,
        bill_id,
        payment_method,
        payment_amount,
        payment_status,
        transaction_reference,
        payment_gateway,
        payment_date,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(payments, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} payments)"
        )

        batch_number += 1

    print(f"\n✅ {len(payments)} Payments Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_payments()