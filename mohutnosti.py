import matplotlib.pyplot as plt
from shapely.geometry import Polygon

points = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        plt.plot(event.xdata, event.ydata, 'ro')
        if len(points) > 1:
            plt.plot([points[-2][0], points[-1][0]], [points[-2][1], points[-1][1]], 'b-')
        plt.draw()

def onkey(event):
    if event.key == 'enter' and len(points) > 2:
        # Close the polygon
        points.append(points[0])
        plt.plot([points[-2][0], points[-1][0]], [points[-2][1], points[-1][1]], 'b-')
        plt.draw()

        # Create polygon and calculate CG and area
        poly = Polygon(points)
        centroid = poly.centroid
        area = poly.area

        print(f"Centroid (CG) from origin: ({centroid.x:.2f}, {centroid.y:.2f})")
        print(f"Area of the shape: {area:.2f}")

        # Mark centroid
        plt.plot(centroid.x, centroid.y, 'go')
        plt.text(centroid.x, centroid.y, 'CG', fontsize=12, color='green')
        plt.draw()

fig, ax = plt.subplots()
ax.set_title("Click to draw shape. Press Enter to finish.")
cid = fig.canvas.mpl_connect('button_press_event', onclick)
kid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.axis('equal')
plt.grid(True)
plt.show()
