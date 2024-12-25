"""
蛇类实现
"""
from typing import List, Tuple
import pygame
import sys
import os
import random
import time

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import (
    CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, 
    DIFFICULTY_SETTINGS, Difficulty, MOVE_DELAY,
    SCORE_SYSTEM, RESPAWN_SYSTEM, LAYOUT
)

class Snake:
    def __init__(self):
        self.speed = DIFFICULTY_SETTINGS[Difficulty.HARD]["speed"]
        self.wall_collision = DIFFICULTY_SETTINGS[Difficulty.HARD]["wall_collision"]
        self.lives = DIFFICULTY_SETTINGS[Difficulty.HARD]["lives"]
        self.move_delay = MOVE_DELAY[Difficulty.HARD]
        self.move_counter = 0
        self.combo_count = 0
        self.invincible = False
        self.invincible_timer = 0
        self.flash_timer = 0
        self.visible = True
        self.position = []  # 初始化位置列表
        self.direction = (CELL_SIZE, 0)  # 初始化方向
        self.length = 1  # 初始化长度
        self.score = 0  # 初始化分数
        self.difficulty = Difficulty.HARD  # 初始化难度
        self.find_safe_position()  # 最后设置安全位置
        
    def reset(self):
        """重置蛇的位置和状态"""
        self.direction = (CELL_SIZE, 0)
        self.length = 1
        self.score = 0
        self.combo_count = 0
        self.invincible = False
        self.invincible_timer = 0
        self.flash_timer = 0
        self.visible = True
        self.find_safe_position()
        
    def find_safe_position(self):
        """找到一个安全的重生位置"""
        game_area_top = int(LAYOUT["game_area"]["top"])
        game_area_bottom = int(LAYOUT["game_area"]["bottom"])
        
        for _ in range(RESPAWN_SYSTEM["position_tries"]):
            x = random.randrange(
                CELL_SIZE * RESPAWN_SYSTEM["safe_distance"],
                WINDOW_WIDTH - CELL_SIZE * (RESPAWN_SYSTEM["safe_distance"] + 1),
                CELL_SIZE
            )
            y = random.randrange(
                game_area_top + CELL_SIZE * RESPAWN_SYSTEM["safe_distance"],
                game_area_bottom - CELL_SIZE * (RESPAWN_SYSTEM["safe_distance"] + 1),
                CELL_SIZE
            )
            
            # 检查位置是否安全
            if not any(abs(x - pos[0]) < CELL_SIZE * 2 and abs(y - pos[1]) < CELL_SIZE * 2 
                      for pos in self.position):
                self.position = [(x, y)]
                return
            
        # 如果找不到安全位置，使用默认位置
        self.position = [(WINDOW_WIDTH // 2, (game_area_top + game_area_bottom) // 2)]
        
    def move(self, allow_wall_pass: bool = False) -> bool:
        """移动蛇并返回是否发生碰撞"""
        new_head = (
            self.position[0][0] + self.direction[0],
            self.position[0][1] + self.direction[1]
        )
        
        # 检查墙壁碰撞
        if not allow_wall_pass:
            if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
                return True
        else:
            new_head = (
                new_head[0] % WINDOW_WIDTH,
                new_head[1] % WINDOW_HEIGHT
            )
            
        # 检查自身碰撞
        if new_head in self.position[:-1]:
            return True
            
        self.position.insert(0, new_head)
        if len(self.position) > self.length:
            self.position.pop()
            
        return False
        
    def grow(self):
        """增加蛇的长度和分数"""
        self.length += 1
        self.combo_count += 1
        
        # 计算基础分数
        score = SCORE_SYSTEM["base_score"]
        
        # 应用连击加成
        for combo, multiplier in sorted(SCORE_SYSTEM["combo_multiplier"].items(), reverse=True):
            if self.combo_count >= combo:
                score *= multiplier
                break
                
        # 应用难度加成
        if self.difficulty in SCORE_SYSTEM["difficulty_bonus"]:
            score *= SCORE_SYSTEM["difficulty_bonus"][self.difficulty]
        
        self.score += int(score)
        
    def respawn(self):
        """重生处理"""
        if self.lives > 0:
            self.lives -= 1
            self.find_safe_position()
            self.invincible = True
            self.invincible_timer = time.time()
            return True
        return False
        
    def update(self, current_time):
        """更新蛇的状态"""
        if self.invincible:
            # 更新无敌状态
            if current_time - self.invincible_timer >= RESPAWN_SYSTEM["invincible_time"]:
                self.invincible = False
                self.visible = True
            else:
                # 闪烁效果
                if current_time - self.flash_timer >= RESPAWN_SYSTEM["flash_interval"]:
                    self.visible = not self.visible
                    self.flash_timer = current_time
        
    def change_direction(self, new_direction: Tuple[int, int]):
        """改变蛇的方向"""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction 
        
    def should_move(self) -> bool:
        """检查是否应该移动"""
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move_counter = 0
            return True
        return False 