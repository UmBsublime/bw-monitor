def convert_to_smallest_repr(initial_bytes, divider=1024):

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit = 0
    modulus = 0
    while True:
        if initial_bytes >= divider:
            modulus = initial_bytes % divider
            initial_bytes = initial_bytes / divider

            if modulus >= (divider / 2):
                initial_bytes += 1
            unit += 1
        else:
            #if initial_bytes == 0:
            #    initial_bytes = float(modulus) / float(divider)
            return str(initial_bytes) + ' ' + units[unit]


print convert_to_smallest_repr(1024)

