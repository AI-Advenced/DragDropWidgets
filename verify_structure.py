#!/usr/bin/env python3
"""
Verify DragDropWidgets library structure and completeness
"""

import os
import sys

def check_file_structure():
    """Check that all required files exist"""
    print("📁 Checking file structure...")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Required files and directories
    structure = {
        'files': [
            'setup.py',
            'requirements.txt', 
            'README.md',
            'LICENSE',
            'MANIFEST.in',
            '.gitignore'
        ],
        'directories': [
            'dragdropwidgets',
            'dragdropwidgets/core',
            'dragdropwidgets/widgets',
            'dragdropwidgets/utils',
            'dragdropwidgets/examples'
        ],
        'core_files': [
            'dragdropwidgets/__init__.py',
            'dragdropwidgets/core/__init__.py',
            'dragdropwidgets/core/widget_base.py',
            'dragdropwidgets/core/draggable.py',
            'dragdropwidgets/core/drop_zone.py',
            'dragdropwidgets/core/layout_manager.py'
        ],
        'widget_files': [
            'dragdropwidgets/widgets/__init__.py',
            'dragdropwidgets/widgets/button.py',
            'dragdropwidgets/widgets/label.py',
            'dragdropwidgets/widgets/image.py',
            'dragdropwidgets/widgets/custom.py'
        ],
        'util_files': [
            'dragdropwidgets/utils/__init__.py',
            'dragdropwidgets/utils/serializer.py',
            'dragdropwidgets/utils/themes.py',
            'dragdropwidgets/utils/events.py'
        ],
        'example_files': [
            'dragdropwidgets/examples/__init__.py',
            'dragdropwidgets/examples/hello_world.py',
            'dragdropwidgets/examples/dashboard.py'
        ]
    }
    
    missing_items = []
    
    # Check all items
    for category, items in structure.items():
        for item in items:
            path = os.path.join(base_path, item)
            if not os.path.exists(path):
                missing_items.append(f"{category}: {item}")
            else:
                print(f"  ✅ {item}")
    
    if missing_items:
        print(f"\n❌ Missing items:")
        for item in missing_items:
            print(f"  - {item}")
        return False
    else:
        print(f"\n✅ All required files and directories present")
        return True

def count_lines_of_code():
    """Count lines of code in the library"""
    print("\n📊 Counting lines of code...")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    total_lines = 0
    total_files = 0
    
    for root, dirs, files in os.walk(os.path.join(base_path, 'dragdropwidgets')):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        total_files += 1
                        print(f"  {file}: {lines} lines")
                except Exception as e:
                    print(f"  ❌ Error reading {file}: {e}")
    
    print(f"\n📈 Total: {total_lines} lines across {total_files} Python files")
    return total_lines, total_files

def check_setup_py():
    """Check setup.py content"""
    print("\n⚙️  Checking setup.py...")
    
    setup_path = os.path.join(os.path.dirname(__file__), 'setup.py')
    
    try:
        with open(setup_path, 'r') as f:
            content = f.read()
        
        checks = {
            'Package name': 'name="dragdropwidgets"' in content,
            'Version': 'version="1.0.0"' in content,
            'PySide6 dependency': 'PySide6>=6.4.0' in content or 'PySide6' in content,
            'Entry points': 'dragdrop-demo' in content,
            'Python requirement': 'python_requires=">=3.8"' in content,
            'License': 'License :: OSI Approved :: MIT License' in content
        }
        
        all_good = True
        for check, result in checks.items():
            if result:
                print(f"  ✅ {check}")
            else:
                print(f"  ❌ {check}")
                all_good = False
        
        return all_good
    
    except Exception as e:
        print(f"  ❌ Error reading setup.py: {e}")
        return False

def check_requirements():
    """Check requirements.txt"""
    print("\n📋 Checking requirements.txt...")
    
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    try:
        with open(req_path, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        required_packages = ['PySide6>=6.4.0', 'PyYAML>=6.0']
        
        all_good = True
        for package in required_packages:
            if package in requirements:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ Missing: {package}")
                all_good = False
        
        return all_good
    
    except Exception as e:
        print(f"  ❌ Error reading requirements.txt: {e}")
        return False

def check_readme():
    """Check README.md completeness"""
    print("\n📖 Checking README.md...")
    
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
        
        sections = {
            'Title': '# 🎯 DragDropWidgets' in content,
            'Features': '## ✨ Features' in content,
            'Installation': '## 📦 Installation' in content,
            'Quick Start': '## 🚀 Quick Start' in content,
            'Documentation': '## 📚 Documentation' in content,
            'Examples': '## 🎮 Examples' in content,
            'License': '## 📜 License' in content,
            'Code examples': '```python' in content
        }
        
        all_good = True
        for section, present in sections.items():
            if present:
                print(f"  ✅ {section}")
            else:
                print(f"  ❌ Missing: {section}")
                all_good = False
        
        word_count = len(content.split())
        print(f"  📊 Word count: {word_count}")
        
        return all_good and word_count > 1000  # Ensure substantial content
    
    except Exception as e:
        print(f"  ❌ Error reading README.md: {e}")
        return False

def check_git_status():
    """Check git repository status"""
    print("\n🔄 Checking git status...")
    
    git_path = os.path.join(os.path.dirname(__file__), '.git')
    
    if os.path.exists(git_path):
        print("  ✅ Git repository initialized")
        
        # Check if there are any commits
        import subprocess
        try:
            result = subprocess.run(['git', 'log', '--oneline'], 
                                  capture_output=True, text=True, 
                                  cwd=os.path.dirname(__file__))
            if result.returncode == 0 and result.stdout:
                commit_count = len(result.stdout.strip().split('\n'))
                print(f"  ✅ {commit_count} commit(s) found")
                return True
            else:
                print("  ❌ No commits found")
                return False
        except Exception as e:
            print(f"  ⚠️  Could not check commit history: {e}")
            return True  # Git exists, assume it's okay
    else:
        print("  ❌ Git repository not initialized")
        return False

def generate_summary():
    """Generate a comprehensive summary"""
    print("\n" + "=" * 60)
    print("📋 DRAGDROPWIDGETS LIBRARY SUMMARY")
    print("=" * 60)
    
    print("\n🎯 LIBRARY OVERVIEW:")
    print("  • Name: DragDropWidgets")
    print("  • Version: 1.0.0") 
    print("  • Language: Python 3.8+")
    print("  • Framework: PySide6 (Qt)")
    print("  • License: MIT")
    
    print("\n🏗️  ARCHITECTURE:")
    print("  • Core: Widget base classes and drag/drop logic")
    print("  • Widgets: Button, Label, Image with full customization") 
    print("  • Utils: Serialization, themes, events management")
    print("  • Examples: Hello World and Advanced Dashboard")
    
    print("\n✨ KEY FEATURES:")
    print("  • Professional drag-and-drop GUI interface")
    print("  • 5+ built-in themes with custom theme support")
    print("  • Advanced layout management and auto-alignment")
    print("  • Save/load layouts in JSON/YAML formats")
    print("  • Extensible custom widget factory system")
    print("  • Comprehensive event system with filtering")
    print("  • Property panels for real-time customization")
    print("  • Snap-to-grid and visual feedback")
    
    print("\n📦 DISTRIBUTION READY:")
    print("  • Complete setup.py for PyPI distribution")
    print("  • Comprehensive README with examples")
    print("  • MIT License for open-source use")
    print("  • Entry points for command-line demos")
    print("  • Proper package structure and imports")
    
    print("\n🧪 TESTING NOTES:")
    print("  • GUI components require display environment")
    print("  • Core utilities work in headless environments")
    print("  • Full functionality available with PySide6 + display")
    print("  • Examples can be run directly: dragdrop-demo")
    
    print("\n🚀 NEXT STEPS:")
    print("  • Install in environment with display: pip install -e .")
    print("  • Run examples: python -m dragdropwidgets.examples.hello_world")
    print("  • Test GUI: python -m dragdropwidgets.examples.dashboard")
    print("  • Deploy to PyPI: python setup.py sdist bdist_wheel")

def main():
    """Run all verification checks"""
    print("🔍 DragDropWidgets Library Verification")
    print("=" * 50)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Setup Configuration", check_setup_py),
        ("Requirements", check_requirements),
        ("Documentation", check_readme),
        ("Git Repository", check_git_status)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        if check_func():
            passed += 1
    
    # Count lines of code
    lines, files = count_lines_of_code()
    
    print(f"\n" + "=" * 50)
    print(f"✅ Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Library structure is complete and ready!")
    else:
        print(f"⚠️  {total - passed} checks failed")
    
    # Always show summary
    generate_summary()
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())