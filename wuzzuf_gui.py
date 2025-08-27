import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import os
from pathlib import Path
import threading
import queue
from datetime import datetime
import json
import csv
import time
import tkinter as tk
from tkinter import ttk

# Optional imports for enhanced features
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available - some image features may be limited")

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available - chart features will be disabled")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("Seaborn not available - using matplotlib styling only")

# Import the scraper
from simple_wuzzuf_scraper import SimpleWuzzufScraper

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class WuzzufScraperGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🚀 Wuzzuf Job Scraper Pro - Advanced Edition")
        self.root.geometry("1700x1100")
        self.root.minsize(1400, 900)
        
        # Set window icon and style
        self.root.after(0, lambda: self.root.iconbitmap(""))  # Remove default icon
        
        # Enhanced color scheme with better contrast
        self.colors = {
            'primary': "#0d7377",        # Teal primary
            'secondary': "#14a085",      # Lighter teal
            'success': "#2dd4bf",        # Bright teal success
            'warning': "#f59e0b",        # Amber warning
            'danger': "#ef4444",         # Red danger
            'info': "#3b82f6",           # Blue info
            'dark': "#1f2937",           # Dark gray
            'light': "#f9fafb",          # Light gray
            'accent': "#8b5cf6",         # Purple accent
            'text_primary': "#ffffff",   # White text
            'text_secondary': "#d1d5db", # Light gray text
            'text_muted': "#9ca3af",     # Muted gray text
            'bg_primary': "#111827",     # Dark background
            'bg_secondary': "#374151",   # Secondary background
            'bg_tertiary': "#4b5563"     # Tertiary background
        }
        
        # Animation variables
        self.animation_running = False
        self.notification_queue = queue.Queue()
        
        # Scraper instance
        self.scraper = None
        self.scraping_thread = None
        self.scraping_queue = queue.Queue()
        
        # Data storage
        self.df = None
        self.filtered_df = None
        self.scraping_stats = {
            'total_jobs': 0,
            'pages_scraped': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize animations and effects
        self.setup_animations()
        
        # Try to load default CSV if it exists
        self.load_default_csv()
        
        # Start monitoring queues
        self.monitor_scraping_queue()
        self.monitor_notifications()
    
    def create_widgets(self):
        # Create main scrollable frame
        self.main_scrollable_frame = ctk.CTkScrollableFrame(
            self.root, 
            fg_color="transparent",
            scrollbar_button_color=self.colors['secondary'],
            scrollbar_button_hover_color=self.colors['primary']
        )
        self.main_scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Main container inside scrollable frame
        main_container = self.main_scrollable_frame
        
        # Enhanced header section with better contrast
        header_frame = ctk.CTkFrame(
            main_container, 
            height=140, 
            corner_radius=15,
            fg_color=self.colors['bg_secondary'],
            border_width=2,
            border_color=self.colors['primary']
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header content frame
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Left side - Title and subtitle
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            title_frame, 
            text="🚀 Wuzzuf Job Scraper Pro", 
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=self.colors['success']
        )
        self.title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Advanced job scraping and data analysis platform",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(8, 0))
        
        # Right side - Quick stats with enhanced styling
        self.stats_frame = ctk.CTkFrame(
            header_content, 
            width=320, 
            corner_radius=12,
            fg_color=self.colors['bg_tertiary'],
            border_width=1,
            border_color=self.colors['secondary']
        )
        self.stats_frame.pack(side="right", fill="y", padx=(25, 0))
        self.stats_frame.pack_propagate(False)
        
        stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Quick Stats",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        stats_title.pack(pady=(15, 8))
        
        self.quick_stats_text = ctk.CTkLabel(
            self.stats_frame,
            text="Ready to start scraping\nNo data loaded yet",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary'],
            justify="center"
        )
        self.quick_stats_text.pack(pady=(0, 15))
        
        # Create enhanced tabview with better styling
        self.tabview = ctk.CTkTabview(
            main_container, 
            corner_radius=15, 
            height=900,
            fg_color=self.colors['bg_secondary'],
            segmented_button_fg_color=self.colors['bg_tertiary'],
            segmented_button_selected_color=self.colors['primary'],
            segmented_button_selected_hover_color=self.colors['secondary'],
            text_color=self.colors['text_primary'],
            text_color_disabled=self.colors['text_muted']
        )
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create tabs with better organization
        self.create_scraping_tab()
        self.create_data_viewer_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
        # Enhanced status bar with notifications
        self.create_enhanced_status_bar(main_container)
    
    def create_scraping_tab(self):
        """Create the scraping configuration and control tab"""
        scraping_frame = self.tabview.add("🔍 Scraping")
        
        # Scraping configuration section
        config_section = self.create_section_frame(scraping_frame, "⚙️ Scraping Configuration")
        
        # Search settings with enhanced styling
        search_frame = ctk.CTkFrame(
            config_section,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['secondary']
        )
        search_frame.pack(fill="x", padx=15, pady=15)
        
        # Keyword input
        keyword_label = ctk.CTkLabel(
            search_frame,
            text="Search Keyword:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        keyword_label.pack(anchor="w", padx=(15, 10), pady=(15, 5))
        
        self.keyword_var = ctk.StringVar(value="software engineering")
        keyword_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.keyword_var,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Enter search keyword..."
        )
        keyword_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Location input
        location_label = ctk.CTkLabel(
            search_frame,
            text="Location (optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        location_label.pack(anchor="w", padx=(15, 10), pady=(15, 5))
        
        self.location_var = ctk.StringVar()
        location_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.location_var,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Enter location (optional)..."
        )
        location_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Advanced settings
        advanced_frame = ctk.CTkFrame(search_frame)
        advanced_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Max pages
        pages_label = ctk.CTkLabel(
            advanced_frame,
            text="Max Pages:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        pages_label.pack(side="left", padx=(0, 10))
        
        self.max_pages_var = ctk.IntVar(value=3)
        pages_spinbox = ctk.CTkEntry(
            advanced_frame,
            textvariable=self.max_pages_var,
            font=ctk.CTkFont(size=14),
            width=100,
            height=35
        )
        pages_spinbox.pack(side="left", padx=(0, 20))
        
        # Headless mode
        self.headless_var = ctk.BooleanVar(value=False)
        headless_check = ctk.CTkCheckBox(
            advanced_frame,
            text="Headless Mode",
            variable=self.headless_var,
            font=ctk.CTkFont(size=14),
            checkbox_width=20,
            checkbox_height=20
        )
        headless_check.pack(side="left")
        
        # Scraping control section
        control_section = self.create_section_frame(scraping_frame, "🎮 Scraping Control")
        
        control_frame = ctk.CTkFrame(control_section)
        control_frame.pack(fill="x", padx=15, pady=15)
        
        # Start button with enhanced styling
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="🚀 Start Scraping",
            command=self.start_scraping,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            width=180,
            corner_radius=12,
            fg_color=self.colors['success'],
            hover_color=self.colors['secondary'],
            border_width=2,
            border_color=self.colors['primary'],
            text_color=self.colors['text_primary']
        )
        self.start_btn.pack(side="left", padx=(20, 15))
        
        # Stop button with enhanced styling
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Stop Scraping",
            command=self.stop_scraping,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            width=180,
            corner_radius=12,
            fg_color=self.colors['danger'],
            hover_color=("#dc2626", "#dc2626"),
            border_width=2,
            border_color=("#b91c1c", "#b91c1c"),
            text_color=self.colors['text_primary'],
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 20))
        
        # Progress section
        progress_section = self.create_section_frame(scraping_frame, "📊 Scraping Progress")
        
        progress_frame = ctk.CTkFrame(progress_section)
        progress_frame.pack(fill="x", padx=15, pady=15)
        
        # Progress bar
        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            variable=self.progress_var,
            height=20
        )
        self.progress_bar.pack(fill="x", padx=15, pady=(15, 10))
        self.progress_bar.set(0)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to start scraping",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        self.progress_label.pack(pady=(0, 15))
        
        # Log section
        log_section = self.create_section_frame(scraping_frame, "📝 Scraping Log")
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            log_section,
            height=300,
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=15)
    
    def create_data_viewer_tab(self):
        """Create the data viewing and analysis tab"""
        viewer_frame = self.tabview.add("📊 Data Viewer")
        
        # File selection section
        file_section = self.create_section_frame(viewer_frame, "📁 File Selection")
        
        file_input_frame = ctk.CTkFrame(file_section)
        file_input_frame.pack(fill="x", padx=15, pady=15)
        
        self.file_path_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(
            file_input_frame,
            textvariable=self.file_path_var,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Select CSV file..."
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=15)
        
        browse_btn = ctk.CTkButton(
            file_input_frame,
            text="🔍 Browse",
            command=self.browse_file,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=100
        )
        browse_btn.pack(side="right", padx=(0, 15), pady=15)
        
        load_btn = ctk.CTkButton(
            file_input_frame,
            text="📥 Load",
            command=self.load_csv,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=100,
            fg_color=("#28a745", "#28a745"),
            hover_color=("#218838", "#218838")
        )
        load_btn.pack(side="right", padx=(0, 10), pady=15)
        
        # Search and filter section
        filter_section = self.create_section_frame(viewer_frame, "🔍 Search & Filter")
        
        filter_controls = ctk.CTkFrame(filter_section)
        filter_controls.pack(fill="x", padx=15, pady=15)
        
        # Search input
        search_label = ctk.CTkLabel(
            filter_controls,
            text="Search:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(side="left", padx=(15, 10), pady=15)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_controls,
            textvariable=self.search_var,
            font=ctk.CTkFont(size=14),
            height=35,
            width=200,
            placeholder_text="Enter search term..."
        )
        self.search_entry.pack(side="left", padx=(0, 20), pady=15)
        self.search_entry.bind('<KeyRelease>', self.filter_data)
        
        # Column selector
        column_label = ctk.CTkLabel(
            filter_controls,
            text="Column:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        column_label.pack(side="left", padx=(0, 10), pady=15)
        
        self.column_var = ctk.StringVar()
        self.column_combo = ctk.CTkComboBox(
            filter_controls,
            variable=self.column_var,
            font=ctk.CTkFont(size=14),
            width=150,
            height=35,
            state="readonly"
        )
        self.column_combo.pack(side="left", padx=(0, 20), pady=15)
        
        # Clear filters button
        clear_btn = ctk.CTkButton(
            filter_controls,
            text="🗑️ Clear",
            command=self.clear_filters,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            width=100,
            fg_color=("#ffc107", "#ffc107"),
            hover_color=("#e0a800", "#e0a800"),
            text_color=("black", "black")
        )
        clear_btn.pack(side="right", padx=(0, 15), pady=15)
        
        # Statistics section
        stats_section = self.create_section_frame(viewer_frame, "📈 Statistics")
        
        self.stats_text = ctk.CTkTextbox(
            stats_section,
            height=120,
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.stats_text.pack(fill="x", padx=15, pady=15)
        
        # Data table section
        table_section = self.create_section_frame(viewer_frame, "📋 Data Table")
        
        # Table container with scrollbars
        table_container = ctk.CTkFrame(table_section)
        table_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create Treeview with custom style
        import tkinter as tk
        from tkinter import ttk
        
        # Create a frame for the treeview
        tree_frame = tk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Export section
        export_section = self.create_section_frame(viewer_frame, "💾 Export Data")
        
        export_buttons = ctk.CTkFrame(export_section)
        export_buttons.pack(fill="x", padx=15, pady=15)
        
        export_filtered_btn = ctk.CTkButton(
            export_buttons,
            text="📤 Export Filtered",
            command=self.export_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=("#28a745", "#28a745"),
            hover_color=("#218838", "#218838")
        )
        export_filtered_btn.pack(side="left", padx=(0, 15))
        
        export_all_btn = ctk.CTkButton(
            export_buttons,
            text="📤 Export All",
            command=self.export_all_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        export_all_btn.pack(side="left")
    
    def create_analytics_tab(self):
        """Create the data analytics and visualization tab"""
        analytics_frame = self.tabview.add("📈 Analytics")
        
        # Analytics controls section
        controls_section = self.create_section_frame(analytics_frame, "🎛️ Analytics Controls")
        
        controls_frame = ctk.CTkFrame(controls_section)
        controls_frame.pack(fill="x", padx=15, pady=15)
        
        # Chart type selector
        chart_label = ctk.CTkLabel(
            controls_frame,
            text="Chart Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        chart_label.pack(side="left", padx=(15, 10), pady=15)
        
        self.chart_type_var = ctk.StringVar(value="Job Count by Company")
        chart_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.chart_type_var,
            values=["Job Count by Company", "Experience Level Distribution", 
                   "Skills Frequency", "Location Analysis", "Job Type Distribution"],
            font=ctk.CTkFont(size=14),
            width=200,
            height=35,
            state="readonly"
        )
        chart_combo.pack(side="left", padx=(0, 20), pady=15)
        
        # Generate chart button
        self.generate_btn = ctk.CTkButton(
            controls_frame,
            text="📊 Generate Chart" if MATPLOTLIB_AVAILABLE else "📊 Install Matplotlib",
            command=self.generate_chart if MATPLOTLIB_AVAILABLE else self.show_matplotlib_info,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            fg_color=self.colors['info'] if MATPLOTLIB_AVAILABLE else self.colors['warning'],
            hover_color=self.colors['secondary'] if MATPLOTLIB_AVAILABLE else self.colors['danger']
        )
        self.generate_btn.pack(side="left", padx=(0, 15), pady=15)
        
        # Export chart button
        export_chart_btn = ctk.CTkButton(
            controls_frame,
            text="💾 Export Chart",
            command=self.export_chart,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            fg_color=self.colors['success'],
            hover_color=("#218838", "#218838")
        )
        export_chart_btn.pack(side="right", padx=(0, 15), pady=15)
        
        # Chart display section
        chart_section = self.create_section_frame(analytics_frame, "📊 Visualization")
        
        # Chart container
        self.chart_container = ctk.CTkFrame(chart_section)
        self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Initial message
        if MATPLOTLIB_AVAILABLE:
            chart_text = ("📊 Load data and select a chart type to begin analysis\n\n"
                         "Available visualizations:\n"
                         "• Job distribution by companies\n"
                         "• Experience level requirements\n"
                         "• Most demanded skills\n"
                         "• Geographic job distribution\n"
                         "• Employment type breakdown")
        else:
            chart_text = ("📊 Data Visualization Available\n\n"
                         "To enable chart generation, install matplotlib:\n"
                         "pip install matplotlib seaborn pillow\n\n"
                         "This will unlock:\n"
                         "• Interactive charts and graphs\n"
                         "• Data visualization tools\n"
                         "• Chart export functionality\n"
                         "• Enhanced analytics features")
        
        self.chart_message = ctk.CTkLabel(
            self.chart_container,
            text=chart_text,
            font=ctk.CTkFont(size=16),
            text_color=("gray60", "gray80"),
            justify="center"
        )
        self.chart_message.pack(expand=True, pady=50)
        
        # Insights section
        insights_section = self.create_section_frame(analytics_frame, "🔍 Data Insights")
        
        self.insights_text = ctk.CTkTextbox(
            insights_section,
            height=150,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.insights_text.pack(fill="x", padx=15, pady=15)
        
        # Initial insights text
        initial_insights = """
🔍 Data Insights will appear here after loading data:

• Market trends and patterns
• Skill demand analysis  
• Salary range insights
• Company hiring patterns
• Location-based opportunities

Load your scraped data to see detailed analytics and insights!
        """
        self.insights_text.insert("1.0", initial_insights.strip())
        self.insights_text.configure(state="disabled")
    
    def create_settings_tab(self):
        """Create the settings and configuration tab"""
        settings_frame = self.tabview.add("⚙️ Settings")
        
        # Configuration section
        config_section = self.create_section_frame(settings_frame, "🔧 Configuration")
        
        config_frame = ctk.CTkFrame(config_section)
        config_frame.pack(fill="x", padx=15, pady=15)
        
        # Engineering fields
        fields_label = ctk.CTkLabel(
            config_frame,
            text="Engineering Fields (one per line):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        fields_label.pack(anchor="w", padx=(15, 10), pady=(15, 5))
        
        self.fields_text = ctk.CTkTextbox(
            config_frame,
            height=200,
            font=ctk.CTkFont(size=14)
        )
        self.fields_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # Load default fields
        default_fields = [
            "software engineering",
            "mechanical engineering",
            "civil engineering",
            "electrical engineering",
            "data engineering",
            "AI engineering",
            "robotics engineering"
        ]
        self.fields_text.insert("1.0", '\n'.join(default_fields))
        
        # Save config button
        save_config_btn = ctk.CTkButton(
            config_frame,
            text="💾 Save Configuration",
            command=self.save_configuration,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=("#28a745", "#28a745"),
            hover_color=("#218838", "#218838")
        )
        save_config_btn.pack(anchor="w", padx=15, pady=(0, 15))
        
        # About section
        about_section = self.create_section_frame(settings_frame, "ℹ️ About")
        
        about_text = ctk.CTkTextbox(
            about_section,
            height=250,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        about_text.pack(fill="x", padx=15, pady=15)
        
        about_content = """
Wuzzuf Job Scraper Pro v2.0

A professional tool for scraping job listings from Wuzzuf.net

Features:
• Automated job scraping with configurable parameters
• Real-time progress monitoring and logging
• Advanced data filtering and search capabilities
• Export functionality (CSV/JSON)
• Modern, intuitive user interface
• Multi-threaded scraping for better performance

Built with Python, Selenium, and CustomTkinter
        """
        about_text.insert("1.0", about_content.strip())
        about_text.configure(state="disabled")
    
    def create_section_frame(self, parent, title):
        """Create a styled section frame with title and better contrast"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", pady=(0, 25))
        
        # Section title with enhanced styling
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['success']
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
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ctk.CTkFrame(parent, height=40)
        status_frame.pack(fill="x", pady=(20, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = ctk.StringVar()
        self.status_var.set("🚀 Ready to start scraping")
        status_bar = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        status_bar.pack(fill="x", padx=15, pady=10)
    
    def create_enhanced_status_bar(self, parent):
        """Create enhanced status bar with notifications and better contrast"""
        status_container = ctk.CTkFrame(
            parent, 
            height=70, 
            corner_radius=15,
            fg_color=self.colors['bg_secondary'],
            border_width=2,
            border_color=self.colors['primary']
        )
        status_container.pack(fill="x", pady=(25, 0))
        status_container.pack_propagate(False)
        
        # Status content frame
        status_content = ctk.CTkFrame(status_container, fg_color="transparent")
        status_content.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Left side - Status text
        status_left = ctk.CTkFrame(status_content, fg_color="transparent")
        status_left.pack(side="left", fill="both", expand=True)
        
        self.status_var = ctk.StringVar()
        self.status_var.set("🚀 Ready to start scraping")
        self.status_label = ctk.CTkLabel(
            status_left,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)
        
        # Right side - Real-time info
        status_right = ctk.CTkFrame(status_content, fg_color="transparent")
        status_right.pack(side="right")
        
        # Live clock with enhanced styling
        self.clock_label = ctk.CTkLabel(
            status_right,
            text=datetime.now().strftime("%H:%M:%S"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['secondary']
        )
        self.clock_label.pack(side="right", padx=(25, 0))
        
        # Update clock
        self.update_clock()
        
        # Notification area (hidden by default)
        self.notification_frame = ctk.CTkFrame(
            parent, 
            height=50, 
            corner_radius=10,
            fg_color=self.colors['success']
        )
        # Don't pack initially - will be shown for notifications
        
        self.notification_label = ctk.CTkLabel(
            self.notification_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        self.notification_label.pack(expand=True)
    
    def setup_animations(self):
        """Initialize animations and effects"""
        # Title animation
        self.animate_title()
        
        # Breathing effect for progress bar
        self.breathing_effect()
    
    def animate_title(self):
        """Animate the title with enhanced color transitions"""
        if hasattr(self, 'title_label'):
            colors = [
                self.colors['success'], 
                self.colors['primary'], 
                self.colors['secondary'], 
                self.colors['info'], 
                self.colors['accent']
            ]
            current_color = getattr(self, '_title_color_index', 0)
            
            self.title_label.configure(text_color=colors[current_color])
            self._title_color_index = (current_color + 1) % len(colors)
            
            # Schedule next animation (slower for better visibility)
            self.root.after(4000, self.animate_title)
    
    def breathing_effect(self):
        """Create breathing effect for progress bar"""
        if hasattr(self, 'progress_bar') and self.animation_running:
            # Simulate breathing by slightly changing opacity
            pass  # CustomTkinter doesn't support opacity changes directly
        
        self.root.after(500, self.breathing_effect)
    
    def show_notification(self, message, notification_type="info", duration=3000):
        """Show animated notification"""
        colors = {
            "success": self.colors['success'],
            "warning": self.colors['warning'], 
            "error": self.colors['danger'],
            "info": self.colors['info']
        }
        
        self.notification_frame.configure(fg_color=colors.get(notification_type, self.colors['info']))
        self.notification_label.configure(text=message)
        
        # Slide in animation
        self.notification_frame.pack(fill="x", pady=(10, 0))
        
        # Auto-hide after duration
        self.root.after(duration, self.hide_notification)
    
    def hide_notification(self):
        """Hide notification with animation"""
        self.notification_frame.pack_forget()
    
    def update_clock(self):
        """Update the live clock"""
        if hasattr(self, 'clock_label'):
            current_time = datetime.now().strftime("%H:%M:%S")
            self.clock_label.configure(text=current_time)
        
        self.root.after(1000, self.update_clock)
    
    def update_quick_stats(self):
        """Update the quick stats display"""
        if self.df is not None:
            total_jobs = len(self.df)
            filtered_jobs = len(self.filtered_df) if self.filtered_df is not None else total_jobs
            
            stats_text = f"📊 {total_jobs} total jobs\n🔍 {filtered_jobs} filtered"
            
            if self.scraping_stats['start_time']:
                elapsed = datetime.now() - self.scraping_stats['start_time']
                stats_text += f"\n⏱️ {str(elapsed).split('.')[0]}"
        else:
            stats_text = "Ready to start scraping\nNo data loaded yet"
        
        if hasattr(self, 'quick_stats_text'):
            self.quick_stats_text.configure(text=stats_text)
    
    def monitor_notifications(self):
        """Monitor notification queue"""
        try:
            while True:
                message, msg_type = self.notification_queue.get_nowait()
                self.show_notification(message, msg_type)
        except queue.Empty:
            pass
        
        self.root.after(100, self.monitor_notifications)
    
    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.scraping_thread and self.scraping_thread.is_alive():
            messagebox.showwarning("Warning", "Scraping is already in progress!")
            return
        
        # Get scraping parameters
        keyword = self.keyword_var.get().strip()
        location = self.location_var.get().strip()
        max_pages = self.max_pages_var.get()
        headless = self.headless_var.get()
        
        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword!")
            return
        
        # Update UI with enhanced feedback
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Initializing scraper...")
        self.status_var.set("🔄 Starting scraper...")
        self.animation_running = True
        
        # Update scraping stats
        self.scraping_stats['start_time'] = datetime.now()
        self.scraping_stats['total_jobs'] = 0
        self.scraping_stats['pages_scraped'] = 0
        
        # Clear log
        self.log_text.delete("1.0", "end")
        self.log("🚀 Starting Wuzzuf job scraper...")
        self.log(f"🔍 Keyword: {keyword}")
        self.log(f"📍 Location: {location or 'All locations'}")
        self.log(f"📄 Max Pages: {max_pages}")
        self.log(f"👻 Headless: {'Yes' if headless else 'No'}")
        self.log("-" * 50)
        
        # Show notification
        self.show_notification("Scraping started! Monitor progress below.", "info")
        
        # Start scraping in separate thread
        self.scraping_thread = threading.Thread(
            target=self.scraping_worker,
            args=(keyword, location, max_pages, headless),
            daemon=True
        )
        self.scraping_thread.start()
    
    def scraping_worker(self, keyword, location, max_pages, headless):
        """Worker function for scraping in separate thread"""
        try:
            # Initialize scraper
            self.scraper = SimpleWuzzufScraper(headless=headless)
            
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
                self.scraper.driver.quit()
                self.log("⏹️ Scraping stopped by user")
                self.status_var.set("⏹️ Scraping stopped")
            except:
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
                elif message_type == 'complete':
                    # Handle new tuple format: (job_count, session_folder)
                    if isinstance(data, tuple):
                        job_count, session_folder = data
                    else:
                        # Handle old format for backward compatibility
                        job_count = data
                        session_folder = "."
                    
                    self.scraping_stats['end_time'] = datetime.now()
                    self.scraping_stats['total_jobs'] = job_count
                    self.animation_running = False
                    
                    elapsed = self.scraping_stats['end_time'] - self.scraping_stats['start_time']
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
                        self.status_var.set(f"✅ Scraping completed - {job_count} jobs saved to {session_name}")
                    else:
                        self.status_var.set(f"✅ Scraping completed - {job_count} jobs saved")
                    
                    # Reset UI
                    self.start_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
                    
                    # Update quick stats
                    self.update_quick_stats()
                    
                    # Show success notification
                    if session_folder != ".":
                        self.show_notification(f"Scraping completed! {job_count} jobs saved to session folder in {elapsed_str}", "success", 5000)
                    else:
                        self.show_notification(f"Scraping completed! {job_count} jobs saved to files in {elapsed_str}", "success", 5000)
                    
                    # Try to load the scraped data
                    self.load_latest_scraped_data()
                    
                elif message_type == 'error':
                    self.log(f"❌ Error: {data}")
                    self.progress_label.configure(text="Error occurred")
                    self.status_var.set("❌ Scraping error")
                    
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
                'headless_mode': self.headless_var.get(),
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
            self.update_quick_stats()
            self.update_insights()
            
            self.status_var.set(f"✅ Loaded {len(self.df)} rows from {os.path.basename(file_path)}")
            self.show_notification(f"Successfully loaded {len(self.df)} job records", "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
            self.status_var.set("❌ Error loading file")
            self.show_notification("Failed to load CSV file", "error")
    
    def display_data(self):
        """Display data in the treeview"""
        if self.filtered_df is None:
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configure columns
        columns = list(self.filtered_df.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            # Adjust column width based on content
            max_width = max(len(str(col)), 
                           self.filtered_df[col].astype(str).str.len().max())
            self.tree.column(col, width=min(max_width * 10, 300))
        
        # Insert data rows
        for idx, row in self.filtered_df.head(1000).iterrows():  # Limit to first 1000 rows for performance
            values = [str(val) if pd.notna(val) else '' for val in row]
            self.tree.insert('', 'end', values=values)
        
        if len(self.filtered_df) > 1000:
            self.status_var.set(f"📊 Showing first 1000 of {len(self.filtered_df)} rows")
    
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
        self.status_var.set(f"🔍 Filtered: {len(self.filtered_df)} rows")
    
    def clear_filters(self):
        """Clear all filters and show original data"""
        self.search_var.set('')
        if self.df is not None:
            self.filtered_df = self.df.copy()
            self.display_data()
            self.update_statistics()
            self.status_var.set(f"📊 Showing all {len(self.df)} rows")
    
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
                self.status_var.set(f"✅ Exported {len(self.filtered_df)} rows to {os.path.basename(filename)}")
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
                self.status_var.set(f"✅ Exported {len(self.df)} rows to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def generate_chart(self):
        """Generate analytics chart based on selected type"""
        if not MATPLOTLIB_AVAILABLE:
            self.show_notification("Matplotlib not available. Please install: pip install matplotlib", "error")
            return
            
        if self.df is None:
            self.show_notification("Please load data first!", "warning")
            return
        
        chart_type = self.chart_type_var.get()
        
        try:
            # Clear previous chart
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            
            # Set up matplotlib for dark theme
            try:
                plt.style.use('dark_background')
            except:
                # Fallback if dark_background style is not available
                plt.style.use('default')
            
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            if chart_type == "Job Count by Company":
                company_counts = self.df['company'].value_counts().head(10)
                bars = ax.bar(range(len(company_counts)), company_counts.values, 
                             color=self.colors['primary'], alpha=0.8)
                ax.set_xlabel('Companies', color='white', fontsize=12)
                ax.set_ylabel('Number of Jobs', color='white', fontsize=12)
                ax.set_title('Top 10 Companies by Job Count', color='white', fontsize=14, fontweight='bold')
                ax.set_xticks(range(len(company_counts)))
                ax.set_xticklabels(company_counts.index, rotation=45, ha='right', color='white')
                ax.tick_params(colors='white')
                
                # Add value labels on bars
                for bar, value in zip(bars, company_counts.values):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           str(value), ha='center', va='bottom', color='white', fontweight='bold')
            
            elif chart_type == "Experience Level Distribution":
                exp_counts = self.df['experience_level'].value_counts()
                colors_pie = [self.colors['primary'], self.colors['secondary'], 
                             self.colors['info'], self.colors['accent'], self.colors['success']]
                wedges, texts, autotexts = ax.pie(exp_counts.values, labels=exp_counts.index, 
                                                 autopct='%1.1f%%', colors=colors_pie[:len(exp_counts)])
                ax.set_title('Experience Level Distribution', color='white', fontsize=14, fontweight='bold')
                for text in texts + autotexts:
                    text.set_color('white')
                    text.set_fontweight('bold')
            
            elif chart_type == "Skills Frequency":
                # Extract skills from the skills column (assuming it's a list or comma-separated)
                all_skills = []
                for skills in self.df['skills'].dropna():
                    if isinstance(skills, str):
                        if skills.startswith('[') and skills.endswith(']'):
                            # Handle list-like strings
                            skills = skills.strip('[]').replace("'", "").replace('"', '')
                        skill_list = [s.strip() for s in skills.split(',')]
                        all_skills.extend(skill_list)
                
                skill_counts = pd.Series(all_skills).value_counts().head(15)
                bars = ax.barh(range(len(skill_counts)), skill_counts.values, 
                              color=self.colors['info'], alpha=0.8)
                ax.set_ylabel('Skills', color='white', fontsize=12)
                ax.set_xlabel('Frequency', color='white', fontsize=12)
                ax.set_title('Top 15 Most Demanded Skills', color='white', fontsize=14, fontweight='bold')
                ax.set_yticks(range(len(skill_counts)))
                ax.set_yticklabels(skill_counts.index, color='white')
                ax.tick_params(colors='white')
                
                # Add value labels
                for bar, value in zip(bars, skill_counts.values):
                    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                           str(value), ha='left', va='center', color='white', fontweight='bold')
            
            elif chart_type == "Location Analysis":
                location_counts = self.df['location'].value_counts().head(10)
                bars = ax.bar(range(len(location_counts)), location_counts.values, 
                             color=self.colors['success'], alpha=0.8)
                ax.set_xlabel('Locations', color='white', fontsize=12)
                ax.set_ylabel('Number of Jobs', color='white', fontsize=12)
                ax.set_title('Job Distribution by Location', color='white', fontsize=14, fontweight='bold')
                ax.set_xticks(range(len(location_counts)))
                ax.set_xticklabels(location_counts.index, rotation=45, ha='right', color='white')
                ax.tick_params(colors='white')
                
                for bar, value in zip(bars, location_counts.values):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           str(value), ha='center', va='bottom', color='white', fontweight='bold')
            
            elif chart_type == "Job Type Distribution":
                type_counts = self.df['job_type'].value_counts()
                colors_pie = [self.colors['warning'], self.colors['danger'], 
                             self.colors['info'], self.colors['success']]
                wedges, texts, autotexts = ax.pie(type_counts.values, labels=type_counts.index, 
                                                 autopct='%1.1f%%', colors=colors_pie[:len(type_counts)])
                ax.set_title('Job Type Distribution', color='white', fontsize=14, fontweight='bold')
                for text in texts + autotexts:
                    text.set_color('white')
                    text.set_fontweight('bold')
            
            plt.tight_layout()
            
            # Create canvas and add to container
            canvas = FigureCanvasTkAgg(fig, self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Store figure for export
            self.current_figure = fig
            
            # Update insights
            self.update_insights()
            
            self.show_notification(f"Chart generated: {chart_type}", "success")
            
        except Exception as e:
            self.show_notification(f"Error generating chart: {str(e)}", "error")
            print(f"Chart generation error: {e}")
    
    def export_chart(self):
        """Export current chart to file"""
        if not hasattr(self, 'current_figure'):
            self.show_notification("No chart to export. Generate a chart first!", "warning")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Chart",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if filename:
            try:
                self.current_figure.savefig(filename, dpi=300, bbox_inches='tight', 
                                          facecolor='#2b2b2b', edgecolor='none')
                self.show_notification(f"Chart exported to {os.path.basename(filename)}", "success")
            except Exception as e:
                self.show_notification(f"Export failed: {str(e)}", "error")
    
    def update_insights(self):
        """Update data insights based on current data"""
        if self.df is None:
            return
        
        insights = []
        
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
    
    def show_matplotlib_info(self):
        """Show information about installing matplotlib"""
        info_message = """
Matplotlib is required for data visualization features.

To install matplotlib and enable chart generation:

1. Open your terminal/command prompt
2. Run: pip install matplotlib seaborn pillow
3. Restart the application

This will enable:
• Interactive charts and graphs
• Data visualization
• Chart export functionality
• Enhanced analytics features
        """
        
        messagebox.showinfo("Install Matplotlib", info_message.strip())
        self.show_notification("Install matplotlib to enable chart features", "info", 5000)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    app = WuzzufScraperGUI()
    app.run()

if __name__ == "__main__":
    main()
