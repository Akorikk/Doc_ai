import re

def extract_fields(text):

    def find(pattern):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None

    data = {
        "shipment_id": find(r"(?:Shipment|Load)\s*ID[:\s]+([A-Z0-9-]+)"),
        "shipper": find(r"Shipper[:\s]+(.+)"),
        "consignee": find(r"Consignee[:\s]+(.+)"),
        "pickup_datetime": find(r"Pickup[:\s]+(.+)"),
        "delivery_datetime": find(r"Delivery[:\s]+(.+)"),
        "equipment_type": find(r"Equipment[:\s]+(.+)"),
        "mode": find(r"Mode[:\s]+(.+)"),
        "rate": find(r"Rate[:\s]+\$?([\d,.]+)"),
        "currency": "USD",
        "weight": find(r"Weight[:\s]+([\d,.]+\s*(?:lbs|kg))"),
        "carrier_name": find(r"Carrier[:\s]+(.+)")
    }

    return data
