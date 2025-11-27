import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from shapely.geometry import Polygon
import tkinter.filedialog as fd

points = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        if len(points) > 1:
            ax.plot([points[-2][0], points[-1][0]], [points[-2][1], points[-1][1]], 'b-')
        canvas.draw()

def onkey(event):
    # Case: button click (event is None)
    if event is None and len(points) > 2:
        finish_polygon()
    # Case: keyboard event
    elif hasattr(event, "key") and event.key == 'enter' and len(points) > 2:
        finish_polygon()

def finish_polygon():
    points.append(points[0])
    ax.plot([points[-2][0], points[-1][0]], [points[-2][1], points[-1][1]], 'b-')
    canvas.draw()

    poly = Polygon(points)
    centroid = poly.centroid
    area = poly.area

    print(f"Centroid (CG) from origin: ({centroid.x:.2f}, {centroid.y:.2f})")
    print(f"Area of the shape: {area:.2f}")

    ax.plot(centroid.x, centroid.y, 'go')
    ax.text(centroid.x, centroid.y, 'CG', fontsize=12, color='green')
    canvas.draw()




# --- Tkinter Setup ---
root = tk.Tk()
root.title("Polygon Drawer with Background Image")

# Load image
#load your own image path here using tkinter file dialog
image_path = fd.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
img = mpimg.imread(image_path)  # Replace with your image path
img_height, img_width, _ = img.shape
# Create figure and axes
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, img_width, 0, img_height])
ax.set_xlim(0, img_width)
ax.set_ylim(0, img_height)
ax.set_title("Click to draw shape. Press Enter to finish.")
ax.set_aspect('equal')
ax.grid(True)

# Embed in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)
canvas.mpl_connect('button_press_event', onclick)
canvas_widget.bind('<Return>', lambda e: onkey)
canvas_widget.focus()
#add button to finish drawing
finish_button = tk.Button(root, text="Finish Drawing (Enter)", command=lambda: onkey(None))
finish_button.pack()    
root.mainloop()
