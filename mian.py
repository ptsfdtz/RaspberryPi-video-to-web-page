import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 初始化pygame
pygame.init()

# 初始化手柄
pygame.joystick.init()

# 检查是否有手柄连接
if pygame.joystick.get_count() == 0:
    print("没有手柄连接")
    exit()

# 获取第一个手柄
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"手柄名称: {joystick.get_name()}")
print(f"轴数量: {joystick.get_numaxes()}")

# 初始化摇杆数据（左摇杆: 轴0和1，右摇杆: 轴2和3，扳机: 轴4和5）
left_stick = [0, 0]
right_stick = [0, 0]
triggers = [0, 0]

# 初始化matplotlib
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

left_stick_plot, = axs[0].plot([], [], 'bo')
right_stick_plot, = axs[2].plot([], [], 'ro')
lt_plot, = axs[1].plot([], [], 'g-', label='LT')
rt_plot, = axs[1].plot([], [], 'm-', label='RT')

axs[0].set_xlim(-1, 1)
axs[0].set_ylim(-1, 1)
axs[0].set_title('Left Stick')
axs[0].set_aspect('equal', adjustable='box')

axs[2].set_ylim(-1, 1)
axs[2].set_xlim(-1, 1)
axs[2].set_title('Right Stick')
axs[2].set_aspect('equal', adjustable='box')

axs[1].set_xlim(0, 100)
axs[1].set_ylim(-1, 1)
axs[1].set_title('Triggers')
axs[1].legend()

lt_data = []
rt_data = []

def init():
    left_stick_plot.set_data([], [])
    right_stick_plot.set_data([], [])
    lt_plot.set_data([], [])
    rt_plot.set_data([], [])
    return left_stick_plot, right_stick_plot, lt_plot, rt_plot

def update(frame):
    # 处理事件队列
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            left_stick[0] = joystick.get_axis(0)
            left_stick[1] = -joystick.get_axis(1)  # Y轴方向反转
            right_stick[0] = joystick.get_axis(2)
            right_stick[1] = -joystick.get_axis(3)  # Y轴方向反转
            triggers[0] = joystick.get_axis(4)
            triggers[1] = joystick.get_axis(5)

    left_stick_plot.set_data([left_stick[0]], [left_stick[1]])
    right_stick_plot.set_data([right_stick[0]], [right_stick[1]])

    # 更新触发器数据
    lt_data.append(triggers[0])
    rt_data.append(triggers[1])

    if len(lt_data) > 100:
        lt_data.pop(0)
    if len(rt_data) > 100:
        rt_data.pop(0)

    lt_plot.set_data(range(len(lt_data)), lt_data)
    rt_plot.set_data(range(len(rt_data)), rt_data)

    return left_stick_plot, right_stick_plot, lt_plot, rt_plot

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=50)

plt.tight_layout()
plt.show()

pygame.quit()
