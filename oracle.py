#!/usr/bin/env python3
# Week Math oracle - mirrors engine.js using Python's datetime and a day-by-day walk, not the engine's integer formulas.
import json, re, datetime as dt, random

DATE_ERR = "enter a date as YYYY-MM-DD, a real calendar date from 1583 to 9000"
YEAR_ERR = "the ISO year must be a whole number from 1583 to 9000"
WEEK_ERR = "the week must be a whole number from 1 to 53"
DAY_ERR = "the weekday must be a whole number from 1 (Monday) to 7 (Sunday)"
NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def pdate(t):
    t = t.strip() if isinstance(t, str) else ""
    m = re.fullmatch(r"([0-9]{4})-([0-9]{2})-([0-9]{2})", t)
    if not m: raise ValueError(DATE_ERR)
    y, mo, d = map(int, m.groups())
    if not 1583 <= y <= 9000: raise ValueError(DATE_ERR)
    try: return dt.date(y, mo, d)
    except ValueError: raise ValueError(DATE_ERR)

def pint(t, pat, lo, hi, err):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(pat, t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)

def weeks_in(y):
    # Cross-check on every call: the Thursday rule must agree with the Dec 28 rule.
    jan1 = dt.date(y, 1, 1).weekday()
    assert (53 if jan1 == 3 or (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) and jan1 == 2) else 52) == dt.date(y, 12, 28).isocalendar()[1]
    # a year has 53 weeks if it starts on Thursday, or is a leap year starting on Wednesday
    return 53 if dt.date(y, 12, 28).isocalendar()[1] == 53 else 52

def plural(n, one, many): return f"{n} {one if n == 1 else many}"

def week_truth(date):
    d = pdate(date)
    iy, wk, wd = d.isocalendar()
    mon = d - dt.timedelta(days=wd - 1)
    out = f"{d.isoformat()} is a {NAMES[wd-1]}. It falls in ISO week {wk} of {iy}, Monday {mon.isoformat()} to Sunday {(mon + dt.timedelta(days=6)).isoformat()}. ISO year {iy} has {weeks_in(iy)} weeks."
    if iy != d.year: out += f" The ISO year {iy} differs from the calendar year {d.year}."
    return out

def date_truth(year, week, weekday):
    y = pint(year, r"[0-9]{1,4}", 1583, 9000, YEAR_ERR)
    w = pint(week, r"[0-9]{1,2}", 1, 53, WEEK_ERR)
    d = pint(weekday, r"[0-9]", 1, 7, DAY_ERR)
    try:
        z = dt.date.fromisocalendar(y, w, d)
    except ValueError:
        raise ValueError(f"ISO year {y} has {weeks_in(y)} weeks, so week {w} does not exist")
    out = f"ISO year {y}, week {w}, weekday {d} is {NAMES[d-1]} {z.isoformat()}. ISO year {y} has {weeks_in(y)} weeks."
    if z.year != y: out += f" That date is in calendar year {z.year}."
    return out

def span_truth(a, b):
    da, db = pdate(a), pdate(b)
    back = db < da
    lo, hi = (db, da) if back else (da, db)
    n = (hi - lo).days
    wk = we = 0
    cur = lo
    while cur < hi:
        if cur.weekday() < 5: wk += 1
        else: we += 1
        cur += dt.timedelta(days=1)
    out = f"From {da.isoformat()} to {db.isoformat()} is {plural(n,'day','days')} ({plural(n//7,'week','weeks')} and {plural(n%7,'day','days')})."
    if back: out += " The second date is earlier, so this counts backward."
    out += f" Counting the earlier date but not the later one: {plural(wk,'weekday','weekdays')} (Monday to Friday) and {plural(we,'weekend day','weekend days')}."
    return out

FNS = {"weekTruth": week_truth, "dateTruth": date_truth, "spanTruth": span_truth}

def cases():
    c = []
    rnd = random.Random(692)
    dates = ["2024-12-30", "2024-12-29", "2026-12-31", "2027-01-01", "2027-01-03", "2027-01-04", "2021-01-03", "2021-01-04",
             "2020-12-31", "2020-02-29", "2021-02-29", "2023-02-29", "2100-02-29", "2000-02-29", "1900-02-28", "1583-01-01",
             "1583-01-02", "9000-12-31", "9000-01-01", "2026-13-01", "2026-00-10", "2026-04-31", "2026-4-1", "", "  2026-06-15  ",
             "1582-12-31", "9001-01-01", "2015-12-31", "2016-01-01", "2016-01-03", "2009-12-31", "2010-01-03", "2026-02-30", "abcd-ef-gh"]
    for _ in range(40):
        dates.append(dt.date.fromordinal(rnd.randint(dt.date(1583, 1, 1).toordinal(), dt.date(9000, 12, 31).toordinal())).isoformat())
    for d in dates: c.append(("weekTruth", [d]))
    for y in [2026, 2025, 2020, 2015, 2021, 2024, 1583, 9000, 2004, 2009, 2032]:
        for w, d in [(1, 1), (52, 7), (53, 4), (53, 1), (26, 3)]:
            c.append(("dateTruth", [str(y), str(w), str(d)]))
    for args in [["1582", "1", "1"], ["9001", "1", "1"], ["2026", "0", "1"], ["2026", "54", "1"], ["2026", "5", "0"], ["2026", "5", "8"],
                 ["abc", "5", "1"], ["2026", "x", "1"], ["2026", "5", "y"], ["", "", ""], [" 2026 ", " 10 ", " 5 "], ["02026", "10", "5"], ["2026", "010", "5"], ["2026", "07", "01"]]:
        c.append(("dateTruth", args))
    for a, b in [("2026-01-01", "2026-03-01"), ("2026-03-01", "2026-01-01"), ("2026-05-05", "2026-05-05"), ("2026-05-05", "2026-05-06"),
                 ("2026-05-02", "2026-05-04"), ("2026-05-09", "2026-05-10"), ("2024-02-28", "2024-03-01"), ("2023-02-28", "2023-03-01"),
                 ("1583-01-01", "9000-12-31"), ("2026-12-31", "2027-01-01"), ("2026-05-04", "2026-05-11"), ("2026-05-04", "2026-05-12"),
                 ("2026-5-4", "2026-05-11"), ("2026-05-04", "bad"), ("bad", "2026-05-04"), ("2026-05-04", "2026-02-30"), ("", "")]:
        c.append(("spanTruth", [a, b]))
    for _ in range(25):
        a = dt.date.fromordinal(rnd.randint(dt.date(1583, 1, 1).toordinal(), dt.date(9000, 12, 31).toordinal()))
        b = a + dt.timedelta(days=rnd.randint(-40, 400)) if rnd.random() < .7 else dt.date.fromordinal(rnd.randint(dt.date(1583, 1, 1).toordinal(), dt.date(9000, 12, 31).toordinal()))
        c.append(("spanTruth", [a.isoformat(), b.isoformat()]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
json.dump(out, open("expected.json", "w"), indent=1)
print(len(out), "cases written")
