import logging
import sys
import os


def count_strm_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".strm"):
                count += 1
    return count


def count_emup(live_tv_entries, tv_dir, movies_dir, unsorted_dir):
    # from parser import tv_dir, movies_dir, unsorted_dir
    tv_strm_count = count_strm_files(tv_dir)
    movie_strm_count = count_strm_files(movies_dir)
    unsorted_strm_count = count_strm_files(unsorted_dir)
    livetv_channels_count = len(live_tv_entries)
    return livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count


def errz(errors):
    if errors:
        print("\nTotal number of errors:", len(errors))
        for error in errors:
            print(error)


def final_output(errors, livetv_channels_count, movie_strm_count, tv_strm_count, unsorted_strm_count):
    print("\nTotal number of errors:", len(errors))
    print("\nNumber of movies parsed =", movie_strm_count)
    print("Number of episodes parsed =", tv_strm_count)
    print("Number of unsorted entries parsed =", unsorted_strm_count)
    print("Number of live TV channels parsed =", livetv_channels_count)


def setup_logging(log_file_path):
    with open(log_file_path, 'w'):
        pass
    # Retrieve log level from environment variable or default to INFO
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    # Configure logging with file and stream handlers
    logging.basicConfig(
        level=numeric_level,
        format='%(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    class StreamToLogger:
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            pass

    # Redirect stdout and stderr to loggers
    sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), numeric_level)
    sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)

def log_shut_down():
    logging.shutdown()