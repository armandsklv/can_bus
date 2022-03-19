import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

# fig, axs = plt.subplots(nrows=4, ncols=2)
# axs[0, 0].plot(x_vals, y_vals)
# axs[0, 0].set_title('Byte1')
# axs[1, 0].set_title('Byte2')
# axs[2, 0].set_title('Byte3')
# axs[3, 0].set_title('Byte4')
# axs[0, 1].set_title('Byte5')
# axs[1, 1].set_title('Byte6')
# axs[2, 1].set_title('Byte7')
# axs[3, 1].set_title('Byte8')

def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))
    plt.cla()
    plt.plot(x_vals, y_vals)

    # axs[0, 0].clear()
    # axs[1, 0].clear()
    # axs[2, 0].clear()
    # axs[3, 0].clear()
    # axs[0, 1].clear()
    # axs[1, 1].clear()
    # axs[2, 1].clear()
    # axs[3, 1].clear()
    #
    # axs[0, 0].plot(x_vals, y_vals)
    # axs[1, 0].plot(x_vals, y_vals)
    # axs[2, 0].plot(x_vals, y_vals)
    # axs[3, 0].plot(x_vals, y_vals)
    # axs[0, 1].plot(x_vals, y_vals)
    # axs[1, 1].plot(x_vals, y_vals)
    # axs[2, 1].plot(x_vals, y_vals)
    # axs[3, 1].plot(x_vals, y_vals)

anim_ = FuncAnimation(plt.gcf(), animate, interval=1)

# plt.tight_layout()
plt.show()

# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']
