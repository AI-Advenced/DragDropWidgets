#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de widgets personnalisés

Ce fichier démontre :
- Création de widgets personnalisés
- Héritage de DraggableWidget
- Gestion des propriétés personnalisées
- Sérialisation de widgets personnalisés
- Factory de widgets

Exécution :
    python custom_widget_demo.py
"""

import sys
import uuid
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QProgressBar, QSpinBox
from PySide6.QtCore import Qt, QPoint, Signal
from dragdropwidgets import create_app, DraggableWidget, DraggableButton, DraggableLabel
from dragdropwidgets.widgets.custom import CustomWidgetFactory


class CounterWidget(DraggableWidget):
    """Widget compteur personnalisé"""
    
    value_changed = Signal(int)
    
    def __init__(self, initial_value=0, parent=None):
        super().__init__(parent)
        self.count = initial_value
        self.setup_ui()
        self.metadata.update({
            'count': self.count,
            'widget_type': 'counter',
            'min_value': 0,
            'max_value': 100
        })
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.label = QLabel(f"Compte: {self.count}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        btn_layout = QHBoxLayout()
        self.minus_btn = QPushButton("-")
        self.plus_btn = QPushButton("+")
        self.reset_btn = QPushButton("Reset")
        
        btn_layout.addWidget(self.minus_btn)
        btn_layout.addWidget(self.plus_btn)
        btn_layout.addWidget(self.reset_btn)
        
        layout.addWidget(self.label)
        layout.addLayout(btn_layout)
        
        # Connexions
        self.plus_btn.clicked.connect(self.increment)
        self.minus_btn.clicked.connect(self.decrement)
        self.reset_btn.clicked.connect(self.reset)
        
        self.resize(150, 80)
        self.setStyleSheet("""
            CounterWidget {
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: #ecf0f1;
            }
        """)
    
    def increment(self):
        if self.count < self.metadata['max_value']:
            self.count += 1
            self.update_display()
    
    def decrement(self):
        if self.count > self.metadata['min_value']:
            self.count -= 1
            self.update_display()
    
    def reset(self):
        self.count = 0
        self.update_display()
    
    def update_display(self):
        self.label.setText(f"Compte: {self.count}")
        self.metadata['count'] = self.count
        self.value_changed.emit(self.count)
    
    def get_value(self):
        return self.count
    
    def set_value(self, value):
        self.count = max(self.metadata['min_value'], 
                        min(self.metadata['max_value'], value))
        self.update_display()


class GaugeWidget(DraggableWidget):
    """Widget jauge circulaire personnalisé"""
    
    def __init__(self, value=50, parent=None):
        super().__init__(parent)
        self.value = value
        self.setup_ui()
        self.metadata.update({
            'value': self.value,
            'widget_type': 'gauge',
            'min_value': 0,
            'max_value': 100,
            'color': '#2ecc71'
        })
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel("Gauge")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(self.value)
        self.progress.setTextVisible(True)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.value)
        self.slider.valueChanged.connect(self.on_value_changed)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.slider)
        
        self.resize(200, 100)
        self.setStyleSheet("""
            GaugeWidget {
                border: 2px solid #27ae60;
                border-radius: 10px;
                background-color: #d5f4e6;
                padding: 5px;
            }
        """)
    
    def on_value_changed(self, value):
        self.value = value
        self.progress.setValue(value)
        self.metadata['value'] = value
    
    def set_title(self, title):
        self.title_label.setText(title)
    
    def get_value(self):
        return self.value


class CalculatorWidget(DraggableWidget):
    """Widget calculatrice simple"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result = 0
        self.setup_ui()
        self.metadata.update({
            'result': self.result,
            'widget_type': 'calculator'
        })
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Display
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            background-color: #34495e; 
            color: #ecf0f1; 
            padding: 10px;
            border-radius: 5px;
        """)
        
        # Input controls
        input_layout = QHBoxLayout()
        
        self.num1_spin = QSpinBox()
        self.num1_spin.setRange(-1000, 1000)
        self.num1_spin.setValue(0)
        
        self.operator_btn = QPushButton("+")
        self.operator_btn.clicked.connect(self.cycle_operator)
        
        self.num2_spin = QSpinBox()
        self.num2_spin.setRange(-1000, 1000)
        self.num2_spin.setValue(0)
        
        self.equals_btn = QPushButton("=")
        self.equals_btn.clicked.connect(self.calculate)
        
        input_layout.addWidget(self.num1_spin)
        input_layout.addWidget(self.operator_btn)
        input_layout.addWidget(self.num2_spin)
        input_layout.addWidget(self.equals_btn)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)
        
        btn_layout.addWidget(self.clear_btn)
        
        layout.addWidget(self.display)
        layout.addLayout(input_layout)
        layout.addLayout(btn_layout)
        
        self.resize(250, 120)
        self.setStyleSheet("""
            CalculatorWidget {
                border: 2px solid #8e44ad;
                border-radius: 8px;
                background-color: #f4ecf7;
                padding: 5px;
            }
        """)
        
        self.operators = ['+', '-', '*', '/']
        self.current_op_index = 0
    
    def cycle_operator(self):
        self.current_op_index = (self.current_op_index + 1) % len(self.operators)
        self.operator_btn.setText(self.operators[self.current_op_index])
    
    def calculate(self):
        try:
            num1 = self.num1_spin.value()
            num2 = self.num2_spin.value()
            op = self.operators[self.current_op_index]
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/' and num2 != 0:
                result = num1 / num2
            else:
                result = 0
            
            self.result = result
            self.display.setText(str(round(result, 2)))
            self.metadata['result'] = result
            
        except Exception as e:
            self.display.setText("Erreur")
    
    def clear(self):
        self.num1_spin.setValue(0)
        self.num2_spin.setValue(0)
        self.current_op_index = 0
        self.operator_btn.setText('+')
        self.display.setText("0")
        self.result = 0
        self.metadata['result'] = 0


def main():
    """Fonction principale de la démonstration"""
    app, window, drop_zone = create_app("Démonstration Widgets Personnalisés", (1200, 800))
    
    print("🛠️ Démonstration de widgets personnalisés")
    print("=" * 50)
    
    # Configuration
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre
    title = DraggableLabel("Galerie de Widgets Personnalisés")
    title.set_style_preset('title')
    title.set_font_size(22)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section 1: Widgets de démonstration
    demo_title = DraggableLabel("Widgets Personnalisés")
    demo_title.set_style_preset('subtitle')
    demo_title.set_font_size(16)
    drop_zone.add_widget(demo_title, QPoint(50, 100))
    
    # Créer des instances des widgets personnalisés
    custom_widgets = []
    
    # Compteurs
    for i in range(3):
        counter = CounterWidget(i * 10)
        drop_zone.add_widget(counter, QPoint(70 + i * 180, 140))
        custom_widgets.append(counter)
    
    # Jauges
    for i in range(2):
        gauge = GaugeWidget((i + 1) * 30)
        gauge.set_title(f"Gauge {i + 1}")
        drop_zone.add_widget(gauge, QPoint(70 + i * 220, 280))
        custom_widgets.append(gauge)
    
    # Calculatrices
    calc1 = CalculatorWidget()
    drop_zone.add_widget(calc1, QPoint(70, 420))
    custom_widgets.append(calc1)
    
    calc2 = CalculatorWidget()
    drop_zone.add_widget(calc2, QPoint(340, 420))
    custom_widgets.append(calc2)
    
    # Section 2: Contrôles et informations
    controls_title = DraggableLabel("Contrôles et Informations")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(700, 100))
    
    # Informations sur les widgets
    info_display = DraggableLabel("Informations sur les widgets personnalisés")
    info_display.resize(350, 200)
    info_display.set_background_color("#f8f9fa")
    info_display.set_word_wrap(True)
    drop_zone.add_widget(info_display, QPoint(720, 140))
    
    def update_info_display():
        """Mettre à jour l'affichage des informations"""
        info_text = "📊 Widgets Personnalisés Actifs:\n\n"
        
        counters = [w for w in custom_widgets if isinstance(w, CounterWidget)]
        gauges = [w for w in custom_widgets if isinstance(w, GaugeWidget)]
        calculators = [w for w in custom_widgets if isinstance(w, CalculatorWidget)]
        
        info_text += f"🔢 Compteurs ({len(counters)}):\n"
        for i, counter in enumerate(counters):
            info_text += f"  • Compteur {i+1}: {counter.get_value()}\n"
        
        info_text += f"\n📊 Jauges ({len(gauges)}):\n"
        for i, gauge in enumerate(gauges):
            info_text += f"  • Gauge {i+1}: {gauge.get_value()}%\n"
        
        info_text += f"\n🧮 Calculatrices ({len(calculators)}):\n"
        for i, calc in enumerate(calculators):
            info_text += f"  • Calc {i+1}: {calc.result}\n"
        
        info_display.set_text(info_text)
    
    # Boutons d'action
    action_buttons = [
        ("Actualiser Info", lambda: update_info_display()),
        ("Créer Compteur", lambda: create_new_counter()),
        ("Créer Jauge", lambda: create_new_gauge()),
        ("Reset Tous", lambda: reset_all_widgets()),
    ]
    
    def create_new_counter():
        counter = CounterWidget(0)
        drop_zone.add_widget(counter, QPoint(600, 300))
        custom_widgets.append(counter)
        update_info_display()
        print("➕ Nouveau compteur créé")
    
    def create_new_gauge():
        gauge = GaugeWidget(50)
        gauge.set_title("Nouvelle Gauge")
        drop_zone.add_widget(gauge, QPoint(600, 400))
        custom_widgets.append(gauge)
        update_info_display()
        print("➕ Nouvelle jauge créée")
    
    def reset_all_widgets():
        for widget in custom_widgets:
            if isinstance(widget, CounterWidget):
                widget.reset()
            elif isinstance(widget, CalculatorWidget):
                widget.clear()
        update_info_display()
        print("🔄 Tous les widgets réinitialisés")
    
    for i, (name, action) in enumerate(action_buttons):
        btn = DraggableButton(name)
        btn.set_style('info')
        btn.button_clicked.connect(lambda _, a=action: a())
        drop_zone.add_widget(btn, QPoint(720, 360 + i * 40))
    
    # Section 3: Enregistrement dans la factory
    factory_title = DraggableLabel("Factory de Widgets")
    factory_title.set_style_preset('subtitle')
    factory_title.set_font_size(16)
    drop_zone.add_widget(factory_title, QPoint(700, 520))
    
    # Enregistrer les widgets personnalisés
    CustomWidgetFactory.register_widget(
        'CounterWidget',
        CounterWidget,
        {
            'description': 'Widget compteur avec boutons +/-',
            'category': 'Personnalisé',
            'icon': '🔢',
            'default_size': (150, 80)
        }
    )
    
    CustomWidgetFactory.register_widget(
        'GaugeWidget', 
        GaugeWidget,
        {
            'description': 'Jauge avec slider et barre de progression',
            'category': 'Personnalisé',
            'icon': '📊',
            'default_size': (200, 100)
        }
    )
    
    # Afficher les widgets disponibles
    available = CustomWidgetFactory.get_available_widgets()
    factory_info = DraggableLabel(f"Widgets enregistrés:\n{', '.join(available)}")
    factory_info.resize(350, 60)
    factory_info.set_background_color("#e8f5e8")
    factory_info.set_word_wrap(True)
    drop_zone.add_widget(factory_info, QPoint(720, 560))
    
    # Instructions
    instructions = DraggableLabel(
        "🛠️ Démonstration de Widgets Personnalisés:\n"
        "• Interagissez avec les compteurs, jauges et calculatrices\n"
        "• Créez de nouveaux widgets avec les boutons\n"
        "• Observez les propriétés personnalisées\n"
        "• Tous les widgets restent déplaçables"
    )
    instructions.set_style_preset('info')
    instructions.resize(500, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 600))
    
    # Connecter les signaux des compteurs
    for widget in custom_widgets:
        if isinstance(widget, CounterWidget):
            widget.value_changed.connect(lambda v: update_info_display())
    
    # Initialiser l'affichage
    update_info_display()
    
    window.show()
    print(f"📱 Démonstration lancée avec {len(custom_widgets)} widgets personnalisés")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)