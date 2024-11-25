import logging
import sys

def configure_logging():
    """Configure logging for the application."""
    log_file = 'data_handler.log'
    handlers = [logging.FileHandler(log_file)]

    # Only add StreamHandler if running with console
    # if sys.stdout is not None:
    #     handlers.append(logging.StreamHandler())

    # Following line is necessary to ensure all libs and packages can 
    # write on log_file. Disabling this and running pyinstaller in --noconsole mode
    # causes these streams to be set as None which causes some libs to throw exceptions.
    # Like tqdm uses std.err and thows exception if does not find it. Hence, by manually
    # setting the stream files we can redirect those streams to log file. 
    # If you Disable following 2 lines then make sure to not pass --noconsole flag in pyinstaller.
    # The only line that causes issue in my knowledge is tqdm. We can remove it but there
    # is a possiblity of other libs causing same issue as well. So, better approach is to redirect
    # all the streams to log file. 
    sys.stdout = open(log_file, 'a') # Sets standard ouput to log_file
    sys.stderr = open(log_file, 'a') # Sets standard error to log_file
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=handlers
    )
