"""
Draggable button widget with full customization
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal
from ..core.draggable import DraggableWidget
import uuid

class DraggableButton(DraggableWidget):
    """Draggable and droppable button"""
    
    button_clicked = Signal(str)  # Click signal with button ID
    
    def __init__(self, text="Button", parent=None):
        super().__init__(parent)
        
        # Create internal button
        self.button = QPushButton(text, self)
        self.button.clicked.connect(self._on_button_clicked)
        
        # Customize appearance
        self.setStyleSheet("""
            DraggableButton {
                background: transparent;
                border: none;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        # Set initial size
        self.resize(100, 35)
        
        # Additional metadata
        self.metadata.update({
            'text': text,
            'button_style': 'primary'
        })
    
    def _on_button_clicked(self):
        """Handle button click"""
        self.button_clicked.emit(self.widget_id)
    
    def set_text(self, text: str):
        """Change button text"""
        self.button.setText(text)
        self.metadata['text'] = text
        
        # Update size based on text
        self.button.adjustSize()
        self.resize(self.button.size())
    
    def get_text(self) -> str:
        """Get button text"""
        return self.button.text()
    
    def set_style(self, style: str):
        """Change button style"""
        styles = {
            'primary': {
                'background': '#0078d4',
                'hover': '#106ebe',
                'pressed': '#005a9e'
            },
            'secondary': {
                'background': '#6c757d',
                'hover': '#5a6268',
                'pressed': '#495057'
            },
            'success': {
                'background': '#28a745',
                'hover': '#218838',
                'pressed': '#1e7e34'
            },
            'danger': {
                'background': '#dc3545',
                'hover': '#c82333',
                'pressed': '#bd2130'
            },
            'warning': {
                'background': '#ffc107',
                'hover': '#e0a800',
                'pressed': '#d39e00'
            },
            'info': {
                'background': '#17a2b8',
                'hover': '#138496',
                'pressed': '#117a8b'
            }
        }
        
        if style in styles:
            colors = styles[style]
            text_color = 'white' if style != 'warning' else 'black'
            
            self.button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['background']};
                    color: {text_color};
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {colors['hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['pressed']};
                }}
            """)
            
            self.metadata['button_style'] = style
    
    def set_enabled(self, enabled: bool):
        """Enable/disable button"""
        self.button.setEnabled(enabled)
        self.metadata['enabled'] = enabled
    
    def set_checkable(self, checkable: bool):
        """Make button checkable (toggle button)"""
        self.button.setCheckable(checkable)
        self.metadata['checkable'] = checkable
    
    def is_checked(self) -> bool:
        """Check if toggle button is checked"""
        return self.button.isChecked()
    
    def set_checked(self, checked: bool):
        """Set toggle button state"""
        if self.button.isCheckable():
            self.button.setChecked(checked)
    
    def resizeEvent(self, event):
        """Update internal button size when widget is resized"""
        super().resizeEvent(event)
        self.button.resize(self.size())
    
    def clone(self):
        """Create a copy of the button"""
        cloned = DraggableButton(self.get_text(), self.parent())
        cloned.set_style(self.metadata.get('button_style', 'primary'))
        
        # Copy basic properties
        properties = self.get_properties()
        properties['id'] = str(uuid.uuid4())
        cloned.set_properties(properties)
        
        # Copy button-specific properties
        if 'enabled' in self.metadata:
            cloned.set_enabled(self.metadata['enabled'])
        if 'checkable' in self.metadata:
            cloned.set_checkable(self.metadata['checkable'])
        
        return cloned
    
    def get_properties(self) -> dict:
        """Override to include button-specific properties"""
        props = super().get_properties()
        props['metadata'].update({
            'enabled': self.button.isEnabled(),
            'checkable': self.button.isCheckable(),
            'checked': self.button.isChecked() if self.button.isCheckable() else False
        })
        return props
    
    def set_properties(self, properties: dict):
        """Override to apply button-specific properties"""
        super().set_properties(properties)
        
        metadata = properties.get('metadata', {})
        if 'text' in metadata:
            self.set_text(metadata['text'])
        if 'button_style' in metadata:
            self.set_style(metadata['button_style'])
        if 'enabled' in metadata:
            self.set_enabled(metadata['enabled'])
        if 'checkable' in metadata:
            self.set_checkable(metadata['checkable'])
        if 'checked' in metadata and self.button.isCheckable():
            self.set_checked(metadata['checked'])