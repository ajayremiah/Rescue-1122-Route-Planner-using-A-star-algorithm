import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from benchmark import run_experiment

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': (8, 5),
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'legend.framealpha': 1,
    'legend.edgecolor': 'black',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    })

def smooth_curve (x, y, num_points=300):
    x_array = np.array(x)
    y_array = np.array(y)   
    x_smooth = np.linspace(np.min(x), np.max(x), num_points)
    spline = make_interp_spline(x_array, y_array, k=3)
    y_smooth = spline(x_smooth)
    return x_smooth, y_smooth

# Graph 1 for runtime
def plot_runtime_comparison(sizes, rt_dijkstra, rt_astar, rt_greedy):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x1, y1 = smooth_curve(sizes, rt_dijkstra)
    x2, y2 = smooth_curve(sizes, rt_astar)
    x3, y3 = smooth_curve(sizes, rt_greedy) 
    
    ax.plot(x1, y1, '-', color='blue', linewidth=2)
    ax.plot(x2, y2, '--', color='gold', linewidth=2)
    ax.plot(x3, y3, '-', color='red', linewidth=2)
    
    ax.plot(sizes, rt_dijkstra, 'o', color='blue', linewidth=2, markersize=8, label='Dijkstra')
    ax.plot(sizes, rt_astar, 's', color='gold', linewidth=2, markersize=8, label='A*')
    ax.plot(sizes, rt_greedy, '^', color='red', linewidth=2, markersize=8, label='Greedy')
    
    ax.set_title('Runtime Comparison of A* vs Other Pathfinding Algorithms', fontsize=14, fontweight='bold')
    ax.set_xlabel('Grid Size (N x N)', fontsize=12)
    ax.set_ylabel('Runtime (ms)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(sizes)
    ax.legend(loc='upper left', fontsize=10, title='Algorithm')     
    
    ax.minorticks_on()
    ax.grid(True, which='major', linestyle='-', linewidth=0.5)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3)
    
    plt.tight_layout()
    plt.savefig('runtime_comparison.png', dpi=150)
    plt.show()
    print("Saved runtime comparison plot as 'runtime_comparison.png'")

# Graph 2 for nodes visited    
def plot_nodes_visited_comparison(sizes, nv_dijkstra, nv_astar, nv_greedy):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x1, y1 = smooth_curve(sizes, nv_dijkstra)
    x2, y2 = smooth_curve(sizes, nv_astar)
    x3, y3 = smooth_curve(sizes, nv_greedy)
    
    ax.plot(x1, y1, '-', color='blue', linewidth=2)
    ax.plot(x2, y2, '--', color='gold', linewidth=2)
    ax.plot(x3, y3, '-', color='red', linewidth=2)
    
    ax.plot(sizes, nv_dijkstra, 'o', label='Dijkstra', color='blue', linewidth=2, markersize=8)
    ax.plot(sizes, nv_astar, 's', label='A*', color='gold', linewidth=2, markersize=8)
    ax.plot(sizes, nv_greedy, '^', label='Greedy', color='red', linewidth=2, markersize=8)
    
    ax.set_title('Nodes Visited Comparison of A* vs Other Pathfinding Algorithms', fontsize=14, fontweight='bold')
    ax.set_xlabel('Grid Size (N x N)', fontsize=12)
    ax.set_ylabel('Nodes Visited', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(sizes)
    ax.legend(loc='upper left', fontsize=10, title='Algorithm')
    
    plt.tight_layout()
    plt.savefig('nodes_visited_comparison.png', dpi=150)
    plt.show()
    print("Saved nodes visited comparison plot as 'nodes_visited_comparison.png'")
    
# Graph 3 for path length        
def plot_path_length_comparison(sizes, pl_dijkstra, pl_astar, pl_greedy):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sizes_array = np.array(sizes)
    offset = 2
    
    x1, y1 = smooth_curve(sizes, pl_dijkstra)
    x2, y2 = smooth_curve(sizes, pl_astar)
    x3, y3 = smooth_curve(sizes, pl_greedy)
    
    ax.plot(x1 - offset, y1, '-', color='blue', linewidth=2)
    ax.plot(x2, y2, '--', color='gold', linewidth=2)
    ax.plot(x3, y3, '-', color='red', linewidth=2)
    
    ax.plot(sizes_array - offset, pl_dijkstra, 'o', color='blue', linewidth=2, markersize=8, label='Dijkstra')
    ax.plot(sizes_array, pl_astar, 's', color='gold', linewidth=2, markersize=8, label='A*')
    ax.plot(sizes_array, pl_greedy, '^', color='red', linewidth=2, markersize=8, label='Greedy')
    
    ax.set_title('Path Length Comparison of A* vs Other Pathfinding Algorithms', fontsize=14, fontweight='bold')
    ax.set_xlabel('Grid Size (N x N)', fontsize=12)
    ax.set_ylabel('Path Length', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(sizes)
    ax.legend(loc='upper left', fontsize=10, title='Algorithm')
    
    ax.minorticks_on()
    ax.grid(True, which='major', linestyle='-', linewidth=0.5)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3)
    
    
    plt.tight_layout()
    plt.savefig('path_length_comparison.png', dpi=150)
    plt.show()
    print("Saved path length comparison plot as 'path_length_comparison.png'")
 
# Generate all 3 graphs from benchmark.py    
def generate_graphs(results):
    sizes = results['sizes']
    
    print("\n" + "="*50)
    print("Generating Graphs...")
    print("="*50 + "\n")   
    
    # Plot all three graphs
    plot_runtime_comparison(sizes, results['dijkstra']['time'], results['astar']['time'], results['greedy']['time'])
    plot_nodes_visited_comparison(sizes, results['dijkstra']['nodes_visited'], results['astar']['nodes_visited'], results['greedy']['nodes_visited'])
    plot_path_length_comparison(sizes, results['dijkstra']['path_length'], results['astar']['path_length'], results['greedy']['path_length']) 
    
if __name__ == "__main__":
    results = run_experiment()
    
    generate_graphs(results)