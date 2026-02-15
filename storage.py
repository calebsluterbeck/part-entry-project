import json
import os
from models import Part

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "entries.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_entries(entries):
    ensure_data_dir()
    data = []
    for entry in entries:
        data.append({
            "po_number": entry.po_number,
            "num_of_parts": entry.num_of_parts,
            "part_type": entry.part_type,
            "part_number": entry.part_number,
            "ref_letter": entry.ref_letter,
            "sharp_edges": entry.sharp_edges,
            "notes": entry.notes,
            "timestamp": entry.timestamp
        })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read entries file. Starting with an empty list.")
        return []
    
    entries = []
    for item in data:
        part = Part(
            po_number=item.get("po_number", ""),
            num_of_parts=item.get("num_of_parts", 0),
            part_type=item.get("part_type"),
            part_number=item.get("part_number", ""),
            ref_letter=item.get("ref_letter"),
            sharp_edges=item.get("sharp_edges"),
            notes=item.get("notes"),
            timestamp=item.get("timestamp")
        )
        entries.append(part)
    return entries