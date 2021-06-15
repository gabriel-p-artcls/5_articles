
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt

"""
Sanity check on the nine ASteCA output for the 5 clusters with different
analyzed CMDs and binary fractions
"""

in_folder = '../2_pipeline/8_ASteCA/'
out_folder = '../2_pipeline/8_ASteCA/tmp/'

data = ascii.read(in_folder + 'final_params.dat')
data.sort('NAME')

labels = list(set([_.split('_')[0] for _ in data['NAME']]))
x = np.arange(len(labels))

xx = {'haf14': 1, 'rup41': 2, 'rup42': 3, 'rup44': 4, 'rup152': 5}
cc = {1: u'#1f77b4', 2: u'#ff7f0e', 3: u'#2ca02c', 4: u'#d62728',
      5: u'#9467bd', 6: u'#8c564b', 7: u'#e377c2', 8: u'#7f7f7f',
      9: u'#bcbd22', 10: u'#17becf'}
# z_sol = 0.0152


def parPlot(data, par):
    for cl in data:
        name, run = cl['NAME'].split('_')
        x = xx[name]
        xoffset = (int(run) - 5) / 12.
        x, y = x + xoffset, cl['{}_median'.format(par)]
        yerr = np.array([[
            y - cl['{}_16th'.format(par)], cl['{}_84th'.format(par)] - y]]).T
        # y, yerr = np.log(y / z_sol), np.log(yerr / z_sol)
        ax.errorbar(x, y, yerr=yerr, fmt='o', lw=2, color=cc[int(run)])

        # ax.scatter(x, cl['{}_mean'.format(par)], marker='x', c='k', lw=.7)
        y, yerr = cl['{}_mean'.format(par)], cl['{}_std'.format(par)]
        ax.errorbar(x - 0.025, y, yerr=yerr, fmt='x', c='k', lw=.7, ls=':')
        # if int(run) in (1, 4, 7):
        #     txt = '0'
        # elif int(run) in (2, 5, 8):
        #     txt = '0.3'
        # elif int(run) in (3, 6, 9):
        #     txt = 'f'
        ax.annotate(int(run), (x + .02, y))


ylabels = {'z': 'z', 'a': 'log(age)', 'E': r'$E_{B-V}$)', 'd': r'$\mu$',
           'M': r'M (M$_{\odot}$)', 'b': r'b$_{fr}$'}
for par in ('z', 'a', 'E', 'd', 'M', 'b'):
    print(par)
    fig, ax = plt.subplots(figsize=(20, 10))
    parPlot(data, par)
    # ax.grid(ls=':')
    ax.set_xticks(np.arange(len(xx)) + 1)
    ax.set_xticklabels((_.upper() for _ in xx.keys()))
    # ax.set_yscale('log')
    ax.axvline(1.5, ls=':', lw=.5)
    ax.axvline(2.5, ls=':', lw=.5)
    ax.axvline(3.5, ls=':', lw=.5)
    ax.axvline(4.5, ls=':', lw=.5)
    plt.ylabel(ylabels[par], fontsize=12)
    plt.savefig(
        out_folder + "{}.png".format(par), dpi=150, bbox_inches='tight')
