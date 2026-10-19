// Week Math engine: ISO week date arithmetic on whole days (proleptic Gregorian calendar, Monday first).
var DATE_ERR = "enter a date as YYYY-MM-DD, a real calendar date from 1583 to 9000";
var YEAR_ERR = "the ISO year must be a whole number from 1583 to 9000";
var WEEK_ERR = "the week must be a whole number from 1 to 53";
var DAY_ERR = "the weekday must be a whole number from 1 (Monday) to 7 (Sunday)";
var DAYNAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

function _fromCivil(y, m, d) {
  y -= m <= 2 ? 1 : 0;
  var era = Math.floor(y / 400);
  var yoe = y - era * 400;
  var doy = Math.floor((153 * (m + (m > 2 ? -3 : 9)) + 2) / 5) + d - 1;
  var doe = yoe * 365 + Math.floor(yoe / 4) - Math.floor(yoe / 100) + doy;
  return era * 146097 + doe - 719468;
}
function _toCivil(z) {
  z += 719468;
  var era = Math.floor(z / 146097);
  var doe = z - era * 146097;
  var yoe = Math.floor((doe - Math.floor(doe / 1460) + Math.floor(doe / 36524) - Math.floor(doe / 146096)) / 365);
  var y = yoe + era * 400;
  var doy = doe - (365 * yoe + Math.floor(yoe / 4) - Math.floor(yoe / 100));
  var mp = Math.floor((5 * doy + 2) / 153);
  var d = doy - Math.floor((153 * mp + 2) / 5) + 1;
  var m = mp + (mp < 10 ? 3 : -9);
  return [y + (m <= 2 ? 1 : 0), m, d];
}
function _p2(n) { return (n < 10 ? "0" : "") + n; }
function _p4(n) { return ("000" + n).slice(-4); }
function _fmt(z) { var c = _toCivil(z); return _p4(c[0]) + "-" + _p2(c[1]) + "-" + _p2(c[2]); }
function _wd(z) { return (((z + 3) % 7) + 7) % 7 + 1; }
function _date(t) {
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(t);
  if (!m) throw new Error(DATE_ERR);
  var y = parseInt(m[1], 10), mo = parseInt(m[2], 10), d = parseInt(m[3], 10);
  if (y < 1583 || y > 9000 || mo < 1 || mo > 12 || d < 1) throw new Error(DATE_ERR);
  var z = _fromCivil(y, mo, d);
  var c = _toCivil(z);
  if (c[0] !== y || c[1] !== mo || c[2] !== d) throw new Error(DATE_ERR);
  return z;
}
function _int(t, re, lo, hi, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!re.test(t)) throw new Error(err);
  var n = parseInt(t, 10);
  if (n < lo || n > hi) throw new Error(err);
  return n;
}
function _isoYearOf(z) {
  var th = z - (_wd(z) - 1) + 3;
  return _toCivil(th)[0];
}
function _weekOf(z) {
  var th = z - (_wd(z) - 1) + 3;
  var iy = _toCivil(th)[0];
  return [iy, Math.floor((th - _fromCivil(iy, 1, 1)) / 7) + 1];
}
function _weeksIn(y) { return _weekOf(_fromCivil(y, 12, 28))[1]; }
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }

function weekTruth(date) {
  var z = _date(date);
  var w = _weekOf(z), iy = w[0], wk = w[1];
  var mon = z - (_wd(z) - 1);
  var out = _fmt(z) + " is a " + DAYNAMES[_wd(z) - 1] + ". It falls in ISO week " + wk + " of " + iy + ", Monday " + _fmt(mon) + " to Sunday " + _fmt(mon + 6) + ". ISO year " + iy + " has " + _weeksIn(iy) + " weeks.";
  var cy = _toCivil(z)[0];
  if (iy !== cy) out += " The ISO year " + iy + " differs from the calendar year " + cy + ".";
  return out;
}
function dateTruth(year, week, weekday) {
  var y = _int(year, /^[0-9]{1,4}$/, 1583, 9000, YEAR_ERR);
  var w = _int(week, /^[0-9]{1,2}$/, 1, 53, WEEK_ERR);
  var d = _int(weekday, /^[0-9]{1}$/, 1, 7, DAY_ERR);
  var n = _weeksIn(y);
  if (w > n) throw new Error("ISO year " + y + " has " + n + " weeks, so week " + w + " does not exist");
  var jan4 = _fromCivil(y, 1, 4);
  var z = jan4 - (_wd(jan4) - 1) + (w - 1) * 7 + (d - 1);
  var out = "ISO year " + y + ", week " + w + ", weekday " + d + " is " + DAYNAMES[d - 1] + " " + _fmt(z) + ". ISO year " + y + " has " + n + " weeks.";
  var cy = _toCivil(z)[0];
  if (cy !== y) out += " That date is in calendar year " + cy + ".";
  return out;
}
function spanTruth(a, b) {
  var za = _date(a), zb = _date(b);
  var back = zb < za;
  var lo = back ? zb : za, hi = back ? za : zb;
  var n = hi - lo;
  var full = Math.floor(n / 7), rest = n % 7;
  var wkdays = full * 5;
  for (var i = 0; i < rest; i++) if (_wd(lo + i) <= 5) wkdays += 1;
  var end = n - wkdays;
  var out = "From " + _fmt(za) + " to " + _fmt(zb) + " is " + _plural(n, "day", "days") + " (" + _plural(full, "week", "weeks") + " and " + _plural(rest, "day", "days") + ").";
  if (back) out += " The second date is earlier, so this counts backward.";
  out += " Counting the earlier date but not the later one: " + _plural(wkdays, "weekday", "weekdays") + " (Monday to Friday) and " + _plural(end, "weekend day", "weekend days") + ".";
  return out;
}
