#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de sauvegarde automatique avec horodatage

Ce fichier démontre :
- Sauvegarde automatique périodique
- Gestion des versions de backup
- Restauration de backups
- Nettoyage automatique des anciens backups
- Monitoring des changements

Exécution :
    python backup_system.py
"""

import sys
import os
import glob
from datetime import datetime, timedelta
from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QMessageBox, QListWidget, QVBoxLayout, QWidget
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.utils.serializer import LayoutSerializer


def main():
    """Fonction principale du système de backup"""
    app, window, drop_zone = create_app("Système de Backup Automatique", (1200, 800))
    
    print("🗄️ Système de backup automatique")
    print("=" * 50)
    
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Créer le dossier de backup
    backup_dir = "auto_backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Dossier de backup créé: {backup_dir}")
    
    # Titre
    title = DraggableLabel("Système de Sauvegarde Automatique")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Créer quelques widgets de test
    test_widgets = []
    
    btn1 = DraggableButton("Widget Test 1")
    btn1.set_style('primary')
    drop_zone.add_widget(btn1, QPoint(100, 100))
    test_widgets.append(btn1)
    
    btn2 = DraggableButton("Widget Test 2") 
    btn2.set_style('success')
    drop_zone.add_widget(btn2, QPoint(250, 100))
    test_widgets.append(btn2)
    
    label1 = DraggableLabel("Modifiez-moi pour tester les backups!")
    label1.set_style_preset('info')
    drop_zone.add_widget(label1, QPoint(100, 150))
    test_widgets.append(label1)
    
    # Section de contrôle
    controls_title = DraggableLabel("Contrôles de Backup")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(500, 80))
    
    # État du système
    backup_state = {
        'auto_backup_enabled': False,
        'backup_interval': 30,  # secondes
        'max_backups': 10,
        'last_backup_time': None,
        'backup_count': 0,
        'changes_detected': False
    }
    
    # Affichage du statut
    status_display = DraggableLabel("Statut: Arrêté")
    status_display.set_style_preset('warning')
    status_display.set_font_size(14)
    drop_zone.add_widget(status_display, QPoint(520, 120))
    
    # Compteur de backups
    backup_counter = DraggableLabel("Backups: 0")
    backup_counter.set_font_size(12)
    drop_zone.add_widget(backup_counter, QPoint(520, 150))
    
    # Dernière sauvegarde
    last_backup_label = DraggableLabel("Dernier backup: Jamais")
    last_backup_label.set_font_size(10)
    drop_zone.add_widget(last_backup_label, QPoint(520, 170))
    
    # Boutons de contrôle
    start_btn = DraggableButton("Démarrer Auto-Backup")
    start_btn.set_style('success')
    drop_zone.add_widget(start_btn, QPoint(520, 200))
    
    stop_btn = DraggableButton("Arrêter Auto-Backup")
    stop_btn.set_style('danger')
    drop_zone.add_widget(stop_btn, QPoint(680, 200))
    
    manual_backup_btn = DraggableButton("Backup Manuel")
    manual_backup_btn.set_style('primary')
    drop_zone.add_widget(manual_backup_btn, QPoint(520, 240))
    
    cleanup_btn = DraggableButton("Nettoyer Anciens")
    cleanup_btn.set_style('warning')
    drop_zone.add_widget(cleanup_btn, QPoint(680, 240))
    
    # Liste des backups
    backups_title = DraggableLabel("Backups Disponibles")
    backups_title.set_style_preset('subtitle')
    backups_title.set_font_size(14)
    drop_zone.add_widget(backups_title, QPoint(520, 290))
    
    backups_list = DraggableLabel("Aucun backup")
    backups_list.resize(350, 150)
    backups_list.set_background_color("#f8f9fa")
    backups_list.set_word_wrap(True)
    backups_list.set_font_size(9)
    drop_zone.add_widget(backups_list, QPoint(520, 320))
    
    # Boutons de restauration
    restore_btn = DraggableButton("Restaurer Dernier")
    restore_btn.set_style('info')
    drop_zone.add_widget(restore_btn, QPoint(520, 480))
    
    # Log des activités
    log_title = DraggableLabel("Log d'Activité")
    log_title.set_style_preset('subtitle')
    log_title.set_font_size(14)
    drop_zone.add_widget(log_title, QPoint(50, 250))
    
    activity_log = DraggableLabel("=== LOG DE BACKUP ===\nSystème initialisé")
    activity_log.resize(400, 200)
    activity_log.set_background_color("#f0f8ff")
    activity_log.set_word_wrap(True)
    activity_log.set_font_size(10)
    drop_zone.add_widget(activity_log, QPoint(50, 280))
    
    # Fonctions utilitaires
    def log_activity(message):
        """Ajouter une entrée au log d'activité"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_log = activity_log.get_text()
        lines = current_log.split('\n')
        if len(lines) > 15:  # Garder seulement 15 lignes
            lines = lines[-15:]
        
        lines.append(f"[{timestamp}] {message}")
        activity_log.set_text('\n'.join(lines))
        print(f"🗄️ [{timestamp}] {message}")
    
    def update_backup_list():
        """Mettre à jour la liste des backups"""
        pattern = os.path.join(backup_dir, "auto_backup_*.json")
        backup_files = sorted(glob.glob(pattern), reverse=True)
        
        if not backup_files:
            backups_list.set_text("Aucun backup disponible")
            return
        
        list_text = f"📦 {len(backup_files)} backup(s) disponible(s):\n\n"
        
        for i, filepath in enumerate(backup_files[:10]):  # Montrer max 10
            filename = os.path.basename(filepath)
            # Extraire la date du nom du fichier
            try:
                date_part = filename.replace("auto_backup_", "").replace(".json", "")
                date_obj = datetime.strptime(date_part, "%Y%m%d_%H%M%S")
                date_str = date_obj.strftime("%d/%m %H:%M:%S")
            except:
                date_str = "Date inconnue"
            
            file_size = os.path.getsize(filepath)
            list_text += f"• {date_str} ({file_size} bytes)\n"
        
        if len(backup_files) > 10:
            list_text += f"... et {len(backup_files) - 10} autre(s)"
        
        backups_list.set_text(list_text)
        backup_state['backup_count'] = len(backup_files)
        backup_counter.set_text(f"Backups: {len(backup_files)}")
    
    def update_status():
        """Mettre à jour l'affichage du statut"""
        if backup_state['auto_backup_enabled']:
            status_display.set_text("Statut: Actif 🟢")
            status_display.set_style_preset('success')
        else:
            status_display.set_text("Statut: Arrêté 🔴")
            status_display.set_style_preset('warning')
        
        if backup_state['last_backup_time']:
            time_str = backup_state['last_backup_time'].strftime("%H:%M:%S")
            last_backup_label.set_text(f"Dernier backup: {time_str}")
        else:
            last_backup_label.set_text("Dernier backup: Jamais")
    
    def create_backup():
        """Créer un backup du layout actuel"""
        try:
            layout_data = drop_zone.get_layout_data()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"auto_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            success = LayoutSerializer.save_to_json(layout_data, backup_path)
            
            if success:
                backup_state['last_backup_time'] = datetime.now()
                backup_state['changes_detected'] = False
                
                log_activity(f"Backup créé: {backup_filename}")
                update_backup_list()
                update_status()
                return True
            else:
                log_activity("Erreur lors de la création du backup")
                return False
                
        except Exception as e:
            log_activity(f"Erreur backup: {str(e)}")
            return False
    
    def cleanup_old_backups():
        """Nettoyer les anciens backups"""
        pattern = os.path.join(backup_dir, "auto_backup_*.json")
        backup_files = sorted(glob.glob(pattern), reverse=True)
        
        if len(backup_files) <= backup_state['max_backups']:
            log_activity("Aucun nettoyage nécessaire")
            return
        
        # Supprimer les anciens backups
        files_to_delete = backup_files[backup_state['max_backups']:]
        deleted_count = 0
        
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                log_activity(f"Erreur suppression {os.path.basename(filepath)}: {e}")
        
        if deleted_count > 0:
            log_activity(f"Nettoyage: {deleted_count} ancien(s) backup(s) supprimé(s)")
            update_backup_list()
    
    def restore_latest_backup():
        """Restaurer le dernier backup"""
        pattern = os.path.join(backup_dir, "auto_backup_*.json")
        backup_files = sorted(glob.glob(pattern), reverse=True)
        
        if not backup_files:
            QMessageBox.warning(window, "Aucun Backup", "Aucun backup disponible pour la restauration")
            return
        
        latest_backup = backup_files[0]
        
        reply = QMessageBox.question(
            window, 'Restaurer Backup',
            f'Restaurer le backup du {os.path.basename(latest_backup)}?\n\nCeci remplacera le layout actuel.',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            layout_data = LayoutSerializer.load_from_json(latest_backup)
            if layout_data:
                drop_zone.load_layout_data(layout_data)
                log_activity(f"Backup restauré: {os.path.basename(latest_backup)}")
                QMessageBox.information(window, "Restauration", "Backup restauré avec succès!")
            else:
                log_activity("Erreur lors de la restauration")
                QMessageBox.warning(window, "Erreur", "Échec de la restauration du backup")
    
    # Timer pour backup automatique
    auto_backup_timer = QTimer()
    
    def auto_backup_tick():
        """Tick du backup automatique"""
        if backup_state['auto_backup_enabled']:
            create_backup()
            # Nettoyer automatiquement si nécessaire
            cleanup_old_backups()
    
    auto_backup_timer.timeout.connect(auto_backup_tick)
    
    # Fonctions de contrôle
    def start_auto_backup():
        """Démarrer le backup automatique"""
        backup_state['auto_backup_enabled'] = True
        auto_backup_timer.start(backup_state['backup_interval'] * 1000)  # Convertir en ms
        
        update_status()
        log_activity(f"Backup automatique démarré (intervalle: {backup_state['backup_interval']}s)")
        
        # Créer un backup initial
        create_backup()
    
    def stop_auto_backup():
        """Arrêter le backup automatique"""
        backup_state['auto_backup_enabled'] = False
        auto_backup_timer.stop()
        
        update_status()
        log_activity("Backup automatique arrêté")
    
    # Connexions des boutons
    start_btn.button_clicked.connect(lambda _: start_auto_backup())
    stop_btn.button_clicked.connect(lambda _: stop_auto_backup())
    manual_backup_btn.button_clicked.connect(lambda _: create_backup())
    cleanup_btn.button_clicked.connect(lambda _: cleanup_old_backups())
    restore_btn.button_clicked.connect(lambda _: restore_latest_backup())
    
    # Instructions
    instructions = DraggableLabel(
        "🗄️ Système de Backup Automatique:\n"
        "• Démarrez le backup automatique pour sauver toutes les 30s\n"
        "• Modifiez les widgets pour voir les backups se créer\n"
        "• Restaurez des versions précédentes\n"
        "• Le nettoyage garde seulement les 10 derniers backups"
    )
    instructions.set_style_preset('info')
    instructions.resize(400, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 500))
    
    # Initialiser l'affichage
    update_backup_list()
    update_status()
    
    window.show()
    print(f"📱 Système de backup lancé - Dossier: {backup_dir}")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)