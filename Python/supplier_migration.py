import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv



# CONFIGURATION

load_dotenv()
DB_HOST = "localhost"
DB_NAME = "nexora_procurement"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("password")
DB_PORT = "5432"

SOURCE_FILE = "../Data/supplier_source.csv"
REPORT_FILE = "../Reports/migration_report.csv"


# 1. LOAD SOURCE DATA


print("\n===== 1. LOADING SOURCE DATA =====")

df = pd.read_csv(SOURCE_FILE)

print(f"Source records: {len(df)}")



# 2. CLEAN DATA


print("\n===== 2. CLEANING DATA =====")

# Supplier name
df["supplier_name"] = df["supplier_name"].str.strip()

# Email
df["email"] = df["email"].fillna("").str.strip().str.lower()

# Phone
df["phone"] = (
    df["phone"]
    .fillna("")
    .str.replace(r"\D", "", regex=True)
)

# Convert 10-digit Indian numbers to +91
df["phone"] = df["phone"].apply(
    lambda x: "+91" + x if len(x) == 10 else ("+" + x if x else "")
)

# City
city_mapping = {
    "PUNE": "Pune",
    "pune": "Pune",
    "MUMBAI": "Mumbai",
    "mumbai": "Mumbai",
    "Bangalore": "Bengaluru",
    "BANGALORE": "Bengaluru",
    "BENGALURU": "Bengaluru"
}

df["city"] = df["city"].replace(city_mapping)

# Status
df["status"] = df["status"].str.strip().str.title()

# GST
df["gst_number"] = (
    df["gst_number"]
    .str.strip()
    .str.upper()
)

print("Cleaning completed.")


# 3. REMOVE DUPLICATES


print("\n===== 3. DEDUPLICATING SOURCE DATA =====")

before = len(df)

# GST is our primary supplier matching key
df = df.drop_duplicates(
    subset=["gst_number"],
    keep="first"
).copy()

after = len(df)

print(f"Records before deduplication: {before}")
print(f"Duplicate records removed: {before - after}")
print(f"Unique suppliers after deduplication: {after}")



# 4. CONNECT TO POSTGRESQL


print("\n===== 4. CONNECTING TO POSTGRESQL =====")


conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)

cursor = conn.cursor()

print("Connected successfully.")


# 5. READ EXISTING SUPPLIERS


print("\n===== 5. CHECKING TARGET DATABASE =====")

target_df = pd.read_sql(
    """
    SELECT
        supplier_id,
        supplier_name,
        email,
        phone,
        gst_number,
        city,
        status
    FROM suppliers
    """,
    conn
)

target_df["gst_number"] = (
    target_df["gst_number"]
    .str.strip()
    .str.upper()
)

print(f"Existing target suppliers: {len(target_df)}")



# 6. MATCH SOURCE WITH TARGET


print("\n===== 6. MATCHING SOURCE WITH TARGET =====")

existing_gst = set(target_df["gst_number"])

df["migration_status"] = df["gst_number"].apply(
    lambda gst: "EXISTING"
    if gst in existing_gst
    else "NEW"
)

print(
    df[
        [
            "supplier_id",
            "supplier_name",
            "gst_number",
            "migration_status"
        ]
    ]
)


# 7. INSERT NEW SUPPLIERS


print("\n===== 7. MIGRATING NEW SUPPLIERS =====")

new_suppliers = df[
    df["migration_status"] == "NEW"
]

inserted = 0

for _, row in new_suppliers.iterrows():

    cursor.execute(
        """
        INSERT INTO suppliers
        (
            supplier_name,
            email,
            phone,
            gst_number,
            city,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            row["supplier_name"],
            row["email"] if row["email"] else None,
            row["phone"] if row["phone"] else None,
            row["gst_number"],
            row["city"],
            row["status"]
        )
    )

    inserted += 1

conn.commit()

print(f"New suppliers inserted: {inserted}")


# 8. RECONCILIATION


print("\n===== 8. RECONCILIATION =====")

cursor.execute(
    "SELECT COUNT(*) FROM suppliers"
)

final_target_count = cursor.fetchone()[0]

expected_target_count = len(target_df) + inserted

print(f"Target count before migration: {len(target_df)}")
print(f"New suppliers inserted: {inserted}")
print(f"Expected target count: {expected_target_count}")
print(f"Actual target count: {final_target_count}")

if final_target_count == expected_target_count:
    reconciliation = "PASS"
else:
    reconciliation = "FAIL"

print(f"Reconciliation result: {reconciliation}")



# 9. CREATE MIGRATION REPORT


print("\n===== 9. CREATING MIGRATION REPORT =====")

report = df[
    [
        "supplier_id",
        "supplier_name",
        "email",
        "phone",
        "gst_number",
        "city",
        "status",
        "migration_status"
    ]
]

report.to_csv(
    REPORT_FILE,
    index=False
)

print("Migration report created.")



# 10. CLOSE CONNECTION


cursor.close()
conn.close()

print("\n===== MIGRATION COMPLETED =====")

print(f"Source records processed: {before}")
print(f"Duplicate records removed: {before - after}")
print(f"Unique source suppliers: {after}")
print(f"Existing suppliers skipped: {len(df[df['migration_status'] == 'EXISTING'])}")
print(f"New suppliers inserted: {inserted}")
print(f"Reconciliation: {reconciliation}")

print("\nReport:")
print(REPORT_FILE)