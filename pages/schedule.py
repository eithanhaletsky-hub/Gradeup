"""pages/schedule.py — מערכת שעות + אירועים אישיים + משימות + AI מסכם"""
import streamlit as st
import plotly.graph_objects as go
from ai_utils import call_gemini, get_api_key
import json
from datetime import date

HOURS = [f"{h:02d}:00" for h in range(6, 23)]

# סוגי פריטים וצבעיהם
TYPE_COLORS = {
    # בית-ספר
    "שיעור":       "#6ee7b7",
    "Class":       "#6ee7b7",
    "מבחן":        "#fb923c",
    "Exam":        "#fb923c",
    # חוגים
    "ספורט/חוג":   "#38bdf8",
    "Sport/Club":  "#38bdf8",
    # אישי
    "אירוע אישי":  "#f472b6",
    "Personal":    "#f472b6",
    "חברתי":       "#a78bfa",
    "Social":      "#a78bfa",
    "רפואי":       "#facc15",
    "Medical":     "#facc15",
    "אחר":         "#94a3b8",
    "Other":       "#94a3b8",
}

SCHOOL_TYPES_HE = ["שיעור", "מבחן"]
SCHOOL_TYPES_EN = ["Class", "Exam"]
PERSONAL_TYPES_HE = ["ספורט/חוג", "אירוע אישי", "חברתי", "רפואי", "אחר"]
PERSONAL_TYPES_EN = ["Sport/Club", "Personal", "Social", "Medical", "Other"]


def _days(lang):
    he = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    en = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return he if lang == "he" else en


def _hour_f(h: str) -> float:
    p = h.split(":")
    return int(p[0]) + int(p[1]) / 60


def _schedule_to_text(items, tasks, lang) -> str:
    days = _days(lang)
    lines = []
    for item in sorted(items, key=lambda x: (x["day"], x["start"])):
        loc = f" | {item['location']}" if item.get("location") else ""
        lines.append(
            f"  יום {days[item['day']]} {item['start']}-{item['end']}: "
            f"{item['subject']} [{item['type']}]{loc}"
        )
    task_lines = [
        f"  {'✅' if t['done'] else '⬜'} {t['name']} [{t['priority']}] — {t['due']}"
        for t in tasks
    ]
    return (
        "מערכת השעות השבועית:\n" + "\n".join(lines) +
        "\n\nמשימות:\n" + "\n".join(task_lines)
    )


def render(t):
    st.markdown(
        f'<div class="sf-section-title">{t("sched_title")}</div>',
        unsafe_allow_html=True,
    )

    # ── Session defaults ──────────────────────────────────────────
    if "schedule" not in st.session_state:
        st.session_state.schedule = [
            {"day": 0, "start": "08:00", "end": "09:00", "subject": "מתמטיקה",  "type": "שיעור",      "teacher": "", "location": "", "notes": ""},
            {"day": 0, "start": "09:00", "end": "10:00", "subject": "אנגלית",    "type": "שיעור",      "teacher": "", "location": "", "notes": ""},
            {"day": 1, "start": "08:00", "end": "09:00", "subject": "פיזיקה",    "type": "שיעור",      "teacher": "", "location": "", "notes": ""},
            {"day": 2, "start": "16:00", "end": "17:30", "subject": "כדורגל",    "type": "ספורט/חוג",  "teacher": "", "location": "מגרש הספורט", "notes": ""},
            {"day": 3, "start": "14:00", "end": "15:00", "subject": "יום הולדת דנה", "type": "חברתי", "teacher": "", "location": "בית דנה", "notes": "לקנות מתנה!"},
            {"day": 4, "start": "10:00", "end": "11:00", "subject": "בגרות מתמטיקה", "type": "מבחן",  "teacher": "", "location": "כיתה 12", "notes": ""},
        ]
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            {"name": "שיעורי בית — מתמטיקה", "priority": "🔴 גבוהה",   "due": str(date.today()), "done": False},
            {"name": "קריאה — ספרות",          "priority": "🟡 בינונית", "due": str(date.today()), "done": False},
        ]

    # ── Tabs ──────────────────────────────────────────────────────
    tab_view, tab_school, tab_personal, tab_tasks, tab_ai = st.tabs([
        t("sched_tab_view"),
        "🏫 " + ("שיעורים/מבחנים" if st.session_state.lang == "he" else "School"),
        "🎯 " + ("אירועים אישיים" if st.session_state.lang == "he" else "Personal Events"),
        t("sched_tab_tasks"),
        t("sched_tab_ai"),
    ])

    with tab_view:
        _render_timetable(t)
    with tab_school:
        _render_add(t, school=True)
    with tab_personal:
        _render_add(t, school=False)
    with tab_tasks:
        _render_tasks(t)
    with tab_ai:
        _render_ai_summary(t)


# ── Plotly timetable ──────────────────────────────────────────────────────
def _render_timetable(t):
    lang  = st.session_state.lang
    days  = _days(lang)
    items = st.session_state.schedule

    # Filter controls
    all_types = list(dict.fromkeys(i["type"] for i in items))
    col_f, col_days = st.columns([2, 3])
    with col_f:
        show_types = st.multiselect(
            t("sched_filter"),
            options=all_types,
            default=all_types,
            key="sched_filter_types",
        )
    with col_days:
        show_days = st.multiselect(
            "ימים" if lang == "he" else "Days",
            options=list(range(7)),
            default=list(range(6)),
            format_func=lambda x: days[x],
            key="sched_filter_days",
        )

    filtered = [i for i in items if i["type"] in show_types and i["day"] in show_days]

    shapes, annotations = [], []
    for item in filtered:
        x   = show_days.index(item["day"]) if show_days else item["day"]
        y0  = _hour_f(item["start"])
        y1  = _hour_f(item["end"])
        col = TYPE_COLORS.get(item["type"], "#94a3b8")

        shapes.append(dict(
            type="rect",
            x0=x - .43, x1=x + .43,
            y0=y0, y1=y1,
            fillcolor="#6ee7b7",
            line=dict(color=col, width=2),
        ))

        label = f"<b>{item['subject']}</b><br>{item['start']}–{item['end']}"
        if item.get("location"):
            label += f"<br>📍 {item['location']}"
        if item.get("teacher"):
            label += f"<br>👤 {item['teacher']}"

        annotations.append(dict(
            x=x, y=(y0 + y1) / 2,
            text=label,
            showarrow=False,
            font=dict(color=col, size=10),
            align="center",
        ))

    visible_labels = [days[d] for d in show_days] if show_days else days

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[], y=[], mode="markers"))
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        plot_bgcolor="#10151f",
        paper_bgcolor="#080b12",
        font=dict(color="#e8edf5", family="Heebo, sans-serif"),
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(visible_labels))),
            ticktext=visible_labels,
            showgrid=False,
            range=[-.6, len(visible_labels) - .4],
            zeroline=False,
        ),
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(6, 23)),
            ticktext=[f"{h:02d}:00" for h in range(6, 23)],
            showgrid=True,
            gridcolor="#1e2a3d",
            range=[22.5, 5.5],
            zeroline=False,
        ),
        height=620,
        margin=dict(l=55, r=20, t=20, b=20),
    )

    # Legend
    legend_items = [(typ, col) for typ, col in TYPE_COLORS.items()
                    if (lang == "he" and typ not in ("Class","Exam","Sport/Club","Personal","Social","Medical","Other"))
                    or (lang == "en" and typ not in ("שיעור","מבחן","ספורט/חוג","אירוע אישי","חברתי","רפואי","אחר"))]
    for i, (typ, col) in enumerate(legend_items):
        fig.add_annotation(
            x=len(visible_labels) - .4, y=6.2 + i * .65,
            text=f"<span style='color:{col}'>■</span> {typ}",
            showarrow=False, font=dict(color=col, size=9.5), xanchor="left",
        )

    st.plotly_chart(fig, use_container_width=True)

    col_exp, _ = st.columns([1, 3])
    with col_exp:
        if st.button(f"📥 Export JSON", key="export_sched"):
            data = json.dumps(st.session_state.schedule, ensure_ascii=False, indent=2)
            st.download_button("הורד JSON", data, "gradeup_schedule.json", "application/json", key="dl_sched")


# ── Add school / personal item ────────────────────────────────────────────
def _render_add(t, school: bool):
    lang  = st.session_state.lang
    days  = _days(lang)

    if school:
        types = SCHOOL_TYPES_HE if lang == "he" else SCHOOL_TYPES_EN
        title = "🏫 " + ("הוסף שיעור / מבחן" if lang == "he" else "Add Class / Exam")
        subj_placeholder = "מתמטיקה, אנגלית, פיזיקה…" if lang == "he" else "Math, English, Physics…"
    else:
        types = PERSONAL_TYPES_HE if lang == "he" else PERSONAL_TYPES_EN
        title = "🎯 " + ("הוסף אירוע אישי" if lang == "he" else "Add Personal Event")
        subj_placeholder = "כדורגל, יום הולדת, רופא…" if lang == "he" else "Football, birthday, doctor…"

    st.markdown(f'<div class="sf-section-title">{title}</div>', unsafe_allow_html=True)

    # ── Form ──────────────────────────────────────────────────────
    suffix = "school" if school else "personal"
    c1, c2, c3 = st.columns(3)
    with c1:
        day = st.selectbox(t("sched_day"), range(7), format_func=lambda x: days[x], key=f"new_day_{suffix}")
    with c2:
        start = st.selectbox(t("sched_start"), HOURS[:-1], key=f"new_start_{suffix}")
    with c3:
        si  = HOURS.index(start)
        end = st.selectbox(t("sched_end"), HOURS[si + 1:], key=f"new_end_{suffix}")

    c4, c5 = st.columns(2)
    with c4:
        subject = st.text_input(
            t("sched_subject") if school else ("שם האירוע" if lang == "he" else "Event name"),
            placeholder=subj_placeholder, key=f"new_subj_{suffix}"
        )
    with c5:
        item_type = st.selectbox(t("sched_type"), types, key=f"new_type_{suffix}")

    c6, c7 = st.columns(2)
    with c6:
        if school:
            extra = st.text_input(t("sched_teacher"), key=f"new_extra_{suffix}", placeholder="(אופציונלי)")
        else:
            extra = st.text_input(
                t("sched_location") if "sched_location" in ["sched_location"] else
                ("מיקום" if lang == "he" else "Location"),
                key=f"new_extra_{suffix}", placeholder="(אופציונלי)"
            )
    with c7:
        notes = st.text_input(
            "הערות" if lang == "he" else "Notes",
            key=f"new_notes_{suffix}", placeholder="(אופציונלי)"
        )

    # Color picker for personal events
    color_override = None
    if not school:
        st.markdown(f'<div style="color:var(--muted);font-size:.82rem;margin:.4rem 0">{"צבע מותאם (אופציונלי):" if lang=="he" else "Custom color (optional):"}</div>', unsafe_allow_html=True)
        color_cols = st.columns(8)
        palette = ["#6ee7b7","#38bdf8","#f472b6","#fb923c","#a78bfa","#facc15","#34d399","#f87171"]
        for i, (cc, hex_c) in enumerate(zip(color_cols, palette)):
            with cc:
                if st.button("●", key=f"col_{suffix}_{i}",
                             help=hex_c,
                             use_container_width=True):
                    st.session_state[f"sel_color_{suffix}"] = hex_c
        if f"sel_color_{suffix}" in st.session_state:
            color_override = st.session_state[f"sel_color_{suffix}"]
            st.markdown(
                f'<div style="display:inline-block;width:14px;height:14px;'
                f'background:{color_override};border-radius:50%;margin-left:4px;vertical-align:middle"></div>'
                f' <span style="font-size:.82rem;color:var(--muted)">{color_override}</span>',
                unsafe_allow_html=True,
            )

    if st.button(f"✅ {t('add')}", type="primary", key=f"btn_add_{suffix}"):
        if not subject.strip():
            st.error("מלא שם" if lang == "he" else "Name required")
        else:
            entry = {
                "day": day, "start": start, "end": end,
                "subject": subject.strip(), "type": item_type,
                "teacher": extra if school else "",
                "location": extra if not school else "",
                "notes": notes,
            }
            if color_override:
                entry["color"] = color_override
            st.session_state.schedule.append(entry)
            st.success(f"✅ '{subject.strip()}' {t('success')}")
            st.rerun()

    # ── Current list ──────────────────────────────────────────────
    relevant = [i for i in st.session_state.schedule
                if i["type"] in (SCHOOL_TYPES_HE + SCHOOL_TYPES_EN if school
                                  else PERSONAL_TYPES_HE + PERSONAL_TYPES_EN)]
    if relevant:
        st.markdown("---")
        label = ("שיעורים ומבחנים קיימים" if school else "אירועים אישיים קיימים") if lang == "he" else ("Existing classes & exams" if school else "Existing personal events")
        st.markdown(f'<div class="sf-section-title">{label}</div>', unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.schedule):
            if item["type"] not in (SCHOOL_TYPES_HE + SCHOOL_TYPES_EN if school
                                     else PERSONAL_TYPES_HE + PERSONAL_TYPES_EN):
                continue
            col = item.get("color") or TYPE_COLORS.get(item["type"], "#94a3b8")
            real_idx = st.session_state.schedule.index(item)
            c1, c2, c3, c4, c5 = st.columns([.6, 2.4, 1.5, 1.5, .4])
            with c1:
                st.markdown(f'<span class="sf-badge">{days[item["day"]]}</span>', unsafe_allow_html=True)
            with c2:
                loc_str = f' 📍{item["location"]}' if item.get("location") else ""
                note_str = f' 📝{item["notes"]}' if item.get("notes") else ""
                st.markdown(
                    f'<b style="color:{col}">{item["subject"]}</b>'
                    f'<span style="color:var(--muted);font-size:.8rem">'
                    f' [{item["type"]}]{loc_str}{note_str}</span>',
                    unsafe_allow_html=True,
                )
            with c3:
                st.caption(f'{item["start"]} – {item["end"]}')
            with c4:
                teacher_or_loc = item.get("teacher") or item.get("location") or "—"
                st.caption(teacher_or_loc)
            with c5:
                if st.button("🗑️", key=f"del_sched_{real_idx}_{suffix}"):
                    st.session_state.schedule.pop(real_idx)
                    st.rerun()


# ── Tasks ─────────────────────────────────────────────────────────────────
def _render_tasks(t):
    lang  = st.session_state.lang
    prios = ["🔴 גבוהה","🟡 בינונית","🟢 נמוכה"] if lang == "he" else ["🔴 High","🟡 Medium","🟢 Low"]

    with st.expander("➕ " + ("הוסף משימה" if lang == "he" else "Add Task"), expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input(t("task_name"), key="new_task_name")
        with c2:
            prio = st.selectbox(t("task_priority"), prios, key="new_task_prio")
        due = st.date_input(t("task_due"), key="new_task_due")
        if st.button(f"✅ {t('add')}", type="primary", key="btn_add_task"):
            if name.strip():
                st.session_state.tasks.append({"name": name.strip(), "priority": prio, "due": str(due), "done": False})
                st.rerun()

    tasks   = st.session_state.tasks
    pending = [x for x in tasks if not x["done"]]
    done    = [x for x in tasks if x["done"]]

    st.markdown(
        f'<div style="color:var(--muted);margin-bottom:.8rem">'
        f'{len(pending)} {"ממתינות" if lang=="he" else "pending"} · '
        f'{len(done)} {"הושלמו" if lang=="he" else "done"}</div>',
        unsafe_allow_html=True,
    )
    for i, task in enumerate(tasks):
        c1, c2, c3, c4 = st.columns([.5, 3, 1.5, .5])
        with c1:
            new_done = st.checkbox("", value=task["done"], key=f"task_cb_{i}")
            if new_done != task["done"]:
                st.session_state.tasks[i]["done"] = new_done
                st.rerun()
        with c2:
            style = "text-decoration:line-through;color:var(--muted)" if task["done"] else ""
            st.markdown(f'<span style="{style}">{task["priority"]} {task["name"]}</span>', unsafe_allow_html=True)
        with c3:
            st.caption(task["due"])
        with c4:
            if st.button("🗑️", key=f"del_task_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()


# ── AI Summary ────────────────────────────────────────────────────────────
def _render_ai_summary(t):
    lang = st.session_state.lang
    st.markdown(
        f'<div class="sf-card sf-card-accent2" style="margin-bottom:1rem">'
        f'<b>{"מה ה-AI יעשה?" if lang=="he" else "What will the AI do?"}</b><br>'
        f'<span style="color:var(--muted);font-size:.87rem">'
        + ("יקבל את כל מערכת השעות — שיעורים, מבחנים, חוגים ואירועים אישיים — ויחזיר ניתוח עומס, המלצות איזון, ואזהרות על ימים עמוסים."
           if lang == "he" else
           "Takes your full schedule — classes, exams, activities & personal events — and returns load analysis, balance tips, and warnings about overloaded days.")
        + "</span></div>",
        unsafe_allow_html=True,
    )
    if not get_api_key():
        st.warning(t("hw_api_missing"))
        return

    if "sched_summary" not in st.session_state:
        st.session_state.sched_summary = None

    if st.button(f"🤖 {t('sched_ai_prompt')}", type="primary", key="btn_sched_ai"):
        text = _schedule_to_text(st.session_state.schedule, st.session_state.tasks, lang)
        sys  = (
            "אתה יועץ לניהול זמן לתלמידי תיכון. קיבלת מערכת שעות הכוללת שיעורים, מבחנים, חוגים ואירועים אישיים. "
            "נתח את העומס הכולל, בדוק איזון בין לימודים לחיים אישיים, תן המלצות ספציפיות, "
            "וציין ימים שנראים עמוסים מדי. ענה בעברית, קצר ומעשי."
            if lang == "he" else
            "You are a time management advisor for high school students. "
            "You received a schedule with classes, exams, clubs and personal events. "
            "Analyze the total load, check study-life balance, give specific tips, "
            "and flag overloaded days. Reply in English, concise and practical."
        )
        with st.spinner(t("hw_thinking")):
            try:
                st.session_state.sched_summary = call_gemini(
                    system_prompt=sys, user_text=text, max_tokens=1200, temperature=0.6
                )
            except Exception as e:
                st.error(f"{t('error')}: {e}")

    if st.session_state.sched_summary:
        st.markdown(
            f'<div class="sf-bubble-ai">'
            f'<div class="sf-bubble-label">{t("ai_label")}</div>'
            f'{st.session_state.sched_summary}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("clear"), key="clear_sched_sum"):
            st.session_state.sched_summary = None
            st.rerun()