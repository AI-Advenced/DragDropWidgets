#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Galerie d'images avec manipulation

Ce fichier démontre :
- Gestion d'images avec DraggableImage
- Transformations d'images (rotation, redimensionnement)
- Interface de galerie interactive
- Sauvegarde d'images modifiées
- Contrôles de manipulation avancés

Exécution :
    python image_gallery.py
"""

import sys
import os
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QFileDialog, QMessageBox
from dragdropwidgets import create_app, DraggableButton, DraggableLabel, DraggableImage


def main():
    """Fonction principale de la galerie d'images"""
    app, window, drop_zone = create_app("Galerie d'Images Interactive", (1400, 1000))
    
    print("🖼️ Démarrage de la galerie d'images")
    print("=" * 60)
    print("Fonctionnalités:")
    print("• Chargement d'images depuis fichiers")
    print("• Rotation et retournement")
    print("• Redimensionnement intelligent")
    print("• Modes d'affichage multiples")
    print("• Sauvegarde d'images modifiées")
    print("• Métadonnées d'images")
    print("=" * 60)
    
    # Configuration de la grille
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 20
    
    # Titre principal
    title = DraggableLabel("Galerie d'Images Interactive")
    title.set_style_preset('title')
    title.set_font_size(24)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section 1: Zone de galerie principale
    gallery_title = DraggableLabel("Zone de Galerie")
    gallery_title.set_style_preset('subtitle')
    gallery_title.set_font_size(18)
    drop_zone.add_widget(gallery_title, QPoint(50, 80))
    
    # Créer 6 emplacements d'images
    image_slots = []
    for i in range(6):
        row = i // 3
        col = i % 3
        
        # Image widget
        img_widget = DraggableImage()
        img_widget.resize(200, 150)
        img_widget.set_snap_to_grid(True, 20)
        x_pos = 70 + col * 220
        y_pos = 120 + row * 200
        drop_zone.add_widget(img_widget, QPoint(x_pos, y_pos))
        
        # Label d'information sous l'image
        info_label = DraggableLabel(f"Slot {i+1}: Vide")
        info_label.set_font_size(10)
        info_label.set_alignment('center')
        drop_zone.add_widget(info_label, QPoint(x_pos, y_pos + 155))
        
        image_slots.append({
            'widget': img_widget,
            'info_label': info_label,
            'index': i,
            'has_image': False,
            'original_path': None,
            'transformations': {
                'rotation': 0,
                'flipped_h': False,
                'flipped_v': False,
                'scale_mode': 'keep_aspect_ratio'
            }
        })
    
    # Section 2: Contrôles de chargement
    loading_title = DraggableLabel("Contrôles de Chargement")
    loading_title.set_style_preset('subtitle')
    loading_title.set_font_size(16)
    drop_zone.add_widget(loading_title, QPoint(750, 80))
    
    # Boutons de chargement
    load_single_btn = DraggableButton("Charger Image")
    load_single_btn.set_style('primary')
    drop_zone.add_widget(load_single_btn, QPoint(770, 120))
    
    load_multiple_btn = DraggableButton("Charger Plusieurs")
    load_multiple_btn.set_style('info')
    drop_zone.add_widget(load_multiple_btn, QPoint(770, 160))
    
    clear_all_btn = DraggableButton("Effacer Tout")
    clear_all_btn.set_style('danger')
    drop_zone.add_widget(clear_all_btn, QPoint(770, 200))
    
    # Sélecteur de slot actuel
    slot_selector_label = DraggableLabel("Slot Sélectionné:")
    slot_selector_label.set_font_size(12)
    slot_selector_label.set_font_bold(True)
    drop_zone.add_widget(slot_selector_label, QPoint(920, 120))
    
    current_slot_label = DraggableLabel("Aucun")
    current_slot_label.set_font_size(14)
    current_slot_label.set_color('#e74c3c')
    drop_zone.add_widget(current_slot_label, QPoint(920, 140))
    
    # Section 3: Contrôles de transformation
    transform_title = DraggableLabel("Transformations")
    transform_title.set_style_preset('subtitle')
    transform_title.set_font_size(16)
    drop_zone.add_widget(transform_title, QPoint(750, 250))
    
    # Contrôles de rotation
    rotation_label = DraggableLabel("Rotation:")
    rotation_label.set_font_size(12)
    rotation_label.set_font_bold(True)
    drop_zone.add_widget(rotation_label, QPoint(770, 290))
    
    rotate_left_btn = DraggableButton("↺ 90°")
    rotate_left_btn.set_style('info')
    rotate_left_btn.resize(60, 30)
    drop_zone.add_widget(rotate_left_btn, QPoint(770, 315))
    
    rotate_right_btn = DraggableButton("↻ 90°")
    rotate_right_btn.set_style('info')
    rotate_right_btn.resize(60, 30)
    drop_zone.add_widget(rotate_right_btn, QPoint(840, 315))
    
    rotate_180_btn = DraggableButton("180°")
    rotate_180_btn.set_style('info')
    rotate_180_btn.resize(60, 30)
    drop_zone.add_widget(rotate_180_btn, QPoint(910, 315))
    
    # Contrôles de retournement
    flip_label = DraggableLabel("Retournement:")
    flip_label.set_font_size(12)
    flip_label.set_font_bold(True)
    drop_zone.add_widget(flip_label, QPoint(770, 360))
    
    flip_h_btn = DraggableButton("⟷ Horizontal")
    flip_h_btn.set_style('warning')
    drop_zone.add_widget(flip_h_btn, QPoint(770, 385))
    
    flip_v_btn = DraggableButton("⟶ Vertical")
    flip_v_btn.set_style('warning')
    drop_zone.add_widget(flip_v_btn, QPoint(890, 385))
    
    # Section 4: Modes d'affichage
    display_title = DraggableLabel("Modes d'Affichage")
    display_title.set_style_preset('subtitle')
    display_title.set_font_size(16)
    drop_zone.add_widget(display_title, QPoint(750, 430))
    
    # Boutons de mode d'affichage
    mode_keep_btn = DraggableButton("Conserver Proportions")
    mode_keep_btn.set_style('success')
    drop_zone.add_widget(mode_keep_btn, QPoint(770, 470))
    
    mode_ignore_btn = DraggableButton("Ignorer Proportions")
    mode_ignore_btn.set_style('secondary')
    drop_zone.add_widget(mode_ignore_btn, QPoint(770, 510))
    
    mode_expand_btn = DraggableButton("Étendre")
    mode_expand_btn.set_style('info')
    drop_zone.add_widget(mode_expand_btn, QPoint(770, 550))
    
    # Section 5: Informations de l'image
    info_title = DraggableLabel("Informations de l'Image")
    info_title.set_style_preset('subtitle')
    info_title.set_font_size(16)
    drop_zone.add_widget(info_title, QPoint(750, 590))
    
    # Zone d'affichage des informations
    image_info_display = DraggableLabel("Sélectionnez une image pour voir ses informations")
    image_info_display.resize(350, 120)
    image_info_display.set_background_color('#f8f9fa')
    image_info_display.set_font_size(11)
    image_info_display.set_word_wrap(True)
    drop_zone.add_widget(image_info_display, QPoint(770, 630))
    
    # Section 6: Actions de sauvegarde
    save_title = DraggableLabel("Sauvegarde")
    save_title.set_style_preset('subtitle')
    save_title.set_font_size(16)
    drop_zone.add_widget(save_title, QPoint(750, 770))
    
    save_current_btn = DraggableButton("Sauvegarder Image")
    save_current_btn.set_style('success')
    drop_zone.add_widget(save_current_btn, QPoint(770, 810))
    
    save_all_btn = DraggableButton("Sauvegarder Tout")
    save_all_btn.set_style('primary')
    drop_zone.add_widget(save_all_btn, QPoint(900, 810))
    
    # Section 7: Galerie en mode miniatures
    thumbs_title = DraggableLabel("Mode Miniatures")
    thumbs_title.set_style_preset('subtitle')
    thumbs_title.set_font_size(16)
    drop_zone.add_widget(thumbs_title, QPoint(50, 540))
    
    # Zone de miniatures
    thumbnails_area = DraggableLabel("Zone des miniatures (sera peuplée automatiquement)")
    thumbnails_area.resize(650, 100)
    thumbnails_area.set_background_color('#e9ecef')
    thumbnails_area.set_alignment('center')
    drop_zone.add_widget(thumbnails_area, QPoint(70, 580))
    
    # État du système
    gallery_state = {
        'selected_slot': None,
        'loaded_images': 0,
        'last_action': 'Initialisation'
    }
    
    # Fonctions utilitaires
    def update_slot_selection(slot_index):
        """Mettre à jour la sélection de slot"""
        gallery_state['selected_slot'] = slot_index
        if slot_index is not None:
            current_slot_label.set_text(f"Slot {slot_index + 1}")
            current_slot_label.set_color('#27ae60')
            
            # Mettre à jour les informations de l'image
            slot = image_slots[slot_index]
            if slot['has_image']:
                update_image_info(slot)
            else:
                image_info_display.set_text("Slot vide - Chargez une image")
        else:
            current_slot_label.set_text("Aucun")
            current_slot_label.set_color('#e74c3c')
            image_info_display.set_text("Sélectionnez une image pour voir ses informations")
    
    def update_image_info(slot):
        """Mettre à jour l'affichage des informations d'image"""
        if not slot['has_image']:
            return
            
        img_info = slot['widget'].get_image_info()
        transformations = slot['transformations']
        
        info_text = f"""📷 Informations de l'Image:
• Fichier: {os.path.basename(slot['original_path']) if slot['original_path'] else 'Inconnu'}
• Dimensions: {img_info.get('width', 0)} x {img_info.get('height', 0)} pixels
• Format: {img_info.get('format', 'Inconnu')}
• Taille: {img_info.get('size_bytes', 0)} bytes

🔄 Transformations:
• Rotation: {transformations['rotation']}°
• Retournement H: {'Oui' if transformations['flipped_h'] else 'Non'}
• Retournement V: {'Oui' if transformations['flipped_v'] else 'Non'}
• Mode d'affichage: {transformations['scale_mode']}"""
        
        image_info_display.set_text(info_text)
        
        # Mettre à jour le label d'info du slot
        filename = os.path.basename(slot['original_path']) if slot['original_path'] else 'Image'
        slot['info_label'].set_text(f"Slot {slot['index']+1}: {filename}")
    
    def update_thumbnails():
        """Mettre à jour la zone des miniatures"""
        loaded_count = sum(1 for slot in image_slots if slot['has_image'])
        if loaded_count == 0:
            thumbnails_area.set_text("Aucune image chargée")
        else:
            thumbnails_area.set_text(f"📸 {loaded_count} image(s) chargée(s) - Cliquez sur les images pour les sélectionner")
    
    # Fonctions d'action
    def load_single_image():
        """Charger une seule image"""
        # Trouver le premier slot vide
        empty_slot = None
        for slot in image_slots:
            if not slot['has_image']:
                empty_slot = slot
                break
        
        if not empty_slot:
            QMessageBox.warning(window, "Galerie Pleine", "Tous les slots sont occupés. Effacez une image d'abord.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            window, "Charger une image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Tous les fichiers (*)"
        )
        
        if file_path:
            success = empty_slot['widget'].load_image(file_path)
            if success:
                empty_slot['has_image'] = True
                empty_slot['original_path'] = file_path
                gallery_state['loaded_images'] += 1
                
                update_slot_selection(empty_slot['index'])
                update_thumbnails()
                
                print(f"📁 Image chargée: {os.path.basename(file_path)} dans slot {empty_slot['index']+1}")
            else:
                QMessageBox.warning(window, "Erreur", f"Impossible de charger l'image: {file_path}")
    
    def load_multiple_images():
        """Charger plusieurs images"""
        # Compter les slots vides
        empty_slots = [slot for slot in image_slots if not slot['has_image']]
        
        if not empty_slots:
            QMessageBox.warning(window, "Galerie Pleine", "Aucun slot disponible.")
            return
        
        file_paths, _ = QFileDialog.getOpenFileNames(
            window, f"Charger jusqu'à {len(empty_slots)} images", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Tous les fichiers (*)"
        )
        
        if file_paths:
            loaded_count = 0
            for i, file_path in enumerate(file_paths[:len(empty_slots)]):
                slot = empty_slots[i]
                success = slot['widget'].load_image(file_path)
                if success:
                    slot['has_image'] = True
                    slot['original_path'] = file_path
                    loaded_count += 1
                    
                    filename = os.path.basename(file_path)
                    slot['info_label'].set_text(f"Slot {slot['index']+1}: {filename}")
            
            gallery_state['loaded_images'] += loaded_count
            update_thumbnails()
            
            if loaded_count > 0:
                update_slot_selection(empty_slots[0]['index'])
            
            print(f"📁 {loaded_count} images chargées sur {len(file_paths)} sélectionnées")
    
    def clear_all_images():
        """Effacer toutes les images"""
        reply = QMessageBox.question(
            window, 'Effacer Toutes les Images', 
            'Êtes-vous sûr de vouloir effacer toutes les images?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for slot in image_slots:
                slot['widget'].load_image("")  # Charger une image vide
                slot['has_image'] = False
                slot['original_path'] = None
                slot['info_label'].set_text(f"Slot {slot['index']+1}: Vide")
                # Reset transformations
                slot['transformations'] = {
                    'rotation': 0,
                    'flipped_h': False,
                    'flipped_v': False,
                    'scale_mode': 'keep_aspect_ratio'
                }
            
            gallery_state['loaded_images'] = 0
            update_slot_selection(None)
            update_thumbnails()
            
            print("🧹 Toutes les images ont été effacées")
    
    def apply_transformation(transform_type, value=None):
        """Appliquer une transformation à l'image sélectionnée"""
        if gallery_state['selected_slot'] is None:
            QMessageBox.information(window, "Aucune Sélection", "Sélectionnez d'abord une image.")
            return
        
        slot = image_slots[gallery_state['selected_slot']]
        if not slot['has_image']:
            QMessageBox.information(window, "Slot Vide", "Ce slot ne contient pas d'image.")
            return
        
        widget = slot['widget']
        transformations = slot['transformations']
        
        if transform_type == 'rotate_left':
            widget.rotate_image(-90)
            transformations['rotation'] = (transformations['rotation'] - 90) % 360
            print("🔄 Rotation -90° appliquée")
            
        elif transform_type == 'rotate_right':
            widget.rotate_image(90)
            transformations['rotation'] = (transformations['rotation'] + 90) % 360
            print("🔄 Rotation +90° appliquée")
            
        elif transform_type == 'rotate_180':
            widget.rotate_image(180)
            transformations['rotation'] = (transformations['rotation'] + 180) % 360
            print("🔄 Rotation 180° appliquée")
            
        elif transform_type == 'flip_horizontal':
            widget.flip_horizontal()
            transformations['flipped_h'] = not transformations['flipped_h']
            print("↔️ Retournement horizontal appliqué")
            
        elif transform_type == 'flip_vertical':
            widget.flip_vertical()
            transformations['flipped_v'] = not transformations['flipped_v']
            print("↕️ Retournement vertical appliqué")
            
        elif transform_type in ['keep_aspect_ratio', 'ignore_aspect_ratio', 'keep_aspect_ratio_by_expanding']:
            widget.set_scale_mode(transform_type)
            transformations['scale_mode'] = transform_type
            print(f"📐 Mode d'affichage changé: {transform_type}")
        
        # Mettre à jour les informations
        update_image_info(slot)
        gallery_state['last_action'] = f"Transformation: {transform_type}"
    
    def save_current_image():
        """Sauvegarder l'image actuelle"""
        if gallery_state['selected_slot'] is None:
            QMessageBox.information(window, "Aucune Sélection", "Sélectionnez d'abord une image.")
            return
        
        slot = image_slots[gallery_state['selected_slot']]
        if not slot['has_image']:
            QMessageBox.information(window, "Slot Vide", "Ce slot ne contient pas d'image.")
            return
        
        # Suggérer un nom de fichier basé sur l'original
        if slot['original_path']:
            base_name = os.path.splitext(os.path.basename(slot['original_path']))[0]
            suggested_name = f"{base_name}_modifie.jpg"
        else:
            suggested_name = f"image_slot_{slot['index']+1}.jpg"
        
        file_path, _ = QFileDialog.getSaveFileName(
            window, "Sauvegarder l'image", suggested_name,
            "JPEG (*.jpg);;PNG (*.png);;Tous les fichiers (*)"
        )
        
        if file_path:
            success = slot['widget'].save_image(file_path, quality=95)
            if success:
                QMessageBox.information(window, "Succès", f"Image sauvegardée: {os.path.basename(file_path)}")
                print(f"💾 Image sauvegardée: {file_path}")
            else:
                QMessageBox.warning(window, "Erreur", "Impossible de sauvegarder l'image.")
    
    def save_all_images():
        """Sauvegarder toutes les images modifiées"""
        images_with_content = [slot for slot in image_slots if slot['has_image']]
        
        if not images_with_content:
            QMessageBox.information(window, "Aucune Image", "Aucune image à sauvegarder.")
            return
        
        # Demander le dossier de destination
        directory = QFileDialog.getExistingDirectory(window, "Choisir le dossier de sauvegarde")
        
        if directory:
            saved_count = 0
            for slot in images_with_content:
                if slot['original_path']:
                    base_name = os.path.splitext(os.path.basename(slot['original_path']))[0]
                    filename = f"{base_name}_modifie_slot_{slot['index']+1}.jpg"
                else:
                    filename = f"image_slot_{slot['index']+1}.jpg"
                
                file_path = os.path.join(directory, filename)
                success = slot['widget'].save_image(file_path, quality=95)
                if success:
                    saved_count += 1
            
            QMessageBox.information(window, "Sauvegarde Terminée", 
                                  f"{saved_count}/{len(images_with_content)} images sauvegardées dans:\n{directory}")
            print(f"💾 Sauvegarde en lot: {saved_count} images dans {directory}")
    
    # Connexion des événements
    
    # Boutons de chargement
    load_single_btn.button_clicked.connect(lambda _: load_single_image())
    load_multiple_btn.button_clicked.connect(lambda _: load_multiple_images())
    clear_all_btn.button_clicked.connect(lambda _: clear_all_images())
    
    # Boutons de transformation
    rotate_left_btn.button_clicked.connect(lambda _: apply_transformation('rotate_left'))
    rotate_right_btn.button_clicked.connect(lambda _: apply_transformation('rotate_right'))
    rotate_180_btn.button_clicked.connect(lambda _: apply_transformation('rotate_180'))
    flip_h_btn.button_clicked.connect(lambda _: apply_transformation('flip_horizontal'))
    flip_v_btn.button_clicked.connect(lambda _: apply_transformation('flip_vertical'))
    
    # Boutons de mode d'affichage
    mode_keep_btn.button_clicked.connect(lambda _: apply_transformation('keep_aspect_ratio'))
    mode_ignore_btn.button_clicked.connect(lambda _: apply_transformation('ignore_aspect_ratio'))
    mode_expand_btn.button_clicked.connect(lambda _: apply_transformation('keep_aspect_ratio_by_expanding'))
    
    # Boutons de sauvegarde
    save_current_btn.button_clicked.connect(lambda _: save_current_image())
    save_all_btn.button_clicked.connect(lambda _: save_all_images())
    
    # Sélection d'images par clic
    for slot in image_slots:
        slot['widget'].image_clicked.connect(
            lambda widget_id, idx=slot['index']: update_slot_selection(idx)
        )
    
    # Instructions
    instructions = DraggableLabel(
        "🖼️ Galerie d'Images Complète:\n"
        "• Chargez des images avec les boutons de chargement\n"
        "• Cliquez sur une image pour la sélectionner\n"
        "• Utilisez les contrôles de transformation\n"
        "• Sauvegardez vos modifications\n"
        "• Toutes les images sont redimensionnables par glisser-déposer"
    )
    instructions.set_style_preset('info')
    instructions.set_font_size(11)
    instructions.resize(500, 100)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 700))
    
    # Initialiser l'affichage
    update_thumbnails()
    
    # Afficher la fenêtre
    window.show()
    
    print(f"📱 Galerie d'images lancée avec {len(image_slots)} slots disponibles")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)