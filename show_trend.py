import pandas as pd
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

folder_names = [
    'data/w6_h4_s30001',
    'data/w7_h4_s30001',
    'data/w8_h4_s30001',
    'data/w6_h5_s30001',
    'data/w7_h5_s30001',
    'data/w8_h5_s30001',
    'data/w6_h6_s30001',
    'data/w7_h6_s30001',
    'data/w8_h6_s30001'
]

extra_move_dfs = []
rehandling_dfs = []

for name in folder_names:
    extra_move_df = pd.read_csv(name + '/extra_move.csv')[['width', 'height', 'hybrid_bay']]
    rehandling_df = pd.read_csv(name + '/rehandling.csv')[['width', 'height', 'hybrid_bay']]
    width = extra_move_df['width'][0]
    height = extra_move_df['height'][0]
    max_extra_move = (height * (height + 1) / 2) * (width - 1)
    max_rehandling = ((height - 1) * height / 2) * width
    extra_move_df['hybrid_bay'] = extra_move_df['hybrid_bay'] / max_extra_move
    rehandling_df['hybrid_bay'] = rehandling_df['hybrid_bay'] / max_rehandling
    extra_move_dfs.append(extra_move_df)
    rehandling_dfs.append(rehandling_df)

extra_move_data = pd.concat(extra_move_dfs)
rehandling_data = pd.concat(rehandling_dfs)

sns.set_style('whitegrid')

fig, ax = plt.subplots(2)

sns.boxplot(data=extra_move_data, x='width', y='hybrid_bay', hue='height', dodge=True, ax=ax[0], showfliers=False)
ax[0].set(xlabel='Width', ylabel='Extra Movements (Normalized)',
          title='Extra Movements with Different Bay Dimensions')

sns.boxplot(data=rehandling_data, x='width', y='hybrid_bay', hue='height', dodge=True, ax=ax[1], showfliers=False)
ax[1].set(xlabel='Width', ylabel='Rehandling (Normalized)',
          title='Rehandling with Different Bay Dimensions')

ax[0].legend(title='Height')
ax[1].legend(title='Height')

plt.show()
