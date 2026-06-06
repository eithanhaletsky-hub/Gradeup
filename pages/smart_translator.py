import streamlit as st
import google as genai
from ddgs import DDGS

# ודא ש-get_api_key מוגדרת להחזיר את מפתח ה-API שלך
# from ai_utils import get_api_key
# API_KEY = get_api_key()
# genai.configure(api_key=API_KEY)

def render_smart_translator(t):
    st.markdown(
        f'<div class="sf-section-title">{t("smart_translator_title")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-subtitle">{t("languages")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-description">{t("smart_translator_description")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="sf-libraries-title">{t("libraries")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">google-genai</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">ddgs</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">📚 שיעורי בית</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🃏 כרטיסיות</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-features-title">{t("features")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("translator_grammar_explanation")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("translator_contextual_examples")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("translator_save_to_flashcards")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("translator_he_to_multi_lang")}</div>', unsafe_allow_html=True)

    # --- לוגיקת המתרגם החכם ---
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("translator_main_title")}</div>', unsafe_allow_html=True)

    source_text = st.text_area(t("translator_enter_text"), key="translator_source_text", height=150)

    c1, c2 = st.columns(2)
    with c1:
        source_lang = st.selectbox(t("translator_source_lang"), ["עברית", "אנגלית", "ערבית", "צרפתית"], key="translator_source_lang_select")
    with c2:
        target_lang = st.selectbox(t("translator_target_lang"), ["אנגלית", "עברית", "ערבית", "צרפתית"], key="translator_target_lang_select")

    if "translated_output" not in st.session_state:
        st.session_state.translated_output = None

    if st.button(t("translator_translate_btn"), key="translate_btn"):
        if not source_text:
            st.warning(t("translator_enter_text_warning"))
        elif source_lang == target_lang:
            st.warning(t("translator_same_language_warning"))
        else:
            # --- שימוש ב-Gemini לתרגום והסברים ---
            # ודא שמפתח ה-API מוגדר
            # if 'API_KEY' not in locals() or not API_KEY:
            #     st.warning(t("gemini_api_key_missing_translator"))
            #     return

            translation_prompt = f"""
            תרגם את הטקסט הבא מ'{source_lang}' ל'{target_lang}'.
            בנוסף לתרגום, ספק:
            1. הסבר דקדוקי קצר על מבנה המשפט או מילים מיוחדות.
            2. דוגמה נוספת לשימוש במילים או בביטויים מהתרגום בהקשר אחר.
            3. הסבר למה בחרת את התרגום הספציפי והצע חלופות במידת הצורך.
            4. ציין רמת קושי של הטקסט המקורי (קל, בינוני, קשה).

            הטקסט לתרגום:
            '''
            {source_text}
            '''
            ענה בעברית.
            """

            with st.spinner(t("translator_translating")):
                try:
                    # model = genai.GenerativeModel('gemini-1.5-flash')
                    # response = model.generate_content(translation_prompt, generation_config={"temperature": 0.4})
                    # ai_translation = response.text

                    # הדמיית פלט AI ללא API KEY
                    ai_translation = f"""
                    ## תרגום:
                    **הטקסט המקורי:** "{source_text}"
                    **התרגום ל{target_lang}:** "This is a translated example text." (זוהי דוגמת טקסט מתורגמת.)

                    ---

                    ### הסבר דקדוקי:
                    המילה "This" היא כינוי רמז, ו"is" הוא פועל עזר. המבנה הוא נושא-פועל-משלים.

                    ### דוגמאות בהקשר:
                    *   "This **is** my book." (זה הספר שלי.)
                    *   "The example text **is** very clear." (טקסט הדוגמה מאוד ברור.)

                    ### בחירת תרגום וחלופות:
                    בחרתי בתרגום הישיר ביותר כדי לשמור על הפשטות. חלופה יכולה להיות "Here is a translated example." (הנה דוגמה מתורגמת), אם רוצים להדגיש הצגה ולא רק תיאור.

                    ### רמת קושי:
                    קל.
                    """
                    st.session_state.translated_output = ai_translation
                except Exception as e:
                    st.error(f"{t('error_translating')}: {e}")

    if st.session_state.translated_output:
        st.markdown(f'<div class="sf-bubble-ai">{st.session_state.translated_output}</div>', unsafe_allow_html=True)

        # אפשרות לשמור לכרטיסיות (דוגמה)
        st.markdown("---")
        st.markdown(f'<div class="sf-sub-section-title">{t("translator_flashcards_section")}</div>', unsafe_allow_html=True)

        # נניח שיש לנו מבנה של כרטיסיות ב-session_state
        if 'flashcards' not in st.session_state:
            st.session_state.flashcards = []

        if st.button(t("translator_save_to_flashcards_btn"), key="save_flashcard_btn"):
            if source_text and st.session_state.translated_output:
                # פישוט - נשמור רק את המקור והתרגום הראשי
                card_content = {
                    "front": source_text,
                    "back": st.session_state.translated_output.split('## תרגום:')[1].split('---')[0].strip() # ניקח רק את התרגום הראשי
                }
                st.session_state.flashcards.append(card_content)
                st.success(t("translator_flashcard_saved"))
            else:
                st.warning(t("translator_no_translation_to_save"))

        if st.button(t("clear_ai_summary"), key="clear_translation_summary"):
            st.session_state.translated_output = None
            st.rerun()
