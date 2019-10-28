import matplotlib.pyplot as plt
import numpy as np
import pickle

methods = ['IEC', 'madsen', 'keck']
cts = [0.3, 0.6, 0.9]

protostring = 'data_jaime/{method}_ct{ct}.pkl'

if __name__ == '__main__':
    
    for method in methods:
        fig, axes = plt.subplots(3, 1, sharex=True)
        
        for i, ct in enumerate(cts):
            filename = protostring.format(method=method, ct=str(ct))
            with open(filename, 'rb') as f:
                r = pickle.load(f)
                x = pickle.load(f)
                U = pickle.load(f)
                V = pickle.load(f)
                
                
            # plot axial induction distribution
            X, Y = np.meshgrid(x, r)
            axes[i].contourf(X, Y, U.T, 30, vmin=0, vmax=1)
            axes[i].contourf(X, -Y, U.T, 30, vmin=0, vmax=1)
            axes[i].text(.5, .85, f'{method} $C_T={ct}$',
                horizontalalignment='center', transform=axes[i].transAxes)

    plt.show()
    
    
