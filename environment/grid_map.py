"""
栅格地图类
用于表示二维栅格地图，支持障碍物检测、路径验证等功能
"""
import numpy as np
import matplotlib. pyplot as plt
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
            width:  地图宽度
            height: 地图高度
        """
        self.width = width
        self.height = height
        self.grid = np. zeros((height, width), dtype=int)
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
            x:  x坐标
            y:  y坐标
            
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
            y:  当前点y坐标
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
                # 对角线移动的代价为sqrt(2)，其他为1
                cost = 1.414 if abs(dx) + abs(dy) == 2 else 1.0
                neighbors.append((nx, ny, cost))
        
        return neighbors
    
    def generate_random_obstacles(self, density: float = 0.2):
        """
        生成随机障碍物
        
        Args:
            density: 障碍物密度，范围[0, 1]
        """
        obstacle_count = int(self.width * self.height * density)
        
        for _ in range(obstacle_count):
            x = np.random. randint(0, self.width)
            y = np.random.randint(0, self. height)
            self.set_obstacle(x, y)
    
    def generate_maze(self):
        """
        生成迷宫式障碍物
        使用递归分割算法
        """
        # 先填满障碍物
        self.grid[:] = 1
        
        # 递归生成迷宫
        self._generate_maze_recursive(0, 0, self. width, self.height)
    
    def _generate_maze_recursive(self, x: int, y: int, w: int, h: int):
        """
        递归生成迷宫
        
        Args: 
            x, y: 区域左上角坐标
            w, h:  区域宽度和高度
        """
        if w < 2 or h < 2:
            return
        
        # 清除一些格子
        for i in range(x, min(x + w, self.width)):
            for j in range(y, min(y + h, self.height)):
                if np.random.random() > 0.3:
                    self.grid[j, i] = 0
    
    def get_distance_to_obstacle(self, x: int, y: int) -> float:
        """
        计算到最近障碍物的距离
        
        Args:
            x: x坐标
            y: y坐标
            
        Returns:
            float:  到最近障碍物的欧氏距离
        """
        min_dist = float('inf')
        
        # 只搜索附近的区域以提高效率
        search_radius = 10
        
        for ox in range(max(0, x - search_radius), min(self.width, x + search_radius + 1)):
            for oy in range(max(0, y - search_radius), min(self.height, y + search_radius + 1)):
                if self. is_obstacle(ox, oy):
                    dist = np. sqrt((x - ox)**2 + (y - oy)**2)
                    min_dist = min(min_dist, dist)
        
        return min_dist if min_dist != float('inf') else 0.0
    
    def save_map(self, filename: str):
        """
        保存地图为图片
        
        Args:
            filename: 保存路径
        """
        plt.figure(figsize=(10, 10))
        plt.imshow(self.grid, cmap='binary', origin='lower')
        plt.title('Grid Map')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"地图已保存到:  {filename}")
    
    def __repr__(self):
        return f"GridMap(width={self.width}, height={self.height}, obstacles={np.sum(self.grid)})"
