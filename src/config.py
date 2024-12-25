"""
游戏配置文件
"""
from enum import Enum, auto
import pygame

# 窗口设置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
CELL_SIZE = 20

# 颜色配置
class Colors:
    class Light:
        BACKGROUND = (240, 240, 240)
        SNAKE = (46, 204, 113)
        FOOD = (231, 76, 60)
        TEXT = (44, 62, 80)
        GRID = (200, 200, 200)

    class Dark:
        BACKGROUND = (44, 62, 80)
        SNAKE = (46, 204, 113)
        FOOD = (231, 76, 60)
        TEXT = (236, 240, 241)
        GRID = (52, 73, 94)

# 游戏设置
class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    INFINITE = 4  # 新增无限模式

DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {
        "speed": 4,
        "wall_collision": True,
        "lives": 3,
        "food_timeout": None,
        "time_limit": 35,  # 35秒
        "name": "Casual Mode"
    },
    Difficulty.MEDIUM: {
        "speed": 6,
        "wall_collision": True,
        "lives": 1,
        "food_timeout": None,
        "time_limit": 60,  # 60秒
        "name": "Hard Mode"
    },
    Difficulty.HARD: {
        "speed": 8,
        "wall_collision": True,
        "lives": 1,
        "food_timeout": 5000,
        "time_limit": 90,  # 90秒
        "name": "Hell Mode"
    },
    Difficulty.INFINITE: {
        "speed": 8,
        "wall_collision": True,
        "lives": 1,
        "food_timeout": 5000,
        "time_limit": None,  # 无时间限制
        "name": "Infinite Mode"
    }
}

# 控制键
CONTROLS = {
    "UP": [pygame.K_UP, pygame.K_w],
    "DOWN": [pygame.K_DOWN, pygame.K_s],
    "LEFT": [pygame.K_LEFT, pygame.K_a],
    "RIGHT": [pygame.K_RIGHT, pygame.K_d],
    "PAUSE": [pygame.K_ESCAPE],
    "RESTART": [pygame.K_SPACE],
    "THEME": [pygame.K_t]
}

# 游戏状态
class GameState(Enum):
    READY = auto()      # 游戏准备开始
    COUNTDOWN = auto()  # 倒计时阶段
    PLAYING = auto()    # 游戏进行中
    PAUSED = auto()     # 游戏暂停
    GAME_OVER = auto()  # 游戏结束
    DIFFICULTY_SELECT = auto()  # 难度选择
    NAME_INPUT = auto()  # 名字输入
    LEADERBOARD = auto()  # 排行榜显示

# 倒计时配置
COUNTDOWN_SECONDS = 3
COUNTDOWN_FONT_SIZE = 120
COUNTDOWN_COLOR = (46, 204, 113)  # 绿色 

# 游戏提示文案
GAME_MESSAGES = {
    "GAME_TITLE": "Snake Game",
    "SUBTITLE": "Challenge from Keith",
    "PRESS_START": "Press SPACE to Start",
    "FIRST_DEATH": "Keith: Already? Choose a difficulty and try again!",
    "DIFFICULTY_EASY": "Casual Mode:\n✓ Wall Pass\n✓ 3 Lives\n✓ Slow Speed\n✓ 90s Time Limit",
    "DIFFICULTY_MEDIUM": "Challenge Mode:\n✓ Wall Collision\n✓ 1 Life\n✓ Medium Speed\n✓ 120s Time Limit",
    "DIFFICULTY_HARD": "Hell Mode:\n✓ Wall Collision\n✓ 1 Life\n✓ High Speed\n✓ Food Disappears\n✓ 150s Time Limit",
    "DIFFICULTY_INFINITE": "Infinite Mode:\n✓ Wall Collision\n✓ 1 Life\n✓ High Speed\n✓ Food Disappears\n✓ No Time Limit",
    "SCORE": "Score",
    "FINAL_SCORE": "Final Score",
    "LIVES": "Lives",
    "PRESS_RESTART": "Press SPACE to Restart",
    "PAUSED": "Game Paused",
    "PRESS_CONTINUE": "Press ESC to Continue",
    "NEW_RECORD": "New Record!",
    "CONTROLS_HINT": "Arrow Keys or WASD to Move",
    "PAUSE_HINT": "ESC to Pause",
    "THEME_HINT": "Press T to Switch Theme",
    "FOOD_TIMEOUT": "Food Disappearing!",
    "WALL_WARNING": "Watch the Wall!",
    "LEVEL_UP": "Level Up! Speed Increased",
    "TIME_LEFT": "Time Left",
    "TIME_UP": "Time's Up!",
    "DAILY_RANK": "Daily Rank",
    "WEEKLY_RANK": "Weekly Rank",
    "ALL_TIME_RANK": "All Time Rank",
    "RANK_TITLE": "{mode} Leaderboard",
    "YOUR_RANK": "Your Rank",
    "VIEW_RANKINGS": "View Rankings [R]",
    "NO_RECORDS": "No Records",
    "ENTER_NAME": "Congratulations! Enter your name:",
    "SUBMIT": "Submit [Enter]",
    "BACK": "Back [Esc]",
    "LEADERBOARD_TITLE": "{mode} Leaderboard",
    "GAME_OVER": "Game Over!"
}

# 视觉效果配置
VISUAL_EFFECTS = {
    "snake_gradient": [(46, 204, 113), (39, 174, 96)],  # 蛇身渐变色
    "food_pulse": True,  # 食物脉冲效果
    "grid_opacity": 0.2,  # 网格透明度
    "shadow_color": (0, 0, 0, 30),  # 阴影颜色和透明度
}

# 游戏元素样式
GAME_STYLE = {
    "snake_radius": 8,  # 蛇身圆角
    "food_radius": 10,  # 食物圆角
    "border_width": 3,  # 游戏区域边框宽度
    "shadow_offset": 4  # 阴影偏移
}

# 字体配置
FONTS = {
    "title": {
        "size": 80,
        "bold": True
    },
    "subtitle": {
        "size": 36,
        "bold": False
    },
    "score": {
        "size": 48,
        "bold": True
    },
    "message": {
        "size": 32,
        "bold": False
    }
}

# 按钮样式
BUTTON_STYLE = {
    "normal": (52, 152, 219),
    "hover": (41, 128, 185),
    "text": (255, 255, 255),
    "padding": 20,
    "width": 300,
    "height": 50,
    "border_radius": 25,
    "ranking_button": {
        "width": 180,
        "height": 45
    }
}

# 界面布局配置
LAYOUT = {
    "score_margin": 20,
    "title_y_pos": WINDOW_HEIGHT * 0.15,
    "subtitle_y_pos": WINDOW_HEIGHT * 0.25,
    "game_area": {
        "top": WINDOW_HEIGHT * 0.2,
        "bottom": WINDOW_HEIGHT * 0.8,
    },
    "buttons_start_y": WINDOW_HEIGHT * 0.35,
    "buttons_spacing": 30,
    "controls_hint_y": WINDOW_HEIGHT * 0.92,
}

# 添加帧率控制
FPS = 60  # 游戏帧率
MOVE_DELAY = {  # 每个难度的移动延迟（帧数）
    Difficulty.EASY: 15,    # 约每秒4次移动
    Difficulty.MEDIUM: 10,  # 约每秒6次移动
    Difficulty.HARD: 8      # 约每秒8次移动
} 

# 分数系统配置
SCORE_SYSTEM = {
    "base_score": 10,  # 基础分数
    "combo_multiplier": {  # 连击倍数
        3: 1.5,  # 3连击 1.5倍
        5: 2.0,  # 5连击 2倍
        7: 2.5,  # 7连击 2.5倍
        10: 3.0  # 10连击 3倍
    },
    "difficulty_bonus": {  # 难度加成
        Difficulty.EASY: 1.0,
        Difficulty.MEDIUM: 1.5,
        Difficulty.HARD: 2.0,
        Difficulty.INFINITE: 2.5
    }
}

# 重生系统配置
RESPAWN_SYSTEM = {
    "invincible_time": 3,  # 重生后无敌时间（秒）
    "flash_interval": 0.2,  # 闪烁间隔（秒）
    "safe_distance": 5,     # 重生安全距离（格子数）
    "position_tries": 10    # 重生位置尝试次数
}

# 触摸控制配置
TOUCH_CONTROLS = {
    "enabled": True,
    "swipe_threshold": 30,  # 滑动触发阈值（像素）
    "double_tap_time": 300, # 双击间隔（毫秒）
    "control_areas": {
        "up": (0.2, 0, 0.6, 0.4),     # 上滑区域 (x, y, width, height)
        "down": (0.2, 0.6, 0.6, 0.4),  # 下滑区域
        "left": (0, 0.2, 0.4, 0.6),    # 左滑区域
        "right": (0.6, 0.2, 0.4, 0.6)  # 右滑区域
    }
} 

# 存档系统配置
SAVE_SYSTEM = {
    "file_path": "save/game_save.json",
    "auto_save": True,
    "save_interval": 5,  # 自动保存间隔（秒）
    "save_fields": [
        "high_score",
        "achievements",
        "current_theme",
        "total_games",
        "total_score"
    ]
}

# 成就系统配置
ACHIEVEMENTS = {
    "beginner": {
        "name": "新手上路",
        "description": "完成第一局游戏",
        "icon": "🎮"
    },
    "score_100": {
        "name": "初露锋芒",
        "description": "单局得分达到100分",
        "icon": "🌟"
    },
    "score_500": {
        "name": "蛇王传说",
        "description": "单局得分达到500分",
        "icon": "👑"
    },
    "combo_master": {
        "name": "连击大师",
        "description": "达成10连击",
        "icon": "⚡"
    },
    "survivor": {
        "name": "生存专家",
        "description": "在困难模式下存活超过5分钟",
        "icon": "🛡️"
    }
}

# 触摸控制增强
TOUCH_CONTROLS.update({
    "gestures": {
        "swipe_up": "UP",
        "swipe_down": "DOWN",
        "swipe_left": "LEFT",
        "swipe_right": "RIGHT",
        "double_tap": "PAUSE",
        "long_press": "RESTART"
    },
    "gesture_time": 300,  # 手势识别时间窗口（毫秒）
    "long_press_time": 500,  # 长按识别时间（毫秒）
    "visual_feedback": True  # 是否显示触摸反馈
}) 

# 排名系统配置
RANKING_SYSTEM = {
    "file_path": "save/rankings.json",
    "max_records": 10,  # 每个难度保存前10名
    "categories": {
        "all_time": {
            "name": "All Time Best",
            "expire_hours": None
        }
    },
    "difficulty_names": {
        Difficulty.EASY: "Casual Mode",
        Difficulty.MEDIUM: "Hard Mode",
        Difficulty.HARD: "Hell Mode"
    }
} 

# 排行榜界面配置
RANKING_UI = {
    "min_score_for_record": 50,  # 最低记录分数
    "name_input": {
        "width": 300,
        "height": 40,
        "max_length": 10,
        "placeholder": "Enter your name",
        "font_size": 24,
        "padding": 5
    },
    "leaderboard": {
        "width": 400,
        "height": 500,
        "title_height": 50,
        "row_height": 40,
        "padding": 20,
        "columns": [
            ("Rank", 0.2),
            ("Player", 0.4),
            ("Score", 0.4)
        ]
    }
} 

# 虚拟摇杆配置
VIRTUAL_JOYSTICK = {
    "position": {
        "x": WINDOW_WIDTH * 0.15,  # 左下角位置
        "y": WINDOW_HEIGHT * 0.85
    },
    "size": 120,  # 摇杆大小
    "button_size": 40,  # 方向键按钮大小
    "colors": {
        "background": (255, 255, 255, 80),  # 半透明白色
        "buttons": (255, 255, 255, 120),    # 半透明白色
        "active": (255, 255, 255, 200)      # 高亮状态
    }
} 

# 界面按钮配置
UI_BUTTONS = {
    "back": {
        "width": 100,
        "height": 40,
        "margin": 20,
        "text": "Back [Esc]",
        "position": {
            "x": WINDOW_WIDTH - 120,  # 右上角
            "y": 20
        }
    },
    "pause": {
        "width": 100,
        "height": 40,
        "margin": 20,
        "text": "Pause [P]",
        "position": {
            "x": WINDOW_WIDTH - 240,  # 返回按钮左侧
            "y": 20
        }
    },
    "start": {
        "width": 200,
        "height": 60,
        "text": "START",
        "position": {
            "x": WINDOW_WIDTH // 2 - 100,  # 居中
            "y": WINDOW_HEIGHT * 0.6  # 在屏幕中下方
        }
    }
} 