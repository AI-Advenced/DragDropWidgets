#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tableau de bord interactif avec widgets de données

Ce fichier démontre :
- Utilisation de widgets personnalisés (ProgressBar, Slider, TextEdit)
- Interactions entre widgets
- Mise à jour dynamique de données
- Interface utilisateur complète

Exécution :
    python interactive_dashboard.py
"""

import sys
from PySide6.QtCore import QPoint, QTimer
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.widgets.custom import DraggableProgressBar, DraggableSlider, DraggableTextEdit


def main():
    """Fonction principale du tableau de bord interactif"""
    app, window, drop_zone = create_app("Tableau de Bord Interactif", (1200, 800))
    
    print("📊 Démarrage du tableau de bord interactif")
    print("=" * 60)
    print("Fonctionnalités:")
    print("• Barres de progression animées")
    print("• Sliders interactifs")
    print("• Zone de saisie de texte")
    print("• Mise à jour temps réel")
    print("• Contrôles de données")
    print("=" * 60)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre principal
    title = DraggableLabel("Tableau de Bord Interactif")
    title.set_style_preset('title')
    title.set_font_size(24)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section 1: Barres de progression
    progress_title = DraggableLabel("Indicateurs de Performance")
    progress_title.set_style_preset('subtitle')
    progress_title.set_font_size(18)
    drop_zone.add_widget(progress_title, QPoint(50, 100))
    
    # Créer plusieurs barres de progression
    progress_bars = []
    progress_labels = []
    progress_configs = [
        ("CPU Usage", 45, "#3498db"),
        ("Memory", 72, "#2ecc71"),
        ("Disk I/O", 28, "#e74c3c"),
        ("Network", 61, "#f39c12")
    ]
    
    for i, (name, initial_value, color) in enumerate(progress_configs):
        # Label du nom
        name_label = DraggableLabel(name)
        name_label.set_font_size(12)
        name_label.set_font_bold(True)
        drop_zone.add_widget(name_label, QPoint(70, 140 + i * 60))
        
        # Barre de progression
        progress = DraggableProgressBar(initial_value)
        progress.resize(200, 25)
        progress.set_snap_to_grid(True, 25)
        drop_zone.add_widget(progress, QPoint(180, 140 + i * 60))
        
        # Label de valeur
        value_label = DraggableLabel(f"{initial_value}%")
        value_label.set_font_size(11)
        drop_zone.add_widget(value_label, QPoint(400, 142 + i * 60))
        
        progress_bars.append(progress)
        progress_labels.append(value_label)
    
    # Section 2: Contrôles interactifs
    controls_title = DraggableLabel("Contrôles Interactifs")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(18)
    drop_zone.add_widget(controls_title, QPoint(500, 100))
    
    # Sliders de contrôle
    sliders = []
    slider_labels = []
    slider_configs = [
        ("Volume", 75),
        ("Luminosité", 60),
        ("Contraste", 85),
        ("Température", 42)
    ]
    
    for i, (name, initial_value) in enumerate(slider_configs):
        # Label du slider
        slider_name = DraggableLabel(name)
        slider_name.set_font_size(12)
        slider_name.set_font_bold(True)
        drop_zone.add_widget(slider_name, QPoint(520, 140 + i * 60))
        
        # Slider
        slider = DraggableSlider(initial_value)
        slider.resize(150, 30)
        slider.set_snap_to_grid(True, 25)
        drop_zone.add_widget(slider, QPoint(620, 140 + i * 60))
        
        # Label de valeur du slider
        slider_value = DraggableLabel(f"{initial_value}")
        slider_value.set_font_size(11)
        drop_zone.add_widget(slider_value, QPoint(790, 142 + i * 60))
        
        sliders.append(slider)
        slider_labels.append(slider_value)
    
    # Section 3: Zone de données
    data_title = DraggableLabel("Données et Logs")
    data_title.set_style_preset('subtitle')
    data_title.set_font_size(18)
    drop_zone.add_widget(data_title, QPoint(50, 380))
    
    # Zone de texte pour logs
    log_area = DraggableTextEdit("=== LOG SYSTÈME ===\nSystème initialisé avec succès.\nToutes les métriques sont opérationnelles.\n")
    log_area.resize(400, 150)
    log_area.set_snap_to_grid(True, 25)
    drop_zone.add_widget(log_area, QPoint(70, 420))
    
    # Zone de saisie de commandes
    command_label = DraggableLabel("Console de Commandes:")
    command_label.set_font_size(12)
    command_label.set_font_bold(True)
    drop_zone.add_widget(command_label, QPoint(500, 420))
    
    command_input = DraggableTextEdit("Entrez une commande...")
    command_input.resize(300, 40)
    command_input.set_snap_to_grid(True, 25)
    drop_zone.add_widget(command_input, QPoint(500, 450))
    
    # Boutons d'action
    buttons_config = [
        ("Exécuter", "success", lambda: execute_command()),
        ("Effacer Logs", "warning", lambda: clear_logs()),
        ("Actualiser", "info", lambda: refresh_data()),
        ("Sauvegarder", "primary", lambda: save_data())
    ]
    
    action_buttons = []
    for i, (text, style, action) in enumerate(buttons_config):
        btn = DraggableButton(text)
        btn.set_style(style)
        btn.set_snap_to_grid(True, 25)
        btn.button_clicked.connect(lambda _, a=action: a())
        drop_zone.add_widget(btn, QPoint(500 + (i % 2) * 120, 520 + (i // 2) * 50))
        action_buttons.append(btn)
    
    # Section 4: Statistiques temps réel
    stats_title = DraggableLabel("Statistiques Temps Réel")
    stats_title.set_style_preset('subtitle')
    stats_title.set_font_size(18)
    drop_zone.add_widget(stats_title, QPoint(50, 600))
    
    # Compteurs
    counters = {
        'operations': 0,
        'commands': 0,
        'updates': 0
    }
    
    counter_labels = {}
    counter_configs = [
        ("operations", "Opérations Totales"),
        ("commands", "Commandes Exécutées"),
        ("updates", "Mises à Jour")
    ]
    
    for i, (key, name) in enumerate(counter_configs):
        counter_name = DraggableLabel(f"{name}:")
        counter_name.set_font_size(12)
        drop_zone.add_widget(counter_name, QPoint(70, 640 + i * 30))
        
        counter_value = DraggableLabel("0")
        counter_value.set_font_size(14)
        counter_value.set_font_bold(True)
        counter_value.set_color("#2980b9")
        drop_zone.add_widget(counter_value, QPoint(220, 640 + i * 30))
        
        counter_labels[key] = counter_value
    
    # Horloge système
    time_label = DraggableLabel("Temps Système")
    time_label.set_font_size(12)
    drop_zone.add_widget(time_label, QPoint(400, 640))
    
    clock_display = DraggableLabel("00:00:00")
    clock_display.set_font_size(16)
    clock_display.set_font_bold(True)
    clock_display.set_style_preset('info')
    drop_zone.add_widget(clock_display, QPoint(400, 665))
    
    # États du système
    system_state = {
        'simulation_active': False,
        'log_count': 3
    }
    
    # Fonctions d'action
    def execute_command():
        """Exécuter une commande"""
        command_text = command_input.get_text().strip()
        if command_text and command_text != "Entrez une commande...":
            counters['commands'] += 1
            counter_labels['commands'].set_text(str(counters['commands']))
            
            # Ajouter au log
            current_log = log_area.get_text()
            new_log = f"{current_log}> {command_text}\nCommande exécutée avec succès.\n"
            log_area.set_text(new_log)
            
            # Effacer la commande
            command_input.set_text("")
            
            system_state['log_count'] += 2
            print(f"💻 Commande exécutée: {command_text}")
    
    def clear_logs():
        """Effacer les logs"""
        log_area.set_text("=== LOG SYSTÈME ===\nLogs effacés.\n")
        system_state['log_count'] = 2
        print("🧹 Logs effacés")
    
    def refresh_data():
        """Actualiser les données"""
        import random
        
        # Mettre à jour les barres de progression
        for i, (progress, label) in enumerate(zip(progress_bars, progress_labels)):
            new_value = random.randint(10, 95)
            progress.set_value(new_value)
            label.set_text(f"{new_value}%")
        
        counters['updates'] += 1
        counter_labels['updates'].set_text(str(counters['updates']))
        
        # Ajouter au log
        current_log = log_area.get_text()
        new_log = f"{current_log}Données actualisées automatiquement.\n"
        log_area.set_text(new_log)
        system_state['log_count'] += 1
        
        print("🔄 Données actualisées")
    
    def save_data():
        """Sauvegarder les données"""
        counters['operations'] += 1
        counter_labels['operations'].set_text(str(counters['operations']))
        
        # Ajouter au log
        current_log = log_area.get_text()
        new_log = f"{current_log}Configuration sauvegardée.\n"
        log_area.set_text(new_log)
        system_state['log_count'] += 1
        
        print("💾 Données sauvegardées")
    
    # Bouton de simulation
    simulate_btn = DraggableButton("Démarrer Simulation")
    simulate_btn.set_style('success')
    simulate_btn.set_snap_to_grid(True, 25)
    drop_zone.add_widget(simulate_btn, QPoint(700, 520))
    
    def toggle_simulation():
        """Basculer la simulation"""
        system_state['simulation_active'] = not system_state['simulation_active']
        
        if system_state['simulation_active']:
            simulate_btn.set_text("Arrêter Simulation")
            simulate_btn.set_style('danger')
            print("▶️ Simulation démarrée")
        else:
            simulate_btn.set_text("Démarrer Simulation")
            simulate_btn.set_style('success')
            print("⏹️ Simulation arrêtée")
    
    simulate_btn.button_clicked.connect(lambda _: toggle_simulation())
    
    # Timer pour mise à jour temps réel
    def update_clock():
        """Mettre à jour l'horloge"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        clock_display.set_text(current_time)
        
        # Si simulation active, mettre à jour aléatoirement
        if system_state['simulation_active']:
            import random
            if random.random() < 0.3:  # 30% de chance de mise à jour
                refresh_data()
    
    # Timer principal
    timer = QTimer()
    timer.timeout.connect(update_clock)
    timer.start(1000)  # Mise à jour chaque seconde
    
    # Connecter les événements des sliders pour mise à jour temps réel
    def update_slider_display(slider_idx):
        """Mettre à jour l'affichage du slider"""
        def update():
            value = sliders[slider_idx].metadata.get('value', 0)
            slider_labels[slider_idx].set_text(str(value))
        return update
    
    # Note: Cette partie nécessiterait l'implémentation des signaux dans DraggableSlider
    # pour être pleinement fonctionnelle
    
    # Instructions finales
    instructions = DraggableLabel(
        "💡 Tableau de bord entièrement interactif!\n"
        "• Utilisez les boutons pour diverses actions\n" 
        "• Tapez des commandes dans la console\n"
        "• Démarrez la simulation pour voir les données changer\n"
        "• Tous les widgets sont déplaçables par glisser-déposer"
    )
    instructions.set_style_preset('info')
    instructions.set_font_size(11)
    instructions.resize(450, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(700, 600))
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Tableau de bord lancé avec {len(progress_bars)} indicateurs")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)