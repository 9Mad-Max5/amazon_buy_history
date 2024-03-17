# Amazon buy History
This program is used to scrape amazon.de in you buy history for all elements. \
It is using python with selenium so using up some resources. \
The scrape process is unfortunatley quite time intesive. \
But can be adjusted  with the constants.py file. \
The information will be stored in one xlsx file.
At the moment it can run multiple times on the same file.

## ToDo
 - [ ] Check and maybe adjust for amazon.com
 - [x] Possibility to update history file
 - [x] Get a UI
 - [x] Running selenium headless
 - [ ] Compile it to a single file


## Known "issues"
Sometimes it takes ages to download a single year. This is normal unfortunately and caused by amazon itself. The use preventive actions to slow down the request speed. Especially if your whole history is downloaded and you used this tool excessively in the meantime. Your account will get slowed down. But just be patient and have a look in the logger file to see some progress.