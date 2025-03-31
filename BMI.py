import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import math

def calculate_bmi():
    try:
        age = int(age_entry.get())
        gender = gender_var.get()
        height = float(height_entry.get()) / 100  # Convert cm to meters
        weight = float(weight_entry.get())
        neck = float(neck_entry.get())
        
        bmi = weight / (height ** 2)
        bmi_label.config(text=f"BMI: {bmi:.2f}")
        
        # Calculate BFP using both methods
        if gender == "Male":
            abdomen = float(abdomen_entry.get())
            # US Navy formula (converted to body fat %)
            bfp_navy = (495 / (1.0324 - 0.19077 * math.log10(abdomen - neck) + 0.15456 * math.log10(height * 100))) - 450
            if age > 17:
                bfp_bmi = (1.20 * bmi) + (0.23 * age) - 16.2
            else:
                bfp_bmi = (1.51 * bmi) - (0.70 * age) - 2.2
        else:
            waist = float(waist_entry.get())
            hip = float(hip_entry.get())
            bfp_navy = (495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height * 100))) - 450
            if age > 17:
                bfp_bmi = (1.20 * bmi) + (0.23 * age) - 5.4
            else:
                bfp_bmi = (1.51 * bmi) - (0.70 * age) + 1.4
        
        bfp_navy_label.config(text=f"BFP (US Navy Method): {bfp_navy:.1f}%")
        bfp_bmi_label.config(text=f"BFP (BMI Method): {bfp_bmi:.1f}%")
        
        plot_bmi_chart(height * 100, weight, bmi)
        plot_bfp_chart(bfp_navy, bfp_bmi, gender)
        
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers for all fields.")

def plot_bmi_chart(height, weight, bmi):
    heights = np.arange(140, 210, 1)  # Heights in cm
    
    underweight = 18.5 * (heights / 100) ** 2
    normal = 25 * (heights / 100) ** 2
    overweight = 30 * (heights / 100) ** 2
    obese = 40 * (heights / 100) ** 2
    
    plt.figure(figsize=(10, 8))
    plt.fill_between(heights, 0, underweight, color='yellow', alpha=0.5, label='Underweight (<18.5)')
    plt.fill_between(heights, underweight, normal, color='green', alpha=0.5, label='Normal (18.5-25)')
    plt.fill_between(heights, normal, overweight, color='orange', alpha=0.5, label='Overweight (25-30)')
    plt.fill_between(heights, overweight, obese, color='red', alpha=0.5, label='Obese (30-40)')
    plt.fill_between(heights, obese, 300, color='darkred', alpha=0.5, label='Severely Obese (40+)')
    
    plt.scatter(height, weight, color='black', marker='o', label=f'You (BMI {bmi:.1f})')
    plt.xlabel("Height (cm)")
    plt.ylabel("Weight (kg)")
    plt.legend()
    plt.title("BMI Chart")
    plt.grid()
    plt.show()

def plot_bfp_chart(bfp_navy, bfp_bmi, gender):
    """
    Plot a BFP chart with colored zones and an embedded reference table.
    For men and women, different body fat percentage ranges are highlighted.
    """
    plt.figure(figsize=(10, 6))
    
    # Define ranges and colors for men and women
    if gender == "Male":
        # Reference ranges for men (percent)
        ranges = {
            "Essential": (2, 5),
            "Athletes": (6, 13),
            "Fitness": (14, 17),
            "Acceptable": (18, 24),
            "Obese": (25, 50)
        }
    else:
        # Reference ranges for women (percent)
        ranges = {
            "Essential": (10, 13),
            "Athletes": (14, 20),
            "Fitness": (21, 24),
            "Acceptable": (25, 31),
            "Obese": (32, 50)
        }
    
    # Colors for the different categories
    colors = {
        "Essential": "#ADD8E6",   # light blue
        "Athletes": "#90EE90",    # light green
        "Fitness": "#FFFF99",     # light yellow
        "Acceptable": "#FFA500",  # orange
        "Obese": "#FF6347"        # tomato/red
    }
    
    # Plot the colored zones using axvspan
    for label, (low, high) in ranges.items():
        plt.axvspan(low, high, color=colors[label], alpha=0.5, label=label)
    
    # Plot vertical dashed lines for BFP values
    plt.axvline(bfp_navy, color='black', linestyle='--', linewidth=2, label=f'US Navy BFP: {bfp_navy:.1f}%')
    plt.axvline(bfp_bmi, color='blue', linestyle='--', linewidth=2, label=f'BMI Method BFP: {bfp_bmi:.1f}%')
    
    plt.xlabel("Body Fat Percentage (%)")
    plt.xlim(0, 55)
    plt.yticks([])  # Hide y-axis
    
    plt.title("Body Fat Percentage (BFP) Chart")
    plt.legend(loc='upper right')
    
    # Create the reference table data
    if gender == "Male":
        table_data = [
            ["Essential", "2 - 5%"],
            ["Athletes", "6 - 13%"],
            ["Fitness", "14 - 17%"],
            ["Acceptable", "18 - 24%"],
            ["Obese", "25%+"]
        ]
    else:
        table_data = [
            ["Essential", "10 - 13%"],
            ["Athletes", "14 - 20%"],
            ["Fitness", "21 - 24%"],
            ["Acceptable", "25 - 31%"],
            ["Obese", "32%+"]
        ]
    
    # Add the table to the plot
    col_labels = ["Category", "Reference Range"]
    table = plt.table(cellText=table_data, colLabels=col_labels, cellLoc='center', loc='bottom', bbox=[0.0, -0.45, 1, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    
    plt.subplots_adjust(bottom=0.3)
    plt.show()

# Build the Tkinter UI
root = tk.Tk()
root.title("BMI and BFP Calculator")
root.geometry("600x600")

gender_var = tk.StringVar(value="Male")

tk.Label(root, text="Age:", font=("Arial", 14)).grid(row=0, column=0, sticky='w', padx=10, pady=5)
age_entry = tk.Entry(root, font=("Arial", 14), width=20)
age_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Gender:", font=("Arial", 14)).grid(row=1, column=0, sticky='w', padx=10, pady=5)
tk.OptionMenu(root, gender_var, "Male", "Female").grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Height (cm):", font=("Arial", 14)).grid(row=2, column=0, sticky='w', padx=10, pady=5)
height_entry = tk.Entry(root, font=("Arial", 14), width=20)
height_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (kg):", font=("Arial", 14)).grid(row=3, column=0, sticky='w', padx=10, pady=5)
weight_entry = tk.Entry(root, font=("Arial", 14), width=20)
weight_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Neck (cm):", font=("Arial", 14)).grid(row=4, column=0, sticky='w', padx=10, pady=5)
neck_entry = tk.Entry(root, font=("Arial", 14), width=20)
neck_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Abdomen (cm, males):", font=("Arial", 14)).grid(row=5, column=0, sticky='w', padx=10, pady=5)
abdomen_entry = tk.Entry(root, font=("Arial", 14), width=20)
abdomen_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Waist (cm, females):", font=("Arial", 14)).grid(row=6, column=0, sticky='w', padx=10, pady=5)
waist_entry = tk.Entry(root, font=("Arial", 14), width=20)
waist_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Hip (cm, females):", font=("Arial", 14)).grid(row=7, column=0, sticky='w', padx=10, pady=5)
hip_entry = tk.Entry(root, font=("Arial", 14), width=20)
hip_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Button(root, text="Calculate", font=("Arial", 14), command=calculate_bmi).grid(row=8, column=0, columnspan=2, pady=10)

bmi_label = tk.Label(root, text="BMI: ", font=("Arial", 14))
bmi_label.grid(row=9, column=0, columnspan=2, pady=5)

bfp_navy_label = tk.Label(root, text="BFP (US Navy Method): ", font=("Arial", 14))
bfp_navy_label.grid(row=10, column=0, columnspan=2, pady=5)

bfp_bmi_label = tk.Label(root, text="BFP (BMI Method): ", font=("Arial", 14))
bfp_bmi_label.grid(row=11, column=0, columnspan=2, pady=5)

root.mainloop()
