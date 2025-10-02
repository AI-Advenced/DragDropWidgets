#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constructeur de formulaires visuels

Ce fichier démontre :
- Création de formulaires par glisser-déposer
- Palette d'éléments de formulaire
- Prévisualisation de formulaires
- Export de formulaires en HTML/CSS
- Validation de formulaires

Exécution :
    python form_builder.py
"""

import sys
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMessageBox, QInputDialog
from dragdropwidgets import create_app, DraggableButton, DraggableLabel
from dragdropwidgets.widgets.custom import DraggableTextEdit, DraggableSlider


def main():
    """Constructeur de formulaires principal"""
    app, window, drop_zone = create_app("Constructeur de Formulaires", (1400, 900))
    
    print("📝 Constructeur de formulaires visuels")
    print("=" * 50)
    
    drop_zone.set_grid_visible(True)
    drop_zone.grid_size = 20
    
    # Titre
    title = DraggableLabel("Constructeur de Formulaires Visuels")
    title.set_style_preset('title')
    title.set_font_size(22)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # Section palette d'outils
    palette_title = DraggableLabel("Palette d'Éléments")
    palette_title.set_style_preset('subtitle')
    palette_title.set_font_size(16)
    drop_zone.add_widget(palette_title, QPoint(50, 80))
    
    # Éléments de formulaire disponibles
    form_elements = [
        ("📝 Champ Texte", lambda: create_text_field()),
        ("📧 Email", lambda: create_email_field()),
        ("🔢 Nombre", lambda: create_number_field()),
        ("📅 Date", lambda: create_date_field()),
        ("☑️ Checkbox", lambda: create_checkbox()),
        ("⚪ Radio", lambda: create_radio_button()),
        ("📋 Select", lambda: create_select_field()),
        ("📄 Textarea", lambda: create_textarea()),
        ("🎚️ Slider", lambda: create_slider_field()),
        ("📊 Progress", lambda: create_progress_field()),
        ("🏷️ Label", lambda: create_label_field()),
        ("✅ Bouton Submit", lambda: create_submit_button()),
        ("❌ Bouton Reset", lambda: create_reset_button()),
    ]
    
    # État du formulaire
    form_state = {
        'elements': [],
        'form_name': 'MonFormulaire',
        'next_y': 120
    }
    
    # Créer les boutons de la palette
    for i, (name, creator) in enumerate(form_elements):
        btn = DraggableButton(name)
        btn.set_style('info')
        btn.resize(130, 30)
        
        col = i % 2
        row = i // 2
        x_pos = 70 + col * 140
        y_pos = 120 + row * 40
        
        drop_zone.add_widget(btn, QPoint(x_pos, y_pos))
        btn.button_clicked.connect(lambda _, c=creator: add_form_element(c()))
    
    # Zone de formulaire
    form_area_title = DraggableLabel("Zone de Formulaire")
    form_area_title.set_style_preset('subtitle')
    form_area_title.set_font_size(16)
    drop_zone.add_widget(form_area_title, QPoint(400, 80))
    
    # Titre du formulaire
    form_title = DraggableLabel("MonFormulaire")
    form_title.set_style_preset('title')
    form_title.set_font_size(18)
    drop_zone.add_widget(form_title, QPoint(420, 120))
    
    # Contrôles
    controls_title = DraggableLabel("Contrôles")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(1000, 80))
    
    preview_btn = DraggableButton("Prévisualiser")
    preview_btn.set_style('primary')
    drop_zone.add_widget(preview_btn, QPoint(1020, 120))
    
    export_btn = DraggableButton("Exporter HTML")
    export_btn.set_style('success')
    drop_zone.add_widget(export_btn, QPoint(1020, 160))
    
    clear_btn = DraggableButton("Effacer Tout")
    clear_btn.set_style('danger')
    drop_zone.add_widget(clear_btn, QPoint(1020, 200))
    
    rename_btn = DraggableButton("Renommer")
    rename_btn.set_style('secondary')
    drop_zone.add_widget(rename_btn, QPoint(1020, 240))
    
    # Info sur le formulaire
    form_info = DraggableLabel("Éléments: 0\nDernier ajout: Aucun")
    form_info.resize(200, 60)
    form_info.set_background_color("#f0f8ff")
    drop_zone.add_widget(form_info, QPoint(1020, 290))
    
    # Fonctions de création d'éléments
    def create_text_field():
        field = DraggableLabel("📝 Nom:")
        field.set_background_color("#ffffff")
        field.resize(200, 25)
        return field
    
    def create_email_field():
        field = DraggableLabel("📧 Email:")
        field.set_background_color("#fff5f5")
        field.resize(200, 25)
        return field
    
    def create_number_field():
        field = DraggableLabel("🔢 Âge:")
        field.set_background_color("#f5fff5")
        field.resize(200, 25)
        return field
    
    def create_date_field():
        field = DraggableLabel("📅 Date:")
        field.set_background_color("#f5f5ff")
        field.resize(200, 25)
        return field
    
    def create_checkbox():
        field = DraggableLabel("☑️ J'accepte les conditions")
        field.set_background_color("#fffacd")
        field.resize(220, 25)
        return field
    
    def create_radio_button():
        field = DraggableLabel("⚪ Option A  ⚪ Option B")
        field.set_background_color("#f0e68c")
        field.resize(200, 25)
        return field
    
    def create_select_field():
        field = DraggableLabel("📋 Pays: [Sélectionner]")
        field.set_background_color("#e0e0e0")
        field.resize(200, 25)
        return field
    
    def create_textarea():
        field = DraggableTextEdit("Commentaires...")
        field.resize(250, 60)
        return field
    
    def create_slider_field():
        field = DraggableSlider(50)
        field.resize(200, 30)
        return field
    
    def create_progress_field():
        from dragdropwidgets.widgets.custom import DraggableProgressBar
        field = DraggableProgressBar(0)
        field.resize(200, 25)
        return field
    
    def create_label_field():
        field = DraggableLabel("🏷️ Nouveau Label")
        field.set_style_preset('body')
        return field
    
    def create_submit_button():
        btn = DraggableButton("✅ Envoyer")
        btn.set_style('success')
        return btn
    
    def create_reset_button():
        btn = DraggableButton("❌ Effacer")
        btn.set_style('warning')
        return btn
    
    def add_form_element(element):
        """Ajouter un élément au formulaire"""
        # Placer dans la zone de formulaire
        form_x = 420
        form_y = form_state['next_y']
        
        drop_zone.add_widget(element, QPoint(form_x, form_y))
        form_state['elements'].append(element)
        form_state['next_y'] += 50
        
        # Mettre à jour les infos
        update_form_info()
        print(f"➕ Élément ajouté: {element.__class__.__name__}")
    
    def update_form_info():
        """Mettre à jour les informations du formulaire"""
        count = len(form_state['elements'])
        if form_state['elements']:
            last_element = form_state['elements'][-1].__class__.__name__
        else:
            last_element = "Aucun"
        
        info_text = f"Éléments: {count}\nDernier ajout: {last_element}"
        form_info.set_text(info_text)
    
    def preview_form():
        """Prévisualiser le formulaire"""
        if not form_state['elements']:
            QMessageBox.information(window, "Formulaire Vide", "Ajoutez des éléments au formulaire d'abord.")
            return
        
        preview_text = f"Aperçu du formulaire '{form_state['form_name']}':\n\n"
        
        for i, element in enumerate(form_state['elements']):
            if hasattr(element, 'get_text'):
                text = element.get_text()
            else:
                text = f"Élément {element.__class__.__name__}"
            preview_text += f"{i+1}. {text}\n"
        
        QMessageBox.information(window, "Aperçu du Formulaire", preview_text)
    
    def export_html():
        """Exporter le formulaire en HTML"""
        if not form_state['elements']:
            QMessageBox.information(window, "Formulaire Vide", "Ajoutez des éléments au formulaire d'abord.")
            return
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{form_state['form_name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .form-container {{ max-width: 600px; }}
        .form-element {{ margin: 10px 0; }}
        input, textarea, select {{ padding: 8px; width: 200px; }}
        button {{ padding: 10px 20px; margin: 5px; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h2>{form_state['form_name']}</h2>
        <form>
"""
        
        for element in form_state['elements']:
            if isinstance(element, DraggableLabel):
                text = element.get_text()
                if "📝" in text:
                    html += f'            <div class="form-element"><label>{text}</label><br><input type="text" name="text_field"></div>\n'
                elif "📧" in text:
                    html += f'            <div class="form-element"><label>{text}</label><br><input type="email" name="email_field"></div>\n'
                elif "🔢" in text:
                    html += f'            <div class="form-element"><label>{text}</label><br><input type="number" name="number_field"></div>\n'
                elif "☑️" in text:
                    html += f'            <div class="form-element"><input type="checkbox" name="checkbox_field"> {text}</div>\n'
                else:
                    html += f'            <div class="form-element"><label>{text}</label></div>\n'
            elif isinstance(element, DraggableTextEdit):
                html += f'            <div class="form-element"><label>Commentaires:</label><br><textarea name="textarea_field">{element.get_text()}</textarea></div>\n'
            elif isinstance(element, DraggableButton):
                text = element.get_text()
                if "Envoyer" in text:
                    html += f'            <div class="form-element"><button type="submit">{text}</button></div>\n'
                else:
                    html += f'            <div class="form-element"><button type="button">{text}</button></div>\n'
        
        html += """        </form>
    </div>
</body>
</html>"""
        
        # Sauvegarder le fichier
        filename = f"{form_state['form_name'].lower().replace(' ', '_')}.html"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            QMessageBox.information(window, "Export Réussi", f"Formulaire exporté: {filename}")
            print(f"📄 Formulaire exporté: {filename}")
        except Exception as e:
            QMessageBox.warning(window, "Erreur Export", f"Erreur: {e}")
    
    def clear_form():
        """Effacer tous les éléments du formulaire"""
        reply = QMessageBox.question(
            window, 'Effacer Formulaire',
            'Êtes-vous sûr de vouloir effacer tous les éléments?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for element in form_state['elements']:
                drop_zone.remove_widget(element.widget_id)
            
            form_state['elements'].clear()
            form_state['next_y'] = 160
            update_form_info()
            print("🧹 Formulaire effacé")
    
    def rename_form():
        """Renommer le formulaire"""
        new_name, ok = QInputDialog.getText(
            window, 'Renommer Formulaire',
            'Nouveau nom du formulaire:', text=form_state['form_name']
        )
        
        if ok and new_name:
            form_state['form_name'] = new_name
            form_title.set_text(new_name)
            print(f"✏️ Formulaire renommé: {new_name}")
    
    # Connexions
    preview_btn.button_clicked.connect(lambda _: preview_form())
    export_btn.button_clicked.connect(lambda _: export_html())
    clear_btn.button_clicked.connect(lambda _: clear_form())
    rename_btn.button_clicked.connect(lambda _: rename_form())
    
    # Instructions
    instructions = DraggableLabel(
        "📝 Constructeur de Formulaires:\n"
        "• Cliquez sur les éléments de la palette pour les ajouter\n"
        "• Réorganisez les éléments par glisser-déposer\n"
        "• Prévisualisez et exportez votre formulaire\n"
        "• Le formulaire peut être sauvegardé en HTML fonctionnel"
    )
    instructions.set_style_preset('info')
    instructions.resize(500, 80)
    instructions.set_word_wrap(True)
    drop_zone.add_widget(instructions, QPoint(50, 700))
    
    window.show()
    print(f"📱 Constructeur de formulaires lancé avec {len(form_elements)} éléments disponibles")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)