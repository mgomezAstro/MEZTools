import numpy as np
import dearpygui.dearpygui as dpg
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


dpg.create_context()
dpg.create_viewport(title="MEZTools", width=800, height=600)


def open_file(sender, app_data):
    data, hdr = fits.getdata(app_data["file_path_name"], header=True)
    if hdr.get("MZTOOL", 0) == 0 or hdr.get("MZTOOL", 0) == "N":
        open_raw_data(data)
    else:
        open_pv_data()


def open_raw_data(kk):
    print("Enter to raw data")
    data = np.random.rand(200, 200)
    with dpg.plot(label="Raw 2D image"):
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.add_heat_series(data, 0, 200, 0, 200)





def open_pv_data():
    pass


def primary_menu_bar():
    with dpg.file_dialog(directory_selector=False, show=False, callback=open_file, id="open file", width=500, height=300):
        dpg.add_file_extension(".fits")

    with dpg.menu_bar(label="Primary menu bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open", callback= lambda: dpg.show_item("open file"))
            dpg.add_menu_item(label="Close")


with dpg.window(label="Raw data", tag="Primary Window"):
    primary_menu_bar()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
