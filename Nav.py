import tkinter as tk
import requests
import json
import webbrowser

class NavApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CarFinder")

        # Set window background color
        self.config(bg="#FFFACD")

        # Create a canvas for the background image
        canvas = tk.Canvas(self, width=500, height=500, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        menubar = tk.Menu(self)

        # Create a file menu and add it to the menubar
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Location", command=self.save_location)
        file_menu.add_command(label="Open Location", command=self.open_location)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create an about menu and add it to the menubar
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Sign Up", command=self.sign_up)
        about_menu.add_command(label="About Us", command=self.about_us)
        menubar.add_cascade(label="About", menu=about_menu)

        # Set the menubar as the window's menu
        self.config(menu=menubar)

        # Load the background image
        # Add the image to the canvas

        # Create buttons
        save_location_button = tk.Button(self, text="Save Location", command=self.save_location,  fg="#000000", font=("Arial", 16))
        open_location_button = tk.Button(self, text="Open Location", command=self.open_location ,fg="#000000", font=("Arial", 16))
        sign_up_button = tk.Button(self, text="Sign Up", command=self.sign_up,  fg="#000000", font=("Arial", 16))
        about_us_button = tk.Button(self, text="About Us", command=self.about_us,  fg="#000000", font=("Arial", 16))

        # Add buttons to the window
        save_location_button.pack(pady=0)
        open_location_button.pack(pady=0)
        sign_up_button.pack(pady=0)
        about_us_button.pack(pady=0)

    def save_location(self):
        # Get user's location using Google Maps Geolocation API
        try:
            response = requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=YOUR_API_KEY")
            response.raise_for_status()
            data = json.loads(response.text)
            latitude = data["location"]["lat"]
            longitude = data["location"]["lng"]
            print("Latitude: {}, Longitude: {}".format(latitude, longitude))

            # Reverse geocode the location using Google Maps Places API
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=YOUR_API_KEY&location={},{}&rankby=distance".format(latitude, longitude)
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            address = data["results"][0]["vicinity"]
            print("Address:", address)

            # Save location and address to file
            location = {"latitude": latitude, "longitude": longitude, "address": address}
            with open("location.json", "w") as f:
                json.dump(location, f)
            print("Location saved to file")
        except Exception as e:
            print("Error getting location:", e)

    def open_location(self):
        # Load location from file
        with open("location.json", "r") as f:
            location = json.load(f)

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Open location in Google Maps
        url = "https://www.google.com/maps/search/?api=1&query={},{}".format(latitude, longitude)
        webbrowser.open_new_tab(url)
        print("Opening location in browser")
    
    def sign_up(self):
        # Add sign up functionality here
        print("Sign up button clicked")
    
    def about_us(self):
        # Add about us functionality here
        print("About us button clicked")

if __name__ == '__main__':
    app = NavApp()
    app.mainloop()
