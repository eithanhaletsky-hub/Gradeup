import streamlit as st
import json
from ddgs import DDGS
import google as genai
from fpdf import FPDF
from io import BytesIO

# ודא ש-get_api_key מוגדרת להחזיר את מפתח ה-API שלך
# from ai_utils import get_api_key
# API_KEY = get_api_key()
# genai.configure(api_key=API_KEY)

def render_project_generator(t):
    st.markdown(
        f'<div class="sf-section-title">{t("project_generator_title")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-subtitle">{t("creativity")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-description">{t("project_generator_description")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="sf-libraries-title">{t("libraries")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">google-genai</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">ddgs</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">fpdf2</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🎯 יעדים</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">📝 מסכם</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-features-title">{t("features")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("project_generator_ideas")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("project_generator_workplan")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("project_generator_pdf_export")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("project_generator_web_examples")}</div>', unsafe_allow_html=True)

    # --- לוגיקת מחולל הפרויקטים ---
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("project_generator_form_title")}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        interests = st.text_area(t("project_generator_interests_input"), placeholder=t("project_generator_interests_placeholder"), key="project_gen_interests")
    with c2:
        strong_subjects = st.text_area(t("project_generator_strong_subjects_input"), placeholder=t("project_generator_strong_subjects_placeholder"), key="project_gen_subjects")

    time_frame = st.selectbox(t("project_generator_time_frame_input"), ["שבוע", "חודש", "סמסטר", "שנה"], key="project_gen_time_frame")

    if "generated_projects" not in st.session_state:
        st.session_state.generated_projects = None

    if st.button(t("project_generator_generate_btn"), key="generate_project_btn"):
        if not interests or not strong_subjects:
            st.warning(t("project_generator_fill_all_fields"))
        else:
            # --- שימוש ב-Gemini ליצירת רעיונות ותוכנית עבודה ---
            # ודא שמפתח ה-API מוגדר
            # if 'API_KEY' not in locals() or not API_KEY:
            #     st.warning(t("gemini_api_key_missing_project_gen"))
            #     return

            project_prompt = f"""
            צור 3-5 רעיונות לפרויקטים שנתיים/עצמאיים לתלמיד עם תחומי עניין: {interests} ומקצועות חזקים: {strong_subjects}.
            מסגרת הזמן לפרויקט היא: {time_frame}.
            לכל רעיון, ספק:
            1. שם הפרויקט
            2. תיאור קצר
            3. מטרות
            4. תוכנית עבודה מפורטת עם שלבים עיקריים וציוני דרך (לפחות 5 שלבים)
            5. משאבים מומלצים (ספרים, אתרים, כלים)
            6. אילו מקצועות הפרויקט משלב

            לאחר מכן, עבור כל פרויקט, חפש ב-DuckDuckGo דוגמה אחת רלוונטית או מקור מידע נוסף, וצרף קישור.
            ענה בעברית, בפורמט ברור ומסודר.
            """

            with st.spinner(t("project_generator_thinking")):
                try:
                    # model = genai.GenerativeModel('gemini-1.5-flash')
                    # response = model.generate_content(project_prompt, generation_config={"temperature": 0.7})
                    # ai_output = response.text

                    # הדמיית פלט AI ללא API KEY
                    ai_output = f"""
                    ## רעיונות לפרויקטים:

                    **1. שם הפרויקט: פיתוח אפליקציית "עוזר שיעורים" אישית**
                    **תיאור:** בניית אפליקציה מבוססת AI שמסייעת לתלמידים לנהל שיעורי בית, מבחנים, ומספקת הסברים מותאמים אישית בחומר הנלמד.
                    **מטרות:** שיפור יכולות תכנות, הבנה מעמיקה ב-AI, פתרון בעיה יומיומית.
                    **תוכנית עבודה:**
                    1. **שלב 1: מחקר ותכנון (שבוע):** הגדרת פיצ'רים, בחירת טכנולוגיות (Python/Streamlit/Kivy, Gemini API), עיצוב UI/UX.
                    2. **שלב 2: בניית בסיס נתונים ו-Backend (שבועיים):** הגדרת מודל נתונים, פיתוח לוגיקה לניהול משימות וציונים.
                    3. **שלב 3: הטמעת AI להסברים (שבועיים):** שילוב Gemini API ליצירת הסברים, תרגומים ותמצות חומר.
                    4. **שלב 4: בניית ממשק משתמש (שבוע):** עיצוב ופיתוח ממשק גרפי ידידותי.
                    5. **שלב 5: בדיקות ושיפורים (שבוע):** בדיקות פנימיות, איסוף משוב וביצוע אופטימיזציות.
                    **משאבים מומלצים:**
                    - ספר: "Python Crash Course"
                    - אתר: Streamlit Docs, Google AI Studio
                    - כלי: VS Code, Git
                    **מקצועות משולבים:** מדעי המחשב, אנגלית, מתמטיקה.

                    **דוגמה מהאינטרנט (DuckDuckGo):** [מדריך לבניית אפליקציה ב-Streamlit](https://www.google.com/search?q=streamlit+app+tutorial) (קישור לדוגמה)

                    **2. שם הפרויקט: בניית רובוט מיון פסולת חכם**
                    **תיאור:** פיתוח רובוט קטן המשתמש במצלמה וראייה ממוחשבת כדי לזהות ולמיין סוגי פסולת שונים (פלסטיק, נייר, מתכת).
                    **מטרות:** לימוד ראייה ממוחשבת, בקרת רובוטים, תרומה לסביבה.
                    **תוכנית עבודה:**
                    1. **שלב 1: לימוד ובחירת חומרה (שבוע):** מחקר על Raspberry Pi, מצלמות, מנועים סרוו.
                    2. **שלב 2: בניית מודל זיהוי תמונה (שבועיים):** אימון מודל למידת מכונה (TensorFlow Lite) לזיהוי פסולת.
                    3. **שלב 3: תכנון ובניית מבנה הרובוט (שבוע):** הדפסת רכיבים במדפסת תלת מימד או שימוש בחומרים קיימים.
                    4. **שלב 4: כתיבת קוד לבקרת הרובוט (שבועיים):** שילוב המצלמה, מנועים ומודל ה-AI.
                    5. **שלב 5: כיול ובדיקות (שבוע):** בדיקת דיוק המיון, אופטימיזציה של תנועה.
                    **משאבים מומלצים:**
                    - ספר: "Practical Computer Vision with Python"
                    - אתר: OpenCV Documentation, Raspberry Pi Foundation
                    - כלי: Python, TensorFlow Lite
                    **מקצועות משולבים:** פיזיקה, מדעי המחשב, כימיה (מחזור).

                    **דוגמה מהאינטרנט (DuckDuckGo):** [פרויקטי מיון פסולת ב-Raspberry Pi](https://www.google.com/search?q=raspberry+pi+waste+sorter+project) (קישור לדוגמה)

                    **3. שם הפרויקט: כתיבת רומן מד"ב המשלב עקרונות פיזיקליים מתקדמים**
                    **תיאור:** יצירת סיפור מדע בדיוני מורכב, תוך שילוב עקרונות כמו תורת היחסות, מכניקת קוונטים וחורים שחורים בצורה מדויקת ומהנה.
                    **מטרות:** פיתוח יכולות כתיבה יצירתית, העמקה בהבנת פיזיקה, שילוב בין מדע לאמנות.
                    **תוכנית עבודה:**
                    1. **שלב 1: מחקר מעמיק בפיזיקה (חודש):** קריאת ספרים ומאמרים על עקרונות פיזיקליים רלוונטיים.
                    2. **שלב 2: פיתוח עלילה ודמויות (שבועיים):** יצירת קונספט, בניית עולם ומערכת דמויות.
                    3. **שלב 3: כתיבת טיוטה ראשונית (חודשיים):** התחלת הכתיבה בפועל, התמקדות בסיפור ובזרימה.
                    4. **שלב 4: ביקורת עמיתים ועריכה (חודש):** קבלת משוב, בדיקת עקביות מדעית ועריכה ספרותית.
                    5. **שלב 5: שכתוב והגהה (שבועיים):** ליטושים אחרונים, תיקוני שגיאות.
                    **משאבים מומלצים:**
                    - ספר: "קיצור תולדות הזמן" (סטיבן הוקינג), "חולית" (פרנק הרברט)
                    - אתר: Khan Academy (פיזיקה), פורומים לכתיבה יצירתית.
                    - כלי: Google Docs, Grammarly
                    **מקצועות משולבים:** ספרות, פיזיקה, אנגלית.

                    **דוגמה מהאינטרנט (DuckDuckGo):** [ספרי מדע בדיוני מבוססי מדע](https://www.google.com/search?q=hard+science+fiction+books) (קישור לדוגמה)
                    """

                    st.session_state.generated_projects = ai_output
                except Exception as e:
                    st.error(f"{t('error_generating_project')}: {e}")

    if st.session_state.generated_projects:
        st.markdown(f'<div class="sf-bubble-ai">{st.session_state.generated_projects}</div>', unsafe_allow_html=True)

        # כפתור לייצוא PDF
        if st.button(t("project_generator_export_pdf_btn"), key="export_project_pdf_btn"):
            _generate_project_pdf(st.session_state.generated_projects, t)

        if st.button(t("clear_ai_summary"), key="clear_project_summary"):
            st.session_state.generated_projects = None
            st.rerun()

# פונקציה ליצירת PDF
def _generate_project_pdf(content, t):
    pdf = FPDF()
    pdf.add_page()
    # הגדרות פונט עברי
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
    except RuntimeError:
        pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, t("project_generator_title"), 0, 1, 'C')
    pdf.ln(5)

    # פיצול התוכן לשורות וכתיבה ל-PDF
    # זהו פישוט, ביישום אמיתי נרצה לפרסר את התוכן בצורה חכמה יותר.
    for line in content.split('\n'):
        if line.strip().startswith('##'):
            pdf.set_font('DejaVu', 'B', 14)
            pdf.cell(0, 10, line.replace('## ', ''), 0, 1, 'R')
            pdf.set_font('DejaVu', '', 12)
        elif line.strip().startswith('**'):
            pdf.set_font('DejaVu', 'B', 12)
            pdf.multi_cell(0, 7, line.replace('**', ''), 0, 'R')
            pdf.set_font('DejaVu', '', 12)
        else:
            pdf.multi_cell(0, 7, line, 0, 'R')
        pdf.ln(1)


    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(
        label=t("project_generator_download_pdf"),
        data=pdf_output,
        file_name="generated_projects_report.pdf",
        mime="application/pdf",
        key="download_project_pdf"
    )
