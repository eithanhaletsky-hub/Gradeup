"""auth.py — הרשמה/כניסה עם bcrypt + JSON"""
import json, os, re, bcrypt, streamlit as st
from datetime import datetime


_BASE = os.path.dirname(os.path.abspath(__file__))

def _users_file() -> str:
    try:
        test = os.path.join(_BASE, ".write_test")
        open(test,"w").close(); os.remove(test)
        return os.path.join(_BASE, "users.json")
    except OSError:
        return "/tmp/gradeup_users.json"

def _load() -> dict:
    p = _users_file()
    if not os.path.exists(p): return {}
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except: return {}

def _save(users: dict):
    with open(_users_file(), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def _verify(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())

def _valid_email(e: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", e.strip()))

def _valid_pw(pw: str) -> tuple[bool, str]:
    if len(pw) < 6: return False, "סיסמה חייבת להכיל לפחות 6 תווים"
    if not re.search(r"\d", pw): return False, "סיסמה חייבת להכיל ספרה אחת לפחות"
    return True, ""

def signup(username: str, email: str, password: str, grade: str) -> tuple[bool, str]:
    username = username.strip(); email = email.strip().lower()
    if len(username) < 2: return False, "שם משתמש חייב להכיל לפחות 2 תווים"
    if not _valid_email(email): return False, "אימייל לא תקין"
    ok, err = _valid_pw(password)
    if not ok: return False, err
    users = _load()
    if username in users: return False, "שם המשתמש תפוס"
    if any(u["email"]==email for u in users.values()): return False, "האימייל כבר רשום"
    users[username] = {"email":email,"password":_hash(password),"grade":grade,"plan":"free","created_at":datetime.now().isoformat()}
    _save(users)
    return True, f"ברוך הבא, {username}! 🎉"

def login(username: str, password: str) -> tuple[bool, str, dict]:
    users = _load()
    if username not in users: return False, "שם משתמש או סיסמה שגויים", {}
    if not _verify(password, users[username]["password"]): return False, "שם משתמש או סיסמה שגויים", {}
    data = {k:v for k,v in users[username].items() if k!="password"}
    data["username"] = username
    return True, f"שלום, {username}! 👋", data

def logout():
    st.session_state.user = None
    st.session_state.page = "home"

def is_logged_in() -> bool:
    return bool(st.session_state.get("user"))

def get_user() -> dict:
    return st.session_state.get("user", {})

def auth_wall(lang: str) -> bool:
    if is_logged_in(): return True
    st.markdown('<div style="max-width:420px;margin:2rem auto">', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-family:Space Grotesk,sans-serif;font-size:2.5rem;'
        'font-weight:700;background:linear-gradient(135deg,#6ee7b7,#38bdf8,#f472b6);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent">🎓 Gradeup</div>'
        f'<div style="text-align:center;color:#5a6a82;margin:.5rem 0 1.5rem">'
        + ("הרשם או התחבר כדי להמשיך" if lang=="he" else "Sign up or log in to continue")
        + "</div>",
        unsafe_allow_html=True,
    )

    tab_in, tab_up = st.tabs([
        "🔑 " + ("כניסה" if lang=="he" else "Log In"),
        "✨ " + ("הרשמה" if lang=="he" else "Sign Up"),
    ])

    with tab_in:
        with st.form("login_form"):
            u = st.text_input("שם משתמש" if lang=="he" else "Username", key="li_u")
            p = st.text_input("סיסמה"    if lang=="he" else "Password", type="password", key="li_p")
            if st.form_submit_button("🔑 " + ("כניסה" if lang=="he" else "Log In"), type="primary", use_container_width=True):
                if u and p:
                    ok, msg, data = login(u, p)
                    if ok: st.session_state.user = data; st.rerun()
                    else:  st.error(msg)

    with tab_up:
        grades = ["כיתה ז׳","כיתה ח׳","כיתה ט׳","כיתה י׳","כיתה י״א","כיתה י״ב"] if lang=="he" else ["Grade 7","Grade 8","Grade 9","Grade 10","Grade 11","Grade 12"]
        with st.form("signup_form"):
            u2 = st.text_input("שם משתמש" if lang=="he" else "Username", key="su_u")
            e2 = st.text_input("אימייל"   if lang=="he" else "Email",    key="su_e")
            g2 = st.selectbox("כיתה"      if lang=="he" else "Grade", grades, key="su_g")
            p2 = st.text_input("סיסמה"    if lang=="he" else "Password", type="password", key="su_p")
            p3 = st.text_input("אימות סיסמה" if lang=="he" else "Confirm", type="password", key="su_p2")
            ag = st.checkbox("אני מאשר את תנאי השימוש" if lang=="he" else "I agree to the terms", key="su_ag")
            if st.form_submit_button("✨ " + ("הרשמה" if lang=="he" else "Sign Up"), type="primary", use_container_width=True):
                if not ag: st.error("יש לאשר תנאי שימוש")
                elif p2!=p3: st.error("הסיסמאות לא תואמות")
                elif u2 and e2 and p2:
                    ok, msg = signup(u2, e2, p2, g2)
                    if ok:
                        _, _, data = login(u2, p2)
                        st.session_state.user = data; st.rerun()
                    else: st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)
    return False