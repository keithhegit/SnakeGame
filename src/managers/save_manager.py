"""
存档管理器
"""
import json
import os
import time
from typing import Dict, Any

class SaveManager:
    def __init__(self, config):
        self.config = config
        self.data = self.load_save()
        self.last_save_time = time.time()
        
    def load_save(self) -> Dict[str, Any]:
        """加载存档"""
        if not os.path.exists(self.config["file_path"]):
            return self.create_default_save()
            
        try:
            with open(self.config["file_path"], 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self.create_default_save()
            
    def create_default_save(self) -> Dict[str, Any]:
        """创建默认存档"""
        return {
            "high_score": 0,
            "achievements": {},
            "current_theme": "light",
            "total_games": 0,
            "total_score": 0
        }
        
    def save_game(self, force: bool = False):
        """保存游戏"""
        current_time = time.time()
        if (force or self.config["auto_save"] and 
            current_time - self.last_save_time >= self.config["save_interval"]):
            os.makedirs(os.path.dirname(self.config["file_path"]), exist_ok=True)
            with open(self.config["file_path"], 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            self.last_save_time = current_time
            
    def update_save(self, key: str, value: Any):
        """更新存档数据"""
        self.data[key] = value
        if self.config["auto_save"]:
            self.save_game() 