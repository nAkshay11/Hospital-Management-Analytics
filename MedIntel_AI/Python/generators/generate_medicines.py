import sys
import os
import random
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

TOTAL_MEDICINES = 5000

CATEGORIES = [
    "Antibiotic",
    "Painkiller",
    "Antiviral",
    "Vitamin",
    "Cardiac",
    "Diabetes",
    "Neurology",
    "Dermatology",
    "Pediatric",
    "Emergency"
]

DOSAGE_FORMS = [
    "Tablet",
    "Capsule",
    "Injection",
    "Syrup",
    "Cream",
    "Drops"
]

STRENGTHS = [
    "100 mg",
    "250 mg",
    "500 mg",
    "650 mg",
    "1 g",
    "5 ml",
    "10 ml"
]

STORAGE = [
    "Room Temperature",
    "Refrigerated",
    "Cool & Dry Place"
]


def expiry_date():
    return date.today() + timedelta(days=random.randint(365, 1825))


def generate_medicines():

    connection = get_connection()
    cursor = connection.cursor()

    # Read actual supplier IDs
    cursor.execute("SELECT supplier_id FROM suppliers ORDER BY supplier_id")
    supplier_ids = [row[0] for row in cursor.fetchall()]

    if not supplier_ids:
        print("❌ No suppliers found.")
        return

    medicines = []

    for i in range(1, TOTAL_MEDICINES + 1):

        category = random.choice(CATEGORIES)

        medicines.append((
            f"MED{i:05}",
            f"{category} Medicine {i}",
            category,
            random.choice([
                "Sun Pharma",
                "Cipla",
                "Dr. Reddy's",
                "Abbott",
                "Lupin"
            ]),
            random.choice(DOSAGE_FORMS),
            random.choice(STRENGTHS),
            round(random.uniform(20, 1500), 2),
            random.choice(supplier_ids),
            random.choice(STORAGE),
            expiry_date(),
            "Active"
        ))

    query = """
    INSERT INTO medicines
    (
        medicine_code,
        medicine_name,
        category,
        manufacturer,
        dosage_form,
        strength,
        unit_price,
        supplier_id,
        storage_condition,
        expiry_date,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(medicines, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"Batch {batch_no} inserted ({len(batch)} medicines)")
        batch_no += 1

    print(f"\n✅ {TOTAL_MEDICINES} Medicines Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_medicines()