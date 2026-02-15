# Part entry main loop
from models import Part
from formatter import formatted_part_id
from manager import add_entry, get_entries_grouped_by_po, delete_entry
from storage import load_entries, save_entries
from export import export_csv

def display():
    print("\n--- Part Entry ---")
    print("1. Add Part Entry")
    print("2. View All Part Entries (Grouped by PO Number)")
    print("3. Delete an Entry")
    print("4. Export to CSV")
    print("5. Exit")

def get_part_input():
    po_number = input("P.O. Number: ")
    num_of_parts = int(input("Number of Parts: "))
    part_number = input("Part Number: ")

    part_type_input = input("Part Type (Leave blank if none):").strip()
    part_type = part_type_input if part_type_input else None

    ref_letter_input = input("Reference Letter (If none then enter 0): ").strip()
    ref_letter = ref_letter_input if ref_letter_input else None

    sharp_edges_input = input("Sharp Edges? (y/n): ").strip().lower()
    sharp_edges = sharp_edges_input == 'y'

    notes = input("Additional Notes (Optional): ").strip() or None

    return Part(
        po_number=po_number,
        num_of_parts=num_of_parts,
        part_type=part_type,
        part_number=part_number,
        ref_letter=ref_letter,
        sharp_edges=sharp_edges,
        notes=notes
    )

def main():
    entries = load_entries()
    while True:
        display()
        choice = input("\n Select an option: ").strip()

        if choice == '1':
            part = get_part_input()
            entries.append(part)
            save_entries(entries)
            part_id = formatted_part_id(part.part_number, part.part_type, part.ref_letter)
            print(f"\nAdded: {part_id} (Deburr: {'Yes' if part.deburr else 'No'})")

        elif choice == '2':
            grouped = get_entries_grouped_by_po(entries)
            if not grouped:
                print("\nNo entries found.")
            else:
                for po, parts in grouped.items():
                   print(f"\n---P.O. Number: {po} ({len(parts)} part{'s' if len(parts) > 1 else ''})---")
                   for i, p in enumerate(parts, 1):
                       part_id = formatted_part_id(p.part_number, p.part_type, p.ref_letter)
                       deburr_tag = "De-burr" if p.deburr else "Sharp"
                       print(f" {i}. {part_id} | Number of Pieces: {p.num_of_parts} | {deburr_tag}")

        elif choice == '3':
            pass

        elif choice == '4':
            filepath = export_csv(entries)
            if filepath:
                print(f"CSV exported successfully to {filepath}")
        
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
    # test 