"""
可视化工具
用于绘制路径、对比图和性能图表
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple, Dict, Optional
import seaborn as sns

class Visualizer:
    """路径规划可视化工具类"""
    
    def __init__(self, grid_map):
        """
        初始化可视化工具
        
        Args:
            grid_map: GridMap对象
        """
        self.grid_map = grid_map
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_path(self, path: List[Tuple[int, int]], start: Tuple[int, int], 
                  goal: Tuple[int, int], title: str = "Path Planning",
                  explored_nodes: List[Tuple[int, int]] = None,
                  save_path: str = None):
        """
        绘制单个路径
        
        Args:
            path: 路径点列表
            start: 起点
            goal: 终点
            title: 图标题
            explored_nodes: 探索过的节点（可选）
            save_path: 保存路径（可选）
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制地图
        ax.imshow(self.grid_map.grid, cmap='binary', origin='upper')
        
        # 绘制探索过的节点
        if explored_nodes:
            explored_x = [node[0] for node in explored_nodes]
            explored_y = [node[1] for node in explored_nodes]
            ax.scatter(explored_x, explored_y, c='lightblue', s=10, 
                      alpha=0.5, label='Explored Nodes')
        
        # 绘制路径
        if path:
            path_x = [p[0] for p in path]
            path_y = [p[1] for p in path]
            ax.plot(path_x, path_y, 'b-', linewidth=2, label='Path', zorder=5)
            ax.plot(path_x, path_y, 'b.', markersize=4, zorder=6)
        
        # 绘制起点和终点
        ax.plot(start[0], start[1], 'go', markersize=15, label='Start', zorder=10)
        ax.plot(goal[0], goal[1], 'r*', markersize=20, label='Goal', zorder=10)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图片已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_comparison(self, paths_dict: Dict[str, List[Tuple[int, int]]], 
                       start: Tuple[int, int], goal: Tuple[int, int],
                       explored_dict: Dict[str, List[Tuple[int, int]]] = None,
                       save_path: str = None):
        """
        对比多个算法的路径
        
        Args:
            paths_dict: 算法名到路径的映射
            start: 起点
            goal: 终点
            explored_dict: 算法名到探索节点的映射（可选）
            save_path: 保存路径（可选）
        """
        n_algorithms = len(paths_dict)
        cols = 2
        rows = (n_algorithms + 1) // 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows))
        if n_algorithms == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        
        for idx, (algo_name, path) in enumerate(paths_dict.items()):
            ax = axes[idx]
            
            # 绘制地图
            ax.imshow(self.grid_map.grid, cmap='binary', origin='upper')
            
            # 绘制探索节点
            if explored_dict and algo_name in explored_dict:
                explored = explored_dict[algo_name]
                if explored:
                    ex = [node[0] for node in explored]
                    ey = [node[1] for node in explored]
                    ax.scatter(ex, ey, c='lightblue', s=5, alpha=0.3)
            
            # 绘制路径
            if path:
                path_x = [p[0] for p in path]
                path_y = [p[1] for p in path]
                ax.plot(path_x, path_y, color=colors[idx % len(colors)], 
                       linewidth=2, label=f'{algo_name} Path')
            
            # 绘制起点和终点
            ax.plot(start[0], start[1], 'go', markersize=12)
            ax.plot(goal[0], goal[1], 'r*', markersize=15)
            
            ax.set_title(f'{algo_name.upper()} Algorithm', fontsize=14, fontweight='bold')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.grid(True, alpha=0.3)
        
        # 隐藏多余的子图
        for idx in range(n_algorithms, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"对比图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_performance_bars(self, metrics_dict: Dict[str, Dict], save_path: str = None):
        """
        绘制性能柱状对比图
        
        Args:
            metrics_dict: 算法名到性能指标的映射
            save_path: 保存路径（可选）
        """
        algorithms = list(metrics_dict.keys())
        metrics_names = ['path_length', 'planning_time', 'nodes_explored', 'smoothness']
        metrics_labels = ['Path Length', 'Planning Time (s)', 'Nodes Explored', 'Smoothness']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for idx, (metric_name, metric_label) in enumerate(zip(metrics_names, metrics_labels)):
            ax = axes[idx]
            
            values = [metrics_dict[algo].get(metric_name, 0) for algo in algorithms]
            
            bars = ax.bar(algorithms, values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
            
            # 在柱子上显示数值
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value:.2f}',
                       ha='center', va='bottom', fontsize=10)
            
            ax.set_ylabel(metric_label, fontsize=12)
            ax.set_title(metric_label, fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"性能对比图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
