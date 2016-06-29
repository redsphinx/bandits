import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from scipy.stats import beta

timeline = np.genfromtxt('timeline.csv', delimiter=',')

color_timeline = timeline[:, 0:10]
adtype_timeline = timeline[:, 10:16]
price_timeline = timeline[:, 16:38]

color_timeline = color_timeline.reshape((10000, 2, 5))
adtype_timeline = adtype_timeline.reshape((10000, 2, 3))
price_timeline = price_timeline.reshape((10000, 2, 11))

x = np.linspace(0, 1.0, 100)

initial_pdf = beta.pdf(x, 1, 1)

fig, axes = plt.subplots(nrows=2, ncols=2)

# lines = plt.plot(x, skyscraper, "-", x, square, "r--", x, banner, "g--")
skyscrapper_plot, = axes[0, 0].plot(x, initial_pdf, "b-")
square_plot, = axes[0, 0].plot(x, initial_pdf, "r-")
banner_plot, = axes[0, 0].plot(x, initial_pdf, "g-")

red_plot, = axes[1, 0].plot(x, initial_pdf, "r-")
green_plot, = axes[1, 0].plot(x, initial_pdf, "g-")
blue_plot, = axes[1, 0].plot(x, initial_pdf, "b-")
black_plot, = axes[1, 0].plot(x, initial_pdf, "k-")
white_plot, = axes[1, 0].plot(x, initial_pdf, "m-")


def run(index):
    def draw(a, b, plot):
        beta_pdf = beta.pdf(x, a, b)
        plot.set_ydata(beta_pdf)
        return beta_pdf

    skyscrapper_beta = draw(adtype_timeline[index, 0, 0], adtype_timeline[index, 1, 0], skyscrapper_plot)
    square_beta = draw(adtype_timeline[index, 0, 1], adtype_timeline[index, 1, 1], square_plot)
    banner_beta = draw(adtype_timeline[index, 0, 2], adtype_timeline[index, 1, 2], banner_plot)

    axes[0, 0].set_ylim(0, np.max((np.max(skyscrapper_beta), np.max(square_beta), np.max(banner_beta))))
    if index == 50:
        for ax in axes.flatten():
            ax.patch.set_facecolor('white')


def init():
    for ax in axes.flatten():
        ax.grid()
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)
        ax.patch.set_facecolor('cyan')


r = range(0, 50)
r.extend(range(50, 10000, 12))
ani = animation.FuncAnimation(fig, run, r, blit=False, interval=10,
                              repeat=False, init_func=init)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("adtype.mp4", writer=writer)
plt.show()
