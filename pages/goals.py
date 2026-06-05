"""pages/goals.py — מעקב יעדים אישיים + דוח שבועי PDF + pandas"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import date, datetime
from ai_utils import call_gemini, get_api_key
import uuid # הוספתי import עבור uuid

# הגדרות גלובליות
GOAL_TYPES_HE = ["📊 ציון מינימום","🔄 הרגל יומי","💰 חיסכון כסף","📚 שעות לימוד","🏃 פעילות גופנית","🎯 אחר"]
GOAL_TYPES_EN = ["📊 Min grade","🔄 Daily habit","💰 Save money","📚 Study hours","🏃 Exercise","🎯 Other"]

TYPE_ICONS = {"📊":"📊","🔄":"🔄","💰":"💰","📚":"📚","🏃":"🏃","🎯":"🎯"}
TYPE_COLORS= {"📊 ציון מינימום":"#6ee7b7","📊 Min grade":"#6ee7b7",
              "🔄 הרגל יומי":"#38bdf8","🔄 Daily habit":"#38bdf8",
              "💰 חיסכון כסף":"#facc15","💰 Save money":"#facc15",
              "📚 שעות לימוד":"#f472b6","📚 Study hours":"#f472b6",
              "🏃 פעילות גופנית":"#fb923c","🏃 Exercise":"#fb923c",
              "🎯 אחר":"#a78bfa","🎯 Other":"#a78bfa"}


# ── יצירת דוח PDF ──────────────────────────────────────────────────────────
def _make_report_pdf(goals: list, username: str, lang: str) -> bytes:
    """
    יוצר דוח PDF שבועי עם סיכום היעדים וההתקדמות.
    :param goals: רשימת היעדים.
    :param username: שם המשתמש.
    :param lang: שפת הממשק (he/en).
    :return: קובץ PDF בייטס.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # כותרת ראשית
    pdf.set_font("Helvetica","B",18)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,12,"Gradeup — Weekly Goals Report",ln=True,align="C")

    # פרטי המשתמש והתאריך
    pdf.set_font("Helvetica","",10)
    pdf.set_text_color(150,160,180)
    pdf.cell(0,7,f"User: {username}  |  {datetime.now().strftime('%d/%m/%Y')}",ln=True,align="C")

    pdf.ln(6)
    pdf.line(10,pdf.get_y(),200,pdf.get_y()) # קו הפרדה
    pdf.ln(6)

    # מעבר על כל יעד והוספתו לדוח
    for g in goals:
        # חישוב אחוז ההתקדמות
        pct     = min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0
        done    = pct >= 100
        # קביעת צבע סרגל ההתקדמות
        bar_col = (110,231,183) if done else (56,189,248) if pct>=50 else (251,146,60)

        # כותרת היעד
        pdf.set_font("Helvetica","B",12)
        pdf.set_text_color(232,237,245)
        pdf.cell(0,8,f"{g['type'][0]} {g['name']}",ln=True)

        # פרטי התקדמות ותאריך יעד
        pdf.set_font("Helvetica","",10)
        pdf.set_text_color(*bar_col)
        status = "DONE!" if done else f"{pct}%"
        pdf.cell(0,6,f"Progress: {g['current']} / {g['target']}  ({status})  |  Deadline: {g['deadline']}",ln=True)

        # סרגל התקדמות ויזואלי
        pdf.set_fill_color(30,42,61) # צבע רקע הסרגל
        pdf.rect(10,pdf.get_y(),180,5,"F")
        fill_w = max(1, int(180*pct/100)) # רוחב החלק המושלם
        pdf.set_fill_color(*bar_col)
        pdf.rect(10,pdf.get_y()-0.1,fill_w,5.2,"F") # צבע ההתקדמות
        pdf.ln(8)

        # הוספת הערה אם קיימת
        if g.get("note"):
            pdf.set_text_color(90,106,130)
            pdf.set_font("Helvetica","I",9)
            pdf.cell(0,5,f"Note: {g['note']}",ln=True)
        pdf.ln(3)

    # פוטר
    pdf.set_font("Helvetica","I",9)
    pdf.set_text_color(40,60,80)
    pdf.cell(0,6,"gradeup.co.il",ln=True,align="C")

    return bytes(pdf.output()) # החזרת הדוח כבייטים


# ── פונקציית רינדור ראשית ────────────────────────────────────────────
def render(t):
    """
    פונקציית הרינדור הראשית של עמוד היעדים.
    מאתחלת את הנתונים, יוצרת לשוניות ומציגה את התוכן המתאים.
    :param t: פונקציית תרגום (למשל, מתרגם מחרוזות).
    """
    lang = st.session_state.lang
    # כותרת ראשית של העמוד
    st.markdown(f'<div class="sf-section-title">{t("goals_title")}</div>', unsafe_allow_html=True)

    # אתחול משתני session state אם אינם קיימים
    if "goals" not in st.session_state:
        st.session_state.goals = [
            {"id":"g1","name":"ציון 85+ במתמטיקה","type":"📊 ציון מינימום",
             "target":85,"current":74,"unit":"נקודות","deadline":"30/06/2025","note":"","done":False},
            {"id":"g2","name":"לימוד 1 שעה ביום","type":"📚 שעות לימוד",
             "target":30,"current":12,"unit":"שעות","deadline":"30/06/2025","note":"יותר בשעה 19-20","done":False},
            {"id":"g3","name":"חסוך 200 ₪","type":"💰 חיסכון כסף",
             "target":200,"current":60,"unit":"₪","deadline":"31/07/2025","note":"","done":False},
        ]

    # יצירת לשוניות לניווט בין מצבי היעדים
    tab_active, tab_add, tab_report = st.tabs([
        t("goals_tab_active"),
        t("goals_tab_add"),
        t("goals_tab_report"),
    ])

    # הצגת התוכן של כל לשונית
    with tab_active: _render_active(t, lang)
    with tab_add:    _render_add(t, lang)
    with tab_report: _render_report(t, lang)


# ── הצגת יעדים פעילים ────────────────────────────────────────────────────
def _render_active(t, lang):
    """
    מרנדר את רשימת היעדים הפעילים והושלמו.
    """
    goals = st.session_state.goals
    # אם אין יעדים, הצג הודעה מתאימה
    if not goals:
        st.info(t("goals_no_goals"))
        return

    # הפרדת יעדים פעילים ומושלמים
    active = [g for g in goals if not g.get("done")]
    done   = [g for g in goals if g.get("done")]

    # הצגת סטטיסטיקת יעדים פעילים/הושלמו
    st.markdown(
        f'<div style="color:var(--muted);font-size:.85rem;margin-bottom:.8rem">'
        f'{len(active)} {"פעילים" if lang=="he" else "active"} · '
        f'{len(done)} {"הושלמו" if lang=="he" else "completed"}</div>',
        unsafe_allow_html=True,
    )

    # הצגת כל יעד ברשימה
    for g in goals:
        pct   = min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0
        color = TYPE_COLORS.get(g["type"], "#a78bfa") # צבע לפי סוג היעד
        is_done = pct >= 100 or g.get("done") # בדיקה אם היעד הושלם

        # עיצוב הכרטיסיה של היעד
        st.markdown(
            f'<div class="sf-card" style="border-color:{color}44;padding:1.2rem;margin-bottom:.8rem">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<div><b style="color:{color}">{g["type"][0]} {g["name"]}</b>'
            f'<span style="color:var(--muted);font-size:.78rem;margin-right:.5rem"> · {g["deadline"]}</span></div>'
            f'<div style="font-family:Space Grotesk,monospace;font-size:1.4rem;font-weight:700;color:{color}">'
            f'{"🏆" if is_done else f"{pct}%"}</div></div>' # הצגת אייקון סיום או אחוז התקדמות
            # סרגל התקדמות ויזואלי
            f'<div style="background:#1e2a3d;border-radius:99px;height:8px;margin:.7rem 0">'
            f'<div style="background:{color};width:{pct}%;height:100%;border-radius:99px;transition:width .4s"></div></div>'
            f'<div style="color:var(--muted);font-size:.82rem">'
            f'{g["current"]} / {g["target"]} {g.get("unit","")}' # הצגת ערך נוכחי/יעד ויחידה
            + (f' · {g["note"]}' if g.get("note") else "") # הוספת הערה אם קיימת
            + f'</div></div>',
            unsafe_allow_html=True,
        )

        # אם היעד אינו מושלם, הצג כפתורי עריכה
        if not is_done:
            col_update, col_done, col_del = st.columns([3, 1, 1])
            with col_update:
                # שדה קלט לעדכון הערך הנוכחי
                new_val = st.number_input(
                    t("goals_current"),
                    min_value=0.0, max_value=float(g["target"]*2),
                    value=float(g["current"]),
                    key=f"goal_upd_{g['id']}",
                    label_visibility="collapsed", # הסתרת התווית כי היא מיותרת כאן
                )
                # אם הערך השתנה, עדכן את היעד ובדוק אם הושלם
                if new_val != g["current"]:
                    g["current"] = new_val
                    if new_val >= g["target"]:
                        g["done"] = True
                    st.rerun() # הפעל מחדש את האפליקציה כדי להציג את השינוי
            with col_done:
                # כפתור לסימון היעד כהושלם
                if st.button(t("goals_done"), key=f"goal_done_{g['id']}"):
                    g["done"] = True
                    st.rerun()
            with col_del:
                # כפתור למחיקת היעד
                if st.button("🗑️", key=f"goal_del_{g['id']}"):
                    st.session_state.goals.remove(g)
                    st.rerun()
        else:
            # אם היעד הושלם, הצג הודעה מתאימה
            st.markdown(
                f'<div style="color:#6ee7b7;font-size:.88rem;margin-top:.3rem">{t("goals_done")}</div>',
                unsafe_allow_html=True,
            )


# ── הוספת יעד חדש ───────────────────────────────────────────────────────
def _render_add(t, lang):
    """
    מרנדר את הטופס להוספת יעד חדש.
    """
    types = GOAL_TYPES_HE if lang == "he" else GOAL_TYPES_EN

    st.markdown(
        f'<div class="sf-section-title">{"הוסף יעד חדש" if lang=="he" else "Add New Goal"}</div>',
        unsafe_allow_html=True,
    )

    # חלוקה לשתי עמודות עבור שדות הקלט
    c1, c2 = st.columns(2)
    with c1:
        name  = st.text_input(t("goals_name"), key="g_name",
                               placeholder="ציון 90 בפיזיקה" if lang=="he" else "Get 90 in Physics")
        gtype = st.selectbox(t("goals_type"), types, key="g_type")
    with c2:
        target  = st.number_input(t("goals_target"), min_value=1, value=100, key="g_target")
        unit    = st.text_input("יחידה" if lang=="he" else "Unit",
                                 value="נקודות" if lang=="he" else "points", key="g_unit")

    # שדות נוספים: תאריך יעד והערה
    deadline = st.date_input(t("goals_deadline"), key="g_deadline")
    note     = st.text_input("הערה" if lang=="he" else "Note", key="g_note", placeholder="(אופציונלי)")

    # כפתור הוספה
    if st.button(f"✅ {t('add')}", type="primary", key="g_add_btn"):
        # בדיקה שהשם אינו ריק
        if not name.strip():
            st.error("כתוב שם ליעד" if lang=="he" else "Enter a goal name")
        else:
            # הוספת היעד החדש לרשימת היעדים ב-session state
            st.session_state.goals.append({
                "id":       str(uuid.uuid4())[:8], # יצירת מזהה ייחודי קצר
                "name":     name.strip(),
                "type":     gtype,
                "target":   target,
                "current":  0, # אתחול הערך הנוכחי ל-0
                "unit":     unit,
                "deadline": str(deadline), # שמירת תאריך היעד כמחרוזת
                "note":     note,
                "done":     False, # יעד חדש מתחיל כלא מושלם
            })
            st.success(f"✅ {t('success')}") # הודעת הצלחה
            st.rerun() # הפעל מחדש כדי לנקות את הטופס ולהציג את היעד החדש


# ── דוח שבועי ─────────────────────────────────────────────────────────
def _render_report(t, lang):
    """
    מרנדר את הדוח השבועי, הכולל טבלה, גרף וסטטיסטיקות.
    """
    goals = st.session_state.goals
    if not goals:
        st.info(t("goals_no_goals"))
        return

    # 1. יצירת DataFrame של Pandas מהיעדים
    df = pd.DataFrame([{
        "שם" if lang=="he" else "Name": g["name"],
        "סוג" if lang=="he" else "Type": g["type"],
        "יעד" if lang=="he" else "Target": g["target"],
        "נוכחי" if lang=="he" else "Current": g["current"],
        "%" : min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0,
        "סטטוס" if lang=="he" else "Status": "✅ הושלם" if g.get("done") or g["current"]>=g["target"] else "🔄 בתהליך",
        "דדליין" if lang=="he" else "Deadline": g["deadline"],
    } for g in goals])

    # הצגת הטבלה ב-Streamlit
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 2. יצירת גרף עמודות (Bar chart) באמצעות Plotly
    names  = [g["name"][:20] for g in goals] # קיצור שמות היעדים לגרף
    pcts   = [min(100, int(g["current"]/g["target"]*100)) if g["target"] else 0 for g in goals]
    colors = [TYPE_COLORS.get(g["type"],"#a78bfa") for g in goals] # צבעי עמודות לפי סוג

    fig = go.Figure(go.Bar(
        x=pcts, y=names, orientation="h", # גרף אופקי
        marker=dict(color=colors, line=dict(color="#080b12",width=1)), # עיצוב העמודות
        text=[f"{p}%" for p in pcts], # טקסט על העמודות
        textposition="outside", # מיקום הטקסט מחוץ לעמודה
        textfont=dict(color="#e8edf5"), # צבע הטקסט
    ))
    # הגדרות עיצוב לגרף
    fig.update_layout(
        plot_bgcolor="#10151f", paper_bgcolor="#080b12", # צבעי רקע
        font=dict(color="#e8edf5",family="Heebo"), # גופן
        xaxis=dict(range=[0,115],showgrid=True,gridcolor="#1e2a3d"), # ציר X
        yaxis=dict(showgrid=False), # הסתרת רשת ציר Y
        height=max(200, 60*len(goals)), # גובה דינמי של הגרף
        margin=dict(l=20,r=60,t=20,b=20), # שוליים
    )
    st.plotly_chart(fig, use_container_width=True) # הצגת הגרף

    # 3. הצגת סטטיסטיקות סיכום
    avg_pct  = df["%"].mean() if "%" in df.columns else 0 # ממוצע אחוז ההתקדמות
    # ספירת יעדים מושלמים/בתהליך
    done_cnt = df[df["%"] >= 100].shape[0] if "%" in df.columns else 0

    # חלוקה לשלוש עמודות לסטטיסטיקות
    c1, c2, c3 = st.columns(3)
    for col, val, lbl in [
        (c1, f"{avg_pct:.0f}%", "ממוצע התקדמות" if lang=="he" else "Avg progress"),
        (c2, done_cnt, "הושלמו" if lang=="he" else "Completed"),
        (c3, len(goals)-done_cnt, "בתהליך" if lang=="he" else "In progress"),
    ]:
        with col:
            # עיצוב קופסת הסטטיסטיקה
            st.markdown(
                f'<div class="sf-stat"><div class="sf-stat-num">{val}</div>'
                f'<div class="sf-stat-label">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True) # רווח

    # 4. יצירת סיכום AI
    if st.button(t("goals_ai_report"), type="primary", key="goals_ai_btn"):
        if not get_api_key(): # בדיקה אם מפתח ה-API זמין
            st.warning(t("hw_api_missing"))
        else:
            # הכנת הטקסט שיועבר ל-AI
            goals_text = "\n".join(
                f"  {g['name']} [{g['type']}]: {g['current']}/{g['target']} ({min(100,int(g['current']/g['target']*100))}%) — {g['deadline']}"
                for g in goals
            )
            # הנחיית המערכת ל-AI
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
            # קריאה ל-AI והצגת התשובה
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

    # 5. כפתור לייצוא הדוח כ-PDF
    if st.button(f"📥 {t('sum_export_pdf')}", key="goals_pdf_btn"):
        user = st.session_state.get("user", {}) # קבלת פרטי המשתמש מה-session state
        try:
            # יצירת הדוח באמצעות הפונקציה _make_report_pdf
            pdf_b = _make_report_pdf(goals, user.get("username","Student"), lang)
            # יצירת כפתור הורדה ל-PDF
            st.download_button(
                "📥 " + ("הורד דוח PDF" if lang=="he" else "Download PDF Report"),
                data=pdf_b,
                file_name=f"gradeup_goals_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="goals_pdf_dl",
            )
        except Exception as e:
            st.error(str(e)) # הצגת הודעת שגיאה אם קרתה בעיה
