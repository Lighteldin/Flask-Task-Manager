#                            TASK MANAGER GRAPHICAL USER INTERFACE APPLICATION (v1.0.0)

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from task_logic.task import Task
from task_logic.task_json import TaskJSON


app = Flask(__name__)
database = TaskJSON()

# Valid operations that can be triggered from the tasks page.
VALID_OPERATIONS = ['add_task','reset_tasks','reset_tags']

# ==================================================================
# Route handlers
#                           Functions:
# index() -> Index page: redirect to daily/overall tasks.
# tasks_page() -> Tasks page: handle task operations for both daily and overall tasks.
# add() -> Add task page: handle adding a new task.
# edit() -> Edit task page: handle editing an existing task.
# view() -> View task page: display task details.
# ==================================================================

@app.route("/", methods=["GET", "POST"])
def index():
    """Index page: redirect to daily/overall tasks."""    
    
    if request.method == 'POST':
        task_type = request.form.get('task_type')

        if task_type in ['daily', 'overall']:
            return _redirect_url_for(task_type)
        
    return render_template('tasks.html', active_tab='index')


@app.route("/<task_type>", methods=["GET", "POST"])
def tasks_page(task_type):
    """Tasks page: handle task operations for both daily and overall tasks."""
    
    if request.method == "POST":
        operation = request.form.get("operation")

        if operation in VALID_OPERATIONS:
            return _process_task_operation(task_type, operation)
        
        task_id_to_delete = request.form.get("row_delete")
        if task_id_to_delete:
            database.delete_task(int(task_id_to_delete), task_type)
            return _redirect_url_for(task_type)
        
        task_id_to_toggle_finished = request.form.get("row_toggle_finished")
        if task_id_to_toggle_finished:
            database.toggle_task_finished(int(task_id_to_toggle_finished), task_type)
            return _redirect_url_for(task_type)


    tasks = database.get_tasks_by_type(task_type)
    return render_template("tasks.html", 
                           tasks=tasks, 
                           active_tab=task_type, 
                           humanize_datetime=humanize_datetime, # function
                           get_deadline_status=get_deadline_status) #function


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add task page: handle task addition or cancel."""
    
    if request.method == 'POST':
        click_operation = request.form.get('click_operation')  # "cancel" or "add"
        
        if click_operation == 'cancel':
            return _redirect_url_for(request.form.get("task_type", "index"))
        if click_operation == 'add':
            _log_form_submission()
            task_type = _process_entry_task('add')
            return _redirect_url_for(task_type)
    
    return render_template('entry.html', 
                           id=database.get_next_id(), # New task ID
                           tags=database.get_tags(), # Existing tags
                           active_tab='add' # For showing the correct tab
                           ) 


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Edit task page: handle task editing or cancel."""
    
    task_id = request.args.get('task')
    result = database.get_task_by_id(int(task_id)) if task_id else None
    if not result:
        return "Task not found", 404

    task, task_type = result  # safe unpacking now
    print(result,'\n') 
    print(task_type,'\n') 
    if request.method == 'POST':
        click_operation = request.form.get('click_operation')  # "cancel" or "save"
        if click_operation == 'cancel':
            return _redirect_url_for(request.form.get("task_type", "index"))
        if click_operation == 'edit':
            _log_form_submission()
            task_type = _process_entry_task('edit')
            print(task_type,'\n')
            return _redirect_url_for(task_type)

    task['deadline'] = fix_deadline_format(task['deadline'])
    # GET request → render form
    return render_template('entry.html', 
                           id=task['id'], 
                           title=task['title'],
                           description=task['description'],
                           tags=database.get_tags(),
                           selected_tags=task['tags'],
                           new_tags="",
                           deadline=task['deadline'],
                           task_type=task_type,
                           active_tab='edit')


@app.route("/view", methods=["GET"])
def view():
    """View task page: display task details."""
    
    task_id = request.args.get('task')
    result = database.get_task_by_id(int(task_id)) if task_id else None
    if not result:
        return "Task not found", 404

    task, task_type = result  # safe unpacking now
    return render_template('view.html', 
                           id=task['id'], 
                           title=task['title'],
                           description=task['description'],
                           selected_tags=task['tags'],
                           deadline=task['deadline'],
                           task_type=task_type,
                           active_tab='view')

# ==================================================================
# Helper functions
#                           Functions:
# _log_form_submission() -> Debugging
# _process_entry_task() -> Process task entry form data
# _redirect_url_for() -> Redirect to URL
# fix_deadline_format() -> Convert ISO 8601 to 'YYYY-MM-DDTHH:MM'
# humanize_datetime() -> Convert datetime to human-readable format
# get_deadline_status() -> Get deadline status

# ==================================================================

def _log_form_submission():
    """Debugging."""
    print(f'task_type: {request.form.get("task_type")}\n')
    print(f'id: {request.form.get("id")}\n')
    print(f'title: {request.form.get("title")}\n')
    print(f'description: {request.form.get("description")}\n')
    print(f'tags: {request.form.getlist("tags")}\n')
    print(f'new_tags: {request.form.get("new_tags")}\n')
    print(f'deadline: {request.form.get("deadline")}\n')


def _process_entry_task(entry_type: str):
    """Process task entry form data and return task type."""
    
    def _build_task_from_form():
        """Build task from form data."""

        task_type = request.form.get("task_type")
        id = request.form.get("id")
        title = request.form.get("title")
        description = request.form.get("description")
        tags = request.form.getlist("tags")
        new_tags = request.form.get("new_tags")
        all_tags = tags if tags else []
        if new_tags:
            for tag in new_tags.split(','):
                tag = tag.strip()
                if tag and tag not in all_tags:
                    all_tags.append(tag)   
        deadline = request.form.get("deadline")
        return task_type.lower(), Task(
            type=task_type.lower(),
            id=int(id),
            title=title,
            description=description,
            tags=all_tags,
            deadline=deadline
        )
    
    task_type, entry_task = _build_task_from_form()
    
    if entry_type == 'edit':
        database.edit_task(entry_task.to_dict(), task_type)
    elif entry_type == 'add':
        database.add_task(entry_task.to_dict(), task_type)
    
    # always return task_type so we redirect correctly
    return task_type


def _redirect_url_for(page_name):
    """Redirect to a specific page."""
        
    if page_name in ("daily", "overall"):
        return redirect(url_for("tasks_page", task_type=page_name))
    return redirect(url_for(page_name))


def _process_task_operation(task_type, operation):
    """Process task operations."""
    
    if operation == VALID_OPERATIONS[0]:  # 'add_task'
        return _redirect_url_for('add')
    
    if operation == VALID_OPERATIONS[1]:  # 'reset_tasks'
        database.reset_tasks(task_type)
        return _redirect_url_for(task_type)
    
    if operation == VALID_OPERATIONS[2]:  # 'reset_tags'
        database.reset_tags()
        return _redirect_url_for(task_type)


def fix_deadline_format(deadline):
    """Convert ISO 8601 to 'YYYY-MM-DDTHH:MM' for HTML datetime-local input."""
    
    if not deadline:
        return None
    try:
        dt = datetime.fromisoformat(deadline)
        return dt.strftime("%Y-%m-%dT%H:%M")
    except ValueError:
        return None


def humanize_datetime(value, format="%a %b %d, %Y %I:%M %p"):
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)  # parse ISO string like 2025-10-01T12:12
        except ValueError:
            return value
    return value.strftime(format).replace("AM", "am").replace("PM", "pm")


def get_deadline_status(task_dict):
    """Get deadline status."""
    
    task = Task.from_dict(task_dict)
    
    delta = task.get_time_left()
    
    if task.finished:
        return "deadline-finished"
    if delta is None:
        return "deadline-none"
    if delta.total_seconds() < 0:
        return "deadline-overdue"
    if delta.days == 0:
        return "deadline-today"
    return "deadline-upcoming"


# ==================================================================
# Application entry point
# ==================================================================

if __name__ == "__main__":
    app.run(debug=True)
