import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config/dicom.ini')
dport = config.getint('Dicom in', 'dport')
sport = config.getint('Dicom in', 'sport')
src_net = config.get('Dicom in', 'src_net')
dst_net = config.get('Dicom in', 'dst_net')

print repr(dport)
print repr(sport)
print repr(dst_net)
print repr(src_net)

print config.sections()
print config.items('Dicom out')