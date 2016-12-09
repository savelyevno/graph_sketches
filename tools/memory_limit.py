import resource

MEM_LIMIT = 4   # gigs

rsrc = resource.RLIMIT_AS
soft, hard = resource.getrlimit(rsrc)
print('Soft limit:', soft, 'Hard limit:', hard)
resource.setrlimit(rsrc, (MEM_LIMIT*int(1e9), MEM_LIMIT*int(1e9)))

soft, hard = resource.getrlimit(rsrc)
print('Hard limit changed to :', hard >> 22, 'MB')

"""
rsrc = resource.RLIMIT_DATA
soft, hard = resource.getrlimit(rsrc)
print('Soft limit:', soft, 'Hard limit:', hard)
resource.setrlimit(rsrc, (0, MEM_LIMIT << 30))

soft, hard = resource.getrlimit(rsrc)
print('Hard limit changed to :', hard >> 20, 'MB')
"""