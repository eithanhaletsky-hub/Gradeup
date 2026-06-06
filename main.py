
with open("/home/claude/studyflow/Main.py") as f:
    content = f.read()

# Update NAV
old_nav = '''    NAV = [
        ("nav_home",        "home"),
        ("nav_schedule",    "schedule"),
        ("nav_homework",    "homework"),
        ("nav_earn",        "earn"),
        ("nav_grades",      "grades"),
        ("nav_wellness",    "wellness"),
        ("nav_flashcards",  "flashcards"),
        ("nav_summarizer",  "summarizer"),
        ("nav_qa",          "qa"),
        ("nav_goals",       "goals"),
    ]'''

new_nav = '''    # ── Navigation groups ─────────────────────────────────────────
    NAV_GROUPS = {
        ("📚 " + ("לימודים" if st.session_state.lang=="he" else "Study")): [
            ("nav_schedule",    "schedule"),
            ("nav_homework",    "homework"),
            ("nav_flashcards",  "flashcards"),
            ("nav_summarizer",  "summarizer"),
            ("nav_science",     "science"),
            ("nav_translator",  "translator"),
        ],
        ("📊 " + ("מעקב" if st.session_state.lang=="he" else "Track")): [
            ("nav_grades",      "grades"),
            ("nav_bagrut",      "bagrut"),
            ("nav_goals",       "goals"),
        ],
        ("💼 " + ("קריירה וכסף" if st.session_state.lang=="he" else "Career & Money")): [
            ("nav_earn",        "earn"),
            ("nav_budget",      "budget"),
            ("nav_scholarships","scholarships"),
            ("nav_projects",    "projects"),
        ],
        ("💆 " + ("רווחה" if st.session_state.lang=="he" else "Wellness")): [
            ("nav_wellness",    "wellness"),
            ("nav_qa",          "qa"),
        ],
    }'''

content = content.replace(old_nav, new_nav)

# Update the nav rendering loop
old_loop = '''    for key, page_id in NAV:
        active = st.session_state.page == page_id
        if st.button(
            t(key),
            use_container_width=True,
            type="primary" if active else "secondary",
            key=f"nav_{page_id}",
        ):
            st.session_state.page = page_id
            st.rerun()'''

new_loop = '''    if "page" not in st.session_state:
        st.session_state.page = "home"

    for group_label, pages in NAV_GROUPS.items():
        st.markdown(
            f\'<div style="font-size:.72rem;color:var(--muted);font-weight:700;\'
            f\'text-transform:uppercase;letter-spacing:.06em;margin:.6rem 0 .3rem">\' 
            f\'{group_label}</div>\',
            unsafe_allow_html=True,
        )
        for key, page_id in pages:
            active = st.session_state.page == page_id
            if st.button(
                t(key),
                use_container_width=True,
                type="primary" if active else "secondary",
                key=f"nav_{page_id}",
            ):
                st.session_state.page = page_id
                st.rerun()'''

content = content.replace(old_loop, new_loop)

# Remove old "if page not in" line since it's now in the loop
content = content.replace(
    '    if "page" not in st.session_state:\n        st.session_state.page = "home"\n\n    for group_label',
    '    for group_label'
)

# Update routing
old_route = '''elif page == "goals":
    from pages.goals import render
else:
    from pages.home import render'''

new_route = '''elif page == "goals":
    from pages.goals import render
elif page == "bagrut":
    from pages.bagrut import render
elif page == "budget":
    from pages.budget import render
elif page == "scholarships":
    from pages.scholarships import render
elif page == "projects":
    from pages.projects import render
elif page == "translator":
    from pages.translator import render
elif page == "science":
    from pages.science_calc import render
else:
    from pages.home import render'''

content = content.replace(old_route, new_route)

with open("/home/claude/studyflow/Main.py", "w") as f:
    f.write(content)

import ast; ast.parse(content)
print("✅ Main.py updated")
