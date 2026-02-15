# Formatting function

def formatted_part_id(part_number, part_type, ref_letter):

    ref = ref_letter if ref_letter else "0"

    if part_type:
        return f"{part_number}-{part_type}-{ref}"
    else:
        return f"{part_number}-{ref}"