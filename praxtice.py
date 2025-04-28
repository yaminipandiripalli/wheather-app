import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import requests

# Weather icon mapping
icon_map = {
    "01d": "sun.png",
    "02d": "cloudy.png",
    "09d": "rain.png",
    "11d": "storm.png",
    "13d": "snow.png",
}

# Get current weather and update UI
def get_weather():
    city = city_entry.get().strip()
    if not city:
        result_label.config(text="⚠️ Please enter a city name.")
        return

    api_key = "a142353f298e810fc1cac2772e9fa4ca"
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(current_url)
        data = response.json()
        print(data)  # Debugging purpose

        if data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]

            icon_filename = icon_map.get(icon_code, "sun.jpg")

            try:
                weather_img = Image.open(icon_filename)
            except FileNotFoundError:
                weather_img = Image.open("default.png")

            weather_img = weather_img.resize((100, 100), Image.Resampling.LANCZOS)
            weather_icon = ImageTk.PhotoImage(weather_img)

            result_label.config(text=f"🌡 Temperature: {temp}°C\n🌤 Condition: {desc.capitalize()}")
            weather_icon_label.config(image=weather_icon)
            weather_icon_label.image = weather_icon  # Keep reference
            show_weather_view()
        else:
            result_label.config(text="⚠️ City not found!")
            show_weather_view()
    except Exception as e:
        result_label.config(text=f"Error: {e}")
        show_weather_view()

# Update time every second
def update_time():
    now = datetime.now()
    current_time = now.strftime("%A, %d %B %Y\n%I:%M:%S %p")
    time_label.config(text=current_time)
    root.after(1000, update_time)

# Show weather view
def show_weather_view():
    city_entry.pack_forget()
    get_btn.pack_forget()
    time_label.pack(pady=10)
    result_label.pack(pady=10)
    weather_icon_label.pack(pady=10)
    back_btn.pack(pady=10)

# Back to search input view
def back_to_search():
    result_label.pack_forget()
    time_label.pack_forget()
    weather_icon_label.pack_forget()
    back_btn.pack_forget()
    result_label.config(text="")
    city_entry.delete(0, tk.END)
    city_entry.pack(pady=10)
    get_btn.pack(pady=10)

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App")
root.attributes('-fullscreen', True)

# --- Fullscreen Background Image ---
try:
    bg_image = Image.open("city.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
except FileNotFoundError:
    print("city.jpg not found. Using plain background.")
    bg_photo = None

if bg_photo:
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    root.config(bg="gray20")

# --- Overlay Frame ---
overlay = tk.Frame(root, bg="black", padx=20, pady=20)
overlay.place(relx=0.5, rely=0.5, anchor="center")

# --- City Input ---
city_entry = tk.Entry(overlay, font=("Arial", 20), width=25, justify="center")
city_entry.pack(pady=10)

# --- Get Weather Button ---
get_btn = tk.Button(
    overlay,
    text="Get Weather",
    font=("Arial", 16),
    command=get_weather,
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
)
get_btn.pack(pady=10)

# --- Result Widgets (initially hidden) ---
time_label = tk.Label(overlay, text="", font=("Arial", 16), fg="lightblue", bg="black")
result_label = tk.Label(overlay, text="", font=("Arial", 16), fg="white", bg="black", justify="center")
weather_icon_label = tk.Label(overlay, bg="black")

back_btn = tk.Button(
    overlay,
    text="Back",
    font=("Arial", 14),
    command=back_to_search,
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
)

# Start time updater
update_time()

# Exit fullscreen on ESC
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
