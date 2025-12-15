"""
A*路径规划算法实现
使用启发式搜索找到从起点到终点的最优路径
"""
import heapq
import math
import time
from typing import Tuple, List, Dict, Optional

class AStarPlanner:
    """
    A*路径规划算法
    
    使用f(n) = g(n) + h(n)评估函数
    - g(n): 从起点到当前节点的实际代价
    - h(n): 从当前节点到终点的启发式估计（欧氏距离）
    """
    
    def __init__(self, grid_map):
        """
        初始化A*规划器
        
        Args:
            grid_map: GridMap对象
        """
        self.grid_map = grid_map
        self.allow_diagonal = True
    
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        使用A*算法规划路径
        
        Args:
            start: 起点坐标 (x, y)
            goal: 终点坐标 (x, y)
            
        Returns:
            Tuple[path, stats]:
                path: 路径点列表，如果未找到则为None
                stats: 统计信息字典
        """
        start_time = time.time()
        
        # 开放列表（优先队列）: (f_score, counter, node)
        open_list = []
        counter = 0
        heapq.heappush(open_list, (0, counter, start))
        counter += 1
        
        # 记录每个节点的父节点
        came_from = {}
        
        # g_score: 从起点到各节点的实际代价
        g_score = {start: 0}
        
        # f_score: g_score + h_score
        f_score = {start: self.heuristic(start, goal)}
        
        # 关闭列表（已探索的节点）
        closed_set = set()
        
        # 记录探索过的节点（用于可视化）
        explored_nodes = []
        
        nodes_explored = 0
        
        while open_list:
            # 取出f值最小的节点
            current_f, _, current = heapq.heappop(open_list)
            
            # 如果已经在关闭列表中，跳过
            if current in closed_set:
                continue
            
            # 添加到已探索节点
            explored_nodes.append(current)
            nodes_explored += 1
            
            # 到达目标
            if current == goal:
                path = self._reconstruct_path(came_from, current)
                planning_time = time.time() - start_time
                
                stats = {
                    'nodes_explored': nodes_explored,
                    'planning_time': planning_time,
                    'explored_nodes': explored_nodes,
                    'path_cost': g_score[current]
                }
                
                return path, stats
            
            # 加入关闭列表
            closed_set.add(current)
            
            # 探索邻居节点
            for neighbor_x, neighbor_y, cost in self.grid_map.get_neighbors(
                current[0], current[1], self.allow_diagonal
            ):
                neighbor = (neighbor_x, neighbor_y)
                
                # 如果已在关闭列表中，跳过
                if neighbor in closed_set:
                    continue
                
                # 计算新的g值
                tentative_g = g_score[current] + cost
                
                # 如果找到更好的路径
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    
                    # 加入开放列表
                    heapq.heappush(open_list, (f, counter, neighbor))
                    counter += 1
        
        # 未找到路径
        planning_time = time.time() - start_time
        stats = {
            'nodes_explored': nodes_explored,
            'planning_time': planning_time,
            'explored_nodes': explored_nodes,
            'path_cost': float('inf')
        }
        
        return None, stats
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        启发式函数：欧氏距离
        
        Args:
            pos1: 位置1
            pos2: 位置2
            
        Returns:
            float: 欧氏距离
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        重构路径
        
        Args:
            came_from: 父节点字典
            current: 当前节点（终点）
            
        Returns:
            List: 从起点到终点的路径
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def __repr__(self):
        return f"AStarPlanner(diagonal={self.allow_diagonal})"
