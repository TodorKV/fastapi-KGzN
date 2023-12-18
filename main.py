from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
import base64
import pandas as pd

app = FastAPI()

# Your existing code for Cartesian coordinates and random data generation
# ...

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """

@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    # Read CSV file and extract data
    # df = pd.read_csv(file.file)
    # coordinates = list(zip(df['X'], df['Y'], df['Z']))
    coordinates = [(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)) for _ in range(500)]

    # Assign colors randomly (blue or red)
    colors = ['blue' if random.random() < 0.5 else 'red' for _ in range(len(coordinates))]

    # Extract x, y, and z coordinates for plotting
    x_values, y_values, z_values = zip(*coordinates)

    # Create a 3D scatter plot with different colors
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_values, y_values, z_values, c=colors, marker='o')

    # Set labels for each axis
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convert the image to base64 for embedding in HTML
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return HTMLResponse(content=f"<h1>Visualization Result</h1><img src='data:image/png;base64,{encoded_image}' alt='3D Scatter Plot'>", status_code=200)
