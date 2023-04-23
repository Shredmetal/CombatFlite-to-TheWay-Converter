from tkinter import *
from tkinter import messagebox
import combatflite_reader
import theway_formatter
import os


class Interface:

    def __init__(self):

        window = Tk()
        window.title("Combatflite to TheWay File Converter")
        window.config(padx=20, pady=20)
        canvas = Canvas(width=500, height=280)
        canvas.grid(row=0, column=0, columnspan=2)
        tomcat = PhotoImage(file="bombcat.png")
        canvas.create_image(250, 140, image=tomcat)

        self.cf_filename = Entry(width=50)
        self.cf_filename.focus()
        self.cf_filename.grid(row=3, column=0, pady=10, sticky=W)

        instruction_label1 = Label(text="Make sure that the CF file is in the same directory as this executable in "
                                        "the folder named 'CF FILE'.")
        instruction_label1.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)

        instruction_label2 = Label(text="Please type in the filename without any file extensions:")
        instruction_label2.grid(row=2, column=0, columnspan=2, sticky=W, pady=10)

        convert_button = Button(text="Convert to TW", width=20, command=self.convert)
        convert_button.grid(row=3, column=1, sticky=W)

        instruction_label3 = Label(text="Please clear the files in the Extracted_CF and the TW_Files directories to "
                                        "avoid file conflicts.")
        instruction_label3.grid(row=4, column=0, columnspan=2, sticky=W, pady=10)

        clear_button = Button(text="Press to delete all content in Extracted_CF and TW_Files directories.",
                              command=self.clear_folders)
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

        window.mainloop()

    def convert(self):

        reader = combatflite_reader.CombatFliteReader()

        cf_file_path = self.cf_filename.get()

        try:

            reader.unzipper(cf_file_path)

        except FileNotFoundError:

            messagebox.showerror(title="File Not Found", message="The file you have entered does not exist. Please"
                                                                 " make sure that your .cf file is in the CF_File"
                                                                 " directory.")
        else:

            formatter = theway_formatter.TheWayFormatter()

            data_dict = reader.xml_parser()

            flight_names = []
            flight_waypoints = []

            formatter.lists_creator(data_dict, flight_names, flight_waypoints)

            formatter.file_writer(flight_names, flight_waypoints)

            messagebox.showinfo(title="Files Converted",
                                message="Your CombatFlite file has been converted. You can find "
                                        "your TheWay file(s) (plural if you had multiple flights"
                                        " in your CombatFlite plan) in the folder named"
                                        "'TW_Files' located in the same directory as the "
                                        "executable file of this program.")

            self.cf_filename.delete(0, 'end')

    def clear_folders(self):

        try:
            extracted_directory = "Extracted_CF"
            for file in os.listdir(extracted_directory):
                os.remove(os.path.join(extracted_directory, file))
        except FileNotFoundError:
            pass

        try:
            tw_directory = "TW_Files"
            for file in os.listdir(tw_directory):
                os.remove(os.path.join(tw_directory, file))
        except FileNotFoundError:
            pass

        messagebox.showinfo(title="Files Deleted", message="The files in the Extracted_CF and TW_Files directories "
                                                           "have been deleted.")
