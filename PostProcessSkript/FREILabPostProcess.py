#!/usr/bin/python
import sys
import re
import tkinter as tk

# Example use in prusa slicer:
#  C:\Users\mariu\AppData\Local\Microsoft\WindowsApps\pythonw.exe C:\Users\mariu\Documents\GitHub\3d-Printing_Scripts\PostProcessSkript\FREILabPostProcess.py;

# Ensure we got a filename argument
if len(sys.argv) < 2:
    print("Error: No file provided.")
    sys.exit(1)

sourceFile = sys.argv[1]

# Function to read the length of the extruded filament
def read_extruded_length(gcode):
    pattern = r";\s*filament used\s*\[mm\]\s*=\s*(\d+\.\d+|\d+)"
    match = re.search(pattern, gcode)
    return float(match.group(1)) if match else None

# Function to read the weight of the extruded filament
def read_extruded_weight(gcode):
    pattern = r";\s*filament used\s*\[g\]\s*=\s*(\d+\.\d+|\d+)"
    match = re.search(pattern, gcode)
    return float(match.group(1)) if match else None

# Function to extract filament type
def extract_filament_type(gcode):
    pattern = r";\s*filament_type\s*=\s*(PETG|PLA|TPU)"
    match = re.search(pattern, gcode)
    return match.group(1) if match else "Unknown"

# Read the entire G-code file into memory
with open(sourceFile, "r") as f:
    lines = f.read()

# Get the extruded length and weight
extruded_length = read_extruded_length(lines) / 1000
extruded_weight = read_extruded_weight(lines)
filament_type = extract_filament_type(lines)


# Function to display the result in a Tkinter window
def wait_for_ok(extruded_length, extruded_weight):
    root = tk.Tk()
    root.title("FREILab")  # Set the window title

    # Load the logo
    try:
        logo = PhotoImage(file="logo.png")  # Make sure logo.png is in the same directory
        logo_label = tk.Label(root, image=logo)
        logo_label.pack(pady=10)
    except Exception as e:
        print("Logo loading failed:", e)

    # Heading label
    header_label = tk.Label(root, text="FREILab Filament Data", font=("Arial", 18, "bold"))
    header_label.pack(pady=10)

    # Create a frame for the parameters
    params_frame = tk.Frame(root)
    params_frame.pack(pady=10)

    # Display Filament Length
    length_label = tk.Label(params_frame, text=f"Filament Länge: {extruded_length:.2f} m", font=("Arial", 14))
    length_label.grid(row=0, column=0, sticky="w", pady=5)

    # Display Filament Weight
    weight_label = tk.Label(params_frame, text=f"Filament Gewicht: {extruded_weight:.2f} g", font=("Arial", 14))
    weight_label.grid(row=1, column=0, sticky="w", pady=5)

    # Display Filament Type
    filament_label = tk.Label(params_frame, text=f"Filament Typ: {filament_type}", font=("Arial", 14))
    filament_label.grid(row=2, column=0, sticky="w", pady=5)

    # OK Button to close the window
    ok_button = tk.Button(root, text="OK", command=root.destroy, font=("Arial", 12))
    ok_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    wait_for_ok(extruded_length, extruded_weight)