import numpy as np
import matplotlib.pyplot as plt
import pickle
from jDWM import DWM

input_files = {
    0.3: 'induction_input_files/induction_ct0.3.csv',
    0.6: 'induction_input_files/induction_ct0.6.csv',
    0.9: 'induction_input_files/induction_ct0.9.csv',
}

methods = {
    'IEC'   : 'IEC',
    'madsen': 'larsen',
    'keck'  : 'keck',
}

if __name__ == '__main__':
    for boundary_method, visc_method in methods.items():
        dwm = DWM(axial_induction_model='userinput', viscosity_method=visc_method, boundary_method=boundary_method)
        
        for i, (ct, fn) in enumerate(input_files.items()):
            # Load boundary condition data.
            data = np.loadtxt(fn)
            _r, a = data[:, 0], data[:, 1]
            
            # run DWM flow solver.
            r, x, U, V, widths = dwm.solve(TI=0.1, axial_r=_r, axial_a=a, ct=ct)
            
            # save DWM output to pickle file.
            with open(f'data_jaime/{boundary_method}_ct{ct}.pkl', 'wb') as f:
                pickle.dump(r, f)
                pickle.dump(x, f)
                pickle.dump(U, f)
                pickle.dump(V, f)
                
                
