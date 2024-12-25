"""
按钮类
"""
import pygame
from typing import Callable, Tuple

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, color: Tuple[int, int, int], 
                 hover_color: Tuple[int, int, int], 
                 action: Callable):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.action = action
        self.is_hovered = False
        
        # 创建字体
        self.font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 32)
        
    def draw(self, screen: pygame.Surface):
        """绘制按钮"""
        # 绘制按钮背景
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=15)
        
        # 绘制按钮文本
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """处理按钮事件"""
        if event.type == pygame.MOUSEMOTION:
            # 检查鼠标悬停
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查点击
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False
        
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """检查按钮是否被点击"""
        if self.rect.collidepoint(pos):
            self.action()
            return True
        return False 