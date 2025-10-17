from faker import Faker
import pandas as pd
import random
import os
from datetime import timedelta

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

fake = Faker()

# Helper to generate date ranges
def format_date(d):
    # Formats date as M/D/YY without leading zeros
    return f"{d.month}/{d.day}/{str(d.year)[-2:]}"  # e.g., 5/7/23

def random_date_range():
    start = fake.date_between(start_date='-2y', end_date='today')
    # 30% chance to make a range of 2 days
    if random.random() < 0.3:
        end = start + timedelta(days=random.randint(1, 2))
        return f"{format_date(start)}-{format_date(end)}"
    else:
        return format_date(start)

# Helper to generate time ranges
def random_time_range():
    start_hour = random.randint(6, 20)
    start_minute = random.choice([0, 15, 30, 45])
    duration_minutes = random.randint(30, 150)
    start_time = f"{start_hour%12 or 12}{'am' if start_hour < 12 else 'pm'}"
    end_hour = (start_hour*60 + start_minute + duration_minutes)//60
    end_minute = (start_hour*60 + start_minute + duration_minutes)%60
    end_time = f"{end_hour%12 or 12}{'am' if end_hour < 12 else 'pm'}"
    return f"{start_time}-{end_time}"

# Generate 1000 simulated interactions
data = []

for _ in range(1000):
    # Parties: 1-3 people, sometimes with parentheses or uncertain '?'
    num_parties = random.randint(1,3)
    parties = []
    for _ in range(num_parties):
        name = fake.first_name()
        if random.random() < 0.2:  # 20% chance to add extra info in parentheses
            name += f" ({fake.word()})"
        if random.random() < 0.1:  # 10% chance to add '?'
            name += "?"
        parties.append(name)
    parties_str = ", ".join(parties)

    # Transportation: pick a random participant who drove
    transportation = f"{random.choice([p.split()[0] for p in parties])} drove"

    # Proof text: randomly mention 1-2 participants
    proof_participants = random.sample([p.split()[0] for p in parties], k=min(len(parties), random.randint(1,2)))
    proof = f"{' and '.join(proof_participants)} texts"

    # Event and Location
    event = random.choice(['Birthday party', 'Meeting', 'Picnic', 'Coffee meeting'])
    location = random.choice(['Home', 'Office', 'Park', 'Cafe'])

    # Pictures
    pictures = random.choice(['Yes','No'])

    # Notes: optional, sometimes blank
    notes = fake.sentence() if random.random() < 0.7 else ""

    data.append({
        'Date': random_date_range(),
        'Time': random_time_range(),
        'Proof': proof,
        'Transportation': transportation,
        'Event': event,
        'Location': location,
        'Parties': parties_str,
        'Pictures': pictures,
        'Notes': notes
    })

df = pd.DataFrame(data)

# Ensure column order matches the raw CSV
df = df[['Date','Time','Proof','Transportation','Event','Location','Parties','Pictures','Notes']]

# Save CSV
df.to_csv('data/simulated_interactions.csv', index=False)
print("Simulated dataset created in 'data/simulated_interactions.csv'")