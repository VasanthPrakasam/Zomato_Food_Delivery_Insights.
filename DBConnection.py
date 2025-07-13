import mysql.connector
from mysql.connector import Error
import pandas as pd

class ZomatoClass:
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.conn = None
        self.cursor = None
        # Establish connection immediately upon initialization
        self.create_connection()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database
            )
            if self.conn.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None # Ensure conn is None on failure
            self.cursor = None # Ensure cursor is None on failure


    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        self.conn = None # Ensure conn is None after closing
        self.cursor = None # Ensure cursor is None after closing


    def fetch_orders(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                    return pd.DataFrame() # Return empty DataFrame if connection fails

            query = "SELECT * FROM tbl_order_details"
            df = pd.read_sql(query, self.conn)
            return df
        except Error as e:
            print(f"Error fetching orders: {e}")
            return pd.DataFrame()

    def fetch_restaurant(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                    return pd.DataFrame() # Return empty DataFrame if connection fails

            query = "SELECT * FROM tbl_restaurant"
            df = pd.read_sql(query, self.conn)
            return df
        except Error as e:
            print(f"Error fetching restaurants: {e}")
            return pd.DataFrame()

    def insert_order(self, order):
        #Inserts a new order into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to insert order: Database connection not established.")
                     return # Exit if connection fails

            query = """
            INSERT INTO tbl_order_details ( customer_id,        restaurant_id, order_date,
            delivery_time,
            status,
            total_amount,
            payment_mode,
            discount_applied,
            feedback_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, order)
            self.conn.commit()
            print("Order inserted successfully!")
        except Error as e:
            print(f"Error inserting order: {e}")


    def insert_customers(self,customer):
    #Inserts a new customer into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to insert customer: Database connection not established.")
                     return # Exit if connection fails

            query = """
            INSERT INTO tbl_customers(name,
            email,
            phone,
            location,
            signup_date,
            is_premium,
            preferred_cuisine,
            total_orders,
            average_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, customer)
            self.conn.commit()
            print("Customer inserted successfully!")
        except Error as e:
            print(f"Error inserting customer: {e}")

    def insert_Delivery_Persons(self,delivery_person):
    #Inserts a new customer into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to insert delivery person: Database connection not established.")
                     return # Exit if connection fails

            query = """
            INSERT INTO tbl_delivery_persons(name,
            contact_number,
            vehicle_type,
            total_deliveries,
            average_rating,
            location)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, delivery_person)
            self.conn.commit()
            print("Delivery person details inserted successfully!")
        except Error as e:
            print(f"Error inserting delivery person: {e}")

    def insert_Restaurants(self,restaurant):
    #Inserts a new Restaurant into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to insert restaurant: Database connection not established.")
                     return # Exit if connection fails

            query = """
            INSERT INTO tbl_restaurant(name,
            cuisine_type,
            location,
            owner_name,
            average_delivery_time,
            contact_number,
            rating,
            total_orders,
            is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, restaurant)
            self.conn.commit()
            print("Restaurant details inserted successfully!")
        except Error as e:
            print(f"Error inserting restaurant: {e}")

    def insert_deliveries(self,delivery): # Corrected method name from insert_deliverys
    #Inserts a new delivery into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to insert delivery: Database connection not established.")
                     return # Exit if connection fails
            query = """
            INSERT INTO tbl_deliveries(order_id,
            delivery_person_id,
            delivery_status,
            distance,
            delivery_time,
            estimated_time,
            delivery_fee,
            vehicle_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, delivery)
            self.conn.commit()
            print("Delivery details inserted successfully!")
        except Error as e:
            print(f"Error inserting delivery: {e}")


    def execute_query(self, query):
    #execute with given query
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
                if self.conn is None: # Check connection again after trying to create
                     print("Failed to execute query: Database connection not established.")
                     return None # Return None if connection fails
            self.cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully!")
        except Error as e:
            print(f"Error executing query: {e}")
            return None # Return None on error
