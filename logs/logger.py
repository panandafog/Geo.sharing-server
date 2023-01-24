from pathlib import Path
from datetime import datetime
import io
import utils.files as files

output_directory = './logs_output/'
main_log_name = 'main_log'
encoding = 'utf8'
log_files = {}


def get_time():
    return datetime.now().strftime("%d/%m/%y %H:%M:%S")


def init_logging(name=main_log_name):
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    filename = output_directory + name + '_' + files.get_long_time_str() + '.log'
    with io.open(filename, 'w', encoding=encoding) as outfile:
        outfile.write(files.get_long_time_str() + ': Start logging\n')
    log_files[name] = filename


def log(message='', file=main_log_name):
    with io.open(log_files[file], 'a', encoding=encoding) as outfile:
        outfile.write(get_time() + ': ' + message + '\n')
        print(message)


def error(message='', file=main_log_name):
    with io.open(log_files[file], 'a', encoding=encoding) as outfile:
        outfile.write('[ERROR] ' + get_time() + ': ' + message + '\n')
        print('[ERROR] ' + message)