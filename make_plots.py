import matplotlib.pyplot as plt
import numpy as np
import pickle

methods = ['IEC', 'madsen', 'keck']
cts = [0.3, 0.6, 0.9]


def load_jaime(method, ct):
    protostring = 'data_jaime/{method}_ct{ct}.pkl'
    filename = protostring.format(method=method, ct=str(ct))
    with open(filename, 'rb') as f:
        r = pickle.load(f)
        x = pickle.load(f)
        U = pickle.load(f)
        V = pickle.load(f)
    
    return r, x, U, V


def load_inga(_method, ct):
    methods = {
        'IEC'   : 'ID_IEC_EV_IEC',
        'madsen': 'ID_LarsenCorrected_EV_Egmond',
        'keck'  : 'ID_Keck_EV_Keck',
              }
    protostring = 'data_inga/induction_ct{ct}_results_{method}.csv'
    filename = protostring.format(method=methods[_method], ct=str(ct))
    r = np.linspace(-3, 3, 999)
    x = np.linspace(0, 10, 102)
    U = np.loadtxt(filename).T
    return r, x, U, None
    
    
if __name__ == '__main__':
    
    for method in methods:
        fig, axes = plt.subplots(3, 2, sharex=True, sharey=True)
        
        axes[0, 0].set_title('Jaime')
        axes[0, 1].set_title('Inga')
        axes[2, 0].set_xlabel('$x/R$')
        axes[2, 1].set_xlabel('$x/R$')
        for i, ct in enumerate(cts):
            r, x, U, V = load_jaime(method, ct)
            axes[i, 0].imshow(U.T, extent=[min(x), max(x), min(r), max(r)], origin='lower', interpolation='bilinear', vmin=0, vmax=1)
            axes[i, 0].imshow(U.T, extent=[min(x), max(x), min(r), -max(r)], origin='lower', interpolation='bilinear', vmin=0, vmax=1)
            axes[i, 0].text(.5, .85, f'{method} $C_T={ct}$',
                horizontalalignment='center', transform=axes[i, 0].transAxes)
                
                
            r, x, U, V = load_inga(method, ct)
            axes[i, 1].imshow(U.T, extent=[min(x), max(x), min(r), max(r)], origin='lower', interpolation='bilinear', vmin=0, vmax=1)
            axes[i, 1].text(.5, .85, f'{method} $C_T={ct}$',
                horizontalalignment='center', transform=axes[i, 1].transAxes)
                
            axes[i, 0].set_ylabel('$r/R$')
                
        plt.savefig(f'fig/side_by_side_{method}.png', dpi=200, bbox_inches='tight')
            

    
    for method in methods:
        fig, axes = plt.subplots(3, 1, figsize=[4, 8], sharex=True)
                

        axes[2].set_xlabel('$x/R$')
        axes[2].set_xlabel('$x/R$')
        for i, ct in enumerate(cts):
            axes[i].set_ylim(-3, 3)
            r1, x1, U1, V1 = load_jaime(method, ct)
            r2, x2, U2, V2 = load_inga(method, ct)
            difference = (U1 - U2[:-1, 498:]).T
            error = np.sqrt((difference**2).mean())
            axes[i].imshow(difference, extent=[0, 10, 0, 3], origin='lower', interpolation='bilinear', cmap='RdBu', vmin=-0.6, vmax=0.6)
            axes[i].imshow(difference, extent=[0, 10, 0, -3], origin='lower', interpolation='bilinear', cmap='RdBu', vmin=-0.6, vmax=0.6)
            axes[i].text(.5, .8, f'{method} $C_T={ct}$\n$\epsilon={error:2.4f}$',
                horizontalalignment='center', transform=axes[i].transAxes)
            axes[i].set_ylabel('$r/R$')


                
        plt.savefig(f'fig/difference_{method}.png', dpi=200, bbox_inches='tight')
    plt.show()
    
    
