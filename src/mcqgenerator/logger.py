import logging
import os
from datetime import datetime

LOG_File = f"{datetime.now().strftime('(%m_%d_%Y) (%H_%M_%S)')}.log"

log_path=os.path.join(os.getcwd(),'logs')
os.makedirs(log_path,exist_ok=True)

LOG_FilePath=os.path.join(log_path,LOG_File)

logging.basicConfig(
    filename=LOG_FilePath,
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s: %(message)s'
)