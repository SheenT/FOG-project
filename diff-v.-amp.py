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


def get_FOG_times(data_path):
    if data_path == "/Users/sheen/Downloads/FOGt1.csv":
        startFOG = 550
        endFOG = 1300
    elif data_path == "/Users/sheen/Downloads/FOGt2.csv":
        startFOG = 495
        endFOG = 1530
    elif data_path == "/Users/sheen/Downloads/FOGt3.csv":
        startFOG = 555
        endFOG = 1621
    elif data_path == "/Users/sheen/Downloads/FOGt4.csv":
        startFOG = 120
        endFOG = 299
    elif data_path == "/Users/sheen/Downloads/FOGt5.csv":
        startFOG = 133
        endFOG = 339
    elif data_path == "/Users/sheen/Downloads/FOGt6.csv":
        startFOG = 130
        endFOG = 359
    elif data_path == "/Users/sheen/Downloads/FOGt7.csv":
        startFOG = 409
        endFOG = 1453
    elif data_path == "/Users/sheen/Downloads/FOGt8.csv":
        startFOG = 132
        endFOG = 326
    return [startFOG, endFOG]


def find_peaks(values):
    high_indices = []
    low_indices = []
    all_indices = []

    for i in range(len(values) - 1):
        if i > 0:
            if values[i] > values[i+1] and values[i] > values[i-1]:
                high_indices.append(i)
                all_indices.append(i)
            elif values[i] < values[i+1] and values[i] < values[i-1]:
                low_indices.append(i)
                all_indices.append(i)

    return [high_indices, low_indices, all_indices]


def get_FOG(high_ind, start, end):
    yFOG = []
    yNormal = []
    for i in range(len(high_ind)):
        if (high_ind[i] > start and high_ind[i] < end):
            yFOG.append(high_ind[i])
        else:
            yNormal.append(high_ind[i])
    return [yFOG, yNormal]


def get_sections(high_ind, startFOG, endFOG, startStop, endStop):
    yFOG = []
    yNormal = []
    for i in range(len(high_ind)):
        if (high_ind[i] > startFOG and high_ind[i] < endFOG):
            yFOG.append(high_ind[i])
        else:
            yNormal.append(high_ind[i])
    return [yFOG, yNormal]


def get_local_max(values, peaks_ind):
    local_max = []
    diff_max = []
    for i in range(len(peaks_ind)):
        max_in_range = 0
        if i > 1 and i <= len(peaks_ind) - 2:
            for j in range(i - 2, i + 2):
                if values[peaks_ind[j]] > max_in_range:
                    max_in_range = values[peaks_ind[j]]
        elif i == 0:
            for j in range(i, i + 4):
                if values[peaks_ind[j]] > max_in_range:
                    max_in_range = values[peaks_ind[j]]
        elif i == 1:
            for j in range(i - 1, i + 3):
                if values[peaks_ind[j]] > max_in_range:
                    max_in_range = values[peaks_ind[j]]
        elif i == len(peaks_ind) - 1:
            for j in range(i - 4, i):
                if values[peaks_ind[j]] > max_in_range:
                    max_in_range = values[peaks_ind[j]]
        elif i == len(peaks_ind) - 2:
            for j in range(i - 3, i + 1):
                if values[peaks_ind[j]] > max_in_range:
                    max_in_range = values[peaks_ind[j]]
        local_max.append(max_in_range)
        diff = max_in_range - values[peaks_ind[i]]
        diff_max.append(diff)
    return [local_max, diff_max]


def sort_peaks(peaks, differences, values):
    normal = []
    fog = []
    fog_count = 0
    normal_count = 0
    for i in range(len(peaks)):
        if (-0.90*(values[peaks[i]]) + 18000) < differences[i]:
            normal_count = normal_count + 1
            fog_count = 0
            if normal_count > 1:
                normal.append(peaks[i])
        else:
            normal_count = 0
            fog_count = fog_count + 1
            if fog_count > 1:
                fog.append(peaks[i])
            else:
                normal.append(peaks[i])
    return [fog, normal]


startFOG = get_FOG_times(data_path)[0]
endFOG = get_FOG_times(data_path)[1]

y_high = np.array(find_peaks(y)[0])
yFOG = get_FOG(y_high, startFOG, endFOG)[0]
yNormal = get_FOG(y_high, startFOG, endFOG)[1]
#yStopped = get_sections(y_high, startFOG, endFOG, start_stop, end_stop)[2]

print(yFOG)
print(yNormal)


diff_max_FOG = np.array(get_local_max(y, yFOG))[1]
diff_max_Normal = np.array(get_local_max(y, yNormal))[1]
diff_max_both = np.array(get_local_max(y, y_high))[1]

plt.scatter(y[yFOG], diff_max_FOG, c='red')
plt.scatter(y[yNormal], diff_max_Normal, c='green')
#plt.scatter(y[y_high], diff_max_both, c='green')

plt.xlabel("Acceleration")
plt.ylabel("Acceleration Difference With Local Max")
plt.title("Comparing Peaks in Normal Walking Data")

red_patch = mpatches.Patch(color='red', label='Manually Labelled FOG Data')
green_patch = mpatches.Patch(color='green', label='Manually Labelled Normal Data')
plt.legend(handles=[green_patch, red_patch], loc=4)

x_line=np.linspace (10000, 22000, 10000)
x_line2=np.linspace (10000, 22000, 10000)

plt.plot(x_line, -0.90 * x_line + 18000, 'black')
#plt.plot(x_line2, -0.90 * x_line + 15200, 'black')

plt.show()

fog = sort_peaks(y_high, diff_max_both, y)[0]
normal = sort_peaks(y_high, diff_max_both, y)[1]


plt.plot(time[normal], y[normal], c='g')
plt.plot(time[fog], y[fog], c='r')

plt.title("2 and 2")
plt.ylabel("Acceleration")
plt.xlabel("Time (s)")
red_patch = mpatches.Patch(color='red', label='Detected FOG')
green_patch = mpatches.Patch(color='green', label='Detected Normal Walking')
plt.legend(handles=[green_patch, red_patch], loc=4)

plt.show()
