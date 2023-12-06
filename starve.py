import random
import matplotlib.pyplot as plt

# 随机生成一些数据点
def generate_data(num_points):
    data = [(random.random(), random.random()) for _ in range(num_points)]
    return data

# 计算矩形内节点数量
def count_points_inside_rect(data, rect_x, rect_y, rect_width, rect_height):
    count = 0
    for point in data:
        if (rect_x <= point[0] <= rect_x + rect_width) and (rect_y <= point[1] <= rect_y + rect_height):
            count += 1
    return count

# 计算优化对象值
def calculate_optimization_objective(rect_width, rect_height, count_points, node_size):
    return (count_points * node_size) / (rect_width * rect_height)

# 绘制矩形和数据点
def plot_rect_and_points(data, rect_x, rect_y, rect_width, rect_height):
    plt.figure(figsize=(6, 6))
    plt.scatter(*zip(*data), s=30, label='数据点')
    plt.gca().add_patch(plt.Rectangle((rect_x, rect_y), rect_width, rect_height, fill=False, color='r', label='矩形'))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend()
    plt.title('矩形与数据点')
    plt.show()

# 初始化数据点和初始矩形
data = generate_data(100)
rect_x, rect_y, rect_width, rect_height = 0.2, 0.2, 0.2, 0.2  # 初始矩形参数
node_size = 0.01  # 节点大小
count_points = count_points_inside_rect(data, rect_x, rect_y, rect_width, rect_height)
best_objective = calculate_optimization_objective(rect_width, rect_height, count_points, node_size)

# 可视化初始状态
plot_rect_and_points(data, rect_x, rect_y, rect_width, rect_height)

print(f"初始矩形参数: x={rect_x}, y={rect_y}, width={rect_width}, height={rect_height}")
print(f"初始优化对象值: {best_objective:.4f}")

# 迭代优化矩形（使用贪心算法）
iterations = 100
for i in range(iterations):
    improved = False

    # 遍历所有可能的参数组合
    for dx in [-1 + i * 0.02 for i in range(101)]:
        for dy in [-1 + i * 0.02 for i in range(101)]:
            for dw in [-0.1 + i * 0.01 for i in range(21)]:
                for dh in [-0.1 + i * 0.01 for i in range(21)]:
                    new_rect_x = rect_x + dx
                    new_rect_y = rect_y + dy
                    new_rect_width = rect_width + dw
                    new_rect_height = rect_height + dh

                    # 添加条件以确保矩形尺寸不会小于某个阈值
                    min_rect_size = 0.05
                    if new_rect_width >= min_rect_size and new_rect_height >= min_rect_size:
                        # 计算新的矩形内的节点数量
                        new_count_points = count_points_inside_rect(data, new_rect_x, new_rect_y, new_rect_width, new_rect_height)

                        # 计算新的优化对象值
                        new_objective = calculate_optimization_objective(new_rect_width, new_rect_height, new_count_points, node_size)

                        # 如果新的优化对象值更好，更新矩形参数
                        if new_objective > best_objective:
                            rect_x, rect_y, rect_width, rect_height = new_rect_x, new_rect_y, new_rect_width, new_rect_height
                            count_points = new_count_points
                            best_objective = new_objective
                            improved = True

    # 如果没有改进，提前结束
    if not improved:
        break

    # 可视化每次迭代的结果
    plot_rect_and_points(data, rect_x, rect_y, rect_width, rect_height)

    print(f"迭代{i + 1}: x={rect_x}, y={rect_y}, width={rect_width}, height={rect_height}")
    print(f"优化对象值: {best_objective:.4f}")

print("最终矩形参数: x={}, y={}, width={}, height={}".format(rect_x, rect_y, rect_width, rect_height))
print("最终优化对象值: {:.4f}".format(best_objective))
