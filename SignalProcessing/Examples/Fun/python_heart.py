import numpy as np
import math
import matplotlib.pyplot as plt
import time

listA = np.arange(0, 30, 0.1)
x1 = np.arange(1.6, 3.3, 0.01)
x2 = np.arange(0, 1.7, 0.01)
# x = np.arange(-1.7, 1.7, 0.01)

plt.figure(1)
for a in listA:
    print(a)
    x11 = x2 ** (2/3)
    x12 = np.sqrt(math.pi - np.power(x2, 2))
    x13 = np.sin(a * math.pi * x2)
    y1 = x11 + x12 * x13

    y2 = np.flip(y1)

    plt.clf()
    plt.plot(x1, y1, '-r')
    plt.plot(x2, y2, '-r')
    plt.xlim([-0.5, 4])
    
    plt.pause(0.05)


# import numpy as np
# import math
# import matplotlib.pyplot as plt
# import time
#
# listA = np.arange(0, 20, 0.1)
# x = np.arange(-1.7, 1.7, 0.1)
# a = 0
# y1 = np.power(x, (2 / 3)) + np.sqrt(math.pi - np.power(x, 2)) * np.sin(a * math.pi * x)
# y2 = np.power(x, (2 / 3)) + np.sqrt(math.pi - np.power(x, 2)) * np.sin(-a * math.pi * x)
#
# # to run GUI event loop
# plt.ion()
#
# # here we are creating sub plots
#
# figure = plt.figure(1)
# ax = figure.add_subplot(111)
# line1, = ax.plot(x, y1)
# line2, = ax.plot(x, y2)
#
# plt.title("HR Jpha", fontsize=20)
#
# figure.canvas.draw()
# plt.show(block=False)
#
# for i in range(len(listA)):
#     a = listA[i]
#     print(a)
#     y1_new = np.power(x, (2 / 3)) + np.sqrt(math.pi - np.power(x, 2)) * np.sin(a * math.pi * x)
#     y2_new = np.power(x, (2 / 3)) + np.sqrt(math.pi - np.power(x, 2)) * np.sin(-a * math.pi * x)
#
#     line1.set_xdata(x)
#     line1.set_ydata(y1_new)
#
#     line2.set_xdata(x)
#     line2.set_ydata(y2_new)
#
#     figure.canvas.draw()
#
#     plt.pause(0.5)
#
#     # figure.canvas.flush_events()
#
#     # # y1 = np.power(x, (2/3)) + np.sqrt(math.pi - np.power(x, 2))*np.sin(a*math.pi*x)
#     # # y2 = np.power(x, (2/3)) + np.sqrt(math.pi - np.power(x, 2))*np.sin(-a*math.pi*x)
#     # plt.figure(1)
#     # # plt.clf()
#     # plt.plot(x, y1, '-r')
#     # plt.plot(x, y2, '-r')
#     # # plt.show(block=False)
#     # plt.show()
#     #
#     time.sleep(0.5)
