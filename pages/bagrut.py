import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF

def render_bagrut_calculator(t):
    st.markdown(
        f'<div class="sf-section-title">{t("bagrut_calculator_title")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-subtitle">{t("bagrut_grades_levels")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-hot-feature">{t("bagrut_calculator_hot_feature")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-description">{t("bagrut_calculator_description")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="sf-libraries-title">{t("libraries")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">plotly</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">pandas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">fpdf2</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">📊 ציונים</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🎯 יעדים</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-features-title">{t("features")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("bagrut_weighted_calculation")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("bagrut_simulation")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("bagrut_pdf_export")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("bagrut_plotly_graph")}</div>', unsafe_allow_html=True)

    # --- לוגיקת מחשבון הבגרות ---
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("bagrut_calculator_main")}</div>', unsafe_allow_html=True)

    # טבלת ציונים קיימים
    st.markdown(f'<div class="sf-label">{t("bagrut_existing_grades")}</div>', unsafe_allow_html=True)
    if "bagrut_grades" not in st.session_state:
        st.session_state.bagrut_grades = pd.DataFrame({
            'מקצוע': [],
            'יחידות לימוד': [],
            'ציון נוכחי': [],
            'סוג': [] # בגרות / פנימי
        })

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        subject = st.text_input(t("bagrut_subject_name"), key="bagrut_subject")
    with c2:
        credits = st.number_input(t("bagrut_credits"), min_value=1, key="bagrut_credits")
    with c3:
        current_grade = st.number_input(t("bagrut_current_grade"), min_value=0, max_value=100, key="bagrut_current_grade")
    with c4:
        grade_type = st.selectbox(t("bagrut_grade_type"), [t("bagrut_exam"), t("bagrut_internal")], key="bagrut_grade_type")

    if st.button(t("bagrut_add_grade"), key="add_bagrut_grade_btn"):
        if subject and credits and current_grade is not None:
            new_grade = pd.DataFrame([{
                'מקצוע': subject,
                'יחידות לימוד': credits,
                'ציון נוכחי': current_grade,
                'סוג': grade_type
            }])
            st.session_state.bagrut_grades = pd.concat([st.session_state.bagrut_grades, new_grade], ignore_index=True)
            # איפוס שדות הקלט
            st.session_state.bagrut_subject = ""
            st.session_state.bagrut_credits = 1
            st.session_state.bagrut_current_grade = 0
            st.session_state.bagrut_grade_type = t("bagrut_exam")
            st.rerun()
        else:
            st.warning(t("bagrut_fill_all_fields"))

    # הצגת טבלת הציונים
    if not st.session_state.bagrut_grades.empty:
        st.data_editor(
            st.session_state.bagrut_grades,
            num_rows="dynamic",
            key="edit_bagrut_grades",
            column_config={
                "מקצוע": st.column_config.TextColumn(t("bagrut_subject_name")),
                "יחידות לימוד": st.column_config.NumberColumn(t("bagrut_credits"), format="%d"),
                "ציון נוכחי": st.column_config.NumberColumn(t("bagrut_current_grade"), format="%d"),
                "סוג": st.column_config.SelectboxColumn(t("bagrut_grade_type"), options=[t("bagrut_exam"), t("bagrut_internal")]),
            },
            use_container_width=True,
            on_change=lambda: _update_bagrut_grades(t) # עדכון session state כאשר הטבלה משתנה
        )

    # סימולציית בגרות
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("bagrut_simulation_title")}</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        target_average = st.number_input(t("bagrut_target_average"), min_value=50.0, max_value=100.0, step=0.1, key="bagrut_target_average")
    with c6:
        bagrut_credits_to_take = st.number_input(t("bagrut_credits_to_take"), min_value=1, key="bagrut_credits_to_take")

    if st.button(t("bagrut_calculate_needed_grade"), key="calculate_needed_grade_btn"):
        if not st.session_state.bagrut_grades.empty and bagrut_credits_to_take and target_average:
            # כאן תהיה הלוגיקה המורכבת של חישוב הציון הנדרש
            # לדוגמה:
            # 1. חשב את הממוצע הקיים משוקלל לפי יחידות
            # 2. חשב את סך היחידות הקיימות
            # 3. השתמש בנוסחה: (ממוצע_קיים * סה"כ_יחידות_קיימות + ציון_נדרש * יחידות_לבגרות) / (סה"כ_יחידות_קיימות + יחידות_לבגרות) = ממוצע_יעד
            # 4. פתור עבור ציון_נדרש
            needed_grade = calculate_required_bagrut_grade(st.session_state.bagrut_grades, target_average, bagrut_credits_to_take)
            if needed_grade is not None:
                st.success(f'{t("bagrut_you_need_on_average")} <b>{needed_grade:.2f}</b> {t("bagrut_on_bagrut_exams")}', unsafe_allow_html=True)
            else:
                st.warning(t("bagrut_calculation_error"))
        else:
            st.warning(t("bagrut_fill_all_fields_for_simulation"))

    # גרף הציונים (דוגמה)
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("bagrut_grades_chart")}</div>', unsafe_allow_html=True)
    if not st.session_state.bagrut_grades.empty:
        fig = go.Figure()
        # נניח שהציונים משוקללים לפי יחידות לצורך הגרף
        st.session_state.bagrut_grades['משקל'] = st.session_state.bagrut_grades['יחידות לימוד'] * st.session_state.bagrut_grades['ציון נוכחי']
        total_credits = st.session_state.bagrut_grades['יחידות לימוד'].sum()
        weighted_average = st.session_state.bagrut_grades['משקל'].sum() / total_credits if total_credits else 0

        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = weighted_average,
            title = {'text': t("bagrut_current_weighted_average")},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4CAF50"},
                'steps' : [
                    {'range': [0, 70], 'color': '#F44336'},
                    {'range': [70, 85], 'color': '#FFEB3B'},
                    {'range': [85, 100], 'color': '#4CAF50'}],
            }))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(t("bagrut_no_grades_to_display"))

    # ייצוא PDF
    st.markdown("---")
    if st.button(t("bagrut_export_to_pdf"), key="export_bagrut_pdf_btn"):
        _generate_bagrut_pdf(st.session_state.bagrut_grades, t)

# פונקציה עזר לעדכון session state כאשר הטבלה משתנה
def _update_bagrut_grades(t):
    if 'edit_bagrut_grades' in st.session_state and st.session_state.edit_bagrut_grades['data'] is not None:
        updated_df = pd.DataFrame(st.session_state.edit_bagrut_grades['data'])
        # ודא שהסוגים מעודכנים כראוי
        updated_df['סוג'] = updated_df['סוג'].apply(lambda x: t("bagrut_exam") if x == t("bagrut_exam") else t("bagrut_internal"))
        st.session_state.bagrut_grades = updated_df
        # st.rerun() # לא תמיד נדרש, תלוי איך streamlit מטפל בעדכונים

# פונקציה לחישוב הציון הנדרש
def calculate_required_bagrut_grade(grades_df, target_average, bagrut_credits_to_take):
    if grades_df.empty or bagrut_credits_to_take is None or target_average is None:
        return None

    total_current_credits = grades_df['יחידות לימוד'].sum()
    weighted_sum_current = (grades_df['יחידות לימוד'] * grades_df['ציון נוכחי']).sum()

    # הנוסחה: (weighted_sum_current + required_grade * bagrut_credits_to_take) / (total_current_credits + bagrut_credits_to_take) = target_average
    # weighted_sum_current + required_grade * bagrut_credits_to_take = target_average * (total_current_credits + bagrut_credits_to_take)
    # required_grade * bagrut_credits_to_take = target_average * (total_current_credits + bagrut_credits_to_take) - weighted_sum_current
    # required_grade = (target_average * (total_current_credits + bagrut_credits_to_take) - weighted_sum_current) / bagrut_credits_to_take

    numerator = (target_average * (total_current_credits + bagrut_credits_to_take)) - weighted_sum_current
    if bagrut_credits_to_take == 0:
        return None # למנוע חלוקה באפס
    required_grade = numerator / bagrut_credits_to_take

    return max(0, min(100, required_grade)) # להבטיח שהציון בין 0 ל-100

# פונקציה ליצירת PDF
def _generate_bagrut_pdf(grades_df, t):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # הגדרות פונט עברי
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
    except RuntimeError:
        # אם הפונט לא זמין, ננסה להשתמש בפונט סטנדרטי (ייתכן שלא יתמוך בעברית כראוי)
        pdf.set_font("Arial", size=12)

    # כותרת
    pdf.cell(200, 10, t("bagrut_calculator_title"), 0, 1, 'C')
    pdf.ln(5)

    # טבלת ציונים
    pdf.set_font('DejaVu', '', 10) # גופן קטן יותר לטבלה
    col_width = pdf.w / 4.5 # רוחב עמודה בערך
    pdf.set_fill_color(220, 220, 220) # צבע רקע לכותרות
    pdf.cell(col_width, 10, t("bagrut_subject_name"), 1, 0, 'C', 1)
    pdf.cell(col_width/2, 10, t("bagrut_credits"), 1, 0, 'C', 1)
    pdf.cell(col_width/2, 10, t("bagrut_current_grade"), 1, 0, 'C', 1)
    pdf.cell(col_width/2, 10, t("bagrut_grade_type"), 1, 0, 'C', 1)
    pdf.ln()

    total_credits = 0
    weighted_sum = 0
    pdf.set_fill_color(255, 255, 255) # צבע רקע רגיל
    for index, row in grades_df.iterrows():
        pdf.cell(col_width, 10, row['מקצוע'], 1, 0, 'R', 1)
        pdf.cell(col_width/2, 10, str(int(row['יחידות לימוד'])), 1, 0, 'C', 1)
        pdf.cell(col_width/2, 10, str(int(row['ציון נוכחי'])), 1, 0, 'C', 1)
        pdf.cell(col_width/2, 10, row['סוג'], 1, 0, 'C', 1)
        pdf.ln()
        total_credits += row['יחידות לימוד']
        weighted_sum += row['יחידות לימוד'] * row['ציון נוכחי']

    # ממוצע משוקלל
    weighted_average = weighted_sum / total_credits if total_credits else 0
    pdf.ln(5)
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(0, 10, f'{t("bagrut_current_weighted_average")}: {weighted_average:.2f}', 0, 1, 'R')

    # הורדת הקובץ
    from io import BytesIO
    img_byte_arr = BytesIO()
    # כאן ניתן להוסיף גרף אם רוצים, אך זה מסובך ב-FPDF. נשאיר זאת כרגע.
    # fig.write_image(img_byte_arr, format='png')
    # img_byte_arr.seek(0)
    # pdf.image(img_byte_arr, x=pdf.get_x(), y=pdf.get_y(), w=pdf.w/2)

    pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(
        label=t("bagrut_download_pdf"),
        data=pdf_output,
        file_name="bagrut_calculator_report.pdf",
        mime="application/pdf",
        key="download_bagrut_pdf"
    )

