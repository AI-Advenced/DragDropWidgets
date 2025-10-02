#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration des options de formatage de texte

Ce fichier démontre :
- Différents presets de style pour labels
- Options de formatage de police
- Couleurs et alignements
- Tailles de police dynamiques

Exécution :
    python text_formatting.py
"""

import sys
from PySide6.QtCore import QPoint
from dragdropwidgets import create_app, DraggableLabel, DraggableButton


def main():
    """Fonction principale pour démontrer le formatage de texte"""
    app, window, drop_zone = create_app("Formatage de Texte - DragDropWidgets", (1000, 800))
    
    print("📝 Démonstration du formatage de texte")
    print("=" * 60)
    print("Presets disponibles:")
    print("• title     - Titre principal (grand, gras)")
    print("• subtitle  - Sous-titre (moyen, gras)")
    print("• body      - Texte normal")
    print("• caption   - Légende (petit)")
    print("• error     - Message d'erreur (rouge)")
    print("• success   - Message de succès (vert)")
    print("• warning   - Avertissement (orange)")
    print("• info      - Information (bleu)")
    print("=" * 60)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 20
    
    # Titre principal de la démonstration
    main_title = DraggableLabel("Galerie de Formatage de Texte")
    main_title.set_style_preset('title')
    main_title.set_font_size(24)
    drop_zone.add_widget(main_title, QPoint(50, 30))
    
    # Section 1: Presets de style
    section1_title = DraggableLabel("1. Presets de Style")
    section1_title.set_style_preset('subtitle')
    section1_title.set_font_size(18)
    drop_zone.add_widget(section1_title, QPoint(50, 100))
    
    # Démonstration des différents presets
    presets_demo = [
        ("Titre Principal", "title", "Utilisé pour les en-têtes principaux"),
        ("Sous-titre Important", "subtitle", "Pour les sections importantes"),
        ("Texte de Corps Normal", "body", "Texte standard de l'application"),
        ("Légende ou Note", "caption", "Informations secondaires"),
        ("Message d'Erreur", "error", "Signaler une erreur à l'utilisateur"),
        ("Message de Succès", "success", "Confirmer une action réussie"),
        ("Avertissement Important", "warning", "Attirer l'attention sur un point"),
        ("Information Utile", "info", "Fournir des informations contextuelles")
    ]
    
    for i, (text, preset, description) in enumerate(presets_demo):
        # Label principal avec le preset
        label = DraggableLabel(text)
        label.set_style_preset(preset)
        label.set_snap_to_grid(True, 20)
        
        # Description du preset
        desc = DraggableLabel(f"({preset}) - {description}")
        desc.set_font_size(10)
        desc.set_color("#666666")
        desc.set_snap_to_grid(True, 20)
        
        # Placement
        y_pos = 140 + i * 50
        drop_zone.add_widget(label, QPoint(70, y_pos))
        drop_zone.add_widget(desc, QPoint(320, y_pos + 5))
    
    # Section 2: Options de police
    section2_title = DraggableLabel("2. Options de Police")
    section2_title.set_style_preset('subtitle')
    section2_title.set_font_size(18)
    drop_zone.add_widget(section2_title, QPoint(600, 100))
    
    # Démonstration des tailles de police
    font_sizes = [10, 12, 14, 16, 18, 20, 24, 28]
    for i, size in enumerate(font_sizes):
        size_label = DraggableLabel(f"Taille {size}px")
        size_label.set_font_size(size)
        size_label.set_snap_to_grid(True, 20)
        drop_zone.add_widget(size_label, QPoint(620, 140 + i * 35))
    
    # Démonstration des styles de police
    font_styles = [
        ("Texte Normal", False, False),
        ("Texte Gras", True, False),
        ("Texte Italique", False, True),
        ("Gras et Italique", True, True)
    ]
    
    for i, (text, bold, italic) in enumerate(font_styles):
        style_label = DraggableLabel(text)
        style_label.set_font_bold(bold)
        style_label.set_font_italic(italic)
        style_label.set_font_size(14)
        style_label.set_snap_to_grid(True, 20)
        drop_zone.add_widget(style_label, QPoint(620, 420 + i * 30))
    
    # Section 3: Alignements
    section3_title = DraggableLabel("3. Alignements de Texte")
    section3_title.set_style_preset('subtitle')
    section3_title.set_font_size(18)
    drop_zone.add_widget(section3_title, QPoint(50, 580))
    
    # Démonstration des alignements
    alignments = [
        ("Texte Aligné à Gauche", "left"),
        ("Texte Centré", "center"),
        ("Texte Aligné à Droite", "right")
    ]
    
    for i, (text, alignment) in enumerate(alignments):
        align_label = DraggableLabel(text)
        align_label.set_alignment(alignment)
        align_label.set_font_size(14)
        align_label.resize(200, 30)
        align_label.set_background_color("#f0f0f0")
        align_label.set_snap_to_grid(True, 20)
        drop_zone.add_widget(align_label, QPoint(70 + i * 220, 620))
    
    # Section interactive: Contrôles de formatage
    interactive_title = DraggableLabel("4. Contrôles Interactifs")
    interactive_title.set_style_preset('subtitle')
    interactive_title.set_font_size(18)
    drop_zone.add_widget(interactive_title, QPoint(600, 580))
    
    # Label de démonstration modifiable
    demo_label = DraggableLabel("Texte Modifiable")
    demo_label.set_font_size(16)
    demo_label.resize(200, 50)
    demo_label.set_background_color("#ffffff")
    demo_label.set_alignment('center')
    drop_zone.add_widget(demo_label, QPoint(650, 620))
    
    # Boutons de contrôle pour modifier le label
    controls = [
        ("Plus Grand", lambda: increase_font_size()),
        ("Plus Petit", lambda: decrease_font_size()),
        ("Gras", lambda: toggle_bold()),
        ("Italique", lambda: toggle_italic()),
        ("Couleur Rouge", lambda: demo_label.set_color("#ff0000")),
        ("Couleur Bleue", lambda: demo_label.set_color("#0000ff")),
        ("Couleur Noire", lambda: demo_label.set_color("#000000")),
        ("Fond Jaune", lambda: demo_label.set_background_color("#ffff99")),
        ("Fond Blanc", lambda: demo_label.set_background_color("#ffffff")),
        ("Réinitialiser", lambda: reset_demo_label())
    ]
    
    # État du label de démonstration
    demo_state = {
        'font_size': 16,
        'is_bold': False,
        'is_italic': False
    }
    
    # Fonctions de contrôle
    def increase_font_size():
        if demo_state['font_size'] < 32:
            demo_state['font_size'] += 2
            demo_label.set_font_size(demo_state['font_size'])
            print(f"📏 Taille augmentée: {demo_state['font_size']}px")
    
    def decrease_font_size():
        if demo_state['font_size'] > 8:
            demo_state['font_size'] -= 2
            demo_label.set_font_size(demo_state['font_size'])
            print(f"📏 Taille diminuée: {demo_state['font_size']}px")
    
    def toggle_bold():
        demo_state['is_bold'] = not demo_state['is_bold']
        demo_label.set_font_bold(demo_state['is_bold'])
        print(f"🔤 Gras: {'Activé' if demo_state['is_bold'] else 'Désactivé'}")
    
    def toggle_italic():
        demo_state['is_italic'] = not demo_state['is_italic']
        demo_label.set_font_italic(demo_state['is_italic'])
        print(f"🔤 Italique: {'Activé' if demo_state['is_italic'] else 'Désactivé'}")
    
    def reset_demo_label():
        demo_state.update({'font_size': 16, 'is_bold': False, 'is_italic': False})
        demo_label.set_font_size(16)
        demo_label.set_font_bold(False)
        demo_label.set_font_italic(False)
        demo_label.set_color("#000000")
        demo_label.set_background_color("#ffffff")
        demo_label.set_text("Texte Modifiable")
        print("🔄 Label de démonstration réinitialisé")
    
    # Créer les boutons de contrôle
    for i, (label_text, action) in enumerate(controls):
        control_btn = DraggableButton(label_text)
        control_btn.set_style('info')
        control_btn.button_clicked.connect(lambda _, a=action: a())
        
        # Arrangement en grille 2x5
        col = i % 2
        row = i // 2
        x_pos = 600 + col * 120
        y_pos = 680 + row * 35
        
        drop_zone.add_widget(control_btn, QPoint(x_pos, y_pos))
    
    # Message d'instruction
    instruction = DraggableLabel(
        "💡 Utilisez les boutons ci-dessus pour modifier le texte de démonstration.\n"
        "Tous les widgets peuvent être déplacés par glisser-déposer!"
    )
    instruction.set_style_preset('info')
    instruction.set_font_size(11)
    instruction.resize(400, 50)
    instruction.set_word_wrap(True)
    drop_zone.add_widget(instruction, QPoint(50, 720))
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Application lancée avec {len(presets_demo)} presets de démonstration")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)