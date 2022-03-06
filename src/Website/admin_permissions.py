from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User

admin_permissions = Blueprint('admin', __name__)

@admin_permissions.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    per = current_user.permissions # Permissions
    if per >= 1:
        users = User.query.filter_by().all()
        return render_template('admin.html', user=current_user, users=users)
    else:
        flash('Sorry you must be the Admin to access the Admin page...', 'error')
        return redirect(url_for('views.dashboard'))