#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sélecteur de thèmes dynamique

Ce fichier démontre :
- Système de thèmes intégré
- Changement de thème en temps réel
- Création de thèmes personnalisés
- Prévisualisation des thèmes
- Sauvegarde des préférences

Exécution :
    python theme_switcher.py
"""

import sys
import json
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QColorDialog, QInputDialog, QMessageBox
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.utils.themes import ThemeManager


def main():
    """Fonction principale pour démontrer le système de thèmes"""
    app, window, drop_zone = create_app("Sélecteur de Thèmes - DragDropWidgets", (1200, 900))
    
    print("🎨 Démonstration du système de thèmes")
    print("=" * 60)
    print("Thèmes disponibles:")
    
    # Initialiser le gestionnaire de thèmes
    theme_manager = ThemeManager()
    available_themes = theme_manager.get_available_themes()
    
    for theme_id, theme_name in available_themes.items():
        print(f"• {theme_id}: {theme_name}")
    print("=" * 60)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre principal
    title = DraggableLabel("Galerie de Thèmes DragDropWidgets")
    title.set_style_preset('title')
    title.set_font_size(24)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section 1: Thèmes prédéfinis
    predefined_title = DraggableLabel("1. Thèmes Prédéfinis")
    predefined_title.set_style_preset('subtitle')
    predefined_title.set_font_size(18)
    drop_zone.add_widget(predefined_title, QPoint(50, 100))
    
    # Créer des boutons pour chaque thème prédéfini
    theme_buttons = []
    theme_descriptions = {
        'light': 'Interface claire et moderne avec accents bleus',
        'dark': 'Mode sombre élégant avec accents bleu clair',
        'blue': 'Thème professionnel en nuances de bleu',
        'green': 'Thème nature avec couleurs vertes apaisantes',
        'high_contrast': 'Contraste élevé pour l\'accessibilité'
    }
    
    current_theme_label = DraggableLabel("Thème Actuel: light")
    current_theme_label.set_style_preset('info')
    current_theme_label.set_font_size(14)
    current_theme_label.set_font_bold(True)
    drop_zone.add_widget(current_theme_label, QPoint(50, 140))
    
    y_offset = 180
    for i, (theme_id, theme_name) in enumerate(available_themes.items()):
        # Bouton du thème
        theme_btn = DraggableButton(theme_name)
        theme_btn.set_style('primary')
        theme_btn.set_snap_to_grid(True, 25)
        drop_zone.add_widget(theme_btn, QPoint(70, y_offset + i * 60))
        
        # Description du thème
        description = theme_descriptions.get(theme_id, 'Thème personnalisé')
        desc_label = DraggableLabel(description)
        desc_label.set_font_size(11)
        desc_label.set_color('#666666')
        drop_zone.add_widget(desc_label, QPoint(220, y_offset + i * 60 + 5))
        
        # Bouton de prévisualisation
        preview_btn = DraggableButton("Aperçu")
        preview_btn.set_style('info')
        preview_btn.resize(80, 30)
        drop_zone.add_widget(preview_btn, QPoint(500, y_offset + i * 60))
        
        theme_buttons.append((theme_btn, preview_btn, theme_id, theme_name))
    
    # Section 2: Widgets de démonstration
    demo_title = DraggableLabel("2. Widgets de Démonstration")
    demo_title.set_style_preset('subtitle')
    demo_title.set_font_size(18)
    drop_zone.add_widget(demo_title, QPoint(650, 100))
    
    # Collection de widgets pour montrer l'effet des thèmes
    demo_widgets = []
    
    # Boutons de démonstration avec différents styles
    demo_button_styles = ['primary', 'success', 'danger', 'warning', 'info', 'secondary']
    for i, style in enumerate(demo_button_styles):
        demo_btn = DraggableButton(f"Bouton {style.title()}")
        demo_btn.set_style(style)
        demo_btn.set_snap_to_grid(True, 25)
        drop_zone.add_widget(demo_btn, QPoint(670, 140 + i * 45))
        demo_widgets.append(demo_btn)
    
    # Labels de démonstration avec différents presets
    demo_label_presets = ['title', 'subtitle', 'body', 'caption', 'error', 'success', 'warning', 'info']
    for i, preset in enumerate(demo_label_presets):
        demo_label = DraggableLabel(f"Label {preset.title()}")
        demo_label.set_style_preset(preset)
        demo_label.set_snap_to_grid(True, 25)
        drop_zone.add_widget(demo_label, QPoint(850, 140 + i * 35))
        demo_widgets.append(demo_label)
    
    # Section 3: Création de thème personnalisé
    custom_title = DraggableLabel("3. Créateur de Thème Personnalisé")
    custom_title.set_style_preset('subtitle')
    custom_title.set_font_size(18)
    drop_zone.add_widget(custom_title, QPoint(50, 480))
    
    # Interface de création de thème
    create_theme_btn = DraggableButton("Nouveau Thème")
    create_theme_btn.set_style('success')
    drop_zone.add_widget(create_theme_btn, QPoint(70, 520))
    
    # Sélecteurs de couleurs
    color_selectors = [
        ("Couleur Principale", "primary_color", "#0078d4"),
        ("Couleur d'Arrière-plan", "background_color", "#ffffff"),
        ("Couleur de Texte", "text_color", "#000000"),
        ("Couleur d'Accent", "accent_color", "#106ebe")
    ]
    
    color_values = {}
    color_buttons = {}
    
    for i, (name, key, default_color) in enumerate(color_selectors):
        color_values[key] = default_color
        
        # Label du sélecteur
        selector_label = DraggableLabel(f"{name}:")
        selector_label.set_font_size(11)
        drop_zone.add_widget(selector_label, QPoint(70, 570 + i * 40))
        
        # Bouton de couleur
        color_btn = DraggableButton("■")
        color_btn.set_style('secondary')
        color_btn.resize(40, 30)
        drop_zone.add_widget(color_btn, QPoint(220, 565 + i * 40))
        color_buttons[key] = color_btn
        
        # Label de la valeur hexadécimale
        hex_label = DraggableLabel(default_color)
        hex_label.set_font_size(10)
        hex_label.set_font_family('monospace')
        drop_zone.add_widget(hex_label, QPoint(280, 572 + i * 40))
        color_buttons[f"{key}_hex"] = hex_label
    
    # Boutons d'action pour thème personnalisé
    save_custom_btn = DraggableButton("Sauvegarder Thème")
    save_custom_btn.set_style('primary')
    drop_zone.add_widget(save_custom_btn, QPoint(400, 520))
    
    apply_custom_btn = DraggableButton("Appliquer Aperçu")
    apply_custom_btn.set_style('info')
    drop_zone.add_widget(apply_custom_btn, QPoint(400, 570))
    
    # Section 4: Gestion des thèmes
    management_title = DraggableLabel("4. Gestion des Thèmes")
    management_title.set_style_preset('subtitle')
    management_title.set_font_size(18)
    drop_zone.add_widget(management_title, QPoint(650, 480))
    
    # Liste des thèmes personnalisés
    custom_themes_label = DraggableLabel("Thèmes Personnalisés:")
    custom_themes_label.set_font_size(12)
    custom_themes_label.set_font_bold(True)
    drop_zone.add_widget(custom_themes_label, QPoint(670, 520))
    
    custom_themes_list = DraggableLabel("Aucun thème personnalisé")
    custom_themes_list.set_font_size(11)
    custom_themes_list.resize(300, 80)
    custom_themes_list.set_background_color("#f8f9fa")
    custom_themes_list.set_word_wrap(True)
    drop_zone.add_widget(custom_themes_list, QPoint(670, 550))
    
    # Boutons de gestion
    export_btn = DraggableButton("Exporter Thème")
    export_btn.set_style('secondary')
    drop_zone.add_widget(export_btn, QPoint(670, 650))
    
    import_btn = DraggableButton("Importer Thème")
    import_btn.set_style('secondary')
    drop_zone.add_widget(import_btn, QPoint(800, 650))
    
    reset_btn = DraggableButton("Thème par Défaut")
    reset_btn.set_style('warning')
    drop_zone.add_widget(reset_btn, QPoint(930, 650))
    
    # Section 5: Informations et statistiques
    info_title = DraggableLabel("5. Informations")
    info_title.set_style_preset('subtitle')
    info_title.set_font_size(18)
    drop_zone.add_widget(info_title, QPoint(50, 720))
    
    # Statistiques du système de thèmes
    stats_text = f"""📊 Statistiques des Thèmes:
• Thèmes prédéfinis: {len(available_themes)}
• Thème actuel: light
• Dernière modification: Jamais
• Thèmes personnalisés: 0"""
    
    stats_display = DraggableLabel(stats_text)
    stats_display.set_font_size(11)
    stats_display.resize(300, 100)
    stats_display.set_background_color("#f0f8ff")
    stats_display.set_word_wrap(True)
    drop_zone.add_widget(stats_display, QPoint(70, 760))
    
    # État du système
    system_state = {
        'current_theme': 'light',
        'custom_themes': [],
        'last_preview': None
    }
    
    # Fonctions utilitaires
    def update_stats_display():
        """Mettre à jour l'affichage des statistiques"""
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        
        stats_text = f"""📊 Statistiques des Thèmes:
• Thèmes prédéfinis: {len(available_themes)}
• Thème actuel: {system_state['current_theme']}
• Dernière modification: {now}
• Thèmes personnalisés: {len(system_state['custom_themes'])}"""
        
        stats_display.set_text(stats_text)
    
    def update_custom_themes_list():
        """Mettre à jour la liste des thèmes personnalisés"""
        if not system_state['custom_themes']:
            custom_themes_list.set_text("Aucun thème personnalisé")
        else:
            themes_text = "Thèmes disponibles:\n"
            for theme_name in system_state['custom_themes']:
                themes_text += f"• {theme_name}\n"
            custom_themes_list.set_text(themes_text)
    
    # Gestionnaires d'événements
    def apply_theme(theme_id, theme_name):
        """Appliquer un thème"""
        success = theme_manager.apply_theme_to_app(theme_id)
        if success:
            system_state['current_theme'] = theme_id
            current_theme_label.set_text(f"Thème Actuel: {theme_name}")
            update_stats_display()
            print(f"🎨 Thème appliqué: {theme_name} ({theme_id})")
        else:
            print(f"❌ Erreur lors de l'application du thème: {theme_id}")
    
    def preview_theme(theme_id, theme_name):
        """Prévisualiser un thème"""
        # Pour la démonstration, on applique temporairement le thème
        preview_colors = theme_manager.get_theme_preview_colors(theme_id)
        if preview_colors:
            print(f"👁️ Aperçu du thème: {theme_name}")
            print(f"   Couleurs: {preview_colors}")
            # Dans un vrai système, on appliquerait juste aux widgets de démo
            apply_theme(theme_id, theme_name)
            system_state['last_preview'] = theme_id
        else:
            print(f"❌ Impossible de prévisualiser le thème: {theme_id}")
    
    def choose_color(color_key):
        """Ouvrir le sélecteur de couleurs"""
        current_color = color_values.get(color_key, "#000000")
        color = QColorDialog.getColor()
        
        if color.isValid():
            hex_color = color.name()
            color_values[color_key] = hex_color
            
            # Mettre à jour l'affichage
            color_buttons[f"{color_key}_hex"].set_text(hex_color)
            
            print(f"🎨 Couleur sélectionnée pour {color_key}: {hex_color}")
    
    def create_custom_theme():
        """Créer un nouveau thème personnalisé"""
        theme_name, ok = QInputDialog.getText(
            window, 'Nouveau Thème', 
            'Nom du thème personnalisé:'
        )
        
        if ok and theme_name:
            # Créer les données du thème
            custom_colors = {
                'background': color_values['background_color'],
                'foreground': color_values['text_color'],
                'accent': color_values['primary_color'],
                'border': '#cccccc',
                'hover': color_values['accent_color'],
                'selection': f"{color_values['primary_color']}33"  # Avec transparence
            }
            
            custom_fonts = {
                'default_size': 14,
                'title_size': 18,
                'small_size': 12,
                'family': 'Segoe UI, Arial, sans-serif'
            }
            
            # Créer le thème
            theme_manager.create_custom_theme(
                theme_name.lower().replace(' ', '_'),
                theme_name,
                custom_colors,
                custom_fonts,
                description=f'Thème personnalisé créé par l\'utilisateur'
            )
            
            system_state['custom_themes'].append(theme_name)
            update_custom_themes_list()
            update_stats_display()
            
            QMessageBox.information(window, "Succès", f"Thème '{theme_name}' créé avec succès!")
            print(f"✅ Thème personnalisé créé: {theme_name}")
    
    def apply_custom_preview():
        """Appliquer un aperçu du thème personnalisé"""
        # Créer un thème temporaire pour l'aperçu
        temp_colors = {
            'background': color_values['background_color'],
            'foreground': color_values['text_color'],
            'accent': color_values['primary_color'],
            'border': '#cccccc',
            'hover': color_values['accent_color']
        }
        
        print(f"👁️ Aperçu du thème personnalisé avec les couleurs: {temp_colors}")
        # Dans un vrai système, on créerait et appliquerait le thème temporaire
    
    def export_current_theme():
        """Exporter le thème actuel"""
        current_theme_data = theme_manager.get_theme(system_state['current_theme'])
        if current_theme_data:
            # Simuler l'export (dans un vrai système, on ouvrirait un dialog de sauvegarde)
            filename = f"theme_{system_state['current_theme']}.json"
            print(f"📤 Thème exporté vers: {filename}")
            QMessageBox.information(window, "Export", f"Thème exporté vers {filename}")
        else:
            QMessageBox.warning(window, "Erreur", "Impossible d'exporter le thème actuel")
    
    def import_theme_file():
        """Importer un thème depuis un fichier"""
        # Simuler l'import (dans un vrai système, on ouvrirait un dialog de fichier)
        QMessageBox.information(window, "Import", "Fonctionnalité d'import disponible dans la version complète")
        print("📥 Import de thème demandé")
    
    def reset_to_default():
        """Réinitialiser au thème par défaut"""
        apply_theme('light', 'Light Theme')
        QMessageBox.information(window, "Reset", "Thème réinitialisé par défaut")
    
    # Connexion des événements
    
    # Boutons de thèmes prédéfinis
    for theme_btn, preview_btn, theme_id, theme_name in theme_buttons:
        theme_btn.button_clicked.connect(
            lambda _, tid=theme_id, tname=theme_name: apply_theme(tid, tname)
        )
        preview_btn.button_clicked.connect(
            lambda _, tid=theme_id, tname=theme_name: preview_theme(tid, tname)
        )
    
    # Sélecteurs de couleurs
    for key in color_values.keys():
        color_buttons[key].button_clicked.connect(
            lambda _, ck=key: choose_color(ck)
        )
    
    # Boutons de création de thème
    create_theme_btn.button_clicked.connect(lambda _: create_custom_theme())
    apply_custom_btn.button_clicked.connect(lambda _: apply_custom_preview())
    save_custom_btn.button_clicked.connect(lambda _: create_custom_theme())
    
    # Boutons de gestion
    export_btn.button_clicked.connect(lambda _: export_current_theme())
    import_btn.button_clicked.connect(lambda _: import_theme_file())
    reset_btn.button_clicked.connect(lambda _: reset_to_default())
    
    # Instructions
    instructions = DraggableLabel(
        "🎨 Sélecteur de Thèmes Complet:\n"
        "• Cliquez sur les thèmes prédéfinis pour les appliquer\n"
        "• Utilisez 'Aperçu' pour tester avant d'appliquer\n"
        "• Créez vos propres thèmes avec le sélecteur de couleurs\n"
        "• Exportez/importez vos thèmes favoris\n"
        "• Observez l'effet sur tous les widgets de démonstration"
    )
    instructions.set_style_preset('info')
    instructions.set_font_size(11)
    instructions.resize(400, 100)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(650, 760))
    
    # Initialiser l'affichage
    update_stats_display()
    update_custom_themes_list()
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Sélecteur de thèmes lancé avec {len(available_themes)} thèmes prédéfinis")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)