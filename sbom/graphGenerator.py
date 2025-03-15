import matplotlib.pyplot as plt
import os
import json

def generate_graphs():
    # Construct the file path for licence.json relative to this script
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "licence.json")

    # Open and load the JSON data
    with open(file_path, "r") as f:
        licences = json.load(f)

    # Extract license names and counts
    license_names = list(licences.keys())
    counts = list(licences.values())

    # Create the bar graph
    plt.figure(figsize=(8, 8 ), dpi=100)
    plt.bar(license_names, counts, color='skyblue')
    plt.xlabel('License')
    plt.ylabel('Count')
    plt.title('License Usage')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the figure as a PNG file in the same directory as this script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(parent_dir, "gui", "graphs")
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Output file path.
    output_file = os.path.join(output_dir, "bargraph.png")
    plt.savefig(output_file, dpi=100)


    # Create figure and plot pie chart
    plt.figure(figsize=(9.5, 7), dpi=50)
    wedges, texts, autotexts = plt.pie(
        counts,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 8}
    )
    plt.title('License Distribution')
    plt.axis('equal')  # Ensures the pie is drawn as a circle

    # Move the pie to the right by adjusting subplot margins
    plt.subplots_adjust(left=0.4)  

    # Place the legend on the left of the pie
    plt.legend(
        wedges,
        license_names,
        title="License",
        loc="center right",         # Align legend's right edge...
        bbox_to_anchor=(-0.15, 0.5),  # ...with an anchor to the left of the plot.
        fontsize=8
    )

    output_file_pie = os.path.join(output_dir, "piechart.png")
    plt.savefig(output_file_pie, dpi=100, bbox_inches='tight')