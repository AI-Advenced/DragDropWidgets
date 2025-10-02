"""
Simple Hello World example for DragDropWidgets library
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QPoint
from dragdropwidgets import create_app, DraggableButton, DraggableLabel, DraggableImage
from dragdropwidgets.utils.events import event_manager, WidgetEvents
from dragdropwidgets.utils.themes import ThemeManager

def main():
    """Simple Hello World example"""
    
    # Create application and window
    app, window, drop_zone = create_app("Hello DragDropWidgets", (800, 600))
    
    # Create theme manager
    theme_manager = ThemeManager()
    
    # Apply light theme
    theme_manager.apply_theme_to_app('light')
    
    print("🎯 DragDropWidgets Hello World Example")
    print("=" * 50)
    
    # Create some sample widgets
    print("Creating sample widgets...")
    
    # Create draggable button
    button1 = DraggableButton("Draggable Button")
    button1.set_style('primary')
    
    # Create another button with different style
    button2 = DraggableButton("Success Button")
    button2.set_style('success')
    
    # Create a warning button
    button3 = DraggableButton("Warning Button")
    button3.set_style('warning')
    
    # Create draggable labels
    label1 = DraggableLabel("Draggable Text Label")
    label1.set_font_size(16)
    label1.set_style_preset('title')
    
    label2 = DraggableLabel("Subtitle Label")
    label2.set_style_preset('subtitle')
    
    label3 = DraggableLabel("Info Message")
    label3.set_style_preset('info')
    
    # Create an image widget (placeholder)
    image1 = DraggableImage()
    
    # Add widgets to drop zone with initial positions
    print("Adding widgets to drop zone...")
    drop_zone.add_widget(button1, QPoint(50, 50))
    drop_zone.add_widget(button2, QPoint(200, 50))
    drop_zone.add_widget(button3, QPoint(350, 50))
    
    drop_zone.add_widget(label1, QPoint(50, 150))
    drop_zone.add_widget(label2, QPoint(50, 200))
    drop_zone.add_widget(label3, QPoint(50, 250))
    
    drop_zone.add_widget(image1, QPoint(400, 150))
    
    # Enable snap to grid for all widgets
    print("Enabling snap-to-grid...")
    for widget in [button1, button2, button3, label1, label2, label3, image1]:
        if hasattr(widget, 'set_snap_to_grid'):
            widget.set_snap_to_grid(True, 25)
    
    # Set up event handlers
    def on_button_clicked(widget_id):
        print(f"🔘 Button clicked: {widget_id}")
        
        # Find which button was clicked
        for widget in drop_zone.widgets:
            if widget.widget_id == widget_id:
                print(f"   Button text: '{widget.get_text()}'")
                break
    
    def on_widget_dropped(widget, position):
        print(f"📍 Widget dropped at position: ({position.x()}, {position.y()})")
        print(f"   Widget type: {widget.__class__.__name__}")
        if hasattr(widget, 'get_text'):
            print(f"   Widget text: '{widget.get_text()}'")
    
    def on_widget_selected(widget):
        print(f"✨ Widget selected: {widget.__class__.__name__}")
        if hasattr(widget, 'get_text'):
            print(f"   Text: '{widget.get_text()}'")
    
    def on_layout_changed():
        print(f"🔄 Layout changed - Total widgets: {len(drop_zone.widgets)}")
    
    def on_image_clicked(widget_id):
        print(f"🖼️ Image widget clicked: {widget_id}")
    
    # Connect button signals
    button1.button_clicked.connect(on_button_clicked)
    button2.button_clicked.connect(on_button_clicked)
    button3.button_clicked.connect(on_button_clicked)
    
    # Connect drop zone signals
    drop_zone.widget_dropped.connect(on_widget_dropped)
    drop_zone.layout_changed.connect(on_layout_changed)
    
    # Connect image signal
    image1.image_clicked.connect(on_image_clicked)
    
    # Register event handlers using the event system
    def on_widget_event(event):
        print(f"📢 Event: {event.event_type} from {event.source.__class__.__name__ if event.source else 'Unknown'}")
    
    # Register global event handler
    event_manager.register_global_handler(on_widget_event)
    
    # Add control panel to window
    create_control_panel(window, drop_zone, theme_manager)
    
    print("\n🚀 Application started!")
    print("Instructions:")
    print("• Drag and drop widgets around the canvas")
    print("• Click buttons to see console output")
    print("• Click the image placeholder to load an image")
    print("• Use Ctrl+Click to multi-select widgets")
    print("• Try the control panel buttons")
    print("• Watch the console for event messages")
    print("\n" + "=" * 50)
    
    # Show window and run application
    window.show()
    return app.exec()

def create_control_panel(window, drop_zone, theme_manager):
    """Create a control panel with useful buttons"""
    
    # Get the central widget and create a layout
    central_widget = window.centralWidget()
    
    # Create main layout
    main_layout = QHBoxLayout()
    
    # Create control panel
    control_panel = QWidget()
    control_panel.setFixedWidth(200)
    control_layout = QVBoxLayout(control_panel)
    
    # Panel title
    title = QLabel("Control Panel")
    title.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
    control_layout.addWidget(title)
    
    # Add widget buttons
    def add_button():
        button = DraggableButton(f"Button {len(drop_zone.widgets) + 1}")
        button.set_snap_to_grid(True, 25)
        drop_zone.add_widget(button, QPoint(100, 100))
        button.button_clicked.connect(lambda widget_id: print(f"🔘 New button clicked: {widget_id}"))
    
    def add_label():
        label = DraggableLabel(f"Label {len(drop_zone.widgets) + 1}")
        label.set_snap_to_grid(True, 25)
        drop_zone.add_widget(label, QPoint(150, 150))
    
    def add_image():
        image = DraggableImage()
        drop_zone.add_widget(image, QPoint(200, 200))
    
    def clear_all():
        for widget in drop_zone.widgets[:]:
            drop_zone.remove_widget(widget.widget_id)
        print("🧹 Cleared all widgets")
    
    def toggle_grid():
        drop_zone.set_grid_visible(not drop_zone.show_grid)
        print(f"📏 Grid {'enabled' if drop_zone.show_grid else 'disabled'}")
    
    def arrange_grid():
        drop_zone.set_layout_mode('grid')
        print("📐 Arranged widgets in grid")
    
    def arrange_flow():
        drop_zone.set_layout_mode('flow')
        print("💧 Arranged widgets in flow")
    
    def free_layout():
        drop_zone.set_layout_mode('free')
        print("🆓 Set layout to free mode")
    
    def change_theme():
        themes = ['light', 'dark', 'blue', 'green', 'high_contrast']
        current_idx = themes.index(theme_manager.current_theme)
        next_idx = (current_idx + 1) % len(themes)
        next_theme = themes[next_idx]
        
        theme_manager.apply_theme_to_app(next_theme)
        print(f"🎨 Changed theme to: {next_theme}")
    
    def save_layout():
        from dragdropwidgets.utils.serializer import LayoutSerializer
        layout_data = drop_zone.get_layout_data()
        
        if LayoutSerializer.save_to_json(layout_data, "hello_world_layout.json"):
            print("💾 Layout saved to hello_world_layout.json")
        else:
            print("❌ Failed to save layout")
    
    def load_layout():
        from dragdropwidgets.utils.serializer import LayoutSerializer
        layout_data = LayoutSerializer.load_from_json("hello_world_layout.json")
        
        if layout_data:
            drop_zone.load_layout_data(layout_data)
            print("📂 Layout loaded from hello_world_layout.json")
        else:
            print("❌ Failed to load layout")
    
    # Create control buttons
    buttons_data = [
        ("Add Button", add_button),
        ("Add Label", add_label),
        ("Add Image", add_image),
        ("", None),  # Separator
        ("Toggle Grid", toggle_grid),
        ("Arrange Grid", arrange_grid),
        ("Arrange Flow", arrange_flow),
        ("Free Layout", free_layout),
        ("", None),  # Separator
        ("Change Theme", change_theme),
        ("", None),  # Separator
        ("Save Layout", save_layout),
        ("Load Layout", load_layout),
        ("", None),  # Separator
        ("Clear All", clear_all),
    ]
    
    for text, callback in buttons_data:
        if not text:  # Separator
            separator = QLabel("─" * 20)
            separator.setStyleSheet("color: #cccccc; margin: 5px 0;")
            control_layout.addWidget(separator)
        else:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 12px;
                    margin: 2px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background-color: white;
                }
                QPushButton:hover {
                    background-color: #e6f3ff;
                    border-color: #0078d4;
                }
                QPushButton:pressed {
                    background-color: #cce7ff;
                }
            """)
            control_layout.addWidget(btn)
    
    control_layout.addStretch()
    
    # Add info label
    info_label = QLabel("💡 Tip: Drag widgets around!\nUse Ctrl+Click for multi-select")
    info_label.setStyleSheet("font-size: 11px; color: #666666; margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
    info_label.setWordWrap(True)
    control_layout.addWidget(info_label)
    
    # Set up main layout
    main_layout.addWidget(control_panel)
    main_layout.addWidget(drop_zone, 1)
    
    # Create a new central widget with the layout
    new_central = QWidget()
    new_central.setLayout(main_layout)
    window.setCentralWidget(new_central)

if __name__ == "__main__":
    sys.exit(main())