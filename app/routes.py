from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, AssetForm
from .models import User, ADAEntry, ChangeLog
from . import db, login_manager
from datetime import datetime

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==============================================================
# STARTUP INTERFACE
# ==============================================================

@main.route('/')
def index():
    if current_app.config.get("DEBUG_BYPASS_STARTUP"):
        return redirect(url_for('main.login'))
    return redirect(url_for('main.startup'))

@main.route('/startup', methods=['GET', 'POST'])
def startup():
    if request.method == 'POST':
        answer = request.form.get('answer', '').strip().lower()
        if answer == 'only at the blind':
            return redirect(url_for('main.login'))
        flash('ACCESS DENIED: Authorization phrase invalid.')
        return redirect(url_for('main.startup'))
    return render_template('startup.html')

# ==============================================================
# AUTHENTICATION
# ==============================================================

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.')
            return redirect(url_for('main.register'))

        new_user = User(
            username=form.username.data,
            password=form.password.data,
            clearance=form.clearance.data,
            role='regular'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ==============================================================
# DASHBOARD + ASSET VIEW
# ==============================================================

@main.route('/dashboard')
@login_required
def dashboard():
    entries = ADAEntry.query.filter(ADAEntry.clearance_level <= current_user.clearance).all()
    return render_template('dashboard.html', user=current_user, entries=entries)

@main.route('/asset/<int:asset_id>')
@login_required
def view_asset(asset_id):
    asset = ADAEntry.query.get_or_404(asset_id)
    if current_user.clearance < asset.clearance_level:
        flash("Insufficient clearance.")
        return redirect(url_for('main.dashboard'))
    return render_template('asset_detail.html', asset=asset)

# ==============================================================
# ASSET CREATION / EDITING
# ==============================================================

@main.route('/add-asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    if current_user.role not in ['admin', 'regular']:
        flash("You do not have permission to add entries.", "danger")
        return redirect(url_for('main.dashboard'))

    form = AssetForm()

    if form.validate_on_submit():
        # Regular users can't assign a higher clearance than their own
        if form.clearance_level.data > current_user.clearance:
            flash("You can't assign a clearance level higher than your own.", "danger")
            return redirect(url_for('main.add_asset'))

        new_entry = ADAEntry(
            asset_number=form.asset_number.data,
            title=form.title.data,
            content=form.content.data,
            redacted_text=form.redacted_text.data,
            clearance_level=form.clearance_level.data,
            created_by=current_user.id
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("New ADA entry created successfully.", "success")
        return redirect(url_for('main.dashboard'))

    return render_template("add_asset.html", form=form, edit=False)


@main.route('/edit-asset/<int:asset_id>', methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    asset = ADAEntry.query.get_or_404(asset_id)
    form = AssetForm(obj=asset)

    if form.validate_on_submit():
        asset.asset_number = form.asset_number.data
        asset.title = form.title.data
        asset.content = form.content.data
        asset.redacted_text = form.redacted_text.data
        asset.clearance_level = form.clearance_level.data
        db.session.commit()

        log = ChangeLog(asset_id=asset.id, edited_by=current_user.id, note="Entry edited")
        db.session.add(log)
        db.session.commit()

        flash("Asset updated.")
        return redirect(url_for('main.dashboard'))

    return render_template('add_asset.html', form=form, edit=True)

@main.route('/delete-asset/<int:asset_id>')
@login_required
def delete_asset(asset_id):
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    asset = ADAEntry.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash("Asset deleted.")
    return redirect(url_for('main.dashboard'))

# ==============================================================
# ADMIN PANEL
# ==============================================================

@main.route('/admin-panel')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    users = User.query.all()
    return render_template('admin_panel.html', users=users)

@main.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.clearance = int(request.form['clearance'])
        user.role = request.form['role']
        db.session.commit()
        flash("User updated.")
        return redirect(url_for('main.admin_panel'))

    return render_template('edit_user.html', user=user)

@main.route('/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own account.")
        return redirect(url_for('main.admin_panel'))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.")
    return redirect(url_for('main.admin_panel'))
