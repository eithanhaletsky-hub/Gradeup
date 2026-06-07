"""pages/scholarships.py — מלגות וקורסים חינמיים + DuckDuckGo + AI דירוג"""
import streamlit as st
from ai_utils import call_gemini, get_api_key, ddg_search

FIELDS_HE = ["מתמטיקה","מדעים","תכנות","עיצוב","מוזיקה","ספורט",
             "כלכלה","רפואה","חינוך","אמנות","שפות","סביבה","אחר"]
FIELDS_EN = ["Math","Sciences","Coding","Design","Music","Sports",
             "Economics","Medicine","Education","Arts","Languages","Environment","Other"]


def render():
    lang = st.session_state.lang
    he   = lang == "he"
    st.markdown(
        '<div class="section-title">🏆 ' +
        ("מלגות וקורסים חינמיים" if he else "Scholarships & Free Courses") +
        '</div>',
        unsafe_allow_html=True,
    )

    if "sch_results" not in st.session_state: st.session_state.sch_results = []
    if "sch_saved"   not in st.session_state: st.session_state.sch_saved   = []
    if "sch_ai_rank" not in st.session_state: st.session_state.sch_ai_rank = None

    tab_search, tab_saved = st.tabs([
        "🔍 " + ("חיפוש" if he else "Search"),
        "⭐ " + ("שמורים" if he else "Saved"),
    ])

    with tab_search: _search(he)
    with tab_saved:  _saved(he)


# ── Search tab ────────────────────────────────────────────────────────────
def _search(he):
    fields = FIELDS_HE if he else FIELDS_EN

    st.markdown(
        f'<div class="card card-b" style="margin-bottom:1rem">'
        f'<span style="color:var(--muted);font-size:.86rem">'
        + ("DuckDuckGo מחפש מלגות וקורסים חינמיים עדכניים בישראל ובעולם. "
           "AI מדרג את התוצאות לפי ההתאמה האישית שלך."
           if he else
           "DuckDuckGo searches for current scholarships and free courses in Israel and worldwide. "
           "AI ranks results by your personal fit.")
        + "</span></div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        field = st.selectbox(
            "תחום עניין" if he else "Field of interest",
            fields, key="sch_field"
        )
    with c2:
        age = st.slider("גיל" if he else "Age", 14, 23, 16, key="sch_age")
    with c3:
        stype_opts = (
            ["הכל", "מלגה", "קורס חינמי"]
            if he else
            ["All", "Scholarship", "Free course"]
        )
        stype = st.selectbox("סוג" if he else "Type", stype_opts, key="sch_type")

    col_s, col_ai = st.columns(2)
    with col_s:
        search_btn = st.button(
            "🔍 " + ("חפש" if he else "Search"),
            type="primary", use_container_width=True, key="sch_search"
        )
    with col_ai:
        ai_btn = st.button(
            "🤖 " + ("דרג עם AI" if he else "Rank with AI"),
            use_container_width=True, key="sch_ai",
            disabled=not st.session_state.sch_results,
        )

    # Run DuckDuckGo search
    if search_btn:
        type_he = {"הכל":"מלגות וקורסים חינמיים","מלגה":"מלגות","קורס חינמי":"קורסים חינמיים"}
        type_en = {"All":"scholarships and free courses","Scholarship":"scholarships","Free course":"free online courses"}
        type_str = type_he.get(stype,"מלגות") if he else type_en.get(stype,"scholarships")
        q = (
            f"{type_str} בתחום {field} לבני {age} ישראל 2025"
            if he else
            f"{type_str} {field} students age {age} Israel 2025"
        )
        with st.spinner("🔍 DuckDuckGo…"):
            results = ddg_search(q, max_results=7)
            st.session_state.sch_results = results
            st.session_state.sch_ai_rank = None
        st.rerun()

    # AI ranking
    if ai_btn and st.session_state.sch_results:
        if not get_api_key():
            st.warning("Gemini API Key required")
        else:
            results_text = "\n".join(
                f"{i+1}. {r.get('title','')} — {r.get('body','')[:120]}"
                for i, r in enumerate(st.session_state.sch_results)
            )
            sys = (
                f"אתה יועץ לתלמיד תיכון בגיל {age} בתחום {field}. "
                "קיבלת תוצאות חיפוש. דרג את 3 הרלוונטיות ביותר ולמה. עברית, קצר."
                if he else
                f"You advise a {age}-year-old student interested in {field}. "
                "You got search results. Rank the 3 most relevant and explain why. English, brief."
            )
            with st.spinner("🤖…"):
                try:
                    st.session_state.sch_ai_rank = call_gemini(
                        system_prompt=sys,
                        user_text=results_text,
                        max_tokens=500, temperature=0.6,
                    )
                except Exception as e:
                    st.error(str(e))

    # Show AI ranking
    if st.session_state.sch_ai_rank:
        st.markdown(
            f'<div class="bubble-ai" style="margin-bottom:1rem">'
            f'<div class="bubble-label">🤖 Gradeup AI — '
            + ("דירוג מומלץ" if he else "Recommended ranking")
            + f'</div>{st.session_state.sch_ai_rank}</div>',
            unsafe_allow_html=True,
        )

    # Results list
    results = st.session_state.sch_results
    if not results:
        return

    st.markdown(
        f'<div class="section-title">'
        + (f"{len(results)} תוצאות" if he else f"{len(results)} results")
        + "</div>",
        unsafe_allow_html=True,
    )
    for i, r in enumerate(results):
        title = r.get("title", "")
        body  = r.get("body",  "")
        href  = r.get("href",  "")
        c1, c2 = st.columns([5, .7])
        with c1:
            link_html = (
                f'<a href="{href}" target="_blank" style="color:var(--b);font-size:.8rem">🔗 {href[:55]}…</a>'
                if href else ""
            )
            st.markdown(
                f'<div class="card" style="padding:.95rem;margin-bottom:.4rem">'
                f'<b>{title}</b><br>'
                f'<span style="color:var(--muted);font-size:.84rem">{body[:230]}…</span><br>'
                f'{link_html}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            if st.button("⭐ " + ("שמור" if he else "Save"), key=f"sch_sv_{i}"):
                if r not in st.session_state.sch_saved:
                    st.session_state.sch_saved.append(r)
                    st.success("✅")


# ── Saved tab ─────────────────────────────────────────────────────────────
def _saved(he):
    saved = st.session_state.sch_saved
    if not saved:
        st.info("אין פריטים שמורים עדיין" if he else "No saved items yet")
        return

    st.markdown(
        f'<div class="section-title">'
        + (f"{len(saved)} שמורים" if he else f"{len(saved)} saved")
        + "</div>",
        unsafe_allow_html=True,
    )
    for i, r in enumerate(saved):
        c1, c2 = st.columns([5, .5])
        with c1:
            href = r.get("href","")
            link_html = (
                f'<a href="{href}" target="_blank" style="color:var(--b);font-size:.8rem">🔗 {href[:55]}…</a>'
                if href else ""
            )
            st.markdown(
                f'<div class="card card-g" style="padding:.95rem;margin-bottom:.4rem">'
                f'<b>{r.get("title","")}</b><br>'
                f'<span style="color:var(--muted);font-size:.84rem">{r.get("body","")[:200]}…</span><br>'
                f'{link_html}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            if st.button("🗑️", key=f"sch_del_{i}"):
                st.session_state.sch_saved.pop(i)
                st.rerun()