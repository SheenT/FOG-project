import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

data_path = "/Users/sheen/Downloads/FOGt3.csv"


data = open(data_path, 'r')

x_acc = []
y_acc = []
z_acc = []
t = []

for line in data:
    line_of_data = line.strip().split(',')

    list.append(t, float(line_of_data[0]))
    list.append(x_acc, float(line_of_data[1]))
    list.append(y_acc, float(line_of_data[2]))
    list.append(z_acc, float(line_of_data[3]))

time = np.array(t)/1000
x = np.array(x_acc)
y = np.array(y_acc)
z = np.array(z_acc)

x = np.convolve(x_acc, np.ones(5)/5, mode='same')
y = np.convolve(y_acc, np.ones(5)/5, mode='same')
z = np.convolve(z_acc, np.ones(5)/5, mode='same')


def find_peaks(values):
    high_indices = []
    low_indices = []
    all_indices = []

    for i in range(len(values)-1):
        if i > 0:
            if values[i] > values[i+1] and values[i] > values[i-1]:
                high_indices.append(i)
                all_indices.append(i)
            elif values[i] < values[i+1] and values[i] < values[i-1]:
                low_indices.append(i)
                all_indices.append(i)

    return [high_indices, low_indices, all_indices]

y_high = np.array(find_peaks(y)[0])
y_low = np.array(find_peaks(y)[1])
y_all = np.array(find_peaks(y)[2])


def get_FOG(high_ind, time):
    yFOG = []
    yNormal = []
    for i in range(len(high_ind)):
        if (time[high_ind[i]] > 15 and time[high_ind[i]] < 52):
            yFOG.append(y_high[i])
        else:
            yNormal.append(y_high[i])
    return [yFOG, yNormal]


def get_differences_amp(values, high_ind, low_ind):
    diff_high = []
    diff_low = []
    for i in range(len(high_ind)):
        diff = values[high_ind[i]] - values[high_ind[i - 1]]
        diff_high.append(diff)

    for i in range(len(low_ind)):
        diff = values[low_ind[i]] - values[low_ind[i - 1]]
        diff_low.append(diff)

    return [diff_high, diff_low]


def get_differences_time(time, ind_1, ind_2):
    diff_1 = []
    diff_2 = []

    for i in range(len(ind_1)):
        diff = time[ind_1[i]] - time[ind_1[i - 1]]
        if diff < 10 and diff > -10:
            diff_1.append(diff)
        else:
            diff_1.append(0)

    for i in range(len(ind_2)):
        diff = time[ind_2[i]] - time[ind_2[i - 1]]
        if diff < 10 and diff > -10:
            diff_2.append(diff)
        else:
            diff_2.append(0)

    return [diff_1, diff_2]


diff_high = get_differences_amp(y, y_high, y_low)[0]
diff_low = get_differences_amp(y, y_high, y_low)[1]

yFOG = get_FOG(y_high, time)[0]
yNormal = get_FOG(y_high, time)[1]

diff_FOG_amp = get_differences_amp(y, yFOG, yNormal )[0]
diff_Normal_amp = get_differences_amp(y, yFOG, yNormal )[1]

diff_FOG_time = get_differences_time(time, yFOG, yNormal )[0]
diff_Normal_time = get_differences_time(time, yFOG, yNormal )[1]

plt.plot(time[y_high], y[y_high], 'x', c='#8B668B')
# plt.plot(time[y_low], y[y_low], 'gx')
# plt.plot(time[y_all], y[y_all], 'bx')
plt.plot(time, y, c='#708090')

plt.ylabel("Acceleration")
plt.xlabel("Time (s)")
plt.title("Y-Acceleration of Normal Walking with FOG and Stopping vs. Time")

plt.show()

print(len(time))
"""
plt.scatter(diff_FOG_amp, y[yFOG], c='red')
plt.scatter(diff_Normal_amp, y[yNormal], c='green')
plt.show()

plt.scatter(diff_FOG_time, y[yFOG], c='red')
plt.scatter(diff_Normal_time, y[yNormal], c='green')

plt.ylabel("Amplitude")
plt.xlabel("Difference")
plt.show()
"""