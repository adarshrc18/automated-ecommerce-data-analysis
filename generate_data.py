import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine

print("Starting MySQL data generation...")

# -----------------------
# Configuration
# -----------------------
USERNAME = "root"
PASSWORD = "YOUR_PASSWORD"   # <-- Put your MySQL password here
HOST = "localhost"
DATABASE = "ecommerce_db"

# -----------------------
# Create MySQL Engine (SAFE METHOD)
# -----------------------
engine = create_engine(
    f"mysql+pymysql://{USERNAME}@{HOST}/{DATABASE}",
    connect_args={"password":"mysqladarshrc18"}
)

# -----------------------
# Generate Fake Data
# -----------------------
fake = Faker()
num_records = 300

categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]

data = []

for _ in range(num_records):
    price = round(random.uniform(100, 5000), 2)
    quantity = random.randint(1, 5)

    data.append({
        "order_id": random.randint(10000, 99999),
        "customer_name": fake.name(),
        "email": fake.email(),
        "product_name": fake.word().capitalize(),
        "category": random.choice(categories),
        "price": price,
        "quantity": quantity,
        "total_amount": price * quantity,
        "order_date": fake.date_this_year()
    })

df = pd.DataFrame(data)

# -----------------------
# Insert into MySQL
# -----------------------
df.to_sql(
    name="sales_data",
    con=engine,
    if_exists="replace",
    index=False
)

print(" 300 records successfully inserted into MySQL!")