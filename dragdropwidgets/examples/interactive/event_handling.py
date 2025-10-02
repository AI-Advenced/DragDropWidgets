#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion avancée des événements et interactions

Ce fichier démontre :
- Système d'événements centralisé
- Communication entre widgets
- Événements personnalisés
- Historique des événements
- Gestion des priorités

Exécution :
    python event_handling.py
"""

import sys
from datetime import datetime
from PySide6.QtCore import QPoint, QTimer
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.utils.events import event_manager, WidgetEvents, EventPriority


def main():
    """Fonction principale pour démontrer la gestion d'événements"""
    app, window, drop_zone = create_app("Gestion d'Événements - DragDropWidgets", (1200, 900))
    
    print("⚡ Démonstration de la gestion d'événements")
    print("=" * 60)
    print("Types d'événements:")
    print("• Événements de widgets (clic, déplacement)")
    print("• Événements personnalisés")
    print("• Communication inter-widgets")
    print("• Historique et priorités")
    print("• Gestionnaires globaux et locaux")
    print("=" * 60)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre principal
    title = DraggableLabel("Système de Gestion d'Événements")
    title.set_style_preset('title')
    title.set_font_size(22)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section 1: Émetteurs d'événements
    emitters_title = DraggableLabel("1. Émetteurs d'Événements")
    emitters_title.set_style_preset('subtitle')
    emitters_title.set_font_size(16)
    drop_zone.add_widget(emitters_title, QPoint(50, 80))
    
    # Boutons émetteurs avec différents types d'événements
    emitter_configs = [
        ("Événement Simple", "simple_event", "primary"),
        ("Événement Prioritaire", "priority_event", "warning"),
        ("Événement en Chaîne", "chain_event", "info"),
        ("Événement d'Erreur", "error_event", "danger"),
        ("Diffusion Globale", "broadcast_event", "success")
    ]
    
    emitters = []
    for i, (text, event_type, style) in enumerate(emitter_configs):
        btn = DraggableButton(text)
        btn.set_style(style)
        btn.set_snap_to_grid(True, 25)
        drop_zone.add_widget(btn, QPoint(70, 120 + i * 50))
        emitters.append((btn, event_type, text))
    
    # Section 2: Récepteurs d'événements
    receivers_title = DraggableLabel("2. Récepteurs d'Événements")
    receivers_title.set_style_preset('subtitle')
    receivers_title.set_font_size(16)
    drop_zone.add_widget(receivers_title, QPoint(350, 80))
    
    # Labels récepteurs qui changent selon les événements
    receiver_configs = [
        ("Récepteur 1", "info"),
        ("Récepteur 2", "success"),
        ("Récepteur 3", "warning"),
        ("Récepteur Global", "error")
    ]
    
    receivers = []
    for i, (text, style) in enumerate(receiver_configs):
        label = DraggableLabel(text)
        label.set_style_preset(style)
        label.set_font_size(12)
        label.set_snap_to_grid(True, 25)
        drop_zone.add_widget(label, QPoint(370, 120 + i * 50))
        receivers.append(label)
    
    # Section 3: Console d'événements
    console_title = DraggableLabel("3. Console d'Événements")
    console_title.set_style_preset('subtitle') 
    console_title.set_font_size(16)
    drop_zone.add_widget(console_title, QPoint(650, 80))
    
    # Zone d'affichage des événements
    event_display = DraggableLabel("=== CONSOLE D'ÉVÉNEMENTS ===\nEn attente d'événements...")
    event_display.resize(400, 200)
    event_display.set_background_color("#f8f9fa")
    event_display.set_font_size(10)
    event_display.set_alignment('left')
    event_display.set_word_wrap(True)
    drop_zone.add_widget(event_display, QPoint(670, 120))
    
    # Section 4: Statistiques d'événements
    stats_title = DraggableLabel("4. Statistiques")
    stats_title.set_style_preset('subtitle')
    stats_title.set_font_size(16)
    drop_zone.add_widget(stats_title, QPoint(50, 380))
    
    # Compteurs d'événements
    event_stats = {
        'total_events': 0,
        'simple_events': 0,
        'priority_events': 0,
        'chain_events': 0,
        'error_events': 0,
        'broadcast_events': 0
    }
    
    stats_labels = {}
    stats_configs = [
        ('total_events', 'Total Événements'),
        ('simple_events', 'Événements Simples'),
        ('priority_events', 'Événements Prioritaires'),
        ('chain_events', 'Événements en Chaîne'),
        ('error_events', 'Événements d\'Erreur'),
        ('broadcast_events', 'Diffusions Globales')
    ]
    
    for i, (key, name) in enumerate(stats_configs):
        stat_name = DraggableLabel(f"{name}:")
        stat_name.set_font_size(11)
        drop_zone.add_widget(stat_name, QPoint(70, 420 + i * 25))
        
        stat_value = DraggableLabel("0")
        stat_value.set_font_size(12)
        stat_value.set_font_bold(True)
        stat_value.set_color("#2980b9")
        drop_zone.add_widget(stat_value, QPoint(250, 420 + i * 25))
        
        stats_labels[key] = stat_value
    
    # Section 5: Contrôles système
    controls_title = DraggableLabel("5. Contrôles Système")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(350, 380))
    
    # Boutons de contrôle
    clear_btn = DraggableButton("Effacer Console")
    clear_btn.set_style('warning')
    drop_zone.add_widget(clear_btn, QPoint(370, 420))
    
    reset_stats_btn = DraggableButton("Reset Statistiques")
    reset_stats_btn.set_style('info')
    drop_zone.add_widget(reset_stats_btn, QPoint(370, 470))
    
    history_btn = DraggableButton("Voir Historique")
    history_btn.set_style('secondary')
    drop_zone.add_widget(history_btn, QPoint(370, 520))
    
    # Section 6: Tests avancés
    advanced_title = DraggableLabel("6. Tests Avancés")
    advanced_title.set_style_preset('subtitle')
    advanced_title.set_font_size(16)
    drop_zone.add_widget(advanced_title, QPoint(650, 380))
    
    # Boutons de test
    cascade_btn = DraggableButton("Test Cascade")
    cascade_btn.set_style('info')
    drop_zone.add_widget(cascade_btn, QPoint(670, 420))
    
    flood_btn = DraggableButton("Test Flood")
    flood_btn.set_style('warning')
    drop_zone.add_widget(flood_btn, QPoint(790, 420))
    
    simulation_btn = DraggableButton("Simulation Auto")
    simulation_btn.set_style('success')
    drop_zone.add_widget(simulation_btn, QPoint(670, 470))
    
    # État du système
    system_state = {
        'simulation_running': False,
        'event_history': []
    }
    
    # Fonctions utilitaires
    def log_event(message, event_type="INFO"):
        """Ajouter un message à la console d'événements"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_text = event_display.get_text()
        
        # Garder seulement les 15 dernières lignes
        lines = current_text.split('\n')
        if len(lines) > 15:
            lines = lines[-15:]
        
        new_line = f"[{timestamp}] {event_type}: {message}"
        lines.append(new_line)
        
        event_display.set_text('\n'.join(lines))
        
        # Ajouter à l'historique
        system_state['event_history'].append({
            'timestamp': timestamp,
            'type': event_type,
            'message': message
        })
        
        print(f"📝 [{timestamp}] {event_type}: {message}")
    
    def update_stats(event_type_key):
        """Mettre à jour les statistiques"""
        event_stats['total_events'] += 1
        if event_type_key in event_stats:
            event_stats[event_type_key] += 1
        
        # Mettre à jour l'affichage
        for key, label in stats_labels.items():
            label.set_text(str(event_stats[key]))
    
    # Gestionnaires d'événements
    
    def handle_simple_event(event):
        """Gestionnaire pour événement simple"""
        log_event(f"Événement simple reçu de {event.source.__class__.__name__}", "SIMPLE")
        receivers[0].set_text("Récepteur 1: ✓ Simple")
        receivers[0].set_style_preset('success')
        update_stats('simple_events')
    
    def handle_priority_event(event):
        """Gestionnaire pour événement prioritaire"""
        log_event(f"Événement PRIORITAIRE reçu!", "PRIORITY")
        receivers[1].set_text("Récepteur 2: ⚡ Priorité")
        receivers[1].set_style_preset('warning')
        update_stats('priority_events')
        
        # Déclencher un événement en cascade
        event_manager.emit_event('cascade_response', source=event.source, 
                                data={'original_event': 'priority'})
    
    def handle_chain_event(event):
        """Gestionnaire pour événement en chaîne"""
        log_event(f"Événement en chaîne démarré", "CHAIN")
        receivers[2].set_text("Récepteur 3: 🔗 Chaîne")
        receivers[2].set_style_preset('info')
        update_stats('chain_events')
        
        # Créer une chaîne d'événements
        for i in range(3):
            event_manager.emit_event(f'chain_link_{i}', source=event.source,
                                   data={'link_number': i, 'chain_id': 'main'})
    
    def handle_error_event(event):
        """Gestionnaire pour événement d'erreur"""
        log_event(f"ERREUR simulée détectée!", "ERROR")
        receivers[3].set_text("Récepteur Global: ❌ Erreur")
        receivers[3].set_style_preset('error')
        update_stats('error_events')
        
        # Simuler une récupération d'erreur
        QTimer.singleShot(2000, lambda: log_event("Système récupéré de l'erreur", "RECOVERY"))
    
    def handle_broadcast_event(event):
        """Gestionnaire pour diffusion globale"""
        log_event(f"DIFFUSION GLOBALE à tous les récepteurs!", "BROADCAST")
        
        # Affecter tous les récepteurs
        messages = ["📡 Broadcast", "📡 Global", "📡 Diffusion", "📡 Reçu"]
        for i, (receiver, msg) in enumerate(zip(receivers, messages)):
            receiver.set_text(f"Récepteur {i+1}: {msg}")
            receiver.set_style_preset('success')
        
        update_stats('broadcast_events')
    
    def handle_cascade_response(event):
        """Gestionnaire pour réponse en cascade"""
        original = event.data.get('original_event', 'unknown')
        log_event(f"Cascade déclenchée par événement {original}", "CASCADE")
    
    def handle_chain_link(event):
        """Gestionnaire pour maillon de chaîne"""
        link_num = event.data.get('link_number', 0)
        log_event(f"Maillon de chaîne #{link_num} traité", "LINK")
    
    def handle_widget_moved(event):
        """Gestionnaire pour déplacement de widget"""
        widget = event.source
        position = event.data.get('position', 'unknown')
        log_event(f"Widget {widget.__class__.__name__} déplacé", "MOVE")
    
    def handle_widget_selected(event):
        """Gestionnaire pour sélection de widget"""
        widget = event.source
        log_event(f"Widget {widget.__class__.__name__} sélectionné", "SELECT")
    
    # Gestionnaire global pour tous les événements
    def global_event_handler(event):
        """Gestionnaire global qui intercepte tous les événements"""
        if hasattr(event, 'event_type') and not event.event_type.startswith('global_'):
            # Éviter la récursion infinie
            pass  # Le logging est déjà fait dans les gestionnaires spécifiques
    
    # Enregistrement des gestionnaires d'événements
    event_manager.register_event('simple_event', handle_simple_event)
    event_manager.register_event('priority_event', handle_priority_event, priority=EventPriority.HIGH)
    event_manager.register_event('chain_event', handle_chain_event)
    event_manager.register_event('error_event', handle_error_event)
    event_manager.register_event('broadcast_event', handle_broadcast_event)
    event_manager.register_event('cascade_response', handle_cascade_response)
    
    # Gestionnaires pour les maillons de chaîne
    for i in range(3):
        event_manager.register_event(f'chain_link_{i}', handle_chain_link)
    
    # Gestionnaires pour événements de widgets
    event_manager.register_event(WidgetEvents.WIDGET_MOVED, handle_widget_moved)
    event_manager.register_event(WidgetEvents.WIDGET_SELECTED, handle_widget_selected)
    
    # Gestionnaire global
    event_manager.register_global_handler(global_event_handler)
    
    # Connexion des boutons émetteurs
    def create_emitter_handler(event_type):
        """Créer un gestionnaire pour émetteur d'événement"""
        def handler(widget_id):
            event_manager.emit_event(event_type, source=None, 
                                   data={'timestamp': datetime.now().isoformat()})
        return handler
    
    for btn, event_type, text in emitters:
        btn.button_clicked.connect(create_emitter_handler(event_type))
    
    # Fonctions des boutons de contrôle
    def clear_console():
        """Effacer la console"""
        event_display.set_text("=== CONSOLE D'ÉVÉNEMENTS ===\nConsole effacée.")
        log_event("Console d'événements effacée", "SYSTEM")
    
    def reset_statistics():
        """Réinitialiser les statistiques"""
        for key in event_stats:
            event_stats[key] = 0
        for label in stats_labels.values():
            label.set_text("0")
        log_event("Statistiques réinitialisées", "SYSTEM")
    
    def show_history():
        """Afficher l'historique des événements"""
        history_count = len(system_state['event_history'])
        recent_events = system_state['event_history'][-5:] if system_state['event_history'] else []
        
        history_text = f"Historique: {history_count} événements\n"
        for event_info in recent_events:
            history_text += f"• [{event_info['timestamp']}] {event_info['type']}\n"
        
        event_display.set_text(history_text)
        log_event(f"Historique affiché ({history_count} événements)", "SYSTEM")
    
    def test_cascade():
        """Test d'événements en cascade"""
        log_event("Début du test en cascade", "TEST")
        event_manager.emit_event('priority_event', source=None, data={'test': 'cascade'})
        QTimer.singleShot(1000, lambda: event_manager.emit_event('chain_event', source=None))
        QTimer.singleShot(2000, lambda: log_event("Test en cascade terminé", "TEST"))
    
    def test_flood():
        """Test d'inondation d'événements"""
        log_event("Début du test d'inondation (10 événements)", "TEST")
        for i in range(10):
            QTimer.singleShot(i * 100, lambda idx=i: event_manager.emit_event(
                'simple_event', source=None, data={'flood_index': idx}))
        QTimer.singleShot(1100, lambda: log_event("Test d'inondation terminé", "TEST"))
    
    def toggle_simulation():
        """Basculer la simulation automatique"""
        system_state['simulation_running'] = not system_state['simulation_running']
        
        if system_state['simulation_running']:
            simulation_btn.set_text("Arrêter Simulation")
            simulation_btn.set_style('danger')
            log_event("Simulation automatique démarrée", "SYSTEM")
            start_auto_simulation()
        else:
            simulation_btn.set_text("Simulation Auto")
            simulation_btn.set_style('success')
            log_event("Simulation automatique arrêtée", "SYSTEM")
    
    def start_auto_simulation():
        """Démarrer la simulation automatique"""
        if system_state['simulation_running']:
            import random
            event_types = ['simple_event', 'priority_event', 'chain_event', 'broadcast_event']
            random_event = random.choice(event_types)
            event_manager.emit_event(random_event, source=None, data={'auto': True})
            
            # Programmer le prochain événement
            QTimer.singleShot(random.randint(2000, 5000), start_auto_simulation)
    
    # Connexion des boutons de contrôle
    clear_btn.button_clicked.connect(lambda _: clear_console())
    reset_stats_btn.button_clicked.connect(lambda _: reset_statistics())
    history_btn.button_clicked.connect(lambda _: show_history())
    cascade_btn.button_clicked.connect(lambda _: test_cascade())
    flood_btn.button_clicked.connect(lambda _: test_flood())
    simulation_btn.button_clicked.connect(lambda _: toggle_simulation())
    
    # Instructions
    instructions = DraggableLabel(
        "🎯 Démonstration complète du système d'événements:\n"
        "• Cliquez sur les boutons émetteurs pour déclencher des événements\n"
        "• Observez les réactions dans les récepteurs et la console\n"
        "• Utilisez les contrôles pour tester des scénarios avancés\n"
        "• Déplacez des widgets pour voir les événements de mouvement\n"
        "• La simulation automatique génère des événements aléatoires"
    )
    instructions.set_style_preset('info')
    instructions.set_font_size(11)
    instructions.resize(500, 100)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 580))
    
    # Message de bienvenue initial
    log_event("Système d'événements initialisé", "SYSTEM")
    log_event("Prêt à recevoir et traiter les événements", "READY")
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Système d'événements lancé avec {len(emitters)} émetteurs et {len(receivers)} récepteurs")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)