import matplotlib.pyplot as plt

# Define the layered architecture data
layers = {
    "Presentation Layer": {
        "Functionality": "Handles user interactions, facilitates user inputs, and communicates with the logic layer to enable backend functionalities.",
        "Details": ["Seamless user experience", "Manages all client-side operations"]
    },
    "Logic Layer": {
        "API Gateway": {
            "Functionality": "Acts as a single-entry point for the presentation layer to access the logic layer. Handles external API calls, and routes requests based on functionality."
        },
        "Core Business Logic": {
            "Functionality": "Contains the main application logic, processes user requests, and applies business rules. Includes data processing, computation, and core functionalities.",
            "Quantification": "The Crop Prediction Model analyses vast datasets to predict crop yields, considering weather, soil conditions, and historical data."
        },
        "Authentication": {
            "Functionality": "Handles authentication by routing between the database layer and the presentation layer."
        }
    },
    "Data Layer": {
        "Functionality": "Stores application data in a managed database, accessible by the logic layer. Ensures efficient data sharing and consistency.",
        "Details": ["Data access mechanisms", "Interacts with the logic layer for data storage and retrieval"]
    }
}

# Plot the layered architecture
fig, ax = plt.subplots(figsize=(12, 8))

# Define layer positions
layer_positions = {
    "Presentation Layer": (0.5, 0.9),
    "Logic Layer": (0.5, 0.6),
    "Data Layer": (0.5, 0.3)
}

# Define layer colors
layer_colors = {
    "Presentation Layer": "skyblue",
    "Logic Layer": "lightgreen",
    "Data Layer": "lightcoral"
}

# Draw the layers
for layer, position in layer_positions.items():
    ax.text(position[0], position[1], layer, ha='center', va='center', fontsize=16, weight='bold',
            bbox=dict(facecolor=layer_colors[layer], edgecolor='black', boxstyle='round,pad=1'))

# Draw sub-components of Logic Layer
logic_subcomponents = {
    "API Gateway": (0.5, 0.7),
    "Core Business Logic": (0.5, 0.6),
    "Authentication": (0.5, 0.5)
}

for subcomponent, position in logic_subcomponents.items():
    ax.text(position[0], position[1], subcomponent, ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'))

# Add arrows
arrows = [
    ("Presentation Layer", "Logic Layer"),
    ("Logic Layer", "Data Layer")
]

for start, end in arrows:
    ax.annotate("", xy=layer_positions[end], xytext=layer_positions[start],
                arrowprops=dict(arrowstyle="->", lw=2))

# Set plot parameters
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("Layered Architecture Diagram", fontsize=20)
plt.show()
