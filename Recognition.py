import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

data_path = "/Users/sheen/Desktop/FOGt8.csv"

data = open(data_path, 'r')

x_acc = []
y_acc = []
z_acc = []
t = []
#time

for line in data:
#separating data with commas 
    line_of_data = line.strip().split(',')
#creating arrays 
    list.append(t, float(line_of_data[0]))
    list.append(x_acc, float(line_of_data[1]))
    list.append(y_acc, float(line_of_data[2]))
    list.append(z_acc, float(line_of_data[3]))

time = np.array(t)/1000
x = np.array(x_acc)
y = np.array(y_acc)
z = np.array(z_acc)

#convolve two functions to smooth out data 
x = np.convolve(x_acc, np.ones(5)/5, mode='same')
y = np.convolve(y_acc, np.ones(5)/5, mode='same')
z = np.convolve(z_acc, np.ones(5)/5, mode='same')


def find_peaks(values):
#function to find where peaks occur
    high_indices = []

    for i in range(len(values) - 1):
        if i > 0:
            if values[i] > values[i+1] and values[i] > values[i-1]:
                high_indices.append(i)
#add to array of high indices 

    return high_indices


#peaks_ind is array with indices of peaks 

def get_diff(values, peaks_ind):
    local_max = []
    diff_max = []
    for i in range(len(peaks_ind)):
        max_in_range = 0
#finding max value in each range 
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
        diff = max_in_range - values[peaks_ind[i]]
#difference of max in range vs other values in range 
        diff_max.append(diff)
    return diff_max


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


y_high = np.array(find_peaks(y))
diff_max_both = np.array(get_diff(y, y_high))
fog = sort_peaks(y_high, diff_max_both, y)[0]
normal = sort_peaks(y_high, diff_max_both, y)[1]

plt.plot(time[normal], y[normal], 'g')
plt.plot(time[fog], y[fog], c='red')
plt.title("Y-Acceleration Peaks of Normal Walking with FOG vs. Time")
plt.ylabel("Acceleration")
plt.xlabel("Time (s)")

red_patch = mpatches.Patch(color='red', label='Detected FOG')
green_patch = mpatches.Patch(color='green', label='Detected Normal Walking')
plt.legend(handles=[green_patch, red_patch], loc=4)

plt.show()
