# UCSD RIMAC Open Rec Timetable

This project periodically scrapes the UCSD RIMAC Open Rec Timetable and logs them in [log.csv](log.csv).

**Usage**: `python3 main.py`

**Why**: I has occurred to me many times when UCSD Recreation post a RIMAC Aux Gym open rec hour for basketball then later changes it to a different hour (either right before the scheduled time or after the scheduled time when the posted hours has become useless). They use the disclaimer that 'posted hours are subject to change' as an excuse for this unacceptable behavior. This project is a way to keep track of the hours and their changes.

**Note**:

- Change line 64 in `main.py` to the desired time interval. Right now is set to 1 hr.
- New columns will be added to the log file only if the hour changes on the website.