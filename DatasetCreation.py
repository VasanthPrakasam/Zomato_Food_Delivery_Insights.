from faker import Faker
from faker.providers import BaseProvider
import random
from datetime import datetime, timedelta

# Initialize Faker with Indian locale
fake = Faker('en_IN')

# Define custom providers
class ChennaiAddressProvider(BaseProvider):
    def chennai_address(self):
        chennai_localities = [
            "T. Nagar", "Adyar", "Velachery", "Anna Nagar", "Mylapore", "Guindy",
            "Tambaram", "Perungudi", "Kodambakkam", "Nungambakkam", "Kilpauk","Chrompet"
        ]
        street = self.generator.street_name()
        locality = self.random_element(chennai_localities)
        return f"{street}, {locality}, Chennai, Tamil Nadu, India - {self.generator.postcode()}"

class TwoWheelerProvider(BaseProvider):
    def two_wheeler(self):
        two_wheelers = ["Bike", "Scooter", "Motorcycle", "Electric Bike", "Electric Scooter", "Moped"]
        return self.random_element(two_wheelers)

# Add custom providers to Faker instance
fake.add_provider(ChennaiAddressProvider)
fake.add_provider(TwoWheelerProvider)

# --- Data Generation Functions ---

def generate_delivery_persons_data(num_records):
    deliveryPersonTable = []
    for i in range(num_records):
        deliveryPersonTable.append((
            fake.name(),
            fake.unique.phone_number(),
            fake.two_wheeler(),
            random.randint(0, 300),
            round(random.uniform(0, 5), 2),
            fake.chennai_address()
        ))
    return deliveryPersonTable

def generate_customers_data(num_records):
    CustTable = []
    for i in range(num_records):
        CustTable.append((
            fake.name(),
            fake.unique.email(),
            fake.unique.phone_number(),
            fake.chennai_address(),
            fake.date_this_decade(),
            random.choice([True, False]),
            random.choice(["North Indian", "South Indian", "Chinese", "Italian", "Continental"]),
            random.randint(0, 100),
            round(random.uniform(0, 5), 2)
        ))
    return CustTable

def generate_restaurants_data(num_records):
    cuisine_types = [
        "South Indian", "North Indian", "Chettinad", "Andhra", "Kerala", "Biryani", "Seafood",
        "Chinese", "Thai", "Japanese", "Korean", "Italian", "Mexican", "French", "Mediterranean",
        "Continental", "BBQ", "Fast Food", "Street Food", "Cafe", "Bakery", "Desserts", "Juice Bar"
    ]
    prefixes = ["Spicy", "Royal", "Tandoori", "Grand", "Golden", "Classic", "Chennai", "Madras", "Authentic", "Savor", "Flavors of", "Delicious"]
    suffixes = ["Kitchen", "Bistro", "Diner", "Cafe", "Grill", "Lounge", "Eatery", "Corner", "Spot", "Point", "House", "Hut"]

    restaurants = []
    while len(restaurants) < num_records:
        name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        cuisine = random.choice(cuisine_types)
        restaurant_entry = f"{name} ({cuisine})"

        if restaurant_entry not in restaurants:
            restaurants.append(restaurant_entry)

    RestaurantTable = []
    for i in range(num_records):
        RestaurantTable.append((
            restaurants[i],
            random.choice(["North Indian", "South Indian", "Chinese", "Italian", "Continental"]),
            fake.chennai_address(),
            fake.name(),
            random.randint(0, 120),
            fake.unique.phone_number(),
            round(random.uniform(0, 5), 2),
            random.randint(0, 3000),
            random.choice([True, False])
        ))
    return RestaurantTable

def generate_orders_data(num_records, max_customer_id, max_restaurant_id):
    orderTable = []
    for i in range(num_records):
        order_datetime = fake.date_time_between(start_date="-2y", end_date="now")
        delivery_datetime = order_datetime + timedelta(minutes=random.randint(30, 90))
        statuses = ['Pending','Delivered','Cancelled']
        random_status = random.choice(statuses)

        orderTable.append((
                random.randint(1, max_customer_id),
                random.randint(1, max_restaurant_id),
                order_datetime,
                delivery_datetime,
                random_status,
                round(random.uniform(1, 5000), 2),
                fake.random_element(["Credit Card", "Cash", "UPI"]),
                round(random.uniform(0, 50), 2),
                round(random.uniform(0, 5), 2)
            ))
    return orderTable

def generate_deliveries_data(num_records, max_order_id, max_delivery_person_id):
    deliveryTable = []
    for i in range(num_records):
        deliveryTable.append((
            random.randint(1, max_order_id),
            random.randint(1, max_delivery_person_id),
            fake.random_element(["Pending", "On the way", "Delivered", "Cancelled"]),
            round(random.uniform(1, 50), 2),
            random.randint(15, 60),
            random.randint(20, 70),
            round(random.uniform(0, 50), 2),
            fake.two_wheeler()
        ))
    return deliveryTable

# Example usage:
# delivery_persons_data = generate_delivery_persons_data(500)
# customers_data = generate_customers_data(500)
# restaurants_data = generate_restaurants_data(200)
# orders_data = generate_orders_data(1500, 500, 200) # Assuming 500 customers and 200 restaurants
# deliveries_data = generate_deliveries_data(1500, 1500, 500) # Assuming 1500 orders and 500 delivery persons
