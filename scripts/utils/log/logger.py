from datetime import datetime

log_file_path = r"log.txt"

def write_to_log(string):

    with open(log_file_path, "a") as log_file:
        
        current_time = datetime.now()
        current_day_time = current_time.strftime("%H:%M:%S")
        current_date = current_time.strftime("%d:%m:%Y")
        
        new_log_line = "\n[" + current_day_time + "][" + current_date + "] " + string
        
        log_file.write(new_log_line)
    