import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from scipy.stats import beta

timeline = np.genfromtxt('timeline-5003.csv', delimiter=',')

color_timeline = timeline[:, 0:10]
adtype_timeline = timeline[:, 10:16]
price_timeline = timeline[:, 16:38]

color_timeline = color_timeline.reshape((10000, 2, 5))
adtype_timeline = adtype_timeline.reshape((10000, 2, 3))
price_timeline = price_timeline.reshape((10000, 2, 11))

x = np.linspace(0, 1.0, 1000)

xlim = 1000

initial_pdf = beta.pdf(x, 1, 1)

fig, axes = plt.subplots(nrows=2, ncols=2)

# lines = plt.plot(x, skyscraper, "-", x, square, "r--", x, banner, "g--")
skyscrapper_plot, = axes[0, 0].plot(x, initial_pdf, "b-", label="skyscraper")
square_plot, = axes[0, 0].plot(x, initial_pdf, "r-", label="square")
banner_plot, = axes[0, 0].plot(x, initial_pdf, "g-", label="banner")

red_plot, = axes[1, 0].plot(x, initial_pdf, "r-", label="red")
green_plot, = axes[1, 0].plot(x, initial_pdf, "g-", label="green")
blue_plot, = axes[1, 0].plot(x, initial_pdf, "b-", label="blue")
black_plot, = axes[1, 0].plot(x, initial_pdf, "k-", label="black")
white_plot, = axes[1, 0].plot(x, initial_pdf, "m-", label="white")

prices = np.array([49.99, 44.99, 39.99, 34.99, 29.99, 24.99, 19.99, 15.99, 9.99, 5.99, 0.99])
price_multipliers = np.log(prices)
price_plot_styles = ['b-.', 'g-.', 'r-.', 'm-.', 'b--', 'g--', 'r--', 'm--', 'b:', 'g:', 'r:', 'm:']
price_plots = []

cumulative_regret_data = np.zeros(10000)
cumulative_regret_plot, = axes[1, 1].plot(range(0, 10000), cumulative_regret_data, "k-", label="Cumulative Regret")

for i in range(0, len(prices)):
    price_plot, = axes[0, 1].plot(x, initial_pdf, price_plot_styles[i], label=str(prices[i]), linewidth=2.0)
    price_plots.append(price_plot)

axes[0, 0].legend(loc="upper left", prop={'size': 9})
axes[1, 0].legend(loc="upper left", prop={'size': 9})
axes[0, 1].legend(loc="upper left", prop={'size': 8})
axes[1, 1].legend(loc="upper left", prop={'size': 9})

axes[0, 0].set_title("(Log)Beta Dist - Ad Type")
axes[0, 1].set_title("(Log)Beta Dist - Price")
axes[1, 0].set_title("(Log)Beta Dist - Color")
axes[1, 1].set_title("Cumulative Regret")


def run(index):
    def draw(a, b, plot, multiplier=1):
        beta_pdf = beta.pdf(x, a, b) * multiplier
        plot.set_ydata(beta_pdf)
        return beta_pdf

    skyscrapper_beta = draw(adtype_timeline[index, 0, 0], adtype_timeline[index, 1, 0], skyscrapper_plot)
    square_beta = draw(adtype_timeline[index, 0, 1], adtype_timeline[index, 1, 1], square_plot)
    banner_beta = draw(adtype_timeline[index, 0, 2], adtype_timeline[index, 1, 2], banner_plot)

    axes[0, 0].set_ylim(0, np.max((np.max(skyscrapper_beta), np.max(square_beta), np.max(banner_beta))))

    green_beta = draw(color_timeline[index, 0, 0], color_timeline[index, 1, 0], green_plot)
    blue_beta = draw(color_timeline[index, 0, 1], color_timeline[index, 1, 1], blue_plot)
    red_beta = draw(color_timeline[index, 0, 2], color_timeline[index, 1, 2], red_plot)
    black_beta = draw(color_timeline[index, 0, 3], color_timeline[index, 1, 3], black_plot)
    white_beta = draw(color_timeline[index, 0, 4], color_timeline[index, 1, 4], white_plot)
    axes[1, 0].set_ylim(0, np.max((
        np.max(green_beta),
        np.max(blue_beta),
        np.max(red_beta),
        np.max(black_beta),
        np.max(white_beta))))

    max_price_y = 0

    for i in range(0, len(prices)):
        price_beta = draw(price_timeline[index, 0, i], price_timeline[index, 1, i], price_plots[i],
                          multiplier=price_multipliers[i])
        max_price_y = np.max((np.max(price_beta), max_price_y))
    axes[0, 1].set_ylim(0, max_price_y)
    if index == 50:
        for ax in axes.flatten():
            ax.patch.set_facecolor('white')

    cumulative_regret_data[0: index + 1] = np.sum(color_timeline[0: index + 1, 1, :], axis=1) - 5
    cumulative_regret_plot.set_data(range(0, index + 1), cumulative_regret_data[0:index + 1])

    if index > 1000:
        axes[1, 1].set_xlim(0, index)


def init():
    for ax in axes.flatten():
        ax.grid()
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)
        ax.patch.set_facecolor('cyan')
    axes[1, 1].set_ylim(0, 300)
    axes[1, 1].set_xlim(0, 1000)
    axes[0, 0].set_yscale("log", nonposy='clip')
    axes[0, 1].set_yscale("log", nonposy='clip')
    axes[1, 0].set_yscale("log", nonposy='clip')


r = range(0, 50)
r.extend(range(50, 10000, 20))
ani = animation.FuncAnimation(fig, run, r, blit=False, interval=10,
                              repeat=False, init_func=init)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=20, metadata=dpast_failuresict(artist='Me'), bitrate=5400)
ani.save("adtype.mp4", writer=writer)
# plt.show()
