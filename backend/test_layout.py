from rectpack import newPacker
import matplotlib.pyplot as plt
import random

rectangles = [
    # Small squares
    {"width": 15, "height": 15, "quantity": 4},
    {"width": 20, "height": 20, "quantity": 3},
    
    # Thin rectangles (good for filling gaps)
    {"width": 10, "height": 80, "quantity": 2},
    {"width": 5, "height": 60, "quantity": 2},
    {"width": 25, "height": 5, "quantity": 3},
    
    # Medium rectangles
    {"width": 45, "height": 30, "quantity": 2},
    {"width": 35, "height": 25, "quantity": 2},
    {"width": 40, "height": 35, "quantity": 2},
    
    # Large rectangles
    {"width": 70, "height": 50, "quantity": 2},
    {"width": 65, "height": 45, "quantity": 1},
    {"width": 80, "height": 40, "quantity": 1},
    
    # Odd shapes
    {"width": 12, "height": 45, "quantity": 2},
    {"width": 55, "height": 18, "quantity": 2},
    {"width": 28, "height": 28, "quantity": 2},
    
    # Very small pieces
    {"width": 8, "height": 12, "quantity": 5},
    {"width": 6, "height": 8, "quantity": 6},
    
    # Wide rectangles
    {"width": 90, "height": 15, "quantity": 1},
    {"width": 75, "height": 22, "quantity": 1},
    
    # Nearly square but slightly off
    {"width": 32, "height": 30, "quantity": 2},
    {"width": 38, "height": 35, "quantity": 1},
]

print_width = 135 # Or 155
max_height = 100000  # Arbitrary large height to ensure all rectangles fit
cost_per_square_meter = 12  # Example cost per square meter


def run_layout(rectangles, print_width):
    packer = newPacker(rotation=True)

    # Add all rectangles to the packer
    for i, rect in rectangles:
        for _ in range(rect["quantity"]):
            packer.add_rect(rect["width"], rect["height"], rid = i)

    packer.add_bin(print_width, max_height)

    packer.pack()

    layout = []
    total_height = 0

    for rect in packer.rect_list():
        # rect is a tuple: (bin_index, x, y, width, height, rid)
        bin_index, x, y, w, h, rid = rect
        layout.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "rid": rid
        })
        total_height = max(total_height, y + h)

    total_area = print_width * total_height  # Area in cm²
    total_area_m2 = total_area / 10000  # Convert cm² to m² (1 m² = 10,000 cm²)
    total_cost = total_area_m2 * cost_per_square_meter

    return layout, total_height, total_area, total_area_m2, total_cost

def visualize_layout(layout, print_width, total_height, total_area, total_area_m2, total_cost):

    fig, ax = plt.subplots()
    ax.set_xlim(0, print_width)
    ax.set_ylim(0, total_height)
    ax.set_aspect('equal')
    ax.set_title('Optimized Layout')
    ax.invert_yaxis()

    colors = {}

    for rect in layout:
        x, y, w, h, rid = rect['x'], rect['y'], rect['width'], rect['height'], rect['rid']
        if rid not in colors:
            colors[rect['rid']] = (random.random(), random.random(), random.random())
        color = colors[rect['rid']]
        rect_patch = plt.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect_patch)
        ax.text(x + w / 2, y + h / 2, f"{w}x{h}", horizontalalignment='center', verticalalignment='center', fontsize = 8)

    plt.xlabel('Width (cm)')
    plt.ylabel('Height (cm)')
    plt.grid(True)
    plt.show()
    
    # Display metrics with proper units
    print(f"Print bed width: {print_width} cm")
    print(f"Total height used: {total_height:.1f} cm")
    print(f"Total area: {total_area:.1f} cm² - ({total_area_m2:.4f} m²)")
    print(f"Total cost: {total_cost:.2f} currency units")

# Run the layout algorithm
layout, total_height, total_area, total_area_m2, total_cost = run_layout(enumerate(rectangles), print_width)
visualize_layout(layout, print_width, total_height, total_area, total_area_m2, total_cost)