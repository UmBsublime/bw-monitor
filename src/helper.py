def convert_to_smallest_repr(initial_bytes, divider=1024):

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit = 0
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

def convert_submask_to_cidr(netmask):
    binary_str = ''
    for octet in netmask.split('.'):
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))
