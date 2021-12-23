from collections import defaultdict
import pandas as pd

cr = defaultdict(list)
cr['Customer'].append('Bob')
cr['Customer'].append('Mariance')
cr['Customer'].append('Jason')
cr['Age'].append(40)
cr['Age'].append(43)
cr['Age'].append(46)

df = pd.DataFrame(cr)
print(df)
