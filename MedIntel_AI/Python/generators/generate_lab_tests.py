import sys
import os
import random
from datetime import datetime

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

fake = Faker("en_IN")

TOTAL_LAB_TESTS = 100000
BATCH_SIZE = 5000


def generate_lab_tests():

    connection = get_connection()
    cursor = connection.cursor()

    print("✅ PostgreSQL Connected Successfully")
    print("Generating lab tests...")

    test_data = [
        ("Complete Blood Count", "Blood"),
        ("Blood Sugar", "Blood"),
        ("Lipid Profile", "Blood"),
        ("Liver Function Test", "Blood"),
        ("Kidney Function Test", "Blood"),
        ("Urine Routine", "Urine"),
        ("Thyroid Profile", "Hormone"),
        ("ECG", "Cardiology"),
        ("2D Echo", "Cardiology"),
        ("Chest X-Ray", "Radiology"),
        ("CT Scan", "Radiology"),
        ("MRI Scan", "Radiology"),
        ("Ultrasound", "Radiology"),
        ("COVID RT-PCR", "Microbiology"),
        ("Dengue Test", "Serology"),
        ("Malaria Test", "Serology"),
        ("Vitamin D", "Blood"),
        ("Vitamin B12", "Blood"),
        ("HbA1c", "Blood"),
        ("Electrolyte Panel", "Blood")
    ]

    statuses = [
        "Pending",
        "Completed",
        "Cancelled"
    ]

    summaries = [
        "Normal findings.",
        "Within reference range.",
        "Abnormal values detected.",
        "Further investigation required.",
        "Patient condition stable.",
        "Mild abnormalities observed.",
        "Critical values detected.",
        "Follow-up recommended.",
        "No significant findings.",
        "Clinical correlation advised."
    ]

    lab_tests = []

    for i in range(1, TOTAL_LAB_TESTS + 1):

        test_name, category = random.choice(test_data)

        row = (
            f"LAB{i:07d}",
            random.randint(1, 100000),
            random.randint(1, 500),
            test_name,
            category,
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            random.choice(statuses),
            random.choice(summaries),
            datetime.now(),
            datetime.now()
        )

        lab_tests.append(row)

    print(f"Generated {len(lab_tests)} lab tests")

    query = """
    INSERT INTO lab_tests
    (
        test_code,
        patient_id,
        doctor_id,
        test_name,
        test_category,
        test_date,
        result_status,
        result_summary,
        created_at,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    batch_number = 1

    for batch in chunk_data(lab_tests, BATCH_SIZE):

        cursor.executemany(query, batch)
        connection.commit()

        print(
            f"Batch {batch_number} inserted "
            f"({len(batch)} records)"
        )

        batch_number += 1

    print(f"\n✅ {TOTAL_LAB_TESTS} Lab Tests Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_lab_tests()