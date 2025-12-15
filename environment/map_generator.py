"""
地图生成器
用于生成不同类型的测试地图
"""
import numpy as np
from typing import Tuple
from .grid_map import GridMap

class MapGenerator:
    """地图生成器类"""
    
    @staticmethod
    def generate_random_map(width: int, height: int, obstacle_density: float = 0.2, 
                           seed: int = 42) -> GridMap:
        """
        生成随机障碍物地图
        
        Args:
            width: 地图宽度
            height: 地图高度
            obstacle_density: 障碍物密度 (0.0-1.0)
            seed: 随机种子
            
        Returns:
            GridMap: 生成的地图
        """
        np.random.seed(seed)
        grid_map = GridMap(width, height)
        
        # 随机生成障碍物
        num_obstacles = int(width * height * obstacle_density)
        
        for _ in range(num_obstacles):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            grid_map.set_obstacle(x, y)
        
        # 生成起点和终点
        MapGenerator._add_random_start_goal(grid_map, seed)
        
        return grid_map
    
    @staticmethod
    def generate_maze(width: int, height: int, seed: int = 42) -> GridMap:
        """
        生成迷宫地图（使用深度优先搜索）
        
        Args:
            width: 地图宽度（应为奇数）
            height: 地图高度（应为奇数）
            seed: 随机种子
            
        Returns:
            GridMap: 迷宫地图
        """
        np.random.seed(seed)
        
        # 确保尺寸为奇数
        width = width if width % 2 == 1 else width - 1
        height = height if height % 2 == 1 else height - 1
        
        grid_map = GridMap(width, height)
        
        # 初始化：全部设为障碍物
        grid_map.grid[:, :] = 1
        
        # 从中心开始雕刻迷宫
        start_x, start_y = 1, 1
        grid_map.grid[start_y, start_x] = 0
        
        # 使用深度优先搜索生成迷宫
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack[-1]
            
            # 找到所有未访问的邻居（2步距离）
            neighbors = []
            for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if (0 < nx < width - 1 and 0 < ny < height - 1 and 
                    grid_map.grid[ny, nx] == 1):
                    neighbors.append((nx, ny, x + dx//2, y + dy//2))
            
            if neighbors:
                # 随机选择一个邻居
                nx, ny, wx, wy = neighbors[np.random.randint(len(neighbors))]
                # 打通墙壁
                grid_map.grid[wy, wx] = 0
                grid_map.grid[ny, nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # 生成起点和终点
        MapGenerator._add_random_start_goal(grid_map, seed)
        
        return grid_map
    
    @staticmethod
    def _add_random_start_goal(grid_map: GridMap, seed: int = 42):
        """
        随机生成起点和终点
        
        Args:
            grid_map: 地图对象
            seed: 随机种子
        """
        np.random.seed(seed)
        
        # 找到所有自由空间
        free_spaces = np.argwhere(grid_map.grid == 0)
        
        if len(free_spaces) < 2:
            # 如果自由空间不够，强制设置
            grid_map.grid[1, 1] = 0
            grid_map.grid[grid_map.height - 2, grid_map.width - 2] = 0
            grid_map.start = (1, 1)
            grid_map.goal = (grid_map.width - 2, grid_map.height - 2)
        else:
            # 随机选择两个远离的点
            idx1 = np.random.randint(0, len(free_spaces))
            
            # 选择离第一个点较远的点作为终点
            distances = np.linalg.norm(free_spaces - free_spaces[idx1], axis=1)
            idx2 = np.argmax(distances)
            
            start_y, start_x = free_spaces[idx1]
            goal_y, goal_x = free_spaces[idx2]
            
            grid_map.start = (int(start_x), int(start_y))
            grid_map.goal = (int(goal_x), int(goal_y))
