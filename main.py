"""
主程序入口
支持命令行参数运行单个算法或对比实验
"""
import argparse
import os
import sys
import time
import numpy as np

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *

def main():
    parser = argparse.ArgumentParser(
        description='路径规划算法演示系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --algorithm astar --map medium --visualize
  python main.py --algorithm all --map complex --visualize --save
  python main.py --algorithm rrt --map maze --visualize
        """
    )
    
    parser.add_argument('--algorithm', '-a', type=str, default='astar',
                       choices=['astar', 'dijkstra', 'rrt', 'genetic', 'all'],
                       help='选择算法: astar, dijkstra, rrt, genetic, all')
    
    parser.add_argument('--map', '-m', type=str, default='medium',
                       help='选择地图名称（不含扩展名）')
    
    parser.add_argument('--visualize', '-v', action='store_true',
                       help='是否显示可视化结果')
    
    parser.add_argument('--save', '-s', action='store_true',
                       help='是否保存结果图片到results/目录')
    
    args = parser.parse_args()
    
    # 设置随机种子
    np.random.seed(RANDOM_SEED)
    
    print("=" * 60)
    print("路径规划算法演示系统".center(60))
    print("=" * 60)
    print(f"\n配置信息:")
    print(f"  算法: {args.algorithm.upper()}")
    print(f"  地图: {args.map}")
    print(f"  可视化: {'是' if args.visualize else '否'}")
    print(f"  保存结果: {'是' if args.save else '否'}")
    print(f"  随机种子: {RANDOM_SEED}")
    
    try:
        # 延迟导入，避免循环依赖
        from environment import GridMap, MapGenerator
        from algorithms import AStarPlanner, DijkstraPlanner, RRTPlanner, GeneticPlanner
        from utils import Visualizer, Metrics
        
        # 加载或生成地图
        map_file = os.path.join(MAPS_DIR, f'{args.map}.txt')
        
        if os.path.exists(map_file):
            print(f"\n加载地图: {map_file}")
            grid_map = GridMap.load_from_file(map_file)
        else:
            print(f"\n地图文件不存在，生成新地图...")
            if args.map in MAP_CONFIG:
                config = MAP_CONFIG[args.map]
                if config.get('type') == 'maze':
                    grid_map = MapGenerator.generate_maze(
                        config['size'][0], 
                        config['size'][1],
                        seed=RANDOM_SEED
                    )
                else:
                    grid_map = MapGenerator.generate_random_map(
                        config['size'][0],
                        config['size'][1],
                        config['obstacle_density'],
                        seed=RANDOM_SEED
                    )
                # 保存生成的地图
                os.makedirs(MAPS_DIR, exist_ok=True)
                grid_map.save_to_file(map_file)
                print(f"  地图已保存: {map_file}")
            else:
                print(f"错误: 未知的地图配置 '{args.map}'")
                return
        
        start = grid_map.start
        goal = grid_map.goal
        
        print(f"\n地图信息:")
        print(f"  尺寸: {grid_map.width} x {grid_map.height}")
        print(f"  起点: {start}")
        print(f"  终点: {goal}")
        print(f"  障碍物数量: {np.sum(grid_map.grid == 1)}")
        
        # 创建规划器
        planners = {
            'astar': lambda: AStarPlanner(grid_map),
            'dijkstra': lambda: DijkstraPlanner(grid_map),
            'rrt': lambda: RRTPlanner(grid_map, **RRT_CONFIG),
            'genetic': lambda: GeneticPlanner(grid_map, **GA_CONFIG)
        }
        
        # 运行算法
        if args.algorithm == 'all':
            print("\n" + "=" * 60)
            print("运行所有算法对比实验".center(60))
            print("=" * 60)
            
            results = {}
            for name in ['astar', 'dijkstra', 'rrt', 'genetic']:
                print(f"\n>>> 运行 {name.upper()} 算法...")
                planner = planners[name]()
                
                start_time = time.time()
                path, stats = planner.plan(start, goal)
                planning_time = time.time() - start_time
                
                if path is None:
                    print(f"  ✗ 算法失败: 未找到路径")
                    continue
                
                metrics = Metrics.evaluate_path(path, grid_map, planning_time, stats.get('nodes_explored', 0))
                results[name] = {
                    'path': path,
                    'metrics': metrics,
                    'explored': stats.get('explored_nodes', [])
                }
                
                print(f"  ✓ 成功!")
                print(f"    - 路径长度: {metrics['path_length']:.2f}")
                print(f"    - 规划时间: {planning_time:.4f}s")
                print(f"    - 探索节点: {metrics['nodes_explored']}")
                print(f"    - 平滑度: {metrics['smoothness']:.2f}")
            
            # 可视化对比
            if args.visualize or args.save:
                print(f"\n生成对比可视化...")
                vis = Visualizer(grid_map)
                save_path = os.path.join(RESULTS_DIR, 'comparison', 'all_algorithms.png') if args.save else None
                
                paths_dict = {name: res['path'] for name, res in results.items()}
                explored_dict = {name: res['explored'] for name, res in results.items()}
                
                vis.plot_comparison(paths_dict, start, goal, explored_dict, save_path=save_path)
                
                if save_path:
                    print(f"  对比图已保存: {save_path}")
                
                # 生成性能对比图
                metrics_dict = {name: res['metrics'] for name, res in results.items()}
                metrics_save_path = os.path.join(RESULTS_DIR, 'comparison', 'performance_comparison.png') if args.save else None
                vis.plot_performance_bars(metrics_dict, save_path=metrics_save_path)
                
                if metrics_save_path:
                    print(f"  性能对比图已保存: {metrics_save_path}")
            
            # 保存数据
            if args.save:
                import pandas as pd
                data_file = os.path.join(RESULTS_DIR, 'data', f'comparison_{args.map}.csv')
                df_data = []
                for name, res in results.items():
                    row = {'algorithm': name}
                    row.update(res['metrics'])
                    df_data.append(row)
                df = pd.DataFrame(df_data)
                df.to_csv(data_file, index=False)
                print(f"  数据已保存: {data_file}")
        
        else:
            # 运行单个算法
            print("\n" + "=" * 60)
            print(f"运行 {args.algorithm.upper()} 算法".center(60))
            print("=" * 60)
            
            planner = planners[args.algorithm]()
            
            print(f"\n开始规划...")
            start_time = time.time()
            path, stats = planner.plan(start, goal)
            planning_time = time.time() - start_time
            
            if path is None:
                print(f"\n✗ 规划失败: 未找到从 {start} 到 {goal} 的路径")
                print(f"  建议: 检查地图连通性或增加算法迭代次数")
                return
            
            print(f"\n✓ 规划成功!")
            
            metrics = Metrics.evaluate_path(path, grid_map, planning_time, stats.get('nodes_explored', 0))
            
            print(f"\n性能指标:")
            print(f"  路径长度: {metrics['path_length']:.2f}")
            print(f"  规划时间: {planning_time:.4f}s")
            print(f"  探索节点数: {metrics['nodes_explored']}")
            print(f"  路径平滑度: {metrics['smoothness']:.2f}")
            print(f"  安全距离: {metrics['safety_margin']:.2f}")
            
            # 可视化
            if args.visualize or args.save:
                print(f"\n生成可视化...")
                vis = Visualizer(grid_map)
                save_path = os.path.join(RESULTS_DIR, 'images', f'{args.algorithm}_{args.map}.png') if args.save else None
                
                vis.plot_path(
                    path, 
                    start, 
                    goal,
                    title=f'{args.algorithm.upper()} - {args.map}',
                    explored_nodes=stats.get('explored_nodes', []),
                    save_path=save_path
                )
                
                if save_path:
                    print(f"  图片已保存: {save_path}")
        
        print("\n" + "=" * 60)
        print("程序执行完成!".center(60))
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n错误: 缺少必要的模块")
        print(f"  {e}")
        print(f"\n请先运行: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
