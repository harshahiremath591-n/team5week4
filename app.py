from flask import Flask, render_template, request, redirect, session, jsonify
from models import db, User, Task, Job, Material, Electrician
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from sqlalchemy import func
from datetime import datetime, timedelta
from datetime import datetime, UTC
today = datetime.now(UTC)

app = Flask(__name__)
app.secret_key = "secret123"

import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def get_current_user():
    if 'user' in session:
        return User.query.filter_by(username=session['user']).first()
    return None

# -------- LOGIN --------
@app.route('/', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()

        if user and check_password_hash(user.password, request.form.get('password')):
            session['user'] = user.username
            return redirect('/dashboard')
        else:
            error = "Invalid Username or Password"

    return render_template('login.html', error=error)

# -------- REGISTER --------
@app.route('/register', methods=['GET','POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password != confirm:
            error = "Passwords do not match"
        else:
            existing = User.query.filter_by(username=username).first()

            if existing:
                error = "User already exists"
            else:
                user = User(
                    username=username,
                    password=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
                return redirect('/')

    return render_template('register.html', error=error)

#-----photo upload------
@app.context_processor
def inject_user():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        return dict(user=user)
    return dict(user=None)

# -------- DASHBOARD --------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    user = User.query.filter_by(username=session['user']).first()

    return render_template('dashboard.html', user=user)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -------- TASKS --------
@app.route('/tasks', methods=['GET','POST'])
def tasks():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        task = Task(
            description=request.form.get('desc'),
            status=request.form.get('status'),
            job_id=request.form.get('job'),
            electrician_id=request.form.get('electrician')
        )
        db.session.add(task)
        db.session.commit()

    return render_template(
    'tasks.html',
    data=Task.query.all(),
    jobs=Job.query.all(),
    electricians=Electrician.query.all(),
    user=get_current_user()
)

# -------- JOBS --------
@app.route('/jobs', methods=['GET','POST'])
def jobs():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            location=request.form.get('location'),
            deadline=request.form.get('deadline'),
            electrician_id=request.form.get('electrician')
        )
        db.session.add(job)
        db.session.commit()

    return render_template(
    'jobs.html',
    data=Job.query.all(),
    electricians=Electrician.query.all(),
    user=get_current_user()
)

# -------- MATERIALS --------
@app.route('/materials', methods=['GET','POST'])
def materials():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        material = Material(
            name=request.form.get('name'),
            quantity=request.form.get('qty')
        )
    elif type == "material":
        item.name = request.form['name']
        item.quantity = int(request.form['qty'])    
    
        db.session.add(material)
        db.session.commit()

    return render_template(
    'materials.html',
    data=Material.query.all(),
    user=get_current_user()
)

# -------- ELECTRICIANS --------
@app.route('/electricians', methods=['GET','POST'])
def electricians():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        e = Electrician(
            name=request.form.get('name'),
            phone=request.form.get('phone')
        )
        db.session.add(e)
        db.session.commit()

    return render_template(
    'electricians.html',
    data=Electrician.query.all(),
    user=get_current_user()
)

# -------- DELETE --------
@app.route('/delete/<type>/<int:id>')
def delete(type, id):
    model = {"task":Task,"job":Job,"material":Material,"electrician":Electrician}.get(type)
    item = model.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/'+type+'s')

# -------- EDIT --------
@app.route('/edit/<type>/<int:id>', methods=['GET','POST'])
def edit(type, id):

    model_map = {
        "task": Task,
        "job": Job,
        "material": Material,
        "electrician": Electrician
    }

    model = model_map.get(type)
    item = model.query.get(id)

    if request.method == 'POST':

        if type == "task":
            item.description = request.form.get('desc')
            item.status = request.form.get('status')

        elif type == "job":
            item.title = request.form.get('title')
            item.location = request.form.get('location')

        elif type == "material":
            item.name = request.form.get('name')
            item.quantity = int(request.form.get('qty'))

        elif type == "electrician":
            item.name = request.form.get('name')
            item.phone = request.form.get('phone')

        db.session.commit()
        return redirect('/' + type + 's')

    return render_template('edit.html', item=item, type=type)

# -------- STATS --------
@app.route('/stats')
def stats():
    return jsonify({
        "tasks": Task.query.count(),
        "jobs": Job.query.count(),
        "materials": Material.query.count(),
        "electricians": Electrician.query.count()
    })
    
# -------- REPORTS --------

# 📅 DAILY WORK REPORT
@app.route('/report/daily', methods=['GET'])
def daily_report():
    date = request.args.get('date')

    if date:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()

        tasks = Task.query.filter(
            func.date(Task.time) == selected_date
        ).all()
    else:
        tasks = Task.query.all()

    return render_template('report_daily.html', data=tasks, user=get_current_user())


# ✅ TASK COMPLETION REPORT
@app.route('/report/completed')
def completed_report():
    tasks = Task.query.filter_by(status="Completed").all()
    return render_template('report_completed.html', data=tasks, user=get_current_user())


# 👷 ELECTRICIAN ACTIVITY REPORT
@app.route('/report/electrician')
def electrician_report():
    electricians = Electrician.query.all()
    return render_template('report_electrician.html', data=electricians, user=get_current_user())

@app.route('/report/pdf')
def download_pdf():
    date = request.args.get('date')

    if date:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        tasks = Task.query.filter(
            func.date(Task.time) == selected_date
        ).all()
    else:
        tasks = Task.query.all()

    file = "report.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Filtered Report", styles['Title']))

    for t in tasks:
        job = t.job.title if t.job else "No Job"
        text = f"{t.description} | {t.status} | {job}"
        content.append(Paragraph(text, styles['Normal']))

    doc.build(content)

    from flask import send_file
    return send_file(file, as_attachment=True)


@app.route('/report/pdf_file')
def pdf_file():
    from flask import send_file
    return send_file("report.pdf", as_attachment=True)

#------------weekly report----------------
@app.route('/report/weekly')
def weekly_report():
    today = datetime.utcnow()
    week_ago = today - timedelta(days=7)

    tasks = Task.query.filter(Task.time >= week_ago).all()

    return render_template('report_daily.html', data=tasks, user=get_current_user())

#------------monthly report----------------
@app.route('/report/monthly')
def monthly_report():
    today = datetime.utcnow()
    month_ago = today - timedelta(days=30)

    tasks = Task.query.filter(Task.time >= month_ago).all()

    return render_template('report_daily.html', data=tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)