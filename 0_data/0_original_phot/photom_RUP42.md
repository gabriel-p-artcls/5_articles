
# Photometry process for RUP42

## Matching

The standard frames for the four nights were matched using the `match` script
in `manual` mode. This meant processing 14 files for `noche1`,  21 for
`noche2`, 19 for `noche3`, and 23 for `noche4`.

The results for all the Landolt field cross-matches were stored in the `.mch`
files in the `1_match/` folder, under the names of the respective field.

Observed frames were matched using the `xyshift` mode for each filter first,
and between filters after that. For each filter the largest exposure frame was
used as the reference. The results are stored in the `1_match/` folder
under the names:

- stk0085 (U)
- stk1108 (B)
- stk3103 (V)
- stk1115 (I)

The inter-filter match was produced in the same way, using the longest exposure
times for each filter. The result is stored in the `master.mch` file.

I also processed the standard frames of `night1` separately to see if that
would produce better transformation coefficients later on. The `.mch` files
`SA98_1`, `SA95_1`, `TPHE_1` are stored in the `night1` subfolder.


## Aperture photometry for standards

### All nights

I  used all the standard files for all the nights:

- TPHE
 - U filter: night1 (1), night2 (2), night3 (1), night4 (1) : 35 stars
 - B filter: night1 (1), night2 (2), night3 (1), night4 (1) : 35 stars
 - V filter: night1 (1), night2 (2), night3 (1), night4 (1) : 35 stars
 - I filter: night1 (1), night2 (2), night3 (1), night4 (1) : 35 stars

- PG0231
 - U filter: night1 (0), night2 (0), night3 (0), night4 (1) : 6  stars
 - B filter: night1 (0), night2 (1), night3 (0), night4 (1) : 12 stars
 - V filter: night1 (0), night2 (0), night3 (0), night4 (1) : 6  stars
 - I filter: night1 (0), night2 (0), night3 (0), night4 (1) : 6  stars

- SA95
 - U filter: night1 (1), night2 (2), night3 (3), night4 (1) : 60 stars
 - B filter: night1 (2), night2 (2), night3 (3), night4 (1) : 67 stars
 - V filter: night1 (3), night2 (2), night3 (3), night4 (1) : 75 stars
 - I filter: night1 (1), night2 (2), night3 (2), night4 (1) : 50 stars

- SA96
 - U filter: night1 (0), night2 (0), night3 (1), night4 (0) : 1 stars
 - B filter: night1 (0), night2 (0), night3 (1), night4 (0) : 1 stars
 - V filter: night1 (0), night2 (0), night3 (1), night4 (0) : 1 stars
 - I filter: night1 (0), night2 (0), night3 (1), night4 (0) : 1 stars

- SA97
 - U filter: night1 (0), night2 (0), night3 (0), night4 (2) : 8 stars
 - B filter: night1 (0), night2 (0), night3 (0), night4 (2) : 8 stars
 - V filter: night1 (0), night2 (0), night3 (0), night4 (2) : 8 stars
 - I filter: night1 (0), night2 (0), night3 (0), night4 (2) : 8 stars

- SA98
 - U filter: night1 (1), night2 (1), night3 (0), night4 (1) : 97 stars
 - B filter: night1 (1), night2 (1), night3 (0), night4 (1) : 97 stars
 - V filter: night1 (1), night2 (1), night3 (0), night4 (1) : 96 stars
 - I filter: night1 (1), night2 (1), night3 (0), night4 (1) : 97 stars

The number of stars processed per filter is:

- Filter I: 197
- Filter B: 220
- Filter U: 207
- Filter V: 221

for a **final total of 845 stars**.

The `.mch` files for all the standard frames were processed with the
`aperphot_standards` script, using an **aperture of 15 px**. The final file
`4nights.apert` is stored in the `2_apert_phot/` folder.

### Separate nights

I employed the matches for `night1` exclusively to generate the `night1.apert`
file, using the same aperture values as above.


## Extinction coefficients

The `K` coefficients were obtained using the same aperture photometry file
obtained above `4nights.apert`. The script `ext_coeff.py` was used to obtain
these values for each filter following the steps:

1. The script identifies stars that were observed in different frames, and
   extracts their ID, airmass, and instrumental magnitude.
2. For each star, a `K` coefficient is found employing an outlier rejection
   algorithm.
3. The median value of these `K` coefficients is stored, for different outlier
   rejection values, and for each filter.
4. The final `K` for each filter is obtained through the median of the `K`
   values for each outlier rejection limit.
5. The results were plotted in the image `ext_coeffs.png`.

These steps were also performed without outlier rejection, which produced a
slightly different set of values. These are:

**K coefficients, w/ outliers removal**: U .326, B .170, V .108, I .052
**K coefficients, w/o outliers removal**: U .389, B .185, V .137, I .064

Output images stored in `3_ext_coeffs/` folder.


## Standard transformation coefficients fit

Using the `4nights.apert` field and the `K` coefficients obtained *with* outlier removal, the standard transformation equation were fitted using three different methods:

- [Linear least-squares regression](https://en.wikipedia.org/wiki/Simple_linear_regression)
- [RANSAC](https://en.wikipedia.org/wiki/Random_sample_consensus)
- [Thiel-Sen](https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator)

Results are stored in the `4_fit_standards/` folder.

Using only the results from `night1`, I obtained the coefficients shown in
`night1.fit`.


## PSF photometry

The `psfphot.cl` IRAF script was used to perform PSF photometry on 14 frames
for all filters.

-  image           filter  airmass  exposure    Sky_mean  Sky_STDDEV  FWHM_(N_stars)  FWHM_(mean)  FWHM_(std)
- stk1105.fits          B    1.002      10.0        6.11        4.05              65         2.55        0.37 
- stk1106.fits          B    1.002      10.0        6.19        4.06              71         2.62        0.38 
- stk1107.fits          B    1.002      90.0       55.36        8.67              73         2.99        0.40 
- stk1108.fits          B    1.002    1200.0      764.75       37.19              50         2.78        0.32 
- stk1109.fits          U    1.006      20.0        2.57        3.56              48         2.95        0.50 
- stk1110.fits          U    1.006     200.0       25.98        6.21               3         4.49        0.08 
- stk0085.fits          U    1.003    1800.0      279.36       18.87              60         3.96        0.69 
- stk1111.fits          V    1.007       5.0        5.46        3.91              88         2.49        0.33 
- stk1112.fits          V    1.008      60.0       65.48        9.37              88         2.62        0.34 
- stk3103.fits          V    1.057     900.0      889.04       45.19              52         3.30        0.36 
- stk3102.fits          V    1.060      90.0       89.71       11.26              46         3.32        0.61 
- stk1114.fits          I    1.009      60.0      487.69       24.96              42         2.98        0.33 
- stk1115.fits          I     1.01     900.0     7465.08      141.72              29         2.65        0.22 
- stk1113.fits          I    1.009       3.0       23.88        5.92              53         2.66        0.23 

The `FWHM`, `Sky STDDEV` and `Sky Mean` values used are taken from the
`fitstats.dat` output file, shown above.


## Master cross-match

The first step is to convert the `.als` files to `.txt` files to feed
`DAOMASTER` extracting the fields:
"ID, XC, YC, MAG, MERR, CHI, SHARPNESS, CHI, SHARPNESS" (CHI & SHARPNESS are
repeated to give the files the proper format with these columns at the end).
This is done using the `als_2_txt` script.

The `.mch` files are edited to fit the proper `DAOMASTER` format:

- Change name to `Xfilter.mch` for each filter.
- Move reference frame to the top of that file.
- Add `.txt` extension to each frame's name.
- Change the `master.mch` file to `daom.mch`, order the filters as "V,B,U,I",
  add `.mag` extension to longest exposure frame's names.

The `.als` files are stored in the `als_files/` folder, while the `.txt` and
`.mch` input files are stored in the `daom_input/` folder.

### DAOMASTER run

The `DAOMASTER` run was performed with *Translations only* (WT=2), a maximum
match radius of 20 and a minimum radius of 1. The results are stored in the
`daom_out/` folder.

The `mag_vs_err` image was created from the `.mag` output files for each filter
using the `daom_mag_check` script. There is more than one population visible
for all filters.

The `rup42_filters_dens` and `rup42_daom` images are created using the
`daom_obs_prepare` script. They show no obvious areas of smaller density, but
a portion of stars have clearly bad photometry, visible in the three diagrams.

The `.obs` file is created with the same script from the `daom.raw` file, by
adding the airmass columns to fit the format needed by the `invertfit` task.


## Invertfit

We used the transformation coefficients obtained with the simple linear
regression method. These were introduced in a `.ans` file borrowed from the
BH73 photometry, leaving the errors as they were in the original file.
Increasing the errors in the fitted parameters by two full orders of magnitude
for all filters resulted in the *exact same* final photometry file. This
proves that the `invertfit` task **does not use the transformation
coefficients uncertainties when producing the final photometry**.

The `daom_rup42.obs` file was processed with the `invertfit` task using the
coefficients obtained with all the nights and those obtained from `night1` only. This produces two final photometry files.
