"""
Amanda's Writing Tool.

Created on Sat Jul  2 15:53:31 2022.

@author: james
"""
import json
import os
import tkinter
import tkinter_helper
from tkinter import LabelFrame
from tkinter_helper import Window
from tkinter import Grid


class Project_Manager_Window(Window):
    """
    Project window where you can create new, edit, or delete projects.

    Should show project name with some stats such as pages, words etc..
    """
    projects_dictionary = {}
    PROJECT_TITLE = "project_title"

    def __init__(self):
        """Init method for Project_Window."""
        print("Project_Window __init__")
        self.project_num = 0
        self.projects_dictionary = {}
        self.selected_index = None
        self.tk_selected_frame = None
        Window.__init__(self, o_parent=None, title="Project Window", create_window=True)
        self.tk_project_frame = LabelFrame(self.tk_window, text="Amanda's Writing Tool: Project Manager", pady=20, padx=20)
        self.tk_project_frame.grid()
        self.tk_frame = self.tk_project_frame
        Grid.rowconfigure(self.tk_window, 1, weight=1)
        Grid.columnconfigure(self.tk_window, 1, weight=1)

        self.initialize_interface()

    def initialize_interface(self):
        tk_helper = tkinter_helper.TkinterHelper(self.tk_project_frame)
        tk_helper.options_dictionary["columnspan"] = 5
        tk_helper.options_dictionary["width"] = 100
        tk_helper.options_dictionary["column"] = 0
        tk_helper.options_dictionary["padx"] = 3
        tk_helper.options_dictionary["pady"] = 3
        tk_helper.options_dictionary["sticky"] = "NSWE"
        self.btn_new = tk_helper.create_button_grid("New", self.button_create_new_action)

    def button_create_new_action(self):
        grid_info = self.btn_new.grid_info()
        print("grid_info for button_new:", grid_info)
        self.btn_new.grid(row=grid_info["row"] + 1, column=grid_info["column"])

        new_project = self.Project(self, self.tk_project_frame, "New Project (" + str(self.project_num) + ")", grid_info["row"],
                                   grid_info["column"])
        self.projects_dictionary[str(self.project_num)] = new_project
        self.project_num += 1

    class Project(Window):
        COLUMN_EDIT = 0
        COLUMN_DELETE = 1
        COLUMN_PROJECT_TITLE = 2

        def __init__(self, o_parent, tk_frame, title, row, column):
            self.o_parent = o_parent
            self.title = title
            self.tk_frame = tk_frame
            self.row = row
            tk_frame.bind("<Button-1>", self.clicked)

            tk_helper = tkinter_helper.TkinterHelper(self.tk_frame)
            tk_helper.options_dictionary["row"] = row
            tk_helper.options_dictionary["sticky"] = "W"
            tk_helper.options_dictionary["width"] = "10"
            tk_helper.options_dictionary["padx"] = 5
            # Create edit button
            self.btn_edit = tk_helper.create_button_grid("Edit", self.button_edit_action)
            tk_helper.next_column()
            self.btn_delete = tk_helper.create_button_grid("Delete", self.button_delete_action)
            tk_helper.next_column()
            tk_helper.options_dictionary["width"] = "80"
            tk_helper.options_dictionary["columnspan"] = 3
            self.entry_project_title = tk_helper.create_entry_grid(title)

        def button_edit_action(self):
            self.isSelected = True
            self.o_parent.selected_index = self.row
            print(self.o_parent.selected_index, self.title, "is now selected.")
            self.o_parent.tk_selected_object = Project_Info_Window(self, self.entry_project_title.get(), True)

        def button_delete_action(self):
            pass

        def clicked(self, event):
            print("The user clicked at coordinates", event.x, event.y, "Which is grid:",
                  self.tk_frame.grid_location(event.x, event.y))

    def clicked(self, event):
        print("The user clicked at coordinates", event.x, event.y, "Which is grid:",
              self.tk_window.grid_location(event.x, event.y))


def main():
    """Start main function for writing_tool_gui.py."""
    print("Starting", os.path.basename(__file__), "as main file..")
    main_window = Project_Manager_Window()
    main_window.main_loop()


class Project_Info_Window(Window):
    total_chapters = 0
    selected_chapter_index = None
    chapters_list = []
    current_chapter_info = None
    CHAPTER_TITLE = "chapter_title"
    CHAPTER_INDEX = "chapter_index"
    CHAPTER_PAGES = "chapter_total_pages"  # Stored as String
    CHAPTER_WORDS = "chapter_total_words"  # Stored as String
    CHAPTER_INFO_COLUMN = 3

    def __init__(self, o_parent, project_title, create_window):
        print("Project_Info_Window __init__")
        Window.__init__(self, o_parent, project_title, create_window)
        print("INIT IN PROJECT INFO WINDOW ", self.tk_window)
        tk_helper = tkinter_helper.TkinterHelper(self.tk_window)
        self.tk_frame = self.tk_window

        tk_helper.options_dictionary["sticky"] = "NSWE"
        tk_helper.create_label_grid(project_title)
        tk_helper.next_column()
        tk_helper.options_dictionary["rowspan"] = 5
        tk_helper.options_dictionary["row"] = 0
        tk_helper.options_dictionary["columnspan"] = 2
        self.listbox_chapters = tk_helper.create_listbox_grid(select_function=self.listbox_chapters_select_action)
        tk_helper.options_dictionary["row"] = 4
        tk_helper.next_row(starting_column=1)
        tk_helper.options_dictionary["rowspan"] = 1
        tk_helper.options_dictionary["columnspan"] = 1
        tk_helper.options_dictionary["width"] = 20
        self.button_new_chapter = tk_helper.create_button_grid("New Chapter", self.new_chapter_action)
        tk_helper.next_column()
        self.button_delete_chapter = tk_helper.create_button_grid("Delete Chapter", self.delete_chapter_action)
        tk_helper.options_dictionary["row"] = 0
        tk_helper.options_dictionary["column"] = self.CHAPTER_INFO_COLUMN
        tk_helper.options_dictionary["columnspan"] = 2
        self.entry_chapter_title = tk_helper.create_entry_grid("")
        tk_helper.next_row(self.CHAPTER_INFO_COLUMN)
        tk_helper.options_dictionary["font_size"] = 15
        tk_helper.options_dictionary["columnspan"] = 1
        self.label_chapter_words = tk_helper.create_label_grid("Words:")
        tk_helper.next_column()
        self.entry_chapter_words = tk_helper.create_entry_grid("",
                                                               validate_function=self.entry_validate_numbers_only)
        tk_helper.next_row(self.CHAPTER_INFO_COLUMN)
        self.label_chapter_pages = tk_helper.create_label_grid("Pages:")
        tk_helper.next_column()
        self.entry_chapter_pages = tk_helper.create_entry_grid("",
                                                               validate_function=self.entry_validate_numbers_only)
        # Load chapters to Listbox
        self.load_chapters_to_listbox()

        Grid.rowconfigure(self.tk_window, 1, weight=1)
        Grid.columnconfigure(self.tk_window, 1, weight=1)

    def entry_validate_numbers_only(self, d, i, P, s, S, v, V, W):
        """
        Validate that only numbers are being entered into the entry.

        Parameters
        ----------
        d : int
            Action Code. 0 for an attempted deletion, 1 for an attempted insertion,
            or -1 if the callback was called for focus in, focus out, or a change to the
            textvariable.
        i : int
            When the user attempts to insert or delete text, this argument will
            be the index of the beginning of the insertion or deletion. If the
            callback was due to focus in, focus out, or a change to the
            textvariable, the argument will be -1.
        P : String
            The value that the text will have if the change is allowed.
        s : String
            The text in the entry before the change.
        S : String
            If the call was due to an insertion or deletion, this argument will
            be the text being inserted or deleted.
        v : String
            The current value of the widget’s validate option.
        V : String
            The reason for this callback: one of 'focusin', 'focusout', 'key',
            or 'forced' if the textvariable was changed.
        W : String
            The name of the widget.

        Returns
        -------
        bool
            True if numbers only, False otherwise.

        """
        if i:
            try:
                int(S)
                return True
            except ValueError:
                return False
        else:
            return False

    def new_chapter_action(self):
        """Create a new chapter."""
        chapter_info_dictionary = {}
        chapter_name = "New Chapter" + " " + str(self.total_chapters)
        chapter_info_dictionary[self.CHAPTER_TITLE] = chapter_name
        chapter_info_dictionary[self.CHAPTER_INDEX] = self.total_chapters
        chapter_info_dictionary[self.CHAPTER_WORDS] = ""
        chapter_info_dictionary[self.CHAPTER_PAGES] = ""
        self.total_chapters += 1
        self.listbox_chapters.insert(tkinter.END, chapter_name)
        self.chapters_list.append(chapter_info_dictionary)

    def save_screen_chapter_info(self):
        """Save all chapter info that is currently on the screen."""
        if self.current_chapter_info is not None:
            self.current_chapter_info[self.CHAPTER_TITLE] = self.entry_chapter_title.get()
            listbox_index = self.current_chapter_info[self.CHAPTER_INDEX]
            self.listbox_chapters.delete(listbox_index, listbox_index)
            self.listbox_chapters.insert(listbox_index, self.current_chapter_info[self.CHAPTER_TITLE])
            self.current_chapter_info[self.CHAPTER_WORDS] = self.entry_chapter_words.get()
            self.current_chapter_info[self.CHAPTER_PAGES] = self.entry_chapter_pages.get()
            with open('project', 'w') as file_out:
                json.dump(self.chapters_list, file_out, indent=2)

    def update_screen_chapter_info(self):
        """
        Update all screen chapter information.

        Update all screen chapter information with what the currently selected
        chapter is.
        """
        if self.current_chapter_info is not None:
            self.entry_chapter_title.delete(0, tkinter.END)
            self.entry_chapter_title.insert(tkinter.END, self.current_chapter_info[self.CHAPTER_TITLE])
            self.entry_chapter_words.delete(0, tkinter.END)
            self.entry_chapter_words.insert(tkinter.END, self.current_chapter_info.get(self.CHAPTER_WORDS, ""))
            self.entry_chapter_pages.delete(0, tkinter.END)
            self.entry_chapter_pages.insert(tkinter.END, self.current_chapter_info.get(self.CHAPTER_PAGES, ""))
            # self.chapters_list[self.current_chapter_info[self.CHAPTER_INDEX]] = self.current_chapter_info

    def delete_chapter_action(self):
        pass

    def load_chapters_to_listbox(self):
        print("LOADED CHAPTERS FOR LISTBOX")
        pass

    def listbox_chapters_select_action(self, event):
        sel = self.listbox_chapters.curselection()
        self.save_screen_chapter_info()
        if len(sel) >= 1:
            self.selected_chapter_index = sel[0]
            self.current_chapter_info = self.chapters_list[sel[0]]
            print(self.chapters_list)
            print("Current chapter:", self.current_chapter_info)
            selected_text = self.listbox_chapters.get(self.selected_chapter_index)
            self.update_screen_chapter_info()

    def close_window(self):
        """Close window."""
        print("Closing window from Project_Info_Window class.")
        self.save_screen_chapter_info()
        super().close_window()


# If this file is the one that was executed as main, start the main function.
if __name__ == "__main__":
    main()
