"""
Advanced event management system for the library
"""

from PySide6.QtCore import QObject, Signal
from typing import Callable, Dict, List, Any, Optional
from enum import Enum
import weakref
from datetime import datetime

class EventPriority(Enum):
    """Event priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class Event:
    """Event object containing event data"""
    
    def __init__(self, event_type: str, source: Any = None, data: Dict[str, Any] = None, priority: EventPriority = EventPriority.NORMAL):
        self.event_type = event_type
        self.source = source
        self.data = data or {}
        self.priority = priority
        self.timestamp = datetime.now()
        self.cancelled = False
        self.handled = False
    
    def cancel(self):
        """Cancel the event (prevent further propagation)"""
        self.cancelled = True
    
    def mark_handled(self):
        """Mark event as handled"""
        self.handled = True

class EventHandler:
    """Event handler wrapper"""
    
    def __init__(self, callback: Callable, priority: EventPriority = EventPriority.NORMAL, once: bool = False):
        self.callback = callback
        self.priority = priority
        self.once = once
        self.call_count = 0
        self.enabled = True
    
    def __call__(self, event: Event) -> Any:
        if not self.enabled:
            return None
        
        result = self.callback(event)
        self.call_count += 1
        
        if self.once:
            self.enabled = False
        
        return result

class EventManager(QObject):
    """Advanced event manager for the library"""
    
    # Qt signals for integration
    event_triggered = Signal(object)  # Emitted when any event is triggered
    
    def __init__(self):
        super().__init__()
        self._event_handlers: Dict[str, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._enabled = True
        
        # Weak references to prevent memory leaks
        self._weak_handlers: Dict[str, List] = {}
    
    def register_event(self, event_name: str, handler: Callable, 
                      priority: EventPriority = EventPriority.NORMAL, 
                      once: bool = False) -> str:
        """Register an event handler"""
        if not callable(handler):
            raise ValueError("Handler must be callable")
        
        event_handler = EventHandler(handler, priority, once)
        
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        
        self._event_handlers[event_name].append(event_handler)
        
        # Sort by priority (highest first)
        self._event_handlers[event_name].sort(key=lambda h: h.priority.value, reverse=True)
        
        # Return handler ID for removal
        return f"{event_name}_{id(event_handler)}"
    
    def register_global_handler(self, handler: Callable, 
                              priority: EventPriority = EventPriority.NORMAL) -> str:
        """Register a global event handler (receives all events)"""
        if not callable(handler):
            raise ValueError("Handler must be callable")
        
        event_handler = EventHandler(handler, priority)
        self._global_handlers.append(event_handler)
        
        # Sort by priority
        self._global_handlers.sort(key=lambda h: h.priority.value, reverse=True)
        
        return f"global_{id(event_handler)}"
    
    def emit_event(self, event_name: str, source: Any = None, 
                   data: Dict[str, Any] = None, 
                   priority: EventPriority = EventPriority.NORMAL) -> Event:
        """Emit an event"""
        if not self._enabled:
            return None
        
        # Create event object
        event = Event(event_name, source, data, priority)
        
        # Add to history
        self._add_to_history(event)
        
        # Emit Qt signal
        self.event_triggered.emit(event)
        
        # Process global handlers first
        for handler in self._global_handlers:
            if not handler.enabled or event.cancelled:
                break
            
            try:
                handler(event)
            except Exception as e:
                print(f"Error in global event handler: {e}")
        
        # Process specific event handlers
        if event_name in self._event_handlers and not event.cancelled:
            for handler in self._event_handlers[event_name]:
                if not handler.enabled or event.cancelled:
                    break
                
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler for '{event_name}': {e}")
        
        return event
    
    def remove_event_handler(self, event_name: str, handler: Callable):
        """Remove a specific event handler"""
        if event_name in self._event_handlers:
            handlers_to_remove = []
            for event_handler in self._event_handlers[event_name]:
                if event_handler.callback == handler:
                    handlers_to_remove.append(event_handler)
            
            for event_handler in handlers_to_remove:
                self._event_handlers[event_name].remove(event_handler)
            
            # Remove empty event lists
            if not self._event_handlers[event_name]:
                del self._event_handlers[event_name]
    
    def remove_all_handlers(self, event_name: str):
        """Remove all handlers for an event"""
        if event_name in self._event_handlers:
            del self._event_handlers[event_name]
    
    def clear_all_handlers(self):
        """Clear all event handlers"""
        self._event_handlers.clear()
        self._global_handlers.clear()
    
    def enable_handler(self, handler_id: str):
        """Enable a specific handler"""
        # This would need more sophisticated handler tracking
        pass
    
    def disable_handler(self, handler_id: str):
        """Disable a specific handler"""
        # This would need more sophisticated handler tracking
        pass
    
    def enable_event_manager(self):
        """Enable the event manager"""
        self._enabled = True
    
    def disable_event_manager(self):
        """Disable the event manager"""
        self._enabled = False
    
    def _add_to_history(self, event: Event):
        """Add event to history"""
        self._event_history.append(event)
        
        # Maintain history size
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
    
    def get_event_history(self, event_type: str = None, limit: int = None) -> List[Event]:
        """Get event history"""
        history = self._event_history
        
        # Filter by event type
        if event_type:
            history = [e for e in history if e.event_type == event_type]
        
        # Apply limit
        if limit:
            history = history[-limit:]
        
        return history
    
    def clear_event_history(self):
        """Clear event history"""
        self._event_history.clear()
    
    def get_handler_count(self, event_name: str = None) -> int:
        """Get number of handlers"""
        if event_name:
            return len(self._event_handlers.get(event_name, []))
        else:
            return sum(len(handlers) for handlers in self._event_handlers.values()) + len(self._global_handlers)
    
    def get_registered_events(self) -> List[str]:
        """Get list of events with registered handlers"""
        return list(self._event_handlers.keys())
    
    def create_event_context(self, context_name: str):
        """Create an event context for scoped handlers"""
        return EventContext(self, context_name)

class EventContext:
    """Event context for scoped event handling"""
    
    def __init__(self, event_manager: EventManager, context_name: str):
        self.event_manager = event_manager
        self.context_name = context_name
        self.handlers: List[tuple] = []  # (event_name, handler)
    
    def register_event(self, event_name: str, handler: Callable, 
                      priority: EventPriority = EventPriority.NORMAL, 
                      once: bool = False) -> str:
        """Register event in this context"""
        handler_id = self.event_manager.register_event(event_name, handler, priority, once)
        self.handlers.append((event_name, handler))
        return handler_id
    
    def clear_context(self):
        """Clear all handlers in this context"""
        for event_name, handler in self.handlers:
            self.event_manager.remove_event_handler(event_name, handler)
        self.handlers.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_context()

# Predefined event types for the library
class WidgetEvents:
    """Standard widget event types"""
    
    # Widget lifecycle
    WIDGET_CREATED = "widget_created"
    WIDGET_DESTROYED = "widget_destroyed"
    WIDGET_SHOWN = "widget_shown"
    WIDGET_HIDDEN = "widget_hidden"
    
    # Widget interaction
    WIDGET_SELECTED = "widget_selected"
    WIDGET_DESELECTED = "widget_deselected"
    WIDGET_CLICKED = "widget_clicked"
    WIDGET_DOUBLE_CLICKED = "widget_double_clicked"
    
    # Drag and drop
    DRAG_STARTED = "drag_started"
    DRAG_MOVED = "drag_moved"
    DRAG_FINISHED = "drag_finished"
    WIDGET_DROPPED = "widget_dropped"
    
    # Widget modification
    WIDGET_MOVED = "widget_moved"
    WIDGET_RESIZED = "widget_resized"
    WIDGET_PROPERTY_CHANGED = "widget_property_changed"
    
    # Layout events
    LAYOUT_CHANGED = "layout_changed"
    LAYOUT_LOADED = "layout_loaded"
    LAYOUT_SAVED = "layout_saved"

class DropZoneEvents:
    """Drop zone specific events"""
    
    DROP_ZONE_ENTERED = "drop_zone_entered"
    DROP_ZONE_LEFT = "drop_zone_left"
    DROP_ZONE_CLEARED = "drop_zone_cleared"
    GRID_TOGGLED = "grid_toggled"
    LAYOUT_MODE_CHANGED = "layout_mode_changed"

class ApplicationEvents:
    """Application-level events"""
    
    APP_STARTED = "app_started"
    APP_CLOSING = "app_closing"
    THEME_CHANGED = "theme_changed"
    SETTINGS_CHANGED = "settings_changed"
    ERROR_OCCURRED = "error_occurred"

# Create global event manager instance
event_manager = EventManager()

# Convenience functions
def on(event_name: str, handler: Callable, priority: EventPriority = EventPriority.NORMAL, once: bool = False) -> str:
    """Shortcut to register event handler"""
    return event_manager.register_event(event_name, handler, priority, once)

def emit(event_name: str, source: Any = None, data: Dict[str, Any] = None, priority: EventPriority = EventPriority.NORMAL) -> Event:
    """Shortcut to emit event"""
    return event_manager.emit_event(event_name, source, data, priority)

def off(event_name: str, handler: Callable):
    """Shortcut to remove event handler"""
    return event_manager.remove_event_handler(event_name, handler)

def once(event_name: str, handler: Callable, priority: EventPriority = EventPriority.NORMAL) -> str:
    """Register one-time event handler"""
    return event_manager.register_event(event_name, handler, priority, once=True)