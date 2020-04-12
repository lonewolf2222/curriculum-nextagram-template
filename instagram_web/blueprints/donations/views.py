from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.donation import Donation
from models.image import Image
from models.user import User
from flask_login import current_user, login_required
from instagram_web.util.braintree import gateway
from instagram_web.util.sendmail import send_email

donations_blueprint = Blueprint(
    'donations', __name__, template_folder="templates")

@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)
    client_token = gateway.client_token.generate()

    if client_token:
        return render_template('donations/new.html', image=image, client_token=client_token)

@donations_blueprint.route('<image_id>', methods=['POST'])
def create(image_id):
    image = Image.get_or_none(Image.id == image_id)
    nonce = request.form.get("payment_method_nonce")
    amount = request.form.get("amount")
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        donation = Donation(amount=amount, image_id=image.id, user_id=current_user.id)
        donation.save()
        sender = current_user.username
        receiver = User.get_or_none(User.id == image.user_id)
        receiver_email = receiver.email
        send_email(sender, receiver_email, amount)
        flash(u"Thank you for your donation", 'success')
        return redirect(url_for('users.index'))
    else:
        flash(u"An error has occurred", 'warning')
        return redirect(url_for('users.index'))
