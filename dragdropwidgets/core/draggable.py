"""
Implementation of drag and drop logic for widgets
"""

from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QMouseEvent, QDrag, QPixmap, QPainter
from PySide6.QtWidgets import QApplication
from .widget_base import WidgetBase
from typing import Optional

class DraggableWidget(WidgetBase):
    """Widget with drag and drop capability"""
    
    # Drag and drop specific signals
    drag_started = Signal(object)
    drag_finished = Signal(object, QPoint)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Drag variables
        self.drag_start_position = QPoint()
        self.is_dragging = False
        self.original_position = QPoint()
        
        # Drag settings
        self.drag_threshold = 5  # Minimum distance to start dragging
        self.snap_to_grid = False
        self.grid_size = 20
        
        # Enable accepting drops
        self.setAcceptDrops(True)
        
    def mousePressEvent(self, event: QMouseEvent):
        """Beginning of potential drag"""
        if event.button() == Qt.LeftButton and self.is_draggable:
            self.drag_start_position = event.pos()
            self.original_position = self.pos()
            
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse movement during drag"""
        if not (event.buttons() & Qt.LeftButton) or not self.is_draggable:
            return super().mouseMoveEvent(event)
        
        # Calculate distance traveled
        distance = (event.pos() - self.drag_start_position).manhattanLength()
        
        if distance < self.drag_threshold:
            return super().mouseMoveEvent(event)
        
        if not self.is_dragging:
            self.is_dragging = True
            self.drag_started.emit(self)
        
        # Update widget position
        new_position = self.mapToParent(event.pos() - self.drag_start_position)
        
        # Apply Snap to Grid if enabled
        if self.snap_to_grid:
            new_position = self._snap_to_grid(new_position)
        
        self.move(new_position)
        self.widget_moved.emit(self, new_position)
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """End of drag operation"""
        if self.is_dragging and event.button() == Qt.LeftButton:
            self.is_dragging = False
            final_position = self.pos()
            
            # Check if new position is valid
            if self._is_valid_position(final_position):
                self.drag_finished.emit(self, final_position)
            else:
                # Return widget to original position
                self.move(self.original_position)
        
        super().mouseReleaseEvent(event)
    
    def _snap_to_grid(self, position: QPoint) -> QPoint:
        """Apply Snap to Grid to position"""
        x = round(position.x() / self.grid_size) * self.grid_size
        y = round(position.y() / self.grid_size) * self.grid_size
        return QPoint(x, y)
    
    def _is_valid_position(self, position: QPoint) -> bool:
        """Check if the new position is valid"""
        if not self.parent():
            return True
        
        parent_rect = self.parent().rect()
        widget_rect = self.rect()
        widget_rect.moveTopLeft(position)
        
        # Ensure widget is within parent bounds
        return parent_rect.contains(widget_rect)
    
    def start_drag_operation(self):
        """Start drag operation using QDrag"""
        drag = QDrag(self)
        mimeData = drag.mimeData()
        
        # Add widget data to drag
        mimeData.setText(f"widget:{self.widget_id}")
        
        # Create widget thumbnail
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        
        # Execute drag operation
        dropAction = drag.exec_(Qt.MoveAction)
        
        return dropAction
    
    def set_snap_to_grid(self, enabled: bool, grid_size: int = 20):
        """Enable/disable Snap to Grid"""
        self.snap_to_grid = enabled
        self.grid_size = grid_size
    
    def animate_to_position(self, target_position: QPoint, duration: int = 300):
        """Animate widget to a specific position"""
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(target_position)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.animation.start()
        
        return self.animation