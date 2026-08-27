from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Medicine, Supplier

def chatbot_response(message: str, db: Session):

    text = message.lower()

    # ---------------- Low Stock ----------------
    if "low stock" in text:

        medicines = db.query(Medicine).all()

        result = []

        for m in medicines:
            if m.inventory <= m.safety_stock:
                result.append(f"• {m.name} ({m.inventory} units left)")

        if result:
            return "\n".join(result)

        return "All medicines currently have sufficient inventory."

    # ---------------- Expiry ----------------
    if "expire" in text or "expiry" in text:

        medicines = db.query(Medicine).all()

        expiring = []

        for m in medicines:

            days = (
                datetime.strptime(m.expiry_date,"%Y-%m-%d")
                - datetime.today()
            ).days

            if days <= 60:
                expiring.append(f"• {m.name} expires in {days} days.")

        if expiring:
            return "\n".join(expiring)

        return "No medicines expire within the next 60 days."

    # ---------------- Supplier ----------------
    if "best supplier" in text:

        suppliers = db.query(Supplier).all()

        best = max(
            suppliers,
            key=lambda s:(s.reliability+s.quality_score)-s.delivery_days
        )

        return (
            f"Best supplier is {best.name}.\n"
            f"Reliability: {best.reliability}%\n"
            f"Quality Score: {best.quality_score}%\n"
            f"Delivery Time: {best.delivery_days} days."
        )

    # ---------------- High Risk ----------------
    if "high risk" in text:

        medicines = db.query(Medicine).filter(
            Medicine.risk_level=="High"
        ).all()

        if medicines:
            return "\n".join([f"• {m.name}" for m in medicines])

        return "No medicines are currently High Risk."

    # ---------------- Inventory Health ----------------
    if "inventory health" in text:

        medicines = db.query(Medicine).all()

        healthy = sum(
            1 for m in medicines if m.inventory > m.safety_stock
        )

        score = round((healthy/len(medicines))*100,2)

        return f"Current Inventory Health is {score}%."

    # ---------------- Search Medicine ----------------
    medicines = db.query(Medicine).all()

    for med in medicines:

        if med.name.lower() in text:

            return (
                f"{med.name}\n\n"
                f"Inventory : {med.inventory}\n"
                f"Demand : {med.demand}\n"
                f"Risk Level : {med.risk_level}\n"
                f"Supplier Reliability : {med.supplier_reliability}%"
            )

    return (
        "I can help you with:\n\n"
        "• Low stock medicines\n"
        "• Expiry alerts\n"
        "• Best supplier\n"
        "• High risk medicines\n"
        "• Inventory health\n"
        "• Search any medicine by name"
    )