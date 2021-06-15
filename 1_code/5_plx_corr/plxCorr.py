
from zero_point import zpt
from pathlib import Path
from astropy.io import ascii
from astropy.table import Table
import matplotlib.pyplot as plt

"""
Based on the functions described in Lindegren et al. 2020, the code returns
the estimated parallax zero-point given the ecliptic latitude, magnitude and
colour of any Gaia (E)DR3 source.

The code automatically deals with a mix of 5-p and 6-p solutions

As explained in Lindegren et al. 2020, the interpolations are only calibrated
within the following intervals:

1. $G$ magnitude: 6 < phot_g_mean_mag < 21
2. Colour:
  1. 1.1 < nu_eff_used_in_astrometry < 1.9 (5-p sources)
  2. 1.24 < pseudocolour < 1.72 (6-p sources)

Outside these ranges, the zero-point obtained is an extrapolation.

Source: https://gitlab.com/icc-ub/public/gaiadr3_zeropoint
"""

cols_keep = (
    'EDR3Name_1', '_x_1', '_y_1', 'RA_ICRS_1', 'DE_ICRS_1', 'Plx_1',
    'e_Plx_1', 'pmRA_1', 'e_pmRA_1', 'pmDE_1', 'e_pmDE_1', 'Gmag_1',
    'e_Gmag_1', 'BP-RP_1', 'e_BP-RP', 'V', 'eV', 'BV', 'eBV', 'UB',
    'eUB', 'VI', 'eVI', 'probs_final', 'membs_select')
cols_new = (
    'EDR3Name', '_x', '_y', 'RA_ICRS', 'DE_ICRS', 'Plx',
    'e_Plx', 'pmRA', 'e_pmRA', 'pmDE', 'e_pmDE', 'Gmag',
    'e_Gmag', 'BP-RP', 'e_BP-RP', 'V', 'eV', 'BV', 'eBV', 'UB',
    'eUB', 'VI', 'eVI', 'probs_final', 'membs_select')


def main():
    """
    """
    # Initialize table of coefficients
    zpt.load_tables()

    # Load file with the estimated true members and the Gaia EDR3 added columns
    files = readFiles()

    for file in files:
        print(file.name)
        data = Table.read(file, format='ascii')

        # The names of the column change because this is data retrieved
        # from Vizier, not from https://gaia.aip.de/query/
        # The catalog_match script changed the names of the duplicated
        # columns, hence the extra '_1' in 'Gmag'

        # phot_g_mean_mag --> Gmag
        gmag = data['Gmag_1'].data
        # nu_eff_used_in_astrometry --> nueff
        nueffused = data['nueff'].data
        # pseudocolour --> pscol
        psc = data['pscol'].data
        # ecl_lat --> ELAT
        ecl_lat = data['ELAT'].data
        # astrometric_params_solved --> Solved
        soltype = data['Solved'].data

        # 'get_zpt()' will fail if there are sources with 2-p solutions
        valid = soltype > 3
        print("Stars with soltype=3: {}".format((~valid).sum()))

        # Apply the Parallax correction. The values here are to be *subtracted*
        # from the observed parallaxes
        zpvals = zpt.get_zpt(gmag[valid], nueffused[valid], psc[valid],
                             ecl_lat[valid], soltype[valid])

        # Re-write parallax values with the corrected values
        data = data[valid]
        data['Plx_1'] = data['Plx_1'] - zpvals

        # Generate the output data with the proper columns
        data = data[cols_keep]
        for i, col in enumerate(cols_keep):
            data.rename_column(col, cols_new[i])

        # Save output file with the corrected parallax values
        out_path = Path(
            Path.cwd().parent.parent, '2_pipeline/5_plx_corr/out',
            file.name.replace('_match', ''))
        ascii.write(data, out_path, overwrite=True)

        out_path = Path(
            Path.cwd().parent.parent, '2_pipeline/5_plx_corr/tmp',
            file.name.replace('_match', '').replace('dat', 'png'))
        fig = plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.scatter(data['Gmag'], zpvals, alpha=.5)
        plt.ylabel("zpvals")
        plt.xlabel("Gmag")
        plt.subplot(122)
        plt.scatter(data['Gmag'], data['e_Plx'], alpha=.5)
        plt.ylabel("e_Plx")
        plt.xlabel("Gmag")
        fig.tight_layout()
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.clf()
        plt.close("all")


def readFiles():
    """
    Read files from the input folder
    """
    files = []

    for pp in Path(Path.cwd().parent.parent,
                   '2_pipeline/5_plx_corr/input').iterdir():
        if not pp.name.endswith(".md"):
            if pp.is_file():
                files += [pp]
            else:
                files += [arch for arch in pp.iterdir()]

    return files


if __name__ == '__main__':
    main()
