
# Photometry process for Ruprecth 41

## Matching

Observed frames were matched using the `xyshift` mode for each filter first,
and between filters after that. For each filter the largest exposure frame was
used as the reference. The results are stored in the `1_match/` folder
under the names:

- stk4117 (U)
- stk4118 (B)
- stk4114 (V)
- stk4111 (I)

The inter-filter match was produced in the same way, using the longest exposure
times for each filter. The result is stored in the `master.mch` file.


## PSF photometry

The `psfphot.cl` IRAF script was used to perform PSF photometry on 12 frames
for all filters.

- image           filter  airmass  exposure    Sky_mean  Sky_STDDEV  FWHM_(N_stars)  FWHM_(mean)  FWHM_(std)
- stk4117.fits          U    1.001    1500.0      138.87       13.60              36         3.46        0.49 
- stk4116.fits          U    1.001     120.0       11.17        4.73              42         3.58        0.74 
- stk4115.fits          U    1.001      10.0        0.96        3.27              23         3.64        0.57  
- stk4118.fits          B    1.008    1200.0      616.36       34.32              40         3.72        0.35 
- stk4119.fits          B    1.022     120.0       77.31       10.24              37         3.86        0.52 
- stk4120.fits          B    1.024      10.0        7.01        4.16              30         3.14        0.78 
- stk4114.fits          V    1.002     900.0      817.00       41.46              37         3.00        0.33 
- stk4113.fits          V    1.002      60.0       54.82        8.78              40         3.03        0.49 
- stk4112.fits          V    1.003       5.0        4.58        3.79              31         2.80        0.49 
- stk4111.fits          I    1.008     900.0     3684.14      141.49              24         2.92        0.46  
- stk4110.fits          I    1.009      60.0      242.24       19.33              53         2.72        0.46 
- stk4109.fits          I    1.009       5.0       20.30        5.72              66         3.04        0.50 

The `FWHM`, `Sky STDDEV` and `Sky Mean` values used are taken from the
`fitstats.dat` output file, shown above.

### V filter 2nd processing

Since the V filter showed an offset of ~0,14 with APASS, and repeating the
`invertfit` process using transformation coefficients from `night4` did not
help, I repeated the PSF photometry on this filter. The aperture values
for all exposures are rather different than what I obtained in the first
run.


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

The `rup41_filters_dens` and `rup41_daom` images are created using the
`daom_obs_prepare` script. They show no obvious areas of smaller density, but
a portion of stars have clearly bad photometry, visible in the three diagrams.

The `.obs` file is created with the same script from the `daom.raw` file, by
adding the airmass columns to fit the format needed by the `invertfit` task.
I manually changed the '99.9999' values to 'INDEF's.


## Invertfit

We used the transformation coefficients obtained with the simple linear
regression method for all the nights. These were introduced in a `.ans`
file borrowed from the BH73 photometry.

The `daom_rup41.obs` file was processed with the `invertfit` task using the
coefficients obtained with all the nights.

The final photometry shows an offset of ~0.14 in the V filter compared to APASS.
I performed a new `invertfit` using only the standards from `night4`, results
stored in the `night4/` folder. The results only improved marginally.
The new photometry shows an offset in the U filter of ~0.047.

I tried re-doing the PSF for the V filter from scratch, and this resulted in
a much better match with APASS data.
