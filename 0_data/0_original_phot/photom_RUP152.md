
# Photometry process for Ruprecth152

## Matching

Observed frames were matched using the `xyshift` mode for each filter first,
and between filters after that. For each filter the largest exposure frame was
used as the reference. The results are stored in the `1_match/` folder
under the names:

- stk3111 (U)
- stk3110 (B)
- stk3116 (V)
- stk3117 (I)

The inter-filter match was produced in the same way, using the longest exposure
times for each filter. The result is stored in the `master.mch` file.


## PSF photometry

The `psfphot.cl` IRAF script was used to perform PSF photometry on 12 frames
for all filters.

- image           filter  airmass  exposure    Sky_mean  Sky_STDDEV  FWHM_(N_stars)  FWHM_(mean)  FWHM_(std)
- stk3117.fits          I    1.015     900.0     8620.11      153.26              15         3.04        0.34 
- stk3113.fits          U    1.013     200.0       20.81        5.76              43         3.39        0.45 
- stk3109.fits          B    1.033     180.0       87.25       11.02              70         3.88        0.36 
- stk3108.fits          B    1.033      10.0        4.94        3.92              51         3.66        0.54 
- stk3114.fits          V    1.013       5.0        4.48        3.81              65         2.81        0.64 
- stk3111.fits          U    1.019    1500.0      154.81       14.69              44         3.74        0.44 
- stk3118.fits          I    1.021       5.0       49.03        7.90              12         2.34        0.44 
- stk3119.fits          I    1.021      60.0      591.54       27.58              42         2.91        0.64 
- stk3116.fits          V    1.013     900.0      807.44       39.29              46         3.30        0.36 
- stk3112.fits          U    1.013      10.0        1.04        3.32              37         4.46        1.17 
- stk3110.fits          B    1.030    1200.0      567.01       33.26              61         3.65        0.33 
- stk3115.fits          V    1.013      60.0       53.49        8.52              65         3.12        0.52 

The `FWHM`, `Sky STDDEV` and `Sky Mean` values used are taken from the
`fitstats.dat` output file, shown above.


## Master cross-match

The first step is to convert the `.als` files to `.txt` files using the
`als_2_txt` script.

The `.mch` files are edited to fit the proper `DAOMASTER` format:

- Change name to `Xfilter.mch` for each filter.
- Remove header.
- Add `.txt` extension to each frame's name.
- Change the `master.mch` file to `daom.mch`, order the filters as "V,B,U,I",
  and change the names to `Xfilter` adding the `.mag` extension.

The `.als` files are stored in the `als_files/` folder, while the `.txt` and
`.mch` input files are stored in the `daom_input/` folder.


### DAOMASTER run

The `DAOMASTER` run was performed with *Translations only* (WT=2), a maximum
match radius of 20 and a minimum radius of 1. The results are stored in the
`daom_out/` folder.

The `mag_vs_err` image was created from the `.mag` output files for each filter
using the `daom_mag_check` script. There is more than one population visible
for all filters.

The `rup152_filters_dens` and `rup152_daom` images are created using the
`daom_obs_prepare` script. They show no obvious areas of smaller density, but
a portion of stars have clearly bad photometry, visible in the three diagrams.

The `.obs` file is created with the same script from the `daom.raw` file, by
adding the airmass columns to fit the format needed by the `invertfit` task.
I manually changed the '99.9999' values to 'INDEF's.


## Invertfit

We used the transformation coefficients obtained with the simple linear
regression method for all the nights. These were introduced in a `.ans`
file borrowed from the BH73 photometry.

The `daom_rup152.obs` file was processed with the `invertfit` task using the
coefficients obtained with all the nights.
