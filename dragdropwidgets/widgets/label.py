"""
Draggable label widget with full customization
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from ..core.draggable import DraggableWidget
import uuid

class DraggableLabel(DraggableWidget):
    """Draggable and droppable label"""
    
    def __init__(self, text="Label", parent=None):
        super().__init__(parent)
        
        # Create internal label
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Customize appearance
        self.setStyleSheet("""
            DraggableLabel {
                background: transparent;
                border: none;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                padding: 4px 8px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 4px;
            }
        """)
        
        # Set initial size
        self.resize(80, 30)
        
        # Additional metadata
        self.metadata.update({
            'text': text,
            'font_size': 14,
            'color': '#333333',
            'alignment': 'center',
            'word_wrap': False,
            'background_color': 'rgba(255, 255, 255, 0.8)'
        })
    
    def set_text(self, text: str):
        """Change label text"""
        self.label.setText(text)
        self.metadata['text'] = text
        
        # Update size based on text
        self.label.adjustSize()
        self.resize(self.label.size())
    
    def get_text(self) -> str:
        """Get label text"""
        return self.label.text()
    
    def set_font_size(self, size: int):
        """Change font size"""
        font = self.label.font()
        font.setPointSize(size)
        self.label.setFont(font)
        self.metadata['font_size'] = size
        
        # Update size
        self.label.adjustSize()
        self.resize(self.label.size())
    
    def set_font_family(self, family: str):
        """Change font family"""
        font = self.label.font()
        font.setFamily(family)
        self.label.setFont(font)
        self.metadata['font_family'] = family
        
        # Update size
        self.label.adjustSize()
        self.resize(self.label.size())
    
    def set_font_bold(self, bold: bool):
        """Set font bold"""
        font = self.label.font()
        font.setBold(bold)
        self.label.setFont(font)
        self.metadata['font_bold'] = bold
        
        # Update size
        self.label.adjustSize()
        self.resize(self.label.size())
    
    def set_font_italic(self, italic: bool):
        """Set font italic"""
        font = self.label.font()
        font.setItalic(italic)
        self.label.setFont(font)
        self.metadata['font_italic'] = italic
        
        # Update size
        self.label.adjustSize()
        self.resize(self.label.size())
    
    def set_color(self, color: str):
        """Change text color"""
        current_style = self.label.styleSheet()
        # Replace existing color
        import re
        new_style = re.sub(r'color:\s*[^;]+;', f'color: {color};', current_style)
        if 'color:' not in new_style:
            new_style = new_style.replace('{', f'{{ color: {color};')
        
        self.label.setStyleSheet(new_style)
        self.metadata['color'] = color
    
    def set_background_color(self, color: str):
        """Change background color"""
        current_style = self.label.styleSheet()
        # Replace existing background-color
        import re
        new_style = re.sub(r'background-color:\s*[^;]+;', f'background-color: {color};', current_style)
        if 'background-color:' not in new_style:
            new_style = new_style.replace('{', f'{{ background-color: {color};')
        
        self.label.setStyleSheet(new_style)
        self.metadata['background_color'] = color
    
    def set_alignment(self, alignment: str):
        """Change text alignment"""
        alignments = {
            'left': Qt.AlignLeft | Qt.AlignVCenter,
            'center': Qt.AlignCenter,
            'right': Qt.AlignRight | Qt.AlignVCenter,
            'top': Qt.AlignHCenter | Qt.AlignTop,
            'bottom': Qt.AlignHCenter | Qt.AlignBottom,
            'top_left': Qt.AlignLeft | Qt.AlignTop,
            'top_right': Qt.AlignRight | Qt.AlignTop,
            'bottom_left': Qt.AlignLeft | Qt.AlignBottom,
            'bottom_right': Qt.AlignRight | Qt.AlignBottom
        }
        
        if alignment in alignments:
            self.label.setAlignment(alignments[alignment])
            self.metadata['alignment'] = alignment
    
    def set_word_wrap(self, wrap: bool):
        """Enable/disable word wrap"""
        self.label.setWordWrap(wrap)
        self.metadata['word_wrap'] = wrap
        
        if wrap:
            # Adjust size for word wrap
            self.label.adjustSize()
            self.resize(self.label.size())
    
    def set_pixmap(self, pixmap: QPixmap):
        """Set label to display an image"""
        self.label.setPixmap(pixmap)
        self.metadata['has_pixmap'] = True
        
        # Update size to match pixmap
        self.resize(pixmap.size())
    
    def clear_pixmap(self):
        """Clear image and return to text mode"""
        self.label.clear()
        if self.metadata.get('text'):
            self.label.setText(self.metadata['text'])
        self.metadata['has_pixmap'] = False
    
    def set_style_preset(self, preset: str):
        """Apply a predefined style preset"""
        presets = {
            'title': {
                'font_size': 24,
                'font_bold': True,
                'color': '#2c3e50',
                'alignment': 'center'
            },
            'subtitle': {
                'font_size': 18,
                'font_bold': False,
                'color': '#34495e',
                'alignment': 'center'
            },
            'body': {
                'font_size': 14,
                'font_bold': False,
                'color': '#2c3e50',
                'alignment': 'left'
            },
            'caption': {
                'font_size': 12,
                'font_bold': False,
                'color': '#7f8c8d',
                'alignment': 'left'
            },
            'warning': {
                'font_size': 14,
                'font_bold': True,
                'color': '#e67e22',
                'background_color': '#fdf2e9',
                'alignment': 'center'
            },
            'error': {
                'font_size': 14,
                'font_bold': True,
                'color': '#e74c3c',
                'background_color': '#fadbd8',
                'alignment': 'center'
            },
            'success': {
                'font_size': 14,
                'font_bold': True,
                'color': '#27ae60',
                'background_color': '#d5f4e6',
                'alignment': 'center'
            },
            'info': {
                'font_size': 14,
                'font_bold': False,
                'color': '#3498db',
                'background_color': '#ebf3fd',
                'alignment': 'center'
            }
        }
        
        if preset in presets:
            style = presets[preset]
            
            if 'font_size' in style:
                self.set_font_size(style['font_size'])
            if 'font_bold' in style:
                self.set_font_bold(style['font_bold'])
            if 'color' in style:
                self.set_color(style['color'])
            if 'background_color' in style:
                self.set_background_color(style['background_color'])
            if 'alignment' in style:
                self.set_alignment(style['alignment'])
            
            self.metadata['style_preset'] = preset
    
    def resizeEvent(self, event):
        """Update internal label size when widget is resized"""
        super().resizeEvent(event)
        self.label.resize(self.size())
    
    def clone(self):
        """Create a copy of the label"""
        cloned = DraggableLabel(self.get_text(), self.parent())
        
        # Copy label-specific properties
        metadata = self.metadata
        if 'font_size' in metadata:
            cloned.set_font_size(metadata['font_size'])
        if 'color' in metadata:
            cloned.set_color(metadata['color'])
        if 'background_color' in metadata:
            cloned.set_background_color(metadata['background_color'])
        if 'alignment' in metadata:
            cloned.set_alignment(metadata['alignment'])
        if 'word_wrap' in metadata:
            cloned.set_word_wrap(metadata['word_wrap'])
        if 'font_family' in metadata:
            cloned.set_font_family(metadata['font_family'])
        if 'font_bold' in metadata:
            cloned.set_font_bold(metadata['font_bold'])
        if 'font_italic' in metadata:
            cloned.set_font_italic(metadata['font_italic'])
        
        # Copy basic properties
        properties = self.get_properties()
        properties['id'] = str(uuid.uuid4())
        cloned.set_properties(properties)
        
        return cloned
    
    def get_properties(self) -> dict:
        """Override to include label-specific properties"""
        props = super().get_properties()
        
        # Add font properties
        font = self.label.font()
        props['metadata'].update({
            'font_family': font.family(),
            'font_bold': font.bold(),
            'font_italic': font.italic(),
            'has_pixmap': self.metadata.get('has_pixmap', False)
        })
        
        return props
    
    def set_properties(self, properties: dict):
        """Override to apply label-specific properties"""
        super().set_properties(properties)
        
        metadata = properties.get('metadata', {})
        
        # Apply text first
        if 'text' in metadata and not metadata.get('has_pixmap', False):
            self.set_text(metadata['text'])
        
        # Apply font properties
        if 'font_size' in metadata:
            self.set_font_size(metadata['font_size'])
        if 'font_family' in metadata:
            self.set_font_family(metadata['font_family'])
        if 'font_bold' in metadata:
            self.set_font_bold(metadata['font_bold'])
        if 'font_italic' in metadata:
            self.set_font_italic(metadata['font_italic'])
        
        # Apply appearance properties
        if 'color' in metadata:
            self.set_color(metadata['color'])
        if 'background_color' in metadata:
            self.set_background_color(metadata['background_color'])
        if 'alignment' in metadata:
            self.set_alignment(metadata['alignment'])
        if 'word_wrap' in metadata:
            self.set_word_wrap(metadata['word_wrap'])