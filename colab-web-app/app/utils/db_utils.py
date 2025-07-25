# app/utils/db_utils.py

import sqlite3
from flask import current_app

def get_connection():
    """
    Open a new SQLite connection using the configured DB_PATH.
    Returns a connection with Row factory enabled.
    """
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    conn.row_factory = sqlite3.Row
    return conn

def get_username_by_id(user_id):
    """
    Return the username for a given user_id, or None if not found.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["username"] if row else None

def get_user_by_id(user_id):
    """
    Return a Row object for the user with id=user_id,
    containing fields id, username, is_admin, or None.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, is_admin FROM users WHERE id = ?",
        (user_id,)
    )
    user = cur.fetchone()
    conn.close()
    return user

def get_all_users():
    """
    Return a list of Row objects for all users (id, username, is_admin).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_tactics():
    """
    Return a list of Row objects for all innovation tactics
    (id, title, summary, purpose).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, summary, purpose
          FROM innovation_tactics;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def update_user(user_id, username, is_admin):
    """
    Update the username and admin flag for a given user_id.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
           SET username = ?, is_admin = ?
         WHERE id = ?;
    """, (username, is_admin, user_id))
    conn.commit()
    conn.close()

def delete_user_db(user_id):
    """
    Delete the user record with id=user_id.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
