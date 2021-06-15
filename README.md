
# Five clusters

Haffner 14, Ruprecht 41, Ruprecht 42, Ruprecht 44, Ruprecht 152.


<!-- MarkdownTOC levels="1,2,3" autolink="true" style="ordered" -->

1. [Previous analysis](#previous-analysis)
1. [Photometric data](#photometric-data)
1. [Structure](#structure)
1. [Membership](#membership)
    1. [Members select](#members-select)
1. [Parallax](#parallax)
1. [Extinction](#extinction)
1. [ASteCA](#asteca)

<!-- /MarkdownTOC -->



## Previous analysis

Haffner 14 was studied in [A comprehensive study of open clusters Czernik 14, Haffner 14, Haffner 17 and King 10 using multicolour photometry and Gaia DR2 astrometry, Bisht et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020MNRAS.494..607B/abstract). The parameters are estimated apparently by eye.

It is also mentioned in [UBVRI observations of stars in the fields of five open clusters with nearby carbon stars, Jorgensen & Westerlund (1988)](https://ui.adsabs.harvard.edu/abs/1988A%26AS...72..193J/abstract) on an analysis of carbon stars.

Ruprecht 41 and 152 are studied in [Characterization of 15 overlooked Ruprecht clusters with ages within 400Myr and 3Gyr, Bonatto & Bica (2010)](https://ui.adsabs.harvard.edu/abs/2010MNRAS.407.1728B/abstract). The isochrone fit is done by eye, with a fixed solar metallicity.

Ruprecht 42 was studied in [CCD Photometry of NGC 2482 and Five Previously Unobserved Open Star Clusters, Krisciunas et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015PASP..127...31K/abstract). Not sure how/if they restricted the cluster region, but the frame is ~15x15 arcmin. They used the 'cross-entropy technique' by Oliveira et al, and fixed the binary fraction to 50%.

Ruprecht 44 was recently analyzed in [CCD photometric search for peculiar stars in open clusters. VIII. King 21, NGC 3293, NGC 5999, NGC 6802, NGC 6830, Ruprecht 44, Ruprecht 115, and Ruprecht 120, Netopil et al. (2007)](https://ui.adsabs.harvard.edu/abs/2007A&A...462..591N) The frame used is 13x13 arcmin with no mention of any radius being used.

```
Name      r_cl       z    log(age)   E_BV       dm     Mass
-----------------------------------------------------------
HAFF14¹     ??      ??      8.2      0.50    11.80       ??
HAFF14²    3.7    sol³      8.5      0.38    13.80      595
RUP41      3.5     sol      8.845    0.13    12.49       ??
RUP42       ??   0.009      8.60     0.39    13.68       ??
RUP44      13?    sol?      6.80     0.58    13.40⁴      ??
RUP152     3.5     sol      8.78     0.67    14.52       ??
----
¹: 1988
²: 2020
³ : z=0.019 (Marigo 2017)
⁴: The distance modulus is listed as 15.2 but the distance as 4.79 kpc
```



## Photometric data

The photometric analysis was performed by GIP, the results are stored in the folder `0_data`. Data from UBVI is processed and merged with Gaia EDR3. Data below is from the OPENCLUST catalog (Dias et al. 2002):

```
Cluster         RA         Dec       diameter
-------------------------------------------
Haffner 14      116.2125  -28.3667   10.0
Ruprecht 41     118.4500  -26.9611   7.0
Ruprecht 42     119.4000  -25.9167   4.0
Ruprecht 44     119.7125  -28.5833   10.0
Ruprecht 152    118.6167  -38.2372   7.0
```

The final files are stored in `2_pipeline/1_data_filter/out`, after removing not used columns and adding the BP-RP uncertainty with the `1_data_filter` code.


## Structure

* Haffner 14: the field is heavily contaminated with strong stellar density variation. Fixing the cluster's center on the central coordinates of the frame, the radius estimated by ASteCA is ~9.6 arcmin. This value appears to be too  large; it is obtained due to the unclear field density estimation. A radius of ~5 arcmin seems to be more reasonable.
* Ruprecht 41: the same problems seen in Haffner 14 are also seen here. The radius estimated by ASteCA is of ~10 arcmin after fixing the cluster's center on the coordinates extracted from the proper motions.
* Ruprecht 42: the center is clear, and the radius is estimated at around ~6 arcmin. The number of members estimated by ASteCA is too large because the field density is too low.
* Ruprecht 44: heavily contaminated field. The RDP appears to indicate a radius of ~5 arcmin. Inspecting the proper motions, the distribution of stars in the coordinate space is clearly elongated and rotated.
* Ruprecht 152: the center is clear and the radius is estimated by ASteCA around ~3 arcmin.


## Membership

The number of true members and radius of each cluster are analyzed with ASteCA, and also manually using the Glue application.

```
              Glue      |     ASteCA
Name    |  Nmemb , rad  |  Nmemb , rad 
-----------------------------------------
HAF14   |   ~170 , 5    |   ~500 , 5
RUP41   |   ~150 , 10   |   ~200 , 10
RUP42   |   ~150 , 4    |   ~500 , 6
RUP44   |   ~240 , 7    |   ~200 , 5
RUP152  |   ~150 , 3    |   ~150 , 3
```



### Members select

The membership estimation was performed with pyUPMASK (GMM). The results are stored in the folder `2_pipeline/2_pyUPMASK/out`.

I used the `members_select` code with manual `Nmemb` values taken from the above table, `Glue` column. The resulting files are stored in the `3_members_select` folder.

The members are selected with the `4_members` code and the files stored in the `4_members` folder.



## Parallax

The subset of members is analyzed to estimate their parallax distances, using no offset as these parallax values are corrected with the Lindegren zero point code.

```
NAME           d_Plx
haffner14      12.97
rup41          12.89
rup42          13.60
rup44          13.27
rup152         14.12
```



## Extinction

The code `SFD_dustmap` was used to estimate the extinction in the region of each cluster.

```
Haffner 14  : median=0.812, min=0.777, max=0.840
Ruprecht 41 : median=0.397, min=0.330, max=0.485
Ruprecht 42 : median=0.252, min=0.221, max=0.311
Ruprecht 44 : median=0.668, min=0.618, max=0.702
Ruprecht 152: median=0.754, min=0.726, max=0.784
```



## ASteCA

Nine runs were performed:

1. `G vs BP-RP, b_fr=0.0`
2. `G vs BP-RP, b_fr=0.3`
3. `G vs BP-RP, b_fr=free`
4. `V vs U-B, b_fr=0.0`
5. `V vs U-B, b_fr=0.3`
6. `V vs U-B, b_fr=free`
7. `G vs U-B, b_fr=0.0`
8. `G vs U-B, b_fr=0.3`
9. `G vs U-B, b_fr=free`

The results are stored in the `final_params.dat` file.
