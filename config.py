"""
全局配置文件
包含所有算法参数、地图配置、可视化配置等
"""
import os

# 项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(PROJECT_ROOT, 'maps')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

# 确保结果目录存在
os.makedirs(os.path.join(RESULTS_DIR, 'images'), exist_ok=True)
os.makedirs(os.path.join(RESULTS_DIR, 'data'), exist_ok=True)
os.makedirs(os.path.join(RESULTS_DIR, 'comparison'), exist_ok=True)

# 地图配置
MAP_CONFIG = {
    'simple': {'size': (50, 50), 'obstacle_density': 0.15},
    'medium': {'size':  (50, 50), 'obstacle_density': 0.25},
    'complex': {'size': (50, 50), 'obstacle_density': 0.35},
    'maze': {'size': (30, 30), 'type': 'maze'},
    'large': {'size':  (100, 100), 'obstacle_density': 0.20}
}

# A*算法配置
ASTAR_CONFIG = {
    'heuristic': 'euclidean',  # 'euclidean', 'manhattan', 'chebyshev'
    'allow_diagonal': True,
    'diagonal_cost': 1.414  # sqrt(2)
}

# Dijkstra算法配置
DIJKSTRA_CONFIG = {
    'allow_diagonal': True,
    'diagonal_cost':  1.414
}

# 可视化配置
VIS_CONFIG = {
    'figure_size': (12, 10),
    'dpi': 300,
    'font_size': 12,
    'line_width': 2,
    'save_format': 'png',
    'color_start': 'green',
    'color_goal': 'red',
    'color_obstacle': 'black',
    'color_free': 'white',
    'color_path': 'blue',
    'color_explored':  'lightblue'
}

# 随机种子（保证可复现性）
RANDOM_SEED = 42
