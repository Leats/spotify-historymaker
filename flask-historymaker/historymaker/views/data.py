from collections import Counter
import functools

from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from historymaker.models import db, Artist, Context, Played, Track
import datetime

bp = Blueprint("data", __name__, url_prefix="/data")


@bp.route("/played", methods=("GET",))
def played():
    # played = db.session.query(Played, Track, Context).join(Track).join(Context).order_by(Played.time.desc()).all()
    played = (
        db.session.query(Played, Track, Context, Artist)
        .join(Track, Track.uri == Played.trackuri, isouter=True)
        .join(Context, Context.uri == Played.contexturi, isouter=True)
        .join(Artist, Artist.uri == Played.artisturi, isouter=True)
        .order_by(Played.time.desc())
        .all()
    )
    data = []
    for p in played:
        p2 = p[2].__dict__ if p[2] is not None else {}
        p3 = p[3].__dict__
        row = {
            **p[0].__dict__,
            **p[1].__dict__,
            **p2,
            **{"genre": p3["genre"], "artistname": p3["name"], "artistid": p3["id"]},
        }
        # spotify's api doesn't tell if a song gets skipped halfway through
        # by calculating the difference between two songs and checking with the duration
        # we should be able to get at least a better estimate of the actual time listened
        row["unixtime"] = (
            row["time"] - datetime.datetime(1970, 1, 1)
        ).total_seconds() * 1000
        row["actualduration"] = (
            min(row["duration"], data[-1]["unixtime"] - row["unixtime"])
            if len(data) > 0
            else row["duration"]
        )
        row.pop("_sa_instance_state")
        data.append(row)
    tracks = Counter(k["id"] for k in data)
    artists = Counter(k["artistid"] for k in data)
    return jsonify(
        {
            "items": data,
            "tracks": [(t, c) for t, c in tracks.most_common()[:5]],
            "artists": [(a, c) for a, c in artists.most_common()[:5]],
        }
    )


@bp.route("/tracks", methods=("GET",))
def tracks():
    tracks = db.session.query(Track).all()
    return jsonify(list(t.title for t in tracks))


@bp.route("/artists", methods=("GET",))
def artists():
    artists = db.session.query(Artist).all()
    return jsonify(list(a.name for a in artists))


@bp.route("/p", methods=("GET",))
def p():
    artists = db.session.query(Played).all()
    return jsonify(list(a.time for a in artists))
