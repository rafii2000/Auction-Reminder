from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import time
import json

import socket
import mysql.connector
import urllib.request


class AuctionReminder:

    f_width = "400"
    f_height = "375"

    # MOST IMPORTANT VARIABLES
    internet_connection = False
    licence_status = "Invalid"  # Expired licence or invalid aut hkey
    cloak_status = "Inactive"

    user_auth_key = ""
    auth_key_origin = ""

    licence_expiry_date = None
    current_server_date = None

    new_settings = None

    diode_error_label = "hide"

    # Main cloak variables
    freq_hour = "01"
    freq_minute = "00"
    freq_second = "00"

    start_hour = "00"
    star_minute = "35"
    start_second = "00"

    end_hour = "23"
    end_minute = "59"
    end_second = "59"

    remind_hour = "--"
    remind_minute = "01"
    remind_second = "00"

    # Next auction variables
    auctions_list = []
    auction_index = 0
    next_auction_time = ""

    def __init__(self, window):

        self.window = window
        self.window.title("Auction Reminder")
        self.window.geometry("500x375+550+265")  # 400x300
        self.window.iconbitmap("Pictures/icon2.ico")

        # self.window.resizable(0, 0)
        # self.window.wm_attributes("-topmost", 1)

        self.initLayout()


    ''' Function initialize all aplication lalyouts'''
    def initLayout(self):

        #MAIN FRAMES
        self.mian_frame = ttk.Frame(self.window, height=self.f_height, width=self.f_width, ) #bg="lightgreen"
        self.settings_frame = ttk.Frame(self.window, height=self.f_height, width=self.f_width, ) #bg="lightblue"
        self.licecne_frame = ttk.Frame(self.window, height=self.f_height, width=self.f_width, ) #bg="lightyellow"
        self.apperance_frame = ttk.Frame(self.window, height=self.f_height, width=self.f_width, ) #bg="#F5DEB3"

        self.mian_frame.pack(side=LEFT, pady=10)
        self.mian_frame.pack_propagate(False)
        self.settings_frame.pack_propagate(False)
        self.licecne_frame.pack_propagate(False)
        self.apperance_frame.pack_propagate(False)

        #NAVBAR FRAME
        self.nav_bar = ttk.Frame(self.window)
        self.nav_bar.pack()


        #MAIN WINDOW LAYOUT
        self.main_window_layout()

        #SETTINGS WINDOW LAYOUT
        self.settings_window_layout()


        # APPEARANCE WINDOW LAYOUT
        self.appearance_window_layout()


        # LICENCE WINDOW LAYOUT
        self.licence_window_layout()


        #NAVBAR LAYOUT (buttons)
        self.main_window_img = PhotoImage(file="Pictures/home-page3-80.png")
        self.main_window_button = ttk.Button(self.nav_bar, image=self.main_window_img, state=NORMAL, command=lambda: self.main_window() ) #bd=1
        self.main_window_button.pack(pady=2, padx=2)

        self.settings_img = PhotoImage(file="Pictures/settings2-80.png")
        self.setting_button = ttk.Button(self.nav_bar, image=self.settings_img, state=NORMAL,command=lambda: self.settings_window() )
        self.setting_button.pack(pady=2, padx=2)

        self.paints_image = PhotoImage(file="Pictures/paints3-80.png")
        self.paints_button = ttk.Button(self.nav_bar, image=self.paints_image, state=NORMAL, command=lambda: self.appearance_window() )
        self.paints_button.pack(pady=2, padx=2)

        self.key_img = PhotoImage(file="Pictures/key3-80.png")
        self.key_button = ttk.Button(self.nav_bar, image=self.key_img, state=NORMAL, command=lambda: self.licence_window() )
        self.key_button.pack(pady=2, padx=2)


    ''' Smallest parts(different windows) of application layout'''
    def main_window_layout(self):


        #self.diodes_frame = Frame(self.window)
        #self.diodes_frame.place(x=280, y=13, bordermode=OUTSIDE)

        # FRAMES
        self.diodes_frame = Frame(self.mian_frame, bg="")

        # LABELS
        self.invisible_sign_1 = Label(self.mian_frame, text="", font=("Tiemes", 1))
        self.invisible_sign_2 = Label(self.mian_frame, text="", font=("Tiemes", 1))
        self.invisible_sign_3 = Label(self.mian_frame, text="", font=("Tiemes", 1))

        self.info_label_1 = Label(self.mian_frame, text="Actual time:", font=("Arial BOLD", 16))
        self.info_label_2 = Label(self.mian_frame, text="Next auction:", font=("Arial BOLD", 15))
        self.info_label_3 = Label(self.mian_frame, text="Remaining time:", font=("Arial BOLD", 14))
        self.info_label_4 = Label(self.mian_frame, text="Error message:", font=("Arial BOLD", 14))
        self.info_label_5 = Label(self.mian_frame, text="You have\nvalid licence", fg="green", font=("Franklin Gothic Medium", 11))  # valid x=267,   invalid x=262
        self.info_label_6 = Label(self.mian_frame, text="You have\ninvalid licence", fg="red", font=("Franklin Gothic Medium", 11))

        self.clock_label = Label(self.mian_frame, font=("Unispace", 30), text="")
        self.next_auction_label = Label(self.mian_frame, font=("Unispace", 21), text="")
        self.timer_label = Label(self.mian_frame, font=("Unispace", 17), text="")
        self.error_message_label = Label(self.mian_frame, font=("Arial BOLD", 12), text="", fg="red")

        self.red = PhotoImage(file="Pictures/cancel-20.png")
        self.red_diode = Button(self.diodes_frame, image=self.red, bd=0, command=lambda: self.show_licence_info("Invalid"))
        self.red_diode.pack(side=LEFT, padx=5)

        self.green = PhotoImage(file="Pictures/ok-20.png")
        self.green_diode = Button(self.diodes_frame, image=self.green, bd=0, command=lambda: self.show_licence_info("Valid"))
        self.green_diode.pack(side=LEFT, padx=5)
        self.diodes_frame.place(x=270, y=20, bordermode=OUTSIDE)

        # MAIN_WINDOW_PACK()
        self.info_label_1.pack(padx=10, pady=1, anchor=NW)
        self.clock_label.pack(padx=20, anchor=W)
        self.invisible_sign_1.pack(pady=7)
        self.info_label_2.pack(padx=10, pady=1, anchor=W)
        self.next_auction_label.pack(padx=30, anchor=W)
        self.invisible_sign_2.pack(pady=7)
        self.info_label_3.pack(padx=10, pady=1, anchor=SW)
        self.timer_label.pack(padx=40, anchor=W)
        self.invisible_sign_3.pack(pady=7)
        self.info_label_4.pack(padx=10, pady=1, anchor=SW)
        self.error_message_label.pack(padx=30, anchor=SW)

    def settings_window_layout(self):

        #self.settings_label_info = Label(self.settings_frame, text="SETTINGS WINDOW")
        #self.settings_label_info.pack()

        frame_frequency = Frame(self.settings_frame)
        frame_start = Frame(self.settings_frame)
        frame_ending = Frame(self.settings_frame)
        frame_reminder = Frame(self.settings_frame)

        # part0 - OTHERS_ELEMENTS
        label_frequency = Label(self.settings_frame, text="Frequency:", font=("Arial BOLD", 17))
        label_start = Label(self.settings_frame, text="Start reminding:", font=("Arial BOLD", 17))
        label_ending = Label(self.settings_frame, text="End reminding:", font=("Arial BOLD", 17))
        label_reminder = Label(self.settings_frame, text="Remind ... before:", font=("Arial BOLD", 17))
        label_info = Label(self.settings_frame, text="It is recommended to restart program, after every changes settings.",
                           font=("Arial BOLD", 9), fg="red")

        colon_1 = Label(frame_frequency, text=":", font=("Arial Black", 15))
        colon_2 = Label(frame_frequency, text=":", font=("Arial Black", 15))
        colon_3 = Label(frame_start, text=":", font=("Arial Black", 15))
        colon_4 = Label(frame_start, text=":", font=("Arial Black", 15))
        colon_5 = Label(frame_ending, text=":", font=("Arial Black", 15))
        colon_6 = Label(frame_ending, text=":", font=("Arial Black", 15))
        colon_7 = Label(frame_reminder, text=":", font=("Arial Black", 15))
        colon_8 = Label(frame_reminder, text=":", font=("Arial Black", 15))

        space_1 = Label(self.settings_frame, text="", font=("Times", 2))
        space_2 = Label(self.settings_frame, text="", font=("Times", 2))
        space_3 = Label(self.settings_frame, text="", font=("Times", 2))
        space_4 = Label(self.settings_frame, text="", font=("Times", 2))

        font_size = 17
        # part1 - FREQUENCY_FRAME
        self.text_freq_hour = Text(frame_frequency, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_freq_minute = Text(frame_frequency, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_freq_second = Text(frame_frequency, bd=1, width=4, height=1, font=("Unispace", font_size))

        self.text_freq_hour.pack(side=LEFT, padx=5, pady=0)
        colon_1.pack(side=LEFT)
        self.text_freq_minute.pack(side=LEFT, padx=5, pady=0)
        colon_2.pack(side=LEFT)
        self.text_freq_second.pack(side=LEFT, padx=5, pady=0)

        # part2 - START_FRAME
        self.text_start_hour = Text(frame_start, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_start_minute = Text(frame_start, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_start_second = Text(frame_start, bd=1, width=4, height=1, font=("Unispace", font_size))

        self.text_start_hour.pack(side=LEFT, padx=5, pady=0)
        colon_3.pack(side=LEFT)
        self.text_start_minute.pack(side=LEFT, padx=5, pady=3)
        colon_4.pack(side=LEFT)
        self.text_start_second.pack(side=LEFT, padx=5, pady=3)

        # part3 - END_FRAME
        self.text_end_hour = Text(frame_ending, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_end_minute = Text(frame_ending, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_end_second = Text(frame_ending, bd=1, width=4, height=1, font=("Unispace", font_size))

        self.text_end_hour.pack(side=LEFT, padx=5, pady=3)
        colon_5.pack(side=LEFT)
        self.text_end_minute.pack(side=LEFT, padx=5, pady=3)
        colon_6.pack(side=LEFT)
        self.text_end_second.pack(side=LEFT, padx=5, pady=3)

        # part4 = REMIND_FRAME
        self.text_remind_hour = Text(frame_reminder, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_remind_minute = Text(frame_reminder, bd=1, width=4, height=1, font=("Unispace", font_size))
        self.text_remind_second = Text(frame_reminder, bd=1, width=4, height=1, font=("Unispace", font_size))

        self.text_remind_hour.insert(1.0, " --")
        self.text_remind_hour.config(state=DISABLED)

        self.text_remind_hour.pack(side=LEFT, padx=5, pady=3)
        colon_7.pack(side=LEFT)
        self.text_remind_minute.pack(side=LEFT, padx=5, pady=3)
        colon_8.pack(side=LEFT)
        self.text_remind_second.pack(side=LEFT, padx=5, pady=3)

        # part5 - BUTTONS
        self.button_save = ttk.Button(self.settings_frame, text="Save", width=10, command=lambda: self.save(), state=DISABLED)
        self.button_default = ttk.Button(self.settings_frame, text="Default", width=10, command=lambda: self.default_config())
        self.button_edit = ttk.Button(self.settings_frame, text="Edit", width=10, command=lambda: self.edit())

        # SETTINGS_WINDOW
        space_1.pack()
        label_frequency.pack(anchor=NW, padx=5)
        frame_frequency.pack(anchor=NW, padx=20, pady=4)
        space_2.pack()
        label_start.pack(anchor=NW, padx=5)
        frame_start.pack(anchor=NW, padx=20, pady=4)
        space_3.pack()
        label_ending.pack(anchor=NW, padx=5)
        frame_ending.pack(anchor=NW, padx=20, pady=4)
        space_4.pack()
        label_reminder.pack(anchor=NW, padx=5)
        frame_reminder.pack(anchor=NW, padx=20, pady=4)
        #label_info.pack(anchor=NW, padx=5, pady=5)


        # button_default.place(x=305, y=190)
        # button_edit.place(x=305, y=217)
        # button_save.place(x=305, y=244)

        self.button_default.place(x=305, y=150)
        self.button_edit.place(x=305, y=177)
        self.button_save.place(x=305, y=204)

    def appearance_window_layout(self):

        self.apperance_label_info = Label(self.apperance_frame, text="APPEARANCE WINDOW")
        self.apperance_label_info.pack()

    def licence_window_layout(self):
        # self.licence_label_info = Label(self.licecne_frame, text="LICENCE WINDOW")
        # self.licence_label_info.pack()

        self.frame_licence_status = Frame(self.licecne_frame) #bg="#E1E1E1"
        self.frame_auth_key = Frame(self.licecne_frame)
        self.frame_info = Frame(self.licecne_frame)
        self.frame_enter_licence = Frame(self.licecne_frame)

        self.label_licence_status = Label(self.frame_licence_status, text="Licence:", font=("Times BOLD", 16))
        self.label_valid_invalid = Label(self.frame_licence_status, text="Invalid", fg="red", font=("Arial BLOD", 16))
        self.label_auth_key_info = Label(self.frame_auth_key, text="Auth key:", font=("Arial BOLD", 13))
        self.label_auth_key_value = Label(self.frame_auth_key, text="none", fg="red", font=("Arial BLOD", 13))
        self.label_validation_info = Label(self.frame_info, text="", fg="red", font=("Arial BLOD", 13))

        self.label_enter_licence_str = Label(self.frame_enter_licence, text="Enter auth key:", font=("Arial BLOD", 11))

        self.text_enter_licence = Text(self.frame_enter_licence, width=35, height=1, font=("Arial BLOD", 12), padx=5, pady=5,
                                  bd=2, relief="solid") #bg="#B9B9B9"

        button_verify_licence = Button(self.frame_enter_licence, text="VERIFY", font=("Arial BLOD", 16), bd=3,
                                       relief="solid", padx=3, justify=CENTER, command=lambda: self.verify_licence())

        space_1 = Label(self.licecne_frame, text="", font=("Times", 5))
        space_2 = Label(self.licecne_frame, text="", font=("Times", 5))

        # WINDOW LAYOUT
        space_1.pack()
        self.frame_licence_status.pack(anchor=NW)
        self.label_licence_status.pack(padx=10, pady=5, side=LEFT)
        self.label_valid_invalid.pack(side=LEFT)

        self.frame_auth_key.pack(anchor=NW)
        self.label_auth_key_info.pack(padx=12, side=LEFT)
        self.label_auth_key_value.pack(side=LEFT)

        space_2.pack(pady=10, anchor=NW)
        self.frame_info.pack(anchor=CENTER, pady=3)
        self.label_validation_info.pack(pady=15)

        self.frame_enter_licence.pack(anchor=CENTER)
        self.label_enter_licence_str.pack(anchor=NW, pady=1)
        self.text_enter_licence.pack()
        button_verify_licence.pack(pady=25, )


    ''' Funtctions responsible for change aplication frames  '''

    def main_window(self):
        self.window.title("Auction Reminder")

        self.licecne_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.apperance_frame.pack_forget()
        self.nav_bar.pack_forget()

        self.mian_frame.pack(side=LEFT, pady=10)
        self.nav_bar.pack()

    def settings_window(self):
        self.window.title("Settings")

        self.mian_frame.pack_forget()
        self.licecne_frame.pack_forget()
        self.apperance_frame.pack_forget()
        self.nav_bar.pack_forget()
        self.settings_frame.pack(side=LEFT)
        self.nav_bar.pack()

    def appearance_window(self):
        self.window.title("Appearance")

        self.mian_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.licecne_frame.pack_forget()
        self.nav_bar.pack_forget()
        self.apperance_frame.pack(side=LEFT)
        self.nav_bar.pack()

    def licence_window(self):
        self.window.title("Licence")

        self.mian_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.apperance_frame.pack_forget()
        self.nav_bar.pack_forget()
        self.licecne_frame.pack(side=LEFT)
        self.nav_bar.pack()

        # tutaj nalezy jeszcze dodac funkcje ktora bedzie sprawdzac
        # status licencji i renderowac okno

        # self.render_licence_window(self.licence_status, self.user_auth_key)
        # self.render_licence_window(None, None, None, "Licence expired")

        # lub w tym miejsu nic nie renderowac, tylko zmieniac okon, a renderowanie
        # wywolywac w funkcji okresowej ktora bedzie sprawdzac polaczenie z internetem
        # i sprawdzac status licencji


    ''' MAIN FRAME functions'''

    def light_diode_up(self):

        if self.licence_status == "Valid":
            self.green_diode.config(state=NORMAL)
            self.red_diode.config(state=DISABLED)
            self.info_label_6.place_forget()
            self.diode_error_label = "hide"
        else:
            self.green_diode.config(state=DISABLED)
            self.red_diode.config(state=NORMAL)
            self.info_label_5.place_forget()

            self.info_label_6.config(text="You have\ninvalid licence")
            self.diode_error_label = "hide"

    def show_licence_info(self, status):

        if status == "Valid":
            print("valid")
            if self.diode_error_label == "hide":
                self.info_label_5.place(x=267, y=45)
                self.diode_error_label = "on screen"
            else:
                self.info_label_5.place_forget()
                self.diode_error_label = "hide"
        else:
            print("invalid")
            if self.diode_error_label == "hide":
                self.info_label_6.place(x=260, y=45, bordermode=OUTSIDE)
                self.diode_error_label = "on screen"
            else:
                self.info_label_6.place_forget()
                self.diode_error_label = "hide"
    # -------------------------------------------
    def digital_clock(self):

        def unset_main_frame_values():

            self.clock_label.config(text="")
            self.next_auction_label.config(text="")
            self.timer_label.config(text="")
            self.error_message_label.config(text="")

        if self.new_settings is True:
            self.new_settings = None

            # tutaj wprowadze wszystkie zmiany zwiazane z ustawieniami
            # wywolam odpowiednie funkcje
            # self.next_auction()

        if self.licence_status == "Valid":
            time_string = time.strftime("%H:%M:%S", time.localtime())
            self.clock_label.config(text=time_string)
            self.clock_label.after(1000, self.digital_clock)

            # tutaj bede wywylowyl inne funkcje
            self.next_auction()

        elif self.licence_status == "Invalid":
            print("Invalid licence")
            self.cloak_status = "Inactive"
            unset_main_frame_values()
        elif self.internet_connection is False:
            print("No internet connection ")
            unset_main_frame_values()
        else:
            print("Unknown issue ")
            unset_main_frame_values()

    def next_auction(self):

        # gdy jest > odlicza (7 ... 1), gdy jest >= odlicza (6 ... 0)
        if self.auctions_list[self.auction_index] >= time.strftime("%H:%M:%S", time.localtime()):
            self.next_auction_label.config(text=self.auctions_list[self.auction_index])
            next_auction_time = self.auctions_list[self.auction_index]
        else:

            if time.strftime("%H:%M:%S", time.localtime()) < self.auctions_list[-1]:
                self.auction_index += 1

            else:
                self.auction_index = 0

        self.next_auction_label.config(text=self.auctions_list[self.auction_index])
        self.next_auction_time = self.auctions_list[self.auction_index]
        self.digital_timer()
        #self.next_auction_label.after(1000, self.next_auction)

    def find_auction_index(self):

        for clock in self.auctions_list:

            if clock > time.strftime("%H:%M:%S", time.localtime()):
                self.auction_index = self.auctions_list.index(clock)
                break
            else:
                self.auction_index = 0

        print("auction index: ", self.auction_index)

    def make_auctions_list(self):

        def complete_time_value(value):
            # uzupelnia zmienne aby wyswietlac
            # prawidlowy format godziny, tj: dwa znaki

            value = str(value)

            if len(value) == 1:
                value = "0" + value

            return value

        def check_value(int_list):

            if int_list[2] >= 60:
                int_list[1] += 1
                int_list[2] = int_list[2] - 60

            if int_list[1] >= 60:
                int_list[0] += 1
                int_list[1] = int_list[1] - 60

            return int_list

        time_str = self.start_hour + ":" + self.star_minute + ":" + self.start_second
        end_str = self.end_hour + ":" + self.end_minute + ":" + self.end_second

        # te wartosci sa string-ami
        freq_list = [int(self.freq_hour), int(self.freq_minute), int(self.freq_second)]
        time_list = [int(self.start_hour), int(self.star_minute), int(self.start_second)]

        self.auctions_list = []

        while time_str <= end_str:
            self.auctions_list.append(time_str)
            # print(time_str)

            time_list[0] = time_list[0] + freq_list[0]  # hour int
            time_list[1] = time_list[1] + freq_list[1]  # minute int
            time_list[2] = time_list[2] + freq_list[2]  # second int

            time_list = check_value(time_list)

            hour = complete_time_value(time_list[0])
            minute = complete_time_value(time_list[1])
            second = complete_time_value(time_list[2])

            time_str = hour + ":" + minute + ":" + second

    def digital_timer(self):

        def clock_calculator(next_time, current_time):

            if self.next_auction_time < actual_time:

                difference_time = [0, 0, 0]
                base_time = [24, 00, 00]

                next_time = next_time.split(":")
                current_time = current_time.split(":")
                remaining_time = [0, 0, 0]

                next_time[0] = int(next_time[0])
                next_time[1] = int(next_time[1])
                next_time[2] = int(next_time[2])

                current_time[0] = int(current_time[0])
                current_time[1] = int(current_time[1])
                current_time[2] = int(current_time[2])

                if current_time[2] < next_time[2]:
                    current_time[1] -= 1
                    current_time[2] += 60

                if current_time[1] < next_time[1]:
                    current_time[0] -= 1
                    current_time[1] += 60

                difference_time[0] = current_time[0] - next_time[0]
                difference_time[1] = current_time[1] - next_time[1]
                difference_time[2] = current_time[2] - next_time[2]

                if base_time[2] < difference_time[2]:
                    base_time[1] -= 1
                    base_time[2] += 60

                if base_time[1] < difference_time[1]:
                    base_time[0] -= 1
                    base_time[1] += 60

                remaining_time[0] = base_time[0] - difference_time[0]
                remaining_time[1] = base_time[1] - difference_time[1]
                remaining_time[2] = base_time[2] - difference_time[2]

                return remaining_time

            else:

                # print(next_time)
                next_time = next_time.split(":")
                current_time = current_time.split(":")
                remaining_time = [0, 0, 0]

                # str values, have to be changed
                next_time[0] = int(next_time[0])
                next_time[1] = int(next_time[1])
                next_time[2] = int(next_time[2])

                current_time[0] = int(current_time[0])
                current_time[1] = int(current_time[1])
                current_time[2] = int(current_time[2])

                if next_time[2] < current_time[2]:
                    next_time[1] -= 1
                    next_time[2] += 60

                if next_time[1] < current_time[1]:
                    next_time[0] -= 1
                    next_time[1] += 60

                # int values
                remaining_time[0] = next_time[0] - current_time[0]
                remaining_time[1] = next_time[1] - current_time[1]
                remaining_time[2] = next_time[2] - current_time[2]

                return remaining_time

        def complete_time_values(list_int):

            for i in range(3):
                if len(str(list_int[i])) < 2:
                    list_int[i] = "0" + str(list_int[i])

            return str(list_int[0]) + ":" + str(list_int[1]) + ":" + str(list_int[2])



        actual_time = time.strftime("%H:%M:%S", time.localtime())
        clock_calculator(str(self.next_auction_time), str(actual_time))

        remaining_time_str = complete_time_values(clock_calculator(str(self.next_auction_time), str(actual_time)))
        self.timer_label.config(text=remaining_time_str)
        self.display_prompt(remaining_time_str)

    def display_prompt(self, remaining_time):


        if remaining_time == "00" + ":" + self.remind_minute + ":" + self.remind_second:
            # alarm()
            if int(self.remind_minute) == 0:
                tkinter.messagebox.showinfo("Auction Reminder Assistant",
                                            self.remind_second + " seconds left to ending the auction.")
            else:
                tkinter.messagebox.showinfo("Auction Reminder Assistant", str(int(self.remind_minute)) + ":" +
                                            self.remind_second + " minutes left to ending the auction.")


    ''' SETTINGS FRAME FUNCTIONS '''

    def render_settings_windows(self):
        print("\nDISPLAY_settings")

        #tutaj byly zmienne dotyczane godzin

        self.state_normal()
        self.clear()

        self.text_freq_hour.insert(1.0, str(self.freq_hour))
        self.text_freq_minute.insert(1.0, str(self.freq_minute))
        self.text_freq_second.insert(1.0, str(self.freq_second))

        self.text_start_hour.insert(1.0, str(self.start_hour))
        self.text_start_minute.insert(1.0, str(self.star_minute))
        self. text_start_second.insert(1.0, str(self.start_second))

        self.text_end_hour.insert(1.0, str(self.end_hour))
        self.text_end_minute.insert(1.0, str(self.end_minute))
        self.text_end_second.insert(1.0, str(self.end_second))

        # text_remind_hour.insert(1.0, "00")
        self.text_remind_minute.insert(1.0, str(self.remind_minute))
        self.text_remind_second.insert(1.0, str(self.remind_second))

        self.justify()
        self.state_disable()

    def default_config(self):
        self.edit()

        print("DEFAULT_settings")

        self.freq_hour = "01"
        self.freq_minute = "00"
        self.freq_second = "00"

        self.start_hour = "00"
        self.star_minute = "35"
        self.start_second = "00"

        self.end_hour = "23"
        self.end_minute = "59"
        self.end_second = "59"

        self.remind_minute = "01"
        self.remind_second = "00"

        self.render_settings_windows()
        self.save()
        self.state_disable()

    def edit(self):
        print("EDIT_settings")

        self.button_save.config(state=NORMAL)
        self.button_edit.config(state=DISABLED)

        self.state_normal()

    def save(self):

        print("SAVE_settings")

        def find_errors(value, pos, err=None):

            hours_boxes = [1, 4, 7]
            minute_second_boxes = [2, 3, 5, 6, 8, 9, 11, 12]

            # pass_further = [0, None]

            if len(value) < 2 or len(value) > 2:
                err += 1

                # pass_further[0] += 1
                # pass_further[1] = 0

                if pos not in change_color:
                    change_color.append(pos)
            else:
                try:
                    int(value)

                    if pos in hours_boxes and int(value) > 23:
                        err += 1

                        if pos not in change_color:
                            change_color.append(pos)

                    if pos in minute_second_boxes and int(value) > 59:
                        err += 1

                        if pos not in change_color:
                            change_color.append(pos)
                except ValueError:
                    err += 1

                    if pos not in change_color:
                        change_color.append(pos)

            return err

        def find_others_errors(err):

            pass_further = []
            error_name = 0

            # frequency cant be equal 0
            if self.freq_hour == "00" and self.freq_minute == "00" and self.freq_second == "00":

                if 1 not in change_color:
                    change_color.append(1)
                if 2 not in change_color:
                    change_color.append(2)
                if 3 not in change_color:
                    change_color.append(3)

                err += 1
                error_name = 1
            # ending must be bigger than star
            elif self.end_hour + ":" + self.end_minute + ":" + self.end_second <= self.start_hour + ":" + self.star_minute + ":" + self.start_second:

                if 7 not in change_color:
                    change_color.append(7)
                if 8 not in change_color:
                    change_color.append(8)
                if 9 not in change_color:
                    change_color.append(9)

                err += 1
                error_name = 2
            # remind before must be lower than frequency
            elif "00" + ":" + self.remind_minute + ":" + self.remind_second >= self.freq_hour + ":" + self.freq_minute + ":" + self.freq_second:

                if 11 not in change_color:
                    change_color.append(11)
                if 12 not in change_color:
                    change_color.append(12)

                err += 1
                error_name = 3

            pass_further.append(err)
            pass_further.append(error_name)

            return pass_further

        def mark_wrong_boxes(boxes_list):

            for num in boxes_list:

                if num == 1:
                    self.text_freq_hour.config(bg="#ff7d66")
                if num == 2:
                    self.text_freq_minute.config(bg="#ff7d66")
                if num == 3:
                    self.text_freq_second.config(bg="#ff7d66")
                if num == 4:
                    self.text_start_hour.config(bg="#ff7d66")
                if num == 5:
                    self.text_start_minute.config(bg="#ff7d66")
                if num == 6:
                    self.text_start_second.config(bg="#ff7d66")
                if num == 7:
                    self.text_end_hour.config(bg="#ff7d66")
                if num == 8:
                    self.text_end_minute.config(bg="#ff7d66")
                if num == 9:
                    self.text_end_second.config(bg="#ff7d66")
                if num == 11:
                    self.text_remind_minute.config(bg="#ff7d66")
                if num == 12:
                    self.text_remind_second.config(bg="#ff7d66")

        error = 0
        # error_type # 0-Value, 1-Frequency, 2-End time, 3-Frequency can't be equal remind before
        change_color = []

        # might be disable state

        self.freq_hour = self.text_freq_hour.get(1.0, END).strip()
        self.freq_minute = self.text_freq_minute.get(1.0, END).strip()
        self.freq_second = self.text_freq_second.get(1.0, END).strip()

        self.start_hour = self.text_start_hour.get(1.0, END).strip()
        self.star_minute = self.text_start_minute.get(1.0, END).strip()
        self.start_second = self.text_start_second.get(1.0, END).strip()

        self.end_hour = self.text_end_hour.get(1.0, END).strip()
        self.end_minute = self.text_end_minute.get(1.0, END).strip()
        self.end_second = self.text_end_second.get(1.0, END).strip()

        # remind_hour = text_remind_hour.get(1.0, END)
        self.remind_minute = self.text_remind_minute.get(1.0, END).strip()
        self.remind_second = self.text_remind_second.get(1.0, END).strip()

        error = find_errors(self.freq_hour, 1, error)
        #error_type.append(find_errors(freq_hour, 1, error)[1])

        error = find_errors(self.freq_minute, 2, error)
        error = find_errors(self.freq_second, 3, error)

        error = find_errors(self.start_hour, 4, error)
        error = find_errors(self.star_minute, 5, error)
        error = find_errors(self.start_second, 6, error)

        error = find_errors(self.end_hour, 7, error)
        error = find_errors(self.end_minute, 8, error)
        error = find_errors(self.end_second, 9, error)

        error = find_errors(self.remind_minute, 11, error)
        error = find_errors(self.remind_second, 12, error)

        if error == 0:
            error = find_others_errors(error)[0]
            error_type = find_others_errors(error)[1]
        else:
            error_type = 0

        # DO zmiany
        if error == 0:

            self.button_edit.config(state=NORMAL)
            self.button_save.config(state=DISABLED)

            user_config = {
                "frequency": {
                    "freq_hour": None,
                    "freq_minute": None,
                    "freq_second": None,
                },
                "start": {
                    "start_hour": None,
                    "start_minute": None,
                    "start_second": None,
                },
                "end": {
                    "end_hour": None,
                    "end_minute": None,
                    "end_second": None
                },
                "remind": {
                    "remind_minute": None,
                    "remind_second": None
                }
            }

            user_config["frequency"]["freq_hour"] = self.freq_hour
            user_config["frequency"]["freq_minute"] = self.freq_minute
            user_config["frequency"]["freq_second"] = self.freq_second

            user_config["start"]["start_hour"] = self.start_hour
            user_config["start"]["start_minute"] = self.star_minute
            user_config["start"]["start_second"] = self.start_second

            user_config["end"]["end_hour"] = self.end_hour
            user_config["end"]["end_minute"] = self.end_minute
            user_config["end"]["end_second"] = self.end_second

            user_config["remind"]["remind_minute"] = self.remind_minute
            user_config["remind"]["remind_second"] = self.remind_second

            #print(user_config)

            json_file = open("config.json", "w")
            json_file.write(json.dumps(user_config, indent=4))
            json_file.close()

            self.white_texts_background()
            self.justify()
            self.state_disable()
            self.render_settings_windows()

            # TODO
            # nie wiem czy takie cos wystarczy czy trzeba zrobic cos lepszego
            self.make_auctions_list()
            self.find_auction_index()
            # self.update_main_window() - stara funkcja
        else:
            self.white_texts_background()
            mark_wrong_boxes(change_color)
            if error_type == 0:
                tkinter.messagebox.showerror("Auction Reminder Assistant",
                                             "Time_Clock_Value_Error\n\nYou have inputted too big values or they have wrong format!\nPlease, "
                                             "correct these mistakes.")
            elif error_type == 1:
                tkinter.messagebox.showerror("Auction Reminder Assistant",
                                             "Time_Clock_Value_Error\n\nFrequency can't be equal zero!\nPlease, "
                                             "correct this mistake.")
            elif error_type == 2:
                tkinter.messagebox.showerror("Auction Reminder Assistant",
                                             "Time_Clock_Value_Error\n\nEnding time must be greater than Starting "
                                             "time!\nPlease, correct this mistake.")
            elif error_type == 3:
                tkinter.messagebox.showerror("Auction Reminder Assistant",
                                             "Time_Clock_Value_Error\n\nRemind time must be lower than Frequency "
                                             "time!\nPlease, correct this mistake.")

            change_color.clear()

    def state_normal(self):

        self.text_freq_hour.config(state=NORMAL)
        self.text_freq_minute.config(state=NORMAL)
        self.text_freq_second.config(state=NORMAL)

        self.text_start_hour.config(state=NORMAL)
        self.text_start_minute.config(state=NORMAL)
        self.text_start_second.config(state=NORMAL)

        self.text_end_hour.config(state=NORMAL)
        self.text_end_minute.config(state=NORMAL)
        self.text_end_second.config(state=NORMAL)

        # text_remind_hour.config(state=NORMAL)
        self.text_remind_minute.config(state=NORMAL)
        self.text_remind_second.config(state=NORMAL)

    def state_disable(self):

        self.text_freq_hour.config(state=DISABLED)
        self.text_freq_minute.config(state=DISABLED)
        self.text_freq_second.config(state=DISABLED)

        self.text_start_hour.config(state=DISABLED)
        self.text_start_minute.config(state=DISABLED)
        self.text_start_second.config(state=DISABLED)

        self.text_end_hour.config(state=DISABLED)
        self.text_end_minute.config(state=DISABLED)
        self.text_end_second.config(state=DISABLED)

        # text_remind_hour.config(state=DISABLED)
        self.text_remind_minute.config(state=DISABLED)
        self.text_remind_second.config(state=DISABLED)

    def white_texts_background(self):

        self.text_freq_hour.config(bg="white")
        self.text_freq_minute.config(bg="white")
        self.text_freq_second.config(bg="white")

        self.text_start_hour.config(bg="white")
        self.text_start_minute.config(bg="white")
        self.text_start_second.config(bg="white")

        self.text_end_hour.config(bg="white")
        self.text_end_minute.config(bg="white")
        self.text_end_second.config(bg="white")

        self.text_remind_minute.config(bg="white")
        self.text_remind_second.config(bg="white")

    def clear(self):

        self.text_freq_hour.delete(1.0, END)
        self.text_freq_minute.delete(1.0, END)
        self.text_freq_second.delete(1.0, END)

        self.text_start_hour.delete(1.0, END)
        self.text_start_minute.delete(1.0, END)
        self.text_start_second.delete(1.0, END)

        self.text_end_hour.delete(1.0, END)
        self.text_end_minute.delete(1.0, END)
        self.text_end_second.delete(1.0, END)

        # text_remind_hour.delete(1.0, END)
        self.text_remind_minute.delete(1.0, END)
        self.text_remind_second.delete(1.0, END)

    def justify(self):

        self.text_freq_hour.tag_configure("center", justify='center')
        self.text_freq_minute.tag_configure("center", justify='center')
        self.text_freq_second.tag_configure("center", justify='center')

        self.text_start_hour.tag_configure("center", justify='center')
        self.text_start_minute.tag_configure("center", justify='center')
        self.text_start_second.tag_configure("center", justify='center')

        self.text_end_hour.tag_configure("center", justify='center')
        self.text_end_minute.tag_configure("center", justify='center')
        self.text_end_second.tag_configure("center", justify='center')

        # text_remind_hour.tag_configure("center", justify='center')
        self.text_remind_minute.tag_configure("center", justify='center')
        self.text_remind_second.tag_configure("center", justify='center')

        self.text_freq_hour.tag_add("center", "1.0", "end")
        self.text_freq_minute.tag_add("center", "1.0", "end")
        self.text_freq_second.tag_add("center", "1.0", "end")

        self.text_start_hour.tag_add("center", "1.0", "end")
        self.text_start_minute.tag_add("center", "1.0", "end")
        self.text_start_second.tag_add("center", "1.0", "end")

        self.text_end_hour.tag_add("center", "1.0", "end")
        self.text_end_minute.tag_add("center", "1.0", "end")
        self.text_end_second.tag_add("center", "1.0", "end")

        # text_remind_hour.tag_add("center", "1.0", "end")
        self.text_remind_minute.tag_add("center", "1.0", "end")
        self.text_remind_second.tag_add("center", "1.0", "end")

    # config.json
    def whether_config_exist(self):
        print("WHETHER FILE EXIST")
        # It looks like, your settings file has been deleted.
        # Please input your settings again.

        default_config = {
            "frequency": {
                "freq_hour": "00",
                "freq_minute": "01",
                "freq_second": "00"
            },
            "start": {
                "start_hour": "00",
                "start_minute": "35",
                "start_second": "00"
            },
            "end": {
                "end_hour": "23",
                "end_minute": "59",
                "end_second": "59"
            },
            "remind": {
                "remind_minute": "01",
                "remind_second": "00"
            }
        }

        try:
            json_file = open("config.json")
            # whether_file_is_complete()
            json_file.close()
        except FileNotFoundError:
            tkinter.messagebox.showerror("Auction Reminder Assistant",
                                         "File_Not_Found_Error:\n\nIt looks like, your settings file has been deleted, "
                                         "has changed directory  or has an inappropriate name.\n\nDefault settings will be recovered.", )

            json_file = open("config.json", "w")
            json_file.write(json.dumps(default_config, indent=4))
            # file.write("01:00:00\n" + "00:35:00\n" + "23:59:59\n" + "00:01:00")
            json_file.close()

    def load_config_json(self):
        print("LOAD_CONFIG_JSON")

        json_file = open("config.json", "r")
        user_config = json.load(json_file)
        json_file.close()

        self.freq_hour = user_config["frequency"]["freq_hour"]
        self.freq_minute = user_config["frequency"]["freq_minute"]
        self.freq_second = user_config["frequency"]["freq_second"]

        self.start_hour = user_config["start"]["start_hour"]
        self.star_minute = user_config["start"]["start_minute"]
        self.start_second = user_config["start"]["start_second"]

        self.remind_minute = user_config["remind"]["remind_minute"]
        self.remind_second = user_config["remind"]["remind_second"]


    ''' FUNCTIONS TO CHECKING '''
    def check_internet_connection(self):
        # INFORMACJA:
        # polaczenie z internetem sprawdzam przed kazda czynosci ktora tego wymaga

        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            print("\nInternet connection exist")
            self.internet_connection = True

        except OSError:
            print("No Internet connection")
            self.internet_connection = False
            self.info_label_4.config(text="No Internet connection")

        self.info_label_4.after(900000, self.check_internet_connection)

    def read_user_auth_key(self):
        # if zero data, then verify is the only one options

        read_auth_key = "none"

        try:
            auth_key_file = open("auth_key_file.txt", "r")
            read_auth_key = auth_key_file.readline()
            self.auth_key_origin = "read"
            self.user_auth_key = read_auth_key
            print("Auth key: " + read_auth_key + " read from local computer")
            auth_key_file.close()

            # check_auth_key_in_database(read_auth_key)

        except FileNotFoundError:
            print("Auth_key_file doesn't exist")
            self.user_auth_key = "none"
            # Jesli nie ma pliku, to sa wyswietlane ustawienia "domyslne" okna

        # print("read_auth_key: " + read_auth_key)

        if self.internet_connection is True:
            if read_auth_key != "none" and len(read_auth_key) > 0:
                self.check_auth_key_in_database(read_auth_key)
            # self.check_auth_key_in_database(read_auth_key)
        else:
            self.render_licence_window(self.licence_status, read_auth_key, "none")
            # if len(read_auth_key) == 0:
            #     self.render_licence_window(self.licence_status, "none", "none")
            # else:
            #     self.render_licence_window(self.licence_status, read_auth_key, "none")

    def get_current_date_from_server(self):
        # HOW PYTHON WORKS WITH PHP
        # Czy to jest bezpieczne ?
        url = 'http://localhost/Auction%20Reminder/php_server/current_date.php'
        response = urllib.request.urlopen(url)
        string_from_url = response.read().decode("utf-8")
        server_date = json.loads(string_from_url)

        # print(type(server_date))
        # print(server_date['fulldate'])

        return server_date

    def check_auth_key_in_database(self, auth_key):


        # Opis dzialania
        # 1 sprawdz auth key
        # a) jesli istnieje pobierze reszte danych
        # b) jesli nie zwroc blad

        try:
            db_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="auction_reminder",
                port=33060
            )
        except mysql.connector.Error as err:
            print("Database issue, validation impossible\n")
            #print(err)

            # licence_window()
            self.render_licence_window(None, auth_key, None, "Database issue, validation impossible")
            self.light_diode_up()
            return

        # POBIERAM DANE Z SERWERA
        db_request = db_conn.cursor()
        db_request.execute("SELECT username, auth_key, status FROM generated_auth_keys WHERE auth_key= %s", (auth_key,))
        req_result = db_request.fetchall()

        if len(req_result) == 0:
            # Jesli pusta wartosc, znaczy ze nie ma takiego auth key
            print("Invalid auth key, doesn't exist in database")

            # licence_status = "invalid"

            # jesli mniejsze od zera przy wczytaniu jest napis none

            self.render_licence_window(self.licence_status, auth_key, "Invalid")
            self.light_diode_up()

            return
        else:

            username = req_result[0][0]
            status = req_result[0][2]

            if status == "used":
                # oznaca to ze ten auth key ejst juz wykorzystany
                self.render_licence_window(None, None, None, "This auth key is already used")
                self.light_diode_up()
                return

            else:
                # Jesli auth key istnieje i jest poprawny, sprawdzamy waznosc licencji
                # do niego przypisanej i pobieramy dane po to aby przerwac dzialanie porgramu
                # jesli licencja straci waznosc

                db_request.execute("SELECT expiry_date FROM licence_informations WHERE username=%s", (username,))
                req_result = db_request.fetchall()

                self.licence_expiry_date = req_result[0][0]  # datetime object
                self.current_server_date = self.get_current_date_from_server()  # dictionary (int)

                print("Current date: " + self.current_server_date["fulldate"])
                print("Expiry date: " + str(self.licence_expiry_date))

                self.licence_status = self.compare_dates(self.current_server_date, self.licence_expiry_date)
                if self.licence_status == "Valid":
                    print("Licence is valid")

                    # ZAPOBIEGA PRZED KILKUKROTNYM WYWOLANIEM ZEGARA
                    if self.licence_status == "Valid" and self.cloak_status == "Inactive":
                        self.make_auctions_list()
                        self.find_auction_index()

                        self.digital_clock()
                        self.cloak_status = "Active"
                    else:
                        print("Prevent from multi using")

                    # Poniewaz caly program zaczynamy od wczytania licencji z pliku nalezy
                    # ten plik w tym miejscu zaktualizowac, poniewz podano poprawny auth key

                    # sprawdzam czy auth key byl wczytany z pliku, czy podany przez uzytkownika
                    if self.auth_key_origin == "input":
                        print("Auth key in local computer changed successful")
                        auth_key_file = open("auth_key_file.txt", "w")
                        auth_key_file.write(auth_key)
                        auth_key_file.close()

                else:
                    print("Licence is expired")

                    # Sorry, your licence expired
                    # Go to our website buy new licence

                self.render_licence_window(self.licence_status, auth_key, "Valid")
                self.light_diode_up()




        db_conn.close()

    def compare_dates(self, current_date, expiry_date):

        # check YEAR
        if current_date['year'] > expiry_date.year:
            return "Invalid"
        elif current_date['year'] == expiry_date.year:

            # check MONTH
            if current_date['month'] > expiry_date.month:
                return "Invalid"
            elif current_date['month'] == expiry_date.month:

                # check DAY
                if current_date['day'] > expiry_date.day:
                    return "Invalid"
                elif current_date['day'] == expiry_date.day:

                    # check HOUR
                    if current_date['hour'] > expiry_date.hour:
                        return "Invalid"
                    elif current_date['hour'] == expiry_date.hour:

                        # check MINUTE
                        if current_date['minute'] > expiry_date.minute:
                            return "Invalid"
                        elif current_date['minute'] == expiry_date.minute:

                            # check SECOND
                            if current_date['second'] > expiry_date.second:
                                return "Invalid"
                            else:
                                return "Valid"

                        else:
                            return "Valid"
                    else:
                        return "Valid"
                else:
                    return "Valid"
            else:
                return "Valid"
        else:
            return "Valid"

    ###########################################################

    def verify_licence(self):

        self.check_internet_connection()

        if self.internet_connection is True:

            inputted_auth_key = self.text_enter_licence.get(1.0, END).strip()
            self.auth_key_origin = "input"
            self.user_auth_key = inputted_auth_key
            print("Auth key: " + inputted_auth_key + " inputted by user")
            self.check_auth_key_in_database(inputted_auth_key)

        else:
            # tutaj nie podaje zadnych argumentow do funkcji bo sprawdzanie stanu
            # polaczenia jest na pierwszym miejscu
            self.render_licence_window()

        # ZAPOBIEGA PRZED KILKUKROTNYM WYWOLANIEM ZEGARA
        # if self.licence_status == "Valid" and self.cloak_status == "Inactive":
        #     self.digital_clock()
        #     self.cloak_status = "Active"
        # else:
        #     print("Prevent from multi using")

    def render_licence_window(self, lic_stat=None, auth_key=None, input_stat=None, other=None):

        # cala ta funckje musze przebudowac
        # musze przewidziec mozliwie jak najwiecej bledow ktore moga wystapic podczas
        # uzytkowania programu, nazwac je i dla kazdej z nazw zrobic osobe renderowaine okna licencij

        #TODO:
        # Nowe nazwy bledow:
        # 1) Brak polaczenia z internetem: 'No internet connection'
        # 2) Bład bazy danych: 'Database issue, validation impossible'
        # 3) Prawidłowy auth_key z wazna licencja: 'Verification successful'
        # 4) Wpisany auth_key jest juz w uzyciu: 'This auth key is already used'
        # 5) Niepoprawny auth_key: 'Invalid auth key'
        # 6) Aktualny auth_key jest poprawny, nowy auth_key nie jest poprawny/wazny: 'Changes not applied, invalid auth key'
        # 7) Licencja wygasła: 'Licence expired'
        # 8) Plik z auth_key nie istnieje: 'Licence status=Invalid Auth key=none'
        # 9) Plik za auth_key istnieje, pokazuje jakis auth key jest w srodku(jak len=0 to none)

        # print("lic_stat: " + str(lic_stat))
        # print("auth_key: " + str(auth_key))
        # print("input_stat: " + str(input_stat))
        # print("other: " + str(other))
        # print("\n")

        if auth_key is not None and len(auth_key) == 0: auth_key = "none"

        if self.internet_connection is False:
            self.label_validation_info.config(text="Validation impossible, no Internet connection")
            self.label_valid_invalid.config(text="Invalid", fg="red", )
            self.label_auth_key_value.config(text=auth_key, fg="red", )
        elif other is not None:

            self.label_valid_invalid.config(text="Invalid", fg="red", )
            self.label_auth_key_value.config(text=auth_key, fg="red", )
            self.label_validation_info.config(text=other)

        else:

            # stylizuje status licencji
            if lic_stat == "Valid" and input_stat == "Valid":
                self.label_valid_invalid.config(text="Valid", fg="#33cc33", )
                self.label_auth_key_value.config(text=auth_key, fg="#33cc33", )

            if lic_stat == "Invalid" and input_stat == "Valid":
                self.label_valid_invalid.config(text="Invalid", fg="red", )
                self.label_auth_key_value.config(text=auth_key, fg="red", )

            if lic_stat == "Invalid" and input_stat == "Invalid":
                self.label_valid_invalid.config(text="Invalid", fg="red", )
                self.label_auth_key_value.config(text=auth_key, fg="red", )

            # przypadek gdy serwer usunie niaktywna licencje
            if lic_stat == "Invalid" and input_stat is None:
                self.label_valid_invalid.config(text="Invalid", fg="red", )
                self.label_auth_key_value.config(text=auth_key, fg="red", )


            # stylizuje komunikaty o bledach
            if lic_stat == "Valid" and input_stat == "Valid":

                if self.auth_key_origin == "input":
                    self.label_validation_info.config(text="Verification successful")
                    self.label_validation_info.config(fg="#33cc33")

            if lic_stat == "Valid" and input_stat == "Invalid":
                self.label_validation_info.config(text="Changes not applied, invalid auth key")
                self.label_validation_info.config(fg="red")

            if lic_stat == "Invalid" and input_stat == "Valid":
                # nie wiem czy w poprawnie dzialjacy serwerze i bazie danych
                # taka sytuacja moze sie wydarzyc, chodzi tutaj o okresowe
                # usuwanie nieaktywnych licencji
                self.label_validation_info.config(text="Licence expired")
                self.label_validation_info.config(fg="red")

            if lic_stat == "Invalid" and input_stat == "Invalid":
                self.label_validation_info.config(text="Invalid auth key")
                self.label_validation_info.config(fg="red")

            if lic_stat == "Invalid" and input_stat is None:
                self.label_validation_info.config(text="Licence expired")
                self.label_validation_info.config(fg="red")


    ''' INFINITY CHECKING FUNCTIONS'''
    def check_licence_remaining_time(self):
        # ta funkcja co 15min bedzie sprawdzac status licencji na podstawie
        # wprowadzonego auth key

        self.current_server_date = self.get_current_date_from_server()  # dictionary (int)

        if self.current_server_date is not None and self.licence_expiry_date is not None:

            if self.compare_dates(self.current_server_date, self.licence_expiry_date) == "Valid":

                print("Licence is still valid: " + self.user_auth_key)
                self.label_validation_info.after(90000, self.check_licence_remaining_time)

            else:
                print("Licence has just expired: " + self.user_auth_key)
                self.licence_status = "Invalid"
                # TODO: odpowiednie rendwrowanie okna Licence
        else:
            print("Good auth key hasn't been entered yet")
            self.label_validation_info.after(90000, self.check_licence_remaining_time)


root = Tk()

app = AuctionReminder(root)

app.whether_config_exist()
app.load_config_json()
app.render_settings_windows()

app.check_internet_connection()
app.read_user_auth_key()

app.check_licence_remaining_time()

root.mainloop()





