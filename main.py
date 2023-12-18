from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
import base64
import pandas as pd
import googlemaps

app = FastAPI()

def get_cartesian(lat=None,lon=None):
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    return x,y,z


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
    api_key = 'AIzaSyBvZkQAzJVubqPixqNV02yYqw0O4TOmTq8'
    gmaps = googlemaps.Client(key=api_key)

    # Read CSV file and extract data
    df = pd.read_csv(file.file)

    lat_lng_list = []
    colors = []

    for _, row in df.iterrows():
        result = gmaps.geocode(row['Address'])
        if result:
            location = result[0]['geometry']['location']
            lat_lng_list.append((location['lat'], location['lng']))
            colors.append('red' if row['Category'] == 1 else 'blue')

    # Create an array of Cartesian coordinates
    cartesian_array = np.array([get_cartesian(lat, lon) for lat, lon in lat_lng_list])

    # Create a 2D scatter plot with different colors based on the "Category" column
    plt.scatter(cartesian_array[:, 0], cartesian_array[:, 1], c=colors)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D Декартови координати')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convert the image to base64 for embedding in HTML
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return HTMLResponse(content=f"<h1>Резултат</h1><img src='data:image/png;base64,{encoded_image}' alt='2D Scatter Plot'>", status_code=200)