
from pathlib import Path
from astropy.io import ascii
from astropy.table import Table

"""
Extract only stars identified as members by the 'members_select' code
"""

cols_rem = ['prob' + str(_) for _ in range(25)]

files = []
for pp in Path('../2_pipeline/3_members_select/out').iterdir():
    if pp.is_file():
        files += [pp]

for file in files:
    print(file)
    data = Table.read(file, format='ascii')
    msk = data['membs_select'] == 1
    data = data[msk]
    data.remove_columns(cols_rem)
    ascii.write(
        data, '../2_pipeline/4_members/' + file.name.replace('membs_', ''),
        format='csv', overwrite=True)
