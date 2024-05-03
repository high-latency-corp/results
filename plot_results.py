import matplotlib.pyplot as plt
import pandas as pd

folders = ["cubic", "ledbat", "hybla", "bbr"]

colours ={"cubic" : "red", "ledbat" : "blue", "hybla": "purple", "bbr" : "green"}
ls ={"cubic" : "-", "ledbat" : "--", "hybla": "-.", "bbr" : ":"}
lines ={"cubic": "solid", "ledbat" : "dashed", "32K": "dotted"}

points = {"cubic" : "o", "ledbat" : "v", "hybla" : "X", "bbr" : "*"}

units = {"rtt": "(s)", "cwnd": "(pkts)", "Rx": "pkts", "throughput": "(Mbps)", "average throughput" : "(Mbps)"}

lw ={"cubic" : 4, "ledbat" : 3, "hybla": 2, "bbr" : 2}

def plot(data, name):
    for key, value in data.items():
            xk, xv = list(value.items())[0]
            yk, yv = list(value.items())[1]
            plt.plot(xv, yv, marker=points[key], linestyle=ls[key], linewidth=lw[key], ms="3", label=key, alpha=0.7)
            plt.xlabel(xk)
            plt.ylabel(f"{yk} {units[yk]}")
    plt.legend(loc="best")
    plt.grid()
    name = f"{name}.png"
    plt.savefig(name, bbox_inches='tight')
    plt.show()


def broken_plot(data, name):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0.05)  # adjust space between axes
    for key, value in data.items():
        xk, xv = list(value.items())[0]
        yk, yv = list(value.items())[1]
        # plot the same data on both axes
        ax1.plot(xv, yv, marker=points[key], linestyle=ls[key], linewidth=lw[key], ms="3", label=key, alpha=0.7)
        ax2.plot(xv, yv, marker=points[key], linestyle=ls[key], linewidth=lw[key], ms="3", label=key, alpha=0.7)
        plt.xlabel(xk)
        plt.ylabel(f"{yk} {units[yk]}")
    # zoom-in / limit the view to different portions of the data
    ax1.set_ylim(100000, 700000)  # outliers only
    ax2.set_ylim(0, 10000)  # most of the data

    # hide the spines between ax and ax2
    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    # Now, let's turn towards the cut-out slanted lines.
    # We create line objects in axes coordinates, in which (0,0), (0,1),
    # (1,0), and (1,1) are the four corners of the axes.
    # The slanted lines themselves are markers at those locations, such that the
    # lines keep their angle and position, independent of the axes size or scale
    # Finally, we need to disable clipping.

    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
    ax1.legend(loc="best")
    ax1.grid()
    ax2.grid()
    name = f"{name}.png"
    plt.savefig(name, bbox_inches='tight')
    plt.show()


def get_dataframe(path, cols, delimiter="\t"):
    return pd.read_csv(path, delimiter=delimiter, names=cols, header=None)

def plot_rtt():
    results = {}
    for folder in folders:
        df = get_dataframe(f"{folder}/clientQUIC-rtt2.txt", ["time", "oldrtt", "newrtt"])
        xs = list(df["time"])
        ys = list(df["newrtt"])
        xs.insert(0, 0)
        ys.insert(0, df["oldrtt"][0])
        results[folder]= {"time" : xs, "rtt": ys}
    plot(results, "rtt")


def plot_cwnd():
    results = {}
    for folder in folders:
        df = get_dataframe(f"{folder}/clientQUIC-cwnd-change2.txt", ["time", "oldcwnd", "newcwnd"])
        xs = list(df["time"])
        ys = list(df["newcwnd"])
        xs.insert(0, 0)
        ys.insert(0, df["oldcwnd"][0])
        results[folder]= {"time" : xs, "cwnd": ys}
    broken_plot(results, "cwnd")

def plot_server_rx():
    results = {}
    for folder in folders:
        df = get_dataframe(f"{folder}/serverQUIC-rx-data3.txt", ["time", "Rx"])
        xs = list(df["time"])
        ys = list(df["Rx"])
        results[folder]= {"time" : xs, "Rx": ys}
    plot(results, "rx")


def plot_throughput():
    results = {}
    for folder in folders:
        df = get_dataframe(f"{folder}/sinkTput.csv", ["time", "mbps"], delimiter=",")
        xs = list(df["time"])
        ys = list(df["mbps"])
        results[folder]= {"time" : xs, "throughput": ys}
    plot(results, "throughput")

def plot_bar(data, ylabel):
           
    plt.bar(data.keys(), data.values(), color ='maroon', 
        width = 0.4) 
    plt.xlabel("CCA Algorithm")
    plt.ylabel(f"{ylabel} {units[ylabel]}")
    name = f"{ylabel.replace(" ", "_")}_bar.png"
    plt.savefig(name, bbox_inches='tight')
    plt.show()

def plot_average_throughput():
    data = {"hybla": 0.324769, "ledbat":  0.324769, "cubic": 0.460166 , "bbr": 0.215639 }
    plot_bar(data, "average throughput")

plot_rtt()
plot_cwnd()
plot_server_rx()
plot_throughput()
plot_average_throughput()