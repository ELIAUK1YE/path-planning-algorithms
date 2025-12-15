"""
性能评估工具
用于评估路径规划算法的各项性能指标
"""
import numpy as np
import math
from typing import List, Tuple, Dict

class Metrics:
    """性能评估工具类"""
    
    @staticmethod
    def calculate_path_length(path: List[Tuple[int, int]]) -> float:
        """
        计算路径总长度
        
        Args:
            path: 路径点列表
            
        Returns:
            float: 路径总长度
        """
        if not path or len(path) < 2:
            return 0.0
        
        length = 0.0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        return length
    
    @staticmethod
    def calculate_smoothness(path: List[Tuple[int, int]]) -> float:
        """
        计算路径平滑度（转角惩罚）
        平滑度越小，路径转角越少
        
        Args:
            path: 路径点列表
            
        Returns:
            float: 路径平滑度（转角和）
        """
        if not path or len(path) < 3:
            return 0.0
        
        total_angle = 0.0
        
        for i in range(1, len(path) - 1):
            # 计算三个连续点形成的角度
            p1 = np.array(path[i - 1])
            p2 = np.array(path[i])
            p3 = np.array(path[i + 1])
            
            # 向量
            v1 = p2 - p1
            v2 = p3 - p2
            
            # 避免除零
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 > 0 and norm2 > 0:
                # 计算夹角（弧度）
                cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                cos_angle = np.clip(cos_angle, -1.0, 1.0)
                angle = math.acos(cos_angle)
                total_angle += angle
        
        return total_angle
    
    @staticmethod
    def calculate_safety_margin(path: List[Tuple[int, int]], grid_map) -> float:
        """
        计算安全距离（路径上所有点到最近障碍物的平均距离）
        
        Args:
            path: 路径点列表
            grid_map: GridMap对象
            
        Returns:
            float: 平均安全距离
        """
        if not path:
            return 0.0
        
        total_distance = 0.0
        
        for x, y in path:
            dist = grid_map.get_distance_to_obstacle(x, y)
            total_distance += dist
        
        return total_distance / len(path)
    
    @staticmethod
    def evaluate_path(path: List[Tuple[int, int]], grid_map, planning_time: float, 
                     nodes_explored: int) -> Dict:
        """
        综合评估路径性能
        
        Args:
            path: 路径点列表
            grid_map: GridMap对象
            planning_time: 规划时间（秒）
            nodes_explored: 探索的节点数
            
        Returns:
            Dict: 包含所有性能指标的字典
        """
        if path is None:
            return {
                'path_length': float('inf'),
                'planning_time': planning_time,
                'nodes_explored': nodes_explored,
                'smoothness': float('inf'),
                'safety_margin': 0.0,
                'success': False
            }
        
        return {
            'path_length': Metrics.calculate_path_length(path),
            'planning_time': planning_time,
            'nodes_explored': nodes_explored,
            'smoothness': Metrics.calculate_smoothness(path),
            'safety_margin': Metrics.calculate_safety_margin(path, grid_map),
            'success': True
        }
    
    @staticmethod
    def save_metrics_to_csv(metrics_dict: Dict[str, Dict], filename: str):
        """
        保存性能指标到CSV文件
        
        Args:
            metrics_dict: 算法名称到指标字典的映射
            filename: 保存的文件名
        """
        import pandas as pd
        
        # 转换为DataFrame
        data = []
        for algo_name, metrics in metrics_dict.items():
            row = {'algorithm': algo_name}
            row.update(metrics)
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"指标已保存到: {filename}")
    
    @staticmethod
    def load_metrics_from_csv(filename: str) -> Dict[str, Dict]:
        """
        从CSV文件加载性能指标
        
        Args:
            filename: CSV文件名
            
        Returns:
            Dict: 算法名称到指标字典的映射
        """
        import pandas as pd
        
        df = pd.read_csv(filename)
        metrics_dict = {}
        
        for _, row in df.iterrows():
            algo_name = row['algorithm']
            metrics = row.drop('algorithm').to_dict()
            metrics_dict[algo_name] = metrics
        
        return metrics_dict
