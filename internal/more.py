from typing import Literal, Union, List, Tuple
import dearpygui.dearpygui as dpg
from . import layout
import traceback

#+----------------------------------------------------------------+
#|                           MORE DATA                            |
#+----------------------------------------------------------------+

#=========== MoreData ===========
#Almacena los datos necesarios para la ejecucion del layout
class MoreData():
    def __init__(self):
        self._execute_after = []
        self._window_loader = ()

    #============ EXECUTE AFTER ============
    def add_execute_after(self, callback):
        self._execute_after.append(callback)

    def get_execute_after(self):
        return self._execute_after

    #=========== WINDOW LOADER ============
    def add_window_loader(self, tag, tag_primary_window, color, secondary_color):
        self._window_loader = (tag, tag_primary_window, color, secondary_color)

    def get_window_loader(self):
        return self._window_loader

    #============== CLEAR LAYOUT ==============
    def clear_data_execute_after(self):
        self._execute_after.clear()

more_data = MoreData()

#+----------------------------------------------------------------+
#|                             MORE                               |
#+----------------------------------------------------------------+

def execute_after():
    callbacks = more_data.get_execute_after()
    for call in callbacks:
        call()
    more_data.clear_data_execute_after()

def execute_loader():
    data_window_loader = more_data.get_window_loader()
    if data_window_loader:
        def _main():
            size_primary_window = dpg.get_item_rect_size(data_window_loader[1])
            with dpg.window(modal=True, 
                            no_resize=True, 
                            no_collapse=True, 
                            no_title_bar=True, 
                            no_move=True,
                            width=size_primary_window[0], 
                            height=size_primary_window[1],
                            tag=data_window_loader[0]
                            ):
                dpg.add_loading_indicator(pos=(10,10), color=data_window_loader[2], secondary_color=data_window_loader[3])
            layout.ExecuteLayout()
        layout.wait_rendering([data_window_loader[1]], _main)
    else:
        layout.ExecuteLayout()