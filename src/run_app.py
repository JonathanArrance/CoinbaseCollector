import subprocess
import schedule
from database import Database

db = Database()

args = ['bash','entrypoint.sh']
out = subprocess.Popen(args, stdout=subprocess.PIPE)
# Run the command
output = out.communicate()[0]

schedule.every().day.at(settings.TRIM).do(db.trim_db)