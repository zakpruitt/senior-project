from itertools import count
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from file_parsing.file_input import FileInput
from file_parsing.parser import Parser
from file_parsing.excel_writer import ExcelWriter
from datetime import date
import pandas as pd

class Snowball:

    def __init__(self):
        self.inputFiles = FileInput()

        self.winWidth = 800
        self.winHeight = 200

        #initialize root
        self.root = Tk()
        self.root.title('Snowball - File Parser')
        self.root.minsize(width=self.winWidth, height=self.winHeight)
        self.root.grid_columnconfigure(0, weight=1)

        #define frame for input lines
        self.inputFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.inputFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inputFrame.grid_columnconfigure(1, weight=1)

        #define frame for parse and cancel buttons
        self.controlFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.controlFrame.grid(column=0, row=1, sticky=(N, S, E, W))
        self.controlFrame.grid_columnconfigure(0, weight=1)
        self.controlFrame.grid_columnconfigure(1, weight=1)

        #create All File controls
        ttk.Label(self.inputFrame, text="All File Selected:").grid(
            column=0, row=0)
        self.allFileEntryText = StringVar()
        self.allFileEntry = Entry(self.inputFrame, textvariable=self.allFileEntryText).grid(
            column=1, row=0, sticky=(W, E))
        self.allFileButton = Button(self.inputFrame, text="Select \"All\" File",
                                    command=self.fetchAllFile).grid(column=2, row=0, sticky=(W, E))

        #create daily file controls
        ttk.Label(self.inputFrame, text="Daily File Selected:").grid(
            column=0, row=1)
        self.dailyFileEntryText = StringVar()
        self.dailyFileEntry = Entry(self.inputFrame, textvariable=self.dailyFileEntryText).grid(
            column=1, row=1, sticky=(W, E))
        self.dailyFileButton = Button(self.inputFrame, text="Select daily File",
                                         command=self.fetchDailyFile).grid(column=2, row=1, sticky=(W, E))

        #create output file controls
        Label(self.inputFrame, text="Out File Selected:").grid(column=0, row=2)
        self.outFileEntryText = StringVar()
        self.outFileEntry = Entry(self.inputFrame, textvariable=self.outFileEntryText).grid(
            column=1, row=2, sticky=(W, E))
        self.outFileButton = Button(self.inputFrame, text="Select Out File",
                                    command=self.fetchOutputFile).grid(column=2, row=2, sticky=(W, E))

        for child in self.inputFrame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        Button(self.controlFrame, text="Parse Files",
               command=self.startParse).grid(column=0, row=0)
        Button(self.controlFrame, text="Close",
               command=self.close).grid(column=1, row=0)

        self.root.mainloop()

    def fetchAllFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.allFileEntryText.set(file)

    def fetchDailyFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.dailyFileEntryText.set(file)

    def fetchOutputFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setOutputFile(file)
        self.outFileEntryText.set(file)
    
    def startParse(self):
        # parse text file(s)
        all_parser = Parser(self.allFileEntryText.get())
        all_parser.parse_text()
        daily_parser = Parser(self.dailyFileEntryText.get())
        daily_parser.parse_text()

        # create excel_writer object and dataframes
        excel_writer = ExcelWriter(self.outFileEntryText.get())
        columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
                'Support #', 'Last User', 'Original User', 'Time Last Changed']
        all_df = pd.DataFrame(all_parser.line_information, columns=columns)
        daily_df = pd.DataFrame(daily_parser.line_information, columns=columns)
        all_count_df = pd.DataFrame(all_parser.count_information)
        daily_count_df = pd.DataFrame(daily_parser.count_information)
        count_df = pd.merge(all_count_df, daily_count_df)

        # create and write new sheets
        today = date.today()
        formatted_date = today.strftime("%m-%d-%Y")
        excel_writer.create_and_write_new_sheet(
            f"MaddenCo Daily Data {formatted_date}", daily_df)
        excel_writer.create_and_write_new_sheet(
            f"MaddenCo All Data {formatted_date}", all_df)
        excel_writer.create_and_write_new_sheet(
            f"MaddenCo Daily Count {formatted_date}", daily_count_df, True)
        excel_writer.create_and_write_new_sheet(
            f"MaddenCo All Count {formatted_date}", all_count_df, True)
        excel_writer.create_and_write_new_sheet(
            f"MaddenCo Total Count {formatted_date}", count_df, True)

        excel_writer.create_formats("file_parsing\ExcelFormats.json")

        # format sheets
        excel_writer.format_headers_af(
            f"MaddenCo Daily Data {formatted_date}", all_df, 0, "blue_header_format", "yellow_header_format")
        excel_writer.format_columns_af(
            f"MaddenCo Daily Data {formatted_date}", all_df, 0, 25, "blue_format", "yellow_format")

        excel_writer.format_headers_af(
            f"MaddenCo All Data {formatted_date}", all_df, 0, "blue_header_format", "yellow_header_format")
        excel_writer.format_columns_af(
            f"MaddenCo All Data {formatted_date}", all_df, 0, 25, "blue_format", "yellow_format")

        excel_writer.format_headers_af(
            f"MaddenCo Daily Count {formatted_date}", daily_count_df, 1, "cyan_header_format", "orange_header_format")
        excel_writer.format_columns_af(
            f"MaddenCo Daily Count {formatted_date}", daily_count_df, 1, 25, "cyan_format", "orange_format")
        excel_writer.format_row_index(
            f"MaddenCo Daily Count {formatted_date}", daily_count_df, "cyan_header_format")
        
        excel_writer.format_headers_af(
            f"MaddenCo All Count {formatted_date}", all_count_df, 1, "cyan_header_format", "orange_header_format")
        excel_writer.format_columns_af(
            f"MaddenCo All Count {formatted_date}", all_count_df, 1, 25, "cyan_format", "orange_format")
        excel_writer.format_row_index(
            f"MaddenCo All Count {formatted_date}", all_count_df, "cyan_header_format")

        excel_writer.format_headers_af(
            f"MaddenCo Total Count {formatted_date}", count_df, 1, "cyan_header_format", "orange_header_format")
        excel_writer.format_columns_af(
            f"MaddenCo Total Count {formatted_date}", count_df, 1, 25, "cyan_format", "orange_format")
        excel_writer.format_row_index(
            f"MaddenCo Total Count {formatted_date}", count_df, "cyan_header_format")

        # save  
        excel_writer.writer.save()
        print("Done!")

    def close(self):
        print("Clean up and Close")

