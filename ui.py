import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from tkinter import scrolledtext
import os

# Configure matplotlib style
plt.style.use('seaborn-v0_8')  # Use a more modern style
sns.set_theme()  # Set seaborn theme

# Configure matplotlib to use a system font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']

# Load the dataset
try:
    df = pd.read_csv('cosmetic_p.csv')
except FileNotFoundError:
    messagebox.showerror("Error", "cosmetic_p.csv file not found. Please make sure the file exists in the same directory.")
    exit(1)
except Exception as e:
    messagebox.showerror("Error", f"Error loading the dataset: {str(e)}")
    exit(1)

# Print the columns to check their names
print("Columns in the DataFrame:", df.columns.tolist())

# Create the main window
root = tk.Tk()
root.title("GLOW PICK")
root.geometry("800x600")    # Adjusted initial size
root.configure(bg='#FFEBEB')  # Set background color
root.minsize(800, 600)  # Set minimum window size

# Add close button handler
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Create the start page
start_frame = tk.Frame(root, bg='#FFEBEB')
start_frame.pack(expand=True, fill='both')

# Create a centered content frame
content_frame = tk.Frame(start_frame, bg='#FFEBEB')
content_frame.place(relx=0.5, rely=0.5, anchor='center')

# Application name label with enhanced styling
app_name_label = tk.Label(content_frame, text="GLOW PICK", 
                         font=("Helvetica", 36, "bold"), 
                         bg='#FFEBEB',
                         fg='#FF6B6B')  # Added a nice pink color
app_name_label.pack(pady=30)

# Logo label (with error handling)
try:
    if os.path.exists("logo2.png"):
        logo_image = tk.PhotoImage(file="logo2.png")
        logo_label = tk.Label(content_frame, image=logo_image, bg='#FFEBEB')
        logo_label.image = logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(pady=5)
    else:
        print("Warning: logo2.png not found. Starting without logo.")
except Exception as e:
    print(f"Warning: Error loading logo: {str(e)}")

# Start button with enhanced styling
start_button = tk.Button(content_frame, 
                        text="Start", 
                        command=lambda: show_main_window(), 
                        width=20, 
                        height=2,
                        font=("Helvetica", 12),
                        bg='#FF6B6B',
                        fg='white',
                        relief='raised',
                        borderwidth=2)
start_button.pack(pady=15)

# Create the main application window frame
main_frame = tk.Frame(root, bg='#FFEBEB')

# Create dropdowns for column selection (including Brand, Name, Price, and Rank)
columns = df.columns.tolist()
if 'name' in columns:
    columns.remove('name')   # Remove Name from the dropdowns

# Add additional filtering options for ingredients and skin types
if 'ingredients' in columns:
    columns.remove('ingredients')  # Remove ingredients from columns list as we'll handle it separately

# Ensure brand is in columns and at the beginning
if 'brand' in columns:
    columns.remove('brand')
columns.insert(0, 'brand')  # Add brand at the beginning of the list

# Handle skin type
if 'skin_type' in columns:
    columns.remove('skin_type')
    columns.append('skin_type')  # Include Skin Type at the end

# Initialize variables for dropdowns and checkboxes
column_vars = {col: tk.StringVar() for col in columns}
checkbox_vars = {col: tk.BooleanVar() for col in columns}
dropdowns = {}

# Function to populate dropdowns with unique values from each column and handle multi-select
def populate_dropdowns():
    try:
        # Populate brand and skin_type dropdowns
        for col in ['brand', 'skin_type']:
            if col in dropdowns:
                unique_values = sorted(df[col].unique().tolist())
                current_value = column_vars[col].get()
                dropdowns[col]['values'] = unique_values
                if current_value in unique_values:
                    column_vars[col].set(current_value)
                else:
                    column_vars[col].set('')
        
        # Populate ingredients listbox
        if 'ingredients' in df.columns:
            # Clear existing items
            ingredients_listbox.delete(0, tk.END)
            
            # Get unique ingredients, split by comma, and clean them
            unique_ingredients = set()
            for ingredients_str in df['ingredients'].dropna():
                ingredients_list = [ing.strip() for ing in ingredients_str.split(',')]
                unique_ingredients.update(ingredients_list)
            
            # Sort and insert ingredients
            for ingredient in sorted(unique_ingredients):
                if ingredient:  # Only add non-empty ingredients
                    ingredients_listbox.insert(tk.END, ingredient)
    except Exception as e:
        messagebox.showerror("Error", f"Error populating dropdowns: {str(e)}")

# Function to fetch data based on user input
def fetch_data(checkbox_vars):
    try:
        # Start with the full DataFrame
        filtered_df = df.copy()

        # Handle brand dropdown
        selected_brand = column_vars['brand'].get()
        if selected_brand and selected_brand != 'All Brands':
            filtered_df = filtered_df[filtered_df['brand'] == selected_brand]

        # Handle skin type checkboxes
        skin_types = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
        selected_skin_types = [st for st in skin_types if checkbox_vars[st].get()]
        
        # If skin types are selected, filter the data
        if selected_skin_types:
            # Create a mask that will be True if any of the selected skin types is 1
            skin_mask = filtered_df[selected_skin_types].any(axis=1)
            filtered_df = filtered_df[skin_mask]
            
            # Only keep the selected skin type columns
            columns_to_keep = [col for col in filtered_df.columns if col not in skin_types or col in selected_skin_types]
            filtered_df = filtered_df[columns_to_keep]

        # Handle ingredients multi-select
        if 'ingredients' in df.columns:
            selected_ingredients = [ingredients_listbox.get(i) for i in ingredients_listbox.curselection()]
            if selected_ingredients:
                mask = filtered_df['ingredients'].apply(lambda x: any(ing.strip() in str(x).split(',') for ing in selected_ingredients))
                filtered_df = filtered_df[mask]

        # Get price and rank range with validation
        try:
            price_min = float(price_min_entry.get()) if price_min_entry.get() else df['price'].min()
            price_max = float(price_max_entry.get()) if price_max_entry.get() else df['price'].max()
            rank_min = int(rank_min_entry.get()) if rank_min_entry.get() else df['rank'].min()
            rank_max = int(rank_max_entry.get()) if rank_max_entry.get() else df['rank'].max()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and rank ranges.")
            return

        # Validate ranges
        if price_min < df['price'].min() or price_max > df['price'].max():
            messagebox.showerror("Error", f"Price must be between {df['price'].min():.2f} and {df['price'].max():.2f}")
            return

        if rank_min < df['rank'].min() or rank_max > df['rank'].max():
            messagebox.showerror("Error", f"Rank must be between {df['rank'].min()} and {df['rank'].max()}")
            return

        if price_min > price_max:
            messagebox.showerror("Error", "Minimum price cannot be greater than maximum price.")
            return

        if rank_min > rank_max:
            messagebox.showerror("Error", "Minimum rank cannot be greater than maximum rank.")
            return

        # Filter based on price and rank
        filtered_df = filtered_df[(filtered_df['price'] >= price_min) & (filtered_df['price'] <= price_max)]
        filtered_df = filtered_df[(filtered_df['rank'] >= rank_min) & (filtered_df['rank'] <= rank_max)]

        # Get number of rows to display
        try:
            num_rows = int(row_entry.get())
            if num_rows <= 0:
                messagebox.showerror("Error", "Number of rows must be positive.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for rows.")
            return

        if len(filtered_df) == 0:
            messagebox.showerror("Error", "No data matches the selected criteria.")
            return
        
        if num_rows > len(filtered_df):
            messagebox.showerror("Error", f"Number of rows ({num_rows}) exceeds filtered dataset size ({len(filtered_df)}).")
            return

        # Store the filtered data globally for visualization
        global fetched_data
        fetched_data = filtered_df.head(num_rows)
        
        # Display the data
        display_data(fetched_data)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching data: {str(e)}")
        print(f"Error details: {str(e)}")  # Print error details for debugging

# Function to display data in a new window
def display_data(data):
    if data is None or data.empty:
        messagebox.showinfo("No Results", "No products match your criteria.")
        return

    # Create a new window for displaying data
    display_window = tk.Toplevel(root)
    display_window.title("Product Results")
    
    # Set window size and position
    window_width = 1200
    window_height = min(800, 100 + len(data) * 25)  # Dynamic height based on data
    screen_width = display_window.winfo_screenwidth()
    screen_height = display_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    display_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create main frame
    main_frame = ttk.Frame(display_window, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create Treeview with scrollbars
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tree = ttk.Treeview(tree_frame, height=20)
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Grid layout for treeview and scrollbars
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)

    # Configure columns
    columns = list(data.columns)
    tree["columns"] = columns
    tree["show"] = "headings"

    # Set column headings and widths
    for col in columns:
        heading = col.replace('_', ' ').title()
        if col in ['price', 'rank']:
            width = 80
        elif col == 'ingredients':
            width = 300
        elif col in ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']:
            width = 100
        else:
            width = 150
        tree.heading(col, text=heading)
        tree.column(col, width=width, minwidth=50)

    # Insert data
    for idx, row in data.iterrows():
        values = []
        for col in columns:
            value = row[col]
            if col == 'price':
                value = f"${value:.2f}" if pd.notna(value) else "N/A"
            elif col == 'rank':
                value = f"{int(value)}" if pd.notna(value) else "N/A"
            elif col in ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']:
                value = "Yes" if value == 1 else "No"
            elif col == 'ingredients':
                value = str(value)[:300] + "..." if len(str(value)) > 300 else str(value)
            values.append(str(value) if pd.notna(value) else "")
        tree.insert("", "end", values=values)

    # Add total count label
    count_label = ttk.Label(main_frame, text=f"Total Products: {len(data)}", 
                           font=("Helvetica", 10, "bold"))
    count_label.pack(pady=5)

    # Add close button
    close_button = ttk.Button(main_frame, text="Close", 
                             command=display_window.destroy)
    close_button.pack(pady=5)

# Function to show the main window
def show_main_window():
    start_frame.pack_forget()  # Hide the start page
    main_frame.pack(expand=True, fill='both')  # Show the main application window
    populate_dropdowns()  # Populate dropdowns with unique values

# Function to show visualization page
def show_visualization_page():
    main_frame.pack_forget()  # Hide the main application window
    visualization_frame.pack(expand=True, fill='both')  # Show the visualization page
    
    # Set visualization window size
    root.geometry("1000x700")  # Set the main window size instead
    create_visualizations()  # Call the function to create visualizations

# Create a scrollable frame for the main window with increased width
main_canvas = tk.Canvas(main_frame, bg='#FFEBEB', width=1150)  # Set canvas width
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

# Enable mousewheel scrolling
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Configure canvas to expand with window
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_canvas.configure(width=1150, height=600)  # Set both width and height

# Add a title to the main window
main_title = tk.Label(scrollable_frame, 
                     text="Cosmetic Product Filter", 
                     font=("Helvetica", 24, "bold"),
                     bg='#FFEBEB',
                     fg='#FF6B6B')
main_title.pack(pady=20)

# Create a frame for filters
filters_frame = ttk.LabelFrame(scrollable_frame, text="Filters", padding=10)
filters_frame.pack(fill='x', padx=20, pady=10)

# Create ingredients listbox with scrollbar in a separate frame
ingredients_frame = ttk.LabelFrame(filters_frame, text="Ingredients Selection", padding=10)
ingredients_frame.pack(fill='x', padx=10, pady=5)

ingredients_label = tk.Label(ingredients_frame, 
                           text="Select Ingredients (Hold Ctrl/Cmd to select multiple):", 
                           bg='#FFEBEB',
                           font=("Helvetica", 10))
ingredients_label.pack(anchor='w', padx=5, pady=5)

ingredients_listbox = tk.Listbox(ingredients_frame, 
                                selectmode=tk.MULTIPLE, 
                                height=5, 
                                width=80,
                                font=("Helvetica", 10))
ingredients_listbox.pack(side='left', fill='both', expand=True, padx=5)

ingredients_scrollbar = ttk.Scrollbar(ingredients_frame, orient="vertical", command=ingredients_listbox.yview)
ingredients_scrollbar.pack(side='right', fill='y')
ingredients_listbox.configure(yscrollcommand=ingredients_scrollbar.set)

# Create a frame for price and rank filters
price_rank_frame = ttk.LabelFrame(filters_frame, text="Price and Rank Range", padding=10)
price_rank_frame.pack(fill='x', padx=10, pady=5)

# Display min and max limits
limits_frame = ttk.Frame(price_rank_frame)
limits_frame.pack(fill='x', pady=5)

# Price limits
price_limits_label = tk.Label(limits_frame, 
                            text=f"Price Range: {df['price'].min():.2f} - {df['price'].max():.2f}", 
                            bg='#FFEBEB', 
                            font=("Helvetica", 10))
price_limits_label.pack(side='left', padx=5)

# Rank limits
rank_limits_label = tk.Label(limits_frame, 
                           text=f"Rank Range: {df['rank'].min()} - {df['rank'].max()}", 
                           bg='#FFEBEB', 
                           font=("Helvetica", 10))
rank_limits_label.pack(side='left', padx=5)

# Entry for price range with enhanced styling
price_frame = ttk.Frame(price_rank_frame)
price_frame.pack(fill='x', pady=5)

price_min_label = tk.Label(price_frame, text="Minimum Price:", bg='#FFEBEB', font=("Helvetica", 10))
price_min_label.pack(side='left', padx=5)
price_min_entry = tk.Entry(price_frame, width=15, font=("Helvetica", 10))
price_min_entry.pack(side='left', padx=5)
price_min_entry.insert(0, str(df['price'].min()))  # Set default value

price_max_label = tk.Label(price_frame, text="Maximum Price:", bg='#FFEBEB', font=("Helvetica", 10))
price_max_label.pack(side='left', padx=5)
price_max_entry = tk.Entry(price_frame, width=15, font=("Helvetica", 10))
price_max_entry.pack(side='left', padx=5)
price_max_entry.insert(0, str(df['price'].max()))  # Set default value

# Entry for rank range with enhanced styling
rank_frame = ttk.Frame(price_rank_frame)
rank_frame.pack(fill='x', pady=5)

rank_min_label = tk.Label(rank_frame, text="Minimum Rank:", bg='#FFEBEB', font=("Helvetica", 10))
rank_min_label.pack(side='left', padx=5)
rank_min_entry = tk.Entry(rank_frame, width=15, font=("Helvetica", 10))
rank_min_entry.pack(side='left', padx=5)
rank_min_entry.insert(0, str(df['rank'].min()))  # Set default value

rank_max_label = tk.Label(rank_frame, text="Maximum Rank:", bg='#FFEBEB', font=("Helvetica", 10))
rank_max_label.pack(side='left', padx=5)
rank_max_entry = tk.Entry(rank_frame, width=15, font=("Helvetica", 10))
rank_max_entry.pack(side='left', padx=5)
rank_max_entry.insert(0, str(df['rank'].max()))  # Set default value

# Entry for number of rows with enhanced styling
row_frame = ttk.Frame(price_rank_frame)
row_frame.pack(fill='x', pady=5)

row_label = tk.Label(row_frame, text="Number of rows to fetch:", bg='#FFEBEB', font=("Helvetica", 10))
row_label.pack(side='left', padx=5)
row_entry = tk.Entry(row_frame, width=15, font=("Helvetica", 10))
row_entry.pack(side='left', padx=5)
row_entry.insert(0, "10")  # Set default value

# Create buttons frame with enhanced styling
buttons_frame = ttk.Frame(scrollable_frame)
buttons_frame.pack(fill='x', padx=20, pady=20)

# Fetch button with enhanced styling
fetch_button = tk.Button(buttons_frame, 
                        text="Fetch Data", 
                        command=lambda: fetch_data(checkbox_vars),
                        width=20,
                        height=2,
                        font=("Helvetica", 12),
                        bg='#FF6B6B',
                        fg='white',
                        relief='raised',
                        borderwidth=2)
fetch_button.pack(side='left', padx=10)

# Visualization button with enhanced styling
visualize_button = tk.Button(buttons_frame, 
                           text="Visualize Data", 
                           command=show_visualization_page,
                           width=20,
                           height=2,
                           font=("Helvetica", 12),
                           bg='#FF6B6B',
                           fg='white',
                           relief='raised',
                           borderwidth=2)
visualize_button.pack(side='left', padx=10)

# Back button with enhanced styling
back_button = tk.Button(buttons_frame, 
                       text="Back to Start", 
                       command=lambda: [main_frame.pack_forget(), start_frame.pack(expand=True, fill='both')],
                       width=20,
                       height=2,
                       font=("Helvetica", 12),
                       bg='#FF6B6B',
                       fg='white',
                       relief='raised',
                       borderwidth=2)
back_button.pack(side='left', padx=10)

# Create other dropdowns and checkboxes with enhanced styling
for i, col in enumerate(columns):
    # Create a frame for each row
    row_frame = ttk.Frame(scrollable_frame)
    row_frame.pack(fill='x', padx=10, pady=5)
    
    label = tk.Label(row_frame, 
                    text=col.title(), 
                    bg='#FFEBEB',
                    font=("Helvetica", 10))  # Capitalize the label
    label.pack(side='left', padx=10)
    
    if col == 'brand':  # Only brand gets a dropdown
        # Create a frame to hold dropdown and buttons
        dropdown_frame = ttk.Frame(row_frame)
        dropdown_frame.pack(side='left', fill='x', expand=True)
        
        dropdown = ttk.Combobox(dropdown_frame, 
                              textvariable=column_vars[col], 
                              state='readonly',
                              width=40,
                              font=("Helvetica", 10))
        dropdown.pack(side='left', fill='x', expand=True)
        dropdowns[col] = dropdown
        
        # Add Select All button for brand
        select_all_button = tk.Button(dropdown_frame, 
                                    text="Select All", 
                                    command=lambda: column_vars['brand'].set('All Brands'),
                                    font=("Helvetica", 10),
                                    bg='#FF6B6B',
                                    fg='white',
                                    relief='raised',
                                    borderwidth=2)
        select_all_button.pack(side='left', padx=5)
        
        # Populate brand dropdown immediately with "All Brands" option
        unique_values = ['All Brands'] + sorted(df[col].unique().tolist())
        dropdowns[col]['values'] = unique_values
        column_vars[col].set('All Brands')  # Set default value
    else:
        # All other columns just get checkboxes
        checkbox = tk.Checkbutton(row_frame, 
                                text='Enable', 
                                variable=checkbox_vars[col],
                                bg='#FFEBEB',
                                font=("Helvetica", 10))
        checkbox.pack(side='left', padx=10)

# Pack the scrollbar and canvas
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

# Create the visualization frame with enhanced styling
visualization_frame = tk.Frame(root, bg='#FFEBEB')

# Add a title to the visualization window
viz_title = tk.Label(visualization_frame, 
                    text="Data Visualization", 
                    font=("Helvetica", 24, "bold"),
                    bg='#FFEBEB',
                    fg='#FF6B6B')
viz_title.pack(pady=20)

# Function to create visualizations
def create_visualizations():
    if 'fetched_data' not in globals():
        messagebox.showerror("Error", "No data fetched for visualization.")
        return

    try:
        # Clear the previous plots
        for widget in visualization_frame.winfo_children():
            if widget != viz_title:  # Don't destroy the title
                widget.destroy()

        # Create main container frame
        viz_container = ttk.Frame(visualization_frame)
        viz_container.pack(fill='both', expand=True, padx=10, pady=5)

        # Create a frame to hold the current visualization
        viz_display_frame = ttk.Frame(viz_container)
        viz_display_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Function to clear current visualization
        def clear_visualization():
            for widget in viz_display_frame.winfo_children():
                widget.destroy()

        # Function to create and display visualizations
        def show_price_distribution():
            clear_visualization()
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(data=fetched_data, x='price', bins=20, ax=ax)
                ax.set_title('Price Distribution')
                ax.set_xlabel('Price ($)')
                ax.set_ylabel('Count')
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating price distribution: {str(e)}")

        def show_brand_distribution():
            clear_visualization()
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                brand_counts = fetched_data['brand'].value_counts()
                brand_counts.plot(kind='bar', ax=ax)
                ax.set_title('Brand Distribution')
                ax.set_xlabel('Brand')
                ax.set_ylabel('Count')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating brand distribution: {str(e)}")

        def show_price_rank_scatter():
            clear_visualization()
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.scatterplot(data=fetched_data, x='price', y='rank', ax=ax)
                ax.set_title('Price vs Rank')
                ax.set_xlabel('Price ($)')
                ax.set_ylabel('Rank')
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating price vs rank scatter plot: {str(e)}")

        def show_price_by_brand_box():
            clear_visualization()
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.boxplot(data=fetched_data, x='brand', y='price', ax=ax)
                ax.set_title('Price Distribution by Brand')
                ax.set_xlabel('Brand')
                ax.set_ylabel('Price ($)')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating price by brand box plot: {str(e)}")

        def show_skin_type_distribution():
            clear_visualization()
            try:
                fig, ax = plt.subplots(figsize=(8, 4))
                skin_types = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
                
                # Get selected skin types from checkboxes
                selected_skin_types = [st for st in skin_types if checkbox_vars[st].get()]
                
                if not selected_skin_types:
                    messagebox.showwarning("Warning", "Please select at least one skin type.")
                    return
                    
                # Create a dictionary with all skin types, setting unselected ones to 0
                skin_data = {}
                for skin_type in skin_types:
                    if skin_type in selected_skin_types:
                        skin_data[skin_type] = fetched_data[skin_type].sum()
                    else:
                        skin_data[skin_type] = 0
                
                # Create a Series from the dictionary
                skin_series = pd.Series(skin_data)
                
                # Only show non-zero values in the pie chart
                non_zero_data = skin_series[skin_series > 0]
                
                if len(non_zero_data) == 0:
                    messagebox.showwarning("Warning", "No data available for the selected skin types.")
                    return
                    
                # Create pie chart with only non-zero values
                non_zero_data.plot(kind='pie', autopct='%1.1f%%', ax=ax)
                ax.set_title('Skin Type Distribution')
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating skin type distribution: {str(e)}")

        def show_ingredients_heatmap():
            clear_visualization()
            try:
                # Create a matrix of ingredients
                ingredients_list = fetched_data['ingredients'].str.split(',').explode().unique()
                matrix = pd.DataFrame(0, index=fetched_data.index, columns=ingredients_list)
                
                for idx, row in fetched_data.iterrows():
                    for ingredient in row['ingredients'].split(','):
                        if ingredient in ingredients_list:
                            matrix.loc[idx, ingredient] = 1

                fig, ax = plt.subplots(figsize=(8, 4))
                sns.heatmap(matrix, cmap='YlOrRd', ax=ax)
                ax.set_title('Ingredients Heatmap')
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=viz_display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error creating ingredients heatmap: {str(e)}")

        # Create visualization buttons with enhanced styling
        viz_buttons = [
            ("Price Distribution", show_price_distribution),
            ("Brand Distribution", show_brand_distribution),
            ("Price vs Rank", show_price_rank_scatter),
            ("Price by Brand", show_price_by_brand_box),
            ("Skin Type Distribution", show_skin_type_distribution),
            ("Ingredients Heatmap", show_ingredients_heatmap)
        ]

        # Create a frame for buttons with grid layout
        viz_buttons_frame = ttk.Frame(viz_container)
        viz_buttons_frame.pack(fill='x', padx=10, pady=5)

        # Create buttons in a grid layout
        for i, (text, command) in enumerate(viz_buttons):
            btn = tk.Button(viz_buttons_frame, 
                          text=text,
                          command=command,
                          width=15,
                          font=("Helvetica", 9),
                          bg='#FF6B6B',
                          fg='white',
                          relief='raised',
                          borderwidth=2)
            btn.grid(row=i//3, column=i%3, padx=5, pady=2)

        # Back button for visualization page
        back_button = tk.Button(visualization_frame, 
                              text="Back to Main", 
                              command=back_to_main,
                              width=20,
                              height=2,
                              font=("Helvetica", 12),
                              bg='#FF6B6B',
                              fg='white',
                              relief='raised',
                              borderwidth=2)
        back_button.pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Error creating visualizations: {str(e)}")

# Function to go back to the main application window
def back_to_main():
    visualization_frame.pack_forget()  # Hide the visualization page
    main_frame.pack(expand=True, fill='both')  # Show the main application window

# Run the application
root.mainloop()
