from flask import Blueprint,render_template,request,redirect,flash,url_for
from . import db
from .models import User, Note 
from flask_login import login_required, current_user,logout_user
from .models import  Note
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1 :
            flash('Note is too short, please write in detail !!!',category="error")
        else:
            new_note = Note(title=title,text=note,user_id=current_user.id)

            db.session.add(new_note)
            db.session.commit()
            flash(' your note is added' ,category= 'success')

    return render_template("index.html",user=current_user)

@views.route("/all-users")
@login_required
def allUsers():
    all_users=User.query.all()
    var=[]
    for user in all_users:
        notes=Note.query.filter_by(user_id=user.id).all()
        if len(notes)>0:
            var.append(len(notes))
        else:
            var.append(0)
    zipped=zip(all_users,var)


    return render_template("showusers.html",all_users=zipped,user=current_user)

@views.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def deleteNote(id):
    note = Note.query.filter_by(id=id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("your note is successfully deleted", category="success")
    return render_template("index.html",user=current_user)

@views.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def updateNote(id):
    if request.method == 'POST':
        title=request.form['title']
        text=request.form['note']   
        note = Note.query.filter_by(id=id).first()
        note.title=title
        note.text=text
        db.session.add(note)
        db.session.commit()
        return render_template("index.html",user=current_user)

    note_update = Note.query.filter_by(id=id).first()
    return render_template("update.html",nu=note_update,user=current_user)

@views.route("/details/<int:id>",methods=['GET','POST'])   
@login_required
def details(id):
    note_update = Note.query.filter_by(id=id).first()
    return render_template("details.html",nu=note_update,user=current_user)

@views.route("/deleteAcc/<int:id>",methods=['GET','POST'])
@login_required
def deleteACC(id):
    user = User.query.filter_by(id=id).first()
    if user:
        if len(user.notes)>0:
            notes=Note.query.filter_by(user_id=user.id).all()
            for note in notes:
                db.session.delete(note)
                db.session.commit()
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Account is successfully deleted",category="success")
        return redirect(url_for("views.home"))
    return render_template("index.html",user=current_user)

@views.route('/changePass/<int:id>',methods=['GET','POST'])
@login_required
def changePass(id):
    if request.method == 'POST':
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        if pass1==pass2:
            user = User.query.filter_by(id=id).first()
            user.password = generate_password_hash(pass1,method="sha256")
            db.session.add(user)
            db.session.commit()
            logout_user()
            flash("Password have changed successfully",category="success")
            return redirect(url_for("views.home"))
            
        else:
            flash('Passwords does not match.' , category="error")
    return render_template("index.html",user=current_user)
            




