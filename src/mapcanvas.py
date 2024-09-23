from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import pycountry
import requests
from io import BytesIO
import time
from PyQt6.QtCore import QThread, pyqtSignal

class DataFetcher(QThread):
    data_fetched = pyqtSignal(list)  # Signal to send data to the main thread

    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget

    def run(self):
        data_old = []
        while True:
            # Fetch data from table widget
            ip_locations = self.get_ip_locations_from_table()
            if ip_locations != data_old:
                data_old = ip_locations
                self.data_fetched.emit(ip_locations)
                time.sleep(1)  # Wait for 10 seconds before fetching data again
            else:
                time.sleep(1)

    def get_ip_locations_from_table(self):
        ip_locations = []
        try:
            for row in range(self.table_widget.rowCount()):
                ip = self.table_widget.item(row, 2).text()
                lat = self.table_widget.item(row, 3).text().split("|")[1].split(",")[0]
                lon = self.table_widget.item(row, 3).text().split("|")[1].split(",")[1]
                country = self.table_widget.item(row, 3).text().split("|")[0].split("-")[1].strip()
                ip_locations.append({'ip': ip, 'lat': float(lat), 'lon': float(lon), 'country': country})
            return ip_locations
        except Exception as e:
            return []

def convert_alpha_2_to_alpha_3(alpha_2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_code)
        return country.alpha_3 if country else "Unknown country code"
    except LookupError:
        return "Unknown country code"

def convert_alpha_3_to_alpha_2(alpha_3_code):
    try:
        country = pycountry.countries.get(alpha_3=alpha_3_code)
        return country.alpha_2 if country else "Unknown country code"
    except LookupError:
        return "Unknown country code"

def fetch_flag_image(alpha_2_code):
    url = f"https://flagcdn.com/w320/{alpha_2_code.lower()}.png"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        return None
class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, ip_locations=None):
        self.ip_locations = ip_locations
        print("IP Locations:", self.ip_locations)
        fig, self.ax = plt.subplots(figsize=(10, 7), tight_layout=True)  # Adjusted size for better view
        super().__init__(fig)
        self.setParent(parent)  # Set parent to ensure proper embedding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Ensure the canvas expands
        self.draw_map()
       
    def update_data(self, ip_locations):
        # xoá hết các label và flag cũ
        for artist in self.ax.artists:
            artist.remove()
        for line in self.ax.lines:
            line.remove()
        for text in self.ax.texts:
            text.remove()
        self.ip_locations = ip_locations
        self.draw_map()
        
    def draw_map(self):
        # Load world map shapefile
        world = gpd.read_file('./map/ne_110m_admin_0_countries.shp')
        if self.ip_locations == []:
            return
        
        ip_locations = [dict(ip_location, country=convert_alpha_2_to_alpha_3(ip_location['country'])) for ip_location in self.ip_locations]
        # Convert to DataFrame
        ip_df = pd.DataFrame(ip_locations)

        # Count IPs per country
        ip_counts = ip_df['country'].value_counts()

        # Merge IP counts with world map data
        world = world.merge(ip_counts, how='left', left_on='ADM0_A3', right_index=True)
        world['count'].fillna(0, inplace=True)

        # Plot the world map with IP counts
        norm = Normalize(vmin=0, vmax=ip_counts.max())
        world.plot(ax=self.ax, column='count', cmap='OrRd', linewidth=0.8, edgecolor='0.8', norm=norm, legend=False)

        # Hide x and y axis labels
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')

        # Hide the grid
        self.ax.grid(False)

        # Remove ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Remove borders and frame
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        # Add labels for IP counts and flags
        for idx, row in world.iterrows():
            if row['count'] > 0:  # Only label countries with IPs
                x, y = row.geometry.centroid.x, row.geometry.centroid.y
                self.ax.annotate(
                    f"{int(row['count'])}",
                    xy=(x, y),
                    xytext=(3, 3),  # Offset text
                    textcoords="offset points",
                    fontsize=8,
                    color='black',
                    weight='bold'
                )

                # Fetch and place flag image
                flag_image = fetch_flag_image(convert_alpha_3_to_alpha_2(row['ADM0_A3']))
                if flag_image:
                    # Convert the image to an appropriate format
                    imagebox = OffsetImage(flag_image, zoom=0.1)  # Adjust zoom for flag size
                    ab = AnnotationBbox(imagebox, (x, y),
                                        frameon=False,
                                        pad=0.1,
                                        xycoords='data',
                                        boxcoords="offset points",
                                        box_alignment=(0.5, 0.5))
                    self.ax.add_artist(ab)

        # Remove the title
        self.ax.set_title('')