"""
Draggable image widget with full customization
"""

from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from ..core.draggable import DraggableWidget
import uuid
import os

class DraggableImage(DraggableWidget):
    """Draggable and droppable image widget"""
    
    image_clicked = Signal(str)  # Click signal with image ID
    
    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)
        
        # Create internal label for image display
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        
        # Image properties
        self.original_pixmap = None
        self.scaled_pixmap = None
        self.image_path = image_path
        
        # Scaling properties
        self.aspect_ratio_locked = True
        self.scale_mode = Qt.KeepAspectRatio
        
        # Customize appearance
        self.setStyleSheet("""
            DraggableImage {
                background: transparent;
                border: 2px dashed #cccccc;
                border-radius: 8px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        
        # Set initial size
        self.resize(150, 100)
        
        # Additional metadata
        self.metadata.update({
            'image_path': image_path,
            'scale_mode': 'keep_aspect_ratio',
            'aspect_ratio_locked': True,
            'has_image': False
        })
        
        # Load initial image if provided
        if image_path:
            self.load_image(image_path)
        else:
            self._set_placeholder()
    
    def _set_placeholder(self):
        """Set placeholder when no image is loaded"""
        self.image_label.setText("📷\nClick to load image")
        self.image_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
                text-align: center;
            }
        """)
        self.metadata['has_image'] = False
    
    def load_image(self, image_path: str) -> bool:
        """Load image from file path"""
        if not os.path.exists(image_path):
            return False
        
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return False
        
        self.original_pixmap = pixmap
        self.image_path = image_path
        self.metadata['image_path'] = image_path
        self.metadata['has_image'] = True
        
        # Update display
        self._update_image_display()
        
        # Update widget size to fit image (if not manually resized)
        if self.width() == 150 and self.height() == 100:  # Default size
            self._fit_to_image()
        
        return True
    
    def set_pixmap(self, pixmap: QPixmap):
        """Set image from QPixmap object"""
        if pixmap and not pixmap.isNull():
            self.original_pixmap = pixmap
            self.image_path = None  # No file path for direct pixmap
            self.metadata['image_path'] = None
            self.metadata['has_image'] = True
            
            self._update_image_display()
            
            # Update widget size if default
            if self.width() == 150 and self.height() == 100:
                self._fit_to_image()
    
    def _update_image_display(self):
        """Update the displayed image based on current size and settings"""
        if not self.original_pixmap:
            return
        
        # Scale pixmap to fit widget size
        widget_size = self.size()
        
        if self.scale_mode == Qt.KeepAspectRatio:
            self.scaled_pixmap = self.original_pixmap.scaled(
                widget_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        elif self.scale_mode == Qt.IgnoreAspectRatio:
            self.scaled_pixmap = self.original_pixmap.scaled(
                widget_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
        else:  # KeepAspectRatioByExpanding
            self.scaled_pixmap = self.original_pixmap.scaled(
                widget_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
        
        self.image_label.setPixmap(self.scaled_pixmap)
        self.image_label.setText("")  # Clear placeholder text
    
    def _fit_to_image(self):
        """Resize widget to fit the original image size (with limits)"""
        if not self.original_pixmap:
            return
        
        # Set maximum size limits
        max_width, max_height = 400, 300
        
        image_size = self.original_pixmap.size()
        width = min(image_size.width(), max_width)
        height = min(image_size.height(), max_height)
        
        # Maintain aspect ratio if locked
        if self.aspect_ratio_locked:
            aspect_ratio = image_size.width() / image_size.height()
            if width / height > aspect_ratio:
                width = int(height * aspect_ratio)
            else:
                height = int(width / aspect_ratio)
        
        self.resize(width, height)
    
    def set_scale_mode(self, mode: str):
        """Set image scaling mode"""
        modes = {
            'keep_aspect_ratio': Qt.KeepAspectRatio,
            'ignore_aspect_ratio': Qt.IgnoreAspectRatio,
            'keep_aspect_ratio_by_expanding': Qt.KeepAspectRatioByExpanding
        }
        
        if mode in modes:
            self.scale_mode = modes[mode]
            self.metadata['scale_mode'] = mode
            self._update_image_display()
    
    def set_aspect_ratio_locked(self, locked: bool):
        """Lock/unlock aspect ratio for resizing"""
        self.aspect_ratio_locked = locked
        self.metadata['aspect_ratio_locked'] = locked
    
    def rotate_image(self, angle: int):
        """Rotate image by specified angle (90, 180, 270 degrees)"""
        if not self.original_pixmap:
            return
        
        if angle % 90 != 0:
            return  # Only allow 90-degree rotations
        
        # Create transformation
        transform = self.original_pixmap.transform()
        transform = transform.rotate(angle)
        
        # Apply transformation
        self.original_pixmap = self.original_pixmap.transformed(transform)
        self._update_image_display()
    
    def flip_horizontal(self):
        """Flip image horizontally"""
        if not self.original_pixmap:
            return
        
        self.original_pixmap = self.original_pixmap.transformed(
            self.original_pixmap.transform().scale(-1, 1)
        )
        self._update_image_display()
    
    def flip_vertical(self):
        """Flip image vertically"""
        if not self.original_pixmap:
            return
        
        self.original_pixmap = self.original_pixmap.transformed(
            self.original_pixmap.transform().scale(1, -1)
        )
        self._update_image_display()
    
    def open_file_dialog(self):
        """Open file dialog to select an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
        )
        
        if file_path:
            return self.load_image(file_path)
        return False
    
    def save_image(self, file_path: str, quality: int = 95) -> bool:
        """Save current image to file"""
        if not self.original_pixmap:
            return False
        
        return self.original_pixmap.save(file_path, quality=quality)
    
    def get_image_info(self) -> dict:
        """Get information about the current image"""
        if not self.original_pixmap:
            return {}
        
        size = self.original_pixmap.size()
        return {
            'width': size.width(),
            'height': size.height(),
            'has_alpha': self.original_pixmap.hasAlphaChannel(),
            'depth': self.original_pixmap.depth(),
            'file_path': self.image_path
        }
    
    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        if event.button() == Qt.LeftButton:
            if not self.metadata.get('has_image', False):
                # Open file dialog if no image is loaded
                self.open_file_dialog()
            else:
                # Emit click signal
                self.image_clicked.emit(self.widget_id)
        
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """Update image display when widget is resized"""
        super().resizeEvent(event)
        
        # Resize internal label
        self.image_label.resize(self.size())
        
        # Update image display
        if self.original_pixmap:
            self._update_image_display()
    
    def clone(self):
        """Create a copy of the image widget"""
        cloned = DraggableImage(self.image_path, self.parent())
        
        # Copy image-specific properties
        if self.original_pixmap:
            cloned.set_pixmap(self.original_pixmap.copy())
        
        cloned.set_scale_mode(self.metadata.get('scale_mode', 'keep_aspect_ratio'))
        cloned.set_aspect_ratio_locked(self.metadata.get('aspect_ratio_locked', True))
        
        # Copy basic properties
        properties = self.get_properties()
        properties['id'] = str(uuid.uuid4())
        cloned.set_properties(properties)
        
        return cloned
    
    def get_properties(self) -> dict:
        """Override to include image-specific properties"""
        props = super().get_properties()
        
        # Add image info
        if self.original_pixmap:
            image_info = self.get_image_info()
            props['metadata'].update(image_info)
        
        return props
    
    def set_properties(self, properties: dict):
        """Override to apply image-specific properties"""
        super().set_properties(properties)
        
        metadata = properties.get('metadata', {})
        
        # Load image if path is provided
        if 'image_path' in metadata and metadata['image_path']:
            self.load_image(metadata['image_path'])
        
        # Apply image settings
        if 'scale_mode' in metadata:
            self.set_scale_mode(metadata['scale_mode'])
        if 'aspect_ratio_locked' in metadata:
            self.set_aspect_ratio_locked(metadata['aspect_ratio_locked'])
    
    def paintEvent(self, event):
        """Custom paint event to show selection and borders"""
        super().paintEvent(event)
        
        # Add custom border for images
        if self.metadata.get('has_image', False):
            painter = QPainter(self)
            
            # Draw image border
            pen = QPen(QColor(200, 200, 200), 1)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
            
            painter.end()