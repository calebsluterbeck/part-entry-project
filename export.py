import csv
import os
from datetime import datetime
from formatter import formatted_part_id
from manager import get_entries_grouped_by_po

EXPORT_DIR = "exports"

def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def export_csv(entries):
    if not entries:
        print("No entries to export.")
        return None

    ensure_export_dir()
    filename = f"part-log-{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    grouped = get_entries_grouped_by_po(entries)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "P.O. Number",
            "Formatted ID",
            "Part Number",
            "Part Type",
            "Ref Letter",
            "Pieces",
            "Sharp Edges",
            "De-burr",
            "Notes",
            "Timestamp"
        ])

        for po, parts in grouped.items():
            for part in parts:
                part_id = formatted_part_id(part.part_number, part.part_type, part.ref_letter)
                writer.writerow([
                    part.po_number,
                    part_id,
                    part.part_number,
                    part.part_type if part.part_type else "",
                    part.ref_letter if part.ref_letter else "0",
                    part.num_of_parts,
                    "Yes" if part.sharp_edges else "No",
                    "Yes" if part.deburr else "No",
                    part.notes if part.notes else "",
                    part.timestamp if part.timestamp else ""
                ])

    print(f"Exported to {filepath}")
    return filepath