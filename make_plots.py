import matplotlib.pyplot as plt
import numpy as np
import pickle

def rotor_area_mean(r, x):
    '''
    Returns the rotor area mean of the quantity, x(r). The rotor mean is defined as
    the area-weighted average of a quantity x(r), which is a function of radial position.
    For example, rotor mean wind speed, or rotor mean induction.

    The rotor_area_mean ignores x(r) such that r > 1
    Args:
        r (1D array): radial positions (nondimensional)
        x (1D array): Quantity to be averaged.
    Returns:
        rotor_area_mean (float): Rotor area mean of x(r).
    '''

    assert len(r) == len(x)

    r, x = r[r<=1], x[r<=1]
    rotor_area_mean = 2*np.trapz(r*x, r)
    
    return rotor_area_mean
    
    
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
    ### Plot flow fields
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
            

    ### Plot flow field difference plots
    for method in methods:
        fig, axes = plt.subplots(3, 1, figsize=[4, 8], sharex=True)
                

        axes[2].set_xlabel('$x/R$')
        axes[2].set_xlabel('$x/R$')
        for i, ct in enumerate(cts):
            print(f'making plot for {method}, ct={ct}...')
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
        
        
        ### plot rotor effective wind speed ratio
        fig, axes = plt.subplots(3, 1, figsize=[4, 8], sharex=True)
        axes[2].set_xlabel('$x/R$')
        for j, method in enumerate(methods):
            
            axes[j].set_xlim(0, 10)
            axes[j].set_ylim(-5, 5)
            axes[j].text(.5, .9, f'{method}',
                horizontalalignment='center', transform=axes[j].transAxes)
            for i, ct in enumerate(cts):
                print(f'making plot for {method}, ct={ct}...')

                r1, x1, U1, V1 = load_jaime(method, ct)
                r2, x2, U2, V2 = load_inga(method, ct)
                
                REWS1 = np.array([rotor_area_mean(r1, U1[i, :]) for i in range(len(x1))])
                REWS2 = np.array([rotor_area_mean(r2[r2>=0], U2[i, r2>=0]) for i in range(len(x2))])
                ratio = (REWS2[:-1]-REWS1)/REWS1*100

                axes[j].plot(x1, ratio, label=f'$C_T={ct}$')
                axes[j].set_ylabel('REWS difference [%]')
                axes[j].grid()
    
        axes[2].legend(ncol=3, fontsize = 'x-small', loc='lower center')
        plt.savefig(f'fig/REWS.png', dpi=200, bbox_inches='tight')
    #plt.show()
    
    
