import sys
import os
import random
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

TOTAL_INVENTORY = 50000


def random_expiry():
    return date.today() + timedelta(days=random.randint(180, 1825))


def random_restock():
    return date.today() - timedelta(days=random.randint(1, 365))


def generate_inventory():

    connection = get_connection()
    cursor = connection.cursor()

    # Get existing medicine IDs
    cursor.execute("SELECT medicine_id FROM medicines ORDER BY medicine_id")
    medicine_ids = [row[0] for row in cursor.fetchall()]

    if not medicine_ids:
        print("❌ No medicines found.")
        return

    inventory = []

    for i in range(1, TOTAL_INVENTORY + 1):

        purchase = round(random.uniform(10, 1000), 2)
        selling = round(purchase * random.uniform(1.15, 1.60), 2)

        inventory.append((
            f"INV{i:06}",
            random.choice(medicine_ids),
            f"BAT{random.randint(100000,999999)}",
            random.randint(20,500),
            random.randint(20,100),
            random_expiry(),
            purchase,
            selling,
            random_restock()
        ))

    query = """
    INSERT INTO pharmacy_inventory
    (
        inventory_code,
        medicine_id,
        batch_number,
        quantity_in_stock,
        reorder_level,
        expiry_date,
        purchase_price,
        selling_price,
        last_restock_date
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(inventory, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"Batch {batch_no} inserted ({len(batch)} inventory records)")
        batch_no += 1

    print(f"\n✅ {TOTAL_INVENTORY} Inventory Records Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_inventory()