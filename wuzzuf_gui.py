# Core GUI framework
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Data processing
import pandas as pd
import os
from pathlib import Path

# Threading and timing
import threading
import queue
from datetime import datetime

# File handling
import json
import csv

# Standard GUI components
import tkinter as tk
from tkinter import ttk

# Import the scraper
from simple_wuzzuf_scraper import SimpleWuzzufScraper

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("Custom_themes/Custom_dark_theme.json")  # Themes: "blue" (standard), "green", "dark-blue"

class WuzzufScraperGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🚀 Wuzzuf Job Scraper")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 850)
        
        # Remove default window icon for cleaner appearance
        self.root.after(0, lambda: self.root.iconbitmap(""))
        
        # Application Color Scheme - Modern Dark Theme
        self.colors = {
            'primary': "#3c3c3c",        # Main accent color for borders and highlights
            'secondary': "#3c3c3c",      # Secondary accent for tabs and hover states
            'success': "#22C55E",        # Success color for start button and positive actions
            'warning': "#FACC15",        # Warning color for alerts and notifications
            'danger': "#EF4444",         # Danger color for stop button and errors
            'text_primary': "#F3F4F6",   # Primary text color for headers and main content
            'text_secondary': "#9CA3AF", # Secondary text color for labels and hints
            'bg_primary': "#0F172A",     # Main background color
            'bg_secondary': "#282828",   # Secondary background for panels and cards
            'white': "#ffffff",          # Pure white for contrast elements
            'wuzzuf_primary': "#0055d9", # Wuzzuf brand color for special highlights
        }

        # Initialize application state variables
        self.scraper = None              # Active scraper instance
        self.scraping_thread = None      # Background scraping thread
        self.scraping_queue = queue.Queue()  # Communication queue for scraping updates
        
        # Data storage variables
        self.df = None                   # Original dataset
        self.filtered_df = None          # Filtered dataset for display
        
        # Build the user interface
        self.create_widgets()
        
        # Auto-load default data if available
        self.load_default_csv()
        
        # Start background task monitoring
        self.monitor_scraping_queue()
    
    def create_widgets(self):
        """Build the main application interface"""
        
        # Main application frame (no scrolling for main interface)
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Main container for all content
        main_container = self.main_frame
        
        # Application Header Section
        header_frame = ctk.CTkFrame(
            main_container, 
            height=120, 
            corner_radius=15,
            fg_color=self.colors['bg_secondary'],
            border_width=2,
            border_color=self.colors['primary']
        )
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)  # Maintain fixed height
        
        # Header content container
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Application title and subtitle
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True)
        
        # Main application title
        self.title_label = ctk.CTkLabel(
            title_frame, 
            text="🚀 Wuzzuf Job Scraper Pro", 
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=self.colors['wuzzuf_primary']
        )
        self.title_label.pack(anchor="center")
        
        # Application subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Simple and efficient job scraping tool",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="center", pady=(8, 0))        # Main Tab Interface
        self.tabview = ctk.CTkTabview(
            main_container, 
            corner_radius=15, 
            height=900,
            fg_color=self.colors['bg_secondary'],
            segmented_button_fg_color=self.colors['bg_secondary'],
            segmented_button_selected_color=self.colors['primary'],
            segmented_button_selected_hover_color=self.colors['secondary'],
            text_color=self.colors['text_primary']
        )
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create application tabs
        self.create_scraping_tab()      # Job scraping configuration and control
        self.create_data_viewer_tab()   # Data viewing and analysis
        
    def create_scraping_tab(self):
        """Create the job scraping configuration and control interface"""
        scraping_frame = self.tabview.add("🔍 Scraping")
        
        # Main scraping interface section
        combined_section = self.create_section_frame(scraping_frame, "⚙️ Scraping Configuration & Control")
        
        # Container for side-by-side layout (configuration + log)
        main_container_frame = ctk.CTkFrame(combined_section)
        main_container_frame.pack(fill="x", padx=15, pady=15)
        
        # Layout configuration: 60% for settings, 40% for log
        main_container_frame.grid_columnconfigure(0, weight=6)  # Configuration panel
        main_container_frame.grid_columnconfigure(1, weight=4)  # Log panel
        
        # Left Panel: Search Configuration (60% width)
        config_control_frame = ctk.CTkFrame(
            main_container_frame,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['secondary']
        )
        config_control_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0, ipadx=15, ipady=15)
        
        # Search Configuration Section Header
        config_title = ctk.CTkLabel(
            config_control_frame,
            text="🔍 Search Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['white']
        )
        config_title.pack(anchor="w", padx=20, pady=(15, 12))
        
        # Search Keyword Input Field
        keyword_label = ctk.CTkLabel(
            config_control_frame,
            text="Search Keyword:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        keyword_label.pack(anchor="w", padx=(20, 10), pady=(8, 5))
        
        # Default keyword for software engineering jobs
        self.keyword_var = ctk.StringVar(value="software engineering")
        keyword_entry = ctk.CTkEntry(
            config_control_frame,
            textvariable=self.keyword_var,
            font=ctk.CTkFont(size=14),
            height=32,
            placeholder_text="Enter search keyword..."
        )
        keyword_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # Location Input Field (Optional)
        location_label = ctk.CTkLabel(
            config_control_frame,
            text="Location (optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        location_label.pack(anchor="w", padx=(20, 10), pady=(8, 5))
        
        # Location variable for filtering jobs by geographic area
        self.location_var = ctk.StringVar()
        location_entry = ctk.CTkEntry(
            config_control_frame,
            textvariable=self.location_var,
            font=ctk.CTkFont(size=14),
            height=32,
            placeholder_text="Enter location (optional)..."
        )
        location_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # Advanced Settings Row
        advanced_frame = ctk.CTkFrame(config_control_frame)
        advanced_frame.pack(fill="x", padx=20, pady=(5, 12))
        
        # Maximum Pages to Scrape
        pages_label = ctk.CTkLabel(
            advanced_frame,
            text="Max Pages:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        pages_label.pack(side="left", padx=(0, 10))
        
        # Default: scrape 3 pages (prevents excessive requests)
        self.max_pages_var = ctk.IntVar(value=3)
        pages_spinbox = ctk.CTkEntry(
            advanced_frame,
            textvariable=self.max_pages_var,
            font=ctk.CTkFont(size=14),
            width=70,
            height=28
        )
        pages_spinbox.pack(side="left", padx=(0, 20))
        

        
        # Scraping Control Section Header
        control_title = ctk.CTkLabel(
            config_control_frame,
            text="🎮 Scraping Control",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['white']
        )
        control_title.pack(anchor="w", padx=20, pady=(12, 10))
        
        # Control Buttons Container
        button_frame = ctk.CTkFrame(config_control_frame)
        button_frame.pack(fill="x", padx=20, pady=(8, 12))
        
        # Start Scraping Button
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Start Scraping",
            command=self.start_scraping,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=42,
            width=140,
            corner_radius=10,
            fg_color=self.colors['success'],
            hover_color=self.colors['secondary'],
            border_width=2,
            border_color=self.colors['primary'],
            text_color=self.colors['text_primary']
        )
        self.start_btn.pack(side="left", padx=(10, 8))
        
        # Stop Scraping Button (initially disabled)
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹️ Stop Scraping",
            command=self.stop_scraping,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=42,
            width=140,
            corner_radius=10,
            fg_color=self.colors['danger'],
            hover_color=("#dc2626", "#dc2626"),
            border_width=2,
            border_color=("#b91c1c", "#b91c1c"),
            text_color=self.colors['text_primary'],
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(8, 10))
        
        # Progress Tracking Section
        progress_frame = ctk.CTkFrame(config_control_frame)
        progress_frame.pack(fill="x", padx=20, pady=(0, 12))
        
        # Visual Progress Bar
        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            variable=self.progress_var,
            height=16,
            progress_color=self.colors['wuzzuf_primary']
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(12, 6))
        self.progress_bar.set(0)  # Initialize at 0%
        
        # Progress Status Text
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to start scraping",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.progress_label.pack(pady=(0, 8))
        
        # Right Panel: Scraping Log (40% width)
        log_frame = ctk.CTkFrame(
            main_container_frame,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['secondary']
        )
        log_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0, ipadx=10, ipady=10)
        
        # Log Section Header
        log_title = ctk.CTkLabel(
            log_frame,
            text="📝 Scraping Log",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['white']
        )
        log_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Real-time Log Display
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=350,  # Optimized height for better proportions
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=15)
    
    def create_data_viewer_tab(self):
        """Create the data viewing and analysis tab"""
        viewer_frame = self.tabview.add("📊 Data Viewer")

        # Create scrollable frame for data viewer content
        self.data_viewer_scrollable = ctk.CTkScrollableFrame(
            viewer_frame,
            fg_color="transparent",
            scrollbar_button_color=self.colors['secondary'],
            scrollbar_button_hover_color=self.colors['primary']
        )
        self.data_viewer_scrollable.pack(fill="both", expand=True, padx=5, pady=5)

        # Use scrollable frame as the container for data viewer content
        data_container = self.data_viewer_scrollable

        # File selection section
        file_section = self.create_section_frame(data_container, "📁 File Selection")
        
        file_input_frame = ctk.CTkFrame(file_section)
        file_input_frame.pack(fill="x", padx=15, pady=12)
        
        self.file_path_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(
            file_input_frame,
            textvariable=self.file_path_var,
            font=ctk.CTkFont(size=14),
            height=36,
            placeholder_text="Select CSV file..."
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=12)
        
        browse_btn = ctk.CTkButton(
            file_input_frame,
            text="🔍 Browse",
            command=self.browse_file,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36,
            width=90
        )
        browse_btn.pack(side="right", padx=(0, 10), pady=12)
        
        load_btn = ctk.CTkButton(
            file_input_frame,
            text="📥 Load",
            command=self.load_csv,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36,
            width=90,
            fg_color=("#28a745", "#28a745"),
            hover_color=("#218838", "#218838")
        )
        load_btn.pack(side="right", padx=(0, 15), pady=12)
        
        # Data Search and Filtering Interface
        filter_section = self.create_section_frame(data_container, "🔍 Search & Filter")
        
        # Filter controls container
        filter_controls = ctk.CTkFrame(filter_section)
        filter_controls.pack(fill="x", padx=15, pady=12)
        
        # Search term input field
        search_label = ctk.CTkLabel(
            filter_controls,
            text="Search:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(side="left", padx=(15, 10), pady=12)
        
        # Real-time search input with auto-filtering
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_controls,
            textvariable=self.search_var,
            font=ctk.CTkFont(size=14),
            height=32,
            width=180,
            placeholder_text="Enter search term..."
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=12)
        self.search_entry.bind('<KeyRelease>', self.filter_data)  # Auto-filter on typing
        
        # Column-specific filtering dropdown
        column_label = ctk.CTkLabel(
            filter_controls,
            text="Column:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        column_label.pack(side="left", padx=(0, 10), pady=12)
        
        # Dropdown to select specific column for filtering
        self.column_var = ctk.StringVar()
        self.column_combo = ctk.CTkComboBox(
            filter_controls,
            variable=self.column_var,
            font=ctk.CTkFont(size=14),
            width=130,
            height=32,
            state="readonly"
        )
        self.column_combo.pack(side="left", padx=(0, 15), pady=12)
        
        # Clear all active filters button
        clear_btn = ctk.CTkButton(
            filter_controls,
            text="🗑️ Clear",
            command=self.clear_filters,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=32,
            width=80,
            fg_color=("#ffc107", "#ffc107"),
            hover_color=("#e0a800", "#e0a800"),
            text_color=("black", "black")
        )
        clear_btn.pack(side="right", padx=(0, 15), pady=12)
        
        # Data Statistics Display
        stats_section = self.create_section_frame(data_container, "📈 Statistics")
        
        # Statistics information display area
        self.stats_text = ctk.CTkTextbox(
            stats_section,
            height=100,
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.stats_text.pack(fill="x", padx=15, pady=12)
        
        # Main Data Table Interface
        table_section = self.create_section_frame(data_container, "📋 Data Table")
        
        # Table container with enhanced scrollbars
        table_container = ctk.CTkFrame(table_section)
        table_container.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Import required GUI components
        import tkinter as tk
        from tkinter import ttk
        
        # Create treeview container with grid layout for scrollbars
        tree_frame = tk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True)
        
        # Configure grid layout for proper scrollbar positioning
        tree_frame.grid_columnconfigure(0, weight=1)  # Main table area
        tree_frame.grid_rowconfigure(0, weight=1)    # Main table area
        
        # Create main data table (Treeview)
        self.tree = ttk.Treeview(tree_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Vertical Scrollbar for row navigation
        v_scrollbar = ctk.CTkScrollbar(
            tree_frame, 
            orientation="vertical", 
            command=self.tree.yview,
            fg_color=self.colors['bg_secondary'],
            button_color=self.colors['secondary'],
            button_hover_color=self.colors['primary'],
            width=12
        )
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Horizontal Scrollbar for column navigation
        h_scrollbar = ctk.CTkScrollbar(
            tree_frame, 
            orientation="horizontal", 
            command=self.tree.xview,
            fg_color=self.colors['bg_secondary'],
            button_color=self.colors['secondary'],
            button_hover_color=self.colors['primary'],
            height=12
        )
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Apply custom styling to match application theme
        style = ttk.Style()
        style.theme_use("clam")  # Use clam theme for better customization
        
        # Main table styling (rows and cells)
        style.configure(
            "Treeview",
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            fieldbackground=self.colors['bg_secondary'],
            borderwidth=0,
            rowheight=25
        )
        
        # Table header styling
        style.configure(
            "Treeview.Heading",
            background=self.colors['primary'],
            foreground=self.colors['text_primary'],
            relief="flat",
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        
        # Row selection highlighting
        style.map(
            "Treeview",
            background=[("selected", self.colors['wuzzuf_primary'])],
            foreground=[("selected", self.colors['white'])]
        )
        
        # Mouse wheel scrolling support (cross-platform)
        self.tree.bind("<MouseWheel>", self.on_mousewheel)      # Windows/Mac
        self.tree.bind("<Button-4>", self.on_mousewheel)        # Linux scroll up
        self.tree.bind("<Button-5>", self.on_mousewheel)        # Linux scroll down
        
        # Keyboard shortcuts for enhanced navigation
        self.tree.bind("<Control-a>", self.select_all_rows)     # Select all rows
        self.tree.bind("<Control-f>", lambda e: self.search_entry.focus())  # Focus search
        

        
        # Export section
        export_section = self.create_section_frame(data_container, "💾 Export Data")
        
        export_buttons = ctk.CTkFrame(export_section)
        export_buttons.pack(fill="x", padx=15, pady=12)
        
        export_filtered_btn = ctk.CTkButton(
            export_buttons,
            text="📤 Export Filtered",
            command=self.export_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36,
            fg_color=("#28a745", "#28a745"),
            hover_color=("#218838", "#218838")
        )
        export_filtered_btn.pack(side="left", padx=(0, 12))
        
        export_all_btn = ctk.CTkButton(
            export_buttons,
            text="📤 Export All",
            command=self.export_all_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36
        )

    
    def create_section_frame(self, parent, title):
        """Create a styled section frame with title and better contrast"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", pady=(0, 25))
        
        # Section title with enhanced styling
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['wuzzuf_primary']
        )
        title_label.pack(anchor="w", pady=(0, 12))
        
        # Add a subtle separator line
        separator = ctk.CTkFrame(
            section, 
            height=2, 
            fg_color=self.colors['primary']
        )
        separator.pack(fill="x", pady=(0, 15))
        
        return section
    
    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.scraping_thread and self.scraping_thread.is_alive():
            messagebox.showwarning("Warning", "Scraping is already in progress!")
            return
        
        # Get scraping parameters
        keyword = self.keyword_var.get().strip()
        location = self.location_var.get().strip()
        max_pages = self.max_pages_var.get()
        
        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword!")
            return
        
        # Update UI with enhanced feedback
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Initializing scraper...")


        
        # Initialize scraping start time
        self.start_time = datetime.now()
        
        # Clear log
        self.log_text.delete("1.0", "end")
        self.log("🚀 Starting Wuzzuf job scraper...")
        self.log(f"🔍 Keyword: {keyword}")
        self.log(f"📍 Location: {location or 'All locations'}")
        self.log(f"📄 Max Pages: {max_pages}")

        self.log("-" * 50)
        
        # Show notification
        print("🚀 Scraping started! Monitor progress below.")
        
        # Start scraping in separate thread
        self.scraping_thread = threading.Thread(
            target=self.scraping_worker,
            args=(keyword, location, max_pages),
            daemon=True
        )
        self.scraping_thread.start()
    
    def scraping_worker(self, keyword, location, max_pages):
        """Worker function for scraping in separate thread"""
        try:
            # Initialize scraper
            self.scraper = SimpleWuzzufScraper(headless=False)
            
            # Store search parameters for potential saving when stopping
            self.scraper.current_keyword = keyword
            self.scraper.current_location = location
            self.scraper.current_max_pages = max_pages
            
            # Override print function to capture output
            original_print = print
            def log_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.scraping_queue.put(('log', message))
                original_print(*args, **kwargs)
            
            # Replace print function temporarily
            import builtins
            builtins.print = log_print
            
            # Start scraping
            self.scraper.search_jobs(
                keyword=keyword,
                location=location,
                max_pages=max_pages
            )
            
            # Restore print function
            builtins.print = original_print
            
            # Save data to files
            if self.scraper.jobs_data:
                # Save data using the scraper's save method (now returns session folder)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_prefix = f"wuzzuf_jobs_{keyword.replace(' ', '_')}"
                
                session_folder = self.scraper.save_data(filename_prefix)
                self.scraping_queue.put(('complete', (len(self.scraper.jobs_data), session_folder)))
            else:
                self.scraping_queue.put(('error', 'No data collected'))
                
        except Exception as e:
            self.scraping_queue.put(('error', str(e)))
    
    def stop_scraping(self):
        """Stop the scraping process"""
        if self.scraper:
            try:
                # Check if there's any data to save before stopping
                if hasattr(self.scraper, 'jobs_data') and self.scraper.jobs_data:
                    job_count = len(self.scraper.jobs_data)
                    
                    # Save the collected data
                    try:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        keyword = getattr(self.scraper, 'current_keyword', 'unknown')
                        filename_prefix = f"wuzzuf_jobs_{keyword.replace(' ', '_')}"
                        
                        session_folder = self.scraper.save_data(filename_prefix)
                        
                        self.log(f"💾 Saved {job_count} jobs before stopping to: {session_folder}")
                        
                        # Show stopped message with save info
                        messagebox.showinfo(
                            "⏹️ Scraping Stopped", 
                            f"Job scraping has been stopped by the user.\n\n"
                            f"✅ Saved {job_count} jobs collected before stopping!\n"
                            f"📁 Data saved to: {Path(session_folder).name}"
                        )
                        
                    except Exception as save_error:
                        self.log(f"⚠️ Warning: Could not save data before stopping: {save_error}")
                        
                        # Show stopped message without save info
                        messagebox.showinfo(
                            "⏹️ Scraping Stopped", 
                            f"Job scraping has been stopped by the user.\n\n"
                            f"⚠️ Could not save {job_count} collected jobs due to an error.\n"
                            f"Error: {save_error}"
                        )
                else:
                    self.log("⏹️ Scraping stopped - no data collected yet")
                    
                    # Show stopped message for no data
                    messagebox.showinfo(
                        "⏹️ Scraping Stopped", 
                        "Job scraping has been stopped by the user.\n\n"
                        "No data was collected yet, so nothing to save."
                    )
                
                # Now quit the driver
                self.scraper.driver.quit()
                self.log("⏹️ Scraping stopped by user")

                
            except Exception as e:
                self.log(f"⚠️ Error while stopping scraper: {e}")
                pass
        
        # Reset UI
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Scraping stopped")
    
    def monitor_scraping_queue(self):
        """Monitor the scraping queue for updates"""
        try:
            while True:
                message_type, data = self.scraping_queue.get_nowait()
                
                if message_type == 'log':
                    self.log(data)
                    
                    # Update progress based on log messages
                    if "Found" in data and "job cards" in data:
                        try:
                            # Extract number of jobs found from message like "Found 15 job cards"
                            import re
                            match = re.search(r'Found (\d+) job cards', data)
                            if match:
                                jobs_found = int(match.group(1))
                                # Update progress label to show current status
                                self.progress_label.configure(text=f"Found {jobs_found} jobs on current page...")
                        except:
                            pass
                    elif "📋" in data:
                        # Job extracted, update progress
                        try:
                            # Count total jobs collected so far
                            if hasattr(self, 'scraper') and hasattr(self.scraper, 'jobs_data'):
                                total_jobs = len(self.scraper.jobs_data)
                                self.progress_label.configure(text=f"Collected {total_jobs} jobs so far...")
                                
                                # Update progress bar (assuming max 100 jobs for now)
                                if total_jobs <= 100:
                                    progress = total_jobs / 100.0
                                    self.progress_bar.set(progress)
                        except:
                            pass
                elif message_type == 'complete':
                    # Handle new tuple format: (job_count, session_folder)
                    if isinstance(data, tuple):
                        job_count, session_folder = data
                    else:
                        # Handle old format for backward compatibility
                        job_count = data
                        session_folder = "."
                    
                    # Calculate elapsed time
                    end_time = datetime.now()
                    elapsed = end_time - self.start_time
                    elapsed_str = str(elapsed).split('.')[0]
                    
                    self.log(f"✅ Scraping completed! Collected {job_count} jobs in {elapsed_str}")
                    if session_folder != ".":
                        self.log(f"📁 Data saved to session folder: {session_folder}")
                    else:
                        self.log(f"💾 Data saved to CSV and JSON files")
                    
                    self.progress_bar.set(1.0)
                    self.progress_label.configure(text=f"Completed! {job_count} jobs saved in {elapsed_str}")
                    
                    # Update status with session folder info
                    if session_folder != ".":
                        session_name = Path(session_folder).name
                        pass  # Status update removed - status bar deleted
                    else:
                        pass  # Status update removed - status bar deleted
                    
                    # Show completion message box
                    messagebox.showinfo(
                        "🎉 Scraping Completed!", 
                        f"Successfully collected {job_count} job listings!\n\n"
                        f"Time taken: {elapsed_str}\n"
                        f"Data saved to: {session_name if session_folder != '.' else 'CSV and JSON files'}"
                    )
                    
                    # Reset UI
                    self.start_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
                    

                    
                    # Show success notification
                    if session_folder != ".":
                        print(f"✅ Scraping completed! {job_count} jobs saved to session folder in {elapsed_str}")
                    else:
                        print(f"✅ Scraping completed! {job_count} jobs saved to files in {elapsed_str}")
                    
                    # Try to load the scraped data
                    self.load_latest_scraped_data()
                    
                elif message_type == 'error':
                    self.log(f"❌ Error: {data}")
                    self.progress_label.configure(text="Error occurred")

                    
                    # Show error message box
                    messagebox.showerror(
                        "❌ Scraping Error", 
                        f"An error occurred during scraping:\n\n{data}\n\n"
                        "Please check your internet connection and try again."
                    )
                    
                    # Reset UI
                    self.start_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.monitor_scraping_queue)
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
    
    def load_latest_scraped_data(self):
        """Try to load the most recently scraped data file"""
        try:
            # Look for the most recent CSV file
            csv_files = [f for f in os.listdir('.') if f.startswith('wuzzuf_jobs_') and f.endswith('.csv')]
            if csv_files:
                # Sort by modification time (newest first)
                csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                latest_file = csv_files[0]
                self.file_path_var.set(latest_file)
                self.load_csv()
                self.log(f"📁 Auto-loaded latest scraped data: {latest_file}")
        except Exception as e:
            self.log(f"⚠️ Could not auto-load scraped data: {e}")
    
    def save_configuration(self):
        """Save the current configuration"""
        try:
            # Get fields from text area
            fields_text = self.fields_text.get("1.0", "end").strip()
            fields = [line.strip() for line in fields_text.split('\n') if line.strip()]
            
            # Create config dictionary
            config = {
                'search_keyword': self.keyword_var.get(),
                'location': self.location_var.get(),
                'max_pages': self.max_pages_var.get(),
                'engineering_fields': fields
            }
            
            # Save to file
            with open('gui_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_default_csv(self):
        """Try to load the default Wuzzuf CSV file if it exists"""
        default_files = [
            'wuzzuf_jobs_20250826_032819.csv',
            'wuzzuf_jobs_*.csv'
        ]
        
        for pattern in default_files:
            if '*' in pattern:
                import glob
                files = glob.glob(pattern)
                if files:
                    self.file_path_var.set(files[0])
                    self.load_csv()
                    break
            elif os.path.exists(pattern):
                self.file_path_var.set(pattern)
                self.load_csv()
                break
    
    def browse_file(self):
        """Open file dialog to select CSV file"""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            self.load_csv()
    
    def load_csv(self):
        """Load CSV file and display data"""
        try:
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a CSV file")
                return
            
            self.df = pd.read_csv(file_path)
            self.filtered_df = self.df.copy()
            
            # Update column selector
            columns = list(self.df.columns)
            self.column_combo.configure(values=columns)
            if columns:
                self.column_combo.set(columns[0])
            
            # Display data
            self.display_data()
            self.update_statistics()
            

            print(f"✅ Successfully loaded {len(self.df)} job records")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")

            print("❌ Failed to load CSV file")
    
    def display_data(self):
        """Display data in the treeview with enhanced scrolling"""
        if self.filtered_df is None:
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configure columns
        columns = list(self.filtered_df.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Set column headings with better formatting
        for col in columns:
            # Clean column name for display
            display_name = col.replace('_', ' ').title()
            self.tree.heading(col, text=display_name)
            
            # Calculate optimal column width based on content
            col_width = len(display_name) * 12  # Base width for header
            
            # Check data content width
            if len(self.filtered_df) > 0:
                data_width = self.filtered_df[col].astype(str).str.len().max() * 10
                col_width = max(col_width, data_width)
            
            # Set reasonable bounds for column width
            col_width = max(100, min(col_width, 400))
            self.tree.column(col, width=col_width, minwidth=80)
        
        # Insert data rows with alternating row colors
        for idx, row in self.filtered_df.head(2000).iterrows():  # Increased limit for better data viewing
            values = []
            for val in row:
                if pd.isna(val):
                    values.append('')
                elif isinstance(val, list):
                    # Handle list values (like skills) - show first few items
                    if val:
                        display_val = ', '.join(str(item) for item in val[:3])
                        if len(val) > 3:
                            display_val += f' (+{len(val)-3} more)'
                        values.append(display_val)
                    else:
                        values.append('')
                else:
                    # Truncate long text values
                    str_val = str(val)
                    if len(str_val) > 100:
                        str_val = str_val[:97] + '...'
                    values.append(str_val)
            
            # Insert row with alternating colors
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure alternating row colors
        self.tree.tag_configure('evenrow', background=self.colors['bg_secondary'])
        self.tree.tag_configure('oddrow', background=self.colors['bg_primary'])
        
        # Update scrollbar ranges
        self.tree.yview_moveto(0)  # Reset to top
        self.tree.xview_moveto(0)  # Reset to left
        
        # Show data summary
        total_rows = len(self.filtered_df)
        displayed_rows = min(total_rows, 2000)
        if total_rows > displayed_rows:
            print(f"📊 Displaying {displayed_rows} of {total_rows} rows (use scrollbars to view more)")
        else:
            print(f"📊 Displaying all {total_rows} rows")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling for the treeview"""
        try:
            if event.num == 4:  # Linux scroll up
                self.tree.yview_scroll(-1, "units")
            elif event.num == 5:  # Linux scroll down
                self.tree.yview_scroll(1, "units")
            else:  # Windows/Mac scroll
                self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            # Fallback for different platforms
            try:
                self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass
    
    def select_all_rows(self, event=None):
        """Select all rows in the treeview"""
        try:
            for item in self.tree.get_children():
                self.tree.selection_add(item)
        except:
            pass
    
    def show_table_tooltip(self, event=None):
        """Show tooltip for table navigation"""
        try:
            # Create tooltip window
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            # Tooltip content
            tooltip_label = tk.Label(
                tooltip, 
                text="💡 Tip: Use mouse wheel to scroll, Ctrl+A to select all",
                background=self.colors['primary'],
                foreground=self.colors['white'],
                relief="solid",
                borderwidth=1,
                font=("Arial", 9)
            )
            tooltip_label.pack()
            
            # Auto-hide after 3 seconds
            tooltip.after(3000, tooltip.destroy)
            
        except:
            pass
    
    def hide_table_tooltip(self, event=None):
        """Hide table tooltip"""
        pass  # Tooltip auto-hides
    
    def filter_data(self, event=None):
        """Filter data based on search term"""
        if self.df is None:
            return
        
        search_term = self.search_var.get().lower()
        column = self.column_var.get()
        
        if not search_term:
            self.filtered_df = self.df.copy()
        else:
            if column and column in self.df.columns:
                # Filter by specific column
                mask = self.df[column].astype(str).str.lower().str.contains(search_term, na=False)
                self.filtered_df = self.df[mask]
            else:
                # Search across all columns
                mask = self.df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)
                self.filtered_df = self.df[mask]
        
        self.display_data()
        self.update_statistics()
        
    
    def clear_filters(self):
        """Clear all filters and show original data"""
        self.search_var.set('')
        if self.df is not None:
            self.filtered_df = self.df.copy()
            self.display_data()
            self.update_statistics()

    
    def update_statistics(self):
        """Update statistics display"""
        if self.filtered_df is None:
            self.stats_text.delete("1.0", "end")
            return
        
        stats_text = f"📊 Total Rows: {len(self.filtered_df)}\n"
        stats_text += f"📋 Columns: {len(self.filtered_df.columns)}\n"
        
        # Show some sample data types
        dtypes = self.filtered_df.dtypes.head(5)
        stats_text += f"🔧 Data Types: {dict(dtypes)}\n"
        
        # Show memory usage
        memory_usage = self.filtered_df.memory_usage(deep=True).sum()
        stats_text += f"💾 Memory Usage: {memory_usage / 1024:.2f} KB"
        
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", stats_text)
    
    def export_data(self):
        """Export filtered data to CSV"""
        if self.filtered_df is None:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Filtered Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.filtered_df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Data exported to {filename}")
    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_all_data(self):
        """Export all data to CSV"""
        if self.df is None:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export All Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"All data exported to {filename}")
    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
        
        # Basic statistics
        total_jobs = len(self.df)
        insights.append(f"📊 Dataset contains {total_jobs} job listings")
        
        # Top company
        if 'company' in self.df.columns:
            top_company = self.df['company'].value_counts().index[0]
            top_count = self.df['company'].value_counts().iloc[0]
            insights.append(f"🏢 Top hiring company: {top_company} ({top_count} jobs)")
        
        # Most common location
        if 'location' in self.df.columns:
            top_location = self.df['location'].value_counts().index[0]
            location_count = self.df['location'].value_counts().iloc[0]
            insights.append(f"📍 Most active location: {top_location} ({location_count} jobs)")
        
        # Experience level insights
        if 'experience_level' in self.df.columns:
            exp_mode = self.df['experience_level'].mode()
            if not exp_mode.empty:
                insights.append(f"💼 Most common experience level: {exp_mode.iloc[0]}")
        
        # Skills analysis
        if 'skills' in self.df.columns:
            all_skills = []
            for skills in self.df['skills'].dropna():
                if isinstance(skills, str) and skills:
                    if skills.startswith('[') and skills.endswith(']'):
                        skills = skills.strip('[]').replace("'", "").replace('"', '')
                    skill_list = [s.strip() for s in skills.split(',') if s.strip()]
                    all_skills.extend(skill_list)
            
            if all_skills:
                top_skill = pd.Series(all_skills).value_counts().index[0]
                skill_count = pd.Series(all_skills).value_counts().iloc[0]
                insights.append(f"🔧 Most demanded skill: {top_skill} ({skill_count} mentions)")
        
        # Job type distribution
        if 'job_type' in self.df.columns:
            job_type_mode = self.df['job_type'].mode()
            if not job_type_mode.empty:
                insights.append(f"💼 Most common job type: {job_type_mode.iloc[0]}")
        
        # Recent postings
        if 'posting_date' in self.df.columns:
            recent_jobs = self.df[self.df['posting_date'].str.contains('day|hour', na=False, case=False)]
            if not recent_jobs.empty:
                insights.append(f"🕒 {len(recent_jobs)} jobs posted recently (within days/hours)")
        
        # Market insights
        insights.append(f"\n🔍 Market Analysis:")
        insights.append(f"• Average jobs per company: {total_jobs / self.df['company'].nunique():.1f}")
        insights.append(f"• Geographic diversity: {self.df['location'].nunique()} unique locations")
        insights.append(f"• Skill diversity: Extracting from {self.df['skills'].notna().sum()} job descriptions")
        
        insights_text = "\n".join(insights)
        
        self.insights_text.configure(state="normal")
        self.insights_text.delete("1.0", "end")
        self.insights_text.insert("1.0", insights_text)
        self.insights_text.configure(state="disabled")
    

    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main application entry point"""
    try:
        print("🚀 Launching Wuzzuf Job Scraper Pro...")
        app = WuzzufScraperGUI()
        app.run()
    except ImportError as e:
        print(f"❌ Error: Could not import required modules: {e}")
        print("💡 Please install required dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Please check your installation and try again")

if __name__ == "__main__":
    main()
