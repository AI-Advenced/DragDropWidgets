"""
Advanced dashboard example with property panel and full customization
"""

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from dragdropwidgets import *
from dragdropwidgets.widgets.custom import CustomWidgetFactory, DraggableProgressBar, DraggableSlider, DraggableTextEdit
from dragdropwidgets.utils.themes import ThemeManager
from dragdropwidgets.utils.events import event_manager, WidgetEvents
from dragdropwidgets.utils.serializer import LayoutSerializer

class DashboardWidget(DraggableWidget):
    """Custom dashboard widget container"""
    
    def __init__(self, title="Dashboard Widget", parent=None):
        super().__init__(parent)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        self.title_bar = QLabel(title)
        self.title_bar.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                color: white;
                padding: 8px 12px;
                font-weight: bold;
                border-radius: 4px 4px 0 0;
                font-size: 12px;
            }
        """)
        
        # Content area
        self.content_area = QFrame()
        self.content_area.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 0 0 4px 4px;
                border-top: none;
            }
        """)
        
        layout.addWidget(self.title_bar)
        layout.addWidget(self.content_area)
        
        self.setMinimumSize(200, 150)
        
        # Additional metadata
        self.metadata.update({
            'title': title,
            'widget_type': 'dashboard_container'
        })
        
    def set_title(self, title: str):
        """Set title text"""
        self.title_bar.setText(title)
        self.metadata['title'] = title
        
    def set_content(self, widget):
        """Set content widget"""
        # Clear existing layout
        if self.content_area.layout():
            QWidget().setLayout(self.content_area.layout())
        
        # Add new content
        layout = QVBoxLayout(self.content_area)
        layout.addWidget(widget)

class PropertyPanel(QFrame):
    """Property editing panel for widgets"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_widget = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup property panel UI"""
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-left: 1px solid #dee2e6;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Properties")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                background-color: #e9ecef;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(title)
        
        # Scroll area for properties
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll_area)
        
        # Default content
        self.show_no_selection()
        
    def show_no_selection(self):
        """Show message when no widget is selected"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel("No widget selected")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                padding: 40px;
            }
        """)
        
        layout.addWidget(label)
        layout.addStretch()
        
        self.scroll_area.setWidget(widget)
        
    def show_widget_properties(self, widget):
        """Show properties for selected widget"""
        self.current_widget = widget
        
        properties_widget = QWidget()
        layout = QVBoxLayout(properties_widget)
        
        # Widget info
        info_group = self.create_info_group(widget)
        layout.addWidget(info_group)
        
        # Position and size
        transform_group = self.create_transform_group(widget)
        layout.addWidget(transform_group)
        
        # Widget-specific properties
        if isinstance(widget, DraggableButton):
            button_group = self.create_button_group(widget)
            layout.addWidget(button_group)
        elif isinstance(widget, DraggableLabel):
            label_group = self.create_label_group(widget)
            layout.addWidget(label_group)
        elif isinstance(widget, DraggableImage):
            image_group = self.create_image_group(widget)
            layout.addWidget(image_group)
        elif isinstance(widget, DashboardWidget):
            dashboard_group = self.create_dashboard_group(widget)
            layout.addWidget(dashboard_group)
        elif isinstance(widget, DraggableProgressBar):
            progress_group = self.create_progress_group(widget)
            layout.addWidget(progress_group)
        elif isinstance(widget, DraggableSlider):
            slider_group = self.create_slider_group(widget)
            layout.addWidget(slider_group)
        elif isinstance(widget, DraggableTextEdit):
            text_group = self.create_text_edit_group(widget)
            layout.addWidget(text_group)
            
        # Behavior properties
        behavior_group = self.create_behavior_group(widget)
        layout.addWidget(behavior_group)
        
        layout.addStretch()
        
        self.scroll_area.setWidget(properties_widget)
        
    def create_info_group(self, widget):
        """Create widget info group"""
        group = QGroupBox("Widget Info")
        layout = QFormLayout(group)
        
        # Widget type
        type_label = QLabel(widget.__class__.__name__)
        type_label.setStyleSheet("font-weight: bold; color: #0078d4;")
        layout.addRow("Type:", type_label)
        
        # Widget ID
        id_label = QLabel(widget.widget_id[:8] + "...")
        id_label.setStyleSheet("font-family: monospace; font-size: 11px;")
        layout.addRow("ID:", id_label)
        
        return group
        
    def create_transform_group(self, widget):
        """Create position and size controls"""
        group = QGroupBox("Transform")
        layout = QFormLayout(group)
        
        # Position controls
        x_spin = QSpinBox()
        x_spin.setRange(-1000, 2000)
        x_spin.setValue(widget.x())
        x_spin.valueChanged.connect(lambda v: self.update_position(widget, v, widget.y()))
        
        y_spin = QSpinBox()
        y_spin.setRange(-1000, 2000)
        y_spin.setValue(widget.y())
        y_spin.valueChanged.connect(lambda v: self.update_position(widget, widget.x(), v))
        
        # Size controls
        width_spin = QSpinBox()
        width_spin.setRange(50, 1000)
        width_spin.setValue(widget.width())
        width_spin.valueChanged.connect(lambda v: self.update_size(widget, v, widget.height()))
        
        height_spin = QSpinBox()
        height_spin.setRange(30, 800)
        height_spin.setValue(widget.height())
        height_spin.valueChanged.connect(lambda v: self.update_size(widget, widget.width(), v))
        
        layout.addRow("X:", x_spin)
        layout.addRow("Y:", y_spin)
        layout.addRow("Width:", width_spin)
        layout.addRow("Height:", height_spin)
        
        return group
        
    def create_button_group(self, button):
        """Create button-specific properties"""
        group = QGroupBox("Button Properties")
        layout = QFormLayout(group)
        
        # Text
        text_edit = QLineEdit(button.get_text())
        text_edit.textChanged.connect(button.set_text)
        layout.addRow("Text:", text_edit)
        
        # Style
        style_combo = QComboBox()
        styles = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']
        style_combo.addItems(styles)
        style_combo.setCurrentText(button.metadata.get('button_style', 'primary'))
        style_combo.currentTextChanged.connect(button.set_style)
        layout.addRow("Style:", style_combo)
        
        # Enabled
        enabled_check = QCheckBox()
        enabled_check.setChecked(button.button.isEnabled())
        enabled_check.toggled.connect(button.set_enabled)
        layout.addRow("Enabled:", enabled_check)
        
        # Checkable
        checkable_check = QCheckBox()
        checkable_check.setChecked(button.button.isCheckable())
        checkable_check.toggled.connect(button.set_checkable)
        layout.addRow("Checkable:", checkable_check)
        
        return group
        
    def create_label_group(self, label):
        """Create label-specific properties"""
        group = QGroupBox("Label Properties")
        layout = QFormLayout(group)
        
        # Text
        text_edit = QLineEdit(label.get_text())
        text_edit.textChanged.connect(label.set_text)
        layout.addRow("Text:", text_edit)
        
        # Font size
        font_spin = QSpinBox()
        font_spin.setRange(8, 72)
        font_spin.setValue(label.metadata.get('font_size', 14))
        font_spin.valueChanged.connect(label.set_font_size)
        layout.addRow("Font Size:", font_spin)
        
        # Font family
        font_combo = QComboBox()
        font_combo.addItems(['Segoe UI', 'Arial', 'Times New Roman', 'Courier New', 'Helvetica'])
        font_combo.setCurrentText(label.metadata.get('font_family', 'Segoe UI'))
        font_combo.currentTextChanged.connect(label.set_font_family)
        layout.addRow("Font Family:", font_combo)
        
        # Font bold
        bold_check = QCheckBox()
        bold_check.setChecked(label.metadata.get('font_bold', False))
        bold_check.toggled.connect(label.set_font_bold)
        layout.addRow("Bold:", bold_check)
        
        # Font italic
        italic_check = QCheckBox()
        italic_check.setChecked(label.metadata.get('font_italic', False))
        italic_check.toggled.connect(label.set_font_italic)
        layout.addRow("Italic:", italic_check)
        
        # Text color
        color_btn = QPushButton("Choose Color")
        color_btn.clicked.connect(lambda: self.choose_color(label, 'text'))
        layout.addRow("Text Color:", color_btn)
        
        # Alignment
        align_combo = QComboBox()
        align_combo.addItems(['left', 'center', 'right', 'top', 'bottom'])
        align_combo.setCurrentText(label.metadata.get('alignment', 'center'))
        align_combo.currentTextChanged.connect(label.set_alignment)
        layout.addRow("Alignment:", align_combo)
        
        # Word wrap
        wrap_check = QCheckBox()
        wrap_check.setChecked(label.metadata.get('word_wrap', False))
        wrap_check.toggled.connect(label.set_word_wrap)
        layout.addRow("Word Wrap:", wrap_check)
        
        # Style preset
        preset_combo = QComboBox()
        presets = ['title', 'subtitle', 'body', 'caption', 'warning', 'error', 'success', 'info']
        preset_combo.addItems([''] + presets)
        preset_combo.currentTextChanged.connect(lambda p: label.set_style_preset(p) if p else None)
        layout.addRow("Style Preset:", preset_combo)
        
        return group
        
    def create_image_group(self, image):
        """Create image-specific properties"""
        group = QGroupBox("Image Properties")
        layout = QFormLayout(group)
        
        # Load image button
        load_btn = QPushButton("Load Image")
        load_btn.clicked.connect(image.open_file_dialog)
        layout.addRow("Image File:", load_btn)
        
        # Scale mode
        scale_combo = QComboBox()
        scale_combo.addItems(['keep_aspect_ratio', 'ignore_aspect_ratio', 'keep_aspect_ratio_by_expanding'])
        scale_combo.setCurrentText(image.metadata.get('scale_mode', 'keep_aspect_ratio'))
        scale_combo.currentTextChanged.connect(image.set_scale_mode)
        layout.addRow("Scale Mode:", scale_combo)
        
        # Aspect ratio locked
        aspect_check = QCheckBox()
        aspect_check.setChecked(image.metadata.get('aspect_ratio_locked', True))
        aspect_check.toggled.connect(image.set_aspect_ratio_locked)
        layout.addRow("Lock Aspect:", aspect_check)
        
        # Transform buttons
        transform_layout = QHBoxLayout()
        
        rotate_btn = QPushButton("Rotate 90°")
        rotate_btn.clicked.connect(lambda: image.rotate_image(90))
        transform_layout.addWidget(rotate_btn)
        
        flip_h_btn = QPushButton("Flip H")
        flip_h_btn.clicked.connect(image.flip_horizontal)
        transform_layout.addWidget(flip_h_btn)
        
        flip_v_btn = QPushButton("Flip V")
        flip_v_btn.clicked.connect(image.flip_vertical)
        transform_layout.addWidget(flip_v_btn)
        
        transform_widget = QWidget()
        transform_widget.setLayout(transform_layout)
        layout.addRow("Transform:", transform_widget)
        
        return group
        
    def create_dashboard_group(self, dashboard):
        """Create dashboard widget properties"""
        group = QGroupBox("Dashboard Properties")
        layout = QFormLayout(group)
        
        # Title
        title_edit = QLineEdit(dashboard.metadata.get('title', ''))
        title_edit.textChanged.connect(dashboard.set_title)
        layout.addRow("Title:", title_edit)
        
        return group
        
    def create_progress_group(self, progress):
        """Create progress bar properties"""
        group = QGroupBox("Progress Properties")
        layout = QFormLayout(group)
        
        # Value
        value_spin = QSpinBox()
        value_spin.setRange(0, 100)
        value_spin.setValue(progress.metadata.get('value', 0))
        value_spin.valueChanged.connect(progress.set_value)
        layout.addRow("Value:", value_spin)
        
        # Range
        min_spin = QSpinBox()
        min_spin.setRange(0, 1000)
        min_spin.setValue(progress.metadata.get('minimum', 0))
        min_spin.valueChanged.connect(lambda v: progress.set_range(v, progress.metadata.get('maximum', 100)))
        layout.addRow("Minimum:", min_spin)
        
        max_spin = QSpinBox()
        max_spin.setRange(1, 1000)
        max_spin.setValue(progress.metadata.get('maximum', 100))
        max_spin.valueChanged.connect(lambda v: progress.set_range(progress.metadata.get('minimum', 0), v))
        layout.addRow("Maximum:", max_spin)
        
        return group
        
    def create_slider_group(self, slider):
        """Create slider properties"""
        group = QGroupBox("Slider Properties")
        layout = QFormLayout(group)
        
        # Value
        value_spin = QSpinBox()
        value_spin.setRange(0, 100)
        value_spin.setValue(slider.metadata.get('value', 50))
        value_spin.valueChanged.connect(slider.set_value)
        layout.addRow("Value:", value_spin)
        
        # Range
        min_spin = QSpinBox()
        min_spin.setRange(0, 1000)
        min_spin.setValue(slider.metadata.get('minimum', 0))
        min_spin.valueChanged.connect(lambda v: slider.set_range(v, slider.metadata.get('maximum', 100)))
        layout.addRow("Minimum:", min_spin)
        
        max_spin = QSpinBox()
        max_spin.setRange(1, 1000)
        max_spin.setValue(slider.metadata.get('maximum', 100))
        max_spin.valueChanged.connect(lambda v: slider.set_range(slider.metadata.get('minimum', 0), v))
        layout.addRow("Maximum:", max_spin)
        
        return group
        
    def create_text_edit_group(self, text_edit):
        """Create text edit properties"""
        group = QGroupBox("Text Edit Properties")
        layout = QFormLayout(group)
        
        # Text content
        text_area = QTextEdit()
        text_area.setPlainText(text_edit.get_text())
        text_area.setMaximumHeight(100)
        text_area.textChanged.connect(lambda: text_edit.set_text(text_area.toPlainText()))
        layout.addRow("Content:", text_area)
        
        # Read only
        readonly_check = QCheckBox()
        readonly_check.setChecked(text_edit.metadata.get('read_only', False))
        readonly_check.toggled.connect(text_edit.set_read_only)
        layout.addRow("Read Only:", readonly_check)
        
        return group
        
    def create_behavior_group(self, widget):
        """Create behavior properties"""
        group = QGroupBox("Behavior")
        layout = QFormLayout(group)
        
        # Draggable
        draggable_check = QCheckBox()
        draggable_check.setChecked(widget.is_draggable)
        draggable_check.toggled.connect(widget.set_draggable)
        layout.addRow("Draggable:", draggable_check)
        
        # Resizable
        resizable_check = QCheckBox()
        resizable_check.setChecked(widget.is_resizable)
        resizable_check.toggled.connect(widget.set_resizable)
        layout.addRow("Resizable:", resizable_check)
        
        # Snap to grid
        if hasattr(widget, 'snap_to_grid'):
            snap_check = QCheckBox()
            snap_check.setChecked(widget.snap_to_grid)
            snap_check.toggled.connect(lambda checked: widget.set_snap_to_grid(checked, widget.grid_size))
            layout.addRow("Snap to Grid:", snap_check)
            
            # Grid size
            grid_spin = QSpinBox()
            grid_spin.setRange(5, 100)
            grid_spin.setValue(widget.grid_size)
            grid_spin.valueChanged.connect(lambda v: widget.set_snap_to_grid(widget.snap_to_grid, v))
            layout.addRow("Grid Size:", grid_spin)
        
        return group
        
    def update_position(self, widget, x, y):
        """Update widget position"""
        widget.move(x, y)
        
    def update_size(self, widget, width, height):
        """Update widget size"""
        widget.resize(width, height)
        
    def choose_color(self, widget, color_type):
        """Open color chooser dialog"""
        color = QColorDialog.getColor()
        if color.isValid():
            if color_type == 'text':
                widget.set_color(color.name())
            elif color_type == 'background':
                widget.set_background_color(color.name())

class ToolboxPanel(QFrame):
    """Widget toolbox panel"""
    
    widget_requested = Signal(str)  # Emitted when user wants to add widget
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup toolbox UI"""
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-right: 1px solid #dee2e6;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Widget Toolbox")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                background-color: #e9ecef;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(title)
        
        # Widget categories
        self.create_widget_category(layout, "Basic Widgets", [
            ("Button", "DraggableButton", "🔘"),
            ("Label", "DraggableLabel", "📝"),
            ("Image", "DraggableImage", "🖼️"),
        ])
        
        self.create_widget_category(layout, "Input Widgets", [
            ("Text Edit", "DraggableTextEdit", "📄"),
            ("Slider", "DraggableSlider", "🎚️"),
        ])
        
        self.create_widget_category(layout, "Display Widgets", [
            ("Progress Bar", "DraggableProgressBar", "📊"),
        ])
        
        self.create_widget_category(layout, "Containers", [
            ("Dashboard Widget", "DashboardWidget", "📱"),
        ])
        
        layout.addStretch()
        
    def create_widget_category(self, parent_layout, category_name, widgets):
        """Create a widget category section"""
        # Category header
        header = QLabel(category_name)
        header.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
                padding: 8px 12px 4px 12px;
                font-size: 12px;
            }
        """)
        parent_layout.addWidget(header)
        
        # Widget buttons
        for name, class_name, icon in widgets:
            btn = QPushButton(f"{icon} {name}")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 16px;
                    margin: 1px 8px;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    background-color: white;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #e6f3ff;
                    border-color: #0078d4;
                }
                QPushButton:pressed {
                    background-color: #cce7ff;
                }
            """)
            btn.clicked.connect(lambda checked, cn=class_name: self.widget_requested.emit(cn))
            parent_layout.addWidget(btn)

class DashboardWindow(QMainWindow):
    """Main dashboard window"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.setup_ui()
        self.create_sample_widgets()
        
        # Connect to layout changes to refresh properties
        self.drop_zone.widget_dropped.connect(self.on_layout_changed)
        self.drop_zone.layout_changed.connect(self.on_layout_changed)
        
    def setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("Advanced Dashboard Designer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply theme
        self.theme_manager.apply_theme_to_app('light')
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create panels
        self.toolbox = ToolboxPanel()
        self.drop_zone = DropZone()
        self.properties = PropertyPanel()
        
        # Setup drop zone
        self.drop_zone.set_grid_visible(True)
        self.drop_zone.grid_size = 20
        
        # Connect signals
        self.toolbox.widget_requested.connect(self.add_widget_from_toolbox)
        self.drop_zone.widget_dropped.connect(self.on_widget_selected_from_drop)
        
        # Add panels to layout
        main_layout.addWidget(self.toolbox)
        main_layout.addWidget(self.drop_zone, 1)
        main_layout.addWidget(self.properties)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().showMessage("Ready - Drag widgets from the toolbox to the canvas")
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Layout', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_layout)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        save_action = QAction('Save Layout', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_layout)
        file_menu.addAction(save_action)
        
        load_action = QAction('Load Layout', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_layout)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('Export as Code', self)
        export_action.triggered.connect(self.export_code)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        select_all_action = QAction('Select All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.drop_zone.select_all)
        edit_menu.addAction(select_all_action)
        
        clear_selection_action = QAction('Clear Selection', self)
        clear_selection_action.setShortcut('Escape')
        clear_selection_action.triggered.connect(self.drop_zone.clear_selection)
        edit_menu.addAction(clear_selection_action)
        
        edit_menu.addSeparator()
        
        delete_action = QAction('Delete Selected', self)
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.drop_zone.delete_selected)
        edit_menu.addAction(delete_action)
        
        # Layout menu
        layout_menu = menubar.addMenu('Layout')
        
        grid_action = QAction('Arrange in Grid', self)
        grid_action.triggered.connect(lambda: self.drop_zone.set_layout_mode('grid'))
        layout_menu.addAction(grid_action)
        
        flow_action = QAction('Arrange in Flow', self)
        flow_action.triggered.connect(lambda: self.drop_zone.set_layout_mode('flow'))
        layout_menu.addAction(flow_action)
        
        free_action = QAction('Free Layout', self)
        free_action.triggered.connect(lambda: self.drop_zone.set_layout_mode('free'))
        layout_menu.addAction(free_action)
        
        layout_menu.addSeparator()
        
        toggle_grid_action = QAction('Toggle Grid', self)
        toggle_grid_action.setShortcut('Ctrl+G')
        toggle_grid_action.triggered.connect(lambda: self.drop_zone.set_grid_visible(not self.drop_zone.show_grid))
        layout_menu.addAction(toggle_grid_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        theme_submenu = view_menu.addMenu('Theme')
        
        themes = self.theme_manager.get_available_themes()
        for theme_id, theme_name in themes.items():
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, tid=theme_id: self.change_theme(tid))
            theme_submenu.addAction(action)
        
    def add_widget_from_toolbox(self, widget_class_name):
        """Add widget from toolbox"""
        widget = None
        
        if widget_class_name == 'DraggableButton':
            widget = DraggableButton("New Button")
        elif widget_class_name == 'DraggableLabel':
            widget = DraggableLabel("New Label")
        elif widget_class_name == 'DraggableImage':
            widget = DraggableImage()
        elif widget_class_name == 'DraggableTextEdit':
            widget = DraggableTextEdit("Enter text here...")
        elif widget_class_name == 'DraggableSlider':
            widget = DraggableSlider(50)
        elif widget_class_name == 'DraggableProgressBar':
            widget = DraggableProgressBar(75)
        elif widget_class_name == 'DashboardWidget':
            widget = DashboardWidget("Dashboard Panel")
            # Add sample content
            content = QLabel("Dashboard Content\n\nThis is a container widget\nthat can hold other widgets.")
            content.setAlignment(Qt.AlignCenter)
            content.setStyleSheet("color: #666666; font-style: italic;")
            widget.set_content(content)
        
        if widget:
            # Enable snap to grid
            if hasattr(widget, 'set_snap_to_grid'):
                widget.set_snap_to_grid(True, self.drop_zone.grid_size)
            
            # Add to drop zone
            position = QPoint(50 + len(self.drop_zone.widgets) * 30, 50 + len(self.drop_zone.widgets) * 30)
            self.drop_zone.add_widget(widget, position)
            
            # Connect selection signal
            widget.widget_selected.connect(self.properties.show_widget_properties)
            
            self.statusBar().showMessage(f"Added {widget_class_name}")
            
    def on_widget_selected_from_drop(self, widget, position):
        """Handle widget selection from drop event"""
        self.properties.show_widget_properties(widget)
        
    def on_layout_changed(self):
        """Handle layout changes"""
        count = len(self.drop_zone.widgets)
        self.statusBar().showMessage(f"Layout updated - {count} widgets")
        
    def create_sample_widgets(self):
        """Create some sample widgets"""
        # Welcome button
        welcome_btn = DraggableButton("Welcome to Dashboard Designer!")
        welcome_btn.set_style('success')
        welcome_btn.set_snap_to_grid(True, 20)
        self.drop_zone.add_widget(welcome_btn, QPoint(100, 100))
        welcome_btn.widget_selected.connect(self.properties.show_widget_properties)
        
        # Info label
        info_label = DraggableLabel("Drag widgets from the toolbox →")
        info_label.set_style_preset('info')
        info_label.set_snap_to_grid(True, 20)
        self.drop_zone.add_widget(info_label, QPoint(100, 180))
        info_label.widget_selected.connect(self.properties.show_widget_properties)
        
        # Progress sample
        progress = DraggableProgressBar(65)
        self.drop_zone.add_widget(progress, QPoint(100, 250))
        progress.widget_selected.connect(self.properties.show_widget_properties)
        
    def new_layout(self):
        """Create new layout"""
        reply = QMessageBox.question(
            self, 'New Layout', 
            'Create new layout? This will clear all current widgets.',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for widget in self.drop_zone.widgets[:]:
                self.drop_zone.remove_widget(widget.widget_id)
            self.properties.show_no_selection()
            self.statusBar().showMessage("New layout created")
            
    def save_layout(self):
        """Save current layout"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Layout", "dashboard_layout.json", 
            "JSON Files (*.json);;YAML Files (*.yaml *.yml)"
        )
        
        if file_path:
            layout_data = self.drop_zone.get_layout_data()
            
            if file_path.endswith(('.yaml', '.yml')):
                success = LayoutSerializer.save_to_yaml(layout_data, file_path)
            else:
                success = LayoutSerializer.save_to_json(layout_data, file_path)
                
            if success:
                self.statusBar().showMessage(f"Layout saved to {file_path}")
                QMessageBox.information(self, "Success", "Layout saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to save layout!")
                
    def load_layout(self):
        """Load layout from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Layout", "", 
            "Layout Files (*.json *.yaml *.yml);;JSON Files (*.json);;YAML Files (*.yaml *.yml)"
        )
        
        if file_path:
            if file_path.endswith(('.yaml', '.yml')):
                layout_data = LayoutSerializer.load_from_yaml(file_path)
            else:
                layout_data = LayoutSerializer.load_from_json(file_path)
                
            if layout_data:
                self.drop_zone.load_layout_data(layout_data)
                
                # Reconnect signals for loaded widgets
                for widget in self.drop_zone.widgets:
                    widget.widget_selected.connect(self.properties.show_widget_properties)
                
                self.properties.show_no_selection()
                self.statusBar().showMessage(f"Layout loaded from {file_path}")
                QMessageBox.information(self, "Success", "Layout loaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to load layout!")
                
    def export_code(self):
        """Export layout as Python code"""
        layout_data = self.drop_zone.get_layout_data()
        code = LayoutSerializer.export_to_code(layout_data, 'python')
        
        # Show code in dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Generated Python Code")
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(code)
        text_edit.setFont(QFont('Courier New', 10))
        layout.addWidget(text_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec()
        
    def change_theme(self, theme_id):
        """Change application theme"""
        self.theme_manager.apply_theme_to_app(theme_id)
        self.statusBar().showMessage(f"Changed theme to {theme_id}")

def main():
    """Run the advanced dashboard example"""
    app = QApplication(sys.argv)
    
    print("🎯 Advanced Dashboard Designer")
    print("=" * 50)
    print("Features:")
    print("• Drag and drop widget creation")
    print("• Real-time property editing")
    print("• Multiple themes")
    print("• Layout serialization")
    print("• Code export")
    print("• Advanced widget types")
    print("=" * 50)
    
    window = DashboardWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())