# 🎯 DragDropWidgets

**Professional Python library for creating interactive GUI interfaces with drag and drop support**

DragDropWidgets is a powerful, easy-to-use library built on PySide6 that allows developers to create modern, interactive desktop applications with intuitive drag-and-drop functionality. Perfect for building dashboard applications, visual editors, and dynamic user interfaces.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.4+-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<img width="1384" height="789" alt="image" src="https://github.com/user-attachments/assets/4ba2ec16-24c0-4308-826a-26c7dd43e2db" />



## ✨ Features

### 🎮 Core Functionality
- **Drag & Drop**: Intuitive drag-and-drop interface for all widgets
- **Snap to Grid**: Automatic alignment with customizable grid sizes
- **Multi-Selection**: Ctrl+Click to select multiple widgets
- **Visual Feedback**: Real-time visual feedback during drag operations
- **Undo/Redo**: Complete undo/redo system for all operations

### 🧩 Widget Library
- **DraggableButton**: Interactive buttons with multiple styles
- **DraggableLabel**: Text labels with rich formatting options
- **DraggableImage**: Image widgets with transformation capabilities
- **DraggableProgressBar**: Progress indicators for status display
- **DraggableSlider**: Value input sliders
- **DraggableTextEdit**: Multi-line text input areas
- **Custom Widgets**: Extensible system for creating custom widgets

### 🎨 Theming & Styling
- **Multiple Themes**: Light, Dark, Blue, Green, High Contrast
- **Custom Themes**: Create and import your own themes
- **Dynamic Styling**: Change themes at runtime
- **Accessibility**: High contrast mode for accessibility compliance

### 💾 Serialization & Export
- **Layout Persistence**: Save/load layouts in JSON or YAML format
- **Code Generation**: Export layouts as executable Python code
- **Backup System**: Automatic backup creation with timestamps
- **Layout Validation**: Built-in validation for layout files

### 🔧 Advanced Features
- **Layout Managers**: Grid, Flow, and Free layout modes
- **Event System**: Comprehensive event handling and custom events
- **Property Panels**: Real-time property editing
- **Widget Factory**: Extensible widget creation system
- **Animation Support**: Smooth animations for widget movements

## 🚀 Quick Start

### Installation

```bash
pip install dragdropwidgets
```

### Hello World Example

```python
import sys
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from PySide6.QtCore import QPoint

# Create application
app, window, drop_zone = create_app("My App", (800, 600))

# Create widgets
button = DraggableButton("Click me!")
button.set_style('primary')

label = DraggableLabel("Drag me around!")
label.set_font_size(16)

# Add to drop zone
drop_zone.add_widget(button, QPoint(100, 100))
drop_zone.add_widget(label, QPoint(100, 200))

# Enable snap to grid
button.set_snap_to_grid(True, 25)
label.set_snap_to_grid(True, 25)

# Show and run
window.show()
sys.exit(app.exec())
```

## 📚 Examples

### Run Built-in Examples

```bash
# Simple Hello World
python -m dragdropwidgets.examples.hello_world

# Advanced Dashboard Designer
python -m dragdropwidgets.examples.dashboard
```

Or using console scripts:

```bash
# After installation
dragdrop-hello
dragdrop-dashboard
```

### Creating Custom Widgets

```python
from dragdropwidgets import DraggableWidget
from PySide6.QtWidgets import QLabel

class MyCustomWidget(DraggableWidget):
    def __init__(self, text="Custom", parent=None):
        super().__init__(parent)
        
        self.label = QLabel(text, self)
        self.resize(120, 40)
        
        # Add custom functionality
        self.setStyleSheet("""
            MyCustomWidget {
                background-color: #e74c3c;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)

# Register with factory
from dragdropwidgets.widgets.custom import CustomWidgetFactory
CustomWidgetFactory.register_widget('MyCustomWidget', MyCustomWidget)
```

### Theme Management

```python
from dragdropwidgets.utils.themes import ThemeManager

theme_manager = ThemeManager()

# Apply built-in theme
theme_manager.apply_theme_to_app('dark')

# Create custom theme
theme_manager.create_custom_theme('my_theme', 'My Theme', {
    'background': '#2c3e50',
    'foreground': '#ecf0f1',
    'accent': '#e74c3c',
    'border': '#34495e'
})

# Apply custom theme
theme_manager.apply_theme_to_app('my_theme')
```

### Layout Serialization

```python
from dragdropwidgets.utils.serializer import LayoutSerializer

# Save layout
layout_data = drop_zone.get_layout_data()
LayoutSerializer.save_to_json(layout_data, 'my_layout.json')

# Load layout
layout_data = LayoutSerializer.load_from_json('my_layout.json')
drop_zone.load_layout_data(layout_data)

# Export as Python code
code = LayoutSerializer.export_to_code(layout_data, 'python')
print(code)
```

### Event Handling

```python
from dragdropwidgets.utils.events import event_manager, WidgetEvents

def on_widget_moved(event):
    widget = event.source
    position = event.data.get('position')
    print(f"Widget {widget.widget_id} moved to {position}")

# Register event handler
event_manager.register_event(WidgetEvents.WIDGET_MOVED, on_widget_moved)

# Emit custom events
event_manager.emit_event('custom_event', source=widget, data={'key': 'value'})
```

## 🎯 Use Cases

### Dashboard Applications
Create interactive dashboards with draggable widgets, real-time data display, and customizable layouts.

### Visual Editors
Build visual editing tools for forms, reports, or user interfaces with drag-and-drop functionality.

### Prototyping Tools
Rapidly prototype desktop applications with interactive components and instant visual feedback.

### Educational Software
Create interactive learning environments where users can manipulate and arrange visual elements.

### Configuration UIs
Build user-friendly configuration interfaces for complex applications with visual widget arrangement.

## 🏗️ Architecture

```
dragdropwidgets/
├── core/                   # Core functionality
│   ├── widget_base.py     # Base widget class
│   ├── draggable.py       # Drag & drop logic
│   ├── drop_zone.py       # Drop zone container
│   └── layout_manager.py  # Layout management
├── widgets/               # Ready-to-use widgets
│   ├── button.py         # Draggable buttons
│   ├── label.py          # Text labels
│   ├── image.py          # Image widgets
│   └── custom.py         # Custom widget factory
├── utils/                # Utilities
│   ├── serializer.py     # Layout serialization
│   ├── themes.py         # Theme management
│   └── events.py         # Event system
└── examples/             # Example applications
    ├── hello_world.py    # Simple example
    └── dashboard.py      # Advanced example
```

## 🎨 Widget Gallery

### Basic Widgets
- **Buttons**: Primary, Secondary, Success, Warning, Danger, Info styles
- **Labels**: Title, Subtitle, Body, Caption with full typography control
- **Images**: Scalable images with transformation and filtering options

### Input Widgets  
- **Text Edit**: Multi-line text input with formatting
- **Sliders**: Horizontal/vertical value selection
- **Progress Bars**: Animated progress indicators

### Container Widgets
- **Dashboard Panels**: Titled containers for grouping widgets
- **Tabs**: Tabbed interface containers
- **Frames**: Decorative frames and borders

## 🔌 Extensibility

### Custom Widget Development
```python
class MyWidget(DraggableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Your custom implementation
        
    def paintEvent(self, event):
        # Custom painting
        super().paintEvent(event)
        
    def mousePressEvent(self, event):
        # Custom interaction
        super().mousePressEvent(event)
```

### Plugin System
Register custom widgets, themes, and event handlers to extend functionality:

```python
# Register custom widget type
CustomWidgetFactory.register_widget('MyWidget', MyWidget, {
    'description': 'My custom widget',
    'category': 'Custom',
    'properties': {...}
})

# Register custom theme
theme_manager.create_custom_theme('corporate', 'Corporate Theme', {...})

# Register event handlers
event_manager.register_event('my_event', my_handler)
```

## 📖 Documentation

### API Reference
- [Core Classes](docs/api/core.md)
- [Widget Library](docs/api/widgets.md)
- [Utilities](docs/api/utils.md)
- [Events](docs/api/events.md)

### Tutorials
- [Getting Started](docs/tutorials/getting-started.md)
- [Creating Custom Widgets](docs/tutorials/custom-widgets.md)
- [Theme Development](docs/tutorials/themes.md)
- [Advanced Layouts](docs/tutorials/layouts.md)

### Examples
- [Hello World](dragdropwidgets/examples/hello_world.py)
- [Dashboard Designer](dragdropwidgets/examples/dashboard.py)
- [Custom Widgets Demo](docs/examples/custom-widgets.md)

## 🛠️ Development

### Requirements
- Python 3.8+
- PySide6 6.4+
- PyYAML 6.0+

### Development Setup
```bash
# Clone repository
git clone https://github.com/dragdropwidgets/dragdropwidgets.git
cd dragdropwidgets

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run examples
python -m dragdropwidgets.examples.hello_world
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dragdropwidgets

# Run specific test
pytest tests/test_widgets.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🧩 Create new widget types
- 🎨 Design new themes
- ✨ Add example applications

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📋 Roadmap

### Version 1.1 (Next Release)
- [ ] Animation system improvements
- [ ] Advanced layout constraints
- [ ] Widget grouping and layers
- [ ] Improved accessibility features
- [ ] Performance optimizations

### Version 1.2 (Future)
- [ ] Web export capabilities
- [ ] Plugin marketplace
- [ ] Visual scripting system
- [ ] Collaborative editing
- [ ] Mobile touch support

## 🐛 Known Issues

- Grid snapping performance with large numbers of widgets
- Theme switching may require application restart in some cases
- Image widget memory usage with large files

See [Issues](https://github.com/dragdropwidgets/dragdropwidgets/issues) for complete list.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the excellent [PySide6](https://doc.qt.io/qtforpython/) framework
- Inspired by modern drag-and-drop interfaces
- Thanks to all contributors and users

## 📞 Support

- 📧 Email: support@dragdropwidgets.com
- 💬 Discussions: [GitHub Discussions](https://github.com/dragdropwidgets/dragdropwidgets/discussions)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/dragdropwidgets/dragdropwidgets/issues)
- 📖 Documentation: [Read the Docs](https://dragdropwidgets.readthedocs.io/)

---

**Made with ❤️ by the DragDropWidgets team**
