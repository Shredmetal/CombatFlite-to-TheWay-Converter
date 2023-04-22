from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as ET
import xmltodict
import zipfile
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

        cf_file_path = self.cf_filename.get()

        try:
            with zipfile.ZipFile(f'CF_File/{cf_file_path}.cf') as zip_ref:
                zip_ref.extractall("Extracted_CF")
        except FileNotFoundError:
            messagebox.showerror(title="File Not Found", message="The file you have entered does not exist. Please"
                                                                 " make sure that your .cf file is in the CF_File"
                                                                 " directory.")
        else:
            tree = ET.parse('Extracted_CF/mission.xml')
            myroot = tree.getroot()
            xmlstr = ET.tostring(myroot, encoding='utf-8', method='xml')

            data_dict = dict(xmltodict.parse(xmlstr))

            flight_names = []
            flight_waypoints = []

            for n in data_dict['Mission']['Routes']['Route']:
                flight_names.append(n['Name'])
                waypoint_num = 0
                each_flight_waypoints = []
                for x in n['Waypoints']['Waypoint']:
                    lat = x['Lat']
                    lon = x['Lon']
                    elev = float(x['Altitude']) * 0.3048
                    waypoint_num += 1
                    waypoint_dict = {
                        "id": waypoint_num,
                        "name": f"Waypoint {waypoint_num}",
                        "lat": lat,
                        "long": lon,
                        "elev": elev
                    }
                    each_flight_waypoints.append(waypoint_dict)
                flight_waypoints.append(each_flight_waypoints)

            for n in range(len(flight_names)):
                with open(f"TW_Files/{flight_names[n]}.tw", mode='w') as file:
                    waypoint_string = str(flight_waypoints[n])
                    joined = waypoint_string.replace(" ", "")
                    apostrophe_replaced = joined.replace("'", '"')
                    file.write(f"{apostrophe_replaced}")

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
