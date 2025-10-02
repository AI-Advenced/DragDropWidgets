#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tableau de bord de surveillance avec données en temps réel

Ce fichier démontre :
- Monitoring de métriques système simulées
- Graphiques et indicateurs temps réel
- Alertes et notifications
- Configuration de seuils
- Historique de données

Exécution :
    python monitoring_dashboard.py
"""

import sys
import random
from datetime import datetime
from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QMessageBox
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.widgets.custom import DraggableProgressBar, DraggableSlider


def main():
    """Tableau de bord de surveillance principal"""
    app, window, drop_zone = create_app("Dashboard de Surveillance", (1400, 1000))
    
    print("📊 Tableau de bord de surveillance temps réel")
    print("=" * 50)
    
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre principal
    title = DraggableLabel("Dashboard de Surveillance Système")
    title.set_style_preset('title')
    title.set_font_size(22)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Horloge système
    clock = DraggableLabel("00:00:00")
    clock.set_style_preset('info')
    clock.set_font_size(16)
    clock.set_font_bold(True)
    drop_zone.add_widget(clock, QPoint(1200, 30))
    
    # Section métriques système
    metrics_title = DraggableLabel("Métriques Système")
    metrics_title.set_style_preset('subtitle')
    metrics_title.set_font_size(18)
    drop_zone.add_widget(metrics_title, QPoint(50, 80))
    
    # État du système de monitoring
    monitoring_state = {
        'active': False,
        'cpu_usage': 25,
        'memory_usage': 45,
        'disk_usage': 60,
        'network_in': 15,
        'network_out': 20,
        'temperature': 42,
        'alerts': [],
        'alert_thresholds': {
            'cpu': 80,
            'memory': 85,
            'disk': 90,
            'temperature': 75
        },
        'data_history': []
    }
    
    # Création des indicateurs de métriques
    metrics = [
        ('CPU Usage', 'cpu_usage', '#3498db'),
        ('Memory', 'memory_usage', '#2ecc71'),  
        ('Disk Space', 'disk_usage', '#e74c3c'),
        ('Network In', 'network_in', '#f39c12'),
        ('Network Out', 'network_out', '#9b59b6'),
        ('Temperature', 'temperature', '#e67e22')
    ]
    
    metric_widgets = {}
    
    for i, (name, key, color) in enumerate(metrics):
        row = i // 3
        col = i % 3
        x_pos = 70 + col * 250
        y_pos = 120 + row * 100
        
        # Label du nom
        name_label = DraggableLabel(name)
        name_label.set_font_size(12)
        name_label.set_font_bold(True)
        drop_zone.add_widget(name_label, QPoint(x_pos, y_pos))
        
        # Barre de progression
        progress = DraggableProgressBar(monitoring_state[key])
        progress.resize(180, 25)
        drop_zone.add_widget(progress, QPoint(x_pos, y_pos + 25))
        
        # Valeur numérique
        value_label = DraggableLabel(f"{monitoring_state[key]}%")
        value_label.set_font_size(14)
        value_label.set_font_bold(True)
        drop_zone.add_widget(value_label, QPoint(x_pos + 190, y_pos + 25))
        
        metric_widgets[key] = {
            'progress': progress,
            'value_label': value_label,
            'name_label': name_label
        }
    
    # Section contrôles
    controls_title = DraggableLabel("Contrôles de Surveillance")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(800, 80))
    
    # Boutons de contrôle
    start_btn = DraggableButton("Démarrer Surveillance")
    start_btn.set_style('success')
    drop_zone.add_widget(start_btn, QPoint(820, 120))
    
    stop_btn = DraggableButton("Arrêter Surveillance")
    stop_btn.set_style('danger')
    drop_zone.add_widget(stop_btn, QPoint(970, 120))
    
    reset_btn = DraggableButton("Reset Alertes")
    reset_btn.set_style('warning')
    drop_zone.add_widget(reset_btn, QPoint(820, 160))
    
    config_btn = DraggableButton("Configuration")
    config_btn.set_style('info')
    drop_zone.add_widget(config_btn, QPoint(970, 160))
    
    # Statut du système
    status_label = DraggableLabel("Statut: Arrêté")
    status_label.set_style_preset('warning')
    status_label.set_font_size(14)
    drop_zone.add_widget(status_label, QPoint(820, 200))
    
    # Section alertes
    alerts_title = DraggableLabel("Centre d'Alertes")
    alerts_title.set_style_preset('subtitle')
    alerts_title.set_font_size(16)
    drop_zone.add_widget(alerts_title, QPoint(50, 350))
    
    # Zone d'affichage des alertes
    alerts_display = DraggableLabel("Aucune alerte active")
    alerts_display.resize(700, 150)
    alerts_display.set_background_color("#fff3cd")
    alerts_display.set_word_wrap(True)
    alerts_display.set_font_size(11)
    drop_zone.add_widget(alerts_display, QPoint(70, 390))
    
    # Compteur d'alertes
    alert_counter = DraggableLabel("Alertes: 0")
    alert_counter.set_font_size(12)
    alert_counter.set_font_bold(True)
    drop_zone.add_widget(alert_counter, QPoint(800, 350))
    
    # Section configuration des seuils
    thresholds_title = DraggableLabel("Seuils d'Alerte")
    thresholds_title.set_style_preset('subtitle')
    thresholds_title.set_font_size(16)
    drop_zone.add_widget(thresholds_title, QPoint(800, 250))
    
    # Sliders pour configurer les seuils
    threshold_sliders = {}
    threshold_configs = [
        ('CPU', 'cpu', 80),
        ('Memory', 'memory', 85),
        ('Disk', 'disk', 90),
        ('Temp', 'temperature', 75)
    ]
    
    for i, (name, key, default_val) in enumerate(threshold_configs):
        x_pos = 820 + (i % 2) * 200
        y_pos = 290 + (i // 2) * 60
        
        # Label
        threshold_label = DraggableLabel(f"{name}: {default_val}%")
        threshold_label.set_font_size(10)
        drop_zone.add_widget(threshold_label, QPoint(x_pos, y_pos))
        
        # Slider
        slider = DraggableSlider(default_val)
        slider.resize(120, 25)
        drop_zone.add_widget(slider, QPoint(x_pos, y_pos + 20))
        
        threshold_sliders[key] = {
            'slider': slider,
            'label': threshold_label
        }
    
    # Section historique
    history_title = DraggableLabel("Historique des Données")
    history_title.set_style_preset('subtitle')
    history_title.set_font_size(16)
    drop_zone.add_widget(history_title, QPoint(50, 560))
    
    # Affichage de l'historique simplifié
    history_display = DraggableLabel("Historique vide - Démarrez la surveillance")
    history_display.resize(600, 100)
    history_display.set_background_color("#f8f9fa")
    history_display.set_word_wrap(True)
    history_display.set_font_size(10)
    drop_zone.add_widget(history_display, QPoint(70, 600))
    
    # Boutons d'historique
    save_history_btn = DraggableButton("Sauver Historique")
    save_history_btn.set_style('primary')
    drop_zone.add_widget(save_history_btn, QPoint(700, 600))
    
    clear_history_btn = DraggableButton("Effacer Historique")
    clear_history_btn.set_style('secondary')
    drop_zone.add_widget(clear_history_btn, QPoint(700, 640))
    
    # Timer pour la surveillance
    monitoring_timer = QTimer()
    
    def update_metrics():
        """Mettre à jour les métriques simulées"""
        if not monitoring_state['active']:
            return
        
        # Simuler des changements de métriques
        for key in ['cpu_usage', 'memory_usage', 'network_in', 'network_out']:
            current = monitoring_state[key]
            change = random.randint(-5, 5)
            new_value = max(0, min(100, current + change))
            monitoring_state[key] = new_value
        
        # Disk usage change plus lentement
        if random.random() < 0.3:
            monitoring_state['disk_usage'] = max(0, min(100, 
                monitoring_state['disk_usage'] + random.randint(-1, 2)))
        
        # Température varie selon le CPU
        base_temp = 35 + (monitoring_state['cpu_usage'] * 0.4)
        monitoring_state['temperature'] = int(base_temp + random.randint(-3, 3))
        
        # Mettre à jour l'affichage
        update_display()
        
        # Vérifier les alertes
        check_alerts()
        
        # Ajouter à l'historique
        add_to_history()
    
    def update_display():
        """Mettre à jour l'affichage des métriques"""
        for key, widgets in metric_widgets.items():
            value = monitoring_state[key]
            widgets['progress'].set_value(value)
            
            if key == 'temperature':
                widgets['value_label'].set_text(f"{value}°C")
            else:
                widgets['value_label'].set_text(f"{value}%")
            
            # Changer la couleur selon la criticité
            if key in monitoring_state['alert_thresholds']:
                threshold = monitoring_state['alert_thresholds'][key]
                if value >= threshold:
                    widgets['value_label'].set_color('#e74c3c')  # Rouge
                elif value >= threshold * 0.8:
                    widgets['value_label'].set_color('#f39c12')  # Orange
                else:
                    widgets['value_label'].set_color('#27ae60')  # Vert
    
    def check_alerts():
        """Vérifier et gérer les alertes"""
        current_time = datetime.now().strftime("%H:%M:%S")
        new_alerts = []
        
        for metric, threshold in monitoring_state['alert_thresholds'].items():
            if metric == 'temperature':
                value = monitoring_state[metric]
                if value >= threshold:
                    alert_msg = f"[{current_time}] ALERTE: Température élevée ({value}°C >= {threshold}°C)"
                    new_alerts.append(alert_msg)
            else:
                key = f"{metric}_usage"
                if key in monitoring_state:
                    value = monitoring_state[key]
                    if value >= threshold:
                        alert_msg = f"[{current_time}] ALERTE: {metric.upper()} élevé ({value}% >= {threshold}%)"
                        new_alerts.append(alert_msg)
        
        # Ajouter les nouvelles alertes
        for alert in new_alerts:
            if alert not in monitoring_state['alerts']:
                monitoring_state['alerts'].append(alert)
                print(f"🚨 {alert}")
        
        # Garder seulement les 10 dernières alertes
        monitoring_state['alerts'] = monitoring_state['alerts'][-10:]
        
        # Mettre à jour l'affichage des alertes
        update_alerts_display()
    
    def update_alerts_display():
        """Mettre à jour l'affichage des alertes"""
        alert_count = len(monitoring_state['alerts'])
        alert_counter.set_text(f"Alertes: {alert_count}")
        
        if alert_count == 0:
            alerts_display.set_text("✅ Aucune alerte active - Tous les systèmes fonctionnent normalement")
            alerts_display.set_background_color("#d1ecf1")
        else:
            alert_text = f"🚨 {alert_count} alerte(s) active(s):\n\n"
            alert_text += "\n".join(monitoring_state['alerts'][-5:])  # 5 dernières alertes
            if alert_count > 5:
                alert_text += f"\n... et {alert_count - 5} autre(s)"
            alerts_display.set_text(alert_text)
            alerts_display.set_background_color("#f8d7da")
    
    def add_to_history():
        """Ajouter les données actuelles à l'historique"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = {
            'time': timestamp,
            'cpu': monitoring_state['cpu_usage'],
            'memory': monitoring_state['memory_usage'],
            'disk': monitoring_state['disk_usage'],
            'temp': monitoring_state['temperature']
        }
        
        monitoring_state['data_history'].append(history_entry)
        
        # Garder seulement les 50 derniers points
        monitoring_state['data_history'] = monitoring_state['data_history'][-50:]
        
        # Mettre à jour l'affichage de l'historique
        update_history_display()
    
    def update_history_display():
        """Mettre à jour l'affichage de l'historique"""
        history = monitoring_state['data_history']
        if not history:
            history_display.set_text("Historique vide - Démarrez la surveillance")
            return
        
        # Afficher les 5 dernières entrées
        recent = history[-5:]
        history_text = f"📊 Historique ({len(history)} entrées):\n\n"
        
        for entry in recent:
            history_text += f"{entry['time']}: CPU={entry['cpu']}% MEM={entry['memory']}% DISK={entry['disk']}% TEMP={entry['temp']}°C\n"
        
        if len(history) > 5:
            history_text += f"... et {len(history) - 5} entrée(s) précédente(s)"
        
        history_display.set_text(history_text)
    
    def update_clock():
        """Mettre à jour l'horloge"""
        current_time = datetime.now().strftime("%H:%M:%S")
        clock.set_text(current_time)
    
    # Fonctions de contrôle
    def start_monitoring():
        """Démarrer la surveillance"""
        monitoring_state['active'] = True
        monitoring_timer.start(2000)  # Mise à jour toutes les 2 secondes
        
        status_label.set_text("Statut: Actif 🟢")
        status_label.set_style_preset('success')
        
        print("▶️ Surveillance démarrée")
    
    def stop_monitoring():
        """Arrêter la surveillance"""
        monitoring_state['active'] = False
        monitoring_timer.stop()
        
        status_label.set_text("Statut: Arrêté 🔴")
        status_label.set_style_preset('warning')
        
        print("⏹️ Surveillance arrêtée")
    
    def reset_alerts():
        """Réinitialiser les alertes"""
        monitoring_state['alerts'].clear()
        update_alerts_display()
        print("🔄 Alertes réinitialisées")
    
    def configure_thresholds():
        """Configurer les seuils d'alerte"""
        # Mettre à jour les seuils depuis les sliders
        for key, widgets in threshold_sliders.items():
            value = widgets['slider'].metadata.get('value', 50)
            monitoring_state['alert_thresholds'][key] = value
            widgets['label'].set_text(f"{key.title()}: {value}%")
        
        QMessageBox.information(window, "Configuration", "Seuils d'alerte mis à jour!")
        print("⚙️ Seuils configurés")
    
    def save_history():
        """Sauvegarder l'historique"""
        if not monitoring_state['data_history']:
            QMessageBox.information(window, "Historique Vide", "Aucune donnée à sauvegarder")
            return
        
        filename = f"monitoring_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w') as f:
                f.write("Time,CPU,Memory,Disk,Temperature\n")
                for entry in monitoring_state['data_history']:
                    f.write(f"{entry['time']},{entry['cpu']},{entry['memory']},{entry['disk']},{entry['temp']}\n")
            
            QMessageBox.information(window, "Sauvegarde", f"Historique sauvé: {filename}")
            print(f"💾 Historique sauvegardé: {filename}")
        except Exception as e:
            QMessageBox.warning(window, "Erreur", f"Erreur de sauvegarde: {e}")
    
    def clear_history():
        """Effacer l'historique"""
        monitoring_state['data_history'].clear()
        update_history_display()
        print("🧹 Historique effacé")
    
    # Connexions
    start_btn.button_clicked.connect(lambda _: start_monitoring())
    stop_btn.button_clicked.connect(lambda _: stop_monitoring())
    reset_btn.button_clicked.connect(lambda _: reset_alerts())
    config_btn.button_clicked.connect(lambda _: configure_thresholds())
    save_history_btn.button_clicked.connect(lambda _: save_history())
    clear_history_btn.button_clicked.connect(lambda _: clear_history())
    
    # Timer pour l'horloge
    clock_timer = QTimer()
    clock_timer.timeout.connect(update_clock)
    clock_timer.start(1000)
    
    # Timer pour les métriques
    monitoring_timer.timeout.connect(update_metrics)
    
    # Instructions
    instructions = DraggableLabel(
        "📊 Dashboard de Surveillance:\n"
        "• Démarrez la surveillance pour voir les métriques en temps réel\n"
        "• Configurez les seuils d'alerte avec les sliders\n"
        "• Surveillez les alertes et l'historique des données\n"
        "• Sauvegardez l'historique en CSV pour analyse"
    )
    instructions.set_style_preset('info')
    instructions.resize(600, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 750))
    
    # Initialiser l'affichage
    update_display()
    update_alerts_display()
    update_clock()
    
    window.show()
    print(f"📱 Dashboard de surveillance lancé avec {len(metrics)} métriques")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)