import numpy as np
import matplotlib.pyplot as plt
from GenericActuatorDisk import GenericActuatorDisk

tsr = 7
CTs = [0.3, 0.6, 0.9]
r = np.linspace(0, 3, 501)
AD = GenericActuatorDisk(b=2, a=1.256, delta=0.2)


for ct in CTs:
    BC = np.zeros(len(r))
    BC[r<=1] = AD.ud(r[r<=1] , tsr, ct)
    out = np.stack([r, BC]).T
    np.savetxt(f'induction_ct{ct}.csv', out)
    plt.plot(r, BC, label=f'$C_T = {ct}$')
plt.legend()
plt.show()


for ct in CTs:
    np.loadtxt(f'induction_input_files/induction_ct{ct}.csv')
