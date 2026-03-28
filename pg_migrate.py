import sys
from sqlalchemy import create_engine
from sqlalchemy.sql import text

print("Loading local application schemas...")
try:
    from app import app, db
except Exception as e:
    print("Failed to import app schema:", e)
    sys.exit(1)

src_uri = "mysql+mysqlconnector://root:Nikesh%402006@localhost/gymcopy"
dst_uri = "postgresql://postgres.dyxrxcfavrfffmepqacl:Nikesh%40%23%232006@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

src_engine = create_engine(src_uri)
dst_engine = create_engine(dst_uri)

def run():
    with app.app_context():
        print("Creating tables on Supabase...")
        db.metadata.create_all(dst_engine)
        
        for table in db.metadata.sorted_tables:
            print(f"Migrating table {table.name}...")
            with src_engine.connect() as src_conn:
                records = src_conn.execute(table.select()).fetchall()
                if records:
                    # Convert to list of dictionaries
                    dicts = [dict(row._mapping) for row in records]
                    
                    # Insert into PG
                    with dst_engine.begin() as dst_conn:
                        # Clear existing data just in case to prevent duplicates
                        dst_conn.execute(table.delete())
                        dst_conn.execute(table.insert(), dicts)
                    print(f"Migrated {len(dicts)} rows in {table.name}.")
                    
                    # Reset Postgres auto-increment identity sequence
                    primary_keys = [key.name for key in table.primary_key]
                    if len(primary_keys) == 1 and primary_keys[0] == 'id':
                        # Special handling for "user" table reserved keyword in Postgres
                        table_name = f'"{table.name}"' if table.name == "user" else table.name
                        try:
                            seq_query = f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE((SELECT MAX(id) FROM {table_name}) + 1, 1), false);"
                            with dst_engine.begin() as d_conn:
                                d_conn.execute(text(seq_query))
                        except Exception as seq_e:
                            print(f"Could not reset sequence for {table.name}: {seq_e}. (May not be a serial column)")
                else:
                    print(f"Table {table.name} is empty.")
                    
        print("Data migration to Supabase completed successfully!")

if __name__ == '__main__':
    run()
