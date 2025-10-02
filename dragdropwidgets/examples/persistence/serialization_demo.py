#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration complète de sérialisation

Ce fichier démontre :
- Sauvegarde/chargement de layouts en JSON et YAML
- Export en code Python
- Gestion des versions de layouts
- Validation des données
- Statistiques de layouts

Exécution :
    python serialization_demo.py
"""

import sys
import os
from datetime import datetime
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.widgets.custom import DraggableProgressBar, DraggableSlider, DraggableTextEdit
from dragdropwidgets.utils.serializer import LayoutSerializer


def main():
    """Fonction principale de démonstration de sérialisation"""
    app, window, drop_zone = create_app("Démonstration Sérialisation", (1200, 800))
    
    print("💾 Démonstration de sérialisation")
    print("=" * 50)
    
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 25
    
    # Titre
    title = DraggableLabel("Système de Sérialisation Avancé")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Créer un layout de test
    test_widgets = []
    
    # Divers widgets pour tester la sérialisation
    btn1 = DraggableButton("Bouton Test")
    btn1.set_style('primary')
    drop_zone.add_widget(btn1, QPoint(100, 100))
    test_widgets.append(btn1)
    
    label1 = DraggableLabel("Label de Test")
    label1.set_style_preset('success')
    drop_zone.add_widget(label1, QPoint(100, 150))
    test_widgets.append(label1)
    
    progress1 = DraggableProgressBar(75)
    drop_zone.add_widget(progress1, QPoint(100, 200))
    test_widgets.append(progress1)
    
    slider1 = DraggableSlider(50)
    drop_zone.add_widget(slider1, QPoint(100, 250))
    test_widgets.append(slider1)
    
    text1 = DraggableTextEdit("Texte de test pour sérialisation")
    drop_zone.add_widget(text1, QPoint(100, 300))
    test_widgets.append(text1)
    
    # Section contrôles
    controls_title = DraggableLabel("Contrôles de Sérialisation")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(500, 80))
    
    # Boutons de sauvegarde
    save_json_btn = DraggableButton("Sauver JSON")
    save_json_btn.set_style('primary')
    drop_zone.add_widget(save_json_btn, QPoint(520, 120))
    
    save_yaml_btn = DraggableButton("Sauver YAML")
    save_yaml_btn.set_style('info')
    drop_zone.add_widget(save_yaml_btn, QPoint(640, 120))
    
    load_json_btn = DraggableButton("Charger JSON")
    load_json_btn.set_style('success')
    drop_zone.add_widget(load_json_btn, QPoint(520, 160))
    
    load_yaml_btn = DraggableButton("Charger YAML")
    load_yaml_btn.set_style('warning')
    drop_zone.add_widget(load_yaml_btn, QPoint(640, 160))
    
    export_code_btn = DraggableButton("Exporter Code")
    export_code_btn.set_style('secondary')
    drop_zone.add_widget(export_code_btn, QPoint(520, 200))
    
    backup_btn = DraggableButton("Backup Auto")
    backup_btn.set_style('danger')
    drop_zone.add_widget(backup_btn, QPoint(640, 200))
    
    # Zone d'information
    info_display = DraggableLabel("Prêt pour les opérations de sérialisation")
    info_display.resize(300, 150)
    info_display.set_background_color("#f8f9fa")
    info_display.set_word_wrap(True)
    drop_zone.add_widget(info_display, QPoint(520, 250))
    
    # Statistiques
    stats_display = DraggableLabel("Statistiques du Layout")
    stats_display.resize(300, 100)
    stats_display.set_background_color("#e8f4f8")
    stats_display.set_word_wrap(True)
    drop_zone.add_widget(stats_display, QPoint(520, 420))
    
    def update_stats():
        """Mettre à jour les statistiques"""
        layout_data = drop_zone.get_layout_data()
        stats = LayoutSerializer.get_layout_statistics(layout_data)
        
        stats_text = f"""📊 Statistiques du Layout:
• Total widgets: {stats.get('total_widgets', 0)}
• Types de widgets: {len(stats.get('widget_types', []))}
• Bounds: {stats.get('layout_bounds', 'N/A')}
• Dernière MAJ: {datetime.now().strftime('%H:%M:%S')}"""
        
        stats_display.set_text(stats_text)
        return stats
    
    def log_action(message):
        """Logger une action"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_text = info_display.get_text()
        lines = current_text.split('\n')[-10:]  # Garder 10 lignes
        lines.append(f"[{timestamp}] {message}")
        info_display.set_text('\n'.join(lines))
        print(f"💾 {message}")
    
    # Fonctions de sérialisation
    def save_to_json():
        """Sauvegarder en JSON"""
        layout_data = drop_zone.get_layout_data()
        
        file_path, _ = QFileDialog.getSaveFileName(
            window, "Sauvegarder Layout JSON", 
            f"layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if file_path:
            success = LayoutSerializer.save_to_json(layout_data, file_path)
            if success:
                log_action(f"Sauvegarde JSON réussie: {os.path.basename(file_path)}")
                QMessageBox.information(window, "Succès", f"Layout sauvegardé en JSON")
            else:
                log_action("Erreur lors de la sauvegarde JSON")
                QMessageBox.warning(window, "Erreur", "Échec de la sauvegarde JSON")
    
    def save_to_yaml():
        """Sauvegarder en YAML"""
        layout_data = drop_zone.get_layout_data()
        
        file_path, _ = QFileDialog.getSaveFileName(
            window, "Sauvegarder Layout YAML", 
            f"layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml",
            "YAML Files (*.yaml *.yml)"
        )
        
        if file_path:
            success = LayoutSerializer.save_to_yaml(layout_data, file_path)
            if success:
                log_action(f"Sauvegarde YAML réussie: {os.path.basename(file_path)}")
                QMessageBox.information(window, "Succès", "Layout sauvegardé en YAML")
            else:
                log_action("Erreur lors de la sauvegarde YAML")
                QMessageBox.warning(window, "Erreur", "Échec de la sauvegarde YAML")
    
    def load_from_json():
        """Charger depuis JSON"""
        file_path, _ = QFileDialog.getOpenFileName(
            window, "Charger Layout JSON", "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            layout_data = LayoutSerializer.load_from_json(file_path)
            if layout_data:
                drop_zone.load_layout_data(layout_data)
                log_action(f"Chargement JSON réussi: {os.path.basename(file_path)}")
                update_stats()
                QMessageBox.information(window, "Succès", "Layout chargé depuis JSON")
            else:
                log_action("Erreur lors du chargement JSON")
                QMessageBox.warning(window, "Erreur", "Échec du chargement JSON")
    
    def load_from_yaml():
        """Charger depuis YAML"""
        file_path, _ = QFileDialog.getOpenFileName(
            window, "Charger Layout YAML", "",
            "YAML Files (*.yaml *.yml);;All Files (*)"
        )
        
        if file_path:
            layout_data = LayoutSerializer.load_from_yaml(file_path)
            if layout_data:
                drop_zone.load_layout_data(layout_data)
                log_action(f"Chargement YAML réussi: {os.path.basename(file_path)}")
                update_stats()
                QMessageBox.information(window, "Succès", "Layout chargé depuis YAML")
            else:
                log_action("Erreur lors du chargement YAML")
                QMessageBox.warning(window, "Erreur", "Échec du chargement YAML")
    
    def export_to_code():
        """Exporter en code Python"""
        layout_data = drop_zone.get_layout_data()
        code = LayoutSerializer.export_to_code(layout_data, 'python')
        
        file_path, _ = QFileDialog.getSaveFileName(
            window, "Exporter Code Python", 
            f"generated_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
            "Python Files (*.py)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                log_action(f"Code exporté: {os.path.basename(file_path)}")
                QMessageBox.information(window, "Succès", f"Code Python exporté")
            except Exception as e:
                log_action(f"Erreur export code: {e}")
                QMessageBox.warning(window, "Erreur", f"Échec de l'export: {e}")
    
    def create_backup():
        """Créer une sauvegarde automatique"""
        layout_data = drop_zone.get_layout_data()
        
        # Créer le dossier backups s'il n'existe pas
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        backup_file = LayoutSerializer.create_backup(layout_data, backup_dir)
        log_action(f"Backup créé: {os.path.basename(backup_file)}")
        QMessageBox.information(window, "Backup", f"Sauvegarde créée:\n{backup_file}")
    
    # Connexions
    save_json_btn.button_clicked.connect(lambda _: save_to_json())
    save_yaml_btn.button_clicked.connect(lambda _: save_to_yaml())
    load_json_btn.button_clicked.connect(lambda _: load_from_json())
    load_yaml_btn.button_clicked.connect(lambda _: load_from_yaml())
    export_code_btn.button_clicked.connect(lambda _: export_to_code())
    backup_btn.button_clicked.connect(lambda _: create_backup())
    
    # Instructions
    instructions = DraggableLabel(
        "💾 Système de Sérialisation Complet:\n"
        "• Sauvegardez/chargez en JSON ou YAML\n"
        "• Exportez en code Python exécutable\n"
        "• Créez des backups automatiques\n"
        "• Modifiez le layout et testez la persistance"
    )
    instructions.set_style_preset('info')
    instructions.resize(400, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 600))
    
    # Initialiser
    update_stats()
    log_action("Système de sérialisation initialisé")
    
    window.show()
    print(f"📱 Sérialisation démo lancée avec {len(test_widgets)} widgets de test")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)