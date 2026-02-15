def validate_part_input(po_number, part_number, num_of_parts, part_type=None, ref_letter=None):
    errors = []

    if not po_number or not po_number.strip():
        errors.append('PO Number is required.')

    if not part_number or not part_number.strip():
        errors.append('Part Number is required.')

    if num_of_parts is None:
        errors.append('Number of Parts is required.')
    elif not isinstance(num_of_parts, int) or num_of_parts <= 0:
        errors.append('Number of Parts must be a positive number.')

    if part_type is not None:
        if not isinstance(part_type, str) or not part_type.strip():
            errors.append('Part Type must be a non-empty string if provided.')
    
    if ref_letter is not None:
        if not ref_letter.isalpha():
            errors.append('Reference Letter must be a single alphabetic character if provided.')

    return errors
    