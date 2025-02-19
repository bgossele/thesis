default_ped_fields = ["family_id", "name", "paternal_id", "maternal_id",
                      "sex", "phenotype"]
missing_member = set(["None", None, "0", "-9"])

def get_ped_fields(ped_file):
    if not ped_file:
        return default_ped_fields

    with open(ped_file) as in_handle:
        possible_header = in_handle.readline()

    if possible_header.startswith("#"):
        header = possible_header.replace("#", "").split()
        # rename the standard fields to a common name
        header = default_ped_fields + header[len(default_ped_fields):]
        return possible_header.replace("#", "").split()
    else:
        return default_ped_fields

def load_ped_file(ped_file):
    ped_dict = {}
    for line in open(ped_file, 'r'):
        if line.startswith("#") or len(line) == 0:
            continue
        fields = _fix_ped_family_fields(line.split())
        ped_dict[fields[1]] = fields
    return ped_dict

def _fix_ped_family_fields(fields):
    """
    translate commonly used values for missing family members to the canonical
    0 == missing style used in the PED spec
    """
    family_fields = [0, 2, 3]
    for field in family_fields:
        if fields[field] in missing_member:
            fields[field] = "0"
    return fields
