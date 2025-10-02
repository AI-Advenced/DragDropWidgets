"""
Base class for all widgets in the DragDropWidgets library
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QObject, QPoint, QSize
from PySide6.QtGui import QPainter, QColor, QPen
from typing import Dict, Any, Optional
import uuid

class WidgetBase(QWidget):
    """Base class for all draggable and droppable widgets"""
    
    # Custom signals for events
    widget_selected = Signal(object)
    widget_moved = Signal(object, QPoint)
    widget_resized = Signal(object, QSize)
    widget_deleted = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Unique identifier for the widget
        self.widget_id = str(uuid.uuid4())
        
        # Basic properties
        self.is_selected = False
        self.is_draggable = True
        self.is_resizable = True
        self.is_deletable = True
        
        # Appearance properties
        self.border_color = QColor(0, 120, 215)  # Blue
        self.selection_color = QColor(0, 120, 215, 100)  # Transparent blue
        self.border_width = 2
        
        # Additional widget data
        self.metadata = {}
        
        # Set default size
        self.setMinimumSize(50, 30)
        
    def set_selected(self, selected: bool):
        """Set selection state for the widget"""
        if self.is_selected != selected:
            self.is_selected = selected
            self.update()  # Repaint the widget
            if selected:
                self.widget_selected.emit(self)
    
    def set_draggable(self, draggable: bool):
        """Enable/disable dragging capability"""
        self.is_draggable = draggable
    
    def set_resizable(self, resizable: bool):
        """Enable/disable resizing capability"""
        self.is_resizable = resizable
    
    def get_properties(self) -> Dict[str, Any]:
        """Get widget properties for saving"""
        return {
            'id': self.widget_id,
            'type': self.__class__.__name__,
            'position': {'x': self.x(), 'y': self.y()},
            'size': {'width': self.width(), 'height': self.height()},
            'visible': self.isVisible(),
            'draggable': self.is_draggable,
            'resizable': self.is_resizable,
            'metadata': self.metadata.copy()
        }
    
    def set_properties(self, properties: Dict[str, Any]):
        """Apply saved properties to the widget"""
        if 'position' in properties:
            pos = properties['position']
            self.move(pos['x'], pos['y'])
        
        if 'size' in properties:
            size = properties['size']
            self.resize(size['width'], size['height'])
        
        if 'visible' in properties:
            self.setVisible(properties['visible'])
        
        if 'draggable' in properties:
            self.set_draggable(properties['draggable'])
        
        if 'resizable' in properties:
            self.set_resizable(properties['resizable'])
        
        if 'metadata' in properties:
            self.metadata.update(properties['metadata'])
    
    def clone(self):
        """Create a copy of the widget"""
        # Create new instance of the same type
        cloned = self.__class__(self.parent())
        
        # Copy properties
        properties = self.get_properties()
        properties['id'] = str(uuid.uuid4())  # New ID
        cloned.set_properties(properties)
        
        return cloned
    
    def paintEvent(self, event):
        """Paint the widget with selection state"""
        super().paintEvent(event)
        
        if self.is_selected:
            painter = QPainter(self)
            
            # Draw selection background
            painter.fillRect(self.rect(), self.selection_color)
            
            # Draw selection border
            pen = QPen(self.border_color, self.border_width)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
            
            painter.end()
    
    def mousePressEvent(self, event):
        """Handle widget click"""
        self.set_selected(True)
        super().mousePressEvent(event)
    
    def get_snap_points(self):
        """Return snapping points for the widget"""
        rect = self.geometry()
        return {
            'left': rect.left(),
            'right': rect.right(),
            'top': rect.top(),
            'bottom': rect.bottom(),
            'center_x': rect.center().x(),
            'center_y': rect.center().y()
        }