"""
排名管理器
"""
import json
import os
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class RankingManager:
    def __init__(self, config):
        self.config = config
        self.rankings = self.load_rankings()
        
    def load_rankings(self) -> Dict:
        """加载排行榜数据"""
        try:
            if not os.path.exists(self.config["file_path"]):
                return self.create_default_rankings()
            
            with open(self.config["file_path"], 'r', encoding='utf-8') as f:
                rankings = json.load(f)
                if not self.validate_rankings(rankings):
                    return self.create_default_rankings()
                self.clean_expired_records(rankings)
                return rankings
        except (json.JSONDecodeError, IOError):
            return self.create_default_rankings()
            
    def create_default_rankings(self) -> Dict:
        """创建默认排行榜结构"""
        rankings = {}
        for category in self.config["categories"]:
            rankings[category] = {}
            for difficulty in self.config["difficulty_names"]:
                rankings[category][difficulty.name] = []
        return rankings
        
    def clean_expired_records(self, rankings: Dict):
        """清理过期记录"""
        now = datetime.now()
        for category, config in self.config["categories"].items():
            if config["expire_hours"]:
                expire_time = now - timedelta(hours=config["expire_hours"])
                for difficulty in rankings[category]:
                    rankings[category][difficulty] = [
                        record for record in rankings[category][difficulty]
                        if datetime.fromtimestamp(record["timestamp"]) > expire_time
                    ]
                    
    def add_score(self, difficulty: str, score: int, player_name: str = "玩家") -> Dict[str, Optional[int]]:
        """添加新分数，返回各个分类的排名"""
        now = time.time()
        rankings = {}
        
        for category in self.config["categories"]:
            records = self.rankings[category][difficulty]
            
            # 添加新记录
            records.append({
                "name": player_name,
                "score": score,
                "timestamp": now
            })
            
            # 按分数排序
            records.sort(key=lambda x: x["score"], reverse=True)
            
            # 只保留前N名
            records = records[:self.config["max_records"]]
            
            # 获取当前分数排名
            for i, record in enumerate(records):
                if record["timestamp"] == now:
                    rankings[category] = i + 1
                    break
            else:
                rankings[category] = None
                
            self.rankings[category][difficulty] = records
            
        self.save_rankings()
        return rankings
        
    def save_rankings(self):
        """保存排行榜"""
        try:
            os.makedirs(os.path.dirname(self.config["file_path"]), exist_ok=True)
            with open(self.config["file_path"], 'w', encoding='utf-8') as f:
                json.dump(self.rankings, f, ensure_ascii=False, indent=2)
        except IOError:
            print("Error saving rankings")
            
    def get_rankings(self, category: str, difficulty: str) -> List[Dict]:
        """获取指定类别和难度的排行榜"""
        return self.rankings[category][difficulty] 

    def validate_rankings(self, rankings: Dict) -> bool:
        """验证排行榜数据格式"""
        try:
            for category in self.config["categories"]:
                if category not in rankings:
                    return False
                for difficulty in self.config["difficulty_names"]:
                    if difficulty.name not in rankings[category]:
                        return False
                    if not isinstance(rankings[category][difficulty.name], list):
                        return False
            return True
        except Exception:
            return False 