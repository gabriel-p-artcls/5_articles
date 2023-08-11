

# Five clusters photometry (Sept 2019)

Photometry of the five clusters: Haffner 14, Ruprecht 41, Ruprecht 42, Ruprecht 44, Ruprecht 152.


<!-- MarkdownTOC levels="1,2" autolink="true" style="ordered" -->

1. [Photometry processing](#photometry-processing)
1. [Clean photometry](#clean-photometry)
1. [Assign \(alpha, delta\) values to the photometry](#assign-alpha-delta-values-to-the-photometry)
1. [Cross match with Gaia DR2](#cross-match-with-gaia-dr2)
1. [Compare with APASS](#compare-with-apass)
1. [Compare with Gaia DR2](#compare-with-gaia-dr2)
1. [Cross-match with Gaia EDR3](#cross-match-with-gaia-edr3)

<!-- /MarkdownTOC -->


## Photometry processing

The cluster RUP44 was already processed (Giovanni?). For the remaining four clusters, I used the `photpy` package.

> The first processing of the four clusters HAF14, RUP41, RUP42, and RUP152
(early 2018) turned out to have a systematic offset in the I filter. I
realized this after I tried fitting the fundamental parameters with `ASteCA`.
Since RUP44 does not show this issue, it must be related to my photometry
process (or to the observations of these four clusters).

The results are stored in the `0_original_phot/` folder, and the details are stored in the `photom_XXX.md` files within that folder.

The processing of standard stars was done for the RUP42 cluster, and that data used for the rest.


## Clean photometry

The script `phot_clean` was used to remove clearly bad stars outside acceptable
color ranges. Also stars with no valid photometry in all the colors and
magnitude are removed. Used the limits:

```
VV      min     max
BV     -0.5       3
VI     -0.5       4
UB       -1       2
```

For the RUP44 file I had to first replace `1000.000, 1000` values with `INDEF` values. Output:

```
rup42_final.dat
Stars in file: 24135
Rejected stars with all nan values: 4444
Rejected stars outside ranges: 836
Stars in cleaned file: 18855

rup41_final.dat
Stars in file: 25527
Rejected stars with all nan values: 6647
Rejected stars outside ranges: 2295
Stars in cleaned file: 16585

haf14_final.dat
Stars in file: 23939
Rejected stars with all nan values: 6838
Rejected stars outside ranges: 2204
Stars in cleaned file: 14897

rup44_final.txt
Stars in file: 15334
No stars with all nan values, all stars kept: 15334
Rejected stars outside ranges: 128
Stars in cleaned file: 15206

rup152_final.dat
Stars in file: 23010
Rejected stars with all nan values: 6350
Rejected stars outside ranges: 1206
Stars in cleaned file: 15454
```

All files stored in the `1_phot_clean` folder.


## Assign (alpha, delta) values to the photometry

Astrometry is added to the final photometry for each cluster using the [astrometry.net](http://nova.astrometry.net) service.

1. From the clean photometry, extract the brightest 1000 stars to feed the service, using the `astrometry` script.
2. Feed the files with the 100 stars to the service. Equatorial coordinates are stored in the `xxx_corr.fits` file, with proper cross match.
3. Take the `*_corr.fits` file along with the clean photometry and feed it to the `astrometry` package, to obtain the `(x-->ra, y-->dec)` transformations. 

This returns astrometry in the J2000 epoch. Stored the resulting files in the `2_add_coords/` folder.


## Cross match with Gaia DR2

The files with the `(ra, dec)` columns added are cross-matched with Gaia DR2 using the `catalog_match.py` package suing:

```
ra_qry          RAJ2000
de_qry          DEJ2000
max_arcsec      5
max_mag_delta   1
```

The maximum number of stars lost (no match) is 4.3% (HAF14), and the maximum median distance between matches is ~1.3 arcsec (HAF14).

The final matched files are stored in the `3_cross_match_GaiaDR2/` folder.


## Compare with APASS

The cross-matched photometry is compared with APASS using the `apass_match` package. Downloaded areas of 0.5 arcsec radius for each cluster from the
[APASS](https://www.aavso.org/download-apass-data) survey, using the APASS DR10. Data is stored in the `XXX_apass.csv` files.

The input `*_apass.csv` and the Gaia DR2 cross-matched files are fed to the script using the input:

```
#    V_min    V_max    eVmax   eBVmax
VM      7.      16.     0.1     0.2
# Tolerance in arcsec for the cross-match.
TO    5
# Outlier max tolerance  (in V mags)
OM            1.
```

Final files are stored in the `4_APASS/` folder.


## Compare with Gaia DR2

The cross-matched photometry is compared with Gaia DR2 transformation polynomials using the `gaia_transf` script. The same input files used for the APASS comparison are used here.

Input parameters for the script:

```
# Maximum V magnitude delta to discard outliers.
#    mag_delta_max
VM              1.
# Maximum uncertainties in V, UB, BV, and VI
#    eVmax   eUBmax    eBVmax   eVImax
EM      .1       .1        .1       .1
```

Final files are stored in the `5_GaiaDR2/` folder.



### Comments on the final cross-matches

All `\Delta`s are calculated as: APASS/Gaia minus our photometry. For APASS only the B, V and BV deltas can be estimated.

* HAF14

```
\Delta U  (median): 0.142 (Gaia)
\Delta B  (median): 0.060 (APASS), 0.089 (Gaia)
\Delta V  (median): 0.021 (APASS), 0.032 (Gaia)
\Delta I  (median): 0.093 (Gaia)

\Delta UB (median): 0.115 (Gaia)
\Delta BV (median): 0.058 (APASS), 0.067 (Gaia)
\Delta VI (median): -0.076 (Gaia)
```

The differences are all below 0.1 mag except for the U filter and UB color. This seems reasonable given that these are the more complicated transformations.

* RUP41

```
\Delta U  (median):  0.066 (Gaia)
\Delta B  (median):  0.055 (APASS),  0.073 (Gaia)
\Delta V  (median): -0.081 (APASS), -0.004 (Gaia)
\Delta I  (median):  0.361 (Gaia)

\Delta UB (median): -0.043 (Gaia)
\Delta BV (median):  0.124 (APASS),  0.063 (Gaia)
\Delta VI (median): -0.379 (Gaia)
```

The I filter has a very large offset. The BV colors shows a large difference (above 0.1 mag) for APASS but only half of that for Gaia.

* RUP42

```
\Delta U  (median): 0.072 (Gaia)
\Delta B  (median): 0.083 (APASS), 0.128 (Gaia)
\Delta V  (median): 0.057 (APASS), 0.098 (Gaia)
\Delta I  (median): 0.517 (Gaia)

\Delta UB (median): -0.039 (Gaia)
\Delta BV (median): 0.036 (APASS), 0.016 (Gaia)
\Delta VI (median): -0.421 (Gaia)
```

The I filter has a very large offset. The rest of the deltas are below 0.1 mag, except for the B filter versus Gaia.

* RUP44

```
\Delta U  (median): -0.086 (Gaia)
\Delta B  (median): -0.048 (APASS), -0.049 (Gaia)
\Delta V  (median): -0.046 (APASS), -0.024 (Gaia)
\Delta I  (median): -0.059 (Gaia)

\Delta UB (median): -0.042 (Gaia)
\Delta BV (median):  0.008 (APASS), -0.022 (Gaia)
\Delta VI (median):  0.029 (Gaia)
```

The differences are all below 0.1 mag. This cluster (processed by Giovanni or Edgard?) shows the best match with APASS and Gaia.

* RUP152

```
\Delta U  (median):  0.245 (Gaia)
\Delta B  (median): 0.063 (APASS), 0.119 (Gaia)
\Delta V  (median): 0.021 (APASS), 0.056 (Gaia)
\Delta I  (median): -0.003 (Gaia)

\Delta UB (median):  0.132 (Gaia)
\Delta BV (median): 0.051 (APASS), 0.044 (Gaia)
\Delta VI (median):  0.081 (Gaia)
```

The B filter versus Gaia shows a difference larger than 0.1 mag, but half of that for APASS. The UB color also shows a larger difference (caused by the large difference in the U filter).


## Cross-match with Gaia EDR3

The Gaia DR2 data is now old, so I discarded the match and re-processed the files in `2_add_coords` cross-matching with Gaia EDR3.