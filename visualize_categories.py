#%%
import matplotlib.pyplot as plt
import pandas as pd

from mongo_driver import *

#%%

print(list(data()))
exit()
#%%
df = pd.DataFrame(list(data()))
# df
#%% 
plt.hist
#%%  
df_sub = df.loc[:, ['_id', 'count']]
tags = df_sub['_id'].unique().tolist()

tally = df_sub.groupby(by='_id').sum().sort_values(by='count', ascending=False)
#%%
df_new = pd.DataFrame({'category': tally.index.tolist(), 'count': tally['count'].tolist()})
df_new.plot.barh(x='category', y='count')
