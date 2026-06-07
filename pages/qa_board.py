"""pages/qa_board.py — לוח שאלות ותשובות קהילתי"""
import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from ai_utils import call_gemini, get_api_key, ddg_search
import uuid

# --- קבועים והגדרות גלובליות -------------------------------------------------

# הגדרות נושאים קבועים בעברית ובאנגלית במבנה נוח יותר
SUBJECTS = {
    "he": ["כללי", "מתמטיקה", "אנגלית", "עברית", "פיזיקה", "כימיה",
           "ביולוגיה", "היסטוריה", "ספרות", 'תנ"ך', "מדעי המחשב", "אזרחות"],
    "en": ["General", "Math", "English", "Hebrew", "Physics", "Chemistry",
           "Biology", "History", "Literature", "Bible", "CS", "Civics"]
}

# מפת צבעים לנושאים (מוגדרת פעם אחת)
SUBJECT_COLOR_MAP = {
    "מתמטיקה": "#6ee7b7", "Math": "#6ee7b7",
    "פיזיקה": "#38bdf8", "Physics": "#38bdf8",
    "כימיה": "#fb923c", "Chemistry": "#fb923c",
    "ביולוגיה": "#34d399", "Biology": "#34d399"
}

# הגדרת נתיב לקובץ אחסון נתונים קבוע
QA_FILE = "/tmp/gradeup_qa.json"

# --- פונקציות עזר לניהול נתונים ----------------------------------------------

def _load_qa() -> list:
    """
    טוען את נתוני השאלות והתשובות מקובץ JSON.
    אם הקובץ אינו קיים או שיש שגיאה בטעינה, מחזיר את נתוני ברירת המחדל.
    :return: רשימת מילונים המייצגים שאלות ותשובות.
    """
    if os.path.exists(QA_FILE):
        try:
            with open(QA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            st.error(f"שגיאה בקריאת קובץ נתונים (JSON Error): {e}")
        except Exception as e:
            st.error(f"שגיאה בטעינת נתונים: {e}")
    return _default_qa()


def _save_qa(data: list):
    """
    שומר את נתוני השאלות והתשובות לקובץ JSON.
    :param data: רשימת מילונים המייצגים שאלות ותשובות לשמירה.
    """
    try:
        with open(QA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"שגיאה בשמירת נתונים: {e}")


def _default_qa() -> list:
    """
    מחזיר רשימת שאלות ותשובות לדוגמה כברירת מחדל.
    :return: רשימת מילונים של שאלות ותשובות.
    """
    return [
        {
            "id": "q1",
            "subject": "מתמטיקה",
            "question": "איך פותרים משוואה ריבועית עם הנוסחה?",
            "asked_by": "תלמיד_א",
            "date": "01/06/2025",
            "upvotes": 4,
            "answers": [
                {"by": "תלמיד_ב", "text": "x = (-b ± √(b²-4ac)) / 2a — תציב את המקדמים ותחשב", "upvotes": 3, "is_ai": False},
            ]
        },
        {
            "id": "q2",
            "subject": "פיזיקה",
            "question": "מה ההבדל בין מהירות לתאוצה?",
            "asked_by": "תלמיד_ג",
            "date": "02/06/2025",
            "upvotes": 2,
            "answers": []
        },
    ]


# --- פונקציות עזר לרינדור רכיבים ---------------------------------------------

def _get_localized_text(lang: str, he_text: str, en_text: str) -> str:
    """מחזירה טקסט מתורגם בהתאם לשפה."""
    return he_text if lang == "he" else en_text


def _render_stat_card(col, number, label):
    """מרנדר כרטיס סטטיסטיקה בודד."""
    with col:
        st.markdown(
            f'<div class="sf-stat"><div class="sf-stat-num" style="font-size:1.1rem">{number}</div>'
            f'<div class="sf-stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )


def _render_answer_card(t, ans: dict):
    """מרנדר כרטיס תשובה בודד."""
    ai_style = "border-color:var(--accent)" if ans.get("is_ai") else ""
    label    = t("ai_label") if ans.get("is_ai") else f"👤 {ans['by']}"
    st.markdown(
        f'<div class="sf-card" style="padding:.9rem;margin-bottom:.5rem;{ai_style}">'
        f'<div class="sf-bubble-label">{label}</div>'
        f'<div style="font-size:.9rem">{ans["text"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# --- פונקציית רינדור ראשית --------------------------------------------------

def render(t):
    """
    פונקציית הרינדור הראשית של לוח השאלות והתשובות.
    מאתחלת את הנתונים, יוצרת לשוניות ומציגה את התוכן המתאים.
    :param t: פונקציית תרגום (למשל, מתרגם מחרוזות).
    """
    lang = st.session_state.lang
    st.markdown(f'<div class="sf-section-title">{t("qa_title")}</div>', unsafe_allow_html=True)

    if "qa_data" not in st.session_state:
        st.session_state.qa_data = _load_qa()

    tab_feed, tab_ask, tab_my = st.tabs([
        t("qa_tab_feed"),
        t("qa_tab_ask"),
        t("qa_tab_my"),
    ])

    with tab_feed: _render_feed(t, lang)
    with tab_ask:  _render_ask(t, lang)
    with tab_my:   _render_my(t, lang)


# --- לשונית פיד שאלות -------------------------------------------------------

def _render_feed(t, lang):
    """
    מרנדר את לשונית "פיד" המציגה את כל השאלות עם אפשרויות סינון ומיון.
    :param t: פונקציית תרגום.
    :param lang: שפת הממשק.
    """
    qa = st.session_state.qa_data
    subjects_list = SUBJECTS[lang]

    col_f, col_sort = st.columns([3, 1])
    with col_f:
        filter_subj = st.selectbox(
            t("qa_subject"),
            [_get_localized_text(lang, "הכל", "All")] + subjects_list,
            key="qa_filter_subj"
        )
    with col_sort:
        sort_by = st.selectbox(
            _get_localized_text(lang, "מיין", "Sort"),
            [_get_localized_text(lang, "חדש", "New"), _get_localized_text(lang, "פופולרי", "Popular")],
            key="qa_sort"
        )

    # סינון
    filtered = qa if filter_subj in ("הכל", "All") else [q for q in qa if q["subject"] == filter_subj]

    # מיון
    if sort_by in ("פופולרי", "Popular"):
        filtered = sorted(filtered, key=lambda x: x["upvotes"], reverse=True)
    else: # "חדש"
        filtered = sorted(filtered, key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True)

    if not filtered:
        st.info(t("qa_no_q"))
        return

    # סטטיסטיקות
    df = pd.DataFrame(qa)
    if not df.empty and "subject" in df.columns and not df["subject"].empty:
        top_subj = df["subject"].value_counts().index[0]
        total_ans = sum(len(q["answers"]) for q in qa)

        c1, c2, c3 = st.columns(3)
        _render_stat_card(c1, len(qa), _get_localized_text(lang, "שאלות", "Questions"))
        _render_stat_card(c2, total_ans, _get_localized_text(lang, "תשובות", "Answers"))
        _render_stat_card(c3, top_subj, _get_localized_text(lang, "מקצוע מוביל", "Top subject"))
        st.markdown("<br>", unsafe_allow_html=True)

    for q in filtered:
        _render_question(t, lang, q)


def _render_question(t, lang, q: dict):
    """
    מרנדר שאלה בודדת יחד עם תשובותיה, אפשרויות הצבעה והוספת תשובה.
    :param t: פונקציית תרגום.
    :param lang: שפת הממשק.
    :param q: מילון המייצג את השאלה.
    """
    ans_count = len(q["answers"])
    badge_col = SUBJECT_COLOR_MAP.get(q["subject"], "#a78bfa")

    with st.expander(
        f'[{q["subject"]}] {q["question"][:80]}{"…" if len(q["question"]) > 80 else ""}  '
        f'│ {ans_count} {t("qa_answers")} │ 👍 {q["upvotes"]}',
        expanded=False
    ):
        st.markdown(
            f'<div class="sf-card" style="padding:1rem;border-color:{badge_col}33">'
            f'<div style="font-size:1rem;font-weight:700">{q["question"]}</div>'
            f'<div style="color:var(--muted);font-size:.78rem;margin-top:.4rem">'
            f'{t("qa_asked_by")} {q["asked_by"]} · {q["date"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_up, _ = st.columns([1, 5])
        with col_up:
            if st.button(f"👍 {q['upvotes']}", key=f"upvote_q_{q['id']}"):
                q["upvotes"] += 1
                _save_qa(st.session_state.qa_data)
                st.rerun()

        if q["answers"]:
            st.markdown(f'<div style="color:var(--muted);font-size:.82rem;margin:.6rem 0">'
                        f'{_get_localized_text(lang, "תשובות:", "Answers:")}</div>', unsafe_allow_html=True)

        for j, ans in enumerate(q["answers"]):
            _render_answer_card(t, ans)
            col_a1, _ = st.columns([1, 5])
            with col_a1:
                if st.button(f"👍 {ans['upvotes']}", key=f"upvote_a_{q['id']}_{j}"):
                    ans["upvotes"] += 1
                    _save_qa(st.session_state.qa_data)
                    st.rerun()

        _render_add_answer_section(t, lang, q)


def _render_add_answer_section(t, lang, q: dict):
    """מרנדר את האזור להוספת תשובה לשאלה נתונה."""
    username = st.session_state.get("user", {}).get("username", "אנונימי")
    new_ans = st.text_area(t("qa_answer"), key=f"ans_text_{q['id']}", height=70)

    ca, cb = st.columns(2)
    with ca:
        if st.button(t("qa_submit_ans"), key=f"submit_ans_{q['id']}"):
            if new_ans.strip():
                q["answers"].append({"by": username, "text": new_ans.strip(), "upvotes": 0, "is_ai": False})
                _save_qa(st.session_state.qa_data)
                st.rerun()
    with cb:
        if st.button(t("qa_get_ai"), key=f"ai_ans_{q['id']}"):
            if not get_api_key():
                st.warning(t("hw_api_missing"))
            else:
                with st.spinner("🤖…"):
                    sys_prompt = (
                        f"אתה עוזר לתלמיד תיכון. מקצוע: {q['subject']}. "
                        "ענה בצורה ברורה, עם דוגמה אם רלוונטי. קצר ומעשי. ענה בעברית."
                        if lang == "he" else
                        f"You help a high school student. Subject: {q['subject']}. "
                        "Answer clearly with an example if relevant. Short and practical."
                    )
                    try:
                        ai_text = call_gemini(system_prompt=sys_prompt, user_text=q["question"], max_tokens=600)
                        q["answers"].append({"by": "Gradeup AI", "text": ai_text, "upvotes": 0, "is_ai": True})
                        _save_qa(st.session_state.qa_data)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))


# --- לשונית שאל שאלה --------------------------------------------------------

def _render_ask(t, lang):
    """
    מרנדר את לשונית "שאל שאלה" המאפשרת למשתמש לפרסם שאלה חדשה.
    :param t: פונקציית תרגום.
    :param lang: שפת הממשק.
    """
    subjects_list = SUBJECTS[lang]
    username = st.session_state.get("user", {}).get("username", "אנונימי")

    st.markdown(
        f'<div class="sf-section-title">{_get_localized_text(lang, "שאל את הקהילה", "Ask the Community")}</div>',
        unsafe_allow_html=True,
    )

    subj = st.selectbox(t("qa_subject"), subjects_list, key="qa_ask_subj")
    q    = st.text_area(
        t("qa_question"), height=100,
        placeholder=_get_localized_text(lang, "הסבר בבקשה איך…", "Can someone explain how…"),
        key="qa_ask_text"
    )

    use_ddg = st.toggle(
        "🔍 " + _get_localized_text(lang, "חפש קודם ב-DuckDuckGo", "Search DuckDuckGo first"),
        key="qa_ddg"
    )

    if st.button(t("qa_post"), type="primary", key="qa_post_btn"):
        if not q.strip():
            st.error(_get_localized_text(lang, "כתוב שאלה", "Write a question"))
            return

        ddg_results = []
        if use_ddg:
            with st.spinner("🔍 DuckDuckGo…"):
                ddg_results = ddg_search(f"{subj} {q}", max_results=3)
            if ddg_results:
                st.markdown(f'<div class="sf-section-title">{_get_localized_text(lang, "תוצאות חיפוש", "Search results")}</div>', unsafe_allow_html=True)
                for r in ddg_results:
                    st.markdown(
                        f'<div class="sf-card" style="padding:.8rem;margin-bottom:.4rem">'
                        f'<b>{r.get("title","")}</b><br>'
                        f'<span style="color:var(--muted);font-size:.83rem">{r.get("body","")[:180]}…</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown("<br>", unsafe_allow_html=True) # רווח אחרי תוצאות חיפוש

        new_q = {
            "id":       str(uuid.uuid4())[:8],
            "subject":  subj,
            "question": q.strip(),
            "asked_by": username,
            "date":     datetime.now().strftime("%d/%m/%Y"),
            "upvotes":  0,
            "answers":  [],
        }
        st.session_state.qa_data.append(new_q)
        _save_qa(st.session_state.qa_data)
        st.success("✅ " + _get_localized_text(lang, "שאלה פורסמה!", "Question posted!"))
        st.rerun()


# --- לשונית השאלות שלי ------------------------------------------------------

def _render_my(t, lang):
    """
    מרנדר את לשונית "השאלות שלי" המציגה את השאלות שפורסמו על ידי המשתמש הנוכחי.
    :param t: פונקציית תרגום.
    :param lang: שפת הממשק.
    """
    username = st.session_state.get("user", {}).get("username", "")
    my_qs    = [q for q in st.session_state.qa_data if q["asked_by"] == username]

    if not my_qs:
        st.info(_get_localized_text(lang, "עדיין לא שאלת שאלות", "You haven't asked any questions yet"))
        return

    df = pd.DataFrame([{
        _get_localized_text(lang, "שאלה", "Question"): q["question"][:50]+"…",
        _get_localized_text(lang, "מקצוע", "Subject"): q["subject"],
        _get_localized_text(lang, "תשובות", "Answers"): len(q["answers"]),
        "👍": q["upvotes"],
        _get_localized_text(lang, "תאריך", "Date"): q["date"],
    } for q in my_qs])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    for q in my_qs:
        col1, col2 = st.columns([5, .5])
        with col1:
            st.markdown(
                f'<div class="sf-card" style="padding:.9rem">'
                f'<b>{q["question"]}</b>'
                f'<span class="sf-badge" style="margin-right:.5rem">{q["subject"]}</span><br>'
                f'<span style="color:var(--muted);font-size:.8rem">'
                f'{len(q["answers"])} {t("qa_answers")} · 👍 {q["upvotes"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("🗑️", key=f"del_my_q_{q['id']}"):
                st.session_state.qa_data.remove(q)
                _save_qa(st.session_state.qa_data)
                st.rerun()
