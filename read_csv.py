#!/usr/bin/env python3
"""
Wuzzuf Job Scraper GUI Launcher
Simple launcher for the comprehensive GUI application
"""

try:
    from wuzzuf_gui import main
    print("🚀 Launching Wuzzuf Job Scraper Pro...")
    main()
except ImportError as e:
    print(f"❌ Error: Could not import GUI module: {e}")
    print("💡 Make sure 'wuzzuf_gui.py' is in the same directory")
    print("💡 Install required dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("💡 Please check your installation and try again")   
