"""D-Kevin guestbook: a small Flask + MySQL full-stack demo application."""
from flask import Flask, jsonify, redirect, render_template, request, url_for

import db


def create_app():
    app = Flask(__name__)

    try:
        db.init_db()
    except Exception as exc:  # pragma: no cover - startup diagnostics only
        app.logger.warning("Could not initialize database on startup: %s", exc)

    @app.route("/")
    def index():
        messages = db.get_messages()
        return render_template("index.html", messages=messages)

    @app.route("/messages", methods=["POST"])
    def create_message():
        name = (request.form.get("name") or "").strip() or "Anonymous"
        content = (request.form.get("content") or "").strip()
        if content:
            db.add_message(name[:80], content[:1000])
        return redirect(url_for("index"))

    @app.route("/api/messages", methods=["GET"])
    def api_list_messages():
        return jsonify(
            [
                {
                    "id": m["id"],
                    "name": m["name"],
                    "content": m["content"],
                    "created_at": m["created_at"].isoformat()
                    if m.get("created_at")
                    else None,
                }
                for m in db.get_messages()
            ]
        )

    @app.route("/api/messages", methods=["POST"])
    def api_create_message():
        payload = request.get_json(silent=True) or {}
        name = (payload.get("name") or "").strip() or "Anonymous"
        content = (payload.get("content") or "").strip()
        if not content:
            return jsonify({"error": "content is required"}), 400
        new_id = db.add_message(name[:80], content[:1000])
        return jsonify({"id": new_id, "name": name, "content": content}), 201

    @app.route("/health")
    def health():
        try:
            db.init_db()
            return jsonify({"status": "ok"})
        except Exception as exc:
            return jsonify({"status": "error", "detail": str(exc)}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
