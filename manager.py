from formatter import formatted_part_id
from models import Part
from collections import OrderedDict

def add_entry(entries, part):
    entries.append(part)

def delete_entry(entries, index):
    if 0 <= index < len(entries):
        removed = entries.pop(index)
        return entries, removed
    return entries, None

def get_entries_grouped_by_po(entries):
    grouped = OrderedDict()
    for entry in entries:
        po = entry.po_number
        if po not in grouped:
            grouped[po] = []
        grouped[po].append(entry)
    return grouped

def get_entry_by_po(entries, po_number):
    return [entry for entry in entries if entry.po_number == po_number]

def search_by_po(entries, query):
    query = query.strip().lower()
    return [entry for entry in entries if query in entry.po_number.lower()]

def search_by_part_number(entries, query):
    query = query.strip().lower()
    return [entry for entry in entries if query in entry.part_number.lower()]

def search_all(entries, query):
    query = query.strip().lower()
    results = []
    for entry in entries:
        if (query in entry.po_number.lower() or
            query in entry.part_number.lower() or
            (entry.part_type and query in str(entry.part_type).lower()) or
            (entry.ref_letter and query in entry.ref_letter.lower())):
            results.append(entry)
    return results

def clear_all():
    return []

