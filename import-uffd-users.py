import httpx
import random
import string
from dotenv import dotenv_values
import sqlite3
import time
import os

config = {
    **dotenv_values(".env"),
    **os.environ,
}


def generate_ref():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(22)
    )


def get_uffd_users():
    response = httpx.get(
        f"{config['UFFD_API_ENDPOINT']}/api/v1/getusers",
        auth=(config["UFFD_API_USER"], config["UFFD_API_PASSWORD"]),
    )
    response.raise_for_status()
    return response.json()


def import_uffd_users():
    db = sqlite3.connect(config["GRIST_DB_PATH"])

    cur = db.cursor()

    for user in get_uffd_users():
        res = cur.execute(
            "SELECT user_id FROM logins WHERE email = ?", (user["loginname"],)
        )
        if u := res.fetchone():
            user_id = u[0]
        else:
            cur.execute(
                "INSERT INTO users (name, ref) VALUES (?, ?)",
                (user["loginname"], generate_ref()),
            )
            user_id = cur.lastrowid
            cur.execute(
                "INSERT INTO logins (user_id, email, display_email) VALUES (?, ?, ?)",
                (
                    user_id,
                    user["loginname"],
                    user["loginname"],
                ),
            )
            user_id = cur.lastrowid

        db.commit()

        res = cur.execute(
            "SELECT * FROM group_users WHERE user_id = ? AND group_id = ?",
            (user_id, config["GRIST_GROUP_ID"]),
        )
        if not res.fetchone():
            cur.execute(
                "INSERT INTO group_users (user_id, group_id) VALUES (?, ?)",
                (user_id, config["GRIST_GROUP_ID"]),
            )
            db.commit()


while True:
    import_uffd_users()
    time.sleep(60)
