"""pages/homework.py — Homework Bot"""
import streamlit as st
from ai_utils import call_gemini, get_api_key, process_image, ddg_search

SUBJECTS_HE = ["כללי","מתמטיקה","פיזיקה","כימיה","ביולוגיה","אנגלית",
                "עברית","היסטוריה",'ספרות','תנ"ך',"מדעי המחשב","כלכלה","גיאוגרפיה"]
SUBJECTS_EN = ["General","Math","Physics","Chemistry","Biology","English",
                "Hebrew","History","Literature","Bible","Computer Sci.","Economics","Geography"]

QUICK_HE = ["הסבר את הנושא", "תן דוגמה מלאה", "שאלות תרגול", "סכם בנקודות", "מה צריך לזכור למבחן?"]
QUICK_EN = ["Explain the topic", "Full example", "Practice questions", "Summarize in points", "Key exam facts?"]


def _sys_prompt(subject: str, mode: str, lang: str) -> str:
    if lang == "he":
        return (
            f"אתה עוזר שיעורי בית חכם לתלמידי תיכון. מקצוע: {subject}. "
            f"סגנון עזרה: {mode}. "
            "הסבר בצורה ברורה, שלב אחר שלב. "
            "אם יש תמונה — נתח אותה וענה על מה שרואים. "
            "אם קיבלת תוצאות חיפוש — השתמש בהן אך כתוב בשפתך. "
            "ענה תמיד בעברית."
        )
    return (
        f"You are a smart homework assistant for high school students. Subject: {subject}. "
        f"Help mode: {mode}. "
        "Explain clearly, step by step. "
        "If there is an image — analyze it and answer based on what you see. "
        "If you got search results — use them but write in your own words. "
        "Always reply in English."
    )


def render(t):
    st.markdown(f'<div class="sf-section-title">{t("hw_title")}</div>', unsafe_allow_html=True)

    if not get_api_key():
        st.warning(t("hw_api_missing"))
        st.info(
            "⚙️ " + ("פתח את 'הגדרות' בתפריט הצדדי והזן Gemini API Key חינמי מ-aistudio.google.com"
                     if st.session_state.lang == "he"
                     else "Open 'Settings' in the sidebar and enter a free Gemini API Key from aistudio.google.com")
        )
        return

    lang = st.session_state.lang

    # ── Controls row ─────────────────────────────────────────────
    c_subj, c_mode, c_ddg = st.columns([2, 2, 1])
    with c_subj:
        subjects = SUBJECTS_HE if lang == "he" else SUBJECTS_EN
        subject  = st.selectbox(t("hw_subject"), subjects, key="hw_subject")
    with c_mode:
        modes_he = ["הסבר נושא", "עזור לפתור", "סכם חומר", "שאלות מבחן"]
        modes_en = ["Explain topic", "Help solve", "Summarize", "Exam questions"]
        modes    = modes_he if lang == "he" else modes_en
        mode     = st.selectbox(t("hw_mode"), modes, key="hw_mode")
    with c_ddg:
        use_ddg = st.toggle(t("hw_search_toggle"), value=False, key="hw_ddg")

    # ── Image upload ─────────────────────────────────────────────
    uploaded = st.file_uploader(
        t("hw_image_upload"),
        type=["png", "jpg", "jpeg", "webp", "bmp"],
        key="hw_img",
    )
    pil_image = process_image(uploaded)
    if pil_image:
        col_i, col_info = st.columns([1, 2])
        with col_i:
            st.image(pil_image, use_container_width=True)
        with col_info:
            st.markdown(
                f'<div class="sf-card" style="padding:.9rem">'
                f'<b>Pillow</b> {"עיבד:" if lang=="he" else "processed:"}<br>'
                f'<span style="color:var(--muted);font-size:.85rem">'
                f'{pil_image.size[0]}×{pil_image.size[1]}px · {pil_image.mode}</span></div>',
                unsafe_allow_html=True,
            )

    # ── Chat history ─────────────────────────────────────────────
    if "hw_chat" not in st.session_state:
        st.session_state.hw_chat = []

    with st.container():
        if not st.session_state.hw_chat:
            st.markdown(
                f'<div class="sf-card" style="text-align:center;padding:2rem">'
                f'<div style="font-size:2.5rem">📚</div>'
                f'<div style="font-weight:700;margin:.5rem 0">{t("hw_welcome")}</div>'
                f'<div style="color:var(--muted);font-size:.88rem">'
                + ("בחר מקצוע, העלה תמונה אם יש, והפעל DuckDuckGo לתוצאות עדכניות"
                   if lang == "he" else
                   "Choose a subject, upload an image if needed, and enable DuckDuckGo for fresh results")
                + "</div></div>",
                unsafe_allow_html=True,
            )

        for msg in st.session_state.hw_chat:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="sf-bubble-user">'
                    f'<div class="sf-bubble-label">{t("you")}</div>'
                    f'{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            elif msg["role"] == "search":
                with st.expander(f'🔍 DuckDuckGo — {msg["query"]}'):
                    for r in msg["results"]:
                        st.markdown(
                            f'**{r.get("title","")}**  \n'
                            f'{r.get("body","")[:200]}…  \n'
                            f'[🔗]({r.get("href","")})'
                        )
            else:
                st.markdown(
                    f'<div class="sf-bubble-ai">'
                    f'<div class="sf-bubble-label">{t("ai_label")}</div>'
                    f'{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

    # ── Quick prompts ─────────────────────────────────────────────
    quick = QUICK_HE if lang == "he" else QUICK_EN
    st.markdown(
        f'<div style="color:var(--muted);font-size:.82rem;margin:.7rem 0 .35rem">'
        f'{"שאלות מהירות:" if lang=="he" else "Quick prompts:"}</div>',
        unsafe_allow_html=True,
    )
    qcols = st.columns(len(quick))
    for i, (col, q) in enumerate(zip(qcols, quick)):
        with col:
            if st.button(q, key=f"hw_quick_{i}", use_container_width=True):
                st.session_state._hw_quick = q

    # ── Input ─────────────────────────────────────────────────────
    user_input = st.chat_input(t("hw_placeholder"))
    if hasattr(st.session_state, "_hw_quick"):
        user_input = st.session_state._hw_quick
        del st.session_state._hw_quick

    if user_input:
        st.session_state.hw_chat.append({"role": "user", "content": user_input})
        search_results = None

        with st.spinner(t("hw_thinking")):
            # DuckDuckGo
            if use_ddg:
                q = f"{subject} {user_input}"
                search_results = ddg_search(q, max_results=4)
                if search_results:
                    st.session_state.hw_chat.append({
                        "role": "search", "query": q, "results": search_results
                    })

            # Gemini
            try:
                history = [m for m in st.session_state.hw_chat if m["role"] in ("user", "assistant")]
                reply   = call_gemini(
                    system_prompt=_sys_prompt(subject, mode, lang),
                    user_text=user_input,
                    history=history,
                    image=pil_image,
                    search_results=search_results,
                    max_tokens=1400,
                )
                st.session_state.hw_chat.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"{t('error')}: {e}")

        st.rerun()

    # ── Clear ─────────────────────────────────────────────────────
    if st.session_state.hw_chat:
        if st.button(t("hw_clear"), key="hw_clear_btn"):
            st.session_state.hw_chat = []
            st.rerun()