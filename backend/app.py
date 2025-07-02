from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rectpack import newPacker

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allows all headers
)

class Rectangle(BaseModel):
    width: float
    height: float
    quantity: int

class LayoutRequest(BaseModel):
    rectangles: List[Rectangle]
    print_width: float = 155  # Print bed width in mm (155mm or 185mm or custom)
    price_per_square_meter: float = 0.0  # Optional, default to 0.0

@app.post("/layout")
def optimize_layout(data: LayoutRequest):
    """
    Optimizes the layout of rectangles using a bin packing algorithm.
    
    The algorithm tries to minimize the total height needed by:
    1. Allowing rectangles to rotate (if beneficial)
    2. Packing rectangles as tightly as possible
    3. Using a fixed width (print bed width) with unlimited height
    
    Returns the optimized layout with positions and total metrics.
    """
    packer = newPacker(rotation=True)

    # Add all rectangles to the packer
    for i, rect in enumerate(data.rectangles):
        for _ in range(rect.quantity):
            packer.add_rect(rect.width, rect.height, rid=i)

    # Create a bin with fixed width and very large height (strip packing)
    max_height = 100000 # Arbitrary large height to ensure all rectangles fit
    packer.add_bin(data.print_width, max_height)

    # Run the packing algorithm
    packer.pack()

    # Extract the results
    layout = []
    total_height = 0

    for rect in packer.rect_list():
        # rect is a tuple: (bin_index, x, y, width, height, rid)
        bin_index, x, y, w, h, rid = rect
        layout.append({
            "width": w,
            "height": h,
            "x": x,
            "y": y
        })
        total_height = max(total_height, y + h)
    
    # Calculate metrics with proper unit conversion
    total_area = data.print_width * total_height  # Area in mm²
    total_area_m2 = total_area / 1000000  # Convert mm² to m² (1 m² = 1,000,000 mm²)
    cost = total_area_m2 * data.price_per_square_meter
    
    return {
        "layout": layout,
        "total_height": total_height,
        "total_area": total_area,
        "total_area_m2": total_area_m2,
        "cost": cost,
        "efficiency": sum(r["width"] * r["height"] for r in layout) / total_area if total_area > 0 else 0
    }