#!/usr/bin/env python3
"""
Test script to verify DragDropWidgets library core functionality (non-GUI components)
"""

import sys
import os

# Add current directory to path to import the library
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_serialization():
    """Test layout serialization without GUI components"""
    print("Testing serialization...")
    
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
        assert loaded_data['layout'] is not None, "Layout data not found"
        
        # Clean up
        os.unlink(temp_path)
        
        print("✅ JSON serialization successful")
        
        # Test validation
        errors = LayoutSerializer.validate_layout_data(test_data)
        assert len(errors) == 0, f"Validation errors: {errors}"
        print("✅ Layout validation successful")
        
        # Test statistics
        stats = LayoutSerializer.get_layout_statistics(test_data)
        assert stats['total_widgets'] == 1
        assert 'DraggableButton' in stats['widget_types']
        print("✅ Layout statistics successful")
        
        return True
    except Exception as e:
        print(f"❌ Serialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_system_core():
    """Test event management system without GUI"""
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
        
        # Test event history
        history = event_manager.get_event_history('test_event')
        assert len(history) == 1
        print("✅ Event history working")
        
        # Test event statistics
        stats = event_manager.get_event_statistics('test_event')
        assert stats['total_calls'] == 1
        print("✅ Event statistics working")
        
        return True
    except Exception as e:
        print(f"❌ Event system error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_theme_data():
    """Test theme management data structures"""
    print("\nTesting theme data...")
    
    try:
        from dragdropwidgets.utils.themes import ThemeManager
        
        theme_manager = ThemeManager()
        
        # Test available themes
        themes = theme_manager.get_available_themes()
        assert 'light' in themes
        assert 'dark' in themes
        assert 'blue' in themes
        assert 'green' in themes
        assert 'high_contrast' in themes
        print(f"✅ Available themes: {themes}")
        
        # Test theme retrieval
        light_theme = theme_manager.get_theme('light')
        assert light_theme is not None
        assert 'colors' in light_theme
        assert 'fonts' in light_theme
        assert 'spacing' in light_theme
        print("✅ Theme structure validation successful")
        
        # Test custom theme creation
        custom_theme = {
            'name': 'Test Theme',
            'colors': {
                'background': '#ffffff',
                'foreground': '#000000',
                'accent': '#0066cc'
            },
            'fonts': {
                'default_family': 'Arial',
                'default_size': 10
            },
            'spacing': {
                'small': 4,
                'medium': 8,
                'large': 16
            }
        }
        
        theme_manager.create_custom_theme('test_theme', custom_theme)
        retrieved_theme = theme_manager.get_theme('test_theme')
        assert retrieved_theme is not None
        assert retrieved_theme['colors']['accent'] == '#0066cc'
        print("✅ Custom theme creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Theme data error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_core_imports():
    """Test that core modules can be imported"""
    print("\nTesting core imports...")
    
    try:
        # Test utils imports (these don't require GUI)
        from dragdropwidgets.utils.serializer import LayoutSerializer
        from dragdropwidgets.utils.events import EventManager, Events
        from dragdropwidgets.utils.themes import ThemeManager
        print("✅ Utils imports successful")
        
        # Test that the main __init__ file works for non-GUI components
        import dragdropwidgets
        assert hasattr(dragdropwidgets, '__version__')
        assert dragdropwidgets.__version__ == "1.0.0"
        print("✅ Main package import successful")
        
        return True
    except Exception as e:
        print(f"❌ Core imports error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_package_structure():
    """Test package structure and metadata"""
    print("\nTesting package structure...")
    
    try:
        import dragdropwidgets
        
        # Test version
        assert hasattr(dragdropwidgets, '__version__')
        assert dragdropwidgets.__version__ == "1.0.0"
        print("✅ Version information correct")
        
        # Test author info
        assert hasattr(dragdropwidgets, '__author__')
        assert dragdropwidgets.__author__ == "DragDropWidgets Team"
        print("✅ Author information correct")
        
        # Test __all__ exports
        assert hasattr(dragdropwidgets, '__all__')
        expected_exports = [
            'WidgetBase', 'DraggableWidget', 'DropZone', 'DynamicLayoutManager',
            'DraggableButton', 'DraggableLabel', 'DraggableImage',
            'LayoutSerializer', 'ThemeManager', 'EventManager', 'create_app'
        ]
        
        for export in expected_exports:
            assert export in dragdropwidgets.__all__, f"Missing export: {export}"
        
        print("✅ Package exports correct")
        
        return True
    except Exception as e:
        print(f"❌ Package structure error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_setup_files():
    """Test that setup files exist and are correct"""
    print("\nTesting setup files...")
    
    try:
        # Test that required files exist
        required_files = [
            'setup.py',
            'requirements.txt',
            'README.md',
            'LICENSE',
            'MANIFEST.in',
            '.gitignore'
        ]
        
        for file in required_files:
            file_path = os.path.join(os.path.dirname(__file__), file)
            assert os.path.exists(file_path), f"Missing file: {file}"
        
        print("✅ All required files exist")
        
        # Test setup.py content
        setup_path = os.path.join(os.path.dirname(__file__), 'setup.py')
        with open(setup_path, 'r') as f:
            setup_content = f.read()
        
        assert 'dragdropwidgets' in setup_content
        assert 'PySide6' in setup_content
        assert '1.0.0' in setup_content
        print("✅ setup.py content correct")
        
        # Test requirements.txt
        req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        with open(req_path, 'r') as f:
            req_content = f.read()
        
        assert 'PySide6>=6.4.0' in req_content
        assert 'PyYAML>=6.0' in req_content
        print("✅ requirements.txt content correct")
        
        return True
    except Exception as e:
        print(f"❌ Setup files error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all core tests"""
    print("🧪 Testing DragDropWidgets Library (Core Components)")
    print("=" * 60)
    
    tests = [
        test_core_imports,
        test_package_structure,
        test_setup_files,
        test_serialization,
        test_event_system_core,
        test_theme_data,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Unexpected error in {test.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Core Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core tests passed! Library structure is correct.")
        print("\nNote: GUI components require a display environment to test.")
        print("The library is ready for distribution and use!")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())