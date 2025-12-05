import psycopg2
from db_config import DB_CONFIG

def create_tables():
    """Create necessary database tables"""
    connection = None
    cursor = None
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create users table for admin authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                full_name VARCHAR(100),
                role VARCHAR(20) DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                passport_number VARCHAR(50),
                nationality VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                booking_reference VARCHAR(50) UNIQUE NOT NULL,
                package_name VARCHAR(200),
                travel_date DATE,
                return_date DATE,
                number_of_people INTEGER,
                total_amount DECIMAL(10, 2),
                status VARCHAR(20) DEFAULT 'pending',
                payment_status VARCHAR(20) DEFAULT 'unpaid',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                booking_id INTEGER REFERENCES bookings(id),
                amount DECIMAL(10, 2) NOT NULL,
                payment_method VARCHAR(50),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                transaction_id VARCHAR(100),
                status VARCHAR(20) DEFAULT 'completed',
                notes TEXT
            )
        """)
        
        # Delete all existing users first
        cursor.execute("DELETE FROM users")
        
        # Insert single admin user
        cursor.execute("""
            INSERT INTO users (username, password, email, full_name, role)
            VALUES ('root', 'roottoor', 'akslnrdn@gmail.com', 'Root User', 'admin')
        """)
        
        connection.commit()
        
        print("✓ All tables created successfully!")
        print("\nCreated tables:")
        print("  - users (admin authentication)")
        print("  - customers (customer information)")
        print("  - bookings (booking records)")
        print("  - payments (payment tracking)")
        print("\nDefault admin user:")
        print("  Username: root")
        print("  Password: roottoor")
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    create_tables()
