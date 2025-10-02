"""
Main drop zone that receives dragged widgets
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication
from PySide6.QtCore import Qt, Signal, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QDragEnterEvent, QDropEvent, QDragMoveEvent
from typing import List, Optional, Dict, Any
from .widget_base import WidgetBase
from .draggable import DraggableWidget

class DropZone(QFrame):
    """Widget drop zone with support for different layouts"""
    
    # Event signals
    widget_dropped = Signal(object, QPoint)
    widget_removed = Signal(str)
    layout_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # List of widgets in the zone
        self.widgets: List[WidgetBase] = []
        self.selected_widgets: List[WidgetBase] = []
        
        # Zone settings
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 300)
        
        # Grid settings
        self.show_grid = True
        self.grid_size = 20
        self.grid_color = QColor(200, 200, 200, 100)
        
        # Appearance settings
        self.background_color = QColor(250, 250, 250)
        self.border_color = QColor(180, 180, 180)
        self.drop_highlight_color = QColor(0, 120, 215, 50)
        
        # Drop state
        self.is_drop_target = False
        
        # Layout mode
        self.layout_mode = 'free'  # 'free', 'grid', 'flow'
        
        self.setStyleSheet("""
            DropZone {
                background-color: #fafafa;
                border: 2px dashed #b4b4b4;
                border-radius: 8px;
            }
        """)
    
    def add_widget(self, widget: WidgetBase, position: Optional[QPoint] = None):
        """Add a new widget to the zone"""
        if widget not in self.widgets:
            self.widgets.append(widget)
            widget.setParent(self)
            
            # Set position
            if position:
                widget.move(position)
            else:
                widget.move(len(self.widgets) * 50, len(self.widgets) * 30)
            
            # Connect signals
            widget.widget_selected.connect(self._on_widget_selected)
            widget.widget_moved.connect(self._on_widget_moved)
            
            widget.show()
            self.layout_changed.emit()
    
    def remove_widget(self, widget_id: str):
        """Remove widget from the zone"""
        for widget in self.widgets[:]:
            if widget.widget_id == widget_id:
                self.widgets.remove(widget)
                if widget in self.selected_widgets:
                    self.selected_widgets.remove(widget)
                
                widget.setParent(None)
                widget.deleteLater()
                
                self.widget_removed.emit(widget_id)
                self.layout_changed.emit()
                break
    
    def clear_selection(self):
        """Clear all widget selections"""
        for widget in self.selected_widgets:
            widget.set_selected(False)
        self.selected_widgets.clear()
    
    def select_all(self):
        """Select all widgets"""
        self.clear_selection()
        for widget in self.widgets:
            widget.set_selected(True)
            self.selected_widgets.append(widget)
    
    def delete_selected(self):
        """Delete selected widgets"""
        for widget in self.selected_widgets[:]:
            if widget.is_deletable:
                self.remove_widget(widget.widget_id)
    
    def _on_widget_selected(self, widget: WidgetBase):
        """Handle widget selection"""
        if not QApplication.keyboardModifiers() & Qt.ControlModifier:
            # Clear other selections if Ctrl not pressed
            for w in self.selected_widgets:
                if w != widget:
                    w.set_selected(False)
            self.selected_widgets = [widget]
        else:
            # Add to multi-selection
            if widget not in self.selected_widgets:
                self.selected_widgets.append(widget)
    
    def _on_widget_moved(self, widget: WidgetBase, position: QPoint):
        """Handle widget movement"""
        self.update()  # Redraw grid
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept drag start"""
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if text.startswith("widget:"):
                event.acceptProposedAction()
                self.is_drop_target = True
                self.update()
    
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Follow drag movement"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dragLeaveEvent(self, event):
        """Leave drag area"""
        self.is_drop_target = False
        self.update()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop"""
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if text.startswith("widget:"):
                widget_id = text.split(":")[1]
                
                # Find the widget
                for widget in self.widgets:
                    if widget.widget_id == widget_id:
                        # Update widget position
                        drop_position = event.pos()
                        
                        # Apply Snap to Grid if enabled
                        if hasattr(widget, 'snap_to_grid') and widget.snap_to_grid:
                            drop_position = self._snap_to_grid(drop_position)
                        
                        widget.move(drop_position)
                        self.widget_dropped.emit(widget, drop_position)
                        break
                
                event.acceptProposedAction()
        
        self.is_drop_target = False
        self.update()
    
    def _snap_to_grid(self, position: QPoint) -> QPoint:
        """Apply Snap to Grid to a position"""
        x = round(position.x() / self.grid_size) * self.grid_size
        y = round(position.y() / self.grid_size) * self.grid_size
        return QPoint(x, y)
    
    def set_grid_visible(self, visible: bool):
        """Show/hide grid"""
        self.show_grid = visible
        self.update()
    
    def set_layout_mode(self, mode: str):
        """Change layout mode"""
        if mode in ['free', 'grid', 'flow']:
            self.layout_mode = mode
            self._apply_layout_mode()
    
    def _apply_layout_mode(self):
        """Apply the selected layout mode"""
        if self.layout_mode == 'grid':
            self._arrange_in_grid()
        elif self.layout_mode == 'flow':
            self._arrange_in_flow()
        # free mode doesn't need special handling
    
    def _arrange_in_grid(self):
        """Arrange widgets in a grid"""
        columns = max(1, self.width() // 150)  # Number of columns
        
        for i, widget in enumerate(self.widgets):
            row = i // columns
            col = i % columns
            
            x = col * 150 + 20
            y = row * 100 + 20
            
            if hasattr(widget, 'animate_to_position'):
                widget.animate_to_position(QPoint(x, y))
            else:
                widget.move(x, y)
    
    def _arrange_in_flow(self):
        """Arrange widgets in a flow"""
        x, y = 20, 20
        max_height = 0
        
        for widget in self.widgets:
            if x + widget.width() > self.width() - 20:
                x = 20
                y += max_height + 10
                max_height = 0
            
            if hasattr(widget, 'animate_to_position'):
                widget.animate_to_position(QPoint(x, y))
            else:
                widget.move(x, y)
            x += widget.width() + 10
            max_height = max(max_height, widget.height())
    
    def paintEvent(self, event):
        """Paint the zone with grid and drop effects"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        
        # Draw grid
        if self.show_grid:
            self._draw_grid(painter)
        
        # Draw drop highlight
        if self.is_drop_target:
            self._draw_drop_highlight(painter)
        
        painter.end()
    
    def _draw_grid(self, painter: QPainter):
        """Draw background grid"""
        painter.setPen(QPen(self.grid_color, 1, Qt.DotLine))
        
        # Vertical lines
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())
        
        # Horizontal lines
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)
    
    def _draw_drop_highlight(self, painter: QPainter):
        """Draw drop zone highlight effect"""
        painter.fillRect(self.rect(), self.drop_highlight_color)
        
        pen = QPen(QColor(0, 120, 215), 3, Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(2, 2, -2, -2))
    
    def get_layout_data(self) -> Dict[str, Any]:
        """Get layout data for saving"""
        return {
            'layout_mode': self.layout_mode,
            'grid_size': self.grid_size,
            'show_grid': self.show_grid,
            'widgets': [widget.get_properties() for widget in self.widgets]
        }
    
    def load_layout_data(self, data: Dict[str, Any]):
        """Load saved layout data"""
        # Clear current widgets
        for widget in self.widgets[:]:
            self.remove_widget(widget.widget_id)
        
        # Apply settings
        self.set_layout_mode(data.get('layout_mode', 'free'))
        self.grid_size = data.get('grid_size', 20)
        self.set_grid_visible(data.get('show_grid', True))
        
        # Create widgets from data
        for widget_data in data.get('widgets', []):
            widget_type = widget_data.get('type')
            
            # Create appropriate widget (needs widget factory)
            widget = self._create_widget_from_type(widget_type)
            if widget:
                widget.set_properties(widget_data)
                self.add_widget(widget)
    
    def _create_widget_from_type(self, widget_type: str) -> Optional[WidgetBase]:
        """Create widget from specified type"""
        # Widget factory can be extended here to support different types
        from ..widgets.button import DraggableButton
        from ..widgets.label import DraggableLabel
        
        widget_classes = {
            'DraggableButton': DraggableButton,
            'DraggableLabel': DraggableLabel,
        }
        
        widget_class = widget_classes.get(widget_type)
        if widget_class:
            return widget_class()
        
        return None