import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

data = [[0,0,0,0,1],
        [0,0,0,0,1],
        [0,0,44,0,1],
        [0,0,0,0,1]]


print(data)
# create discrete colormap
cmap = colors.ListedColormap(['red', 'blue'])
bounds = [0,10,9999]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-73.59,-73.55,0.002 ));
ax.set_yticks(np.arange(45.490,45.530,0.002));


print(data)
plt.show()
