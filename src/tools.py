import matplotlib.pyplot as plt

def plotter(dictionary, title, xlabel, ylabel, output):
    keys = []
    values = []
    for key in sorted(dictionary.keys()):
        keys.append(key)
        values.append(dictionary[key])

    plt.figure(figsize=(16, 9), dpi=100)
    plt.plot(keys, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(output+".png")