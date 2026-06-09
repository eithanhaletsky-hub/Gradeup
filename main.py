"""Main.py — Gradeup entry point | streamlit run Main.py"""
import os, streamlit as st
from translations import t

st.set_page_config(
    page_title="Gradeup | לומדים חכם",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────
_css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
with open(_css) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session defaults ──────────────────────────────────────────────────────
if "lang" not in st.session_state: st.session_state.lang = "he"
if "page" not in st.session_state: st.session_state.page = "home"

lang = st.session_state.lang

# ── Auth wall ─────────────────────────────────────────────────────────────
from auth import auth_wall, is_logged_in, get_user, logout

with st.sidebar:
    if st.button("🌐 " + ("English" if lang=="he" else "עברית"), key="lang_pre"):
        st.session_state.lang = "en" if lang=="he" else "he"
        st.rerun()

if not auth_wall(lang):
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────
user = get_user()
lang = st.session_state.lang   # refresh after potential rerun

with st.sidebar:
    st.markdown('<div class="logo">🎓 Gradeup</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="logo-sub">{"לומדים חכם, עולים קדימה" if lang=="he" else "Study smart, level up"}</div>',
        unsafe_allow_html=True,
    )

    plan_col = "#6ee7b7" if user.get("plan")=="free" else "#f472b6"
    st.markdown(
        f'<div class="card" style="padding:.8rem;margin-bottom:.6rem">'
        f'<div style="font-weight:700">👤 {user.get("username","")}</div>'
        f'<div style="color:var(--muted);font-size:.78rem">{user.get("email","")}</div>'
        f'<div style="font-size:.73rem;margin-top:.3rem;color:{plan_col};font-weight:700">'
        f'{"🆓 Free" if user.get("plan")=="free" else "⭐ Pro"}'
        f' · {user.get("grade","")}</div></div>',
        unsafe_allow_html=True,
    )

    if st.button("🌐 " + ("English" if lang=="he" else "עברית"), key="lang_btn", use_container_width=True):
        st.session_state.lang = "en" if lang=="he" else "he"
        st.rerun()

    st.markdown("---")

    # Grouped navigation
    NAV = [
        ("🏠", "home",         "ראשי",             "Home",            None),
        # Study
        ("🗓️","schedule",      "מערכת שעות",       "Schedule",        "study"),
        ("📚","homework",      "עוזר שיעורי בית",  "Homework Bot",    "study"),
        ("🃏","flashcards",    "כרטיסיות",          "Flashcards",      "study"),
        ("📝","summarizer",    "מסכם חומר",         "Summarizer",      "study"),
        ("🔬","science",       "מחשבון מדעי",      "Science Calc",    "study"),
        ("🌍","translator",    "מתרגם חכם",         "Translator",      "study"),
        # Track
        ("📊","grades",        "מעקב ציונים",      "Grade Tracker",   "track"),
        ("🎓","bagrut",        "מחשבון בגרות",     "Bagrut Calc",     "track"),
        ("🎯","goals",         "מעקב יעדים",       "Goals",           "track"),
        # Career & Money
        ("💰","budget",        "תקציב חודשי",      "Budget",          "career"),
        ("🏆","scholarships",  "מלגות וקורסים",    "Scholarships",    "career"),
        ("💡","projects",      "מחולל פרויקטים",   "Projects",        "career"),
        # Wellness
        ("👥","qa",            "לוח שאלות",         "Q&A Board",       "wellness"),
    ]

    GROUPS = {
        "study":   ("📚 לימודים"      if lang=="he" else "📚 Study"),
        "track":   ("📊 מעקב"         if lang=="he" else "📊 Track"),
        "career":  ("💼 קריירה וכסף"  if lang=="he" else "💼 Career & Money"),
        "wellness":("💆 רווחה"        if lang=="he" else "💆 Wellness"),
    }

    current_group = None
    for icon, pid, lbl_he, lbl_en, group in NAV:
        lbl = lbl_he if lang=="he" else lbl_en

        if group and group != current_group:
            current_group = group
            st.markdown(f'<div class="nav-group-label">{GROUPS[group]}</div>', unsafe_allow_html=True)

        active = st.session_state.page == pid
        if st.button(
            f"{icon} {lbl}",
            use_container_width=True,
            type="primary" if active else "secondary",
            key=f"nav_{pid}",
        ):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")

    from ai_utils import api_key_widget
    api_key_widget()

    st.markdown("---")
    if st.button("🚪 " + ("התנתק" if lang=="he" else "Log Out"), use_container_width=True):
        logout(); st.rerun()

    st.markdown(
        '<div style="text-align:center;color:#1a2535;font-size:.68rem;margin-top:.8rem">'
        'Gradeup v1.0 © 2025 | gradeup.co.il</div>',
        unsafe_allow_html=True,
    )

# ── Page routing ──────────────────────────────────────────────────────────
page = st.session_state.page

if   page == "home":         from pages.home          import render
elif page == "schedule":     from pages.schedule      import render
elif page == "homework":     from pages.homework      import render
elif page == "flashcards":   from pages.flashcards    import render
elif page == "summarizer":   from pages.summarizer    import render
elif page == "science":      from pages.science_calc  import render
elif page == "translator":   from pages.translator    import render
elif page == "grades":       from pages.grades        import render
elif page == "bagrut":       from pages.bagrut        import render
elif page == "goals":        from pages.goals         import render
elif page == "budget":       from pages.budget        import render
elif page == "scholarships": from pages.scholarships  import render
elif page == "projects":     from pages.projects      import render
elif page == "qa":           from pages.qa_board      import render
else:                        from pages.home          import render

render(t)