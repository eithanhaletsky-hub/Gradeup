"""pages/bagrut.py — מחשבון בגרות משוקלל + סימולציה"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

SUBJECTS_HE = [
    "מתמטיקה","אנגלית","עברית","ספרות","היסטוריה","אזרחות",
    "פיזיקה","כימיה","ביולוגיה","מדעי המחשב","גיאוגרפיה","תנ\"ך","אחר"
]
SUBJECTS_EN = [
    "Math","English","Hebrew","Literature","History","Civics",
    "Physics","Chemistry","Biology","CS","Geography","Bible","Other"
]

def _weighted_avg(subjects: list) -> float:
    total_units = sum(s["units"] for s in subjects)
    if total_units == 0:
        return 0.0
    total_score = sum(
        (s["school"] * 0.4 + s["bagrut"] * 0.6) * s["units"]
        for s in subjects
    )
    return total_score / total_units

def _grade_color(avg: float) -> str:
    if avg >= 90: return "#6ee7b7"
    if avg >= 75: return "#38bdf8"
    if avg >= 60: return "#facc15"
    return "#f87171"

def _make_pdf(subjects, avg, lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica","B",20)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,12,"Gradeup — Bagrut Report",ln=True,align="C")
    pdf.set_font("Helvetica","",10)
    pdf.set_text_color(150,160,180)
    pdf.cell(0,7,datetime.now().strftime("%d/%m/%Y"),ln=True,align="C")
    pdf.ln(6)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(6)
    for s in subjects:
        combined = s["school"]*0.4 + s["bagrut"]*0.6
        pdf.set_font("Helvetica","B",11)
        pdf.set_text_color(232,237,245)
        pdf.cell(90,8,s["name"],ln=False)
        pdf.set_font("Helvetica","",11)
        col = (110,231,183) if combined>=90 else (56,189,248) if combined>=75 else (251,196,60)
        pdf.set_text_color(*col)
        pdf.cell(0,8,f"{combined:.1f}  ({s['units']} units)",ln=True)
    pdf.ln(4)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica","B",14)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,10,f"Average: {avg:.2f}",ln=True,align="C")
    pdf.set_font("Helvetica","I",9)
    pdf.set_text_color(40,60,80)
    pdf.cell(0,8,"gradeup.co.il",ln=True,align="C")
    return bytes(pdf.output())

def render(t):
    lang = st.session_state.lang
    st.markdown(f'<div class="sf-section-title">🎓 {t("bag_title")}</div>', unsafe_allow_html=True)

    if "bag_subjects" not in st.session_state:
        st.session_state.bag_subjects = [
            {"name":"מתמטיקה", "units":5, "school":82, "bagrut":78},
            {"name":"אנגלית",  "units":5, "school":90, "bagrut":88},
            {"name":"עברית",   "units":5, "school":76, "bagrut":74},
            {"name":"פיזיקה",  "units":5, "school":85, "bagrut":80},
            {"name":"היסטוריה","units":5, "school":79, "bagrut":77},
        ]

    tab_calc, tab_sim, tab_export = st.tabs([
        f"🧮 {t('bag_tab_calc')}",
        f"🎯 {t('bag_tab_sim')}",
        f"📥 {t('bag_tab_export')}",
    ])

    with tab_calc:
        _render_calc(t, lang)
    with tab_sim:
        _render_sim(t, lang)
    with tab_export:
        _render_export(t, lang)


def _render_calc(t, lang):
    subjects = SUBJECTS_HE if lang == "he" else SUBJECTS_EN

    # Add subject form
    with st.expander(f"➕ {t('bag_add_subject')}", expanded=False):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            name = st.selectbox(t("bag_subject"), subjects, key="bag_new_name")
        with c2:
            units = st.selectbox(t("bag_units"), [1,2,3,4,5], index=4, key="bag_new_units")
        with c3:
            school = st.number_input(t("bag_school_grade"), 0, 100, 80, key="bag_new_school")
        with c4:
            bagrut = st.number_input(t("bag_bagrut_grade"), 0, 100, 80, key="bag_new_bagrut")
        with c5:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"✅ {t('add')}", key="bag_add_btn", type="primary"):
                st.session_state.bag_subjects.append({
                    "name": name, "units": units,
                    "school": school, "bagrut": bagrut
                })
                st.rerun()

    subs = st.session_state.bag_subjects
    if not subs:
        st.info(t("bag_no_subjects"))
        return

    avg = _weighted_avg(subs)
    avg_color = _grade_color(avg)

    # Big average display
    st.markdown(
        f'<div class="sf-card" style="text-align:center;padding:2rem;border-color:{avg_color}44">'
        f'<div style="color:var(--muted);font-size:.9rem;margin-bottom:.3rem">{t("bag_avg")}</div>'
        f'<div style="font-size:4rem;font-weight:800;color:{avg_color};font-family:Space Grotesk,monospace">{avg:.2f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Subject table
    st.markdown("<br>", unsafe_allow_html=True)
    for i, s in enumerate(subs):
        combined = s["school"]*0.4 + s["bagrut"]*0.6
        col_c = _grade_color(combined)
        c1,c2,c3,c4,c5,c6 = st.columns([2.5, 1, 1.2, 1.2, 1.2, .5])
        with c1:
            new_name = st.text_input("", value=s["name"], key=f"bag_name_{i}", label_visibility="collapsed")
            st.session_state.bag_subjects[i]["name"] = new_name
        with c2:
            new_u = st.number_input("", 1, 5, s["units"], key=f"bag_u_{i}", label_visibility="collapsed")
            st.session_state.bag_subjects[i]["units"] = new_u
        with c3:
            new_sc = st.number_input("", 0, 100, s["school"], key=f"bag_sc_{i}", label_visibility="collapsed")
            st.session_state.bag_subjects[i]["school"] = new_sc
        with c4:
            new_bg = st.number_input("", 0, 100, s["bagrut"], key=f"bag_bg_{i}", label_visibility="collapsed")
            st.session_state.bag_subjects[i]["bagrut"] = new_bg
        with c5:
            st.markdown(
                f'<div style="text-align:center;padding:.4rem;color:{col_c};font-weight:700;font-size:1.05rem">'
                f'{combined:.1f}</div>',
                unsafe_allow_html=True,
            )
        with c6:
            if st.button("🗑️", key=f"bag_del_{i}"):
                st.session_state.bag_subjects.pop(i)
                st.rerun()

    # Plotly bar chart
    names   = [s["name"] for s in subs]
    schools = [s["school"] for s in subs]
    bagruts = [s["bagrut"] for s in subs]
    combined_scores = [s["school"]*0.4+s["bagrut"]*0.6 for s in subs]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="בית ספר" if lang=="he" else "School",
                         x=names, y=schools, marker_color="#38bdf8", opacity=0.7))
    fig.add_trace(go.Bar(name="בגרות" if lang=="he" else "Bagrut",
                         x=names, y=bagruts, marker_color="#6ee7b7", opacity=0.7))
    fig.add_trace(go.Scatter(name="משוקלל" if lang=="he" else "Combined",
                              x=names, y=combined_scores,
                              mode="lines+markers",
                              line=dict(color="#f472b6", width=2.5),
                              marker=dict(size=8, color="#f472b6")))
    fig.update_layout(
        barmode="group",
        plot_bgcolor="#10151f", paper_bgcolor="#080b12",
        font=dict(color="#e8edf5", family="Heebo"),
        legend=dict(font=dict(color="#e8edf5")),
        yaxis=dict(range=[0,105], showgrid=True, gridcolor="#1e2a3d"),
        xaxis=dict(showgrid=False),
        height=320, margin=dict(l=20,r=20,t=20,b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_sim(t, lang):
    subs = st.session_state.bag_subjects
    if not subs:
        st.info(t("bag_no_subjects"))
        return

    current_avg = _weighted_avg(subs)
    st.markdown(
        f'<div class="sf-card sf-card-accent2" style="margin-bottom:1.2rem">'
        f'<b>{"מה הציון שאני צריך?"if lang=="he" else "What grade do I need?"}</b><br>'
        f'<span style="color:var(--muted);font-size:.87rem">'
        + ("הגדר יעד ממוצע — המחשבון יחשב איזה ציון בגרות אתה צריך במקצוע שתבחר"
           if lang=="he" else
           "Set a target average — the calculator shows what bagrut grade you need in a chosen subject")
        + "</span></div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        target = st.slider(
            t("bag_target"), 60, 100, int(min(current_avg + 5, 100)), key="bag_target_sl"
        )
    with c2:
        sub_names = [s["name"] for s in subs]
        chosen = st.selectbox(
            "מקצוע לשיפור" if lang=="he" else "Subject to improve",
            sub_names, key="bag_sim_sub"
        )

    chosen_sub = next((s for s in subs if s["name"] == chosen), None)
    if not chosen_sub:
        return

    # Calculate needed bagrut grade
    other_contribution = sum(
        (s["school"]*0.4 + s["bagrut"]*0.6) * s["units"]
        for s in subs if s["name"] != chosen
    )
    other_units = sum(s["units"] for s in subs if s["name"] != chosen)
    total_units = sum(s["units"] for s in subs)

    needed_combined = (target * total_units - other_contribution) / chosen_sub["units"]
    needed_bagrut   = (needed_combined - chosen_sub["school"] * 0.4) / 0.6

    nb_color = _grade_color(needed_bagrut)
    feasible = 0 <= needed_bagrut <= 100

    st.markdown(
        f'<div class="sf-card" style="text-align:center;padding:2rem;border-color:{nb_color}44">'
        f'<div style="color:var(--muted);margin-bottom:.4rem">'
        f'{"ציון בגרות נדרש ב" if lang=="he" else "Required bagrut grade in"} {chosen}</div>'
        f'<div style="font-size:3.5rem;font-weight:800;color:{nb_color};font-family:Space Grotesk,monospace">'
        f'{"בלתי אפשרי" if not feasible else f"{needed_bagrut:.1f}"}</div>'
        + (f'<div style="color:var(--muted);font-size:.85rem;margin-top:.5rem">{"ציון נוכחי:" if lang=="he" else "Current grade:"} {chosen_sub["bagrut"]}</div>' if feasible else "")
        + f'</div>',
        unsafe_allow_html=True,
    )

    if not feasible:
        st.warning(
            "הממוצע הזה לא ניתן להשגה במקצוע הזה בלבד. נסה להוריד את היעד או לשפר מקצועות נוספים."
            if lang=="he" else
            "This average can't be reached through this subject alone. Try lowering the target or improving multiple subjects."
        )


def _render_export(t, lang):
    subs = st.session_state.bag_subjects
    if not subs:
        st.info(t("bag_no_subjects"))
        return

    avg = _weighted_avg(subs)

    # pandas summary
    df = pd.DataFrame([{
        t("bag_subject"): s["name"],
        t("bag_units"):   s["units"],
        t("bag_school_grade"): s["school"],
        t("bag_bagrut_grade"): s["bagrut"],
        "Combined": round(s["school"]*0.4 + s["bagrut"]*0.6, 1),
    } for s in subs])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.metric(t("bag_avg"), f"{avg:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSV", csv, "gradeup_bagrut.csv", "text/csv", key="bag_csv")
    with col2:
        if st.button("📥 PDF", key="bag_pdf_btn", type="primary"):
            pdf_bytes = _make_pdf(subs, avg, lang)
            st.download_button(
                "⬇️ " + ("הורד PDF" if lang=="he" else "Download PDF"),
                pdf_bytes, f"gradeup_bagrut_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf", key="bag_pdf_dl"
            )