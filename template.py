import os
from pathlib import Path
import logging

#logging string--format of log --logging msg
# logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')
list_of_files = [
    ".github/workflows/.gitkeep",
    "models/components/__init__.py",
    "models/utils/__init__.py",
    "models/config/configuration.py",
    "models/pipeline/__init__.py",
    "requirements.txt",
    "setup.py",
    "notebook/trials.ipynb",
    "templates/index.html",
    "frontend"
    "backend/scrapper.py",
    "backend/seo.py",
    "backend/wordpressapi.py",
    "backend/database",
    
#flask framework
]
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename=os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"creating directory:{filedir} for file{filename}") 

    if(not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
            pass
        logging.info(f"creating file:{filename}")
    
    else:
        logging.info(f"file already exist:{filename}")

