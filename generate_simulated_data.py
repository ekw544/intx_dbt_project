from faker import Faker
import pandas as pd
import random
import os

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

fake = Faker()

# Generate 1000 simulated interactions
data = []
categories = ['Email', 'Call', 'Meeting', 'Chat']

for i in range(1000):
    data.append({
        'interaction_id': i + 1,
        'participant': fake.name(),
        'date': fake.date_between(start_date='-2y', end_date='today'),
        'category': random.choice(categories),
        'duration_minutes': random.randint(5, 120),
        'factor_score': random.randint(1, 10)   # example factor
    })

df = pd.DataFrame(data)

# Save CSV for loading into SQLite/dbt
df.to_csv('data/simulated_interactions.csv', index=False)

print("Simulated dataset created in 'data/simulated_interactions.csv'")