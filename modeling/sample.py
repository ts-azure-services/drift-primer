import pandas as pd
import numpy as np

a = pd.DataFrame(
        {'name':['Jason', 'Mark', 'Parik'],
            'age':[24, 56, 51]
            }
        )
a['allocation']= np.random.choice(
        [1,1],size=len(a), p=[0.5,0.5]
        )

print(a)
