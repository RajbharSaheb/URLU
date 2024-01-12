
import calendar
import time
import os
from pyrogram import Client, filters, emoji

@Client.on_message(filters.command(["Calendar"]))
def print_calendar(year):
  """Prints a calendar for the given year."""

  # Get the first and last day of the year.
  first_day = calendar.datetime(year, 1, 1)
  last_day = calendar.datetime(year, 12, 31)

  # Get the number of days in the year.
  num_days = (last_day - first_day).days + 1

  # Get the number of weeks in the year.
  num_weeks = calendar.monthrange(year, 1)[1]

  # Create a list of the days of the year.
  days = []
  for i in range(num_days):
    day = first_day + timedelta(days=i)
    days.append(day)

  # Create a list of the weeks of the year.
  weeks = []
  for i in range(num_weeks):
    week = days[i * 7:(i + 1) * 7]
    weeks.append(week)

  # Print the calendar.
  for week in weeks:
    for day in week:
      print(day.strftime("%Y-%m-%d"), end=" ")
    print()

if __name__ == "main":
  # Get the year from the user.
  year = int(input("Enter a year: "))

  # Print the calendar.
  print_calendar(year)
