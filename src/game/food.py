"""
食物类实现
"""
import random
from typing import Tuple
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import (
    CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
    LAYOUT
)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.spawn_time = 0
        
    def generate_position(self, snake_positions: list = None) -> Tuple[int, int]:
        """生成新的食物位置"""
        # 根据游戏区域计算可用格子
        min_x = 0
        max_x = (WINDOW_WIDTH - CELL_SIZE)
        min_y = int(LAYOUT["game_area"]["top"])
        max_y = int(LAYOUT["game_area"]["bottom"] - CELL_SIZE)
        
        while True:
            # 确保食物位置对齐网格
            x = random.randrange(min_x, max_x + 1, CELL_SIZE)
            y = random.randrange(min_y, max_y + 1, CELL_SIZE)
            position = (x, y)
            
            if snake_positions is None or position not in snake_positions:
                return position
                
    def respawn(self, snake_positions: list):
        """重新生成食物"""
        self.position = self.generate_position(snake_positions) 