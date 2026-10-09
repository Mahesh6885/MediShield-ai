import random
from datetime import datetime, timedelta
from .models import User, Notification, Setting
from .database import SessionLocal, engine
from .models import Medicine, Supplier, Base

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear old data
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
db.query(User).delete()
db.query(Notification).delete()
db.query(Setting).delete()

# Admin User
admin = User(
    full_name="Mahesh Waran",
    email="admin@medishield.ai",
    phone="+91 9876543210",
    role="Hospital Administrator",
    department="Pharmacy Department",
    hospital="MediShield General Hospital",
)

db.add(admin)

# Settings
db.add(
    Setting(
        theme="light",
        email_alert=True,
        sms_alert=False,
        desktop_alert=True,
    )
)

# Notifications
notifications = [
    ("Critical Medicine Shortage","Insulin stock dropped below safety stock.","Critical"),
    ("Expiry Alert","57 medicines expire within the next 60 days.","Warning"),
    ("Supplier Delivery","Sun Pharma delivered 120 medicines today.","Info"),
    ("AI Prediction Alert","Losartan predicted HIGH shortage risk.","Critical"),
    ("Inventory Health","Inventory health improved to 92%.","Info"),
]

for n in notifications:
    db.add(
        Notification(
            title=n[0],
            message=n[1],
            priority=n[2],
            created_at=datetime.utcnow(),
        )
    )
# ------------------ Medicines ------------------

for i in range(500):

    inventory = random.randint(5, 200)
    demand = random.randint(20, 220)

    expiry = (
        datetime.today() +
        timedelta(days=random.randint(15, 365))
    ).strftime("%Y-%m-%d")

    # AI Risk Logic
    if inventory <= 30:
        risk_level = "High"
    elif inventory <= 80:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    med = Medicine(
        name=f"{random.choice(medicine_names)} {i+1}",
        category=random.choice(categories),
        inventory=inventory,
        demand=demand,
        lead_time=random.randint(1, 8),
        supplier=random.choice(suppliers),
        supplier_reliability=random.randint(60, 99),
        expiry_date=expiry,
        safety_stock=random.randint(5, 25),
        risk_level=risk_level      # ⭐ THIS WAS MISSING
    )

    db.add(med)

# ------------------ Suppliers ------------------

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

print("✅ Database Seeded Successfully!")