# Lock-It

Lock-It is a simple student planner for organizing assignments, tracking due dates, and keeping coursework on schedule.

## Features

- Add assignments with a title, course name, due date, and priority.
- Mark assignments complete or incomplete; completed assignments have a distinct visual style.
- Delete assignments from the list.
- Search assignments by title or course name.
- Filter the assignment list to show All, Active, or Completed assignments. Search can be combined with these filters.
- View due dates in a monthly calendar with previous- and next-month navigation.
- Select a calendar date with assignments to see all assignments due that day, including their completion status.
- Use the responsive layout, which places the calendar beside the planner on wider screens and below it on smaller screens.

## Technologies Used

- **Python** for the application and calendar calculations.
- **Flask** for HTTP routes and serving the web application. It is the only package listed in `requirements.txt`.
- **Jinja2** for rendering dynamic values and assignment rows in the HTML template.
- **HTML and CSS** for the page structure, forms, calendar, and responsive visual design.

The calendar uses Python's built-in `calendar` and `datetime` modules. The project does not currently use JavaScript, a database, or an external calendar library.

## Project Structure

```text
.
|-- .gitignore
|-- README.md
|-- app.py
|-- requirements.txt
|-- static/
|   `-- style.css
`-- templates/
    `-- index.html
```

- `.gitignore` lists generated and local files Git should ignore.
- `app.py` creates the Flask app and contains the assignment routes, in-memory list, search and filter logic, and calendar date preparation.
- `requirements.txt` lists the Python package dependencies; currently, it contains Flask.
- `static/` holds static assets served by Flask. `static/style.css` contains the page and calendar styles.
- `templates/` holds Jinja2 HTML templates. `templates/index.html` defines the homepage, assignment form and list, search and filters, and calendar.

## Installation and Setup

Install Python 3 and Git before starting. Then open a terminal and follow these steps.

1. Clone the repository and move into its folder:

    ```bash
    git clone https://github.com/barrowsa1/lock-it-student-planner.git
    cd lock-it-student-planner
    ```

2. Create a virtual environment. A virtual environment keeps this project's Python packages separate from other projects.

    **Windows PowerShell**

    ```powershell
    python -m venv .venv
    ```

    **macOS or Linux**

    ```bash
    python3 -m venv .venv
    ```

3. Activate the virtual environment.

    **Windows PowerShell**

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

    **macOS or Linux**

    ```bash
    source .venv/bin/activate
    ```

4. Install the project requirements:

    ```bash
    python -m pip install -r requirements.txt
    ```

## Running Lock-It

After completing Installation and Setup and activating the virtual environment, start the Flask app from the project folder.

**Windows PowerShell**

```powershell
python app.py
```

**macOS or Linux**

```bash
python3 app.py
```

Keep the terminal open while using the app. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. To stop the app, press `Ctrl+C` in the terminal.

## How to Use Lock-It

1. Add an assignment by entering its title, course name, due date, and priority, then select **Add assignment**.
2. Search for assignments by typing a title or course name into the search box and selecting **Search**.
3. Choose **All**, **Active**, or **Completed** to filter the assignment list. Search can be used together with a filter.
4. Select **Mark complete** to complete an assignment. Select **Mark incomplete** to make it active again.
5. Select **Delete** to remove an assignment from the list.
6. Use the calendar arrows to view another month. Select a marked date to see the assignments due on that day.

## Limitations and Notes

In this version, assignments are stored in a Python list in memory rather than in a database. This keeps the project simple, but means assignments are temporary and are cleared when the Flask app restarts. This is an expected limitation of the current version, not an error.

The app runs with Flask's development server and debug mode enabled. Use it for local development, not as a production deployment.
