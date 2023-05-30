import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import csv
import logging
import logging.handlers

class ImageDownloader:
    def __init__(self, master):
        self.master = master
        master.title("Image Downloader")
        self.file_path = ""
        self.download_path = ""

        # Create a frame with a 100-pixel margin
        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack()

        # Create a label for the CSV file input
        self.csv_label = tk.Label(self.frame, text="CSV File Path:")
        self.csv_label.pack()

        # Create a frame to hold the CSV file input field and browse button
        self.csv_frame = tk.Frame(self.frame)
        self.csv_frame.pack()

        # Create an entry box for the CSV file input
        self.csv_entry = tk.Entry(self.csv_frame, width=50)
        self.csv_entry.pack(side=tk.LEFT)

        # Create a button to select the CSV file
        self.csv_button = tk.Button(self.csv_frame, text="Browse...", command=self.browse_csv)
        self.csv_button.pack(side=tk.LEFT)

        # Create a label for the download path input
        self.path_label = tk.Label(self.frame, text="Download Path:")
        self.path_label.pack()

        # Create a frame to hold the download path input field and browse button
        self.path_frame = tk.Frame(self.frame)
        self.path_frame.pack()

        # Create an entry box for the download path input
        self.path_entry = tk.Entry(self.path_frame, width=50)
        self.path_entry.pack(side=tk.LEFT)

        # Create a button to select the download path
        self.path_button = tk.Button(self.path_frame, text="Browse...", command=self.browse_path)
        self.path_button.pack(side=tk.LEFT)

        # Create a run button
        self.run_button = tk.Button(self.frame, text="Run", command=self.download_images, height=2, width=20)
        self.run_button.pack(pady=10)

    def browse_csv(self):
        # Show a file dialog to select the CSV file
        self.file_path = filedialog.askopenfilename()
        self.csv_entry.delete(0, tk.END)
        self.csv_entry.insert(0, self.file_path)

    def browse_path(self):
        # Show a file dialog to select the download path
        self.download_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.download_path)

    # Initialize the logger
        self.logger = logging.getLogger('error_logger')
        self.logger.setLevel(logging.ERROR)
        # Create a file handler
        handler = logging.FileHandler('error.log')
        # Set the logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # Add the file handler to the logger
        self.logger.addHandler(handler)

    def download_images(self):
        # Check if the file path and download path are specified
        if not self.file_path or not self.download_path:
            messagebox.showerror("Error", "Please specify a CSV file path and a download path.")
            return

        # Open the CSV file
        with open(self.file_path) as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            next(reader)
            # Loop through the rows in the CSV file
            for row in reader:
                # Get the name and URL from the current row
                name, url = row 
                # Download the image data
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception if there was an error downloading the image
                except requests.exceptions.RequestException as e:
                    # Log the error to the file
                    self.logger.error(f"Error downloading image {name}: {e}")
                    continue
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception if there was an error downloading the image
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error downloading image {name}: {e}")
                    continue
                image_data = response.content
                # Convert the image data to base64
                b64_data = base64.b64encode(image_data).decode('utf-8')
                # Decode the base64 data and save it as a JPEG file with the name from the CSV
                try:
                    im = Image.open(BytesIO(base64.b64decode(b64_data)))
                    # Convert the image to RGB mode
                    im = im.convert('RGB')
                    im.save(self.download_path + "/" + name + ".jpg", "JPEG")
                except UnidentifiedImageError as e:
                    # Handle error where image file type could not be identified
                    logging.error(f"Error decoding image {name}: {e}")
                    continue
                except Exception as e:
                    # Handle other exceptions
                    logging.error(f"Error saving image {name}: {e}")
                    continue
                
                # Check if the image has a low resolution
                if im.size[0] < 300 or im.size[1] < 300:
                    logging.warning(f"Low resolution image {name}: {im.size[0]}x{im.size[1]}")
                
                # Check if the image is in grayscale
                if im.mode == "L":
                    logging.warning(f"Grayscale image {name}")
                    
                # Check if the image is too dark
                if sum(im.convert("L").getextrema()) < 255:
                    logging.warning(f"Dark image {name}")
                    
        messagebox.showinfo("Success", "Images downloaded successfully.")
    
root = tk.Tk()
app = ImageDownloader(root)
# Set the window size and position
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set a minimum window size
root.minsize(window_width, window_height)

# Set the window background color
root.configure(bg="#F0F0F0")

root.mainloop()
