"""
游戏界面
"""
import pygame
import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.game.snake import Snake
from src.game.food import Food
from src.ui.theme import ThemeManager
from src.ui.buttons import Button
from src.managers.ranking_manager import RankingManager
from src.managers.save_manager import SaveManager
from src.managers.achievement_manager import AchievementManager
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, CONTROLS, 
    GameState, COUNTDOWN_SECONDS, COUNTDOWN_FONT_SIZE, COUNTDOWN_COLOR,
    Difficulty, DIFFICULTY_SETTINGS, BUTTON_STYLE, GAME_MESSAGES,
    LAYOUT, MOVE_DELAY, FONTS, VISUAL_EFFECTS, GAME_STYLE,
    TOUCH_CONTROLS, RANKING_SYSTEM, SAVE_SYSTEM, ACHIEVEMENTS,
    RANKING_UI, VIRTUAL_JOYSTICK, UI_BUTTONS
)

class GameScreen:
    def __init__(self, screen: pygame.Surface, theme_manager: ThemeManager):
        self.screen = screen
        self.theme_manager = theme_manager
        
        # 初始化字体
        self.fonts = {
            "title": pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', FONTS["title"]["size"], bold=FONTS["title"]["bold"]),
            "subtitle": pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', FONTS["subtitle"]["size"], bold=FONTS["subtitle"]["bold"]),
            "score": pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', FONTS["score"]["size"], bold=FONTS["score"]["bold"]),
            "message": pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', FONTS["message"]["size"], bold=FONTS["message"]["bold"])
        }
        
        # 初始化管理器
        self.ranking_manager = RankingManager(RANKING_SYSTEM)
        self.save_manager = SaveManager(SAVE_SYSTEM)
        self.achievement_manager = AchievementManager(ACHIEVEMENTS, self.save_manager)
        
        # 初始化游戏对象
        self.snake = Snake()
        self.food = Food()
        
        # 初始化游戏状态
        self.state = GameState.DIFFICULTY_SELECT
        self.countdown_start = 0
        self.countdown_current = COUNTDOWN_SECONDS
        self.is_first_game = True
        self.difficulty = Difficulty.HARD
        
        # 初始化按钮
        self.buttons = []
        self.setup_difficulty_buttons()
        
        # 触摸控制相关
        self.touch_start = None
        self.touch_start_time = 0
        self.last_tap_time = 0
        
        # 游戏效果相关
        self.pulse_value = 0
        self.pulse_direction = 1
        self.game_start_time = 0
        self.time_left = 0
        
        # 排行榜相关
        self.current_leaderboard_page = "all_time"
        self.input_text = ""
        
        # 初始化通用UI按钮
        self.ui_buttons = {
            "back": Button(
                UI_BUTTONS["back"]["position"]["x"],
                UI_BUTTONS["back"]["position"]["y"],
                UI_BUTTONS["back"]["width"],
                UI_BUTTONS["back"]["height"],
                UI_BUTTONS["back"]["text"],
                BUTTON_STYLE["normal"],
                BUTTON_STYLE["hover"],
                self.handle_back
            ),
            "pause": Button(
                UI_BUTTONS["pause"]["position"]["x"],
                UI_BUTTONS["pause"]["position"]["y"],
                UI_BUTTONS["pause"]["width"],
                UI_BUTTONS["pause"]["height"],
                UI_BUTTONS["pause"]["text"],
                BUTTON_STYLE["normal"],
                BUTTON_STYLE["hover"],
                self.handle_pause
            ),
            "start": Button(
                UI_BUTTONS["start"]["position"]["x"],
                UI_BUTTONS["start"]["position"]["y"],
                UI_BUTTONS["start"]["width"],
                UI_BUTTONS["start"]["height"],
                UI_BUTTONS["start"]["text"],
                BUTTON_STYLE["normal"],
                BUTTON_STYLE["hover"],
                self.start_countdown
            )
        }
        
    def setup_difficulty_buttons(self):
        """设置难度选择按钮"""
        button_width = BUTTON_STYLE["width"]
        button_height = BUTTON_STYLE["height"]
        spacing = LAYOUT["buttons_spacing"]
        start_y = LAYOUT["buttons_start_y"]
        
        # 添加标题
        title_text = self.fonts["title"].render(GAME_MESSAGES["GAME_TITLE"], True, self.theme_manager.current_theme.TEXT)
        self.title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, LAYOUT["title_y_pos"]))
        
        # 添加排行榜按钮在右上角
        ranking_button = Button(
            WINDOW_WIDTH - BUTTON_STYLE["ranking_button"]["width"] - LAYOUT["score_margin"],
            LAYOUT["score_margin"],
            BUTTON_STYLE["ranking_button"]["width"],
            BUTTON_STYLE["ranking_button"]["height"],
            GAME_MESSAGES["VIEW_RANKINGS"],
            BUTTON_STYLE["normal"],
            BUTTON_STYLE["hover"],
            self.show_leaderboard
        )
        self.buttons.append(ranking_button)
        
        # 难度选择按钮
        difficulties = [
            (Difficulty.EASY, DIFFICULTY_SETTINGS[Difficulty.EASY]["name"]),
            (Difficulty.MEDIUM, DIFFICULTY_SETTINGS[Difficulty.MEDIUM]["name"]),
            (Difficulty.HARD, DIFFICULTY_SETTINGS[Difficulty.HARD]["name"]),
            (Difficulty.INFINITE, DIFFICULTY_SETTINGS[Difficulty.INFINITE]["name"])
        ]
        
        for i, (diff, text) in enumerate(difficulties):
            y = start_y + i * (button_height + spacing)
            button = Button(
                WINDOW_WIDTH//2 - button_width//2,
                y,
                button_width,
                button_height,
                text,
                BUTTON_STYLE["normal"],
                BUTTON_STYLE["hover"],
                lambda d=diff: self.select_difficulty(d)
            )
            self.buttons.append(button)
        
    def select_difficulty(self, difficulty: Difficulty):
        """选择难度"""
        self.difficulty = difficulty
        self.snake = Snake()  # 重新创建蛇
        self.snake.difficulty = difficulty  # 设置难度
        self.food = Food()  # 重新创建食物
        self.state = GameState.READY  # 设置为准备状态
        self.is_first_game = False
        
    def start_countdown(self):
        """开始倒计时"""
        self.state = GameState.COUNTDOWN
        self.countdown_start = time.time()
        self.countdown_current = COUNTDOWN_SECONDS
        self.game_start_time = time.time()  # 记录游戏开始时间
        # 设置游戏时间限制
        if DIFFICULTY_SETTINGS[self.difficulty]["time_limit"]:
            self.time_left = DIFFICULTY_SETTINGS[self.difficulty]["time_limit"]
        
    def update(self):
        """更新游戏状态"""
        current_time = time.time()
        
        if self.state == GameState.COUNTDOWN:
            elapsed = int(current_time - self.countdown_start)
            self.countdown_current = max(0, COUNTDOWN_SECONDS - elapsed)
            
            if self.countdown_current == 0:
                self.state = GameState.PLAYING
                self.game_start_time = current_time
            return
            
        if self.state == GameState.PLAYING:
            # 更新时间限制
            if DIFFICULTY_SETTINGS[self.difficulty]["time_limit"]:
                self.time_left = max(0, DIFFICULTY_SETTINGS[self.difficulty]["time_limit"] - 
                                   int(current_time - self.game_start_time))
                if self.time_left == 0:
                    self.handle_game_over()  # 调用游戏结束处理
                    return
                    
            # 只在应该移动时才移动蛇
            if self.snake.should_move():
                collision = self.snake.move(
                    allow_wall_pass=not DIFFICULTY_SETTINGS[self.difficulty]["wall_collision"]
                )
                if collision:
                    if not self.snake.respawn():
                        self.state = GameState.GAME_OVER
                    return
                    
                if self.snake.position[0] == self.food.position:
                    self.snake.grow()
                    self.food.respawn(self.snake.position)
                
    def draw(self):
        """绘制游戏界面"""
        theme = self.theme_manager.current_theme
        self.screen.fill(theme.BACKGROUND)
        
        if self.state == GameState.DIFFICULTY_SELECT:
            # 绘制标题
            title_text = self.fonts["title"].render(GAME_MESSAGES["GAME_TITLE"], True, theme.TEXT)
            self.screen.blit(title_text, self.title_rect)
            
            # 绘制副标题
            subtitle_text = self.fonts["subtitle"].render(GAME_MESSAGES["SUBTITLE"], True, theme.TEXT)
            subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH/2, LAYOUT["subtitle_y_pos"]))
            self.screen.blit(subtitle_text, subtitle_rect)
            
            # 绘制所有按钮
            for button in self.buttons:
                button.draw(self.screen)
        else:
            # 绘制游戏区域
            self.draw_game_area()
            
            # 绘制游戏元素
            self.draw_snake()
            self.draw_food()
            
            # 绘制UI元素
            self.draw_score()
            self.draw_lives()
            
            # 绘制剩余时间（如果有时间限制）
            if self.state == GameState.PLAYING and DIFFICULTY_SETTINGS[self.difficulty]["time_limit"]:
                time_text = self.fonts["message"].render(
                    f"{GAME_MESSAGES['TIME_LEFT']}: {self.time_left}秒", 
                    True, 
                    theme.TEXT
                )
                time_rect = time_text.get_rect(
                    midtop=(WINDOW_WIDTH/2, LAYOUT["score_margin"])
                )
                self.screen.blit(time_text, time_rect)
                
                # 时间不足10秒时闪烁提示
                if self.time_left <= 10:
                    if int(time.time() * 2) % 2:  # 每0.5秒闪烁一次
                        warning_text = self.fonts["message"].render(
                            f"⚠ {self.time_left} ⚠", 
                            True, 
                            (231, 76, 60)  # 红色警告
                        )
                        warning_rect = warning_text.get_rect(
                            midtop=(WINDOW_WIDTH/2, time_rect.bottom + 5)
                        )
                        self.screen.blit(warning_text, warning_rect)
            
            # 绘制游戏状态
            if self.state == GameState.READY:
                self.draw_ready_screen()
            elif self.state == GameState.COUNTDOWN:
                self.draw_countdown()
            elif self.state == GameState.PAUSED:
                self.draw_pause_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            if self.state == GameState.NAME_INPUT:
                self.draw_name_input()
            elif self.state == GameState.LEADERBOARD:
                self.draw_leaderboard()
        
        # 在游戏进行中时显示暂停按钮
        if self.state == GameState.PLAYING:
            self.ui_buttons["pause"].draw(self.screen)
        
        # 在除了难度选择界面外的所有界面显示返回按钮
        if self.state != GameState.DIFFICULTY_SELECT:
            self.ui_buttons["back"].draw(self.screen)
        
        self.draw_virtual_joystick()
        
    def draw_ready_screen(self):
        """绘制准备界面"""
        theme = self.theme_manager.current_theme
        
        # 标题
        title = self.fonts["title"].render(
            f"{DIFFICULTY_SETTINGS[self.difficulty]['name']}", 
            True, theme.TEXT
        )
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, LAYOUT["title_y_pos"]))
        self.screen.blit(title, title_rect)
        
        # 绘制难度说明
        description = GAME_MESSAGES[f"DIFFICULTY_{self.difficulty.name}"]
        y_offset = LAYOUT["subtitle_y_pos"]
        for line in description.split('\n'):
            desc_text = self.fonts["message"].render(line, True, theme.TEXT)
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH/2, y_offset))
            self.screen.blit(desc_text, desc_rect)
            y_offset += 40
        
        # 绘制开始按钮
        self.ui_buttons["start"].draw(self.screen)
        
    def draw_countdown(self):
        """绘制倒计时"""
        font = pygame.font.Font(None, COUNTDOWN_FONT_SIZE)
        text = font.render(str(self.countdown_current), True, COUNTDOWN_COLOR)
        rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(text, rect)
        
    def draw_game_over(self):
        """绘制游戏结束界面"""
        theme = self.theme_manager.current_theme
        
        # 添加分数到排行榜
        rankings = self.ranking_manager.add_score(
            self.difficulty.name,
            self.snake.score
        )
        
        texts = [
            (self.fonts["title"].render(GAME_MESSAGES["GAME_OVER"], True, theme.TEXT), 
             LAYOUT["title_y_pos"]),
            (self.fonts["subtitle"].render(
                f"{GAME_MESSAGES['FINAL_SCORE']}: {self.snake.score}", 
                True, theme.TEXT
            ), LAYOUT["subtitle_y_pos"])
        ]
        
        # 显示排名信息
        y_offset = LAYOUT["subtitle_y_pos"] + 50
        for category, rank in rankings.items():
            if rank is not None:
                category_name = RANKING_SYSTEM["categories"][category]["name"]
                rank_text = self.fonts["message"].render(
                    f"{category_name}: #{rank}", True, 
                    (46, 204, 113) if rank <= 3 else theme.TEXT
                )
                texts.append((rank_text, y_offset))
                y_offset += 40
        
        # 绘制所有文本
        for text_surface, y_pos in texts:
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH/2, y_pos))
            self.screen.blit(text_surface, text_rect)
        
        if self.is_first_game:
            for button in self.buttons:
                button.draw(self.screen)
        
    def handle_event(self, event: pygame.event.Event):
        """处理游戏事件"""
        if event.type == pygame.KEYDOWN:
            # 名字输入处理
            if self.state == GameState.NAME_INPUT:
                if event.key == pygame.K_RETURN and self.input_text:
                    # 保存记录
                    self.ranking_manager.add_score(
                        self.difficulty.name,
                        self.snake.score,
                        self.input_text
                    )
                    self.state = GameState.GAME_OVER
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.GAME_OVER
                elif len(self.input_text) < RANKING_UI["name_input"]["max_length"]:
                    if event.unicode.isprintable():
                        self.input_text += event.unicode
                return
            # 键盘事件处理
            if event.key == pygame.K_ESCAPE:
                self.handle_back()
            elif event.key == pygame.K_p and self.state == GameState.PLAYING:
                self.handle_pause()
            elif self.state == GameState.PLAYING:
                # 游戏控制
                if event.key in CONTROLS["UP"]:
                    self.snake.change_direction((0, -CELL_SIZE))
                elif event.key in CONTROLS["DOWN"]:
                    self.snake.change_direction((0, CELL_SIZE))
                elif event.key in CONTROLS["LEFT"]:
                    self.snake.change_direction((-CELL_SIZE, 0))
                elif event.key in CONTROLS["RIGHT"]:
                    self.snake.change_direction((CELL_SIZE, 0))
            elif self.state == GameState.LEADERBOARD and event.key == pygame.K_TAB:
                # 切换排行榜分类
                categories = list(RANKING_SYSTEM["categories"].keys())
                current_index = categories.index(self.current_leaderboard_page)
                self.current_leaderboard_page = categories[
                    (current_index + 1) % len(categories)
                ]
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # 难度选择界面的按钮处理
            if self.state == GameState.DIFFICULTY_SELECT:
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.action()
                        return
            
            # 准备界面的开始按钮处理
            elif self.state == GameState.READY:
                if self.ui_buttons["start"].rect.collidepoint(mouse_pos):
                    self.start_countdown()
                    return
            
            # 通用UI按钮处理
            if self.state != GameState.DIFFICULTY_SELECT:
                if self.ui_buttons["back"].rect.collidepoint(mouse_pos):
                    self.handle_back()
                    return
                
            if self.state == GameState.PLAYING:
                if self.ui_buttons["pause"].rect.collidepoint(mouse_pos):
                    self.handle_pause()
                    return
        
        elif event.type == pygame.MOUSEMOTION:
            # 处理按钮悬停效果
            mouse_pos = event.pos
            
            # 更新难度选择按钮状态
            if self.state == GameState.DIFFICULTY_SELECT:
                for button in self.buttons:
                    button.is_hovered = button.rect.collidepoint(mouse_pos)
                    button.current_color = button.hover_color if button.is_hovered else button.color
            
            # 更新通用UI按钮状态
            if self.state != GameState.DIFFICULTY_SELECT:
                self.ui_buttons["back"].is_hovered = self.ui_buttons["back"].rect.collidepoint(mouse_pos)
                self.ui_buttons["back"].current_color = (
                    self.ui_buttons["back"].hover_color if self.ui_buttons["back"].is_hovered 
                    else self.ui_buttons["back"].color
                )
                
            if self.state == GameState.PLAYING:
                self.ui_buttons["pause"].is_hovered = self.ui_buttons["pause"].rect.collidepoint(mouse_pos)
                self.ui_buttons["pause"].current_color = (
                    self.ui_buttons["pause"].hover_color if self.ui_buttons["pause"].is_hovered 
                    else self.ui_buttons["pause"].color
                )
        
        elif event.type in (pygame.FINGERDOWN, pygame.FINGERUP, pygame.FINGERMOTION):
            # 触摸事件处理
            self.handle_touch(event)
        
    def reset_game(self):
        """重置游戏"""
        self.snake.reset()
        self.food.respawn(self.snake.position)
        # 根据难度设置游戏参数
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.snake.speed = settings["speed"]
        self.snake.wall_collision = settings["wall_collision"]
        self.snake.lives = settings["lives"]
        self.snake.move_delay = MOVE_DELAY[self.difficulty]  # 设置移动延迟
        self.snake.move_counter = 0  # 重置移动计数器
        # 重置状态
        self.state = GameState.READY
        self.countdown_start = 0
        self.countdown_current = COUNTDOWN_SECONDS
        
    def draw_game_area(self):
        """绘制游戏区域"""
        theme = self.theme_manager.current_theme
        
        # 绘制游戏区域边框
        game_area = pygame.Rect(
            0,
            LAYOUT["game_area"]["top"],
            WINDOW_WIDTH,
            LAYOUT["game_area"]["bottom"] - LAYOUT["game_area"]["top"]
        )
        pygame.draw.rect(self.screen, theme.GRID, game_area, GAME_STYLE["border_width"])
        
    def draw_score(self):
        """绘制分数"""
        theme = self.theme_manager.current_theme
        score_text = self.fonts["score"].render(
            f"{GAME_MESSAGES['SCORE']}: {self.snake.score}", 
            True, 
            theme.TEXT
        )
        score_rect = score_text.get_rect(
            topleft=(LAYOUT["score_margin"], LAYOUT["score_margin"])
        )
        self.screen.blit(score_text, score_rect)
        
    def draw_snake(self):
        """绘制蛇"""
        theme = self.theme_manager.current_theme
        for i, segment in enumerate(self.snake.position):
            # 使用渐变色
            color_index = i % len(VISUAL_EFFECTS["snake_gradient"])
            color = VISUAL_EFFECTS["snake_gradient"][color_index]
            
            # 绘制蛇身方块
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(
                    segment[0],
                    segment[1],
                    CELL_SIZE - 2,  # 留出间隙
                    CELL_SIZE - 2
                ),
                border_radius=GAME_STYLE["snake_radius"]
            )
        
    def draw_food(self):
        """绘制食物"""
        theme = self.theme_manager.current_theme
        if VISUAL_EFFECTS["food_pulse"]:
            # 脉冲效果
            pulse_size = int(4 * self.pulse_value)
            rect = pygame.Rect(
                self.food.position[0] - pulse_size//2,
                self.food.position[1] - pulse_size//2,
                CELL_SIZE - 2 + pulse_size,
                CELL_SIZE - 2 + pulse_size
            )
        else:
            rect = pygame.Rect(
                self.food.position[0],
                self.food.position[1],
                CELL_SIZE - 2,
                CELL_SIZE - 2
            )
        
        pygame.draw.rect(
            self.screen,
            theme.FOOD,
            rect,
            border_radius=GAME_STYLE["food_radius"]
        )
        
    def draw_lives(self):
        """绘制生命值"""
        if self.snake.lives > 1:
            heart_text = "❤" * self.snake.lives
            lives_text = self.fonts["message"].render(
                f"{GAME_MESSAGES['LIVES']}: {heart_text}", True, 
                self.theme_manager.current_theme.TEXT
            )
            lives_rect = lives_text.get_rect(
                topright=(WINDOW_WIDTH - LAYOUT["score_margin"], LAYOUT["score_margin"])
            )
            self.screen.blit(lives_text, lives_rect)
        
    def handle_touch(self, event):
        """处理触摸事件"""
        if event.type == pygame.FINGERDOWN:
            self.touch_start = (event.x * WINDOW_WIDTH, event.y * WINDOW_HEIGHT)
            self.touch_start_time = time.time()
        elif event.type == pygame.FINGERUP:
            if self.touch_start:
                end_pos = (event.x * WINDOW_WIDTH, event.y * WINDOW_HEIGHT)
                touch_time = time.time() - self.touch_start_time
                
                # 检测手势类型
                if touch_time < TOUCH_CONTROLS["gesture_time"] / 1000:
                    # 快速点击判断为轻触
                    dx = end_pos[0] - self.touch_start[0]
                    dy = end_pos[1] - self.touch_start[1]
                    
                    if abs(dx) < TOUCH_CONTROLS["swipe_threshold"] and abs(dy) < TOUCH_CONTROLS["swipe_threshold"]:
                        # 双击检测
                        if time.time() - self.last_tap_time < TOUCH_CONTROLS["double_tap_time"] / 1000:
                            self.handle_double_tap()
                        self.last_tap_time = time.time()
                    else:
                        # 滑动手势
                        if abs(dx) > abs(dy):
                            if dx > 0:
                                self.snake.change_direction((CELL_SIZE, 0))
                            else:
                                self.snake.change_direction((-CELL_SIZE, 0))
                        else:
                            if dy > 0:
                                self.snake.change_direction((0, CELL_SIZE))
                            else:
                                self.snake.change_direction((0, -CELL_SIZE))
                elif touch_time >= TOUCH_CONTROLS["long_press_time"] / 1000:
                    # 长按
                    self.handle_long_press()
                    
                self.touch_start = None
                
    def handle_double_tap(self):
        """处理双击事件"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            
    def handle_long_press(self):
        """处理长按事件"""
        if self.state == GameState.GAME_OVER:
            self.reset_game()
        
    def draw_grid(self):
        """绘制网格"""
        theme = self.theme_manager.current_theme
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # 获取当前难度的网格大小
        grid_size = DIFFICULTY_SETTINGS[self.difficulty]["grid_size"]
        cell_size = min(
            (WINDOW_WIDTH) // grid_size,
            (LAYOUT["game_area"]["bottom"] - LAYOUT["game_area"]["top"]) // grid_size
        )
        
        # 计算游戏区域的实际大小和起始位置
        game_width = cell_size * grid_size
        game_height = cell_size * grid_size
        start_x = (WINDOW_WIDTH - game_width) // 2
        start_y = (LAYOUT["game_area"]["bottom"] + LAYOUT["game_area"]["top"] - game_height) // 2
        
        # 绘制竖线
        for x in range(grid_size + 1):
            x_pos = start_x + x * cell_size
            pygame.draw.line(
                grid_surface,
                GAME_STYLE["grid_color"],
                (x_pos, start_y),
                (x_pos, start_y + game_height),
                GAME_STYLE["grid_line_width"]
            )
        
        # 绘制横线
        for y in range(grid_size + 1):
            y_pos = start_y + y * cell_size
            pygame.draw.line(
                grid_surface,
                GAME_STYLE["grid_color"],
                (start_x, y_pos),
                (start_x + game_width, y_pos),
                GAME_STYLE["grid_line_width"]
            )
        
        self.screen.blit(grid_surface, (0, 0))
        
    def show_leaderboard(self):
        """显示排行榜"""
        self.state = GameState.LEADERBOARD
        self.current_leaderboard_page = "all_time"  # 默认显示历史最佳
        
    def draw_leaderboard(self):
        """绘制排行榜界面"""
        theme = self.theme_manager.current_theme
        config = RANKING_UI["leaderboard"]
        
        # 绘制半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色背景
        self.screen.blit(overlay, (0, 0))
        
        # 绘制排行榜面板
        board_rect = pygame.Rect(
            WINDOW_WIDTH//2 - config["width"]//2,
            WINDOW_HEIGHT//2 - config["height"]//2,
            config["width"],
            config["height"]
        )
        pygame.draw.rect(self.screen, theme.BACKGROUND, board_rect,
                        border_radius=GAME_STYLE["border_width"])
        pygame.draw.rect(self.screen, theme.GRID, board_rect,
                        GAME_STYLE["border_width"], border_radius=GAME_STYLE["border_width"])
        
        # 绘制标题
        title_text = self.fonts["subtitle"].render(  # 改用较小的字体
            f"{RANKING_SYSTEM['categories'][self.current_leaderboard_page]['name']} Rankings",
            True, theme.TEXT
        )
        title_rect = title_text.get_rect(
            midtop=(WINDOW_WIDTH//2, board_rect.top + config["padding"])
        )
        self.screen.blit(title_text, title_rect)
        
        # 绘制记录
        start_y = title_rect.bottom + config["padding"]
        records = self.ranking_manager.get_rankings(
            self.current_leaderboard_page,
            self.difficulty.name
        )
        
        # 绘制返回按钮
        back_button = Button(
            board_rect.left + config["padding"],
            board_rect.bottom - config["padding"] - BUTTON_STYLE["height"],
            BUTTON_STYLE["width"]//2,
            BUTTON_STYLE["height"],
            "Back [Esc]",
            BUTTON_STYLE["normal"],
            BUTTON_STYLE["hover"],
            lambda: setattr(self, 'state', GameState.DIFFICULTY_SELECT)
        )
        back_button.draw(self.screen)
        self.leaderboard_back_button = back_button  # 保存引用以处理点击
        
        # 绘制切换分类提示
        hint_text = self.fonts["message"].render(
            "Press TAB to Switch Category", True, theme.TEXT
        )
        hint_rect = hint_text.get_rect(
            midtop=(WINDOW_WIDTH//2, back_button.rect.top - 10)
        )
        self.screen.blit(hint_text, hint_rect)
        
    def draw_name_input(self):
        """绘制名字输入界面"""
        theme = self.theme_manager.current_theme
        config = RANKING_UI["name_input"]
        
        # 绘制提示文本
        prompt_text = self.fonts["message"].render(
            GAME_MESSAGES["ENTER_NAME"], True, theme.TEXT
        )
        prompt_rect = prompt_text.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50)
        )
        self.screen.blit(prompt_text, prompt_rect)
        
        # 绘制输入框
        input_rect = pygame.Rect(
            WINDOW_WIDTH//2 - config["width"]//2,
            prompt_rect.bottom + 20,
            config["width"],
            config["height"]
        )
        pygame.draw.rect(self.screen, theme.GRID, input_rect,
                        border_radius=GAME_STYLE["border_width"])
        
        # 绘制输入的文本
        if self.input_text:
            text_surface = self.fonts["message"].render(self.input_text, True, theme.TEXT)
        else:
            text_surface = self.fonts["message"].render(
                config["placeholder"], True, (*theme.TEXT[:3], 128)
            )
        text_rect = text_surface.get_rect(
            midleft=(input_rect.left + config["padding"], input_rect.centery)
        )
        self.screen.blit(text_surface, text_rect)
        
        # 绘制确认按钮提示
        submit_text = self.fonts["message"].render(
            GAME_MESSAGES["SUBMIT"], True, theme.TEXT
        )
        submit_rect = submit_text.get_rect(
            midtop=(WINDOW_WIDTH//2, input_rect.bottom + 20)
        )
        self.screen.blit(submit_text, submit_rect)

    def handle_game_over(self):
        """处理游戏结束"""
        if self.snake.score >= RANKING_UI["min_score_for_record"]:
            self.state = GameState.NAME_INPUT
            self.input_text = ""
        else:
            self.state = GameState.GAME_OVER

    def draw_virtual_joystick(self):
        """绘制虚拟摇杆"""
        if self.state != GameState.PLAYING:
            return
        
        config = VIRTUAL_JOYSTICK
        joystick_surface = pygame.Surface((config["size"], config["size"]), pygame.SRCALPHA)
        
        # 绘制背景圆
        pygame.draw.circle(joystick_surface, config["colors"]["background"], 
                          (config["size"]//2, config["size"]//2), config["size"]//2)
        
        # 定义方向键位置
        buttons = {
            "UP": (config["size"]//2, config["button_size"]//2),
            "DOWN": (config["size"]//2, config["size"] - config["button_size"]//2),
            "LEFT": (config["button_size"]//2, config["size"]//2),
            "RIGHT": (config["size"] - config["button_size"]//2, config["size"]//2)
        }
        
        # 获取当前按下的键
        keys = pygame.key.get_pressed()
        
        # 绘制方向键
        for direction, pos in buttons.items():
            color = config["colors"]["active"] if any(keys[key] for key in CONTROLS[direction]) \
                    else config["colors"]["buttons"]
            pygame.draw.circle(joystick_surface, color, pos, config["button_size"]//2)
        
        # 绘制到屏幕
        self.screen.blit(joystick_surface, 
                        (config["position"]["x"] - config["size"]//2,
                         config["position"]["y"] - config["size"]//2))

    def handle_back(self):
        """处理返回按钮点击"""
        if self.state == GameState.PLAYING:
            self.state = GameState.DIFFICULTY_SELECT
        elif self.state == GameState.PAUSED:
            self.state = GameState.DIFFICULTY_SELECT
        elif self.state == GameState.LEADERBOARD:
            self.state = GameState.DIFFICULTY_SELECT
        elif self.state == GameState.GAME_OVER:
            self.state = GameState.DIFFICULTY_SELECT

    def handle_pause(self):
        """处理暂停按钮点击"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING