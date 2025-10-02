#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jeu simple avec widgets - Cliquer pour scorer

Ce fichier démontre :
- Jeu interactif avec widgets
- Système de score
- Timer de jeu
- Animations et effets
- Gestion des high scores

Exécution :
    python widget_game.py
"""

import sys
import random
from datetime import datetime
from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QMessageBox, QInputDialog
from dragdropwidgets import create_app, DraggableButton, DraggableLabel


def main():
    """Jeu de widgets principal"""
    app, window, drop_zone = create_app("Widget Game - Cliquez pour Scorer!", (1000, 800))
    
    print("🎮 Jeu de widgets interactif")
    print("=" * 50)
    
    drop_zone.set_grid_visible(False)  # Pas de grille pour le jeu
    
    # Titre
    title = DraggableLabel("🎮 Widget Game - Attrapez les Cibles!")
    title.set_style_preset('title')
    title.set_font_size(20)
    drop_zone.add_widget(title, QPoint(50, 25))
    
    # État du jeu
    game_state = {
        'active': False,
        'score': 0,
        'time_left': 30,
        'targets_hit': 0,
        'targets_missed': 0,
        'difficulty': 'Normal',
        'high_scores': [],
        'current_targets': []
    }
    
    # Affichage du score
    score_label = DraggableLabel("Score: 0")
    score_label.set_style_preset('success')
    score_label.set_font_size(18)
    score_label.set_font_bold(True)
    drop_zone.add_widget(score_label, QPoint(300, 25))
    
    # Timer
    timer_label = DraggableLabel("Temps: 30s")
    timer_label.set_style_preset('warning')
    timer_label.set_font_size(16)
    timer_label.set_font_bold(True)
    drop_zone.add_widget(timer_label, QPoint(500, 25))
    
    # Statistiques
    stats_label = DraggableLabel("Cibles: 0 | Ratées: 0")
    stats_label.set_font_size(12)
    drop_zone.add_widget(stats_label, QPoint(700, 30))
    
    # Contrôles du jeu
    controls_title = DraggableLabel("Contrôles")
    controls_title.set_style_preset('subtitle')
    controls_title.set_font_size(16)
    drop_zone.add_widget(controls_title, QPoint(50, 80))
    
    start_btn = DraggableButton("🎯 Commencer le Jeu")
    start_btn.set_style('success')
    start_btn.resize(150, 40)
    drop_zone.add_widget(start_btn, QPoint(70, 120))
    
    stop_btn = DraggableButton("⏹️ Arrêter")
    stop_btn.set_style('danger')
    drop_zone.add_widget(stop_btn, QPoint(240, 120))
    
    # Difficulté
    difficulty_label = DraggableLabel("Difficulté:")
    difficulty_label.set_font_size(12)
    drop_zone.add_widget(difficulty_label, QPoint(70, 170))
    
    easy_btn = DraggableButton("Facile")
    easy_btn.set_style('info')
    easy_btn.resize(80, 30)
    drop_zone.add_widget(easy_btn, QPoint(70, 190))
    
    normal_btn = DraggableButton("Normal")
    normal_btn.set_style('primary')
    normal_btn.resize(80, 30)
    drop_zone.add_widget(normal_btn, QPoint(160, 190))
    
    hard_btn = DraggableButton("Difficile")
    hard_btn.set_style('danger')
    hard_btn.resize(80, 30)
    drop_zone.add_widget(hard_btn, QPoint(250, 190))
    
    # Statut actuel
    status_label = DraggableLabel("Prêt à jouer!")
    status_label.set_style_preset('info')
    status_label.set_font_size(14)
    drop_zone.add_widget(status_label, QPoint(70, 240))
    
    # High Scores
    highscores_title = DraggableLabel("🏆 Meilleurs Scores")
    highscores_title.set_style_preset('subtitle')
    highscores_title.set_font_size(16)
    drop_zone.add_widget(highscores_title, QPoint(500, 80))
    
    highscores_display = DraggableLabel("1. Aucun score\n2. ---\n3. ---\n4. ---\n5. ---")
    highscores_display.resize(300, 120)
    highscores_display.set_background_color("#f8f9fa")
    highscores_display.set_font_size(11)
    drop_zone.add_widget(highscores_display, QPoint(520, 120))
    
    # Zone de jeu
    game_area_title = DraggableLabel("🎯 Zone de Jeu")
    game_area_title.set_style_preset('subtitle')
    game_area_title.set_font_size(16)
    drop_zone.add_widget(game_area_title, QPoint(50, 300))
    
    # Instructions
    instructions = DraggableLabel(
        "🎮 Comment jouer:\n"
        "• Cliquez sur 'Commencer le Jeu' pour débuter\n"
        "• Cliquez rapidement sur les cibles qui apparaissent\n"
        "• Plus vous êtes rapide, plus vous gagnez de points\n"
        "• Évitez de manquer les cibles!\n"
        "• Vous avez 30 secondes pour faire le meilleur score"
    )
    instructions.set_style_preset('info')
    instructions.resize(400, 120)
    instructions.set_word_wrap(True)
    instructions.set_font_size(10)
    drop_zone.add_widget(instructions, QPoint(50, 600))
    
    # Timers du jeu
    game_timer = QTimer()  # Timer principal du jeu
    spawn_timer = QTimer()  # Timer pour créer des cibles
    
    def update_display():
        """Mettre à jour l'affichage du jeu"""
        score_label.set_text(f"Score: {game_state['score']}")
        timer_label.set_text(f"Temps: {game_state['time_left']}s")
        stats_label.set_text(f"Cibles: {game_state['targets_hit']} | Ratées: {game_state['targets_missed']}")
        
        # Changer la couleur du timer selon le temps restant
        if game_state['time_left'] <= 5:
            timer_label.set_color("#e74c3c")  # Rouge
        elif game_state['time_left'] <= 10:
            timer_label.set_color("#f39c12")  # Orange
        else:
            timer_label.set_color("#27ae60")  # Vert
    
    def create_target():
        """Créer une nouvelle cible"""
        if not game_state['active']:
            return
        
        # Créer une cible aléatoire
        target_texts = ["🎯", "⭐", "💎", "🔥", "⚡", "💰", "🎁", "🌟"]
        target_styles = ['success', 'warning', 'info', 'primary']
        
        target = DraggableButton(random.choice(target_texts))
        target.set_style(random.choice(target_styles))
        target.resize(60, 40)
        
        # Position aléatoire dans la zone de jeu
        x = random.randint(100, 800)
        y = random.randint(350, 550)
        drop_zone.add_widget(target, QPoint(x, y))
        
        # Points selon la difficulté et le type
        base_points = 10
        if game_state['difficulty'] == 'Facile':
            points = base_points
            lifetime = 3000  # 3 secondes
        elif game_state['difficulty'] == 'Normal':
            points = base_points * 2
            lifetime = 2000  # 2 secondes
        else:  # Difficile
            points = base_points * 3
            lifetime = 1200  # 1.2 secondes
        
        # Bonus pour certaines cibles
        text = target.get_text()
        if text in ["💎", "💰"]:
            points *= 2
        elif text in ["⚡", "🔥"]:
            points = int(points * 1.5)
        
        # Stocker les infos de la cible
        target.game_points = points
        target.creation_time = datetime.now()
        
        # Connecter l'événement de clic
        def on_target_hit(widget_id, target_widget=target):
            hit_target(target_widget)
        
        target.button_clicked.connect(on_target_hit)
        
        # Ajouter à la liste des cibles actives
        game_state['current_targets'].append(target)
        
        # Programmer la disparition automatique
        QTimer.singleShot(lifetime, lambda: miss_target(target))
    
    def hit_target(target):
        """Cible touchée"""
        if target not in game_state['current_targets']:
            return  # Déjà supprimée
        
        # Calculer le bonus de rapidité
        time_bonus = 1.0
        if hasattr(target, 'creation_time'):
            reaction_time = (datetime.now() - target.creation_time).total_seconds()
            if reaction_time < 0.5:
                time_bonus = 2.0  # Super rapide!
            elif reaction_time < 1.0:
                time_bonus = 1.5  # Rapide
        
        # Ajouter les points
        points_earned = int(target.game_points * time_bonus)
        game_state['score'] += points_earned
        game_state['targets_hit'] += 1
        
        # Effet visuel temporaire
        target.set_text(f"+{points_earned}")
        target.set_style('success')
        
        # Supprimer la cible après un court délai
        QTimer.singleShot(200, lambda: remove_target(target))
        
        print(f"🎯 Cible touchée! +{points_earned} points (bonus x{time_bonus:.1f})")
    
    def miss_target(target):
        """Cible ratée (disparition automatique)"""
        if target not in game_state['current_targets']:
            return  # Déjà supprimée
        
        game_state['targets_missed'] += 1
        
        # Effet visuel de ratage
        target.set_text("💥")
        target.set_style('danger')
        
        # Supprimer après animation
        QTimer.singleShot(300, lambda: remove_target(target))
        
        print("💥 Cible ratée!")
    
    def remove_target(target):
        """Supprimer une cible du jeu"""
        if target in game_state['current_targets']:
            game_state['current_targets'].remove(target)
            drop_zone.remove_widget(target.widget_id)
    
    def game_tick():
        """Tick principal du jeu (chaque seconde)"""
        if not game_state['active']:
            return
        
        game_state['time_left'] -= 1
        update_display()
        
        if game_state['time_left'] <= 0:
            end_game()
    
    def spawn_target():
        """Créer une cible selon la difficulté"""
        if not game_state['active']:
            return
        
        # Limiter le nombre de cibles simultanées
        max_targets = 3 if game_state['difficulty'] == 'Facile' else 5 if game_state['difficulty'] == 'Normal' else 7
        
        if len(game_state['current_targets']) < max_targets:
            create_target()
    
    def start_game():
        """Démarrer le jeu"""
        if game_state['active']:
            return
        
        # Réinitialiser l'état
        game_state.update({
            'active': True,
            'score': 0,
            'time_left': 30,
            'targets_hit': 0,
            'targets_missed': 0,
            'current_targets': []
        })
        
        # Effacer les cibles existantes
        for target in game_state['current_targets'][:]:
            remove_target(target)
        
        # Configurer les timers selon la difficulté
        if game_state['difficulty'] == 'Facile':
            spawn_interval = 1500  # 1.5 secondes
        elif game_state['difficulty'] == 'Normal':
            spawn_interval = 1000  # 1 seconde
        else:  # Difficile
            spawn_interval = 700   # 0.7 secondes
        
        # Démarrer les timers
        game_timer.start(1000)  # Tick chaque seconde
        spawn_timer.start(spawn_interval)
        
        status_label.set_text(f"🎮 Jeu en cours - Difficulté: {game_state['difficulty']}")
        status_label.set_style_preset('success')
        
        update_display()
        print(f"🎮 Jeu démarré - Difficulté: {game_state['difficulty']}")
    
    def stop_game():
        """Arrêter le jeu"""
        if not game_state['active']:
            return
        
        end_game()
    
    def end_game():
        """Terminer le jeu"""
        game_state['active'] = False
        game_timer.stop()
        spawn_timer.stop()
        
        # Effacer toutes les cibles
        for target in game_state['current_targets'][:]:
            remove_target(target)
        
        final_score = game_state['score']
        accuracy = 0
        if game_state['targets_hit'] + game_state['targets_missed'] > 0:
            accuracy = (game_state['targets_hit'] / (game_state['targets_hit'] + game_state['targets_missed'])) * 100
        
        status_label.set_text(f"🏁 Jeu terminé! Score: {final_score} (Précision: {accuracy:.1f}%)")
        status_label.set_style_preset('info')
        
        # Vérifier si c'est un high score
        check_high_score(final_score)
        
        print(f"🏁 Jeu terminé - Score: {final_score}, Précision: {accuracy:.1f}%")
    
    def check_high_score(score):
        """Vérifier et enregistrer les high scores"""
        # Ajouter le score à la liste
        game_state['high_scores'].append(score)
        game_state['high_scores'].sort(reverse=True)
        game_state['high_scores'] = game_state['high_scores'][:5]  # Garder top 5
        
        # Mettre à jour l'affichage
        update_highscores_display()
        
        # Si c'est dans le top 5, féliciter
        if score in game_state['high_scores'][:5]:
            position = game_state['high_scores'].index(score) + 1
            if position == 1:
                QMessageBox.information(window, "🥇 Nouveau Record!", 
                                      f"Félicitations! Nouveau meilleur score: {score} points!")
            else:
                QMessageBox.information(window, f"🏆 Top {position}!", 
                                      f"Excellent! Vous êtes {position}ème avec {score} points!")
    
    def update_highscores_display():
        """Mettre à jour l'affichage des high scores"""
        if not game_state['high_scores']:
            highscores_display.set_text("1. Aucun score\n2. ---\n3. ---\n4. ---\n5. ---")
            return
        
        scores_text = ""
        for i in range(5):
            if i < len(game_state['high_scores']):
                score = game_state['high_scores'][i]
                scores_text += f"{i+1}. {score} points\n"
            else:
                scores_text += f"{i+1}. ---\n"
        
        highscores_display.set_text(scores_text.strip())
    
    def set_difficulty(level):
        """Définir le niveau de difficulté"""
        if game_state['active']:
            QMessageBox.warning(window, "Jeu en Cours", "Arrêtez le jeu avant de changer la difficulté.")
            return
        
        game_state['difficulty'] = level
        
        # Réinitialiser les styles des boutons
        easy_btn.set_style('info')
        normal_btn.set_style('primary')
        hard_btn.set_style('danger')
        
        # Mettre en évidence le niveau sélectionné
        if level == 'Facile':
            easy_btn.set_style('success')
        elif level == 'Normal':
            normal_btn.set_style('success')
        else:
            hard_btn.set_style('success')
        
        status_label.set_text(f"Difficulté changée: {level}")
        print(f"⚙️ Difficulté: {level}")
    
    # Connexions des événements
    start_btn.button_clicked.connect(lambda _: start_game())
    stop_btn.button_clicked.connect(lambda _: stop_game())
    easy_btn.button_clicked.connect(lambda _: set_difficulty('Facile'))
    normal_btn.button_clicked.connect(lambda _: set_difficulty('Normal'))
    hard_btn.button_clicked.connect(lambda _: set_difficulty('Difficile'))
    
    # Configurer les timers
    game_timer.timeout.connect(game_tick)
    spawn_timer.timeout.connect(spawn_target)
    
    # Initialiser l'affichage
    update_display()
    update_highscores_display()
    set_difficulty('Normal')  # Difficulté par défaut
    
    window.show()
    print("📱 Widget Game lancé - Prêt à jouer!")
    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)