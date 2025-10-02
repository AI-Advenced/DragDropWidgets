#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collection de contrôles de base avec différents styles

Ce fichier démontre :
- Différents styles de boutons
- Configuration de widgets
- Placement automatique
- Interaction avec multiple widgets

Exécution :
    python basic_controls.py
"""

import sys
from PySide6.QtCore import QPoint
from dragdropwidgets import create_app, DraggableButton, DraggableLabel


def main():
    """Fonction principale pour démontrer les contrôles basiques"""
    # Créer l'application
    app, window, drop_zone = create_app("Contrôles Basiques - DragDropWidgets", (800, 600))
    
    print("🎨 Démonstration des contrôles basiques")
    print("=" * 50)
    print("Styles de boutons disponibles:")
    print("• Primary (Bleu) - Action principale")
    print("• Success (Vert) - Action positive")
    print("• Danger (Rouge) - Action destructive")
    print("• Warning (Orange) - Attention")
    print("• Info (Cyan) - Information")
    print("• Secondary (Gris) - Action secondaire")
    print("=" * 50)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre principal
    title = DraggableLabel("Galerie de Contrôles Basiques")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 50))
    
    # Différents styles de boutons avec leurs caractéristiques
    button_styles = [
        ("Bouton Primaire", "primary", "Action principale du formulaire"),
        ("Bouton Succès", "success", "Confirmer une action positive"),
        ("Bouton Danger", "danger", "Action potentiellement destructive"),
        ("Bouton Avertissement", "warning", "Action nécessitant attention"),
        ("Bouton Info", "info", "Affichage d'informations"),
        ("Bouton Secondaire", "secondary", "Action secondaire ou annulation")
    ]
    
    # Créer et placer les boutons
    buttons = []
    for i, (text, style, description) in enumerate(button_styles):
        # Créer le bouton
        btn = DraggableButton(text)
        btn.set_style(style)
        btn.set_snap_to_grid(True, 25)
        
        # Créer une description
        desc_label = DraggableLabel(description)
        desc_label.set_font_size(10)
        desc_label.set_style_preset('caption')
        desc_label.set_snap_to_grid(True, 25)
        
        # Calculer les positions
        x_pos = 50
        y_pos = 120 + i * 80
        
        # Ajouter à la zone de dépôt
        drop_zone.add_widget(btn, QPoint(x_pos, y_pos))
        drop_zone.add_widget(desc_label, QPoint(x_pos + 200, y_pos + 5))
        
        buttons.append((btn, style, text))
    
    # Zone d'interaction à droite
    interaction_title = DraggableLabel("Zone d'Interaction")
    interaction_title.set_style_preset('subtitle')
    interaction_title.set_font_size(16)
    drop_zone.add_widget(interaction_title, QPoint(500, 120))
    
    # Label de statut
    status_label = DraggableLabel("Cliquez sur un bouton pour voir l'action")
    status_label.set_style_preset('info')
    status_label.resize(250, 60)
    status_label.set_word_wrap(True)
    drop_zone.add_widget(status_label, QPoint(500, 160))
    
    # Compteur de clics
    click_counter = {"count": 0}
    counter_label = DraggableLabel("Clics: 0")
    counter_label.set_style_preset('body')
    drop_zone.add_widget(counter_label, QPoint(500, 240))
    
    # Bouton de réinitialisation
    reset_btn = DraggableButton("Réinitialiser")
    reset_btn.set_style('secondary')
    drop_zone.add_widget(reset_btn, QPoint(500, 280))
    
    # Gestionnaire d'événements centralisé
    def handle_button_click(widget_id, button_info=None):
        """Gestionnaire centralisé pour tous les clics de boutons"""
        click_counter["count"] += 1
        counter_label.set_text(f"Clics: {click_counter['count']}")
        
        if button_info:
            btn, style, text = button_info
            status_message = f"Action '{style}' exécutée!\nBouton: {text}"
            status_label.set_text(status_message)
            
            # Animation visuelle simple : changer temporairement le texte
            original_text = btn.get_text()
            btn.set_text("Cliqué! ✓")
            
            # Remettre le texte original après 1 seconde
            from PySide6.QtCore import QTimer
            timer = QTimer()
            timer.singleShot(1000, lambda: btn.set_text(original_text))
            
            print(f"🔥 {style.upper()}: {text} - Clic #{click_counter['count']}")
    
    def reset_interactions():
        """Réinitialiser les interactions"""
        click_counter["count"] = 0
        counter_label.set_text("Clics: 0")
        status_label.set_text("Compteurs réinitialisés!")
        print("🔄 Interactions réinitialisées")
    
    # Connecter les signaux pour chaque bouton
    for btn, style, text in buttons:
        btn.button_clicked.connect(
            lambda widget_id, info=(btn, style, text): handle_button_click(widget_id, info)
        )
    
    # Connecter le bouton de réinitialisation
    reset_btn.button_clicked.connect(lambda _: reset_interactions())
    
    # Créer quelques contrôles additionnels
    
    # Bouton activable/désactivable
    toggle_btn = DraggableButton("Bouton Activable")
    toggle_btn.set_checkable(True)  # Rendre le bouton toggleable
    toggle_btn.set_style('info')
    drop_zone.add_widget(toggle_btn, QPoint(500, 350))
    
    toggle_status = DraggableLabel("État: Désactivé")
    toggle_status.set_font_size(10)
    drop_zone.add_widget(toggle_status, QPoint(500, 390))
    
    def handle_toggle(widget_id):
        """Gestionnaire pour le bouton toggle"""
        is_checked = toggle_btn.is_checked()
        if is_checked:
            toggle_btn.set_text("Désactiver")
            toggle_btn.set_style('success')
            toggle_status.set_text("État: Activé ✓")
            toggle_status.set_style_preset('success')
        else:
            toggle_btn.set_text("Bouton Activable")
            toggle_btn.set_style('info')
            toggle_status.set_text("État: Désactivé")
            toggle_status.set_style_preset('body')
        
        print(f"🔀 Toggle: {'Activé' if is_checked else 'Désactivé'}")
    
    toggle_btn.button_clicked.connect(handle_toggle)
    
    # Instructions finales
    final_instructions = DraggableLabel(
        "💡 Astuce: Tous les widgets peuvent être déplacés par glisser-déposer!"
    )
    final_instructions.set_style_preset('warning')
    final_instructions.set_font_size(11)
    final_instructions.resize(300, 40)
    final_instructions.set_word_wrap(True)
    drop_zone.add_widget(final_instructions, QPoint(50, 520))
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Application lancée: {len(buttons)} boutons créés")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)