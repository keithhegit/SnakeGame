"""
主题管理器
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import Colors

class ThemeManager:
    def __init__(self):
        self.is_dark_mode = False
        
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_mode = not self.is_dark_mode
        
    @property
    def current_theme(self):
        """获取当前主题的颜色配置"""
        return Colors.Dark if self.is_dark_mode else Colors.Light 