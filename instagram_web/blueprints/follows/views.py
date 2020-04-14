from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.follow import IdolFan
from flask_login import current_user, login_required
from instagram_web.util.sendmail import send_email_follow


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/new', methods = ['GET'])
@login_required
def new():
    idol = User.get_or_none(User.username == current_user.username)
    requests = IdolFan.select().where(IdolFan.idol_id == idol.id)
    return render_template('follows/new.html', requests = requests)

@follows_blueprint.route('<fan_username>/edit', methods=['POST'])
def edit(fan_username):
    fan = User.get_or_none(User.username == fan_username)
    request = IdolFan.get_or_none((IdolFan.idol_id == current_user.id) & (IdolFan.fan_id == fan.id))
    request.approved = True
    request.save()
    flash(u"Request approved", 'success')
    return redirect(url_for('follows.new'))

@follows_blueprint.route('/<idol_id>', methods=['POST'])
def create(idol_id):
    if not current_user.image_path:
        flash(u"Please set a profile image for yourself first", 'warning')
        return redirect(url_for('users.edit', id=current_user.id))

    idol = User.get_or_none(User.id == idol_id)
    if current_user.id == idol.id:
        flash(u"You cannot follow yourself", 'warning')
        return redirect(url_for('home'))
    elif idol.private:
        follow = IdolFan(fan = current_user.id, idol = idol.id)
        follow.save()
        sender = current_user.username
        receiver_email = idol.email
        send_email_follow(sender, receiver_email)
        flash (u"Your request have been submitted for approval", 'info')
        return redirect(url_for('users.show', username = idol.username))
    else:
        follow = IdolFan(fan = current_user.id, idol = idol.id, approved=True)
        follow.save()
        flash(f"You are now following {idol.username}", 'success')
        return redirect(url_for('users.show', username = idol.username))

@follows_blueprint.route('/<idol_id>/delete', methods=['POST'])
def delete(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    unfollow = IdolFan.get_or_none((IdolFan.fan_id == current_user.id) & (IdolFan.idol_id == idol.id))
    if not unfollow:
        flash(u"Cannot unfollow", 'warning')
        return redirect(url_for('users.show', username=idol.username))
    else:
        try:
            unfollow.delete_instance()
            flash(u"You unfollowed this user", 'success')
            return redirect(url_for('users.show', username=idol.username))
        except:
            flash(u"An error has occurred. Please try again", 'warning')
            return redirect(url_for('users.show', username=idol.username))







