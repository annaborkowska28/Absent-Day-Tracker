from tkinter import *
import psycopg2
from tkcalendar import Calendar
import datetime
import holidays
import os
from dotenv import load_dotenv
from tkinter import ttk #for styling


#connect to postgres
load_dotenv()
conn = psycopg2.connect(
    host='localhost',
    database='calendar',
    user=os.getenv('user'),
    password=os.getenv('password')

)

#create cursor object
cur = conn.cursor()

# Create a table to store absences

cur.execute("""
CREATE TABLE IF NOT EXISTS absences(
id SERIAL PRIMARY KEY,
date DATE NOT NULL)

""")

conn.commit()



# Create Object
window = Tk()
window.title('Absent Day Tracker')
# Set geometry
window.geometry("500x600")


#datetime module to get current year, day and month
x = datetime.datetime.now()
current_year = x.year
current_day = x.day
current_month = x.month



style = ttk.Style(window)
style.map('Calendar.DateEntry', fieldbackground=[('selected', 'red')])
# Add Calendar
cal = Calendar(window, selectmode='day', year=current_year, month=current_month, day=current_day, weekendforeground='blue')
cal.pack(pady=20)

# Listbox for displaying holidays
holiday_listbox = Listbox(window, width=50, height=5)
holiday_listbox.pack(pady=20)

# Label for displaying absence count
absence_count_label = Label(window, text=f"Total Absences: 0")
absence_count_label.pack(pady=10)

def select_date():
    #get selected date
    selected_date = cal.selection_get()
    date.config(text=str(selected_date) + ' Added successfully to the data base ')
    selected_date_str = selected_date.strftime('%Y-%m-%d')

    #insert selected_date into the DB
    query = f"INSERT INTO absences (date) VALUES ('{selected_date_str}')"
    cur.execute(query)
    conn.commit()
    count_absences()

    cal.tag_config('highlight', background='red')
    cal.calevent_create(selected_date, 'selected', 'highlight')

#Load and highlight saved dates
cur.execute('SELECT date from absences', )
rows = cur.fetchall()
for row in rows:
    saved_date = row[0]
    # selected dates remain highlighted in red when you reopen the calendar
    cal.tag_config('highlight', background='red')
    cal.calevent_create(saved_date, 'saved', 'highlight', )


def holiday_days(year, month):
    pl_holidays = holidays.country_holidays('PL', years=current_year)
    holiday_listbox.delete(0, END)
    cal.calevent_remove(tag='highlight_green')
    holidays_found = False

    for holiday_date, holiday_name in pl_holidays.items():
        if holiday_date.month == month and holiday_date.year == year:
            cal.tag_config('highlight_green', background='green')
            cal.calevent_create(holiday_date, 'Holiday', 'highlight_green')
            holiday_listbox.insert(END, f"{holiday_date} : {holiday_name}")
            holidays_found = True

    if not holidays_found:
        holiday_listbox.insert(END, "No holidays this month")


def month_changed(event):
    selected_year = cal.get_displayed_month()[1]
    selected_month = cal.get_displayed_month()[0]
    holiday_days(selected_year, selected_month)

def count_absences():
    selected_year = cal.get_displayed_month()[1]
    selected_month = cal.get_displayed_month()[0]
    query = f"""
    SELECT COUNT(*)
    FROM absences
    WHERE EXTRACT(YEAR from date) = {selected_year}
    AND EXTRACT(MONTH from date) = {selected_month}
"""
    cur.execute(query)
    count = cur.fetchone()[0]
    absence_count_label.config(text=f"Total Absences: {count}")

cal.bind("<<CalendarMonthChanged>>", month_changed)

# Add Button and Label
Button(window, text="Add Absence", command=select_date).pack(pady=20)

date = Label(window, text="")
date.pack(pady=20)

current_displayed_year = cal.get_displayed_month()[1]
current_displayed_month = cal.get_displayed_month()[0]
holiday_days(current_displayed_year, current_displayed_month)
count_absences()

window.mainloop()
# Close the database connection when the window is closed
conn.close()