"""
Layout serialization system for saving and loading layouts
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class LayoutSerializer:
    """Class for saving and loading interface layouts"""
    
    @staticmethod
    def save_to_json(layout_data: Dict[str, Any], file_path: str) -> bool:
        """Save layout to JSON file"""
        try:
            # Add metadata
            layout_data['metadata'] = {
                'version': '1.0.0',
                'created_at': datetime.now().isoformat(),
                'library': 'DragDropWidgets'
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(layout_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_from_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Load layout from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate format
            if LayoutSerializer._validate_layout_data(data):
                return data
            else:
                print("Invalid layout file format")
                return None
                
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None
    
    @staticmethod
    def save_to_yaml(layout_data: Dict[str, Any], file_path: str) -> bool:
        """Save layout to YAML file"""
        try:
            # Add metadata
            layout_data['metadata'] = {
                'version': '1.0.0',
                'created_at': datetime.now().isoformat(),
                'library': 'DragDropWidgets'
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(layout_data, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            return True
        except Exception as e:
            print(f"Error saving YAML: {e}")
            return False
    
    @staticmethod
    def load_from_yaml(file_path: str) -> Optional[Dict[str, Any]]:
        """Load layout from YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Validate format
            if LayoutSerializer._validate_layout_data(data):
                return data
            else:
                print("Invalid layout file format")
                return None
                
        except Exception as e:
            print(f"Error loading YAML: {e}")
            return None
    
    @staticmethod
    def create_backup(layout_data: Dict[str, Any], backup_dir: str = "backups") -> str:
        """Create backup copy of layout"""
        Path(backup_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/layout_backup_{timestamp}.json"
        
        if LayoutSerializer.save_to_json(layout_data, backup_file):
            return backup_file
        
        return ""
    
    @staticmethod
    def export_to_code(layout_data: Dict[str, Any], language: str = "python") -> str:
        """Export layout as executable code"""
        if language.lower() == "python":
            return LayoutSerializer._generate_python_code(layout_data)
        else:
            return "# Unsupported language"
    
    @staticmethod
    def _generate_python_code(layout_data: Dict[str, Any]) -> str:
        """Generate Python code from layout data"""
        code_lines = [
            "#!/usr/bin/env python3",
            "\"\"\"",
            "Generated code from DragDropWidgets layout",
            f"Created: {datetime.now().isoformat()}",
            "\"\"\"",
            "",
            "import sys",
            "from dragdropwidgets import create_app, DraggableButton, DraggableLabel, DraggableImage",
            "from PySide6.QtCore import QPoint",
            "",
            "def main():",
            "    # Create application",
            "    app, window, drop_zone = create_app('Generated Layout', (800, 600))",
            "",
            "    # Configure drop zone",
        ]
        
        # Add drop zone settings
        if 'layout_mode' in layout_data:
            code_lines.append(f"    drop_zone.set_layout_mode('{layout_data['layout_mode']}')")
        if 'grid_size' in layout_data:
            code_lines.append(f"    drop_zone.grid_size = {layout_data['grid_size']}")
        if 'show_grid' in layout_data:
            code_lines.append(f"    drop_zone.set_grid_visible({layout_data['show_grid']})")
        
        code_lines.append("")
        code_lines.append("    # Create widgets")
        
        # Generate widget creation code
        widget_counter = 1
        for widget_data in layout_data.get('widgets', []):
            widget_type = widget_data.get('type', 'WidgetBase')
            metadata = widget_data.get('metadata', {})
            position = widget_data.get('position', {'x': 0, 'y': 0})
            size = widget_data.get('size', {'width': 100, 'height': 30})
            
            var_name = f"widget_{widget_counter}"
            
            # Create widget based on type
            if widget_type == 'DraggableButton':
                text = metadata.get('text', 'Button')
                code_lines.append(f"    {var_name} = DraggableButton('{text}')")
                
                if 'button_style' in metadata:
                    code_lines.append(f"    {var_name}.set_style('{metadata['button_style']}')")
                    
            elif widget_type == 'DraggableLabel':
                text = metadata.get('text', 'Label')
                code_lines.append(f"    {var_name} = DraggableLabel('{text}')")
                
                if 'font_size' in metadata:
                    code_lines.append(f"    {var_name}.set_font_size({metadata['font_size']})")
                if 'color' in metadata:
                    code_lines.append(f"    {var_name}.set_color('{metadata['color']}')")
                if 'alignment' in metadata:
                    code_lines.append(f"    {var_name}.set_alignment('{metadata['alignment']}')")
                    
            elif widget_type == 'DraggableImage':
                image_path = metadata.get('image_path', '')
                if image_path:
                    code_lines.append(f"    {var_name} = DraggableImage('{image_path}')")
                else:
                    code_lines.append(f"    {var_name} = DraggableImage()")
                    
                if 'scale_mode' in metadata:
                    code_lines.append(f"    {var_name}.set_scale_mode('{metadata['scale_mode']}')")
            else:
                code_lines.append(f"    # Unsupported widget type: {widget_type}")
                continue
            
            # Set position and size
            code_lines.append(f"    {var_name}.move({position['x']}, {position['y']})")
            code_lines.append(f"    {var_name}.resize({size['width']}, {size['height']})")
            
            # Add to drop zone
            code_lines.append(f"    drop_zone.add_widget({var_name})")
            code_lines.append("")
            
            widget_counter += 1
        
        # Add main execution code
        code_lines.extend([
            "    # Show window and run application",
            "    window.show()",
            "    return app.exec()",
            "",
            "if __name__ == '__main__':",
            "    sys.exit(main())"
        ])
        
        return "\n".join(code_lines)
    
    @staticmethod
    def _validate_layout_data(data: Dict[str, Any]) -> bool:
        """Validate layout data format"""
        if not isinstance(data, dict):
            return False
        
        # Check for required fields
        if 'widgets' not in data:
            return False
        
        if not isinstance(data['widgets'], list):
            return False
        
        # Validate each widget
        for widget in data['widgets']:
            if not isinstance(widget, dict):
                return False
            
            required_fields = ['id', 'type', 'position', 'size']
            for field in required_fields:
                if field not in widget:
                    return False
        
        return True
    
    @staticmethod
    def merge_layouts(layout1: Dict[str, Any], layout2: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two layout files"""
        merged = layout1.copy()
        
        # Merge widgets
        existing_ids = {w['id'] for w in merged.get('widgets', [])}
        
        for widget in layout2.get('widgets', []):
            if widget['id'] not in existing_ids:
                merged.setdefault('widgets', []).append(widget)
        
        # Update metadata
        merged['metadata'] = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'library': 'DragDropWidgets',
            'merged_from': [
                layout1.get('metadata', {}).get('created_at', 'unknown'),
                layout2.get('metadata', {}).get('created_at', 'unknown')
            ]
        }
        
        return merged
    
    @staticmethod
    def get_layout_statistics(layout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about a layout"""
        widgets = layout_data.get('widgets', [])
        
        # Count widgets by type
        widget_counts = {}
        for widget in widgets:
            widget_type = widget.get('type', 'Unknown')
            widget_counts[widget_type] = widget_counts.get(widget_type, 0) + 1
        
        # Calculate area coverage
        if widgets:
            min_x = min(w.get('position', {}).get('x', 0) for w in widgets)
            max_x = max(w.get('position', {}).get('x', 0) + w.get('size', {}).get('width', 0) for w in widgets)
            min_y = min(w.get('position', {}).get('y', 0) for w in widgets)
            max_y = max(w.get('position', {}).get('y', 0) + w.get('size', {}).get('height', 0) for w in widgets)
            
            layout_bounds = {
                'min_x': min_x, 'max_x': max_x,
                'min_y': min_y, 'max_y': max_y,
                'width': max_x - min_x,
                'height': max_y - min_y
            }
        else:
            layout_bounds = {}
        
        return {
            'total_widgets': len(widgets),
            'widget_types': widget_counts,
            'layout_bounds': layout_bounds,
            'layout_mode': layout_data.get('layout_mode', 'free'),
            'grid_size': layout_data.get('grid_size', 20),
            'created_at': layout_data.get('metadata', {}).get('created_at', 'unknown')
        }