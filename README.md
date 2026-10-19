# Week Math

ISO week date arithmetic. Monday 30 December 2024 is already in week 1 of 2025, and 2026 has a week 53.

## What it computes

- **The week truth** - the ISO week and ISO year of a date, its Monday-to-Sunday span, and whether the ISO year has 52 or 53 weeks.
- **The date truth** - the calendar date of an ISO year, week and weekday (1 is Monday, 7 is Sunday). Week 53 is refused for years that have only 52 weeks.
- **The span truth** - days, whole weeks and leftover days between two dates, plus weekdays (Monday to Friday) and weekend days, counting the earlier date but not the later one.

Dates use the plain Gregorian calendar, written YYYY-MM-DD, from 1583 to 9000.

## Boundary

Arithmetic only. It counts days and ISO weeks from the owner's own dates. It does not know any employer's, school's, court's or tax office's own week numbering, holidays or deadline rules and gives no verdict on when anything is due.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (whole-day counts, no Date object).
- `oracle.py` - the Python mirror (datetime, day-by-day walk) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (185 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/weekmath/
Repo: https://github.com/iLanis-agent/weekmath
