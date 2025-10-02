#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Premier exemple simple - Création d'une interface basique

Ce fichier démontre les concepts de base du système DragDropWidgets :
- Création d'une application simple
- Ajout de widgets draggables
- Configuration basique des styles

Exécution :
    python hello_world.py
"""

import sys
from PySide6.QtCore import QPoint
from dragdropwidgets import create_app, DraggableButton, DraggableLabel


def main():
    """Fonction principale de l'exemple Hello World"""
    # Créer l'application et la fenêtre principale
    app, window, drop_zone = create_app("Hello World - DragDropWidgets", (600, 400))
    
    print("🚀 Démarrage de l'exemple Hello World")
    print("=" * 50)
    print("Instructions:")
    print("• Cliquez et faites glisser les widgets")
    print("• Le bouton est cliquable")
    print("• Fermez la fenêtre pour quitter")
    print("=" * 50)
    
    # Créer un bouton simple
    button = DraggableButton("Hello World!")
    button.set_style('primary')  # Style bleu primaire
    
    # Créer un label informatif
    label = DraggableLabel("Bienvenue dans DragDropWidgets!")
    label.set_font_size(16)
    label.set_style_preset('title')
    
    # Créer un second label avec instructions
    instructions = DraggableLabel("Faites glisser les widgets pour les déplacer")
    instructions.set_font_size(12)
    instructions.set_style_preset('info')
    
    # Ajouter les widgets à la zone de dépôt avec des positions spécifiques
    drop_zone.add_widget(button, QPoint(100, 100))
    drop_zone.add_widget(label, QPoint(100, 200))
    drop_zone.add_widget(instructions, QPoint(100, 280))
    
    # Activer la grille pour un placement plus précis
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 20
    
    # Configurer le snap-to-grid pour tous les widgets
    for widget in [button, label, instructions]:
        if hasattr(widget, 'set_snap_to_grid'):
            widget.set_snap_to_grid(True, 20)
    
    # Gestionnaire d'événements pour le bouton
    def on_button_click(widget_id):
        """Gestionnaire de clic sur le bouton"""
        print(f"✅ Bouton cliqué! ID: {widget_id}")
        # Changer le texte du bouton
        button.set_text("Bouton cliqué!")
        button.set_style('success')  # Changer en vert
        
        # Mettre à jour le label
        label.set_text("Excellent! Le bouton fonctionne!")
        label.set_style_preset('success')
    
    # Connecter le signal du bouton
    button.button_clicked.connect(on_button_click)
    
    # Afficher la fenêtre et démarrer la boucle d'événements
    window.show()
    
    print(f"📱 Fenêtre affichée: {window.windowTitle()}")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)