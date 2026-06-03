"""
auth.py — מערכת הרשמה/כניסה
• bcrypt  — הצפנת סיסמאות (hash + verify)
• json    — אחסון משתמשים בקובץ users.json
• אין DB חיצוני — מתאים לפרויקט MVP
"""
import json
import os
import re
import bcrypt
import streamlit as st
from datetime import datetime

USERS_FILE = "users.json"


# ── JSON helpers ─────────────────────────────────────────────────────────
def _load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


# ── bcrypt helpers ────────────────────────────────────────────────────────
def _hash_password(password: str) -> str:
    """מחזיר hash של הסיסמה כ-string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, hashed: str) -> bool:
    """בודק סיסמה מול hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ── Validation ────────────────────────────────────────────────────────────
def _validate_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email.strip()))


def _validate_password(pw: str) -> tuple[bool, str]:
    """מחזיר (valid, error_message)"""
    if len(pw) < 6:
        return False, "סיסמה חייבת להכיל לפחות 6 תווים"
    if not re.search(r"\d", pw):
        return False, "סיסמה חייבת להכיל לפחות ספרה אחת"
    return True, ""


# ── Public API ────────────────────────────────────────────────────────────
def signup(username: str, email: str, password: str, grade: str) -> tuple[bool, str]:
    """
    רושם משתמש חדש.
    מחזיר (success, message)
    """
    username = username.strip()
    email    = email.strip().lower()

    if not username or len(username) < 2:
        return False, "שם משתמש חייב להכיל לפחות 2 תווים"
    if not _validate_email(email):
        return False, "כתובת אימייל לא תקינה"
    pw_ok, pw_err = _validate_password(password)
    if not pw_ok:
        return False, pw_err

    users = _load_users()

    if username in users:
        return False, "שם המשתמש כבר תפוס — בחר אחר"
    if any(u["email"] == email for u in users.values()):
        return False, "אימייל זה כבר רשום — נסה להתחבר"

    users[username] = {
        "email":      email,
        "password":   _hash_password(password),
        "grade":      grade,
        "created_at": datetime.now().isoformat(),
        "plan":       "free",
    }
    _save_users(users)
    return True, f"ברוך הבא, {username}! 🎉"


def login(username: str, password: str) -> tuple[bool, str, dict]:
    """
    מתחבר משתמש קיים.
    מחזיר (success, message, user_data)
    """
    username = username.strip()
    users    = _load_users()

    if username not in users:
        return False, "שם משתמש או סיסמה שגויים", {}

    user = users[username]
    if not _verify_password(password, user["password"]):
        return False, "שם משתמש או סיסמה שגויים", {}

    safe_user = {k: v for k, v in user.items() if k != "password"}
    safe_user["username"] = username
    return True, f"שלום, {username}! 👋", safe_user


def is_logged_in() -> bool:
    return bool(st.session_state.get("user"))


def get_current_user() -> dict:
    return st.session_state.get("user", {})


def logout() -> None:
    st.session_state.user = None
    st.session_state.page = "home"


# ── UI Widget ─────────────────────────────────────────────────────────────
def auth_wall(t_fn) -> bool:
    """
    מציג מסך Sign Up / Log In.
    מחזיר True אם המשתמש מחובר, False אחרת.
    """
    if is_logged_in():
        return True

    lang = st.session_state.get("lang", "he")

    st.markdown(
        '<div style="max-width:420px;margin:3rem auto">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sf-hero-title" style="text-align:center;font-size:2.5rem">📚 StudyFlow</div>'
        f'<div class="sf-hero-sub" style="text-align:center">'
        + ("הרשם או התחבר כדי להמשיך" if lang == "he" else "Sign up or log in to continue")
        + "</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs([
        "🔑 " + ("כניסה" if lang == "he" else "Log In"),
        "✨ " + ("הרשמה" if lang == "he" else "Sign Up"),
    ])

    # ── Login ─────────────────────────────────────────────────────
    with tab_login:
        with st.form("login_form"):
            uname = st.text_input(
                "שם משתמש" if lang == "he" else "Username",
                placeholder="הכנס שם משתמש" if lang == "he" else "Enter username",
            )
            pw = st.text_input(
                "סיסמה" if lang == "he" else "Password",
                type="password",
                placeholder="••••••",
            )
            submitted = st.form_submit_button(
                "🔑 " + ("התחבר" if lang == "he" else "Log In"),
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not uname or not pw:
                st.error("מלא את כל השדות" if lang == "he" else "Fill in all fields")
            else:
                ok, msg, user_data = login(uname, pw)
                if ok:
                    st.session_state.user = user_data
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # ── Sign Up ───────────────────────────────────────────────────
    with tab_signup:
        grades_he = ["כיתה ז׳", "כיתה ח׳", "כיתה ט׳", "כיתה י׳", "כיתה י״א", "כיתה י״ב", "אחר"]
        grades_en = ["Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Other"]
        grades    = grades_he if lang == "he" else grades_en

        with st.form("signup_form"):
            new_user  = st.text_input(
                "שם משתמש" if lang == "he" else "Username",
                placeholder="לפחות 2 תווים" if lang == "he" else "At least 2 characters",
                key="su_username",
            )
            new_email = st.text_input(
                "אימייל" if lang == "he" else "Email",
                placeholder="student@example.com",
                key="su_email",
            )
            new_grade = st.selectbox(
                "כיתה" if lang == "he" else "Grade",
                grades,
                key="su_grade",
            )
            new_pw   = st.text_input(
                "סיסמה" if lang == "he" else "Password",
                type="password",
                placeholder="לפחות 6 תווים + ספרה" if lang == "he" else "At least 6 chars + digit",
                key="su_pw",
            )
            new_pw2  = st.text_input(
                "אימות סיסמה" if lang == "he" else "Confirm password",
                type="password",
                placeholder="••••••",
                key="su_pw2",
            )
            agreed = st.checkbox(
                "אני מאשר את תנאי השימוש" if lang == "he" else "I agree to the terms of service",
                key="su_agree",
            )
            submitted2 = st.form_submit_button(
                "✨ " + ("הרשמה" if lang == "he" else "Sign Up"),
                type="primary",
                use_container_width=True,
            )

        if submitted2:
            if not agreed:
                st.error("יש לאשר את תנאי השימוש" if lang == "he" else "Please agree to the terms")
            elif new_pw != new_pw2:
                st.error("הסיסמאות אינן תואמות" if lang == "he" else "Passwords do not match")
            elif not new_user or not new_email or not new_pw:
                st.error("מלא את כל השדות" if lang == "he" else "Fill in all fields")
            else:
                ok, msg = signup(new_user, new_email, new_pw, new_grade)
                if ok:
                    # auto-login after signup
                    _, _, user_data = login(new_user, new_pw)
                    st.session_state.user = user_data
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)
    return False