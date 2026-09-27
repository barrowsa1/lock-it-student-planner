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

	filtered_assignments = [
		(index, assignment)
		for index, assignment in enumerate(assignments)
		if selected_filter == "all"
		or selected_filter == "active" and not assignment["completed"]
		or selected_filter == "completed" and assignment["completed"]
	]
	return render_template(
		"index.html",
		filtered_assignments=filtered_assignments,
		selected_filter=selected_filter,
		error=error,
	)


@app.post("/assignments/<int:assignment_index>/toggle-completion")
def toggle_completion(assignment_index):
	if assignment_index >= len(assignments):
		abort(404)

	assignments[assignment_index]["completed"] = not assignments[assignment_index]["completed"]
	return redirect(url_for("home", filter=selected_assignment_filter()))


@app.post("/assignments/<int:assignment_index>/delete")
def delete_assignment(assignment_index):
	if assignment_index >= len(assignments):
		abort(404)

	assignments.pop(assignment_index)
	return redirect(url_for("home", filter=selected_assignment_filter()))


if __name__ == "__main__":
	app.run(debug=True)
