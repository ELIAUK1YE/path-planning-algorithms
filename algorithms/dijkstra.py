"""
Dijkstra路径规划算法实现
经典的最短路径算法，不使用启发式函数
"""
import heapq
import time
from typing import Tuple, List, Dict, Optional

class DijkstraPlanner:
    """
    Dijkstra路径规划算法
    
    与A*类似，但不使用启发式函数（h(n) = 0）
    保证找到最优路径，但效率低于A*
    """
    
    def __init__(self, grid_map):
        """
        初始化Dijkstra规划器
        
        Args:
            grid_map: GridMap对象
        """
        self.grid_map = grid_map
        self.allow_diagonal = True
    
    def plan(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        使用Dijkstra算法规划路径
        
        Args:
            start: 起点坐标 (x, y)
            goal: 终点坐标 (x, y)
            
        Returns:
            Tuple[path, stats]:
                path: 路径点列表，如果未找到则为None
                stats: 统计信息字典
        """
        start_time = time.time()
        
        # 优先队列: (cost, counter, node)
        open_list = []
        counter = 0
        heapq.heappush(open_list, (0, counter, start))
        counter += 1
        
        # 记录每个节点的父节点
        came_from = {}
        
        # cost_so_far: 从起点到各节点的实际代价
        cost_so_far = {start: 0}
        
        # 关闭列表（已探索的节点）
        closed_set = set()
        
        # 记录探索过的节点（用于可视化）
        explored_nodes = []
        
        nodes_explored = 0
        
        while open_list:
            # 取出代价最小的节点
            current_cost, _, current = heapq.heappop(open_list)
            
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
                    'path_cost': cost_so_far[current]
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
                
                # 计算新的代价
                new_cost = cost_so_far[current] + cost
                
                # 如果找到更好的路径
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    
                    # 加入开放列表（注意：Dijkstra只使用实际代价，无启发式）
                    heapq.heappush(open_list, (new_cost, counter, neighbor))
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
        return f"DijkstraPlanner(diagonal={self.allow_diagonal})"
