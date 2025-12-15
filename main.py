"""
路径规划算法主程序
支持A*和Dijkstra算法的比较测试
"""
import time
import numpy as np
from environment. grid_map import GridMap
from algorithms.astar import AStarPlanner
from algorithms. dijkstra import DijkstraPlanner
from utils.visualizer import Visualizer
from utils. metrics import Metrics
from config import MAP_CONFIG, ASTAR_CONFIG, DIJKSTRA_CONFIG, RESULTS_DIR, RANDOM_SEED
import os

def run_single_test(grid_map, start, goal, algorithm_name='astar'):
    """
    运行单个算法测试
    
    Args:
        grid_map: GridMap对象
        start: 起点坐标
        goal: 终点坐标
        algorithm_name: 算法名称 ('astar' 或 'dijkstra')
    
    Returns:
        tuple: (path, planning_time, nodes_explored, explored_nodes)
    """
    print(f"\n运行 {algorithm_name. upper()} 算法...")
    
    # 选择算法
    if algorithm_name == 'astar': 
        planner = AStarPlanner(grid_map)
        planner.allow_diagonal = ASTAR_CONFIG['allow_diagonal']
    elif algorithm_name == 'dijkstra':
        planner = DijkstraPlanner(grid_map)
        planner.allow_diagonal = DIJKSTRA_CONFIG['allow_diagonal']
    else:
        raise ValueError(f"未知算法:  {algorithm_name}")
    
    # 开始规划
    path, stats = planner.plan(start, goal)
    
    if path: 
        print(f"✓ 找到路径!  长度: {len(path)}, 耗时: {stats['planning_time']:.4f}秒, 探索节点: {stats['nodes_explored']}")
    else:
        print(f"✗ 未找到路径!  耗时: {stats['planning_time']:.4f}秒, 探索节点: {stats['nodes_explored']}")
    
    return path, stats['planning_time'], stats['nodes_explored'], stats['explored_nodes']


def run_comparison(map_type='medium'):
    """
    运行A*和Dijkstra算法的对比测试
    
    Args:
        map_type: 地图类型 ('simple', 'medium', 'complex', 'maze', 'large')
    """
    print("="*60)
    print(f"路径规划算法对比测试 - {map_type. upper()} 地图")
    print("="*60)
    
    # 设置随机种子
    np.random.seed(RANDOM_SEED)
    
    # 创建地图
    config = MAP_CONFIG[map_type]
    if config. get('type') == 'maze':
        grid_map = GridMap(config['size'][0], config['size'][1])
        grid_map.generate_maze()
    else:
        grid_map = GridMap(config['size'][0], config['size'][1])
        grid_map.generate_random_obstacles(config['obstacle_density'])
    
    # 设置起点和终点
    start = (5, 5)
    goal = (config['size'][0]-6, config['size'][1]-6)
    
    # 确保起点和终点不是障碍物
    grid_map.grid[start[1], start[0]] = 0
    grid_map.grid[goal[1], goal[0]] = 0
    
    print(f"地图大小: {config['size']}")
    print(f"起点: {start}, 终点: {goal}")
    
    # 保存地图
    map_save_path = os.path.join(RESULTS_DIR, 'images', f'{map_type}_map.png')
    grid_map.save_map(map_save_path)
    
    # 运行算法
    algorithms = ['astar', 'dijkstra']
    paths = {}
    explored = {}
    metrics_data = {}
    
    for algo in algorithms:
        path, plan_time, nodes_exp, explored_nodes = run_single_test(grid_map, start, goal, algo)
        paths[algo] = path
        explored[algo] = explored_nodes
        
        # 计算性能指标
        metrics = Metrics. evaluate_path(path, grid_map, plan_time, nodes_exp)
        metrics_data[algo] = metrics
    
    # 可视化
    visualizer = Visualizer(grid_map)
    
    # 绘制单独的路径图
    for algo, path in paths.items():
        if path:
            save_path = os.path.join(RESULTS_DIR, 'images', f'{map_type}_{algo}_path.png')
            visualizer.plot_path(
                path, start, goal,
                title=f'{algo. upper()} Path Planning - {map_type.upper()}',
                explored_nodes=explored[algo],
                save_path=save_path
            )
    
    # 绘制对比图
    comparison_path = os.path.join(RESULTS_DIR, 'comparison', f'{map_type}_comparison. png')
    visualizer.plot_comparison(paths, start, goal, explored, save_path=comparison_path)
    
    # 绘制性能对比图
    performance_path = os.path.join(RESULTS_DIR, 'comparison', f'{map_type}_performance.png')
    visualizer.plot_performance_bars(metrics_data, save_path=performance_path)
    
    # 保存性能数据
    csv_path = os.path.join(RESULTS_DIR, 'data', f'{map_type}_metrics.csv')
    Metrics.save_metrics_to_csv(metrics_data, csv_path)
    
    # 打印性能对比
    print("\n" + "="*60)
    print("性能对比")
    print("="*60)
    print(f"{'算法':<15} {'路径长度':<12} {'规划时间(s)':<15} {'探索节点': <12} {'平滑度':<10}")
    print("-"*60)
    for algo, metrics in metrics_data.items():
        if metrics['success']:
            print(f"{algo. upper():<15} {metrics['path_length']:<12.2f} "
                  f"{metrics['planning_time']:<15.4f} {metrics['nodes_explored']:<12} "
                  f"{metrics['smoothness']:<10.2f}")
        else:
            print(f"{algo.upper():<15} {'FAILED':<12} {metrics['planning_time']:<15.4f} "
                  f"{metrics['nodes_explored']:<12} {'N/A':<10}")
    print("="*60)


def main():
    """主函数"""
    # 可以测试不同复杂度的地图
    test_maps = ['simple', 'medium', 'complex']
    
    for map_type in test_maps:
        run_comparison(map_type)
        print("\n\n")


if __name__ == '__main__':
    main()
