"""
DragDropWidgets - Professional Python library for creating interactive GUI interfaces with drag and drop support
"""

__version__ = "1.0.0"
__author__ = "DragDropWidgets Team"
__email__ = "team@dragdropwidgets.com"

# Import core components
from .core.widget_base import WidgetBase
from .core.draggable import DraggableWidget
from .core.drop_zone import DropZone
from .core.layout_manager import DynamicLayoutManager

# Import ready-to-use widgets
from .widgets.button import DraggableButton
from .widgets.label import DraggableLabel
from .widgets.image import DraggableImage

# Import utilities
from .utils.serializer import LayoutSerializer
from .utils.themes import ThemeManager
from .utils.events import EventManager

def create_app(title="DragDrop App", size=(800, 600)):
    """Create a new application with default settings"""
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QPoint
    import sys
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    window = QMainWindow()
    window.setWindowTitle(title)
    window.resize(*size)
    
    # Create main drop zone
    drop_zone = DropZone()
    window.setCentralWidget(drop_zone)
    
    return app, window, drop_zone

__all__ = [
    'WidgetBase', 'DraggableWidget', 'DropZone', 'DynamicLayoutManager',
    'DraggableButton', 'DraggableLabel', 'DraggableImage',
    'LayoutSerializer', 'ThemeManager', 'EventManager',
    'create_app'
]