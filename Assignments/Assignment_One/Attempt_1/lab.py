from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch

data = [[0,0,0,0,1],
        [0,0,0,0,1],
        [0,0,44,0,1],
        [0,0,0,0,1]]

xBot=-73.557
xTop=-73.554
yBot=45.523
yTop=45.526
Blocksize = 0.003

fig = plt.figure(None, dpi=90)
ax = fig.add_subplot(111)
count = 0
while(count < 3):

        polygon = Polygon([(xBot, yBot),(xBot,yTop),(xTop,yTop),(xTop,yBot)])
        if(count == 1):
                patch = PolygonPatch(polygon, fc= 'blue')
        else:
                patch = PolygonPatch(polygon, fc= 'red')
        ax.add_patch(patch)
        yBot -= Blocksize
        yTop -= Blocksize
        count += 1


axes = plt.gca()
axes.set_xlim([-73.59,-73.55])
axes.set_ylim([45.49,45.53])

plt.show()
