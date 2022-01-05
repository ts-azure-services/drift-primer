import pandas as pd
import numpy as np

a = pd.DataFrame(
        {'name':['Jason', 'Mark', 'Parik'],
            'age':[24, 56, 51],
            'score':[1,2,3]
            }
        )
#a['allocation']= np.random.choice(
#        [1,1],size=len(a), p=[0.5,0.5]
#        )

#print(np.random.choice([1,1],size=len(a), p=[0.5,0.5]))
a.loc[a.index,'score'] += 1
#a.loc
print(a)
