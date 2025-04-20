# Glow-Pick

The project "GLOW PICK" is a Python-based desktop application designed to help users filter and explore cosmetic products interactively. It uses the Tkinter library for the graphical user interface and relies on a dataset loaded from a CSV file named "cosmetic_p.csv" containing detailed information about various cosmetic products.

The code combines data processing with an interactive GUI to provide a comprehensive tool for filtering and visualizing cosmetic product data.Here's an explanation of the main parts of the code:

1. Imports and Setup:
- The code imports necessary libraries including pandas for data manipulation, tkinter and ttk for GUI components, matplotlib and seaborn for plotting, and os for file handling.
- Matplotlib is configured to use the 'TkAgg' backend suitable for Tkinter integration.
- A modern seaborn style and system fonts are set for consistent and visually appealing plots.
  
2. Data Loading:
- The application attempts to load a CSV file named 'cosmetic_p.csv' into a pandas DataFrame.
- If the file is missing or an error occurs, an error message box is shown and the app exits.

3. Main Window and Start Page:
- A Tkinter root window is created with a title, size, background color, and minimum size.
- A start page frame is created with the app name label styled in pink and large font.
- The app attempts to load and display a logo image if available.
- A "Start" button is provided to transition from the start page to the main application window.

4. Main Application Window:
- The main frame contains filters and controls for the user to specify criteria for cosmetic products.
- Dropdowns and checkboxes are created for filtering by brand, skin type, and other columns.
- An ingredients multi-select listbox allows users to select multiple ingredients to filter by.
- Entry fields allow users to specify price and rank ranges, with validation to ensure correct input.
- A "Fetch Data" button triggers filtering of the dataset based on user selections.
- A "Visualize Data" button opens the visualization page.
- A "Back to Start" button returns to the start page.
  
5. Data Filtering and Display:
- The fetch_data function applies filters to the DataFrame based on user inputs.
- It filters by brand, skin types, selected ingredients, price range, and rank range.
- Validation ensures inputs are within valid ranges and that the number of rows requested is positive and does not exceed the filtered dataset size.
- Filtered data is stored globally and displayed in a new window using a Treeview widget with scrollbars.
- The display window shows product details with formatted columns and a total count label.

6. Visualization Page:
- The visualization frame provides various charts to analyze the filtered data.
- Charts include price distribution histogram, brand distribution bar chart, price vs rank scatter plot, price by brand box plot, skin type distribution pie chart, and ingredients heatmap.
- Each chart is created using matplotlib and seaborn and embedded in the Tkinter window via FigureCanvasTkAgg.
- Buttons allow users to switch between different visualizations.
- A "Back to Main" button returns to the main application window.

7. Event Handling and Navigation:
- The app handles window closing events with confirmation.
- Navigation between start, main, and visualization pages is managed by packing and unpacking frames.
- Mouse wheel scrolling is enabled for the main canvas.
- Dropdowns and listboxes are populated dynamically based on the dataset.

How it works:

-Upon launching, the application displays a start page with the app name and logo, and a "Start" button to enter the main interface.
- The main interface allows users to filter cosmetic products based on multiple criteria including brand, skin type, ingredients, price range, and rank range.
- Users can select brands from a dropdown, choose skin types via checkboxes, and select multiple ingredients from a list.
- Price and rank filters are input fields with validation to ensure correct ranges.
- After setting filters, users can fetch the filtered product data, which is displayed in a new window in a tabular format with scrollbars for easy navigation.
- The application also provides a visualization page where users can view various charts such as price distribution, brand distribution, price vs rank scatter plots, price by brand box plots, skin type distribution pie charts, and ingredients heatmaps to better understand the data.
- The UI is styled with a pink-themed color scheme and uses matplotlib and seaborn libraries for creating modern and informative visualizations.
- The app handles errors gracefully, showing message boxes for missing files, invalid inputs, or when no data matches the selected criteria.

What it does:

- "GLOW PICK" serves as an interactive tool for users to explore and analyze cosmetic products based on their preferences and needs.
- It helps users filter products by brand, ingredients, skin type suitability, price, and ranking.
- The visualization features provide insights into product distributions and relationships within the dataset, aiding in informed decision-making.

# How to run the Project:
The project requires the following Python modules to be installed, as specified in the requirements.txt file:

- pandas (version 1.5.0 or higher)
- matplotlib (version 3.5.0 or higher)
- seaborn (version 0.12.0 or higher)

Additionally, the project uses the built-in tkinter module for the GUI, which is included with standard Python installations.

To install the required modules, you can run the following command in your terminal or command prompt:


- pip install -r requirements.txt

This will install pandas, matplotlib, and seaborn with the specified minimum versions.

To run the application, navigate to the project directory (where ui.py is located) and execute:


- python ui.py

This will launch the "GLOW PICK" desktop application window.

Make sure you have the 'cosmetic_p.csv' file and optionally 'logo2.png' image in the same directory as ui.py for the application to function correctly.
Overall, the project is a user-friendly cosmetic product filtering and visualization tool that leverages Python's data handling and GUI capabilities to deliver an engaging experience.
