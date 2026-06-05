"""pages/goals.py — מעקב יעדים אישיים + דוח שבועי PDF + pandas"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import date, datetime
from ai_utils import call_gemini, get_api_key

GOAL_TYPES_HE = ["📊 ציון מינימום","🔄 הרגל יומי","💰 חיסכון כסף","📚 שעות לימוד","🏃 פעילות גופנית","🎯 אחר"]
GOAL_TYPES_EN = ["📊 Min grade","🔄 Daily habit","💰 Save money","📚 Study hours","🏃 Exercise","🎯 Other"]

TYPE_ICONS = {"📊":"📊","🔄":"🔄","💰":"💰","📚":"📚","🏃":"🏃","🎯":"🎯"}
TYPE_COLORS= {"📊 ציון מינימום":"#6ee7b7","📊 Min grade":"#6ee7b7",
              "🔄 הרגל יומי":"#38bdf8","🔄 Daily habit":"#38bdf8",
              "💰 חיסכון כסף":"#facc15","💰 Save money":"#facc15",
              "📚 שעות לימוד":"#f472b6","📚 Study hours":"#f472b6",
              "🏃 פעילות גופנית":"#fb923c","🏃 Exercise":"#fb923c",
              "🎯 אחר":"#a78bfa","🎯 Other":"#a78bfa"}


def _make_report_pdf(goals: list, username: str, lang: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica","B",18)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,12,"Gradeup — Weekly Goals Report",ln=True,align="C")
    pdf.set_font("Helvetica","",10)
    pdf.set_text_color(150,160,180)
    pdf.cell(0,7,f"User: {username}  |  {datetime.now().strftime('%d/%m/%Y')}",ln=True,align="C")
    pdf.ln(6)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(6)

    for g in goals:
        pct     = min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0
        done    = pct >= 100
        bar_col = (110,231,183) if done else (56,189,248) if pct>=50 else (251,146,60)

        pdf.set_font("Helvetica","B",12)
        pdf.set_text_color(232,237,245)
        pdf.cell(0,8,f"{g['type'][0]} {g['name']}",ln=True)

        pdf.set_font("Helvetica","",10)
        pdf.set_text_color(*bar_col)
        status = "DONE!" if done else f"{pct}%"
        pdf.cell(0,6,f"Progress: {g['current']} / {g['target']}  ({status})  |  Deadline: {g['deadline']}",ln=True)

        # Progress bar
        pdf.set_fill_color(30,42,61)
        pdf.rect(10,pdf.get_y(),180,5,"F")
        fill_w = max(1, int(180*pct/100))
        pdf.set_fill_color(*bar_col)
        pdf.rect(10,pdf.get_y()-0.1,fill_w,5.2,"F")
        pdf.ln(8)

        if g.get("note"):
            pdf.set_text_color(90,106,130)
            pdf.set_font("Helvetica","I",9)
            pdf.cell(0,5,f"Note: {g['note']}",ln=True)
        pdf.ln(3)

    pdf.set_font("Helvetica","I",9)
    pdf.set_text_color(40,60,80)
    pdf.cell(0,6,"gradeup.co.il",ln=True,align="C")
    return bytes(pdf.output())


def render(t):
    lang = st.session_state.lang
    st.markdown(f'<div class="sf-section-title">{t("goals_title")}</div>', unsafe_allow_html=True)

    if "goals" not in st.session_state:
        st.session_state.goals = [
            {"id":"g1","name":"ציון 85+ במתמטיקה","type":"📊 ציון מינימום",
             "target":85,"current":74,"unit":"נקודות","deadline":"30/06/2025","note":"","done":False},
            {"id":"g2","name":"לימוד 1 שעה ביום","type":"📚 שעות לימוד",
             "target":30,"current":12,"unit":"שעות","deadline":"30/06/2025","note":"יותר בשעה 19-20","done":False},
            {"id":"g3","name":"חסוך 200 ₪","type":"💰 חיסכון כסף",
             "target":200,"current":60,"unit":"₪","deadline":"31/07/2025","note":"","done":False},
        ]

    tab_active, tab_add, tab_report = st.tabs([
        t("goals_tab_active"),
        t("goals_tab_add"),
        t("goals_tab_report"),
    ])

    with tab_active: _render_active(t, lang)
    with tab_add:    _render_add(t, lang)
    with tab_report: _render_report(t, lang)


# ── Active goals ──────────────────────────────────────────────────────────
def _render_active(t, lang):
    goals = st.session_state.goals
    if not goals:
        st.info(t("goals_no_goals"))
        return

    active = [g for g in goals if not g.get("done")]
    done   = [g for g in goals if g.get("done")]

    st.markdown(
        f'<div style="color:var(--muted);font-size:.85rem;margin-bottom:.8rem">'
        f'{len(active)} {"פעילים" if lang=="he" else "active"} · '
        f'{len(done)} {"הושלמו" if lang=="he" else "completed"}</div>',
        unsafe_allow_html=True,
    )

    for g in goals:
        pct   = min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0
        color = TYPE_COLORS.get(g["type"], "#a78bfa")
        is_done = pct >= 100 or g.get("done")

        st.markdown(
            f'<div class="sf-card" style="border-color:{color}44;padding:1.2rem;margin-bottom:.8rem">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<div><b style="color:{color}">{g["type"][0]} {g["name"]}</b>'
            f'<span style="color:var(--muted);font-size:.78rem;margin-right:.5rem"> · {g["deadline"]}</span></div>'
            f'<div style="font-family:Space Grotesk,monospace;font-size:1.4rem;font-weight:700;color:{color}">'
            f'{"🏆" if is_done else f"{pct}%"}</div></div>'
            f'<div style="background:#1e2a3d;border-radius:99px;height:8px;margin:.7rem 0">'
            f'<div style="background:{color};width:{pct}%;height:100%;border-radius:99px;transition:width .4s"></div></div>'
            f'<div style="color:var(--muted);font-size:.82rem">'
            f'{g["current"]} / {g["target"]} {g.get("unit","")}'
            + (f' · {g["note"]}' if g.get("note") else "")
            + f'</div></div>',
            unsafe_allow_html=True,
        )

        if not is_done:
            col_update, col_done, col_del = st.columns([3, 1, 1])
            with col_update:
                new_val = st.number_input(
                    t("goals_current"),
                    min_value=0.0, max_value=float(g["target"]*2),
                    value=float(g["current"]),
                    key=f"goal_upd_{g['id']}",
                    label_visibility="collapsed",
                )
                if new_val != g["current"]:
                    g["current"] = new_val
                    if new_val >= g["target"]:
                        g["done"] = True
                    st.rerun()
            with col_done:
                if st.button(t("goals_done"), key=f"goal_done_{g['id']}"):
                    g["done"] = True
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"goal_del_{g['id']}"):
                    st.session_state.goals.remove(g)
                    st.rerun()
        else:
            st.markdown(
                f'<div style="color:#6ee7b7;font-size:.88rem;margin-top:.3rem">{t("goals_done")}</div>',
                unsafe_allow_html=True,
            )


# ── Add goal ──────────────────────────────────────────────────────────────
def _render_add(t, lang):
    types = GOAL_TYPES_HE if lang == "he" else GOAL_TYPES_EN
    import uuid

    st.markdown(
        f'<div class="sf-section-title">{"הוסף יעד חדש" if lang=="he" else "Add New Goal"}</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        name  = st.text_input(t("goals_name"), key="g_name",
                               placeholder="ציון 90 בפיזיקה" if lang=="he" else "Get 90 in Physics")
        gtype = st.selectbox(t("goals_type"), types, key="g_type")
    with c2:
        target  = st.number_input(t("goals_target"), min_value=1, value=100, key="g_target")
        unit    = st.text_input("יחידה" if lang=="he" else "Unit",
                                 value="נקודות" if lang=="he" else "points", key="g_unit")

    deadline = st.date_input(t("goals_deadline"), key="g_deadline")
    note     = st.text_input("הערה" if lang=="he" else "Note", key="g_note", placeholder="(אופציונלי)")

    if st.button(f"✅ {t('add')}", type="primary", key="g_add_btn"):
        if not name.strip():
            st.error("כתוב שם ליעד" if lang=="he" else "Enter a goal name")
        else:
            st.session_state.goals.append({
                "id":       str(uuid.uuid4())[:8],
                "name":     name.strip(),
                "type":     gtype,
                "target":   target,
                "current":  0,
                "unit":     unit,
                "deadline": str(deadline),
                "note":     note,
                "done":     False,
            })
            st.success(f"✅ {t('success')}")
            st.rerun()


# ── Weekly report ─────────────────────────────────────────────────────────
def _render_report(t, lang):
    goals = st.session_state.goals
    if not goals:
        st.info(t("goals_no_goals"))
        return

    # Pandas DataFrame
    df = pd.DataFrame([{
        "שם" if lang=="he" else "Name": g["name"],
        "סוג" if lang=="he" else "Type": g["type"],
        "יעד" if lang=="he" else "Target": g["target"],
        "נוכחי" if lang=="he" else "Current": g["current"],
        "%" : min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0,
        "סטטוס" if lang=="he" else "Status": "✅ הושלם" if g.get("done") or g["current"]>=g["target"] else "🔄 בתהליך",
        "דדליין" if lang=="he" else "Deadline": g["deadline"],
    } for g in goals])

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Plotly bar — progress
    names  = [g["name"][:20] for g in goals]
    pcts   = [min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0 for g in goals]
    colors = [TYPE_COLORS.get(g["type"],"#a78bfa") for g in goals]

    fig = go.Figure(go.Bar(
        x=pcts, y=names, orientation="h",
        marker=dict(color=colors, line=dict(color="#080b12",width=1)),
        text=[f"{p}%" for p in pcts],
        textposition="outside",
        textfont=dict(color="#e8edf5"),
    ))
    fig.update_layout(
        plot_bgcolor="#10151f", paper_bgcolor="#080b12",
        font=dict(color="#e8edf5",family="Heebo"),
        xaxis=dict(range=[0,115],showgrid=True,gridcolor="#1e2a3d"),
        yaxis=dict(showgrid=False),
        height=max(200, 60*len(goals)),
        margin=dict(l=20,r=60,t=20,b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Pandas stats
    avg_pct  = df["%"].mean() if "%" in df.columns else 0
    done_cnt = df[df["%" if True else "%"] >= 100].shape[0] if "%" in df.columns else 0

    c1, c2, c3 = st.columns(3)
    for col, val, lbl in [
        (c1, f"{avg_pct:.0f}%", "ממוצע התקדמות" if lang=="he" else "Avg progress"),
        (c2, done_cnt, "הושלמו" if lang=="he" else "Completed"),
        (c3, len(goals)-done_cnt, "בתהליך" if lang=="he" else "In progress"),
    ]:
        with col:
            st.markdown(
                f'<div class="sf-stat"><div class="sf-stat-num">{val}</div>'
                f'<div class="sf-stat-label">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # AI report
    if st.button(t("goals_ai_report"), type="primary", key="goals_ai_btn"):
        if not get_api_key():
            st.warning(t("hw_api_missing"))
        else:
            goals_text = "\n".join(
                f"  {g['name']} [{g['type']}]: {g['current']}/{g['target']} ({min(100,int(g['current']/g['target']*100))}%) — {g['deadline']}"
                for g in goals
            )
            sys = (
                "אתה מאמן אישי לתלמיד תיכון. קיבלת רשימת יעדים והתקדמות. "
                "1. ציין מה מתקדם טוב ומה פחות. "
                "2. תן 2-3 המלצות ספציפיות לשבוע הקרוב. "
                "3. שאלה מוטיבציונית אחת. ענה בעברית, ידידותי."
                if lang == "he" else
                "You are a personal coach for a high school student. You received their goals and progress. "
                "1. Note what's going well and what's lagging. "
                "2. Give 2-3 specific recommendations for next week. "
                "3. One motivational question. Reply in English, friendly."
            )
            with st.spinner("🤖…"):
                try:
                    result = call_gemini(system_prompt=sys, user_text=goals_text, max_tokens=700)
                    st.markdown(
                        f'<div class="sf-bubble-ai"><div class="sf-bubble-label">{t("ai_label")}</div>'
                        f'{result}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(str(e))

    # PDF export
    if st.button(f"📥 {t('sum_export_pdf')}", key="goals_pdf_btn"):
        user = st.session_state.get("user", {})
        try:
            pdf_b = _make_report_pdf(goals, user.get("username","Student"), lang)
            st.download_button(
                "📥 " + ("הורד דוח PDF" if lang=="he" else "Download PDF Report"),
                data=pdf_b,
                file_name=f"gradeup_goals_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="goals_pdf_dl",
            )
        except Exception as e:
            st.error(str(e))