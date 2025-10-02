#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sélecteur de couleurs interactif

Ce fichier démontre :
- Jeu de couleurs interactif
- Sélecteur de couleurs avancé
- Palette de couleurs prédéfinies
- Générateur de couleurs aléatoires
- Harmonie de couleurs

Exécution :
    python color_picker.py
"""

import sys
import random
import colorsys
from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QColorDialog, QMessageBox
from dragdropwidgets import create_app, DraggableButton, DraggableLabel


def main():
    """Sélecteur de couleurs interactif principal"""
    app, window, drop_zone = create_app("Jeu de Couleurs Interactif", (1200, 900))
    
    print("🎨 Jeu de couleurs interactif")
    print("=" * 50)
    
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre
    title = DraggableLabel("🎨 Studio de Couleurs Interactif")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Widget de démonstration principal
    demo_widget = DraggableLabel("Texte Coloré de Démonstration")
    demo_widget.resize(300, 100)
    demo_widget.set_style_preset('title')
    demo_widget.set_font_size(18)
    demo_widget.set_alignment('center')
    demo_widget.set_background_color('#ffffff')
    demo_widget.set_color('#000000')
    drop_zone.add_widget(demo_widget, QPoint(400, 100))
    
    # État des couleurs
    color_state = {
        'current_text_color': '#000000',
        'current_bg_color': '#ffffff',
        'color_history': [],
        'game_mode': False,
        'target_color': None,
        'score': 0,
        'attempts': 0
    }
    
    # Section palette prédéfinie
    palette_title = DraggableLabel("🎨 Palettes de Couleurs")
    palette_title.set_style_preset('subtitle')
    palette_title.set_font_size(16)
    drop_zone.add_widget(palette_title, QPoint(50, 80))
    
    # Couleurs prédéfinies
    predefined_colors = [
        ("Rouge", "#ff0000"),
        ("Vert", "#00ff00"),
        ("Bleu", "#0000ff"),
        ("Jaune", "#ffff00"),
        ("Violet", "#ff00ff"),
        ("Cyan", "#00ffff"),
        ("Orange", "#ff8000"),
        ("Rose", "#ff80c0"),
        ("Lime", "#80ff00"),
        ("Indigo", "#4000ff"),
        ("Turquoise", "#00ff80"),
        ("Corail", "#ff4080")
    ]
    
    color_buttons = []
    for i, (name, color) in enumerate(predefined_colors):
        col = i % 4
        row = i // 4
        x_pos = 70 + col * 80
        y_pos = 120 + row * 40
        
        color_btn = DraggableButton("■")
        color_btn.resize(70, 30)
        color_btn.setStyleSheet(f"""
            DraggableButton {{
                background-color: {color};
                color: white;
                border: 2px solid #333;
                font-size: 16px;
                font-weight: bold;
            }}
            DraggableButton:hover {{
                border: 3px solid #fff;
            }}
        """)
        
        drop_zone.add_widget(color_btn, QPoint(x_pos, y_pos))
        
        # Connecter l'événement
        color_btn.button_clicked.connect(
            lambda _, c=color, n=name: apply_color_to_demo(c, 'text', n)
        )
        color_buttons.append((color_btn, color, name))
        
        # Label du nom de couleur
        name_label = DraggableLabel(name)
        name_label.set_font_size(9)
        name_label.set_alignment('center')
        drop_zone.add_widget(name_label, QPoint(x_pos, y_pos + 32))
    
    # Section contrôles avancés
    controls_title = DraggableLabel("🛠️ Contrôles Avancés")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(50, 280))
    
    # Boutons de contrôle
    custom_color_btn = DraggableButton("🎨 Couleur Personnalisée")
    custom_color_btn.set_style('primary')
    drop_zone.add_widget(custom_color_btn, QPoint(70, 320))
    
    random_color_btn = DraggableButton("🎲 Couleur Aléatoire")
    random_color_btn.set_style('info')
    drop_zone.add_widget(random_color_btn, QPoint(250, 320))
    
    bg_color_btn = DraggableButton("🖼️ Couleur de Fond")
    bg_color_btn.set_style('secondary')
    drop_zone.add_widget(bg_color_btn, QPoint(70, 360))
    
    gradient_btn = DraggableButton("🌈 Dégradé")
    gradient_btn.set_style('warning')
    drop_zone.add_widget(gradient_btn, QPoint(250, 360))
    
    # Générateurs d'harmonie
    harmony_title = DraggableLabel("🎼 Harmonies de Couleurs")
    harmony_title.set_style_preset('subtitle')
    harmony_title.set_font_size(16)
    drop_zone.add_widget(harmony_title, QPoint(50, 410))
    
    complementary_btn = DraggableButton("Complémentaire")
    complementary_btn.set_style('info')
    drop_zone.add_widget(complementary_btn, QPoint(70, 450))
    
    triadic_btn = DraggableButton("Triadique")
    triadic_btn.set_style('info')
    drop_zone.add_widget(triadic_btn, QPoint(190, 450))
    
    analogous_btn = DraggableButton("Analogue")
    analogous_btn.set_style('info')
    drop_zone.add_widget(analogous_btn, QPoint(290, 450))
    
    # Zone d'harmonies générées
    harmony_display = DraggableLabel("Cliquez sur un bouton d'harmonie pour générer des couleurs")
    harmony_display.resize(350, 60)
    harmony_display.set_background_color('#f8f9fa')
    harmony_display.set_word_wrap(True)
    drop_zone.add_widget(harmony_display, QPoint(70, 490))
    
    # Section jeu de couleurs
    game_title = DraggableLabel("🎮 Jeu: Devinez la Couleur!")
    game_title.set_style_preset('subtitle')
    game_title.set_font_size(16)
    drop_zone.add_widget(game_title, QPoint(50, 570))
    
    start_game_btn = DraggableButton("🎯 Commencer le Jeu")
    start_game_btn.set_style('success')
    drop_zone.add_widget(start_game_btn, QPoint(70, 610))
    
    game_info = DraggableLabel("Score: 0 | Essais: 0")
    game_info.set_font_size(12)
    game_info.set_font_bold(True)
    drop_zone.add_widget(game_info, QPoint(250, 615))
    
    # Zone de couleur cible pour le jeu
    target_display = DraggableLabel("Cible")
    target_display.resize(100, 60)
    target_display.set_alignment('center')
    target_display.set_background_color('#cccccc')
    target_display.hide()  # Caché par défaut
    drop_zone.add_widget(target_display, QPoint(70, 650))
    
    # Informations sur la couleur actuelle
    color_info_title = DraggableLabel("ℹ️ Informations Couleur")
    color_info_title.set_style_preset('subtitle')
    color_info_title.set_font_size(16)
    drop_zone.add_widget(color_info_title, QPoint(800, 80))
    
    color_info_display = DraggableLabel("Couleur: #000000\nRGB: (0, 0, 0)\nHSL: (0°, 0%, 0%)")
    color_info_display.resize(300, 100)
    color_info_display.set_background_color('#f0f8ff')
    color_info_display.set_font_size(11)
    drop_zone.add_widget(color_info_display, QPoint(820, 120))
    
    # Historique des couleurs
    history_title = DraggableLabel("📜 Historique")
    history_title.set_style_preset('subtitle')
    history_title.set_font_size(16)
    drop_zone.add_widget(history_title, QPoint(800, 240))
    
    history_display = DraggableLabel("Aucune couleur dans l'historique")
    history_display.resize(300, 150)
    history_display.set_background_color('#f8f8f8')
    history_display.set_font_size(10)
    history_display.set_word_wrap(True)
    drop_zone.add_widget(history_display, QPoint(820, 280))
    
    clear_history_btn = DraggableButton("Effacer Historique")
    clear_history_btn.set_style('secondary')
    drop_zone.add_widget(clear_history_btn, QPoint(820, 440))
    
    # Fonctions utilitaires
    def hex_to_rgb(hex_color):
        """Convertir hex en RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hsl(r, g, b):
        """Convertir RGB en HSL"""
        r, g, b = r/255.0, g/255.0, b/255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return int(h*360), int(s*100), int(l*100)
    
    def hsl_to_rgb(h, s, l):
        """Convertir HSL en RGB"""
        h, s, l = h/360.0, s/100.0, l/100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r*255), int(g*255), int(b*255)
    
    def rgb_to_hex(r, g, b):
        """Convertir RGB en hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def update_color_info(hex_color):
        """Mettre à jour les informations de couleur"""
        r, g, b = hex_to_rgb(hex_color)
        h, s, l = rgb_to_hsl(r, g, b)
        
        info_text = f"""Couleur: {hex_color.upper()}
RGB: ({r}, {g}, {b})
HSL: ({h}°, {s}%, {l}%)
Luminosité: {'Claire' if l > 50 else 'Sombre'}
Saturation: {'Vive' if s > 70 else 'Terne' if s < 30 else 'Modérée'}"""
        
        color_info_display.set_text(info_text)
    
    def add_to_history(color, name=""):
        """Ajouter une couleur à l'historique"""
        timestamp = QTimer()
        entry = f"{color} {name}".strip()
        
        if entry not in color_state['color_history']:
            color_state['color_history'].insert(0, entry)
            color_state['color_history'] = color_state['color_history'][:10]  # Max 10
            
            update_history_display()
    
    def update_history_display():
        """Mettre à jour l'affichage de l'historique"""
        if not color_state['color_history']:
            history_display.set_text("Aucune couleur dans l'historique")
            return
        
        history_text = "Couleurs récentes:\n\n"
        for i, entry in enumerate(color_state['color_history'][:8], 1):
            history_text += f"{i}. {entry}\n"
        
        history_display.set_text(history_text)
    
    def apply_color_to_demo(color, target='text', name=""):
        """Appliquer une couleur au widget de démonstration"""
        if target == 'text':
            demo_widget.set_color(color)
            color_state['current_text_color'] = color
        elif target == 'background':
            demo_widget.set_background_color(color)
            color_state['current_bg_color'] = color
        
        update_color_info(color)
        add_to_history(color, name)
        
        # Vérifier si c'est pour le jeu
        if color_state['game_mode'] and color_state['target_color']:
            check_color_match(color)
        
        print(f"🎨 Couleur appliquée: {color} ({name}) -> {target}")
    
    def choose_custom_color():
        """Ouvrir le sélecteur de couleurs personnalisé"""
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            apply_color_to_demo(hex_color, 'text', 'Personnalisée')
    
    def generate_random_color():
        """Générer une couleur aléatoire"""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        hex_color = rgb_to_hex(r, g, b)
        apply_color_to_demo(hex_color, 'text', 'Aléatoire')
    
    def generate_gradient():
        """Générer un effet de dégradé simulé"""
        # Créer plusieurs nuances de la couleur actuelle
        base_color = hex_to_rgb(color_state['current_text_color'])
        
        for i, widget in enumerate([demo_widget]):  # On pourrait avoir plusieurs widgets
            factor = 0.3 + (i * 0.2)  # Variation de luminosité
            new_r = min(255, int(base_color[0] * factor))
            new_g = min(255, int(base_color[1] * factor))
            new_b = min(255, int(base_color[2] * factor))
            
            gradient_color = rgb_to_hex(new_r, new_g, new_b)
            widget.set_background_color(gradient_color)
        
        add_to_history(gradient_color, 'Dégradé')
        print("🌈 Dégradé appliqué")
    
    def generate_complementary():
        """Générer la couleur complémentaire"""
        r, g, b = hex_to_rgb(color_state['current_text_color'])
        comp_r, comp_g, comp_b = 255-r, 255-g, 255-b
        comp_color = rgb_to_hex(comp_r, comp_g, comp_b)
        
        harmony_display.set_text(f"Couleur complémentaire: {comp_color}")
        harmony_display.setStyleSheet(f"background-color: {comp_color}; color: white;")
        
        # Appliquer automatiquement
        apply_color_to_demo(comp_color, 'background', 'Complémentaire')
    
    def generate_triadic():
        """Générer une harmonie triadique"""
        r, g, b = hex_to_rgb(color_state['current_text_color'])
        h, s, l = rgb_to_hsl(r, g, b)
        
        # Couleurs à +120° et +240°
        h2 = (h + 120) % 360
        h3 = (h + 240) % 360
        
        r2, g2, b2 = hsl_to_rgb(h2, s, l)
        r3, g3, b3 = hsl_to_rgb(h3, s, l)
        
        color2 = rgb_to_hex(r2, g2, b2)
        color3 = rgb_to_hex(r3, g3, b3)
        
        harmony_display.set_text(f"Triade: {color2}, {color3}")
        
        # Appliquer la deuxième couleur
        apply_color_to_demo(color2, 'background', 'Triadique')
    
    def generate_analogous():
        """Générer une harmonie analogue"""
        r, g, b = hex_to_rgb(color_state['current_text_color'])
        h, s, l = rgb_to_hsl(r, g, b)
        
        # Couleurs à +30° et -30°
        h2 = (h + 30) % 360
        h3 = (h - 30) % 360
        
        r2, g2, b2 = hsl_to_rgb(h2, s, l)
        r3, g3, b3 = hsl_to_rgb(h3, s, l)
        
        color2 = rgb_to_hex(r2, g2, b2)
        color3 = rgb_to_hex(r3, g3, b3)
        
        harmony_display.set_text(f"Analogues: {color2}, {color3}")
        
        # Appliquer la deuxième couleur
        apply_color_to_demo(color2, 'background', 'Analogue')
    
    # Jeu de couleurs
    def start_color_game():
        """Démarrer le jeu de devinette de couleurs"""
        color_state['game_mode'] = True
        color_state['score'] = 0
        color_state['attempts'] = 0
        
        generate_target_color()
        target_display.show()
        
        start_game_btn.set_text("🎯 Nouvelle Cible")
        QMessageBox.information(window, "Jeu Démarré!", 
                              "Regardez la couleur cible et essayez de la reproduire en cliquant sur les couleurs!")
    
    def generate_target_color():
        """Générer une nouvelle couleur cible"""
        target_colors = [color for _, color in predefined_colors]
        color_state['target_color'] = random.choice(target_colors)
        
        target_display.setStyleSheet(f"background-color: {color_state['target_color']};")
        target_display.set_text("Cible\nà reproduire")
    
    def check_color_match(selected_color):
        """Vérifier si la couleur sélectionnée correspond à la cible"""
        color_state['attempts'] += 1
        
        if selected_color.lower() == color_state['target_color'].lower():
            color_state['score'] += 10
            QMessageBox.information(window, "🎉 Bravo!", 
                                  f"Couleur correcte! +10 points\nScore: {color_state['score']}")
            generate_target_color()  # Nouvelle cible
        else:
            # Donner un indice sur la proximité
            target_rgb = hex_to_rgb(color_state['target_color'])
            selected_rgb = hex_to_rgb(selected_color)
            
            distance = sum(abs(a - b) for a, b in zip(target_rgb, selected_rgb))
            if distance < 100:
                hint = "Très proche!"
            elif distance < 200:
                hint = "Assez proche"
            else:
                hint = "Assez loin"
            
            QMessageBox.information(window, "Pas tout à fait", 
                                  f"Ce n'est pas la bonne couleur.\nIndice: {hint}")
        
        update_game_info()
    
    def update_game_info():
        """Mettre à jour les informations du jeu"""
        if color_state['game_mode']:
            accuracy = (color_state['score'] / max(1, color_state['attempts'] * 10)) * 100
            game_info.set_text(f"Score: {color_state['score']} | Essais: {color_state['attempts']} | Précision: {accuracy:.1f}%")
        else:
            game_info.set_text("Score: 0 | Essais: 0")
    
    # Connexions d'événements
    custom_color_btn.button_clicked.connect(lambda _: choose_custom_color())
    random_color_btn.button_clicked.connect(lambda _: generate_random_color())
    bg_color_btn.button_clicked.connect(lambda _: apply_color_to_demo(
        QColorDialog.getColor().name() if QColorDialog.getColor().isValid() else '#ffffff', 
        'background', 'Fond personnalisé'))
    gradient_btn.button_clicked.connect(lambda _: generate_gradient())
    
    complementary_btn.button_clicked.connect(lambda _: generate_complementary())
    triadic_btn.button_clicked.connect(lambda _: generate_triadic())
    analogous_btn.button_clicked.connect(lambda _: generate_analogous())
    
    start_game_btn.button_clicked.connect(lambda _: start_color_game())
    clear_history_btn.button_clicked.connect(lambda _: (
        color_state['color_history'].clear(), update_history_display()))
    
    # Instructions
    instructions = DraggableLabel(
        "🎨 Studio de Couleurs Interactif:\n"
        "• Cliquez sur les couleurs pour changer le texte de démonstration\n"
        "• Explorez les harmonies de couleurs automatiques\n"
        "• Jouez au jeu de devinette de couleurs\n"
        "• Créez vos propres couleurs avec le sélecteur personnalisé"
    )
    instructions.set_style_preset('info')
    instructions.resize(500, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 750))
    
    # Initialiser l'affichage
    update_color_info('#000000')
    update_history_display()
    update_game_info()
    
    window.show()
    print("📱 Studio de couleurs lancé avec palette complète")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)