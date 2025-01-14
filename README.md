# Absent-Day-Tracker
The Absent Day Tracker is a desktop application built using Python, Tkinter, and PostgreSQL. It allows users to track absences and public holidays. Users can select dates from a calendar, add them as absences to the database, and view the total count of absences for the currently displayed month. Additionally, the application highlights public holidays in Poland and displays them in a list.  
Key Features:

1. Calendar Integration:
Uses the **tkcalendar** library to display a calendar widget.
Users can select dates to mark as absences.
Selected dates are highlighted in red on the calendar.
2. Database Connectivity:
Connects to a **PostgreSQL** database to store and retrieve absences.
Uses the psycopg2 library for database operations.
Absences are stored in a table named absences.
3. Public Holidays:
Displays public holidays in Poland for the selected month.
Highlights public holidays in green on the calendar.
Lists holidays in a listbox for easy viewing.
4. Absence Count:
Calculates and displays the total number of absences for the currently displayed month.
Automatically updates the absence count when a new date is added or the month is changed.

Libraries Used:
1. Tkinter: For the graphical user interface.
2. tkcalendar: For the calendar widget.
3. psycopg2: For PostgreSQL database connectivity.
4. holidays: To fetch public holidays.
5. dotenv: To load environment variables (e.g., database credentials).
