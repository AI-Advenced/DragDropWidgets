# 📚 DragDropWidgets - Complete Documentation

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Widget Library](#widget-library)
5. [Layout Management](#layout-management)
6. [Event System](#event-system)
7. [Theming & Styling](#theming--styling)
8. [Serialization & Export](#serialization--export)
9. [Advanced Usage](#advanced-usage)
10. [Custom Widgets](#custom-widgets)
11. [Examples & Tutorials](#examples--tutorials)
12. [API Reference](#api-reference)
13. [Troubleshooting](#troubleshooting)

---

## 📦 Installation

### Requirements
- Python 3.8 or higher
- PySide6 >= 6.4.0
- PyYAML >= 6.0

### Installation Methods

#### From Source (Current)
```bash
# Clone the repository
git clone <repository-url>
cd dragdropwidgets

# Install in development mode
pip install -e .

# Or install dependencies manually
pip install PySide6>=6.4.0 PyYAML>=6.0
```

#### Future PyPI Installation
```bash
pip install dragdropwidgets
```

### Verify Installation
```bash
# Test basic functionality
python -c "import dragdropwidgets; print('✅ Installation successful!')"

# Run examples
python -m dragdropwidgets.examples.hello_world
python -m dragdropwidgets.examples.dashboard

# Or using console scripts (after installation)
dragdrop-hello
dragdrop-dashboard
```

---

## 🚀 Quick Start

### Basic Application Setup

```python
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from PySide6.QtCore import QPoint

def main():
    # Create application and main window
    app, window, drop_zone = create_app("My First App", (800, 600))
    
    # Create some widgets
    button = DraggableButton("Hello World!")
    button.set_style('primary')
    
    label = DraggableLabel("Drag me around!")
    label.set_font_size(16)
    
    # Add widgets to the drop zone
    drop_zone.add_widget(button, QPoint(100, 100))
    drop_zone.add_widget(label, QPoint(100, 200))
    
    # Enable snap to grid
    button.set_snap_to_grid(True, 25)
    label.set_snap_to_grid(True, 25)
    
    # Show window and run
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
```

### Manual Setup (Advanced)

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from dragdropwidgets import DropZone, DraggableButton

def main():
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Manual Setup")
    window.resize(800, 600)
    
    # Create drop zone
    drop_zone = DropZone()
    window.setCentralWidget(drop_zone)
    
    # Add widgets
    button = DraggableButton("Manual Button")
    drop_zone.add_widget(button, QPoint(50, 50))
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
```

---

## 🧩 Core Concepts

### Widget Hierarchy

```
WidgetBase (Abstract Base)
└── DraggableWidget
    ├── DraggableButton
    ├── DraggableLabel
    ├── DraggableImage
    ├── DraggableProgressBar
    ├── DraggableSlider
    ├── DraggableTextEdit
    └── Custom Widgets...
```

### Key Classes

#### `WidgetBase`
Base class for all widgets with core functionality:
- Selection management
- Property serialization
- Metadata system
- Event handling

#### `DraggableWidget`
Extends WidgetBase with drag & drop capabilities:
- Mouse event handling
- Drag threshold detection
- Snap to grid functionality
- Animation support

#### `DropZone`
Container for draggable widgets:
- Accepts dropped widgets
- Manages widget collections
- Provides layout modes
- Handles grid display

### Widget Lifecycle

1. **Creation** - Widget instantiated with initial properties
2. **Configuration** - Properties set (text, style, etc.)
3. **Registration** - Added to drop zone
4. **Interaction** - User dragging, clicking, resizing
5. **Serialization** - Save/load widget state
6. **Destruction** - Proper cleanup and memory management

---

## 🎨 Widget Library

### DraggableButton

Interactive buttons with multiple styles and states.

```python
from dragdropwidgets import DraggableButton

# Basic button
button = DraggableButton("Click Me!")

# Styling
button.set_style('primary')    # primary, secondary, success, danger, warning, info
button.set_enabled(True)       # Enable/disable
button.set_checkable(True)     # Make it a toggle button

# Event handling
def on_button_click(widget_id):
    print(f"Button {widget_id} was clicked!")

button.button_clicked.connect(on_button_click)

# Properties
text = button.get_text()
is_checked = button.is_checked()  # For checkable buttons
```

#### Button Styles
- **Primary** - Blue, main action button
- **Secondary** - Gray, secondary actions
- **Success** - Green, positive actions
- **Danger** - Red, destructive actions
- **Warning** - Yellow, caution actions
- **Info** - Cyan, informational actions

### DraggableLabel

Rich text labels with extensive formatting options.

```python
from dragdropwidgets import DraggableLabel

# Basic label
label = DraggableLabel("Hello World!")

# Typography
label.set_font_size(18)
label.set_font_family("Arial")
label.set_font_bold(True)
label.set_font_italic(False)

# Colors
label.set_color("#333333")
label.set_background_color("#f0f0f0")

# Alignment
label.set_alignment('center')  # left, center, right, top, bottom
label.set_word_wrap(True)

# Style presets
label.set_style_preset('title')  # title, subtitle, body, caption, warning, error, success, info

# Properties
text = label.get_text()
```

#### Style Presets
- **Title** - Large, bold text for headings
- **Subtitle** - Medium text for subheadings  
- **Body** - Regular text for content
- **Caption** - Small text for descriptions
- **Warning** - Orange background for warnings
- **Error** - Red background for errors
- **Success** - Green background for success messages
- **Info** - Blue background for information

### DraggableImage

Image widgets with scaling and transformation capabilities.

```python
from dragdropwidgets import DraggableImage

# Create image widget
image = DraggableImage("path/to/image.jpg")

# Or create empty and load later
image = DraggableImage()
image.load_image("path/to/image.jpg")
image.open_file_dialog()  # Let user select image

# Scaling
image.set_scale_mode('keep_aspect_ratio')  # keep_aspect_ratio, ignore_aspect_ratio, keep_aspect_ratio_by_expanding
image.set_aspect_ratio_locked(True)

# Transformations
image.rotate_image(90)      # Rotate by degrees (90, 180, 270)
image.flip_horizontal()     # Flip horizontally
image.flip_vertical()       # Flip vertically

# Information
info = image.get_image_info()
print(f"Size: {info['width']}x{info['height']}")

# Save
image.save_image("output.jpg", quality=95)
```

### DraggableProgressBar

Animated progress indicators for showing completion status.

```python
from dragdropwidgets.widgets.custom import DraggableProgressBar

# Create progress bar
progress = DraggableProgressBar(value=50)

# Set value and range
progress.set_value(75)
progress.set_range(0, 100)

# Properties
current_value = progress.metadata['value']
min_val = progress.metadata['minimum']
max_val = progress.metadata['maximum']
```

### DraggableSlider

Value input sliders for numeric input.

```python
from dragdropwidgets.widgets.custom import DraggableSlider

# Create slider
slider = DraggableSlider(value=50)

# Configure
slider.set_value(25)
slider.set_range(0, 100)

# Get value
current_value = slider.metadata['value']
```

### DraggableTextEdit

Multi-line text input areas with formatting.

```python
from dragdropwidgets.widgets.custom import DraggableTextEdit

# Create text edit
text_edit = DraggableTextEdit("Initial text content")

# Configure
text_edit.set_text("New content")
text_edit.set_read_only(False)

# Get content
content = text_edit.get_text()
```

---

## 📐 Layout Management

### Drop Zone Basics

```python
from dragdropwidgets import DropZone
from PySide6.QtCore import QPoint

# Create drop zone
drop_zone = DropZone()

# Configure grid
drop_zone.set_grid_visible(True)
drop_zone.grid_size = 20

# Add widgets
drop_zone.add_widget(widget, QPoint(100, 100))

# Remove widgets
drop_zone.remove_widget(widget.widget_id)

# Selection management
drop_zone.select_all()
drop_zone.clear_selection()
drop_zone.delete_selected()
```

### Layout Modes

#### Free Layout (Default)
```python
drop_zone.set_layout_mode('free')
# Widgets can be positioned anywhere
```

#### Grid Layout
```python
drop_zone.set_layout_mode('grid')
# Widgets automatically arranged in a grid
```

#### Flow Layout
```python
drop_zone.set_layout_mode('flow')
# Widgets flow left-to-right, top-to-bottom
```

### Advanced Layout Management

```python
from dragdropwidgets.core.layout_manager import DynamicLayoutManager

# Create layout manager
layout_manager = DynamicLayoutManager(drop_zone)

# Widget alignment
selected_widgets = drop_zone.selected_widgets
layout_manager.auto_align_widgets(selected_widgets, 'left')    # left, right, top, bottom, center_horizontal, center_vertical

# Distribution
layout_manager.distribute_widgets(selected_widgets, 'horizontal')  # horizontal, vertical

# Uniform sizing
layout_manager.resize_widgets_uniform(selected_widgets, 'width')   # width, height, both

# Grid arrangement
layout_manager.create_layout_grid(selected_widgets, columns=3, spacing=20)

# Circular arrangement
from PySide6.QtCore import QPoint
center = QPoint(400, 300)
layout_manager.create_circular_layout(selected_widgets, center, radius=150)
```

### Snap to Grid

```python
# Enable for individual widgets
widget.set_snap_to_grid(True, grid_size=25)

# Grid settings
drop_zone.grid_size = 20        # Grid spacing
drop_zone.set_grid_visible(True)  # Show/hide grid lines
```

---

## 🎭 Event System

### Basic Event Handling

```python
from dragdropwidgets.utils.events import event_manager, WidgetEvents

# Register event handler
def on_widget_moved(event):
    widget = event.source
    position = event.data.get('position')
    print(f"Widget {widget.widget_id} moved to {position}")

event_manager.register_event(WidgetEvents.WIDGET_MOVED, on_widget_moved)

# Emit custom events
event_manager.emit_event('my_custom_event', source=widget, data={'key': 'value'})
```

### Event Types

#### Widget Events
```python
from dragdropwidgets.utils.events import WidgetEvents

# Lifecycle events
WidgetEvents.WIDGET_CREATED
WidgetEvents.WIDGET_DESTROYED
WidgetEvents.WIDGET_SHOWN
WidgetEvents.WIDGET_HIDDEN

# Interaction events
WidgetEvents.WIDGET_SELECTED
WidgetEvents.WIDGET_DESELECTED
WidgetEvents.WIDGET_CLICKED
WidgetEvents.WIDGET_DOUBLE_CLICKED

# Drag & drop events
WidgetEvents.DRAG_STARTED
WidgetEvents.DRAG_MOVED
WidgetEvents.DRAG_FINISHED
WidgetEvents.WIDGET_DROPPED

# Modification events
WidgetEvents.WIDGET_MOVED
WidgetEvents.WIDGET_RESIZED
WidgetEvents.WIDGET_PROPERTY_CHANGED
```

### Advanced Event Handling

```python
from dragdropwidgets.utils.events import EventManager, EventPriority, EventContext

# Create event manager
event_manager = EventManager()

# Priority handling
def high_priority_handler(event):
    print("High priority handler")
    if some_condition:
        event.cancel()  # Cancel event propagation

event_manager.register_event('test_event', high_priority_handler, priority=EventPriority.HIGH)

# One-time handlers
def one_time_handler(event):
    print("This runs only once")

event_manager.register_event('test_event', one_time_handler, once=True)

# Event contexts for scoped handling
with EventContext(event_manager, 'my_context') as ctx:
    ctx.register_event('temp_event', temp_handler)
    # handlers automatically removed when exiting context
```

### Global Event Handler

```python
def global_handler(event):
    print(f"Global: {event.event_type} from {event.source}")

event_manager.register_global_handler(global_handler)
```

---

## 🎨 Theming & Styling

### Built-in Themes

```python
from dragdropwidgets.utils.themes import ThemeManager

theme_manager = ThemeManager()

# Get available themes
themes = theme_manager.get_available_themes()
# {'light': 'Light Theme', 'dark': 'Dark Theme', 'blue': 'Blue Theme', 'green': 'Nature Theme', 'high_contrast': 'High Contrast'}

# Apply theme to entire application
theme_manager.apply_theme_to_app('dark')

# Apply theme to specific widget
theme_manager.apply_theme(widget, 'blue')

# Get current theme
current = theme_manager.get_current_theme()
```

### Theme Descriptions

#### Light Theme
- Clean, bright interface
- Blue accents (#0078d4)
- White backgrounds
- Dark gray text

#### Dark Theme  
- Modern dark interface
- Bright blue accents (#0099ff)
- Dark gray backgrounds
- White text

#### Blue Theme
- Professional blue color scheme
- Light blue backgrounds
- Navy blue text
- Business-friendly appearance

#### Green Theme
- Nature-inspired colors
- Soft green backgrounds
- Forest green accents
- Calming, organic feel

#### High Contrast Theme
- Maximum accessibility
- Black backgrounds
- White text
- Yellow accents
- WCAG AAA compliant

### Custom Theme Creation

```python
# Create custom theme
custom_colors = {
    'background': '#2c3e50',
    'foreground': '#ecf0f1',
    'accent': '#e74c3c',
    'border': '#34495e',
    'hover': '#3d4f65',
    'selection': 'rgba(231, 76, 60, 0.2)',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db'
}

custom_fonts = {
    'default_size': 14,
    'title_size': 18,
    'small_size': 12,
    'family': 'Roboto, Arial, sans-serif'
}

custom_spacing = {
    'small': 4,
    'medium': 8,
    'large': 16,
    'xlarge': 24
}

theme_manager.create_custom_theme(
    'corporate',
    'Corporate Theme',
    custom_colors,
    custom_fonts,
    custom_spacing,
    'Professional corporate color scheme'
)

# Apply custom theme
theme_manager.apply_theme_to_app('corporate')
```

### Theme Import/Export

```python
# Export theme to file
theme_manager.export_theme('corporate', 'corporate_theme.json')

# Import theme from file
theme_manager.import_theme('downloaded_theme.json', 'imported_theme')

# Delete custom theme
theme_manager.delete_custom_theme('old_theme')
```

### Theme Preview

```python
# Get preview colors for theme selection UI
preview = theme_manager.get_theme_preview_colors('dark')
# {'background': '#2d2d2d', 'foreground': '#ffffff', 'accent': '#0099ff', 'border': '#555555'}
```

---

## 💾 Serialization & Export

### Layout Serialization

```python
from dragdropwidgets.utils.serializer import LayoutSerializer

# Get layout data from drop zone
layout_data = drop_zone.get_layout_data()

# Save to JSON
LayoutSerializer.save_to_json(layout_data, 'my_layout.json')

# Save to YAML
LayoutSerializer.save_to_yaml(layout_data, 'my_layout.yaml')

# Load from file
layout_data = LayoutSerializer.load_from_json('my_layout.json')
layout_data = LayoutSerializer.load_from_yaml('my_layout.yaml')

# Apply loaded layout
drop_zone.load_layout_data(layout_data)
```

### Automatic Backups

```python
# Create timestamped backup
backup_file = LayoutSerializer.create_backup(layout_data, backup_dir='backups')
print(f"Backup saved to: {backup_file}")
# Output: backups/layout_backup_20240115_143022.json
```

### Python Code Export

```python
# Export layout as executable Python code
code = LayoutSerializer.export_to_code(layout_data, 'python')

# Save to file
with open('generated_layout.py', 'w') as f:
    f.write(code)

# The generated code can be run directly
exec(code)
```

### Layout Validation

```python
# Validate layout data
is_valid = LayoutSerializer._validate_layout_data(layout_data)

if not is_valid:
    print("Invalid layout format")
```

### Layout Operations

```python
# Merge two layouts
layout1 = LayoutSerializer.load_from_json('layout1.json')
layout2 = LayoutSerializer.load_from_json('layout2.json')
merged = LayoutSerializer.merge_layouts(layout1, layout2)

# Get layout statistics
stats = LayoutSerializer.get_layout_statistics(layout_data)
print(f"Total widgets: {stats['total_widgets']}")
print(f"Widget types: {stats['widget_types']}")
print(f"Layout bounds: {stats['layout_bounds']}")
```

---

## 🔧 Advanced Usage

### Property Management

```python
# Get widget properties for serialization
properties = widget.get_properties()
print(properties)
# {
#     'id': 'uuid-string',
#     'type': 'DraggableButton', 
#     'position': {'x': 100, 'y': 100},
#     'size': {'width': 120, 'height': 35},
#     'metadata': {'text': 'Button', 'style': 'primary'}
# }

# Apply properties to widget
widget.set_properties(properties)

# Clone widget
cloned_widget = widget.clone()
```

### Widget Metadata

```python
# Access widget metadata
widget.metadata['custom_key'] = 'custom_value'
widget.metadata.update({
    'category': 'ui_controls',
    'version': '1.0'
})

# Use metadata in serialization
properties = widget.get_properties()
metadata = properties['metadata']
```

### Selection Management

```python
# Single selection
widget.set_selected(True)
is_selected = widget.is_selected

# Multi-selection in drop zone
drop_zone.select_all()
drop_zone.clear_selection()
selected_widgets = drop_zone.selected_widgets

# Selection events
def on_selection_changed(widget):
    print(f"Selected: {widget.__class__.__name__}")

drop_zone.widget_selected.connect(on_selection_changed)
```

### Animation System

```python
from PySide6.QtCore import QPoint

# Animate widget to position
target_position = QPoint(200, 300)
animation = widget.animate_to_position(target_position, duration=500)

# Animation with callback
def on_animation_finished():
    print("Animation completed!")

animation.finished.connect(on_animation_finished)
```

### Drag & Drop Customization

```python
# Configure drag behavior
widget.drag_threshold = 10  # Pixels before drag starts
widget.set_snap_to_grid(True, 25)

# Drag event handling
def on_drag_started(widget):
    print(f"Started dragging {widget.widget_id}")

def on_drag_finished(widget, position):
    print(f"Dropped at {position.x()}, {position.y()}")

widget.drag_started.connect(on_drag_started)
widget.drag_finished.connect(on_drag_finished)
```

---

## 🛠️ Custom Widgets

### Creating Custom Widgets

```python
from dragdropwidgets.core.draggable import DraggableWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
import uuid

class MyCustomWidget(DraggableWidget):
    # Custom signals
    value_changed = Signal(int)
    
    def __init__(self, initial_value=0, parent=None):
        super().__init__(parent)
        
        # Create UI elements
        self.label = QLabel(f"Value: {initial_value}", self)
        self.value = initial_value
        
        # Set appearance
        self.setStyleSheet("""
            MyCustomWidget {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        # Set size
        self.resize(120, 60)
        
        # Update metadata
        self.metadata.update({
            'value': initial_value,
            'widget_type': 'custom_value_display'
        })
    
    def set_value(self, value):
        """Set the widget value"""
        self.value = value
        self.label.setText(f"Value: {value}")
        self.metadata['value'] = value
        self.value_changed.emit(value)
    
    def get_value(self):
        """Get the widget value"""
        return self.value
    
    def clone(self):
        """Create a copy of this widget"""
        cloned = MyCustomWidget(self.value, self.parent())
        
        # Copy base properties
        properties = self.get_properties()
        properties['id'] = str(uuid.uuid4())  # New unique ID
        cloned.set_properties(properties)
        
        return cloned
    
    def get_properties(self):
        """Override to include custom properties"""
        props = super().get_properties()
        props['metadata']['value'] = self.value
        return props
    
    def set_properties(self, properties):
        """Override to apply custom properties"""
        super().set_properties(properties)
        
        metadata = properties.get('metadata', {})
        if 'value' in metadata:
            self.set_value(metadata['value'])
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        self.label.resize(self.size())
```

### Registering Custom Widgets

```python
from dragdropwidgets.widgets.custom import CustomWidgetFactory

# Register the custom widget
CustomWidgetFactory.register_widget(
    'MyCustomWidget',
    MyCustomWidget,
    {
        'description': 'A custom value display widget',
        'category': 'Custom',
        'icon': '🔢',
        'default_size': (120, 60),
        'properties': {
            'value': {
                'type': 'int',
                'default': 0,
                'min': -1000,
                'max': 1000,
                'description': 'The numeric value to display'
            }
        }
    }
)

# Create widget using factory
custom_widget = CustomWidgetFactory.create_widget('MyCustomWidget', initial_value=42)

# Add to drop zone
drop_zone.add_widget(custom_widget, QPoint(100, 100))
```

### Advanced Custom Widget Example

```python
from PySide6.QtWidgets import QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt

class InteractiveSliderWidget(DraggableWidget):
    def __init__(self, min_val=0, max_val=100, value=50, parent=None):
        super().__init__(parent)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(value)
        
        # Create value label
        self.value_label = QLabel(f"{value}")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        # Add to layout
        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)
        
        # Connect signals
        self.slider.valueChanged.connect(self._on_value_changed)
        
        # Set size
        self.resize(200, 80)
        
        # Update metadata
        self.metadata.update({
            'min_value': min_val,
            'max_value': max_val,
            'current_value': value
        })
    
    def _on_value_changed(self, value):
        self.value_label.setText(str(value))
        self.metadata['current_value'] = value
    
    def get_value(self):
        return self.slider.value()
    
    def set_value(self, value):
        self.slider.setValue(value)
```

---

## 📖 Examples & Tutorials

### Tutorial 1: Basic Application

```python
"""
Tutorial 1: Creating a basic drag-and-drop application
"""
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from PySide6.QtCore import QPoint

def tutorial_1():
    # Step 1: Create the application
    app, window, drop_zone = create_app("Tutorial 1: Basics", (600, 400))
    
    # Step 2: Create widgets
    button1 = DraggableButton("Button 1")
    button1.set_style('primary')
    
    button2 = DraggableButton("Button 2") 
    button2.set_style('success')
    
    label = DraggableLabel("Drag me around!")
    label.set_font_size(14)
    
    # Step 3: Add widgets to drop zone
    drop_zone.add_widget(button1, QPoint(50, 50))
    drop_zone.add_widget(button2, QPoint(200, 50))
    drop_zone.add_widget(label, QPoint(50, 150))
    
    # Step 4: Configure drag behavior
    for widget in [button1, button2, label]:
        widget.set_snap_to_grid(True, 20)
    
    # Step 5: Add event handlers
    def on_button_click(widget_id):
        print(f"Button clicked: {widget_id}")
    
    button1.button_clicked.connect(on_button_click)
    button2.button_clicked.connect(on_button_click)
    
    # Step 6: Show and run
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(tutorial_1())
```

### Tutorial 2: Theme System

```python
"""
Tutorial 2: Working with themes
"""
import sys
from dragdropwidgets import create_app, DraggableButton
from dragdropwidgets.utils.themes import ThemeManager
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QPoint

def tutorial_2():
    app, window, drop_zone = create_app("Tutorial 2: Themes", (800, 600))
    
    # Create theme manager
    theme_manager = ThemeManager()
    
    # Create some widgets
    button = DraggableButton("Sample Button")
    drop_zone.add_widget(button, QPoint(100, 100))
    
    # Create theme switcher panel
    panel = QWidget()
    panel_layout = QVBoxLayout(panel)
    
    themes = theme_manager.get_available_themes()
    for theme_id, theme_name in themes.items():
        theme_btn = QPushButton(theme_name)
        theme_btn.clicked.connect(lambda checked, tid=theme_id: theme_manager.apply_theme_to_app(tid))
        panel_layout.addWidget(theme_btn)
    
    # Add panel to window (simplified for tutorial)
    window.setMenuWidget(panel)
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(tutorial_2())
```

### Tutorial 3: Layout Management

```python
"""
Tutorial 3: Advanced layout management
"""
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.core.layout_manager import DynamicLayoutManager
from PySide6.QtCore import QPoint

def tutorial_3():
    app, window, drop_zone = create_app("Tutorial 3: Layout Management", (800, 600))
    
    # Create layout manager
    layout_manager = DynamicLayoutManager(drop_zone)
    
    # Create multiple widgets
    widgets = []
    for i in range(6):
        button = DraggableButton(f"Button {i+1}")
        widgets.append(button)
        drop_zone.add_widget(button, QPoint(50 + i*30, 50 + i*30))
    
    # Create layout control functions
    def arrange_grid():
        layout_manager.create_layout_grid(widgets, columns=3, spacing=20)
    
    def align_left():
        layout_manager.auto_align_widgets(widgets, 'left')
    
    def distribute_horizontal():
        layout_manager.distribute_widgets(widgets, 'horizontal')
    
    def circular_layout():
        center = QPoint(400, 300)
        layout_manager.create_circular_layout(widgets, center, radius=100)
    
    # You would typically add UI controls to call these functions
    # For this tutorial, we'll just arrange in a grid automatically
    arrange_grid()
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(tutorial_3())
```

### Tutorial 4: Serialization

```python
"""
Tutorial 4: Saving and loading layouts
"""
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.utils.serializer import LayoutSerializer
from PySide6.QtCore import QPoint

def tutorial_4():
    app, window, drop_zone = create_app("Tutorial 4: Serialization", (800, 600))
    
    # Create initial layout
    button1 = DraggableButton("Save Layout")
    button2 = DraggableButton("Load Layout")
    label = DraggableLabel("This layout can be saved!")
    
    drop_zone.add_widget(button1, QPoint(100, 100))
    drop_zone.add_widget(button2, QPoint(250, 100))
    drop_zone.add_widget(label, QPoint(100, 200))
    
    # Save layout function
    def save_layout():
        layout_data = drop_zone.get_layout_data()
        success = LayoutSerializer.save_to_json(layout_data, 'tutorial_layout.json')
        print(f"Layout saved: {success}")
    
    # Load layout function
    def load_layout():
        layout_data = LayoutSerializer.load_from_json('tutorial_layout.json')
        if layout_data:
            drop_zone.load_layout_data(layout_data)
            print("Layout loaded successfully")
        else:
            print("Failed to load layout")
    
    # Connect button events
    button1.button_clicked.connect(lambda _: save_layout())
    button2.button_clicked.connect(lambda _: load_layout())
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(tutorial_4())
```

### Tutorial 5: Custom Events

```python
"""
Tutorial 5: Working with the event system
"""
import sys
from dragdropwidgets import create_app, DraggableButton
from dragdropwidgets.utils.events import event_manager, WidgetEvents, EventPriority
from PySide6.QtCore import QPoint

def tutorial_5():
    app, window, drop_zone = create_app("Tutorial 5: Events", (800, 600))
    
    # Create widgets
    button1 = DraggableButton("Event Source")
    button2 = DraggableButton("Another Widget")
    
    drop_zone.add_widget(button1, QPoint(100, 100))
    drop_zone.add_widget(button2, QPoint(300, 100))
    
    # Event handlers
    def on_widget_moved(event):
        widget = event.source
        position = event.data.get('position', 'unknown')
        print(f"Widget {widget.__class__.__name__} moved to {position}")
    
    def on_widget_selected(event):
        widget = event.source
        print(f"Widget selected: {widget.widget_id}")
    
    def on_custom_event(event):
        print(f"Custom event received: {event.data}")
    
    # Register event handlers
    event_manager.register_event(WidgetEvents.WIDGET_MOVED, on_widget_moved)
    event_manager.register_event(WidgetEvents.WIDGET_SELECTED, on_widget_selected)
    event_manager.register_event('custom_tutorial_event', on_custom_event)
    
    # Button click handler that emits custom event
    def on_button_click(widget_id):
        event_manager.emit_event('custom_tutorial_event', 
                               source=button1, 
                               data={'message': 'Hello from tutorial!', 'timestamp': '2024-01-15'})
    
    button1.button_clicked.connect(on_button_click)
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(tutorial_5())
```

---

## 📚 API Reference

### Core Classes

#### `create_app(title, size)`
Convenience function to create a basic application setup.

**Parameters:**
- `title` (str): Window title
- `size` (tuple): Window size as (width, height)

**Returns:**
- `app` (QApplication): The application instance
- `window` (QMainWindow): The main window
- `drop_zone` (DropZone): The central drop zone

#### `WidgetBase(parent=None)`
Base class for all widgets.

**Properties:**
- `widget_id` (str): Unique identifier
- `is_selected` (bool): Selection state
- `is_draggable` (bool): Can be dragged
- `is_resizable` (bool): Can be resized
- `is_deletable` (bool): Can be deleted
- `metadata` (dict): Custom data storage

**Methods:**
- `set_selected(selected: bool)`: Set selection state
- `set_draggable(draggable: bool)`: Enable/disable dragging
- `set_resizable(resizable: bool)`: Enable/disable resizing
- `get_properties() -> Dict`: Get serializable properties
- `set_properties(properties: Dict)`: Apply properties
- `clone() -> WidgetBase`: Create a copy
- `get_snap_points() -> Dict`: Get alignment points

**Signals:**
- `widget_selected(object)`: Emitted when selected
- `widget_moved(object, QPoint)`: Emitted when moved
- `widget_resized(object, QSize)`: Emitted when resized
- `widget_deleted(str)`: Emitted when deleted

#### `DraggableWidget(parent=None)`
Extends WidgetBase with drag and drop functionality.

**Properties:**
- `drag_threshold` (int): Pixels to start drag (default: 5)
- `snap_to_grid` (bool): Enable grid snapping
- `grid_size` (int): Grid spacing in pixels

**Methods:**
- `set_snap_to_grid(enabled: bool, grid_size: int = 20)`: Configure grid snapping
- `animate_to_position(target: QPoint, duration: int = 300)`: Animate movement
- `start_drag_operation()`: Manually start drag

**Signals:**
- `drag_started(object)`: Emitted when drag begins
- `drag_finished(object, QPoint)`: Emitted when drag ends

#### `DropZone(parent=None)`
Container widget that accepts dragged widgets.

**Properties:**
- `widgets` (List[WidgetBase]): All widgets in the zone
- `selected_widgets` (List[WidgetBase]): Currently selected widgets
- `show_grid` (bool): Grid visibility
- `grid_size` (int): Grid spacing
- `layout_mode` (str): Current layout mode ('free', 'grid', 'flow')

**Methods:**
- `add_widget(widget: WidgetBase, position: QPoint = None)`: Add widget
- `remove_widget(widget_id: str)`: Remove widget by ID
- `clear_selection()`: Deselect all widgets
- `select_all()`: Select all widgets
- `delete_selected()`: Delete selected widgets
- `set_grid_visible(visible: bool)`: Show/hide grid
- `set_layout_mode(mode: str)`: Change layout mode
- `get_layout_data() -> Dict`: Get serializable layout data
- `load_layout_data(data: Dict)`: Load layout from data

**Signals:**
- `widget_dropped(object, QPoint)`: Widget was dropped
- `widget_removed(str)`: Widget was removed
- `layout_changed()`: Layout structure changed

### Widget Classes

#### `DraggableButton(text="Button", parent=None)`

**Methods:**
- `set_text(text: str)`: Change button text
- `get_text() -> str`: Get button text
- `set_style(style: str)`: Set button style
- `set_enabled(enabled: bool)`: Enable/disable button
- `set_checkable(checkable: bool)`: Make toggleable
- `is_checked() -> bool`: Get toggle state
- `set_checked(checked: bool)`: Set toggle state

**Signals:**
- `button_clicked(str)`: Button was clicked (emits widget ID)

#### `DraggableLabel(text="Label", parent=None)`

**Methods:**
- `set_text(text: str)`: Change label text
- `get_text() -> str`: Get label text
- `set_font_size(size: int)`: Change font size
- `set_font_family(family: str)`: Change font family
- `set_font_bold(bold: bool)`: Set bold style
- `set_font_italic(italic: bool)`: Set italic style
- `set_color(color: str)`: Change text color
- `set_background_color(color: str)`: Change background
- `set_alignment(alignment: str)`: Set text alignment
- `set_word_wrap(wrap: bool)`: Enable word wrapping
- `set_style_preset(preset: str)`: Apply style preset

#### `DraggableImage(image_path=None, parent=None)`

**Methods:**
- `load_image(path: str) -> bool`: Load image from file
- `set_pixmap(pixmap: QPixmap)`: Set image directly
- `open_file_dialog() -> bool`: Show file dialog
- `save_image(path: str, quality: int = 95) -> bool`: Save image
- `set_scale_mode(mode: str)`: Set scaling mode
- `set_aspect_ratio_locked(locked: bool)`: Lock aspect ratio
- `rotate_image(angle: int)`: Rotate by degrees
- `flip_horizontal()`: Flip horizontally
- `flip_vertical()`: Flip vertically
- `get_image_info() -> Dict`: Get image information

**Signals:**
- `image_clicked(str)`: Image was clicked

### Utility Classes

#### `ThemeManager()`

**Methods:**
- `get_available_themes() -> Dict[str, str]`: List available themes
- `get_theme(theme_id: str) -> Optional[Dict]`: Get theme data
- `apply_theme(widget: QWidget, theme_id: str) -> bool`: Apply to widget
- `apply_theme_to_app(theme_id: str) -> bool`: Apply to application
- `create_custom_theme(id: str, name: str, colors: Dict, fonts: Dict = None, spacing: Dict = None)`: Create custom theme
- `delete_custom_theme(theme_id: str) -> bool`: Delete custom theme
- `export_theme(theme_id: str, file_path: str) -> bool`: Export theme
- `import_theme(file_path: str, theme_id: str) -> bool`: Import theme
- `get_current_theme() -> str`: Get current theme ID

**Signals:**
- `theme_changed(str)`: Theme was changed

#### `EventManager()`

**Methods:**
- `register_event(event_name: str, handler: Callable, priority: EventPriority = NORMAL, once: bool = False) -> str`: Register handler
- `register_global_handler(handler: Callable, priority: EventPriority = NORMAL) -> str`: Register global handler
- `emit_event(event_name: str, source: Any = None, data: Dict = None, priority: EventPriority = NORMAL) -> Event`: Emit event
- `remove_event_handler(event_name: str, handler: Callable)`: Remove handler
- `remove_all_handlers(event_name: str)`: Remove all handlers for event
- `clear_all_handlers()`: Remove all handlers
- `get_event_history(event_type: str = None, limit: int = None) -> List[Event]`: Get event history
- `get_handler_count(event_name: str = None) -> int`: Count handlers

#### `LayoutSerializer`

**Static Methods:**
- `save_to_json(data: Dict, file_path: str) -> bool`: Save layout to JSON
- `load_from_json(file_path: str) -> Optional[Dict]`: Load layout from JSON
- `save_to_yaml(data: Dict, file_path: str) -> bool`: Save layout to YAML
- `load_from_yaml(file_path: str) -> Optional[Dict]`: Load layout from YAML
- `create_backup(data: Dict, backup_dir: str = "backups") -> str`: Create backup
- `export_to_code(data: Dict, language: str = "python") -> str`: Export as code
- `merge_layouts(layout1: Dict, layout2: Dict) -> Dict`: Merge layouts
- `get_layout_statistics(data: Dict) -> Dict`: Get layout statistics

#### `CustomWidgetFactory`

**Class Methods:**
- `register_widget(name: str, widget_class: Type, metadata: Dict = None)`: Register widget type
- `create_widget(name: str, *args, **kwargs) -> Optional[WidgetBase]`: Create widget instance
- `get_available_widgets() -> List[str]`: Get registered widget names
- `get_widget_metadata(name: str) -> Dict`: Get widget metadata
- `unregister_widget(name: str)`: Remove widget type

---

## ❓ Troubleshooting

### Common Issues

#### Import Errors

**Problem:** `ImportError: libEGL.so.1: cannot open shared object file`
```python
# This occurs in headless environments (like servers)
# Solution: Use QApplication with offscreen platform
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from dragdropwidgets import create_app
```

**Problem:** `ModuleNotFoundError: No module named 'dragdropwidgets'`
```bash
# Ensure proper installation
pip install -e .

# Or check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

#### Widget Issues

**Problem:** Widgets not responding to drag
```python
# Check if dragging is enabled
widget.set_draggable(True)

# Check drag threshold
widget.drag_threshold = 5  # Lower threshold for easier dragging
```

**Problem:** Snap to grid not working
```python
# Ensure both widget and drop zone have grid enabled
widget.set_snap_to_grid(True, 20)
drop_zone.grid_size = 20
drop_zone.set_grid_visible(True)
```

#### Layout Issues

**Problem:** Layout not saving correctly
```python
# Ensure all widgets are properly added to drop zone
for widget in widgets:
    drop_zone.add_widget(widget)

# Check layout data before saving
layout_data = drop_zone.get_layout_data()
print(f"Widgets in layout: {len(layout_data.get('widgets', []))}")
```

#### Theme Issues

**Problem:** Theme not applying
```python
# Make sure to apply to application, not just widget
theme_manager.apply_theme_to_app('dark')

# For custom themes, verify theme data
theme_data = theme_manager.get_theme('custom_theme')
if not theme_data:
    print("Theme not found")
```

#### Event Issues

**Problem:** Events not firing
```python
# Check if event manager is enabled
event_manager.enable_event_manager()

# Verify handler registration
handler_count = event_manager.get_handler_count('my_event')
print(f"Handlers registered: {handler_count}")

# Check event history
history = event_manager.get_event_history('my_event', limit=10)
```

### Performance Issues

#### Large Numbers of Widgets
```python
# Disable animations for better performance
for widget in widgets:
    if hasattr(widget, 'animate_to_position'):
        # Use direct positioning instead of animation
        widget.move(target_position)

# Reduce grid resolution for smoother dragging
drop_zone.grid_size = 50  # Larger grid = better performance
```

#### Memory Usage
```python
# Properly clean up widgets when removing
def cleanup_widget(widget):
    # Disconnect signals
    widget.disconnect()
    
    # Remove from drop zone
    drop_zone.remove_widget(widget.widget_id)
    
    # Delete widget
    widget.deleteLater()
```

### Debugging Tips

#### Enable Debug Output
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Event system debugging
from dragdropwidgets.utils.events import event_manager

def debug_handler(event):
    print(f"DEBUG: {event.event_type} - {event.source}")

event_manager.register_global_handler(debug_handler)
```

#### Widget Inspector
```python
def inspect_widget(widget):
    """Debug widget properties"""
    properties = widget.get_properties()
    print(f"Widget: {properties['type']}")
    print(f"ID: {properties['id']}")
    print(f"Position: {properties['position']}")
    print(f"Size: {properties['size']}")
    print(f"Metadata: {properties['metadata']}")

# Usage
inspect_widget(my_widget)
```

#### Layout Validation
```python
def validate_layout(drop_zone):
    """Validate layout state"""
    widgets = drop_zone.widgets
    print(f"Total widgets: {len(widgets)}")
    
    for i, widget in enumerate(widgets):
        print(f"Widget {i}: {widget.__class__.__name__} at ({widget.x()}, {widget.y()})")
    
    # Check for overlapping widgets
    positions = [(w.x(), w.y()) for w in widgets]
    if len(set(positions)) != len(positions):
        print("WARNING: Overlapping widgets detected")

# Usage
validate_layout(drop_zone)
```

### Getting Help

1. **Check Examples**: Run the built-in examples to see working code
2. **Read Source**: The library is well-documented with inline comments
3. **Event Debugging**: Use the event system to understand widget behavior
4. **Community**: Check GitHub issues for similar problems

---
