import sys
import os
import random
from datetime import datetime, timedelta

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_CLAIMS = 50000
BATCH_SIZE = 5000


def generate_insurance_claims():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating insurance claims...")

    cursor.execute("""
        SELECT bill_id, net_amount
        FROM billing
    """)

    bills = cursor.fetchall()

    providers = [
        "Star Health",
        "ICICI Lombard",
        "HDFC ERGO",
        "Niva Bupa",
        "Care Health",
        "New India Assurance",
        "Bajaj Allianz",
        "ACKO"
    ]

    statuses = [
        "Submitted",
        "Under Review",
        "Approved",
        "Rejected"
    ]

    remarks = [
        "Documents verified.",
        "Awaiting approval.",
        "Approved successfully.",
        "Rejected due to missing documents.",
        "Additional verification required.",
        "Claim settled."
    ]

    claims = []

    for i, (bill_id, net_amount) in enumerate(bills, start=1):

        claim_amount = round(float(net_amount), 2)

        approved_amount = round(
            claim_amount * random.uniform(0.60, 1.00),
            2
        )

        submit_date = fake.date_between(
            start_date="-2y",
            end_date="today"
        )

        approval_date = submit_date + timedelta(
            days=random.randint(1, 15)
        )

        row = (
            f"CLM{i:07d}",
            bill_id,
            random.choice(providers),
            claim_amount,
            approved_amount,
            random.choice(statuses),
            submit_date,
            approval_date,
            random.choice(remarks),
            datetime.now(),
            datetime.now()
        )

        claims.append(row)

    print(f"Generated {len(claims)} insurance claims")
    query = """
    INSERT INTO insurance_claims
    (
        claim_number,
        bill_id,
        insurance_provider,
        claim_amount,
        approved_amount,
        claim_status,
        claim_submission_date,
        claim_approval_date,
        remarks,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(claims, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} claims)"
        )

        batch_number += 1

    print(f"\n✅ {len(claims)} Insurance Claims Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_insurance_claims()