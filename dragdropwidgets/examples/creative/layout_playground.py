#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terrain de jeu pour tester différents layouts

Ce fichier démontre :
- Gestionnaire de layout dynamique
- Arrangements automatiques (grille, circulaire, alignement)
- Distribution spatiale
- Redimensionnement uniforme
- Animations de layout

Exécution :
    python layout_playground.py
"""

import sys
import random
from PySide6.QtCore import QPoint, QTimer
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.core.layout_manager import DynamicLayoutManager


def main():
    """Fonction principale du terrain de jeu layout"""
    app, window, drop_zone = create_app("Layout Playground", (1400, 900))
    
    print("📐 Terrain de jeu pour layouts")
    print("=" * 50)
    
    # Configuration
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 20
    
    # Titre
    title = DraggableLabel("Layout Playground - Gestionnaire de Layouts Dynamiques")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Créer le gestionnaire de layout
    layout_manager = DynamicLayoutManager(drop_zone)
    
    # Créer des widgets de test
    test_widgets = []
    colors = ['primary', 'success', 'danger', 'warning', 'info', 'secondary']
    
    for i in range(12):
        btn = DraggableButton(f"Widget {i+1}")
        btn.set_style(colors[i % len(colors)])
        btn.set_snap_to_grid(True, 20)
        # Placement initial aléatoire
        x = random.randint(100, 600)
        y = random.randint(100, 400)
        drop_zone.add_widget(btn, QPoint(x, y))
        test_widgets.append(btn)
    
    # Section de contrôles
    controls_title = DraggableLabel("Contrôles de Layout")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(800, 80))
    
    # Boutons de layout
    layout_controls = [
        ("Grille 3x4", lambda: layout_manager.create_layout_grid(test_widgets, 3, 30)),
        ("Grille 4x3", lambda: layout_manager.create_layout_grid(test_widgets, 4, 25)),
        ("Grille 2x6", lambda: layout_manager.create_layout_grid(test_widgets, 2, 35)),
        ("Ligne Horizontale", lambda: layout_manager.create_layout_grid(test_widgets, 12, 20)),
        ("Colonne Verticale", lambda: layout_manager.create_layout_grid(test_widgets, 1, 25)),
        ("Cercle Large", lambda: layout_manager.create_circular_layout(test_widgets, QPoint(400, 300), 200)),
        ("Cercle Petit", lambda: layout_manager.create_circular_layout(test_widgets, QPoint(400, 300), 120)),
        ("Distribution H", lambda: layout_manager.distribute_widgets(test_widgets, 'horizontal')),
        ("Distribution V", lambda: layout_manager.distribute_widgets(test_widgets, 'vertical')),
        ("Aligner Gauche", lambda: layout_manager.auto_align_widgets(test_widgets, 'left')),
        ("Aligner Droite", lambda: layout_manager.auto_align_widgets(test_widgets, 'right')),
        ("Centrer H", lambda: layout_manager.auto_align_widgets(test_widgets, 'center_horizontal')),
        ("Centrer V", lambda: layout_manager.auto_align_widgets(test_widgets, 'center_vertical')),
        ("Taille Uniforme", lambda: layout_manager.resize_widgets_uniform(test_widgets, 'both')),
        ("Largeur Uniforme", lambda: layout_manager.resize_widgets_uniform(test_widgets, 'width')),
        ("Hauteur Uniforme", lambda: layout_manager.resize_widgets_uniform(test_widgets, 'height')),
        ("Mélanger", lambda: randomize_positions()),
        ("Animation Spirale", lambda: animate_spiral()),
    ]
    
    control_buttons = []
    for i, (name, action) in enumerate(layout_controls):
        btn = DraggableButton(name)
        btn.set_style('info')
        btn.button_clicked.connect(lambda _, a=action: a())
        
        col = i % 2
        row = i // 2
        x_pos = 820 + col * 140
        y_pos = 120 + row * 40
        
        drop_zone.add_widget(btn, QPoint(x_pos, y_pos))
        control_buttons.append(btn)
    
    # Fonctions spéciales
    def randomize_positions():
        """Mélanger les positions aléatoirement"""
        for widget in test_widgets:
            x = random.randint(100, 600)
            y = random.randint(100, 500)
            widget.animate_to_position(QPoint(x, y), duration=500)
        print("🎲 Positions mélangées")
    
    def animate_spiral():
        """Animation en spirale"""
        center = QPoint(400, 300)
        import math
        
        for i, widget in enumerate(test_widgets):
            angle = (i / len(test_widgets)) * 4 * math.pi
            radius = 50 + (i * 10)
            x = center.x() + int(radius * math.cos(angle))
            y = center.y() + int(radius * math.sin(angle))
            
            # Délai progressif pour effet de spirale
            QTimer.singleShot(i * 100, lambda w=widget, pos=QPoint(x, y): w.animate_to_position(pos, 600))
        
        print("🌀 Animation spirale démarrée")
    
    # Zone d'information
    info_display = DraggableLabel("Cliquez sur les boutons pour tester les différents layouts")
    info_display.resize(350, 60)
    info_display.set_background_color("#e8f4f8")
    info_display.set_word_wrap(True)
    drop_zone.add_widget(info_display, QPoint(800, 500))
    
    # Statistiques
    stats_title = DraggableLabel("Statistiques")
    stats_title.set_style_preset('subtitle')
    drop_zone.add_widget(stats_title, QPoint(800, 580))
    
    stats_display = DraggableLabel(f"Widgets: {len(test_widgets)}\nLayouts disponibles: {len(layout_controls)}")
    stats_display.set_font_size(11)
    drop_zone.add_widget(stats_display, QPoint(820, 610))
    
    # Instructions
    instructions = DraggableLabel(
        "📐 Playground de Layouts:\n"
        "• Testez différents arrangements automatiques\n"
        "• Observez les animations de transition\n"
        "• Mélangez et réorganisez à volonté\n"
        "• Tous les widgets restent interactifs"
    )
    instructions.set_style_preset('info')
    instructions.resize(400, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 600))
    
    window.show()
    print(f"📱 Layout Playground lancé avec {len(test_widgets)} widgets de test")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)