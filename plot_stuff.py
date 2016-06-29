import matplotlib.pyplot as plt
import csv
import numpy as np

avg_reward = [7.91, 9.67, 10.70, 30.02, 32.23, 11.79, 14.51, 13.24, 18.78, 25.66]
num_suc = [2332, 3151,2618, 7055, 7808, 2904, 5371, 4724, 6408, 6434]
avg_suc_price = [33.90, 30.71, 40.90, 42.55, 41.28, 40.60, 27.02, 28.03, 29.30, 39.88]
avg_runtime = [0.054, 0.039, 0.035, 0.035, 0.034, 0.036, 0.037, 0.037, 0.036, 0.035]
lines = ["solid", "dashed", "dotted"]
colors = ["#00cc00", "#ff0066", "#ff3300", "#0066ff", "#0000cc", "#336699", "#6600ff", "#006666", "#663300", "#660033"]

def plotit(name_list):
    for i in xrange(len(name_list)):
        with open(name_list[i], 'rb') as f:
            reader = csv.reader(f)
            your_list = list(reader)
        # fig, ax = plt.subplots()
        data = map(float, your_list[0])
        l = str(name_list[i]).split(".")[0]
        ii = i % len(lines)
        plt.plot(data, label=l, linestyle=lines[ii], color=colors[i], lw=2.0)

    plt.legend(loc="top")
    plt.ylabel("Regret")
    plt.xlabel("Request Number")
    plt.title("Regret per Run ID")
    # plt.set_ylabel("Regret")
    # plt.set_title("Regret per Run ID")
    plt.savefig('regret_plot_lazy_thompson.png', format='png', dpi=400)

    plt.show()

def plotother(name):
    if name == "avg_reward":
        plt.plot(avg_reward)
    elif name == "num_suc":
        plt.plot(num_suc)
    elif name == "avg_suc_price":
        plt.plot(avg_suc_price)
    elif name == "avg_runtime":
        plt.plot(avg_runtime)

    plt.show()
    pass


def plotall(name, title, yaxis, color):
    pn = str(yaxis)
    N = 10
    ind = np.arange(N)  # the x locations for the groups
    width = 0.6  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, name, width, color=color)

    # add some text for labels, title and axes ticks
    ax.set_ylabel(yaxis)
    ax.set_title(title)
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(('5000', '5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009'))


    def autolabel(rects):
        # attach some text labels
        n=0
        for rect in rects:

            # height = rect.get_height()
            height = name[n]

            ax.text(rect.get_x() + rect.get_width() / 2., height,
                    str(float(height)),
                    ha='center', va='bottom')
            n += 1
    autolabel(rects1)
    plt.savefig(str(pn)+'.png', format='png', dpi=320)
    plt.show()
    pass



if __name__ == "__main__":
    # plotit("avg_success_price_5000.csv")
    # plotit("avg_success_price_5001.csv")
    # plotit("avg_success_price_5002.csv")
    # plotit("avg_success_price_5003.csv")
    # plotother("avg_reward")
    # plotall(avg_reward, "Mean Reward per Run ID", "Mean Reward", "#990033")
    # plotall(num_suc, "Number of Successful Serves per Run ID", "Number of Serves", "#b3003b")
    # plotall(avg_suc_price, "Average Successful per Run ID", "Price", "#cc0044")
    # plotall(avg_runtime, "Average Serving Time per Run ID", "Time", "#ff1a8c")
    plotit(["5000.csv", "5001.csv", "5002.csv", "5003.csv", "5004.csv", "5005.csv", "5006.csv", "5007.csv", "5008.csv", "5009.csv"])
    # plotit(["5000.csv"])
    pass