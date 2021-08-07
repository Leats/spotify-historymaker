import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


bp = Blueprint("visualizations", __name__, url_prefix="/visualizations")


@bp.route("/overview", methods=("GET",))
def overview():
    return render_template("/overview.html")
