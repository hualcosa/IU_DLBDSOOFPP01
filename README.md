# IU_DLBDSOOFPP01
This repository contains the files for my final project of the course <br>
"OBJECT ORIENTED AND FUNCTIONAL PROGRAMMING WITH PYTHON"

To run the habit-tracking app, follow the below steps:
1. Install sqlite3 in your system.(<a href=https://www.servermania.com/kb/articles/install-sqlite/>sqlite installation tutorial</a>)
2. Install python>=3.6  your system. (<a href=https://www.python.org/downloads/>Python installtion tutorial</a>)
3. Install pytest ("pip install pytest")
3. clone this repo
4. *cd* into the folder and type: "python main.py"

An interactive prompt will appear in your terminal with further explanations on how to use the application.

The "file tables_creation.sql" contain the default database data in case you want to "restore factory defaults".
To restoure the defaults, delete the habits.db, then type the following:

sqlite3 habits.db
.read tables_creation.sql

press ctrl+D to quit the SQLITE terminal. 