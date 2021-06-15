
import numpy as np
from astropy.io import ascii
from astropy.table import Table

"""
Remove not used columns from a data file. Makes the file smaller and more
manageable.
"""


cols = (
    'EDR3Name', '_x', '_y', 'RA_ICRS', 'DE_ICRS', 'Plx', 'e_Plx', 'pmRA',
    'e_pmRA', 'pmDE', 'e_pmDE', 'Gmag', 'e_Gmag', 'BP-RP', 'e_BP-RP',
    'V', 'eV', 'BV', 'eBV', 'UB', 'eUB', 'VI', 'eVI')

in_folder = '../0_data/6_GaiaEDR3/'
out_folder = '../2_pipeline/1_data_filter/out/'
files = ("haf14_match", "rup41_match", "rup42_match", "rup44_match",
         "rup152_match")

for file in files:
    print(file)
    data = Table.read(in_folder + file + '.dat', format='ascii')

    # Add BP-RP uncertainty
    data['e_BP-RP'] = np.sqrt(data['e_BPmag']**2 + data['e_RPmag']**2)

    data = data[cols]
    print("Total number of stars in file", len(data))

    out_file = file.replace("_match", "")
    ascii.write(data, out_folder + out_file + '.dat', format='csv',
                overwrite=True)
