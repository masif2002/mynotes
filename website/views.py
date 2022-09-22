from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
from . import db
from .models import Note
import json

views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('note')
        note = Note(text=text, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('Note created successfully!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})