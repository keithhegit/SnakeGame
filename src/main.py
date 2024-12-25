"""
游戏主入口
"""
import os
import sys
import pygame

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.screens import GameScreen
from src.ui.theme import ThemeManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Modern Snake Game")
        self.clock = pygame.time.Clock()
        self.theme_manager = ThemeManager()
        self.game_screen = GameScreen(self.screen, self.theme_manager)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.game_screen.handle_event(event)
            
            self.game_screen.update()
            self.game_screen.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run() 