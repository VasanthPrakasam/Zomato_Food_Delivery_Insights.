import mysql.connector
from mysql.connector import Error

# Database configuration (replace with your actual details or import from DBConnection)
# For simplicity, we are including it here, but in a real application,
# you might import the connection object or configuration from DBConnection.py
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "3vt9swSrSwtAhk9.root",
    "password": "CoCcz77GGaohhPXx",
    "port": 4000,
    "database": "ZomatoClass" # Assuming a database name exists
}

def create_tables(host, user, password, port, database):
    """Creates the necessary tables in the database."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        if conn.is_connected():
            print("Connected to MySQL database for table creation")
            cursor = conn.cursor()

            # Define the SQL CREATE TABLE statements
            create_customers_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                phone VARCHAR(20),
                location TEXT,
                signup_date DATE,
                is_premium BOOLEAN,
                preferred_cuisine VARCHAR(100),
                total_orders INT DEFAULT 0,
                average_rating DECIMAL(3, 2) DEFAULT 0.0
            );
            """

            create_restaurants_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_restaurant (
                restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                cuisine_type VARCHAR(100),
                location TEXT,
                owner_name VARCHAR(255),
                average_delivery_time INT,
                contact_number VARCHAR(20),
                rating DECIMAL(3, 2),
                total_orders INT DEFAULT 0,
                is_active BOOLEAN
            );
            """

            create_delivery_persons_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_delivery_persons (
                delivery_person_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                contact_number VARCHAR(20),
                vehicle_type VARCHAR(50),
                total_deliveries INT DEFAULT 0,
                average_rating DECIMAL(3, 2) DEFAULT 0.0,
                location TEXT
            );
            """

            create_orders_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_order_details (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                restaurant_id INT,
                order_date DATETIME,
                delivery_time DATETIME,
                status VARCHAR(50),
                total_amount DECIMAL(10, 2),
                payment_mode VARCHAR(50),
                discount_applied DECIMAL(10, 2),
                feedback_rating DECIMAL(3, 2),
                FOREIGN KEY (customer_id) REFERENCES tbl_customers (customer_id),
                FOREIGN KEY (restaurant_id) REFERENCES tbl_restaurant (restaurant_id)
            );
            """

            create_deliveries_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_deliveries (
                delivery_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                delivery_person_id INT,
                delivery_status VARCHAR(50),
                distance DECIMAL(10, 2),
                delivery_time INT,
                estimated_time INT,
                delivery_fee DECIMAL(10, 2),
                vehicle_type VARCHAR(50),
                FOREIGN KEY (order_id) REFERENCES tbl_order_details (order_id),
                FOREIGN KEY (delivery_person_id) REFERENCES tbl_delivery_persons (delivery_person_id)
            );
            """

            # Execute the CREATE TABLE statements in the correct order
            print("Creating tbl_customers...")
            cursor.execute(create_customers_table_sql)
            print("Creating tbl_restaurant...")
            cursor.execute(create_restaurants_table_sql)
            print("Creating tbl_delivery_persons...")
            cursor.execute(create_delivery_persons_table_sql)
            print("Creating tbl_order_details...")
            cursor.execute(create_orders_table_sql)
            print("Creating tbl_deliveries...")
            cursor.execute(create_deliveries_table_sql)


            # Commit the changes
            conn.commit()
            print("All tables created successfully (if they didn't exist).")

    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed after table creation.")

if __name__ == '__main__':
    # Example usage:
    # Replace with your actual database configuration
    # config = {
    #     "host": "your_host",
    #     "user": "your_user",
    #     "password": "your_password",
    #     "port": your_port,
    #     "database": "your_database"
    # }
    create_tables(**config)
