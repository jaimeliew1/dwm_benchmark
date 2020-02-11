import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from jDWM.Wake import StaticWake

wsp = 10
TIs = [0.0001, 0.05, 0.1, 0.15, 0.2]


def plot_wake_profiles(R, a, ax, label, TI=0):
    dwm = StaticWake(axial_induction_model='UserInput',
                     meandercompensator='Reinwardt',
                     TI=TI,
                     U=10,
                     D_rot=100)
    r, x, U, V, widths = dwm.solve(axial_r=R, axial_a=a)

    meander_std = dwm.meandercompensator.meander_std(x)
    plot_wake(ax, r, x, U, V, widths, label, meander_std)
    print(
        f'TI:{TI} meander std (10R): {dwm.meandercompensator.meander_std(10):2.3f}'
    )


def plot_wake(ax, r, x, U, V, widths, label, meander_std):
    ax.set_ylim(-max(r), max(r))
    ax.imshow(U.T,
              extent=[min(x), max(x), min(r), max(r)],
              origin='lower',
              interpolation='bilinear',
              vmin=0,
              vmax=1,
              aspect=0.6)
    ax.imshow(U.T,
              extent=[min(x), max(x), min(r), -max(r)],
              origin='lower',
              interpolation='bilinear',
              vmin=0,
              vmax=1,
              aspect=0.6)

    ax.plot(x, widths, 'r--', lw=0.5)
    ax.plot(x, -widths, 'r--', lw=0.5)
    ax.grid()
    ax.set_yticks([-2, -1, 0, 1, 2])

    ax.text(0.5,
            0.98,
            label,
            horizontalalignment='center',
            verticalalignment='top',
            transform=ax.transAxes)

    ax.plot(x, meander_std, '--k', lw=0.5)
    ax.plot(x, -meander_std, '--k', lw=0.5)


if __name__ == '__main__':

    data = np.loadtxt('induction_input_files/induction_ct0.6.csv')
    r, a = data[:, 0], data[:, 1]

    fig, axes = plt.subplots(len(TIs),
                             1,
                             sharex=True,
                             sharey=True,
                             figsize=[4, 8])
    axes = axes.ravel()
    for TI, ax in zip(TIs, axes):
        plot_wake_profiles(r, a, ax, label=f'TI={TI}', TI=TI)

    # Shared axes labels
    fig.text(0.5, 0.05, 'Downstream distance $[x/R]$', ha='center')
    fig.text(0.04,
             0.5,
             'Crosswind distance $[r/R$]',
             va='center',
             rotation='vertical')

    # Colorbar
    fig.subplots_adjust(right=0.89)
    cbar_ax = fig.add_axes([0.91, 0.11, 0.03, 0.77])
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
                               norm=plt.Normalize(vmin=0, vmax=1))
    sm._A = []
    cb = fig.colorbar(sm, cax=cbar_ax, label='Windspeed $[U/U_\infty]$')

    # Save
    plt.savefig(f'meandercomp_comparison', dpi=300, bbox_inches='tight')
    plt.show()
