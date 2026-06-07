"""pages/projects.py — מחולל פרויקטים + DuckDuckGo + fpdf2"""
import streamlit as st
from datetime import datetime
from fpdf import FPDF
from ai_utils import call_gemini, get_api_key, ddg_search

INTERESTS_HE = ["מדעים","תכנות","עיצוב","מוזיקה","כלכלה","ספורט",
                "חברה","סביבה","בריאות","אמנות","היסטוריה","שפות"]
INTERESTS_EN = ["Sciences","Coding","Design","Music","Economics","Sports",
                "Society","Environment","Health","Arts","History","Languages"]

SUBJECTS_HE = ["מתמטיקה","פיזיקה","כימיה","ביולוגיה","אנגלית","מדעי המחשב","גיאוגרפיה","אחר"]
SUBJECTS_EN = ["Math","Physics","Chemistry","Biology","English","CS","Geography","Other"]

DURATION_HE = ["שבוע אחד","חודש","סמסטר","שנה שלמה"]
DURATION_EN = ["One week","One month","Semester","Full year"]

LEVEL_HE = ["קל — מתחיל","בינוני — יש ניסיון","מאתגר — מתקדם"]
LEVEL_EN = ["Easy — beginner","Medium — some experience","Hard — advanced"]


def _make_pdf(content: str, title: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica","B",18)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,12,"Gradeup — Project Plan",ln=True,align="C")
    pdf.set_font("Helvetica","",10)
    pdf.set_text_color(150,160,180)
    pdf.cell(0,7,f"{title}  |  {datetime.now().strftime('%d/%m/%Y')}",ln=True,align="C")
    pdf.ln(5)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica","",11)
    pdf.set_text_color(232,237,245)
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(4); continue
        if line.startswith("**") or line.startswith("##"):
            pdf.set_font("Helvetica","B",12)
            pdf.set_text_color(110,231,183)
            pdf.multi_cell(0,7,line.lstrip("#* "))
            pdf.set_font("Helvetica","",11)
            pdf.set_text_color(232,237,245)
        elif line.startswith("- ") or line.startswith("• "):
            pdf.multi_cell(0,6,"  " + line)
        else:
            pdf.multi_cell(0,6,line)
    pdf.set_font("Helvetica","I",8)
    pdf.set_text_color(40,60,80)
    pdf.cell(0,8,"gradeup.co.il",ln=True,align="C")
    return bytes(pdf.output())


def render():
    lang = st.session_state.lang
    he   = lang == "he"
    st.markdown(
        '<div class="section-title">💡 ' +
        ("מחולל פרויקטים" if he else "Project Generator") +
        '</div>',
        unsafe_allow_html=True,
    )

    if "proj_result" not in st.session_state: st.session_state.proj_result = None
    if "proj_saved"  not in st.session_state: st.session_state.proj_saved  = []

    tab_gen, tab_saved = st.tabs([
        "✨ " + ("צור רעיון" if he else "Generate idea"),
        "📁 " + ("שמורים"   if he else "Saved"),
    ])

    with tab_gen:   _generate(he)
    with tab_saved: _saved(he)


# ── Generate ──────────────────────────────────────────────────────────────
def _generate(he):
    interests_opts = INTERESTS_HE if he else INTERESTS_EN
    subjects_opts  = SUBJECTS_HE  if he else SUBJECTS_EN
    duration_opts  = DURATION_HE  if he else DURATION_EN
    level_opts     = LEVEL_HE     if he else LEVEL_EN

    st.markdown(
        f'<div class="card card-o" style="margin-bottom:1rem">'
        f'<span style="color:var(--muted);font-size:.86rem">'
        + ("מלא את הפרטים שלך — AI + DuckDuckGo יצרו 3 רעיונות לפרויקט עם תוכנית עבודה מלאה."
           if he else
           "Fill in your details — AI + DuckDuckGo will generate 3 project ideas with a full work plan.")
        + "</span></div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        interests = st.multiselect(
            "תחומי עניין" if he else "Interests",
            interests_opts, default=interests_opts[:2], key="proj_int"
        )
    with c2:
        subjects = st.multiselect(
            "מקצועות חזקים" if he else "Strong subjects",
            subjects_opts, default=subjects_opts[:2], key="proj_sub"
        )

    c3, c4 = st.columns(2)
    with c3:
        duration = st.selectbox("משך הפרויקט" if he else "Duration", duration_opts, index=1, key="proj_dur")
    with c4:
        level = st.selectbox("רמת קושי" if he else "Difficulty", level_opts, index=1, key="proj_lvl")

    extra = st.text_input(
        "מידע נוסף (אופציונלי)" if he else "Additional info (optional)",
        placeholder="יש לי גישה למעבדה / פרויקט קבוצתי…" if he else "I have lab access / team project…",
        key="proj_extra"
    )

    use_ddg = st.toggle(
        "🔍 " + ("הוסף דוגמאות מהאינטרנט (DuckDuckGo)" if he else "Add real-world examples (DuckDuckGo)"),
        value=True, key="proj_ddg"
    )

    if not get_api_key():
        st.warning("Gemini API Key required"); return

    if st.button(
        "✨ " + ("צור 3 רעיונות לפרויקט" if he else "Generate 3 Project Ideas"),
        type="primary", use_container_width=True, key="proj_gen"
    ):
        if not interests:
            st.error("בחר לפחות תחום עניין אחד" if he else "Select at least one interest")
            return

        ddg_ctx = ""
        if use_ddg:
            q = (
                f"דוגמאות פרויקטים בתחום {', '.join(interests)} לתלמידי תיכון"
                if he else
                f"creative high school project ideas {', '.join(interests)}"
            )
            with st.spinner("🔍 DuckDuckGo…"):
                ddg_results = ddg_search(q, max_results=4)
            if ddg_results:
                ddg_ctx = "\n".join(
                    f"- {r.get('title','')} — {r.get('body','')[:100]}"
                    for r in ddg_results
                )

        sys = (
            "אתה יועץ פרויקטים לתלמידי תיכון. "
            "צור בדיוק 3 רעיונות לפרויקט. לכל רעיון: "
            "1) שם, 2) תיאור קצר (2 משפטים), 3) שלבי ביצוע (4-5 נקודות), "
            "4) כלים נדרשים, 5) מה תלמד. "
            "הפרד בין רעיונות ב-'---'. ענה בעברית."
            if he else
            "You are a project advisor for high school students. "
            "Create exactly 3 project ideas. For each: "
            "1) Name, 2) Short description (2 sentences), "
            "3) Steps (4-5 bullets), 4) Tools needed, 5) What you will learn. "
            "Separate ideas with '---'. Reply in English."
        )
        user_text = (
            f"תחומי עניין: {', '.join(interests)}\n"
            f"מקצועות חזקים: {', '.join(subjects)}\n"
            f"משך: {duration} | רמה: {level}\n"
            f"מידע נוסף: {extra or 'אין'}"
            + (f"\n\nדוגמאות מהאינטרנט:\n{ddg_ctx}" if ddg_ctx else "")
            if he else
            f"Interests: {', '.join(interests)}\n"
            f"Strong subjects: {', '.join(subjects)}\n"
            f"Duration: {duration} | Level: {level}\n"
            f"Extra info: {extra or 'None'}"
            + (f"\n\nReal-world examples:\n{ddg_ctx}" if ddg_ctx else "")
        )

        with st.spinner("✨ " + ("מחולל רעיונות…" if he else "Generating ideas…")):
            try:
                result = call_gemini(
                    system_prompt=sys, user_text=user_text,
                    max_tokens=2000, temperature=0.8,
                )
                st.session_state.proj_result = result
            except Exception as e:
                st.error(str(e))

    # Display results
    if not st.session_state.proj_result:
        return

    projects = [p.strip() for p in st.session_state.proj_result.split("---") if p.strip()]
    for i, proj in enumerate(projects):
        first_line = proj.split("\n")[0].strip().lstrip("#* ")
        with st.expander(f"💡 {first_line or f'Project {i+1}'}", expanded=(i==0)):
            st.markdown(
                f'<div style="color:#e8edf5;font-size:.9rem;line-height:1.75">'
                f'{proj.replace(chr(10),"<br>")}</div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 " + ("שמור" if he else "Save"), key=f"psv_{i}", use_container_width=True):
                    st.session_state.proj_saved.append({
                        "title": first_line,
                        "content": proj,
                        "date": datetime.now().strftime("%d/%m/%Y"),
                    })
                    st.success("✅")
            with c2:
                if st.button("📥 PDF", key=f"ppdf_{i}", use_container_width=True):
                    pdf_b = _make_pdf(proj, first_line)
                    st.download_button(
                        "⬇️ Download", pdf_b,
                        f"gradeup_project_{i+1}.pdf", "application/pdf",
                        key=f"ppdl_{i}"
                    )


# ── Saved ─────────────────────────────────────────────────────────────────
def _saved(he):
    saved = st.session_state.proj_saved
    if not saved:
        st.info("אין פרויקטים שמורים עדיין" if he else "No saved projects yet")
        return

    st.markdown(
        f'<div class="section-title">'
        + (f"{len(saved)} פרויקטים שמורים" if he else f"{len(saved)} saved projects")
        + "</div>",
        unsafe_allow_html=True,
    )
    for i, proj in enumerate(saved):
        c1, c2 = st.columns([5.5, .5])
        with c1:
            with st.expander(f"📁 {proj['title']}  ·  {proj['date']}"):
                st.markdown(
                    f'<div style="color:#e8edf5;font-size:.88rem;line-height:1.7">'
                    f'{proj["content"].replace(chr(10),"<br>")}</div>',
                    unsafe_allow_html=True,
                )
                if st.button("📥 PDF", key=f"spdf_{i}"):
                    pdf_b = _make_pdf(proj["content"], proj["title"])
                    st.download_button(
                        "⬇️ Download", pdf_b,
                        f"gradeup_{proj['title'][:20]}.pdf", "application/pdf",
                        key=f"spdl_{i}"
                    )
        with c2:
            if st.button("🗑️", key=f"sdel_{i}"):
                st.session_state.proj_saved.pop(i); st.rerun()