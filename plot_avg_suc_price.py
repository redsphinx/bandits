import matplotlib.pyplot as plt
import csv

def plotit(name):
    filen = name
    with open(filen, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    data = map(float, your_list[0])
    plt.plot(data)
    plt.show()


if __name__ == "__main__":
    plotit("avg_success_price_5000.csv")
