import pandas as pd
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

FOLDER_NAME = 'data/w6_h4_s30000'

extra_move_df = pd.read_csv(FOLDER_NAME + '/extra_move.csv')
rehandling_df = pd.read_csv(FOLDER_NAME + '/rehandling.csv')

extra_move_mean_df = extra_move_df.mean()
extra_move_max_df = extra_move_df.max()
extra_move_min_df = extra_move_df.min()
extra_move_std_df = extra_move_df.std()

rehandling_mean_df = rehandling_df.mean()
rehandling_max_df = rehandling_df.max()
rehandling_min_df = rehandling_df.min()
rehandling_std_df = rehandling_df.std()

print("Hybrid Bay Extra Movements:")
print("Mean: {0}, Max: {1}, Min: {2}, Std: {3}".format(extra_move_mean_df['hybrid_bay'],
                                                       extra_move_max_df['hybrid_bay'],
                                                       extra_move_min_df['hybrid_bay'],
                                                       extra_move_std_df['hybrid_bay']))

print("Vertical Bay Extra Movements:")
print("Mean: {0}, Max: {1}, Min: {2}, Std: {3}".format(extra_move_mean_df['vertical_bay'],
                                                       extra_move_max_df['vertical_bay'],
                                                       extra_move_min_df['vertical_bay'],
                                                       extra_move_std_df['vertical_bay']))

print("Hybrid Bay Rehandling:")
print("Mean: {0}, Max: {1}, Min: {2}, Std: {3}".format(rehandling_mean_df['hybrid_bay'],
                                                       rehandling_max_df['hybrid_bay'],
                                                       rehandling_min_df['hybrid_bay'],
                                                       rehandling_std_df['hybrid_bay']))

print("Vertical Bay Rehandling:")
print("Mean: {0}, Max: {1}, Min: {2}, Std: {3}".format(rehandling_mean_df['vertical_bay'],
                                                       rehandling_max_df['vertical_bay'],
                                                       rehandling_min_df['vertical_bay'],
                                                       rehandling_std_df['vertical_bay']))

print("Random Bay Rehandling:")
print("Mean: {0}, Max: {1}, Min: {2}, Std: {3}".format(rehandling_mean_df['random_bay'],
                                                       rehandling_max_df['random_bay'],
                                                       rehandling_min_df['random_bay'],
                                                       rehandling_std_df['random_bay']))

sns.set_style('whitegrid')
colors = sns.husl_palette(3)

fig, ax = plt.subplots(2)

data = extra_move_df['hybrid_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    ax=ax[0],
    label='HSSA',
    color=colors[1]
)
data = extra_move_df['vertical_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    ax=ax[0],
    label='VSA',
    color=colors[2]
)
ax[0].set(xlabel='Extra Movements', ylabel='Frequency', title='Extra Movements with HSSA and VSA')

data = rehandling_df['hybrid_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='HSSA',
    color=colors[1]
)
data = rehandling_df['random_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='RSA',
    color=colors[0]
)
data = rehandling_df['vertical_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='VSA',
    color=colors[2]
)
ax[1].set(xlabel='Rehandling', ylabel='Frequency', title='Rehandling with HSSA, VSA and RSA')

ax[0].legend()
ax[1].legend()

colors = sns.husl_palette(3)
fig, ax = plt.subplots(2)
data = extra_move_df['hybrid_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    ax=ax[0],
    label='HSSA',
    color=colors[0]
)
data = extra_move_df['hybrid_left_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    ax=ax[0],
    label='HSSAL',
    color=colors[1]
)
data = extra_move_df['hybrid_right_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    ax=ax[0],
    label='HSSAR',
    color=colors[2]
)
ax[0].set(xlabel='Extra Movements', ylabel='Frequency', title='Extra Movements with HSSA, HSSAL and HSSAR')

data = rehandling_df['hybrid_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='HSSA',
    color=colors[0]
)
data = rehandling_df['hybrid_left_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='HSSAL',
    color=colors[1]
)
data = rehandling_df['hybrid_right_bay']
sns.distplot(
    data,
    bins=data.max() - data.min(),
    kde_kws={'bw': 0.32},
    ax=ax[1],
    label='HSSAR',
    color=colors[2]
)
ax[1].set(xlabel='Rehandling', ylabel='Frequency', title='Rehandling with HSSA, HSSAL and HSSAR')

ax[0].legend()
ax[1].legend()
plt.show()
