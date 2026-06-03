"""
Main.py — Gradeup entry point
הרץ עם: streamlit run Main.py
"""
import streamlit as st

st.set_page_config(
    page_title="Gradeup | לומדים חכם, עולים קדימה",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from lang import init_lang, t
init_lang()

from auth import auth_wall, is_logged_in, get_current_user, logout

# Language toggle לפני login
with st.sidebar:
    if st.button(f"🌐 {t('lang_toggle')}", key="lang_btn_pre"):
        st.session_state.lang = "en" if st.session_state.lang == "he" else "he"
        st.rerun()

if not auth_wall(t):
    st.stop()

user = get_current_user()

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sf-logo">🎓 Gradeup</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sf-logo-sub">{t("tagline")}</div>', unsafe_allow_html=True)

    # User card
    plan_color = "#6ee7b7" if user.get("plan") == "free" else "#f472b6"
    st.markdown(
        f'<div class="sf-card" style="padding:.9rem;margin-bottom:.5rem">'
        f'<div style="font-weight:700">👤 {user.get("username","")}</div>'
        f'<div style="color:var(--muted);font-size:.8rem">{user.get("email","")}</div>'
        f'<div style="font-size:.75rem;margin-top:.4rem">'
        f'<span style="color:{plan_color};font-weight:700">'
        f'{"⭐ Pro" if user.get("plan")=="pro" else "🆓 Free"}</span>'
        f' · {user.get("grade","")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.button(f"🌐 {t('lang_toggle')}", use_container_width=True, key="lang_btn"):
        st.session_state.lang = "en" if st.session_state.lang == "he" else "he"
        st.rerun()

    st.markdown("---")

    NAV = [
        ("nav_home",     "home"),
        ("nav_schedule", "schedule"),
        ("nav_homework", "homework"),
        ("nav_earn",     "earn"),
        ("nav_grades",   "grades"),
        ("nav_wellness", "wellness"),
    ]
    if "page" not in st.session_state:
        st.session_state.page = "home"

    for key, page_id in NAV:
        active = st.session_state.page == page_id
        if st.button(
            t(key),
            use_container_width=True,
            type="primary" if active else "secondary",
            key=f"nav_{page_id}",
        ):
            st.session_state.page = page_id
            st.rerun()

    st.markdown("---")

    from ai_utils import api_key_widget
    api_key_widget(t)

    st.markdown("---")

    if st.button("🚪 " + ("התנתק" if st.session_state.lang == "he" else "Log Out"),
                 use_container_width=True):
        logout()
        st.rerun()

    st.markdown(
        '<div style="text-align:center;color:#1e2a3d;font-size:.72rem;margin-top:1rem">'
        'Gradeup v1.0 © 2025 | gradeup.co.il</div>',
        unsafe_allow_html=True,
    )

# ── Page routing ───────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    from pages.home import render
elif page == "schedule":
    from pages.schedule import render
elif page == "homework":
    from pages.homework import render
elif page == "earn":
    from pages.earn import render
elif page == "grades":
    from pages.grades import render
elif page == "wellness":
    from pages.wellness import render
else:
    from pages.home import render

render(t)