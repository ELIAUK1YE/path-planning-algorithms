"""
栅格地图类
用于表示二维栅格地图，支持障碍物检测、路径验证等功能
"""
import numpy as np
from typing import Tuple, List, Optional

class GridMap:
    """
    栅格地图类
    
    Attributes:
        width (int): 地图宽度
        height (int): 地图高度
        grid (np.ndarray): 地图数据，0表示自由空间，1表示障碍物
        start (Tuple[int, int]): 起点坐标
        goal (Tuple[int, int]): 终点坐标
    """
    
    def __init__(self, width: int, height: int):
        """
        初始化栅格地图
        
        Args:
            width: 地图宽度
            height: 地图高度
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.start = None
        self.goal = None
    
    def set_obstacle(self, x: int, y: int):
        """
        设置障碍物
        
        Args:
            x: x坐标
            y: y坐标
        """
        if self.is_valid(x, y):
            self.grid[y, x] = 1
    
    def is_obstacle(self, x: int, y: int) -> bool:
        """
        检查是否为障碍物
        
        Args:
            x: x坐标
            y: y坐标
            
        Returns:
            bool: 如果是障碍物返回true
        """
        if not self.is_valid(x, y):
            return True
        return self.grid[y, x] == 1
    
    def is_valid(self, x: int, y: int) -> bool:
        """
        检查坐标是否在地图范围内
        
        Args:
            x: x坐标
            y: y坐标
            
        Returns:
            bool: 如果坐标有效返回true
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_neighbors(self, x: int, y: int, allow_diagonal: bool = True) -> List[Tuple[int, int, float]]:
        """
        获取邻居节点
        
        Args:
            x: 当前点x坐标
            y: 当前点y坐标
            allow_diagonal: 是否允许对角线移动
            
        Returns:
            List[Tuple[int, int, float]]: 邻居节点列表，每个元素为(nx, ny, cost)
        """
        neighbors = []
        
        # 4个方向：上下左右
        directions_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # 8个方向：包括对角线
        directions_8 = [(0, 1), (1, 0), (0, -1), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        directions = directions_8 if allow_diagonal else directions_4
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if self.is_valid(nx, ny) and not self.is_obstacle(nx, ny):
                # 对角线移动的代价为sqrt(2)
                cost = 1.414 if (dx != 0 and dy != 0) else 1.0
                neighbors.append((nx, ny, cost))
        
        return neighbors
    
    def get_distance_to_obstacle(self, x: int, y: int) -> float:
        """
        计算到最近障碍物的距离
        
        Args:
            x: x坐标
            y: y坐标
            
        Returns:
            float: 到最近障碍物的距离
        """
        min_dist = float('inf')
        
        # 只在附近区域搜索（优化性能）
        search_radius = 10
        
        for dx in range(-search_radius, search_radius + 1):
            for dy in range(-search_radius, search_radius + 1):
                ox, oy = x + dx, y + dy
                if self.is_valid(ox, oy) and self.is_obstacle(ox, oy):
                    dist = np.sqrt(dx**2 + dy**2)
                    min_dist = min(min_dist, dist)
        
        return min_dist if min_dist != float('inf') else search_radius
    
    def set_start(self, x: int, y: int):
        """设置起点"""
        if self.is_valid(x, y) and not self.is_obstacle(x, y):
            self.start = (x, y)
        else:
            raise ValueError(f"起点 ({x}, {y}) 不合法")
    
    def set_goal(self, x: int, y: int):
        """设置终点"""
        if self.is_valid(x, y) and not self.is_obstacle(x, y):
            self.goal = (x, y)
        else:
            raise ValueError(f"终点 ({x}, {y}) 不合法")
    
    def save_to_file(self, filename: str):
        """
        保存地图到文件
        
        Args:
            filename: 文件名
        """
        with open(filename, 'w') as f:
            f.write(f"# Grid Map {self.width}x{self.height}\n")
            f.write(f"{self.width} {self.height}\n")
            
            if self.start:
                f.write(f"START {self.start[0]} {self.start[1]}\n")
            if self.goal:
                f.write(f"GOAL {self.goal[0]} {self.goal[1]}\n")
            
            for y in range(self.height):
                row = ' '.join(str(self.grid[y, x]) for x in range(self.width))
                f.write(row + '\n')
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'GridMap':
        """
        从文件加载地图
        
        Args:
            filename: 文件名
            
        Returns:
            GridMap: 加载的地图对象
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # 跳过注释行
        lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        # 读取尺寸
        width, height = map(int, lines[0].split())
        grid_map = cls(width, height)
        
        line_idx = 1
        
        # 读取起点和终点
        while line_idx < len(lines) and not lines[line_idx][0].isdigit():
            parts = lines[line_idx].split()
            if parts[0] == 'START':
                grid_map.start = (int(parts[1]), int(parts[2]))
            elif parts[0] == 'GOAL':
                grid_map.goal = (int(parts[1]), int(parts[2]))
            line_idx += 1
        
        # 读取地图数据
        for y in range(height):
            if line_idx + y < len(lines):
                row_data = list(map(int, lines[line_idx + y].split()))
                for x in range(min(width, len(row_data))):
                    grid_map.grid[y, x] = row_data[x]
        
        return grid_map
    
    def __repr__(self):
        return f"GridMap({self.width}x{self.height}, obstacles={np.sum(self.grid==1)})"