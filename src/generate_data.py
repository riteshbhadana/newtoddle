import pandas as pd
import random
from faker import Faker

fake = Faker()

NUM_CUSTOMERS = 2000
NUM_JOB_CHANGES = 1000

schools = [fake.company() + " School" for _ in range(300)]
toddle_schools = set(random.sample(schools, 120))

school_df = pd.DataFrame({
    "school_name": schools,
    "is_toddle_customer": ["Yes" if s in toddle_schools else "No" for s in schools]
})

customers = []
for i in range(NUM_CUSTOMERS):
    school = random.choice(list(toddle_schools))
    customers.append([i, fake.name(), school])

customer_df = pd.DataFrame(customers, columns=["person_id", "name", "current_school"])

job_changes = []
for _ in range(NUM_JOB_CHANGES):
    person = random.choice(customers)
    new_school = random.choice(schools)
    job_changes.append([
        person[0],
        person[2],
        new_school,
        fake.date_this_year()
    ])

job_df = pd.DataFrame(job_changes, columns=[
    "person_id", "old_school", "new_school", "change_date"
])

school_df.to_csv("../data/schools.csv", index=False)
customer_df.to_csv("../data/customers.csv", index=False)
job_df.to_csv("../data/job_changes.csv", index=False)

print("Data generated!")