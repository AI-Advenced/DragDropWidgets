"""
Custom widget factory for extensible widget creation
"""

from typing import Dict, Type, Any, Optional
from ..core.widget_base import WidgetBase
from ..core.draggable import DraggableWidget

class CustomWidgetFactory:
    """Factory for creating custom widgets"""
    
    _widget_classes: Dict[str, Type[WidgetBase]] = {}
    _widget_metadata: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register_widget(cls, name: str, widget_class: Type[WidgetBase], 
                       metadata: Optional[Dict[str, Any]] = None):
        """Register a custom widget type"""
        if not issubclass(widget_class, WidgetBase):
            raise ValueError(f"Widget class must inherit from WidgetBase")
        
        cls._widget_classes[name] = widget_class
        cls._widget_metadata[name] = metadata or {}
    
    @classmethod
    def create_widget(cls, name: str, *args, **kwargs) -> Optional[WidgetBase]:
        """Create widget from registered name"""
        if name in cls._widget_classes:
            widget_class = cls._widget_classes[name]
            return widget_class(*args, **kwargs)
        return None
    
    @classmethod
    def get_available_widgets(cls) -> list:
        """Get list of available widget names"""
        return list(cls._widget_classes.keys())
    
    @classmethod
    def get_widget_metadata(cls, name: str) -> Dict[str, Any]:
        """Get metadata for a widget type"""
        return cls._widget_metadata.get(name, {})
    
    @classmethod
    def unregister_widget(cls, name: str):
        """Remove a widget type from the factory"""
        if name in cls._widget_classes:
            del cls._widget_classes[name]
        if name in cls._widget_metadata:
            del cls._widget_metadata[name]

# Pre-register built-in widgets
def _register_builtin_widgets():
    """Register built-in widget types"""
    from .button import DraggableButton
    from .label import DraggableLabel
    from .image import DraggableImage
    
    CustomWidgetFactory.register_widget(
        'DraggableButton', 
        DraggableButton,
        {
            'description': 'Interactive button with click events',
            'category': 'Input',
            'icon': '🔘',
            'default_size': (100, 35),
            'properties': {
                'text': {'type': 'string', 'default': 'Button'},
                'style': {
                    'type': 'choice', 
                    'choices': ['primary', 'secondary', 'success', 'danger', 'warning', 'info'],
                    'default': 'primary'
                },
                'enabled': {'type': 'bool', 'default': True},
                'checkable': {'type': 'bool', 'default': False}
            }
        }
    )
    
    CustomWidgetFactory.register_widget(
        'DraggableLabel',
        DraggableLabel,
        {
            'description': 'Text display with formatting options',
            'category': 'Display',
            'icon': '📝',
            'default_size': (80, 30),
            'properties': {
                'text': {'type': 'string', 'default': 'Label'},
                'font_size': {'type': 'int', 'default': 14, 'min': 8, 'max': 72},
                'color': {'type': 'color', 'default': '#333333'},
                'alignment': {
                    'type': 'choice',
                    'choices': ['left', 'center', 'right', 'top', 'bottom'],
                    'default': 'center'
                },
                'word_wrap': {'type': 'bool', 'default': False}
            }
        }
    )
    
    CustomWidgetFactory.register_widget(
        'DraggableImage',
        DraggableImage,
        {
            'description': 'Image display with scaling and transformation',
            'category': 'Media',
            'icon': '🖼️',
            'default_size': (150, 100),
            'properties': {
                'image_path': {'type': 'file', 'filter': 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)'},
                'scale_mode': {
                    'type': 'choice',
                    'choices': ['keep_aspect_ratio', 'ignore_aspect_ratio', 'keep_aspect_ratio_by_expanding'],
                    'default': 'keep_aspect_ratio'
                },
                'aspect_ratio_locked': {'type': 'bool', 'default': True}
            }
        }
    )

# Initialize built-in widgets
_register_builtin_widgets()

# Example custom widgets that can be created

class DraggableProgressBar(DraggableWidget):
    """Custom progress bar widget"""
    
    def __init__(self, value=0, parent=None):
        super().__init__(parent)
        
        from PySide6.QtWidgets import QProgressBar
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(value)
        
        self.resize(200, 25)
        
        self.metadata.update({
            'value': value,
            'minimum': 0,
            'maximum': 100
        })
    
    def set_value(self, value: int):
        """Set progress value"""
        self.progress_bar.setValue(value)
        self.metadata['value'] = value
    
    def set_range(self, minimum: int, maximum: int):
        """Set progress range"""
        self.progress_bar.setRange(minimum, maximum)
        self.metadata['minimum'] = minimum
        self.metadata['maximum'] = maximum
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.progress_bar.resize(self.size())

class DraggableSlider(DraggableWidget):
    """Custom slider widget"""
    
    def __init__(self, value=50, parent=None):
        super().__init__(parent)
        
        from PySide6.QtWidgets import QSlider
        from PySide6.QtCore import Qt
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(value)
        self.slider.setRange(0, 100)
        
        self.resize(200, 30)
        
        self.metadata.update({
            'value': value,
            'minimum': 0,
            'maximum': 100,
            'orientation': 'horizontal'
        })
    
    def set_value(self, value: int):
        """Set slider value"""
        self.slider.setValue(value)
        self.metadata['value'] = value
    
    def set_range(self, minimum: int, maximum: int):
        """Set slider range"""
        self.slider.setRange(minimum, maximum)
        self.metadata['minimum'] = minimum
        self.metadata['maximum'] = maximum
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.slider.resize(self.size())

class DraggableTextEdit(DraggableWidget):
    """Custom text edit widget"""
    
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        
        from PySide6.QtWidgets import QTextEdit
        
        self.text_edit = QTextEdit(text, self)
        
        self.resize(200, 100)
        
        self.metadata.update({
            'text': text,
            'read_only': False
        })
    
    def set_text(self, text: str):
        """Set text content"""
        self.text_edit.setPlainText(text)
        self.metadata['text'] = text
    
    def get_text(self) -> str:
        """Get text content"""
        return self.text_edit.toPlainText()
    
    def set_read_only(self, read_only: bool):
        """Set read-only mode"""
        self.text_edit.setReadOnly(read_only)
        self.metadata['read_only'] = read_only
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.text_edit.resize(self.size())

# Register example custom widgets
CustomWidgetFactory.register_widget(
    'DraggableProgressBar',
    DraggableProgressBar,
    {
        'description': 'Progress bar for showing completion status',
        'category': 'Display',
        'icon': '📊',
        'default_size': (200, 25),
        'properties': {
            'value': {'type': 'int', 'default': 0, 'min': 0, 'max': 100},
            'minimum': {'type': 'int', 'default': 0},
            'maximum': {'type': 'int', 'default': 100}
        }
    }
)

CustomWidgetFactory.register_widget(
    'DraggableSlider',
    DraggableSlider,
    {
        'description': 'Slider for selecting values from a range',
        'category': 'Input',
        'icon': '🎚️',
        'default_size': (200, 30),
        'properties': {
            'value': {'type': 'int', 'default': 50, 'min': 0, 'max': 100},
            'minimum': {'type': 'int', 'default': 0},
            'maximum': {'type': 'int', 'default': 100}
        }
    }
)

CustomWidgetFactory.register_widget(
    'DraggableTextEdit',
    DraggableTextEdit,
    {
        'description': 'Multi-line text input and display',
        'category': 'Input',
        'icon': '📄',
        'default_size': (200, 100),
        'properties': {
            'text': {'type': 'text', 'default': ''},
            'read_only': {'type': 'bool', 'default': False}
        }
    }
)