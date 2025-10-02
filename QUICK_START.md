# 🚀 DragDropWidgets - Quick Start Guide

## 📦 Installation

### Method 1: Direct Installation
```bash
# Clone the repository
git clone https://github.com/dragdropwidgets/dragdropwidgets.git
cd dragdropwidgets

# Install in development mode
pip install -e .
```

### Method 2: Requirements Only
```bash
# Install dependencies manually
pip install PySide6>=6.4.0 PyYAML>=6.0

# Download and extract the library
# Then run examples directly
```

## ⚡ Quick Demo

### Run Built-in Examples
```bash
# Hello World example
python -m dragdropwidgets.examples.hello_world

# Advanced Dashboard
python -m dragdropwidgets.examples.dashboard
```

### 5-Minute Tutorial

#### 1. Basic Setup
```python
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from PySide6.QtCore import QPoint

# Create application
app, window, drop_zone = create_app("My First App", (800, 600))
```

#### 2. Add Widgets
```python
# Create a button
button = DraggableButton("Click Me!")
button.set_style('success')  # Green button
button.set_snap_to_grid(True, 20)  # Snap to 20px grid

# Create a label
label = DraggableLabel("Drag me around!")
label.set_font_size(16)
label.set_style_preset('title')  # Large title style
```

#### 3. Position and Display
```python
# Add widgets to the drop zone
drop_zone.add_widget(button, QPoint(100, 100))
drop_zone.add_widget(label, QPoint(100, 200))

# Show window and run
window.show()
sys.exit(app.exec())
```

#### 4. Complete Example
```python
#!/usr/bin/env python3
"""
Simple DragDropWidgets example
"""
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from PySide6.QtCore import QPoint

def main():
    # Create application
    app, window, drop_zone = create_app("Quick Start Demo", (800, 600))
    
    # Create widgets
    button = DraggableButton("Hello World!")
    button.set_style('primary')
    button.set_snap_to_grid(True, 25)
    
    label = DraggableLabel("Drag & Drop Widget Library")
    label.set_font_size(18)
    label.set_style_preset('subtitle')
    
    # Add to drop zone
    drop_zone.add_widget(button, QPoint(150, 150))
    drop_zone.add_widget(label, QPoint(150, 250))
    
    # Handle button clicks
    def on_button_click(widget_id):
        print(f"Button {widget_id} was clicked!")
    
    button.button_clicked.connect(on_button_click)
    
    # Show and run
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
```

## 🎨 Theme Switching

```python
from dragdropwidgets.utils.themes import ThemeManager

theme_manager = ThemeManager()

# Switch themes
theme_manager.apply_theme_to_application('dark')    # Dark theme
theme_manager.apply_theme_to_application('blue')    # Blue theme  
theme_manager.apply_theme_to_application('light')   # Back to light
```

## 💾 Save & Load Layouts

```python
from dragdropwidgets.utils.serializer import LayoutSerializer

# Save current layout
layout_data = drop_zone.get_layout_data()
LayoutSerializer.save_to_json(layout_data, 'my_layout.json')

# Load saved layout
layout_data = LayoutSerializer.load_from_json('my_layout.json')
drop_zone.load_layout_data(layout_data)
```

## 📐 Layout Management

```python
from dragdropwidgets.core.layout_manager import DynamicLayoutManager

layout_manager = DynamicLayoutManager(drop_zone)

# Auto-align selected widgets
selected_widgets = drop_zone.selected_widgets
layout_manager.auto_align_widgets(selected_widgets, 'left')

# Distribute widgets evenly
layout_manager.distribute_widgets(selected_widgets, 'horizontal')

# Arrange in grid
layout_manager.create_layout_grid(drop_zone.widgets, columns=3)
```

## 🔧 Custom Widgets

```python
from dragdropwidgets.widgets.custom import CustomWidgetFactory

# Use built-in custom widgets
progress_bar = CustomWidgetFactory.create_widget('DraggableProgressBar', 50)
slider = CustomWidgetFactory.create_widget('DraggableSlider', 75)
text_edit = CustomWidgetFactory.create_widget('DraggableTextEdit', "Hello!")

# Add to drop zone
drop_zone.add_widget(progress_bar, QPoint(300, 100))
drop_zone.add_widget(slider, QPoint(300, 150))
drop_zone.add_widget(text_edit, QPoint(300, 200))
```

## 🎯 Common Use Cases

### Dashboard Creation
```python
# Create dashboard panels
from dragdropwidgets.examples.dashboard import DashboardWidget

panel1 = DashboardWidget("System Status")
panel2 = DashboardWidget("Performance Metrics")

# Add content to panels
status_label = QLabel("All systems operational")
panel1.set_content_widget(status_label)

# Add to drop zone
drop_zone.add_widget(panel1, QPoint(50, 50))
drop_zone.add_widget(panel2, QPoint(350, 50))
```

### Form Builder
```python
# Create form elements
name_label = DraggableLabel("Name:")
name_label.set_style_preset('body')

email_label = DraggableLabel("Email:")
email_label.set_style_preset('body')

submit_btn = DraggableButton("Submit")
submit_btn.set_style('success')

# Position in form layout
drop_zone.add_widget(name_label, QPoint(50, 100))
drop_zone.add_widget(email_label, QPoint(50, 150))
drop_zone.add_widget(submit_btn, QPoint(50, 200))
```

## 🐛 Troubleshooting

### Common Issues
1. **Import Error**: Make sure PySide6 is installed
   ```bash
   pip install PySide6
   ```

2. **Display Error**: Need GUI environment (not headless)
   - Install display libraries on Linux
   - Use X11 forwarding for SSH
   - Run on desktop environment

3. **Permission Error**: Use virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

### Performance Tips
- Enable snap-to-grid for smoother dragging
- Use fewer widgets for better performance
- Disable animations on slower systems
- Use appropriate widget sizes

## 📖 Learn More

- **Full Examples**: Check `dragdropwidgets/examples/` directory
- **API Documentation**: Read docstrings in source code  
- **Advanced Features**: Explore `utils/` modules
- **Customization**: Study `widgets/custom.py`

## 🎉 You're Ready!

You now have everything needed to create interactive drag-and-drop applications with DragDropWidgets. Start with the simple examples above and gradually explore more advanced features.

**Happy coding!** 🚀