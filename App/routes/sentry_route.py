
from flask import render_template,Blueprint, request


sentry_blue = Blueprint("sentry", __name__, static_folder="../static", template_folder="../templates")


@sentry_blue.route('/debug-sentry')
def trigger_error():
  division_by_zero = 1 / 0