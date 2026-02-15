# Part entry main loop
from models import Part
from formatter import formatted_part_id
from storage import load_entries, save_entries
from export import export_csv
from validation import validate_part_input
from manager import add_entry, get_entries_grouped_by_po, delete_entry, search_by_part_number, search_by_po, search_all

def display():
    print("\n--- Part Entry ---")
    print("1. Add Part Entry")
    print("2. View All Entries (Grouped by P.O.)")
    print("3. Search Entries")
    print("4. Delete an Entry")
    print("5. Export to CSV")
    print("6. Exit")

def get_part_input():
    while True:
        po_number = input("P.O. Number: ").strip()
        part_number = input("Part Number: ").strip()

        pieces_input = input("Number of Pieces: ").strip()
        try:
            num_of_parts = int(pieces_input)
        except ValueError:
            print("Invalid input. Number of pieces must be a number.")
            continue

        part_type_input = input("Part Type (leave blank if none): ").strip()
        part_type = part_type_input if part_type_input else None

        ref_letter_input = input("Reference Letter (leave blank if none): ").strip().upper()
        ref_letter = ref_letter_input if ref_letter_input else None

        sharp_input = input("Sharp edges requested? (y/n): ").strip().lower()
        sharp_edges = sharp_input == "y"

        notes = input("Notes (leave blank to skip): ").strip() or None

        errors = validate_part_input(po_number, part_number, num_of_parts, part_type, ref_letter)

        if errors:
            print("\nPlease fix the following:")
            for error in errors:
                print(f"  - {error}")
            print()
            continue

        return Part(
            po_number=po_number,
            part_number=part_number,
            num_of_parts=num_of_parts,
            part_type=part_type,
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
            print("\nSearch by:")
            print("a. P.O. Number")
            print("b. Part Number")
            print("c. All Fields")
            search_type = input("Select: ").strip().lower()

            query = input("Search query: ").strip()
            if not query:
                print('No query entered.')
                continue

            results = []
            if search_type == 'a':
                results = search_by_po(entries, query)
            elif search_type == 'b':
                results = search_by_part_number(entries, query)
            elif search_type == 'c':
                results = search_all(entries, query)

            if not results:
                print(f"\nNo results found for '{query}'.")
            else:
                print(f"\nFound {len(results)} result{'s' if len(results) > 1 else ''} for '{query}':")
                grouped = get_entries_grouped_by_po(results)
                for po, parts in grouped.items():
                    print(f"\n---P.O. Number: {po} ({len(parts)} part{'s' if len(parts) > 1 else ''})---")
                    for i, p in enumerate(parts, 1):
                        part_id = formatted_part_id(p.part_number, p.part_type, p.ref_letter)
                        deburr_tag = "De-burr" if p.deburr else "Sharp"
                        print(f" {i}. {part_id} | Number of Pieces: {p.num_of_parts} | {deburr_tag}")

        elif choice == '4':
            if not entries:
                print("\nNo entries to delete.")
                continue

            print("\nSelect an entry to delete:")
            for i, entry in enumerate(entries, 1):
                part_id = formatted_part_id(entry.part_number, entry.part_type, entry.ref_letter)
                print(f" {i}. P.O. {entry.po_number} | {part_id} | Pieces: {entry.num_of_parts}")

            try:
                index_input = input("Enter the number of the entry to delete: ").strip()
                index = int(index_input) - 1
                if 0 <= index < len(entries):
                    removed_entry = entries.pop(index)
                    save_entries(entries)
                    part_id = formatted_part_id(removed_entry.part_number, removed_entry.part_type, removed_entry.ref_letter)
                    print(f"\nDeleted: P.O. {removed_entry.po_number} | {part_id}")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '5':
            filepath = export_csv(entries)
            if filepath:
                print(f"CSV exported successfully to {filepath}")
        
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
    # test 