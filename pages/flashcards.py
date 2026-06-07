"""pages/flashcards.py — כרטיסיות לימוד + AI מייצר"""
import streamlit as st
import json
import random
from ai_utils import call_gemini, get_api_key
from translations import t

# הגדרת נושאים קבועים בעברית ובאנגלית
SUBJECTS_HE = ["כללי","מתמטיקה","אנגלית","עברית","פיזיקה","כימיה",
                "ביולוגיה","היסטוריה","ספרות",'תנ"ך',"מדעי המחשב","אזרחות"]
SUBJECTS_EN = ["General","Math","English","Hebrew","Physics","Chemistry",
                "Biology","History","Literature","Bible","CS","Civics"]

def _init():
    """
    אתחול משתני session state של Streamlit אם הם לא קיימים.
    זה מבטיח שהאפליקציה תתחיל עם מצב ברירת מחדל.
    """
    if "fc_decks"   not in st.session_state: st.session_state.fc_decks   = _default_decks()
    if "fc_idx"     not in st.session_state: st.session_state.fc_idx     = 0
    if "fc_flipped" not in st.session_state: st.session_state.fc_flipped = False
    if "fc_knew"    not in st.session_state: st.session_state.fc_knew    = 0
    if "fc_missed"  not in st.session_state: st.session_state.fc_missed  = 0
    if "fc_deck_sel"not in st.session_state: st.session_state.fc_deck_sel= "כללי"
    if "fc_order"   not in st.session_state: st.session_state.fc_order   = []

def _default_decks():
    """
    מחזיר את מבנה הנתונים של חפיסות קלפים ברירת מחדל.
    """
    return {
        "כללי": [
            {"q": "מהי הנוסחה לשטח מעגל?",        "a": "π × r²"},
            {"q": "מהו מספר אבוגדרו?",              "a": "6.022 × 10²³"},
            {"q": "מתי הייתה מלחמת העולם הראשונה?", "a": "1914–1918"},
            {"q": "מה פירוש המילה 'Democracy'?",    "a": "שלטון העם — שיטת ממשל שבה האזרחים בוחרים נציגים"},
        ]
    }

def _current_deck(lang):
    """
    מחזיר את החפיסה הנבחרת הנוכחית.
    """
    decks = st.session_state.fc_decks
    sel   = st.session_state.fc_deck_sel
    return decks.get(sel, [])

def _reset_study():
    """
    מאפס את מצב הלמידה הנוכחי - מערבב את סדר הקלפים ומוודא שהם לא הפוכים.
    """
    cards = _current_deck(st.session_state.lang)
    order = list(range(len(cards)))
    random.shuffle(order)
    st.session_state.fc_order   = order
    st.session_state.fc_idx     = 0
    st.session_state.fc_flipped = False
    st.session_state.fc_knew    = 0
    st.session_state.fc_missed  = 0

def render(t):
    """
    פונקציית הרינדור הראשית של עמוד הכרטיסיות.
    מאתחלת את המצב, מציגה את הכותרת הראשית ומארגנת את הלשוניות השונות.
    :param t: פונקציית תרגום (למשל, מתרגם מחרוזות).
    """
    lang = st.session_state.lang
    _init()

    # עיצוב כותרת ראשית באמצעות HTML
    st.markdown(f'<div class="sf-section-title">{t("fc_title")}</div>', unsafe_allow_html=True)

    # יצירת לשוניות לניווט בין מצבי האפליקציה השונים
    tab_study, tab_create, tab_ai, tab_manage = st.tabs([
        t("fc_tab_study"), t("fc_tab_create"), t("fc_tab_ai"), t("fc_tab_manage")
    ])

    # הצגת התוכן של כל לשונית באמצעות פונקציות עזר
    with tab_study:   _render_study(t, lang)
    with tab_create:  _render_create(t, lang)
    with tab_ai:      _render_ai_gen(t, lang)
    with tab_manage:  _render_manage(t, lang)


# ── מצב לימוד ────────────────────────────────────────────────────────────
def _render_study(t, lang):
    """
    מרנדר את ממשק המשתמש עבור מצב הלימוד של כרטיסיות.
    """
    decks   = st.session_state.fc_decks
    deck_names = list(decks.keys())

    # אם אין חפיסות קלפים, הצג הודעה מתאימה
    if not deck_names:
        st.info(t("fc_no_cards"))
        return

    # עמודות לבחירת חפיסה וכפתור ערבוב
    col_sel, col_shuffle = st.columns([3, 1])
    with col_sel:
        # בחירת החפיסה
        sel = st.selectbox(
            t("fc_subject"), deck_names, key="fc_deck_select",
            index=deck_names.index(st.session_state.fc_deck_sel)
            if st.session_state.fc_deck_sel in deck_names else 0
        )
        # אם נבחרה חפיסה אחרת, עדכן את המצב ואתחל את הלמידה
        if sel != st.session_state.fc_deck_sel:
            st.session_state.fc_deck_sel = sel
            _reset_study()
            st.rerun()
    with col_shuffle:
        # כפתור ערבוב הכרטיסיות
        if st.button("🔀 " + ("ערבב" if lang=="he" else "Shuffle"), use_container_width=True):
            _reset_study()
            st.rerun()

    cards = decks.get(st.session_state.fc_deck_sel, [])
    # אם החפיסה שנבחרה ריקה, הצג הודעה
    if not cards:
        st.info(t("fc_no_cards"))
        return

    # אתחול סדר הקלפים אם הוא לא קיים
    if not st.session_state.fc_order:
        _reset_study()

    order = st.session_state.fc_order
    idx   = st.session_state.fc_idx

    # ── סיום הלמידה ──────────────────────────────────────────────────
    if idx >= len(order):
        total  = st.session_state.fc_knew + st.session_state.fc_missed
        pct    = int(st.session_state.fc_knew / total * 100) if total else 0
        # קביעת צבע התוצאה בהתאם לאחוז ההצלחה
        color  = "#6ee7b7" if pct >= 70 else "#facc15" if pct >= 50 else "#f87171"
        # הצגת סיכום הלמידה
        st.markdown(
            f'<div class="sf-card" style="text-align:center;padding:2.5rem;border-color:{color}">'
            f'<div style="font-size:3rem">🎉</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{color};margin:.5rem 0">{t("fc_done")}</div>'
            f'<div style="font-size:2rem;font-weight:700;color:{color}">{pct}%</div>'
            f'<div style="color:var(--muted)">{t("fc_score")}: {st.session_state.fc_knew}/{total}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # כפתור להתחלת למידה מחדש
        if st.button(t("fc_restart"), type="primary", use_container_width=True):
            _reset_study()
            st.rerun()
        return

    card = cards[order[idx]]

    # פס התקדמות
    progress = idx / len(order)
    st.markdown(
        f'<div style="background:#1e2a3d;border-radius:99px;height:6px;margin-bottom:1rem">'
        f'<div style="background:#6ee7b7;width:{progress*100:.0f}%;height:100%;border-radius:99px;transition:width .3s"></div>'
        f'</div>'
        f'<div style="color:var(--muted);font-size:.82rem;text-align:left">'
        f'{idx+1} / {len(order)} {t("fc_card_count")}</div>',
        unsafe_allow_html=True,
    )

    # הצגת הכרטיסיה (שאלה או תשובה)
    flipped = st.session_state.fc_flipped
    face_content = card["a"] if flipped else card["q"]
    face_label   = t("fc_answer") if flipped else t("fc_question")
    face_color   = "#38bdf8" if flipped else "#6ee7b7"
    face_bg      = "#0a2e4022" if flipped else "#04352822"

    # עיצוב הכרטיסיה עצמה
    st.markdown(
        f'<div class="sf-card" style="background:{face_bg};border-color:{face_color};'
        f'padding:2.5rem;text-align:center;min-height:180px;'
        f'display:flex;flex-direction:column;justify-content:center;cursor:pointer">'
        f'<div style="font-size:.78rem;color:{face_color};font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem">{face_label}</div>'
        f'<div style="font-size:1.25rem;font-weight:600;color:#e8edf5;line-height:1.6">{face_content}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # כפתורים לפעולות: היפוך, סימון "ידעתי" או "לא ידעתי"
    col_flip, col_knew, col_miss = st.columns([2, 1, 1])
    with col_flip:
        if st.button(t("fc_flip"), use_container_width=True, key="fc_flip_btn"):
            st.session_state.fc_flipped = not st.session_state.fc_flipped
            st.rerun()
    with col_knew:
        if st.button(t("fc_knew"), use_container_width=True, type="primary", key="fc_knew_btn",
                     disabled=not flipped):
            st.session_state.fc_knew   += 1
            st.session_state.fc_idx    += 1
            st.session_state.fc_flipped = False
            st.rerun()
    with col_miss:
        if st.button(t("fc_didnt"), use_container_width=True, key="fc_miss_btn",
                     disabled=not flipped):
            # העברת הכרטיסיה לסוף התור כדי להציג אותה שוב
            order.append(order[idx])
            st.session_state.fc_missed  += 1
            st.session_state.fc_idx     += 1
            st.session_state.fc_flipped  = False
            st.rerun()

    # הצגת סטטיסטיקות נוכחיות של הלמידה
    k = st.session_state.fc_knew
    m = st.session_state.fc_missed
    if k + m > 0:
        st.markdown(
            f'<div style="display:flex;gap:1rem;margin-top:.5rem">'
            f'<span style="color:#6ee7b7;font-size:.85rem">✅ {k}</span>'
            f'<span style="color:#f87171;font-size:.85rem">❌ {m}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── יצירה ידנית ─────────────────────────────────────────────────────────
def _render_create(t, lang):
    """
    מרנדר את ממשק המשתמש ליצירה ידנית של כרטיסיות.
    """
    subjects = SUBJECTS_HE if lang == "he" else SUBJECTS_EN

    # עיצוב כותרת הלשונית
    st.markdown(
        f'<div class="sf-section-title">{"הוסף כרטיסייה" if lang=="he" else "Add Card"}</div>',
        unsafe_allow_html=True,
    )
    # שדות קלט לבחירת נושא, שאלה ותשובה
    subj = st.selectbox(t("fc_subject"), subjects, key="fc_new_subj")
    q    = st.text_input(t("fc_question"), key="fc_new_q",
                          placeholder="מהי הנוסחה ל…" if lang=="he" else "What is the formula for…")
    a    = st.text_area(t("fc_answer"), key="fc_new_a", height=80,
                         placeholder="הסבר מלא…" if lang=="he" else "Full explanation…")

    # כפתור להוספת הכרטיסיה
    if st.button(f"✅ {t('add')}", type="primary", key="fc_add_btn"):
        # בדיקה שהשאלה והתשובה אינן ריקות
        if not q.strip() or not a.strip():
            st.error("מלא שאלה ותשובה" if lang=="he" else "Fill question and answer")
        else:
            decks = st.session_state.fc_decks
            # הוספת הכרטיסיה החדשה לחפיסה המתאימה
            decks.setdefault(subj, []).append({"q": q.strip(), "a": a.strip()})
            st.success(f"✅ {t('success')}")
            st.rerun()


# ── יצירה בעזרת AI ───────────────────────────────────────────────────────────
def _render_ai_gen(t, lang):
    """
    מרנדר את ממשק המשתמש ליצירת כרטיסיות באמצעות AI.
    """
    # בדיקה אם מפתח ה-API זמין
    if not get_api_key():
        st.warning(t("hw_api_missing"))
        return

    subjects = SUBJECTS_HE if lang == "he" else SUBJECTS_EN
    # בחירת נושא
    subj = st.selectbox(t("fc_subject"), subjects, key="fc_ai_subj")
    # בחירת כמות הכרטיסיות
    count= st.slider("כמה כרטיסיות?" if lang=="he" else "How many cards?", 3, 15, 7, key="fc_count")
    # שדה קלט להדבקת טקסט מקור
    text = st.text_area(
        t("fc_ai_prompt"), height=160,
        placeholder="הדבק כאן פרק מספר לימוד, הערות שיעור, מאמר…" if lang=="he"
        else "Paste a textbook chapter, lecture notes, article…",
        key="fc_ai_text"
    )

    # כפתור ליצירת הכרטיסיות
    if st.button(t("fc_ai_generate"), type="primary", key="fc_ai_btn"):
        # בדיקה שהוזן טקסט
        if not text.strip():
            st.error("הדבק טקסט קודם" if lang=="he" else "Please paste some text first")
            return

        # הגדרת הנחיית מערכת עבור ה-AI
        sys = (
            f"אתה מייצר כרטיסיות לימוד לתלמיד תיכון. מקצוע: {subj}. "
            f"צור בדיוק {count} כרטיסיות מהטקסט. "
            "החזר JSON בלבד — מערך של אובייקטים עם שדות 'q' (שאלה) ו-'a' (תשובה). "
            "שאלות קצרות וברורות. תשובות מלאות אך תמציתיות. "
            "אל תוסיף כלום מחוץ ל-JSON."
            if lang == "he" else
            f"You generate flashcards for a high school student. Subject: {subj}. "
            f"Create exactly {count} cards from the text. "
            "Return JSON only — array of objects with 'q' (question) and 'a' (answer) fields. "
            "Short clear questions. Full but concise answers. Nothing outside the JSON."
        )

        # הצגת הודעת טעינה בזמן יצירת הכרטיסיות
        with st.spinner("🤖 " + ("מייצר כרטיסיות…" if lang=="he" else "Generating cards…")):
            try:
                # קריאה לפונקציית ה-AI
                raw = call_gemini(system_prompt=sys, user_text=text, max_tokens=2000, temperature=0.5)

                # ניקוי הפלט של ה-AI והמרתו ל-JSON
                clean = raw.strip()
                if clean.startswith("```"):
                    clean = clean.split("```")[1]
                    if clean.startswith("json"):
                        clean = clean[4:]
                cards = json.loads(clean.strip())

                # הוספת הכרטיסיות שנוצרו לחפיסה המתאימה
                decks = st.session_state.fc_decks
                decks.setdefault(subj, []).extend(cards)
                st.success(f"✅ {len(cards)} " + ("כרטיסיות נוצרו!" if lang=="he" else "cards generated!"))
                st.rerun()
            except Exception as e:
                # הצגת הודעת שגיאה אם נוצרת בעיה
                st.error(f"שגיאה: {e}" if lang=="he" else f"Error: {e}")


# ── ניהול כרטיסיות ───────────────────────────────────────────────────────────
def _render_manage(t, lang):
    """
    מרנדר את ממשק המשתמש לניהול (צפייה ומחיקה) של כרטיסיות קיימות.
    """
    decks = st.session_state.fc_decks
    # אם אין חפיסות, הצג הודעה
    if not decks:
        st.info(t("fc_no_cards"))
        return

    # מעבר על כל חפיסה והצגת הכרטיסיות שבתוכה
    for deck_name, cards in list(decks.items()):
        # שימוש ב-expander כדי לקפל/לפתוח כל חפיסה
        with st.expander(f"📚 {deck_name} — {len(cards)} {t('fc_card_count')}"):
            for i, card in enumerate(cards):
                # חלוקת השורה לשתי עמודות: אחת לכרטיסיה ואחת לכפתור מחיקה
                c1, c2 = st.columns([5, .5])
                with c1:
                    # הצגת השאלה והתשובה של הכרטיסיה
                    st.markdown(
                        f'<div style="font-size:.88rem">'
                        f'<b style="color:#6ee7b7">Q:</b> {card["q"]}<br>'
                        f'<b style="color:#38bdf8">A:</b> {card["a"]}</div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    # כפתור מחיקה לכל כרטיסיה
                    if st.button("🗑️", key=f"del_card_{deck_name}_{i}"):
                        # הסרת הכרטיסיה מהחפיסה
                        decks[deck_name].pop(i)
                        # אם החפיסה נהיית ריקה, מחק אותה לגמרי
                        if not decks[deck_name]:
                            del decks[deck_name]
                        st.rerun()
