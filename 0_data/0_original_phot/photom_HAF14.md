
# Photometry process for Haffner14

## Matching

Observed frames were matched using the `xyshift` mode for each filter first,
and between filters after that. For each filter the largest exposure frame was
used as the reference. The results are stored in the `1_match/` folder
under the names:

- stk2124 (U)
- stk2118 (B)
- stk2121 (V)
- stk2125 (I)

The inter-filter match was produced in the same way, using the longest exposure
times for each filter. The result is stored in the `master.mch` file.


## PSF photometry

The `psfphot.cl` IRAF script was used to perform PSF photometry on 12 frames
for all filters.

- image           filter  airmass  exposure    Sky_mean  Sky_STDDEV  FWHM_(N_stars)  FWHM_(mean)  FWHM_(std)
- stk2125.fits          I    1.022     700.0     5172.60   151.48              31         2.75        0.32 
- stk2126.fits          I    1.033      30.0      244.81    18.18              81         2.57        0.38 
- stk2127.fits          I    1.034       3.0       25.15     6.05              68         2.98        0.48 
- stk2121.fits          V    1.001     900.0      842.16    49.19              55         2.70        0.30 
- stk2120.fits          V    1.000      30.0       27.94     6.57              91         2.70        0.36 
- stk2119.fits          V    1.000       5.0        4.68     3.79              92         2.66        0.38 
- stk2118.fits          B    1.001    1100.0      552.08    36.41              15         3.95        0.99 
- stk2117.fits          B    1.002      60.0       29.84     6.79              11         3.72        0.90 
- stk2116.fits          B    1.002      10.0        4.99    3.88               8         3.72        1.05 
- stk2124.fits          U    1.006    1500.0      166.74    15.23              46         2.98        0.45 
- stk2123.fits          U    1.005     150.0       15.29     5.19              51         3.09        0.31 
- stk2122.fits          U    1.004      20.0        2.05     3.44              30         3.02        0.63 

The `FWHM`, `Sky STDDEV` and `Sky Mean` values used are taken from the
`fitstats.dat` output file, shown above.


## Master cross-match

The first step is to convert the `.als` files to `.txt` files using the
`als_2_txt` script.

The `.mch` files are edited to fit the proper `DAOMASTER` format:

- Change name to `Xfilter.mch` for each filter.
- Add `.txt` extension to each frame's name.
- Change the `master.mch` file to `daom.mch`, order the filters as "V,B,U,I",
  and change the names to `Xfilter` adding the `.mag` extension.
- Remove all the headers.

The `.als` files are stored in the `als_files/` folder, while the `.txt` and
`.mch` input files are stored in the `daom_input/` folder.


### DAOMASTER run

The `DAOMASTER` run was performed with *Translations only* (WT=2), a maximum
match radius of 20 and a minimum radius of 1. The results are stored in the
`daom_out/` folder.

The `mag_vs_err` image was created from the `.mag` output files for each filter
using the `daom_mag_check` script. There is more than one population visible
for all filters.

The `haf14_filters_dens` and `haf14_daom` images are created using the
`daom_obs_prepare` script. They show no obvious areas of smaller density, but
a portion of stars have clearly bad photometry, visible in the three diagrams.

The `.obs` file is created with the same script from the `daom.raw` file, by
adding the airmass columns to fit the format needed by the `invertfit` task.
I manually changed the '99.9999' values to 'INDEF's.


## Invertfit

We used the transformation coefficients obtained with the simple linear
regression method for all the nights. These were introduced in a `.ans`
file borrowed from the BH73 photometry.

The `daom_haf14.obs` file was processed with the `invertfit` task using the
coefficients obtained with all the nights.

