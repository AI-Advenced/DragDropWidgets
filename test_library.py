#!/usr/bin/env python3
"""
Test script to verify DragDropWidgets library functionality
"""

import sys
import os

# Add current directory to path to import the library
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("Testing imports...")
    
    try:
        # Test core imports
        from dragdropwidgets import (
            WidgetBase, DraggableWidget, DropZone, DynamicLayoutManager,
            DraggableButton, DraggableLabel, DraggableImage,
            LayoutSerializer, ThemeManager, EventManager, create_app
        )
        print("✅ Core imports successful")
        
        # Test widget factory
        from dragdropwidgets.widgets.custom import CustomWidgetFactory
        print("✅ Custom widget factory import successful")
        
        # Test utils
        from dragdropwidgets.utils.events import Events
        print("✅ Utils imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_widget_creation():
    """Test basic widget creation"""
    print("\nTesting widget creation...")
    
    try:
        from dragdropwidgets import DraggableButton, DraggableLabel, DraggableImage
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QPoint
        
        # Create application (required for Qt widgets)
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test button creation
        button = DraggableButton("Test Button")
        button.set_style('primary')
        print("✅ DraggableButton created successfully")
        
        # Test label creation
        label = DraggableLabel("Test Label")
        label.set_font_size(14)
        label.set_style_preset('title')
        print("✅ DraggableLabel created successfully")
        
        # Test image creation
        image = DraggableImage()
        print("✅ DraggableImage created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Widget creation error: {e}")
        return False

def test_drop_zone():
    """Test drop zone functionality"""
    print("\nTesting drop zone...")
    
    try:
        from dragdropwidgets import DropZone, DraggableButton
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QPoint
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create drop zone
        drop_zone = DropZone()
        drop_zone.set_grid_visible(True)
        drop_zone.set_layout_mode('free')
        print("✅ DropZone created successfully")
        
        # Add a widget
        button = DraggableButton("Test")
        drop_zone.add_widget(button, QPoint(50, 50))
        print("✅ Widget added to DropZone successfully")
        
        # Test layout data
        layout_data = drop_zone.get_layout_data()
        assert 'widgets' in layout_data
        assert len(layout_data['widgets']) == 1
        print("✅ Layout data extraction successful")
        
        return True
    except Exception as e:
        print(f"❌ Drop zone error: {e}")
        return False

def test_theme_manager():
    """Test theme management"""
    print("\nTesting theme manager...")
    
    try:
        from dragdropwidgets.utils.themes import ThemeManager
        
        theme_manager = ThemeManager()
        
        # Test available themes
        themes = theme_manager.get_available_themes()
        assert 'light' in themes
        assert 'dark' in themes
        print(f"✅ Available themes: {themes}")
        
        # Test theme retrieval
        light_theme = theme_manager.get_theme('light')
        assert light_theme is not None
        assert 'colors' in light_theme
        print("✅ Theme retrieval successful")
        
        return True
    except Exception as e:
        print(f"❌ Theme manager error: {e}")
        return False

def test_serialization():
    """Test layout serialization"""
    print("\nTesting serialization...")
    
    try:
        from dragdropwidgets.utils.serializer import LayoutSerializer
        import tempfile
        import os
        
        # Test data
        test_data = {
            'layout_mode': 'free',
            'grid_size': 20,
            'show_grid': True,
            'widgets': [
                {
                    'id': 'test-widget-1',
                    'type': 'DraggableButton',
                    'position': {'x': 100, 'y': 100},
                    'size': {'width': 100, 'height': 35},
                    'metadata': {'text': 'Test Button'}
                }
            ]
        }
        
        # Test JSON serialization
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        # Save and load JSON
        success = LayoutSerializer.save_to_json(test_data, temp_path)
        assert success, "JSON save failed"
        
        loaded_data = LayoutSerializer.load_from_json(temp_path)
        assert loaded_data is not None, "JSON load failed"
        assert loaded_data['layout_mode'] == 'free'
        
        # Clean up
        os.unlink(temp_path)
        
        print("✅ JSON serialization successful")
        
        return True
    except Exception as e:
        print(f"❌ Serialization error: {e}")
        return False

def test_event_system():
    """Test event management system"""
    print("\nTesting event system...")
    
    try:
        from dragdropwidgets.utils.events import EventManager, Events
        
        event_manager = EventManager()
        
        # Test event registration
        test_events = []
        
        def test_handler(data):
            test_events.append(data)
        
        event_manager.register_event('test_event', test_handler)
        print("✅ Event handler registered successfully")
        
        # Test event emission
        event_manager.emit_event('test_event', 'test_data')
        assert len(test_events) == 1
        assert test_events[0] == 'test_data'
        print("✅ Event emission successful")
        
        # Test predefined events
        assert hasattr(Events, 'WIDGET_CREATED')
        assert hasattr(Events, 'WIDGET_MOVED')
        print("✅ Predefined events available")
        
        return True
    except Exception as e:
        print(f"❌ Event system error: {e}")
        return False

def test_custom_widgets():
    """Test custom widget factory"""
    print("\nTesting custom widget factory...")
    
    try:
        from dragdropwidgets.widgets.custom import CustomWidgetFactory
        
        # Test available widgets
        available = CustomWidgetFactory.get_available_widgets()
        assert 'DraggableButton' in available
        assert 'DraggableLabel' in available
        print(f"✅ Available custom widgets: {len(available)}")
        
        # Test widget creation via factory
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        button = CustomWidgetFactory.create_widget('DraggableButton', 'Factory Button')
        assert button is not None
        print("✅ Custom widget creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Custom widget factory error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing DragDropWidgets Library")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_widget_creation,
        test_drop_zone,
        test_theme_manager,
        test_serialization,
        test_event_system,
        test_custom_widgets
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Unexpected error in {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Library is working correctly.")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())