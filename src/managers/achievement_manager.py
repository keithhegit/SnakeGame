"""
成就管理器
"""
from typing import Dict, List
import time

class AchievementManager:
    def __init__(self, achievements_config, save_manager):
        self.config = achievements_config
        self.save_manager = save_manager
        self.unlocked = save_manager.data.get("achievements", {})
        
    def check_achievements(self, game_state) -> List[Dict]:
        """检查成就解锁"""
        new_achievements = []
        
        # 检查各项成就条件
        if game_state["total_games"] == 1:
            new_achievements.extend(self.unlock_achievement("beginner"))
            
        if game_state["current_score"] >= 100:
            new_achievements.extend(self.unlock_achievement("score_100"))
            
        if game_state["current_score"] >= 500:
            new_achievements.extend(self.unlock_achievement("score_500"))
            
        if game_state["combo_count"] >= 10:
            new_achievements.extend(self.unlock_achievement("combo_master"))
            
        if (game_state["difficulty"] == "HARD" and 
            game_state["survival_time"] >= 300):
            new_achievements.extend(self.unlock_achievement("survivor"))
            
        return new_achievements
        
    def unlock_achievement(self, achievement_id: str) -> List[Dict]:
        """解锁成就"""
        if achievement_id not in self.unlocked:
            achievement = self.config[achievement_id]
            self.unlocked[achievement_id] = {
                "unlock_time": time.time(),
                **achievement
            }
            self.save_manager.update_save("achievements", self.unlocked)
            return [achievement]
        return [] 