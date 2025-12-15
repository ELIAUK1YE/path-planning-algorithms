# 基于搜索与优化算法的路径规划系统

## 📋 项目简介

本项目实现了一个完整的路径规划系统，适用于室内移动机器人、自动导航等应用场景。系统实现了4种经典路径规划算法，并提供了完整的可视化和性能评估工具。

### ✨ 功能特性

- ✅ **4种核心算法**: A*, Dijkstra, RRT, 遗传算法
- ✅ **多种测试地图**: 简单、中等、复杂、迷宫、大规模
- ✅ **完整可视化**: 路径图、对比图、性能图
- ✅ **性能评估**: 6项评估指标，CSV数据导出
- ✅ **详细报告**: 30+页技术文档
- ✅ **易于使用**: 命令行界面，配置灵活

## 🛠️ 技术栈

- Python 3.8+
- NumPy (数值计算)
- Matplotlib (可视化)
- Pandas (数据处理)
- SciPy (科学计算)

## 📦 环境要求

- Python 3.8+
- 操作系统: Windows/Linux/macOS

## 🚀 安装说明

```bash
# 1. 克隆仓库
git clone https://github.com/ELIAUK1YE/path-planning-algorithms.git
cd path-planning-algorithms

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 创建结果目录
mkdir -p results/images results/data results/comparison
```

## 💡 快速开始

### 1. 运行单个算法

```bash
# 运行A*算法
python main.py --algorithm astar --map medium --visualize

# 运行RRT算法并保存结果
python main.py --algorithm rrt --map complex --visualize --save

# 运行遗传算法
python main.py --algorithm genetic --map maze --visualize
```

### 2. 对比所有算法

```bash
# 在中等复杂度地图上对比所有算法
python main.py --algorithm all --map medium --visualize --save
```

### 3. 运行完整实验

```bash
# 运行所有实验（生成完整结果数据）
python experiments/run_experiments.py

# 运行算法对比实验
python experiments/compare_algorithms.py
```

## 📁 项目结构

```
path-planning-algorithms/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── config.py                    # 全局配置文件
├── main.py                      # 主程序入口
│
├── algorithms/                  # 算法实现模块
│   ├── __init__.py
│   ├── astar.py                # A*算法
│   ├── dijkstra.py             # Dijkstra算法
│   ├── rrt.py                  # RRT算法
│   └── genetic_algorithm.py    # 遗传算法
│
├── environment/                 # 环境模块
│   ├── __init__.py
│   ├── grid_map.py             # 栅格地图类
│   └── map_generator.py        # 地图生成器
│
├── utils/                       # 工具模块
│   ├── __init__.py
│   ├── visualizer.py           # 可视化工具
│   └── metrics.py              # 性能评估工具
│
├── experiments/                 # 实验脚本
│   ├── __init__.py
│   ├── run_experiments.py      # 运行所有实验
│   └── compare_algorithms.py   # 算法对比
│
├── maps/                        # 测试地图数据
│   ├── simple_50x50.txt
│   ├── medium_50x50.txt
│   ├── complex_50x50.txt
│   ├── maze_30x30.txt
│   └── large_100x100.txt
│
├── results/                     # 实验结果（运行后生成）
│   ├── images/                 # 可视化图片
│   ├── data/                   # CSV数据文件
│   └── comparison/             # 对比结果
│
└── report/                      # 技术报告
    └── technical_report.md     # 技术报告文档
```

## 🎯 算法说明

### A*算法
- **原理**: 启发式搜索算法，f(n) = g(n) + h(n)
- **时间复杂度**: O((V+E)logV)
- **优点**: 保证最优解，效率高
- **适用场景**: 静态环境，地图规模中小

### Dijkstra算法
- **原理**: 经典最短路径算法（无启发式）
- **时间复杂度**: O((V+E)logV)
- **优点**: 保证最优解，不需要启发式函数
- **适用场景**: 需要到所有点的最短路径

### RRT算法
- **原理**: 快速扩展随机树
- **时间复杂度**: O(n)
- **优点**: 适用于高维空间和复杂环境
- **适用场景**: 复杂障碍物环境，高维空间

### 遗传算法
- **原理**: 模拟生物进化的优化算法
- **时间复杂度**: O(G×P×L)
- **优点**: 全局搜索能力强，多目标优化
- **适用场景**: 复杂约束，多目标优化

## 📊 性能指标

系统评估以下6项指标：

1. **路径长度** (Path Length): 路径总距离
2. **规划时间** (Planning Time): 算法运行时间
3. **探索节点数** (Nodes Explored): 搜索的节点数量
4. **路径平滑度** (Smoothness): 路径转角惩罚
5. **安全距离** (Safety Margin): 到障碍物的最小距离
6. **成功率** (Success Rate): 是否找到可行路径

## 📈 实验结果示例

### 性能对比（50x50中等地图）

| 算法 | 路径长度 | 规划时间(s) | 探索节点 | 平滑度 |
|------|---------|------------|---------|--------|
| A* | 68.5 | 0.05 | 1200 | 8.2 |
| Dijkstra | 68.5 | 0.12 | 2400 | 8.2 |
| RRT | 85.3 | 0.35 | 3500 | 15.6 |
| Genetic | 72.1 | 2.50 | - | 6.5 |

*详细实验结果请查看 `report/technical_report.md`*

## 🔧 配置说明

所有配置参数位于 `config.py`：

```python
# 算法参数
ASTAR_CONFIG = {
    'heuristic': 'euclidean',
    'allow_diagonal': True
}

RRT_CONFIG = {
    'max_iter': 5000,
    'step_size': 5,
    'goal_sample_rate': 0.1
}

GA_CONFIG = {
    'population_size': 100,
    'generations': 200,
    'mutation_rate': 0.1
}
```

## ❓ 常见问题

**Q: 如何修改算法参数？**  
A: 编辑 `config.py` 文件中的相应配置字典。

**Q: 如何创建自定义地图？**  
A: 在 `maps/` 目录下创建文本文件，格式参考现有地图文件。

**Q: 如何保存实验结果？**  
A: 使用 `--save` 参数，或运行 `run_experiments.py` 自动保存所有结果。

**Q: 算法运行失败怎么办？**  
A: 检查地图连通性，增加算法迭代次数（修改config.py）。

**Q: 如何生成技术报告中的图表？**  
A: 运行 `python experiments/run_experiments.py`，所有图表会自动保存到 `results/`。

## 📚 技术报告

完整的技术报告位于 `report/technical_report.md`，包含：

- 理论分析（算法原理、复杂度分析）
- 系统设计（架构设计、模块说明）
- 实验结果（4组对比实验，12+张图表）
- 性能分析（算法优缺点、适用场景）
- 参考文献（15+篇学术文献）

## 👤 开发者

- **作者**: ELIAUK1YE
- **项目**: 人工智能课程大作业
- **日期**: 2025年12月

## 📄 许可证

MIT License

## 🙏 致谢

感谢以下开源项目和学术文献的启发：
- Hart et al. (1968) - A* Algorithm
- LaValle (1998) - RRT Algorithm
- PythonRobotics项目

## 📮 联系方式

如有问题或建议，请提Issue或Pull Request。

---

**注**: 本项目仅用于学习和研究目的。