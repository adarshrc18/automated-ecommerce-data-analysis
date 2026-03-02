import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


#  DATABASE CONNECTION 

#  Replace 'yourpassword' with your MySQL password
engine = create_engine(
    "mysql+mysqlconnector://root:mysqladarshrc18@localhost/ecommerce_db"
)

# Read data from MySQL
df = pd.read_sql("SELECT * FROM sales_data", engine)

print("\n===== SAMPLE DATA =====")
print(df.head())

print("\nTotal Rows:", len(df))



#  BUSINESS KPI CALCULATIONS

print("\n===== BUSINESS KPIs =====")

# Total Revenue
total_revenue = df['total_amount'].sum()
print("Total Revenue:", round(total_revenue, 2))

# Simulate cost price (60% of selling price)
df['cost_price'] = df['price'] * 0.6

# Calculate profit per order
df['profit'] = df['total_amount'] - (df['cost_price'] * df['quantity'])

# Total Profit
total_profit = df['profit'].sum()
print("Total Profit:", round(total_profit, 2))

# Profit Margin %
profit_margin = (total_profit / total_revenue) * 100
print("Profit Margin %:", round(profit_margin, 2))




#  TOP 5 CUSTOMERS

print("\n===== TOP 5 CUSTOMERS BY REVENUE =====")

top_customers = (
    df.groupby('customer_name')['total_amount']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_customers)




# CATEGORY PERFORMANCE

print("\n===== CATEGORY PERFORMANCE =====")

category_analysis = (
    df.groupby('category')
    .agg({
        'total_amount': 'sum',
        'profit': 'sum'
    })
    .sort_values(by='total_amount', ascending=False)
)

print(category_analysis)




#  MONTHLY REVENUE TREND

print("\n===== MONTHLY REVENUE TREND =====")

df['order_date'] = pd.to_datetime(df['order_date'])

monthly_trend = (
    df.groupby(df['order_date'].dt.month)['total_amount']
    .sum()
)

print(monthly_trend)

# Dynamic Top N Customers and Products


N = 5  # You can change this dynamically

top_customers = df.groupby('customer_name')['total_amount'].sum().sort_values(ascending=False).head(N)
top_products = df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head(N)

print("\n===== TOP CUSTOMERS =====")
print(top_customers)
print("\n===== TOP PRODUCTS =====")
print(top_products)




# Category Performance with Profit Margin
category_summary = df.groupby('category').agg({'total_amount':'sum', 'profit':'sum'})
category_summary['profit_margin'] = (category_summary['profit'] / category_summary['total_amount']) * 100

print("\n===== CATEGORY PERFORMANCE =====")
print(category_summary.sort_values(by='total_amount', ascending=False))




# Visualizations

# Revenue by Category
plt.figure(figsize=(8,5))
sns.barplot(x=category_summary.index, y=category_summary['total_amount'])
plt.title("Revenue by Category")
plt.ylabel("Revenue")
plt.xlabel("Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Monthly Revenue Trend
monthly_revenue = df.groupby(df['order_date'].dt.month)['total_amount'].sum()
plt.figure(figsize=(8,5))
sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(monthly_revenue.index)
plt.tight_layout()
plt.show()