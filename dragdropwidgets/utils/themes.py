"""
Theme management system for styling widgets
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QPalette
from typing import Dict, Any, Optional

class ThemeManager(QObject):
    """Manager for themes and visual styles"""
    
    theme_changed = Signal(str)  # Emitted when theme changes
    
    THEMES = {
        'light': {
            'name': 'Light Theme',
            'description': 'Clean light theme with blue accents',
            'colors': {
                'background': '#ffffff',
                'foreground': '#333333',
                'accent': '#0078d4',
                'border': '#cccccc',
                'hover': '#e6f3ff',
                'selection': 'rgba(0, 120, 215, 0.2)',
                'success': '#28a745',
                'warning': '#ffc107',
                'danger': '#dc3545',
                'info': '#17a2b8'
            },
            'fonts': {
                'default_size': 14,
                'title_size': 18,
                'small_size': 12,
                'family': 'Segoe UI, Arial, sans-serif'
            },
            'spacing': {
                'small': 4,
                'medium': 8,
                'large': 16,
                'xlarge': 24
            }
        },
        
        'dark': {
            'name': 'Dark Theme',
            'description': 'Modern dark theme for low-light environments',
            'colors': {
                'background': '#2d2d2d',
                'foreground': '#ffffff',
                'accent': '#0099ff',
                'border': '#555555',
                'hover': '#3d3d3d',
                'selection': 'rgba(0, 153, 255, 0.2)',
                'success': '#28a745',
                'warning': '#ffc107',
                'danger': '#dc3545',
                'info': '#17a2b8'
            },
            'fonts': {
                'default_size': 14,
                'title_size': 18,
                'small_size': 12,
                'family': 'Segoe UI, Arial, sans-serif'
            },
            'spacing': {
                'small': 4,
                'medium': 8,
                'large': 16,
                'xlarge': 24
            }
        },
        
        'blue': {
            'name': 'Blue Theme',
            'description': 'Professional blue theme for business applications',
            'colors': {
                'background': '#e6f3ff',
                'foreground': '#003d82',
                'accent': '#0078d4',
                'border': '#b3d9ff',
                'hover': '#cce7ff',
                'selection': 'rgba(0, 120, 215, 0.3)',
                'success': '#28a745',
                'warning': '#ffc107',
                'danger': '#dc3545',
                'info': '#17a2b8'
            },
            'fonts': {
                'default_size': 14,
                'title_size': 18,
                'small_size': 12,
                'family': 'Segoe UI, Arial, sans-serif'
            },
            'spacing': {
                'small': 4,
                'medium': 8,
                'large': 16,
                'xlarge': 24
            }
        },
        
        'green': {
            'name': 'Nature Theme',
            'description': 'Refreshing green theme inspired by nature',
            'colors': {
                'background': '#f0f8f0',
                'foreground': '#2d4a2d',
                'accent': '#28a745',
                'border': '#a8d5a8',
                'hover': '#e8f5e8',
                'selection': 'rgba(40, 167, 69, 0.2)',
                'success': '#28a745',
                'warning': '#ffc107',
                'danger': '#dc3545',
                'info': '#17a2b8'
            },
            'fonts': {
                'default_size': 14,
                'title_size': 18,
                'small_size': 12,
                'family': 'Segoe UI, Arial, sans-serif'
            },
            'spacing': {
                'small': 4,
                'medium': 8,
                'large': 16,
                'xlarge': 24
            }
        },
        
        'high_contrast': {
            'name': 'High Contrast',
            'description': 'High contrast theme for accessibility',
            'colors': {
                'background': '#000000',
                'foreground': '#ffffff',
                'accent': '#ffff00',
                'border': '#ffffff',
                'hover': '#333333',
                'selection': 'rgba(255, 255, 0, 0.3)',
                'success': '#00ff00',
                'warning': '#ffff00',
                'danger': '#ff0000',
                'info': '#00ffff'
            },
            'fonts': {
                'default_size': 16,
                'title_size': 20,
                'small_size': 14,
                'family': 'Segoe UI, Arial, sans-serif'
            },
            'spacing': {
                'small': 6,
                'medium': 12,
                'large': 18,
                'xlarge': 30
            }
        }
    }
    
    def __init__(self):
        super().__init__()
        self.current_theme = 'light'
        self.custom_themes: Dict[str, Dict[str, Any]] = {}
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with descriptions"""
        themes = {}
        
        # Add built-in themes
        for theme_id, theme_data in self.THEMES.items():
            themes[theme_id] = theme_data['name']
        
        # Add custom themes
        for theme_id, theme_data in self.custom_themes.items():
            themes[theme_id] = theme_data.get('name', theme_id)
        
        return themes
    
    def get_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Get theme data by ID"""
        if theme_id in self.THEMES:
            return self.THEMES[theme_id]
        elif theme_id in self.custom_themes:
            return self.custom_themes[theme_id]
        return None
    
    def apply_theme(self, widget: QWidget, theme_id: str):
        """Apply theme to a widget"""
        theme = self.get_theme(theme_id)
        if not theme:
            print(f"Theme '{theme_id}' not found")
            return False
        
        colors = theme.get('colors', {})
        fonts = theme.get('fonts', {})
        spacing = theme.get('spacing', {})
        
        # Generate stylesheet
        stylesheet = self._generate_stylesheet(colors, fonts, spacing)
        
        # Apply to widget
        widget.setStyleSheet(stylesheet)
        
        # Update current theme
        self.current_theme = theme_id
        self.theme_changed.emit(theme_id)
        
        return True
    
    def apply_theme_to_app(self, theme_id: str):
        """Apply theme to entire application"""
        app = QApplication.instance()
        if not app:
            return False
        
        theme = self.get_theme(theme_id)
        if not theme:
            return False
        
        colors = theme.get('colors', {})
        fonts = theme.get('fonts', {})
        spacing = theme.get('spacing', {})
        
        # Generate global stylesheet
        stylesheet = self._generate_global_stylesheet(colors, fonts, spacing)
        
        # Apply to application
        app.setStyleSheet(stylesheet)
        
        # Update current theme
        self.current_theme = theme_id
        self.theme_changed.emit(theme_id)
        
        return True
    
    def _generate_stylesheet(self, colors: Dict[str, str], fonts: Dict[str, Any], spacing: Dict[str, int]) -> str:
        """Generate CSS stylesheet from theme data"""
        return f"""
            * {{
                background-color: {colors.get('background', '#ffffff')};
                color: {colors.get('foreground', '#333333')};
                font-family: {fonts.get('family', 'Segoe UI, Arial, sans-serif')};
                font-size: {fonts.get('default_size', 14)}px;
                border: 1px solid {colors.get('border', '#cccccc')};
                padding: {spacing.get('medium', 8)}px;
            }}
            
            *:hover {{
                background-color: {colors.get('hover', '#e6f3ff')};
            }}
            
            *:focus {{
                border: 2px solid {colors.get('accent', '#0078d4')};
            }}
            
            QWidget[selected="true"] {{
                background-color: {colors.get('selection', 'rgba(0, 120, 215, 0.2)')};
                border: 2px solid {colors.get('accent', '#0078d4')};
            }}
        """
    
    def _generate_global_stylesheet(self, colors: Dict[str, str], fonts: Dict[str, Any], spacing: Dict[str, int]) -> str:
        """Generate global application stylesheet"""
        return f"""
            QApplication {{
                font-family: {fonts.get('family', 'Segoe UI, Arial, sans-serif')};
                font-size: {fonts.get('default_size', 14)}px;
            }}
            
            QMainWindow {{
                background-color: {colors.get('background', '#ffffff')};
                color: {colors.get('foreground', '#333333')};
            }}
            
            QWidget {{
                background-color: {colors.get('background', '#ffffff')};
                color: {colors.get('foreground', '#333333')};
                border: 1px solid {colors.get('border', '#cccccc')};
            }}
            
            QPushButton {{
                background-color: {colors.get('accent', '#0078d4')};
                color: white;
                border: none;
                padding: {spacing.get('medium', 8)}px {spacing.get('large', 16)}px;
                border-radius: 4px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors.get('hover', '#106ebe')};
            }}
            
            QPushButton:pressed {{
                background-color: {colors.get('accent', '#005a9e')};
            }}
            
            QLabel {{
                background-color: transparent;
                color: {colors.get('foreground', '#333333')};
                border: none;
            }}
            
            QFrame {{
                background-color: {colors.get('background', '#ffffff')};
                border: 1px solid {colors.get('border', '#cccccc')};
            }}
            
            QScrollArea {{
                background-color: {colors.get('background', '#ffffff')};
                border: 1px solid {colors.get('border', '#cccccc')};
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {colors.get('border', '#cccccc')};
                margin-top: {spacing.get('medium', 8)}px;
                padding-top: {spacing.get('medium', 8)}px;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {spacing.get('medium', 8)}px;
                padding: 0 {spacing.get('small', 4)}px 0 {spacing.get('small', 4)}px;
            }}
            
            QLineEdit, QTextEdit, QSpinBox, QComboBox {{
                background-color: {colors.get('background', '#ffffff')};
                color: {colors.get('foreground', '#333333')};
                border: 1px solid {colors.get('border', '#cccccc')};
                padding: {spacing.get('small', 4)}px;
                border-radius: 2px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border: 2px solid {colors.get('accent', '#0078d4')};
            }}
            
            QSlider::groove:horizontal {{
                border: 1px solid {colors.get('border', '#cccccc')};
                height: 8px;
                background: {colors.get('background', '#ffffff')};
                margin: 2px 0;
            }}
            
            QSlider::handle:horizontal {{
                background: {colors.get('accent', '#0078d4')};
                border: 1px solid {colors.get('border', '#cccccc')};
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }}
            
            QProgressBar {{
                border: 1px solid {colors.get('border', '#cccccc')};
                border-radius: 2px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {colors.get('success', '#28a745')};
                border-radius: 2px;
            }}
        """
    
    def create_custom_theme(self, theme_id: str, name: str, colors: Dict[str, str], 
                          fonts: Optional[Dict[str, Any]] = None, 
                          spacing: Optional[Dict[str, int]] = None,
                          description: str = "Custom theme"):
        """Create a custom theme"""
        theme_data = {
            'name': name,
            'description': description,
            'colors': colors,
            'fonts': fonts or self.THEMES['light']['fonts'].copy(),
            'spacing': spacing or self.THEMES['light']['spacing'].copy()
        }
        
        self.custom_themes[theme_id] = theme_data
    
    def delete_custom_theme(self, theme_id: str) -> bool:
        """Delete a custom theme"""
        if theme_id in self.custom_themes:
            del self.custom_themes[theme_id]
            return True
        return False
    
    def export_theme(self, theme_id: str, file_path: str) -> bool:
        """Export theme to JSON file"""
        theme = self.get_theme(theme_id)
        if not theme:
            return False
        
        try:
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(theme, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting theme: {e}")
            return False
    
    def import_theme(self, file_path: str, theme_id: str) -> bool:
        """Import theme from JSON file"""
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
            
            # Validate theme data
            required_fields = ['name', 'colors']
            for field in required_fields:
                if field not in theme_data:
                    print(f"Missing required field: {field}")
                    return False
            
            self.custom_themes[theme_id] = theme_data
            return True
            
        except Exception as e:
            print(f"Error importing theme: {e}")
            return False
    
    def get_current_theme(self) -> str:
        """Get current theme ID"""
        return self.current_theme
    
    def get_theme_preview_colors(self, theme_id: str) -> Dict[str, str]:
        """Get preview colors for theme selection"""
        theme = self.get_theme(theme_id)
        if not theme:
            return {}
        
        colors = theme.get('colors', {})
        return {
            'background': colors.get('background', '#ffffff'),
            'foreground': colors.get('foreground', '#333333'),
            'accent': colors.get('accent', '#0078d4'),
            'border': colors.get('border', '#cccccc')
        }