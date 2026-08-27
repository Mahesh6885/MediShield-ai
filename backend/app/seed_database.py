import random
from datetime import datetime, timedelta

from .database import SessionLocal
from .models import Medicine, Supplier

db = SessionLocal()

db.query(Medicine).delete()
db.query(Supplier).delete()

medicine_names = [
    "Paracetamol","Ibuprofen","Amoxicillin","Cefixime","Azithromycin",
    "Insulin","Metformin","Aspirin","Vitamin C","Vitamin D",
    "Rabies Vaccine","Omeprazole","Pantoprazole","Cetirizine",
    "ORS","Dolo","Losartan","Atorvastatin","Cough Syrup","Salbutamol"
]

categories = [
    "Analgesic",
    "Antibiotic",
    "Vaccine",
    "Antidiabetic",
    "Vitamin",
    "Cardiology"
]

suppliers = [
    "Sun Pharma",
    "Cipla",
    "Apollo Pharma",
    "Dr. Reddy's",
    "Aurobindo",
    "Mankind"
]

for i in range(500):

    expiry = (
        datetime.today() +
        timedelta(days=random.randint(15,365))
    ).strftime("%Y-%m-%d")

    med = Medicine(
        name=f"{random.choice(medicine_names)} {i+1}",
        category=random.choice(categories),
        inventory=random.randint(5,200),
        demand=random.randint(20,220),
        lead_time=random.randint(1,8),
        supplier=random.choice(suppliers),
        supplier_reliability=random.randint(60,99),
        expiry_date=expiry,
        safety_stock=random.randint(5,25)
    )

    db.add(med)

supplier_data = [
    ("Sun Pharma",95,98,2,120),
    ("Cipla",92,95,3,110),
    ("Dr. Reddy's",90,93,4,105),
    ("Apollo Pharma",91,94,3,112),
    ("Aurobindo",88,89,5,95),
    ("Mankind",87,88,4,100)
]

for s in supplier_data:
    supplier = Supplier(
        name=s[0],
        quality_score=s[1],
        reliability=s[2],
        delivery_days=s[3],
        cost=s[4],
        score=0
    )
    db.add(supplier)

db.commit()
db.close()

print("Database Seeded Successfully!")