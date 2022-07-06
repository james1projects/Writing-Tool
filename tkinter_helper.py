"""Tkinter Helper.

Used to make creating tkinter widgets easier.
"""
import tkinter
from tkinter import ttk, VERTICAL, Text
from tkinter import WORD, StringVar, Listbox
from tkinter import messagebox, PhotoImage
from tkinter import IntVar, Grid, Toplevel
from tkinter import Frame, END
from tkinter import font
from tkinter import TclError
# pylint: disable=too-many-instance-attributes


class TkinterHelper():
    """Used to make creating tkinter widgets easier."""

    def __init__(self, frame):
        """Initialize variables for TkinterHelper."""
        self.options_dictionary = {"row": 0,
                                   "column": 0,
                                   "rowspan": 1,
                                   "columnspan": 1,
                                   "frame": frame,
                                   "sticky": "",
                                   "padx": 6,
                                   "pady": 6,
                                   "string_var": None,
                                   "text_height": 10,
                                   "text_width": 10,
                                   "listbox_height": 10,
                                   "listbox_width": 30,
                                   "width": 25,
                                   "font_size": 20}

    def next_row(self, starting_column=0):
        """Move to next row and resets column.

        Parameters
        ----------
        starting_column: int, optional
            The column to reset to. The default is 0.
        """
        self.options_dictionary["row"] = self.options_dictionary["row"] + 1
        self.reset_column(column=starting_column)

    def next_column(self, columns_to_skip=1):
        """Move to next column."""
        self.options_dictionary["column"] = self.options_dictionary["column"] + columns_to_skip

    def reset_column(self, column=0):
        """Reset the column.

        Parameters
        ----------
        column : int, optional
            DESCRIPTION. The default is 0.
        """
        self.options_dictionary["column"] = column

    def create_scrollbar_grid(self, function, orient=VERTICAL):
        """Create a ttk scrollbar that is grided.

        Parameters
        ----------
        command : function, optional
            function for the scrollbar.
        orient : ENUM, optional
            VERTICAL/HORIZONTAL. The orientation of the scrollbar.
            The default is VERTICAL.

        Returns
        -------
        scrollbar_new : ttk.Scrollbar
            Newly created Scrollbar object.
        """
        opt = self.options_dictionary
        scrollbar_new = ttk.Scrollbar(opt["frame"], orient=opt["orient"], command=opt["function"],
                                      y_scroll_command=None)
        scrollbar_new.grid(row=opt["row"], column=opt["column"],
                           rowspan=opt["rowspan"],
                           columnspan=opt["columnspan"], sticky=opt["sticky"])

        return scrollbar_new

    def create_checkbox_grid(self, text, int_var, function):
        """Create a ttk checkbox that is grided.

        Parameters
        ----------
        text : String
            String for the label of checkbox.
        int_var : IntVar
            IntVar that keeps track of checkbox state.
        function : function
            function to be run when checkbox is clicked.

        Returns
        -------
        checkbox_new : ttk.Checkbutton
            The new checkbox.

        """
        opt = self.options_dictionary
        checkbox_new = ttk.Checkbutton(opt["frame"], text=text, variable=int_var,
                                       command=function)
        checkbox_new.grid(row=opt["row"], column=opt["column"], pady=opt["pady"],
                          padx=opt["padx"], sticky=opt["sticky"])

        return checkbox_new

    def create_button_grid(self, text, function):
        """Create a ttk button that is grided.

        Parameters
        ----------
        text : String
            Text on the button.
        command : function
            function to be run.

        Returns
        -------
        button_new : ttk.Button
            The new Button.

        """
        opt = self.options_dictionary
        button_new = ttk.Button(opt["frame"], text=text, command=function)
        button_new.grid(sticky=opt["sticky"], row=opt["row"], column=opt["column"], pady=opt["pady"],
                        padx=opt["padx"], rowspan=opt["rowspan"], columnspan=opt["columnspan"])
        button_new.configure(width=opt["width"])

        return button_new

    def create_label_grid(self, text=""):
        """Create a ttk Label.

        Parameters
        ----------
        text : String, optional
            Text on the Label.
            The default is "".

        Returns
        -------
        label_new : ttk.Label
            The new Label.

        """
        opt = self.options_dictionary
        label_new = ttk.Label(opt["frame"], text=text)
        label_new.grid(sticky=opt["sticky"], row=opt["row"], column=opt["column"], rowspan=opt["rowspan"],
                       columnspan=opt["columnspan"], pady=opt["pady"], padx=opt["padx"])
        label_new.config(font=(label_new.cget("font"),
                               opt["font_size"]))
        return label_new

    def create_entry_grid(self, text="", entry_changed_function=None, validate_function=None):
        """Create entry that is grided.

        Parameters
        ----------
        text : String, optional
            Text on entry. The default is "".
        entry_changed_function : TYPE, optional
            Function to be run if the entry is changed. The default is True.

        Returns
        -------
        entry_new : ttk.Entry
            The new Entry.

        """
        opt = self.options_dictionary
        if (validate_function is not None):
            print("added validate command for entry")
            vcmd = (opt['frame'].register(validate_function),
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            entry_new = ttk.Entry(opt["frame"], width=opt["width"],
                                  validatecommand=vcmd, validate="key")
        else:
            entry_new = ttk.Entry(opt["frame"], width=opt["width"])
        entry_new.grid(row=opt["row"], column=opt["column"], rowspan=opt["rowspan"],
                       columnspan=opt["columnspan"])
        entry_new.insert(0, text)

        # if entry_changed_function is not None:
        #     string_var = StringVar()
        #     string_var.trace("w", lambda name, index, mode, sv=string_var:
        #                           entry_changed_function(sv))
        #     entry_new.config(textvariable=string_var)

        return entry_new

    def create_text_grid(self):
        """Create tkinter Text that is grided.

        Returns
        -------
        text_new : tkinter Text
            The new Text.
        """
        opt = self.options_dictionary
        text_new = Text(opt["frame"], opt["text_height"], width=opt["width"])
        text_new.configure(state="normal", wrap=WORD)
        text_new.grid(row=opt["row"], column=opt["column"], rowspan=opt["rowspan"], sticky=opt["sticky"],
                      columnspan=opt["columnspan"], padx=opt["padx"], pady=opt["pady"])

        return text_new

    def create_listbox_grid(self, select_function=None):
        """Create listbox that is grided.

        Parameters
        ----------
        select_function : function, optional
            Function to be ran when listbox has a selection made.
            The default is None.

        Returns
        -------
        listbox_new : tkinter Listbox
            tkinter Listbox object.
        """
        opt = self.options_dictionary
        listbox_new = Listbox(opt["frame"], height=opt["listbox_height"], width=opt["listbox_width"], selectmode=tkinter.SINGLE)
        if select_function is not None:
            listbox_new.bind('<<ListboxSelect>>', select_function)
        listbox_new.grid(row=opt["row"], column=opt["column"], rowspan=opt["rowspan"],
                         columnspan=opt["columnspan"], sticky=opt["sticky"])

        return listbox_new


class Window:
    """Window object for tkinter."""

    # The tk top level window. Closing this closes everything.
    tk_root = None

    # The tk window we are currently using.
    tk_window = None

    # The tk frame we are currently using.
    tk_frame = None

    def __init__(self, o_parent, title, create_window):
        print("Window init", title, create_window)
        self.o_parent = o_parent
        if o_parent is not None:
            self.tk_root = o_parent.tk_root
        else:
            self.tk_root = None

        if create_window:
            self.create_window(self.tk_root)

        self.tk_frame = self.tk_window
        if title != "":
            self.tk_window.title(title)

    def main_loop(self):
        """Enter main loop for program logic."""
        # Start the mainloop of the window...
        print("Entering window loop...")
        while (True):
            try:
                self.tk_root.update()
                self.tk_root.update_idletasks()
            except TclError:
                print("TclError. Closing application.")
                break

        print("End of main loop.")

    def create_window(self, tk_root):
        """Create a new tkinter window for this object."""
        self.tk_root = tk_root
        if tk_root is None:
            # For main window, the root and window are the same.
            self.tk_root = tkinter.Tk()
            self.tk_window = self.tk_root
        else:
            self.tk_window = Toplevel(self.o_parent.tk_window)

        self.tk_root.tk.call("source", "sun-valley.tcl")
        self.tk_root.tk.call("set_theme", "dark")
        # self.set_window_image()

        # Set the function for when clicking the x to close the window.
        self.tk_window.wm_protocol("WM_DELETE_WINDOW", self.close_window)
        self.tk_window.lift()

        Grid.rowconfigure(self.tk_window, 1, weight=1)
        Grid.columnconfigure(self.tk_window, 1, weight=1)

    def set_window_image(self):
        """Set window image."""
        # TODO: add functionality for image
        # config = HatBotConfig.HatBotConfig()
        # path_image_hat = config.loadOption(config.SECTION_SETTINGS,
        #                                    config.PATH_ICON_HAT)
        # if os.path.exists(path_image_hat):
        #     image_hat = PhotoImage(file=path_image_hat)
        #     self.window.tk.call('wm', 'iconphoto', self.window._w, image_hat)
        pass

    def close_window(self):
        """Close window."""
        print("Closing window from Window class.")
        self.tk_window.destroy()
