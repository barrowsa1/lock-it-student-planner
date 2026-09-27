import calendar as month_calendar
from datetime import date, timedelta

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
assignments = []
priorities = {"low", "medium", "high"}
assignment_filters = {"all", "active", "completed"}


def selected_assignment_filter():
	selected_filter = request.args.get("filter", "all")
	return selected_filter if selected_filter in assignment_filters else "all"


@app.route("/", methods=["GET", "POST"])
def home():
	selected_filter = selected_assignment_filter()
	search_query = request.args.get("q", "").strip()
	today = date.today()
	try:
		calendar_year = int(request.args.get("year", today.year))
		calendar_month = int(request.args.get("month", today.month))
		month_start = date(calendar_year, calendar_month, 1)
	except (TypeError, ValueError):
		month_start = today.replace(day=1)
		calendar_year = month_start.year
		calendar_month = month_start.month

	error = None
	if request.method == "POST":
		assignment = {
			"title": request.form.get("title", "").strip(),
			"course": request.form.get("course", "").strip(),
			"due_date": request.form.get("due_date", "").strip(),
			"priority": request.form.get("priority", "").strip().lower(),
			"completed": False,
		}
		if not all(assignment[field] for field in ("title", "course", "due_date", "priority")) or assignment["priority"] not in priorities:
			error = "Please complete every field and choose a valid priority."
		else:
			assignments.append(assignment)
			selected_filter = "all"
			search_query = ""

	filtered_assignments = [
		(index, assignment)
		for index, assignment in enumerate(assignments)
		if (
			selected_filter == "all"
			or selected_filter == "active" and not assignment["completed"]
			or selected_filter == "completed" and assignment["completed"]
		)
		and (
			not search_query
			or search_query.casefold() in assignment["title"].casefold()
			or search_query.casefold() in assignment["course"].casefold()
		)
	]

	due_by_date = {}
	for assignment in assignments:
		try:
			due_date = date.fromisoformat(assignment["due_date"])
		except (KeyError, TypeError, ValueError):
			continue
		if due_date.year == calendar_year and due_date.month == calendar_month:
			due_by_date.setdefault(due_date.isoformat(), []).append(assignment)

	selected_day = None
	try:
		requested_day = date.fromisoformat(request.args.get("day", ""))
	except (TypeError, ValueError):
		requested_day = None
	if requested_day and requested_day.strftime("%Y-%m") == month_start.strftime("%Y-%m") and requested_day.isoformat() in due_by_date:
		selected_day = requested_day

	calendar_weeks = []
	for week in month_calendar.Calendar(firstweekday=month_calendar.MONDAY).monthdayscalendar(calendar_year, calendar_month):
		calendar_week = []
		for day_number in week:
			day_date = date(calendar_year, calendar_month, day_number) if day_number else None
			calendar_week.append({
				"day": day_number or None,
				"iso_date": day_date.isoformat() if day_date else None,
				"assignments": due_by_date.get(day_date.isoformat(), []) if day_date else [],
			})
		calendar_weeks.append(calendar_week)

	previous_month = month_start - timedelta(days=1) if month_start > date.min else None
	if calendar_month == 12:
		next_month = date(calendar_year + 1, 1, 1) if calendar_year < date.max.year else None
	else:
		next_month = date(calendar_year, calendar_month + 1, 1)
	selected_day_assignments = due_by_date.get(selected_day.isoformat(), []) if selected_day else []

	return render_template(
		"index.html",
		filtered_assignments=filtered_assignments,
		selected_filter=selected_filter,
		search_query=search_query,
		calendar_year=calendar_year,
		calendar_month=calendar_month,
		calendar_month_label=month_start.strftime("%B %Y"),
		calendar_weeks=calendar_weeks,
		weekday_names=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
		today=today,
		previous_month=previous_month,
		next_month=next_month,
		selected_day=selected_day,
		selected_day_label=selected_day.strftime("%A, %B %d") if selected_day else None,
		selected_day_assignments=selected_day_assignments,
		error=error,
	)


@app.post("/assignments/<int:assignment_index>/toggle-completion")
def toggle_completion(assignment_index):
	if assignment_index >= len(assignments):
		abort(404)

	assignments[assignment_index]["completed"] = not assignments[assignment_index]["completed"]
	return redirect(url_for(
		"home",
		filter=selected_assignment_filter(),
		q=request.args.get("q", "").strip() or None,
		year=request.args.get("year", type=int),
		month=request.args.get("month", type=int),
		day=request.args.get("day") or None,
	))


@app.post("/assignments/<int:assignment_index>/delete")
def delete_assignment(assignment_index):
	if assignment_index >= len(assignments):
		abort(404)

	assignments.pop(assignment_index)
	return redirect(url_for(
		"home",
		filter=selected_assignment_filter(),
		q=request.args.get("q", "").strip() or None,
		year=request.args.get("year", type=int),
		month=request.args.get("month", type=int),
		day=request.args.get("day") or None,
	))


if __name__ == "__main__":
	app.run(debug=True)
