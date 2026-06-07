"""pages/translator.py — מתרגם חכם + דקדוק + שמירה לכרטיסיות + pandas היסטוריה"""
import streamlit as st
import pandas as pd
from datetime import datetime
from ai_utils import call_gemini, get_api_key



LANGS_HE = ["עברית","אנגלית","ערבית","צרפתית","ספרדית","רוסית","גרמנית","איטלקית","יפנית","סינית"]
LANGS_EN = ["Hebrew","English","Arabic","French","Spanish","Russian","German","Italian","Japanese","Chinese"]

LANG_MAP = dict(zip(LANGS_HE, LANGS_EN)) | dict(zip(LANGS_EN, LANGS_EN))


def render(t):
    lang = st.session_state.lang
    he   = lang == "he"
    st.markdown(
        '<div class="section-title">🌍 ' +
        ("מתרגם חכם" if he else "Smart Translator") +
        '</div>',
        unsafe_allow_html=True,
    )

    if "tr_history" not in st.session_state: st.session_state.tr_history = []
    if "tr_result"  not in st.session_state: st.session_state.tr_result  = None

    tab_tr, tab_hist = st.tabs([
        "🔄 " + ("תרגום" if he else "Translate"),
        "📚 " + ("היסטוריה" if he else "History"),
    ])

    with tab_tr:   _translate(he)
    with tab_hist: _history(he)


# ── Translate ─────────────────────────────────────────────────────────────
def _translate(he):
    langs = LANGS_HE if he else LANGS_EN

    if not get_api_key():
        st.warning("Gemini API Key required — add it in the sidebar settings")
        return

    # Language pair
    c1, mid, c2 = st.columns([2, .35, 2])
    with c1:
        from_lang = st.selectbox("משפה" if he else "From", langs, index=0, key="tr_from")
    with mid:
        st.markdown('<div style="text-align:center;padding-top:1.9rem;font-size:1.5rem;color:var(--muted)">→</div>', unsafe_allow_html=True)
    with c2:
        to_lang = st.selectbox("לשפה" if he else "To", langs, index=1, key="tr_to")

    # Text input
    text_in = st.text_area(
        "טקסט לתרגום" if he else "Text to translate",
        height=120,
        placeholder="הכנס טקסט כאן…" if he else "Enter text here…",
        key="tr_text_inp"
    )
    char_count = len(text_in)
    st.markdown(
        f'<div style="color:var(--muted);font-size:.78rem;text-align:left">{char_count} chars</div>',
        unsafe_allow_html=True,
    )

    # Options
    col_a, col_b, col_c = st.columns(3)
    with col_a: show_grammar  = st.toggle("📖 " + ("דקדוק"   if he else "Grammar"),  value=True,  key="tr_gram")
    with col_b: show_examples = st.toggle("💬 " + ("דוגמאות" if he else "Examples"), value=True,  key="tr_ex")
    with col_c: formal        = st.toggle("🎩 " + ("פורמלי"  if he else "Formal"),   value=False, key="tr_form")

    if st.button("🔄 " + ("תרגם" if he else "Translate"), type="primary", use_container_width=True, key="tr_go"):
        if not text_in.strip():
            st.error("הכנס טקסט" if he else "Enter some text"); return

        from_en = LANG_MAP.get(from_lang, from_lang)
        to_en   = LANG_MAP.get(to_lang,   to_lang)
        tone    = "formal/academic" if formal else "natural/conversational"

        sections = ["**Translation:**\n[translation here]"]
        if show_grammar:  sections.append("**Grammar note:**\n[brief grammar/structure explanation]")
        if show_examples: sections.append("**Usage examples:**\n[2-3 natural examples]")

        sys = (
            f"You are a professional translator and language teacher. "
            f"Translate from {from_en} to {to_en}. Tone: {tone}. "
            f"Return your response in these sections:\n\n"
            + "\n\n".join(sections)
            + "\n\nReply explanations in "
            + ("Hebrew" if he else "English")
            + " but the actual translation in the target language."
        )

        with st.spinner("🔄 " + ("מתרגם…" if he else "Translating…")):
            try:
                result = call_gemini(
                    system_prompt=sys,
                    user_text=text_in.strip(),
                    max_tokens=700, temperature=0.3,
                )
                entry = {
                    "from": from_lang, "to": to_lang,
                    "input": text_in.strip(),
                    "output": result,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                }
                st.session_state.tr_result = entry
                st.session_state.tr_history.insert(0, entry)
            except Exception as e:
                st.error(str(e))

    # Result
    res = st.session_state.tr_result
    if res:
        st.markdown(
            f'<div class="bubble-ai" style="margin-top:1rem">'
            f'<div class="bubble-label">'
            f'🌍 {res["from"]} → {res["to"]}</div>'
            f'{res["output"].replace(chr(10), "<br>")}'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_fc, col_clr = st.columns(2)
        with col_fc:
            if st.button("🃏 " + ("שמור ככרטיסייה" if he else "Save as flashcard"), key="tr_to_fc"):
                if "fc_decks" not in st.session_state:
                    st.session_state.fc_decks = {}
                deck = f"{res['from']} → {res['to']}"
                # Extract translation line
                lines = res["output"].split("\n")
                trans_line = next(
                    (l for l in lines if l.strip() and not l.startswith("**")),
                    res["output"][:100]
                )
                st.session_state.fc_decks.setdefault(deck, []).append({
                    "q": res["input"],
                    "a": trans_line.strip(),
                })
                st.success(f"✅ {deck}")
        with col_clr:
            if st.button("🗑️ " + ("נקה" if he else "Clear"), key="tr_clr"):
                st.session_state.tr_result = None; st.rerun()


# ── History (pandas) ──────────────────────────────────────────────────────
def _history(he):
    history = st.session_state.tr_history
    if not history:
        st.info("אין תרגומים עדיין" if he else "No translations yet")
        return

    df = pd.DataFrame([{
        ("משפה"  if he else "From"):   h["from"],
        ("לשפה"  if he else "To"):     h["to"],
        ("טקסט"  if he else "Text"):   h["input"][:45] + ("…" if len(h["input"])>45 else ""),
        ("תאריך" if he else "Date"):   h["date"],
    } for h in history])

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat"><div class="stat-num">{len(history)}</div><div class="stat-label">{"תרגומים" if he else "Translations"}</div></div>', unsafe_allow_html=True)
    with c2:
        top_pair = df.groupby([("משפה" if he else "From"),("לשפה" if he else "To")]).size().idxmax() if len(df)>0 else ("?","?")
        st.markdown(f'<div class="stat"><div class="stat-num" style="font-size:.9rem">{top_pair[0]}→{top_pair[1]}</div><div class="stat-label">{"שכיח" if he else "Most common"}</div></div>', unsafe_allow_html=True)
    with c3:
        avg_len = int(pd.Series([len(h["input"]) for h in history]).mean())
        st.markdown(f'<div class="stat"><div class="stat-num">{avg_len}</div><div class="stat-label">{"ממוצע תווים" if he else "Avg chars"}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSV", csv, "gradeup_translations.csv", "text/csv", key="tr_csv"
    )

    st.markdown("---")
    for i, h in enumerate(history[:15]):
        with st.expander(f"🌍 {h['from']} → {h['to']}  ·  {h['input'][:40]}…  ·  {h['date']}"):
            st.markdown(
                f'<div class="card" style="padding:.85rem">'
                f'<b style="color:var(--muted)">{"קלט" if he else "Input"}:</b> {h["input"]}<br><br>'
                f'{h["output"].replace(chr(10),"<br>")}</div>',
                unsafe_allow_html=True,
            )