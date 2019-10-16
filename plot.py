#!/usr/bin/env python3

import pandas
import matplotlib.pyplot as plt
import numpy as np

DATA_SPEED_DS_FILE = "data/July19_myspeed.csv"
AIR_TRAFFIC_DS_FILE = "data/Totaldom17_Monthly_SCHEDULED_DOMESTIC_2017.csv"

BOX_PLOT_FILE = "plots/box.png"
SCATTER_PLOT_FILE = "plots/scatter.png"
BAR_CHART_FILE = "plots/bar.png"


def draw_scatter_plot():
    plt.figure()
    air_traffic_df = pandas.read_csv(AIR_TRAFFIC_DS_FILE)
    air_traffic_df = air_traffic_df[:-1]
    hours = list(air_traffic_df["AIRCRAFT FLOWN - HOURS (IN NUMBER)"] / 1000)
    distance = list(
        air_traffic_df["AIRCRAFT FLOWN - KILOMETRE (IN THOUSAND)"] / 1000)
    plt.scatter(hours, distance)
    plt.xlabel("Total hours flown in a month (1000 hours)")
    plt.ylabel("Total distance covered in a month  (1000 Kms)")
    plt.title("Monthly distance covered vs hours flown for\n"
              "scheduled domestic Indian flights in 2017")
    plt.tight_layout()
    plt.savefig(SCATTER_PLOT_FILE, dpi=300)


def draw_box_plot():
    plt.figure()
    data_speed_df = pandas.read_csv(DATA_SPEED_DS_FILE)
    data_speed_df = data_speed_df.query("technology == '4G'").query(
        "Download_Upload == 'download'")
    service_providers = data_speed_df.Service_provider.unique()
    speeds = {}
    for sp in service_providers:
        speeds[sp] = list(
            data_speed_df.query("Service_provider == '" + sp +
                                "'")["Data_Speed.Kbps."] / (1024 * 8))
    plt.boxplot([speeds[sp] for sp in service_providers], 0, None)
    plt.xticks([y + 1 for y in range(len(service_providers))],
               service_providers)
    plt.xlabel("Service providers")
    plt.ylabel("4G Download speed (MB/s)")
    plt.title("4G data speeds in India for July, 2019")
    plt.tight_layout()
    plt.savefig(BOX_PLOT_FILE, dpi=300)


def draw_bar_chart():
    plt.figure()
    data_speed_df = pandas.read_csv(DATA_SPEED_DS_FILE)
    techs = data_speed_df.technology.unique()
    bar_width = 0.35
    num_service_providers = -1
    service_providers = None
    ind = None
    num = 0
    for tech in techs:
        filtered_df = data_speed_df.query(
            "technology == '" + tech +
            "'").query("Download_Upload == 'download'").query(
                "Service_provider != 'JIO'").query(
                    "Service_provider != 'DOLPHIN'")
        processed_df = filtered_df.groupby(["Service_provider"]).mean()
        service_providers = processed_df.index.values
        means = list(processed_df["Data_Speed.Kbps."]/(1024 * 8))
        num_service_providers = len(service_providers)
        ind = np.arange(num_service_providers)
        plt.bar(ind + num * bar_width, means, bar_width, label=tech)
        num += 1
    plt.xticks(ind + bar_width / 2, service_providers)
    plt.legend(loc='best')
    plt.xlabel("Service providers")
    plt.ylabel("Average download speed (MB/s)")
    plt.title("Data speeds in India for July, 2019")
    plt.tight_layout()
    plt.savefig(BAR_CHART_FILE, dpi=300)


if __name__ == "__main__":
    draw_scatter_plot()
    draw_box_plot()
    draw_bar_chart()
