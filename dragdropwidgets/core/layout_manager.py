"""
Dynamic layout management system for widgets
"""

from PySide6.QtCore import QObject, Signal, QPoint, QSize, QRect
from PySide6.QtWidgets import QWidget
from typing import List, Dict, Any, Optional
from .widget_base import WidgetBase

class DynamicLayoutManager(QObject):
    """Manager for dynamic widget layouts and arrangements"""
    
    # Layout signals
    layout_changed = Signal()
    widget_aligned = Signal(str, QPoint)
    
    def __init__(self, drop_zone=None):
        super().__init__()
        self.drop_zone = drop_zone
        self.alignment_threshold = 10  # Pixels for alignment snapping
        
    def auto_align_widgets(self, widgets: List[WidgetBase], alignment_type: str = 'left'):
        """Automatically align widgets"""
        if not widgets:
            return
        
        if alignment_type == 'left':
            min_x = min(widget.x() for widget in widgets)
            for widget in widgets:
                new_pos = QPoint(min_x, widget.y())
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
                
        elif alignment_type == 'right':
            max_x = max(widget.x() + widget.width() for widget in widgets)
            for widget in widgets:
                new_x = max_x - widget.width()
                new_pos = QPoint(new_x, widget.y())
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
                
        elif alignment_type == 'top':
            min_y = min(widget.y() for widget in widgets)
            for widget in widgets:
                new_pos = QPoint(widget.x(), min_y)
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
                
        elif alignment_type == 'bottom':
            max_y = max(widget.y() + widget.height() for widget in widgets)
            for widget in widgets:
                new_y = max_y - widget.height()
                new_pos = QPoint(widget.x(), new_y)
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
                
        elif alignment_type == 'center_horizontal':
            avg_x = sum(widget.x() + widget.width() // 2 for widget in widgets) // len(widgets)
            for widget in widgets:
                new_x = avg_x - widget.width() // 2
                new_pos = QPoint(new_x, widget.y())
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
                
        elif alignment_type == 'center_vertical':
            avg_y = sum(widget.y() + widget.height() // 2 for widget in widgets) // len(widgets)
            for widget in widgets:
                new_y = avg_y - widget.height() // 2
                new_pos = QPoint(widget.x(), new_y)
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                self.widget_aligned.emit(widget.widget_id, new_pos)
        
        self.layout_changed.emit()
    
    def distribute_widgets(self, widgets: List[WidgetBase], direction: str = 'horizontal'):
        """Distribute widgets evenly"""
        if len(widgets) < 2:
            return
        
        # Sort widgets by position
        if direction == 'horizontal':
            widgets.sort(key=lambda w: w.x())
            
            # Calculate spacing
            total_width = max(w.x() + w.width() for w in widgets) - min(w.x() for w in widgets)
            available_space = total_width - sum(w.width() for w in widgets)
            spacing = available_space / (len(widgets) - 1) if len(widgets) > 1 else 0
            
            # Position widgets
            current_x = widgets[0].x()
            for i, widget in enumerate(widgets):
                if i > 0:
                    current_x += widgets[i-1].width() + spacing
                
                new_pos = QPoint(int(current_x), widget.y())
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
                    
        elif direction == 'vertical':
            widgets.sort(key=lambda w: w.y())
            
            # Calculate spacing
            total_height = max(w.y() + w.height() for w in widgets) - min(w.y() for w in widgets)
            available_space = total_height - sum(w.height() for w in widgets)
            spacing = available_space / (len(widgets) - 1) if len(widgets) > 1 else 0
            
            # Position widgets
            current_y = widgets[0].y()
            for i, widget in enumerate(widgets):
                if i > 0:
                    current_y += widgets[i-1].height() + spacing
                
                new_pos = QPoint(widget.x(), int(current_y))
                if hasattr(widget, 'animate_to_position'):
                    widget.animate_to_position(new_pos)
                else:
                    widget.move(new_pos)
        
        self.layout_changed.emit()
    
    def resize_widgets_uniform(self, widgets: List[WidgetBase], size_type: str = 'width'):
        """Resize widgets to uniform size"""
        if not widgets:
            return
        
        if size_type == 'width':
            max_width = max(widget.width() for widget in widgets)
            for widget in widgets:
                if widget.is_resizable:
                    widget.resize(max_width, widget.height())
                    
        elif size_type == 'height':
            max_height = max(widget.height() for widget in widgets)
            for widget in widgets:
                if widget.is_resizable:
                    widget.resize(widget.width(), max_height)
                    
        elif size_type == 'both':
            max_width = max(widget.width() for widget in widgets)
            max_height = max(widget.height() for widget in widgets)
            for widget in widgets:
                if widget.is_resizable:
                    widget.resize(max_width, max_height)
        
        self.layout_changed.emit()
    
    def create_layout_grid(self, widgets: List[WidgetBase], columns: int, spacing: int = 20):
        """Arrange widgets in a grid layout"""
        if not widgets:
            return
        
        start_x, start_y = 20, 20
        if self.drop_zone:
            # Use drop zone's top-left as starting point
            start_x, start_y = 20, 20
        
        for i, widget in enumerate(widgets):
            row = i // columns
            col = i % columns
            
            x = start_x + col * (150 + spacing)
            y = start_y + row * (100 + spacing)
            
            new_pos = QPoint(x, y)
            if hasattr(widget, 'animate_to_position'):
                widget.animate_to_position(new_pos)
            else:
                widget.move(new_pos)
        
        self.layout_changed.emit()
    
    def create_circular_layout(self, widgets: List[WidgetBase], center: QPoint, radius: int = 200):
        """Arrange widgets in a circular pattern"""
        if not widgets:
            return
        
        import math
        angle_step = 2 * math.pi / len(widgets)
        
        for i, widget in enumerate(widgets):
            angle = i * angle_step
            x = center.x() + int(radius * math.cos(angle)) - widget.width() // 2
            y = center.y() + int(radius * math.sin(angle)) - widget.height() // 2
            
            new_pos = QPoint(x, y)
            if hasattr(widget, 'animate_to_position'):
                widget.animate_to_position(new_pos)
            else:
                widget.move(new_pos)
        
        self.layout_changed.emit()
    
    def get_alignment_suggestions(self, widget: WidgetBase, other_widgets: List[WidgetBase]) -> Dict[str, QPoint]:
        """Get alignment suggestions for a widget relative to others"""
        suggestions = {}
        
        widget_rect = widget.geometry()
        
        for other in other_widgets:
            if other == widget:
                continue
            
            other_rect = other.geometry()
            
            # Left alignment
            if abs(widget_rect.left() - other_rect.left()) <= self.alignment_threshold:
                suggestions['align_left'] = QPoint(other_rect.left(), widget.y())
            
            # Right alignment
            if abs(widget_rect.right() - other_rect.right()) <= self.alignment_threshold:
                new_x = other_rect.right() - widget.width()
                suggestions['align_right'] = QPoint(new_x, widget.y())
            
            # Top alignment
            if abs(widget_rect.top() - other_rect.top()) <= self.alignment_threshold:
                suggestions['align_top'] = QPoint(widget.x(), other_rect.top())
            
            # Bottom alignment
            if abs(widget_rect.bottom() - other_rect.bottom()) <= self.alignment_threshold:
                new_y = other_rect.bottom() - widget.height()
                suggestions['align_bottom'] = QPoint(widget.x(), new_y)
            
            # Center alignment
            widget_center_x = widget_rect.center().x()
            other_center_x = other_rect.center().x()
            if abs(widget_center_x - other_center_x) <= self.alignment_threshold:
                new_x = other_center_x - widget.width() // 2
                suggestions['align_center_h'] = QPoint(new_x, widget.y())
            
            widget_center_y = widget_rect.center().y()
            other_center_y = other_rect.center().y()
            if abs(widget_center_y - other_center_y) <= self.alignment_threshold:
                new_y = other_center_y - widget.height() // 2
                suggestions['align_center_v'] = QPoint(widget.x(), new_y)
        
        return suggestions
    
    def apply_alignment_suggestion(self, widget: WidgetBase, suggestion_key: str, suggested_position: QPoint):
        """Apply an alignment suggestion to a widget"""
        if hasattr(widget, 'animate_to_position'):
            widget.animate_to_position(suggested_position)
        else:
            widget.move(suggested_position)
        
        self.widget_aligned.emit(widget.widget_id, suggested_position)
        self.layout_changed.emit()