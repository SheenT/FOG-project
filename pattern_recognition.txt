import matplotlib.pyplot as plt
import numpy as np

data_path = "/Users/seale/Downloads/FOG4.csv"


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

//ask about convolve function 
x = np.convolve(x_acc, np.ones(5)/5, mode='same')
y = np.convolve(y_acc, np.ones(5)/5, mode='same')
z = np.convolve(z_acc, np.ones(5)/5, mode='same')


def find_peak(values):
    high_indices = []
    low_indices = []

    for i in range(len(values) - 1):
        if i > 0:
            if values[i] > values[i+1] and values[i] > values[i-1]:
                high_indices.append(i)
            elif values[i] < values[i+1] and values[i] < values[i-1]:
                low_indices.append(i)
    return [high_indices, low_indices]


z_high = np.array(find_peak(z)[0])
z_low = np.array(find_peak(z)[1])

y_high = np.array(find_peak(y)[0])
y_low = np.array(find_peak(y)[1])

x_high = np.array(find_peak(x)[0])
x_low = np.array(find_peak(x)[1])

plt.plot(time[x_high], x[x_high], 'rx')
plt.plot(time[x_low], x[x_low], 'gx')
plt.plot(time[y_high], y[y_high], 'rx')
plt.plot(time[y_low], y[y_low], 'gx')
plt.plot(time[z_high], z[z_high], 'rx')
plt.plot(time[z_low], z[z_low], 'gx')

plt.plot(time, x)
plt.plot(time, y)
plt.plot(time, z)

plt.ylabel("Acceleration (unknown units)")
plt.xlabel("Time (s)")
plt.show()
