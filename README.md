# Nexora Supplier Data Migration & Validation

## Project Overview

This project demonstrates the migration of supplier data from a legacy CSV source into the existing Nexora Technologies PostgreSQL supplier master.

The project focuses on data profiling, cleaning, standardization, duplicate detection, source-to-target matching, controlled migration, and post-migration validation.

Nexora Technologies is a fictional company created for this portfolio project.

## Objective

The main objective was to migrate supplier data safely while:

- Cleaning inconsistent supplier information
- Standardizing fields such as phone numbers, city, and status
- Identifying duplicate supplier records
- Matching source suppliers with existing target suppliers
- Inserting only genuinely new suppliers
- Validating the final migrated data
- Generating a migration report


## Tools & Technologies

- Python
- Pandas
- PostgreSQL
- pgAdmin
- SQL
- CSV
- python-dotenv

## Source Data

The source file contains legacy supplier records with intentional data-quality issues such as:

- Leading/trailing spaces
- Inconsistent capitalization
- Different phone number formats
- City name variations
- Different status formats
- Missing email information
- Duplicate supplier records
- Supplier name variations

## Data Cleaning

Python and Pandas were used to standardize the source data.

Examples include:

- Removing unnecessary spaces
- Standardizing email values
- Cleaning phone number formats
- Standardizing city names
- Standardizing supplier status
- Cleaning GST numbers
- Creating matching keys for duplicate detection

Supplier names were preserved rather than unnecessarily changing their business names.

## Duplicate Detection

GST number was used as the primary business key for identifying duplicate supplier records.

Duplicate records were grouped and evaluated before migration.

The source dataset contained duplicate/variant records for suppliers such as:

- ABC Technologies
- NetConnect

The duplicate records were consolidated so that only one valid supplier record was migrated.

## Source-to-Target Matching

The cleaned source data was compared against the existing Nexora PostgreSQL `suppliers` table.

Migration decisions were made as follows:

```text
Existing supplier → Skip
Duplicate source record → Deduplicate
New supplier → Insert
```

The original target contained 8 suppliers.

The migration identified 2 genuinely new suppliers:

- CloudServe Solutions
- NextGen Solutions

Therefore, the expected final supplier count was:

**10 unique suppliers**

## PostgreSQL Target

The migration was performed against the existing Nexora Procurement PostgreSQL database.

The target `suppliers` table contains fields including:

- supplier_id
- supplier_name
- email
- phone
- gst_number
- city
- status

## Validation & Reconciliation

After migration, SQL validation was performed to confirm that:

- Duplicate supplier records were not introduced
- Existing suppliers were not unnecessarily duplicated
- New suppliers were inserted successfully
- Supplier records were consistent with the cleaned source data
- The final target count matched the expected migration result

## Project Structure

```text
Nexora-Supplier-Data-Migration/
│
├── Data/
│   └── supplier_source.csv
│
├── Python/
│   └── supplier_migration.py
│
├── SQL/
│   └── validation_queries.sql
│
├── Reports/
│   └── migration_report.csv
│
├── README.md
│
└── .gitignore
```

## How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Nexora-Supplier-Data-Migration
```

### 2. Install dependencies

```bash
pip install pandas psycopg2-binary python-dotenv
```

### 3. Configure database credentials

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=nexora_procurement
DB_USER=postgres
DB_PASSWORD=your_actual_postgres_password
DB_PORT=5432
```

Do not commit the `.env` file to GitHub.

### 4. Run the migration script

```bash
python Python/supplier_migration.py
```

### 5. Validate the migration

Run the queries in:

```text
SQL/validation_queries.sql
```

The generated migration report is available in:

```text
Reports/migration_report.csv
```

## Key Learning Outcomes

This project provided practical experience with:

- ETL/data migration concepts
- Data profiling
- Data cleaning
- Data standardization
- Duplicate detection
- Business-key matching
- PostgreSQL data migration
- SQL validation
- Data reconciliation
- Migration reporting

## Note

Nexora Technologies is a fictional company created for educational and portfolio purposes.
