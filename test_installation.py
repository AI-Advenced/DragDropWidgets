#!/usr/bin/env python3
"""
Test script to verify DragDropWidgets installation and basic functionality
"""

import sys
import traceback

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🔍 Testing imports...")
    
    try:
        # Test main package
        import dragdropwidgets
        print("✅ dragdropwidgets - OK")
        
        # Test core modules
        from dragdropwidgets.core import WidgetBase, DraggableWidget, DropZone
        print("✅ Core modules - OK")
        
        # Test widget modules
        from dragdropwidgets.widgets import DraggableButton, DraggableLabel, DraggableImage
        print("✅ Widget modules - OK")
        
        # Test utilities
        from dragdropwidgets.utils import LayoutSerializer, ThemeManager, EventManager
        print("✅ Utility modules - OK")
        
        # Test convenience function
        from dragdropwidgets import create_app
        print("✅ Convenience functions - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_widget_creation():
    """Test basic widget creation without GUI"""
    print("\n🔧 Testing widget creation...")
    
    try:
        from dragdropwidgets import DraggableButton, DraggableLabel, DraggableImage
        from dragdropwidgets.widgets.custom import DraggableProgressBar, DraggableSlider
        
        # Test button creation
        button = DraggableButton("Test Button")
        assert button.get_text() == "Test Button"
        print("✅ DraggableButton creation - OK")
        
        # Test label creation
        label = DraggableLabel("Test Label")
        assert label.get_text() == "Test Label"
        print("✅ DraggableLabel creation - OK")
        
        # Test image creation
        image = DraggableImage()
        assert image.metadata['has_image'] == False
        print("✅ DraggableImage creation - OK")
        
        # Test progress bar creation
        progress = DraggableProgressBar(50)
        assert progress.metadata['value'] == 50
        print("✅ DraggableProgressBar creation - OK")
        
        # Test slider creation
        slider = DraggableSlider(75)
        assert slider.metadata['value'] == 75
        print("✅ DraggableSlider creation - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Widget creation error: {e}")
        traceback.print_exc()
        return False

def test_utilities():
    """Test utility functions"""
    print("\n🛠️ Testing utilities...")
    
    try:
        # Test theme manager
        from dragdropwidgets.utils.themes import ThemeManager
        theme_manager = ThemeManager()
        themes = theme_manager.get_available_themes()
        assert len(themes) >= 5  # Should have at least 5 built-in themes
        print(f"✅ ThemeManager - {len(themes)} themes available")
        
        # Test event manager
        from dragdropwidgets.utils.events import EventManager, Event
        event_manager = EventManager()
        
        test_handled = False
        def test_handler(event):
            nonlocal test_handled
            test_handled = True
        
        event_manager.register_event('test_event', test_handler)
        event_manager.emit_event('test_event')
        assert test_handled == True
        print("✅ EventManager - OK")
        
        # Test serializer
        from dragdropwidgets.utils.serializer import LayoutSerializer
        test_data = {
            'widgets': [],
            'layout_mode': 'free',
            'grid_size': 20
        }
        
        # Test validation
        valid = LayoutSerializer._validate_layout_data(test_data)
        assert valid == True
        print("✅ LayoutSerializer - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Utilities error: {e}")
        traceback.print_exc()
        return False

def test_widget_factory():
    """Test custom widget factory"""
    print("\n🏭 Testing widget factory...")
    
    try:
        from dragdropwidgets.widgets.custom import CustomWidgetFactory
        
        # Test getting available widgets
        widgets = CustomWidgetFactory.get_available_widgets()
        assert len(widgets) > 0
        print(f"✅ Widget factory - {len(widgets)} widget types registered")
        
        # Test creating widgets
        button = CustomWidgetFactory.create_widget('DraggableButton', "Factory Button")
        assert button is not None
        assert button.get_text() == "Factory Button"
        print("✅ Widget creation via factory - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Widget factory error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🎯 DragDropWidgets Installation Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Widget Creation", test_widget_creation),
        ("Utilities", test_utilities),
        ("Widget Factory", test_widget_factory),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! DragDropWidgets is ready to use.")
        print("\nTo run examples:")
        print("  python -m dragdropwidgets.examples.hello_world")
        print("  python -m dragdropwidgets.examples.dashboard")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)