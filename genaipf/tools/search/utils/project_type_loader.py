import csv
import os
from typing import List, Dict, Set
from genaipf.utils.log_utils import logger


class ProjectTypeLoader:
    """项目类型加载器，用于从CSV文件加载和管理Web3项目分类"""
    
    def __init__(self, csv_file_path: str = None):
        """
        初始化项目类型加载器
        
        Args:
            csv_file_path: CSV文件路径，默认为当前目录下的project_type.csv
        """
        if csv_file_path is None:
            # 默认路径为当前文件同目录下的project_type.csv
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file_path = os.path.join(current_dir, 'project_type.csv')
        
        self.csv_file_path = csv_file_path
        self.project_types = []
        self.project_type_set = set()
        self.project_type_map = {}
        self._load_project_types()
    
    def _load_project_types(self):
        """从CSV文件加载项目类型"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    project_type = row['project_type'].strip()
                    num = int(row['num']) if row['num'].isdigit() else 0
                    
                    self.project_types.append({
                        'type': project_type,
                        'num': num
                    })
                    self.project_type_set.add(project_type)
                    self.project_type_map[project_type] = num
            
            logger.info(f"成功加载 {len(self.project_types)} 个项目类型分类")
        except FileNotFoundError:
            logger.error(f"项目类型CSV文件未找到: {self.csv_file_path}")
            self.project_types = []
        except Exception as e:
            logger.error(f"加载项目类型CSV文件失败: {e}")
            self.project_types = []
    
    def get_all_types(self) -> List[str]:
        """获取所有项目类型列表"""
        return [pt['type'] for pt in self.project_types]
    
    def get_all_types_with_counts(self) -> List[Dict[str, any]]:
        """获取所有项目类型及其数量"""
        return self.project_types.copy()
    
    def get_types_by_count_range(self, min_count: int = 0, max_count: int = None) -> List[str]:
        """根据数量范围筛选项目类型"""
        if max_count is None:
            max_count = float('inf')
        
        return [
            pt['type'] for pt in self.project_types 
            if min_count <= pt['num'] <= max_count
        ]
    
    def get_top_types(self, limit: int = 50) -> List[str]:
        """获取数量最多的前N个项目类型"""
        sorted_types = sorted(self.project_types, key=lambda x: x['num'], reverse=True)
        return [pt['type'] for pt in sorted_types[:limit]]
    
    def is_valid_type(self, project_type: str) -> bool:
        """检查项目类型是否有效"""
        return project_type in self.project_type_set
    
    def get_type_count(self, project_type: str) -> int:
        """获取指定项目类型的数量"""
        return self.project_type_map.get(project_type, 0)
    
    def get_types_by_keywords(self, keywords: List[str]) -> List[str]:
        """
        根据关键词匹配项目类型
        
        Args:
            keywords: 关键词列表
            
        Returns:
            匹配的项目类型列表
        """
        matched_types = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for pt in self.project_types:
            project_type = pt['type'].lower()
            
            # 精确匹配
            if any(kw in project_type for kw in keywords_lower):
                matched_types.append(pt['type'])
                continue
            
            # 部分匹配（包含关系）
            if any(project_type in kw or kw in project_type for kw in keywords_lower):
                matched_types.append(pt['type'])
                continue
        
        return matched_types
    
    def get_similar_types(self, target_type: str, threshold: float = 0.6) -> List[str]:
        """
        获取相似的项目类型（基于字符串相似度）
        
        Args:
            target_type: 目标类型
            threshold: 相似度阈值
            
        Returns:
            相似的项目类型列表
        """
        from difflib import SequenceMatcher
        
        similar_types = []
        target_lower = target_type.lower()
        
        for pt in self.project_types:
            project_type = pt['type']
            similarity = SequenceMatcher(None, target_lower, project_type.lower()).ratio()
            
            if similarity >= threshold:
                similar_types.append((project_type, similarity))
        
        # 按相似度排序
        similar_types.sort(key=lambda x: x[1], reverse=True)
        return [pt[0] for pt in similar_types]
    
    def get_category_string(self, separator: str = "|") -> str:
        """获取用于prompt的分类字符串"""
        return separator.join(self.get_all_types()) + f"{separator}null"
    
    def get_top_category_string(self, limit: int = 50, separator: str = "|") -> str:
        """获取前N个分类的字符串"""
        top_types = self.get_top_types(limit)
        return separator.join(top_types) + f"{separator}null"


# 全局实例
_project_type_loader = None

def get_project_type_loader() -> ProjectTypeLoader:
    """获取全局项目类型加载器实例"""
    global _project_type_loader
    if _project_type_loader is None:
        _project_type_loader = ProjectTypeLoader()
    return _project_type_loader
