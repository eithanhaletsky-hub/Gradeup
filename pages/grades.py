"""pages/grades.py — מעקב ציונים + ניתוח AI"""
import streamlit as st
import plotly.graph_objects as go
from datetime import date
from ai_utils import call_gemini, get_api_key

SUBJECTS_HE = ["מתמטיקה","אנגלית","עברית","פיזיקה","כימיה","ביולוגיה",
                "היסטוריה","ספרות",'תנ"ך',"מדעי המחשב","אזרחות","גיאוגרפיה","אחר"]
SUBJECTS_EN = ["Math","English","Hebrew","Physics","Chemistry","Biology",
                "History","Literature","Bible","Computer Sci.","Civics","Geography","Other"]

ASSESS_HE = ["מבחן","בוחן","שיעורי בית","פרויקט","בעל-פה","אחר"]
ASSESS_EN = ["Test","Quiz","Homework","Project","Oral","Other"]

GRADE_COLORS = {
    range(90,101): "#6ee7b7",
    range(75,90):  "#38bdf8",
    range(60,75):  "#facc15",
    range(0,60):   "#f87171",
}

def _grade_color(score: float, max_score: float) -> str:
    pct = score / max_score * 100
    for rng, col in GRADE_COLORS.items():
        if int(pct) in rng:
            return col
    return "#94a3b8"

def _grade_emoji(pct: float) -> str:
    if pct >= 90: return "🏆"
    if pct >= 75: return "✅"
    if pct >= 60: return "📈"
    return "⚠️"


def render(t):
    lang = st.session_state.lang
    st.markdown(
        f'<div class="sf-section-title">{t("grades_title")}</div>',
        unsafe_allow_html=True,
    )

    if "grades" not in st.session_state:
        st.session_state.grades = [
            {"subject":"מתמטיקה","score":87,"max":100,"type":"מבחן",  "date":str(date.today()),"note":""},
            {"subject":"אנגלית",  "score":92,"max":100,"type":"בוחן",  "date":str(date.today()),"note":"טוב מאוד"},
            {"subject":"פיזיקה",  "score":74,"max":100,"type":"מבחן",  "date":str(date.today()),"note":""},
            {"subject":"עברית",   "score":55,"max":100,"type":"פרויקט","date":str(date.today()),"note":"צריך שיפור"},
        ]

    subjects = SUBJECTS_HE if lang == "he" else SUBJECTS_EN
    assess   = ASSESS_HE   if lang == "he" else ASSESS_EN

    tab_enter, tab_overview, tab_ai = st.tabs([
        t("grades_tab_enter"),
        t("grades_tab_overview"),
        t("grades_tab_ai"),
    ])

    # ── Tab 1: Enter grade ────────────────────────────────────────
    with tab_enter:
        st.markdown(
            f'<div class="sf-section-title">{"הכנס ציון חדש" if lang=="he" else "Add New Grade"}</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            subj = st.selectbox(t("grades_subject"), subjects, key="g_subj")
        with c2:
            atype = st.selectbox(t("grades_type"), assess, key="g_type")
        with c3:
            gdate = st.date_input(t("grades_date"), key="g_date")

        c4, c5, c6 = st.columns(3)
        with c4:
            score = st.number_input(t("grades_score"), min_value=0, max_value=200, value=80, key="g_score")
        with c5:
            max_s = st.number_input(t("grades_max"), min_value=1, max_value=200, value=100, key="g_max")
        with c6:
            note = st.text_input(t("grades_note"), key="g_note", placeholder="(אופציונלי)")

        # Live preview
        pct = score / max_s * 100
        col = _grade_color(score, max_s)
        st.markdown(
            f'<div class="sf-card" style="border-color:{col};padding:1rem;text-align:center">'
            f'<span style="font-size:1.8rem;font-weight:800;color:{col}">'
            f'{score}/{max_s}</span>'
            f'<span style="font-size:1.2rem;color:var(--muted)"> ({pct:.1f}%) {_grade_emoji(pct)}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if st.button(f"✅ {t('add')}", type="primary", key="btn_add_grade"):
            st.session_state.grades.append({
                "subject": subj, "score": score, "max": max_s,
                "type": atype, "date": str(gdate), "note": note,
            })
            st.success(t("success"))
            st.rerun()

        # Existing grades table
        if st.session_state.grades:
            st.markdown("---")
            st.markdown(
                f'<div class="sf-section-title">{"כל הציונים" if lang=="he" else "All Grades"}</div>',
                unsafe_allow_html=True,
            )
            for i, g in enumerate(st.session_state.grades):
                pct_g = g["score"] / g["max"] * 100
                col_g = _grade_color(g["score"], g["max"])
                c1, c2, c3, c4, c5 = st.columns([2, 1.2, 1.2, 1.5, .4])
                with c1:
                    st.markdown(
                        f'<b>{g["subject"]}</b>'
                        f'<span style="color:var(--muted);font-size:.8rem"> [{g["type"]}]</span>'
                        + (f'<span style="color:var(--muted);font-size:.78rem"> — {g["note"]}</span>' if g.get("note") else ""),
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        f'<span style="color:{col_g};font-weight:700">{g["score"]}/{g["max"]}</span>',
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        f'<span style="color:{col_g}">{pct_g:.1f}% {_grade_emoji(pct_g)}</span>',
                        unsafe_allow_html=True,
                    )
                with c4:
                    st.caption(g["date"])
                with c5:
                    if st.button("🗑️", key=f"del_g_{i}"):
                        st.session_state.grades.pop(i)
                        st.rerun()

    # ── Tab 2: Overview charts ────────────────────────────────────
    with tab_overview:
        grades = st.session_state.grades
        if not grades:
            st.info(t("grades_no_data"))
            return

        # Per-subject averages
        subj_scores: dict[str, list] = {}
        for g in grades:
            pct = g["score"] / g["max"] * 100
            subj_scores.setdefault(g["subject"], []).append(pct)

        subj_avgs  = {s: sum(v)/len(v) for s, v in subj_scores.items()}
        sorted_sub = sorted(subj_avgs.items(), key=lambda x: x[1], reverse=True)
        labels     = [s for s, _ in sorted_sub]
        avgs       = [v for _, v in sorted_sub]
        bar_colors = [_grade_color(v, 100) for v in avgs]

        fig_bar = go.Figure(go.Bar(
            x=labels, y=avgs,
            marker=dict(color=bar_colors, line=dict(color="#080b12", width=1)),
            text=[f"{v:.1f}%" for v in avgs],
            textposition="outside",
            textfont=dict(color="#e8edf5"),
        ))
        fig_bar.update_layout(
            title=dict(text="ממוצע לפי מקצוע" if lang=="he" else "Average by Subject",
                       font=dict(color="#e8edf5")),
            plot_bgcolor="#10151f", paper_bgcolor="#080b12",
            font=dict(color="#e8edf5", family="Heebo"),
            yaxis=dict(range=[0,110], showgrid=True, gridcolor="#1e2a3d"),
            xaxis=dict(showgrid=False),
            height=350, margin=dict(l=30,r=20,t=50,b=40),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Trend line per subject
        if len(grades) >= 3:
            st.markdown(
                f'<div class="sf-section-title">{"מגמה לאורך זמן" if lang=="he" else "Trend Over Time"}</div>',
                unsafe_allow_html=True,
            )
            sel_subj = st.selectbox(
                "בחר מקצוע" if lang == "he" else "Select subject",
                list(subj_scores.keys()), key="trend_subj"
            )
            trend_data = [(g["date"], g["score"]/g["max"]*100)
                          for g in grades if g["subject"] == sel_subj]
            trend_data.sort(key=lambda x: x[0])
            dates_t = [d for d, _ in trend_data]
            scores_t= [s for _, s in trend_data]

            trend_col = _grade_color(scores_t[-1], 100) if scores_t else "#6ee7b7"
            fig_line = go.Figure(go.Scatter(
                x=dates_t, y=scores_t,
                mode="lines+markers",
                line=dict(color=trend_col, width=2.5),
                marker=dict(color=trend_col, size=8),
            ))
            fig_line.update_layout(
                plot_bgcolor="#10151f", paper_bgcolor="#080b12",
                font=dict(color="#e8edf5", family="Heebo"),
                yaxis=dict(range=[0,105], showgrid=True, gridcolor="#1e2a3d",
                           title="%"),
                xaxis=dict(showgrid=False),
                height=280, margin=dict(l=40,r=20,t=20,b=40),
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # Summary stats
        all_pcts = [g["score"]/g["max"]*100 for g in grades]
        overall  = sum(all_pcts) / len(all_pcts)
        best_s   = max(subj_avgs, key=subj_avgs.get)
        weak_s   = min(subj_avgs, key=subj_avgs.get)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="sf-stat">'
                f'<div class="sf-stat-num" style="color:{_grade_color(overall,100)}">{overall:.1f}%</div>'
                f'<div class="sf-stat-label">{"ממוצע כללי" if lang=="he" else "Overall avg"}</div>'
                f'</div>', unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="sf-stat">'
                f'<div class="sf-stat-num" style="color:#6ee7b7;font-size:1rem">{best_s}</div>'
                f'<div class="sf-stat-label">{"הכי חזק" if lang=="he" else "Strongest"} 💪</div>'
                f'</div>', unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="sf-stat">'
                f'<div class="sf-stat-num" style="color:#facc15;font-size:1rem">{weak_s}</div>'
                f'<div class="sf-stat-label">{"צריך חיזוק" if lang=="he" else "Needs work"} 📚</div>'
                f'</div>', unsafe_allow_html=True,
            )

    # ── Tab 3: AI Analysis ────────────────────────────────────────
    with tab_ai:
        st.markdown(
            f'<div class="sf-card sf-card-accent2" style="margin-bottom:1rem">'
            f'<span style="color:var(--muted);font-size:.87rem">'
            + ("ה-AI יקבל את כל הציונים שלך ויחזיר: ניתוח חוזקות וחולשות, המלצות ספציפיות לשיפור, ועל מה לשים דגש בלימודים."
               if lang == "he" else
               "The AI gets all your grades and returns: strengths & weaknesses analysis, specific improvement tips, and what to focus on.")
            + "</span></div>",
            unsafe_allow_html=True,
        )

        if not get_api_key():
            st.warning(t("hw_api_missing"))
            return
        if not st.session_state.grades:
            st.info(t("grades_no_data"))
            return

        if "grades_ai" not in st.session_state:
            st.session_state.grades_ai = None

        if st.button(f"🤖 {t('grades_ai_prompt')}", type="primary", key="btn_grades_ai"):
            grades_text = "\n".join(
                f"  {g['subject']} | {g['type']} | {g['score']}/{g['max']} ({g['score']/g['max']*100:.1f}%) | {g['date']}"
                + (f" | {g['note']}" if g.get("note") else "")
                for g in st.session_state.grades
            )
            sys = (
                "אתה יועץ לימודי לתלמיד תיכון. קיבלת רשימת ציונים. "
                "1. זהה 2-3 מקצועות חזקים ו-2-3 שצריכים שיפור. "
                "2. תן המלצות לימוד ספציפיות לכל מקצוע חלש. "
                "3. זהה מגמות (עולה/יורד). "
                "4. שאלה אחת שתעזור לך להבין את הסיבה לקשיים. "
                "ענה בעברית, ידידותי ומעשי."
                if lang == "he" else
                "You are a study advisor for a high school student. You received their grades list. "
                "1. Identify 2-3 strong subjects and 2-3 needing improvement. "
                "2. Give specific study tips for each weak subject. "
                "3. Spot trends (rising/falling). "
                "4. Ask one question to understand the root of difficulties. "
                "Reply in English, friendly and practical."
            )
            with st.spinner(t("hw_thinking")):
                try:
                    st.session_state.grades_ai = call_gemini(
                        system_prompt=sys, user_text=grades_text,
                        max_tokens=1200, temperature=0.65,
                    )
                except Exception as e:
                    st.error(f"{t('error')}: {e}")

        if st.session_state.grades_ai:
            st.markdown(
                f'<div class="sf-bubble-ai">'
                f'<div class="sf-bubble-label">{t("ai_label")}</div>'
                f'{st.session_state.grades_ai}</div>',
                unsafe_allow_html=True,
            )
            if st.button(t("clear"), key="clear_grades_ai"):
                st.session_state.grades_ai = None
                st.rerun()