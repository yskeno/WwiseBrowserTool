#! python3
import tkinter
import tkinter.ttk as ttk
from pprint import pprint


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("State Browser Tool")
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.minsize(750, 220)

        # Variables.
        self.isautoupdate = tkinter.BooleanVar(value=True)
        self.isautosetstate = tkinter.BooleanVar(value=True)
        self.visibleonlyname = tkinter.BooleanVar(value=True)

        self._lbltxt_wproj_info = tkinter.StringVar()
        self._btntxt_connectwaapi = tkinter.StringVar()

        # { 'StateGroup' : {'Label' : LabelObject<StateGroupName>,
        #                   'ComboBox' : ComboBoxObject<StateName> }
        self.dict_statebrowser_object = {}
        # { 'StateGroup' : 'NewState' }
        self.dict_statebrowser_old = {}
        self.dict_statebrowser_changed = {}

        # Design Settings Frame.
        self.frame_settings = ttk.Labelframe(self,
                                             text="Settings",
                                             padding=3, border=1, relief="solid")
        self.frame_settings.grid(column=0, row=0, sticky="nw",
                                 padx=10, pady=3, ipadx=2, ipady=0)

        self.btn_updatestate = ttk.Button(self.frame_settings,
                                          text="Force Update",
                                          state='disabled',
                                          padding=3,
                                          command=lambda: print(
                                              self.isautoupdate.get()))
        self.btn_updatestate.grid(column=0, row=0, padx=3, pady=0)

        self.chk_autoupdate = ttk.Checkbutton(self.frame_settings,
                                              text="Auto Update State Browser",
                                              padding=3,
                                              variable=self.isautoupdate,
                                              )
        self.chk_autoupdate.grid(column=1, row=0, padx=3, pady=0)

        self.btn_setstate = ttk.Button(self.frame_settings,
                                       text="Set State", padding=3,
                                       state='disabled',
                                       command=lambda: print(
                                           self.isautosetstate.get()))
        self.btn_setstate.grid(column=2, row=0, padx=3, pady=0)

        self.chk_autosetstate = ttk.Checkbutton(self.frame_settings,
                                                text="Auto Set State When State Changed",
                                                padding=3,
                                                variable=self.isautosetstate)
        self.chk_autosetstate.grid(column=3, row=0, padx=3, pady=0)

        # Design Status Frame.
        self.frame_status = ttk.Labelframe(self,
                                           text="Connection Status",
                                           padding=3, border=1, relief="solid")
        self.frame_status.grid(column=0, row=2, sticky="sw",
                               padx=5, pady=3, ipadx=2, ipady=0,)

        self.btn_connectwaapi = ttk.Button(self.frame_status,
                                           textvariable=self._btntxt_connectwaapi,
                                           state='active',
                                           padding=3, width=10)
        self.btn_connectwaapi.pack(side="left")

        self.lbl_wproj_info = ttk.Label(self.frame_status,
                                        textvariable=self._lbltxt_wproj_info,
                                        padding=3)
        self.lbl_wproj_info.pack(side="left")

        # Design State Browser.
        self.frame_statebrowser = ttk.Labelframe(self,
                                                 text="State List",
                                                 padding=3, border=1, relief="solid")
        self.frame_statebrowser.grid(column=0, row=1, sticky="nsew",
                                     padx=10, pady=3, ipadx=2, ipady=0)

        # Design State Settings.
        self.frame_statesettings = ttk.Frame(self.frame_statebrowser,
                                             padding=3)
        self.frame_statesettings.grid(column=0, row=0, sticky="EW")

        self.chk_visibleonlyname = ttk.Checkbutton(self.frame_statesettings,
                                                   text="Visible Only StateGroup Name",
                                                   padding=3,
                                                   variable=self.visibleonlyname
                                                   )
        self.chk_visibleonlyname.grid(column=0, row=0, padx=3, pady=0)

        # Design State List.
        self.frame_statelist = ttk.Frame(self.frame_statebrowser,
                                         padding=3, border=1, relief="solid")
        self.frame_statelist.grid(column=0, row=1, sticky="NSEW")

        self.lbl_title_stategroup = ttk.Label(self.frame_statelist,
                                              text="StateGroup", width=25, anchor="center")
        self.lbl_title_stategroup.grid(column=0, row=0, sticky="EW")
        self.lbl_title_statename = ttk.Label(self.frame_statelist,
                                             text="State", width=50, anchor="center")
        self.lbl_title_statename.grid(column=1, row=0, sticky="EW")

        self.update_wproj_info()

    def show_connecting_message(self):
        self._lbltxt_wproj_info.set("Connecting to Wwise...")
        self.lbl_wproj_info.update()

    def update_wproj_info(self, isconnected=False, wprojinfo=""):
        if isconnected == True:
            self._lbltxt_wproj_info.set("Connected: " + wprojinfo)
            self._btntxt_connectwaapi.set("Disconnect")
            self.btn_connectwaapi['state'] = 'normal'
            self.btn_updatestate['state'] = 'normal'
            self.btn_setstate['state'] = 'normal'
        else:
            self._lbltxt_wproj_info.set(
                "NotConnected: Check Wwise is running and WAAPI is enabled.")
            self._btntxt_connectwaapi.set("Connect")
            self.btn_updatestate['state'] = 'disabled'
            self.btn_setstate['state'] = 'disabled'

    def clear_statebrowser(self):
        for stategroupname in self.dict_statebrowser_object.keys():
            self.dict_statebrowser_object[stategroupname]['Label'].destroy()
            self.dict_statebrowser_object[stategroupname]['ComboBox'].destroy()
        self.dict_statebrowser_object.clear()
        self.dict_statebrowser_changed.clear()

    def update_statebrowser(self, statedict: dict, currentstate_dict: dict):
        self.clear_statebrowser()
        self.dict_statebrowser_old = currentstate_dict
        # Create StateGroupName Label.
        for statedict_stategroup, statedict_statelist in statedict.items():

            self.dict_statebrowser_object.setdefault(
                statedict_stategroup, {})
            self.dict_statebrowser_object.get(
                statedict_stategroup, {}).setdefault(
                    'Label', ttk.Label(self.frame_statelist,
                                       text=statedict_stategroup,
                                       width=50, border=1, relief="solid"))

            combobox_values = []
            for i in statedict_statelist:
                combobox_values.append(i['name'])

            self.dict_statebrowser_object.get(
                statedict_stategroup, {}).setdefault(
                    'ComboBox', ttk.Combobox(self.frame_statelist,
                                             name=statedict_stategroup,
                                             state='readonly',
                                             width=50,
                                             values=combobox_values,))
            self.dict_statebrowser_object.get(statedict_stategroup, {}).get(
                'ComboBox').current(0)
            self.dict_statebrowser_object.get(statedict_stategroup, {}).get(
                'ComboBox').bind('<<ComboboxSelected>>', self.__add_changedstate_dict)

            for i in range(len(self.dict_statebrowser_object)):
                self.dict_statebrowser_object.get(statedict_stategroup, {}).get(
                    'Label').grid(column=0, row=i+1, sticky="EW")
                self.dict_statebrowser_object.get(statedict_stategroup, {}).get(
                    'ComboBox').grid(column=1, row=i+1, sticky="EW")

        self.update_current_state(currentstate_dict)

    def update_current_state(self, currentstate_dict: dict):
        for stategroup, currentstate in currentstate_dict.items():
            self.dict_statebrowser_object.get(stategroup, {}).get(
                'ComboBox').set(currentstate)

    def __add_changedstate_dict(self, event):
        if self.dict_statebrowser_old[event.widget._name] == event.widget.get():
            if event.widget._name in self.dict_statebrowser_changed.keys():
                del self.dict_statebrowser_changed[event.widget._name]
        else:
            self.dict_statebrowser_changed[event.widget._name] = event.widget.get(
            )

if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
