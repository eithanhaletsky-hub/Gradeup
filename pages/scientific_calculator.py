import streamlit as st
import sympy
import plotly.graph_objects as go
import google as genai

# ודא ש-get_api_key מוגדרת להחזיר את מפתח ה-API שלך
# from ai_utils import get_api_key
# API_KEY = get_api_key()
# genai.configure(api_key=API_KEY)

def render_scientific_calculator(t):
    st.markdown(
        f'<div class="sf-section-title">{t("scientific_calculator_title")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-subtitle">{t("math_physics_chemistry")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="sf-libraries-title">{t("libraries")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">sympy</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">plotly</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">google-genai</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">📚 שיעורי בית</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🃏 כרטיסיות</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-features-title">{t("features")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("calculator_step_by_step")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("calculator_function_graph")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("calculator_ai_explanation_he")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("calculator_physics_chemistry_formulas")}</div>', unsafe_allow_html=True)

    # --- לוגיקת המחשבון המדעי ---
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("scientific_calculator_main_title")}</div>', unsafe_allow_html=True)

    expression_input = st.text_input(
        t("calculator_enter_equation_or_expression"),
        placeholder=t("calculator_example_expression"),
        key="calc_expression_input"
    )

    if "calc_result" not in st.session_state:
        st.session_state.calc_result = None
    if "calc_graph" not in st.session_state:
        st.session_state.calc_graph = None

    if st.button(f"🔢 {t('calculator_solve_btn')}", key="solve_calc_btn"):
        if not expression_input:
            st.warning(t("calculator_enter_expression_warning"))
        else:
            try:
                x = sympy.symbols('x')
                # נסה לפשט ביטוי
                simplified_expr = sympy.simplify(expression_input)

                # נסה לפתור משוואה
                solution_text = ""
                if '=' in expression_input:
                    eq_parts = expression_input.split('=')
                    lhs = sympy.sympify(eq_parts[0])
                    rhs = sympy.sympify(eq_parts[1])
                    equation = sympy.Eq(lhs, rhs)
                    solutions = sympy.solve(equation, x)
                    solution_text = f"{t('calculator_solution')}: {solutions}"
                else:
                    solution_text = f"{t('calculator_simplified_expression')}: {simplified_expr}"

                st.session_state.calc_result = solution_text

                # --- שימוש ב-plotly לגרף פונקציה ---
                if 'x' in str(simplified_expr): # אם הביטוי מכיל משתנה x, ננסה לשרטט גרף
                    x_vals = [i/10.0 for i in range(-50, 51)]
                    y_vals = []
                    for val in x_vals:
                        try:
                            y_vals.append(float(simplified_expr.subs(x, val)))
                        except (TypeError, ValueError, sympy.core.add.Add, sympy.core.function.Function):
                            y_vals.append(None) # טיפול בנקודות שבהן הפונקציה לא מוגדרת

                    fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines'))
                    fig.update_layout(title=f"גרף של: {simplified_expr}", xaxis_title="x", yaxis_title="f(x)")
                    st.session_state.calc_graph = fig
                else:
                    st.session_state.calc_graph = None

                # --- שימוש ב-Gemini להסבר AI ---
                # ודא שמפתח ה-API מוגדר
                # if 'API_KEY' not in locals() or not API_KEY:
                #     st.warning(t("gemini_api_key_missing_calculator"))
                # else:
                #     explanation_prompt = f"""
                #     הסבר צעד אחר צעד את הפתרון/פישוט של הביטוי המתמטי: '{expression_input}'.
                #     אם מדובר במשוואה, הסבר את שלבי הפתרון. אם בביטוי, הסבר את הפישוט.
                #     הדגש מושגים מתמטיים רלוונטיים.
                #     ענה בעברית, בצורה ברורה ומובנת לתלמיד תיכון.
                #     """
                #     model = genai.GenerativeModel('gemini-1.5-flash')
                #     response = model.generate_content(explanation_prompt, generation_config={"temperature": 0.3})
                #     st.session_state.calc_explanation = response.text

                # הדמיית פלט AI ללא API KEY
                st.session_state.calc_explanation = f"""
                ## הסבר AI צעד אחר צעד:
                **הביטוי/משוואה:** {expression_input}

                **שלב 1: זיהוי:** זיהינו שמדובר בביטוי מתמטי/משוואה שניתן לפשט/לפתור.

                **שלב 2: פישוט/פתרון:**
                *   אם ביטוי, sympy מבצע פישוט אלגברי כדי להגיע לצורה הפשוטה ביותר.
                *   אם משוואה, sympy מבודד את המשתנה X (במקרה זה) על ידי העברת אגפים וביצוע פעולות חשבוניות הפוכות.

                **שלב 3: תוצאה:** התוצאה הסופית היא {solution_text}.

                **מושגים רלוונטיים:** פישוט אלגברי, משוואות לינאריות/ריבועיות (בהתאם לביטוי).
                """

            except Exception as e:
                st.error(f"{t('calculator_calculation_error')}: {e}")
                st.session_state.calc_result = None
                st.session_state.calc_graph = None
                st.session_state.calc_explanation = None

    if st.session_state.calc_result:
        st.markdown("---")
        st.markdown(f'<div class="sf-sub-section-title">{t("calculator_results_title")}</div>', unsafe_allow_html=True)
        st.success(st.session_state.calc_result)

        if st.session_state.calc_graph:
            st.markdown(f'<div class="sf-sub-section-title">{t("calculator_function_graph")}</div>', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.calc_graph, use_container_width=True)

        if st.session_state.calc_explanation:
            st.markdown("---")
            st.markdown(f'<div class="sf-sub-section-title">{t("calculator_ai_explanation_he")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sf-bubble-ai">{st.session_state.calc_explanation}</div>', unsafe_allow_html=True)

        if st.button(t("clear_ai_summary"), key="clear_calc_results"):
            st.session_state.calc_result = None
            st.session_state.calc_graph = None
            st.session_state.calc_explanation = None
            st.rerun()

    # נוסחאות פיזיקה/כימיה (דוגמה פשוטה)
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("calculator_physics_chemistry_formulas_title")}</div>', unsafe_allow_html=True)

    formula_choice = st.selectbox(t("calculator_select_formula"), ["חוק אוהם (חשמל)", "נוסחת מהירות (פיזיקה)", "ריכוז מולרי (כימיה)"], key="formula_select")

    if formula_choice == "חוק אוהם (חשמל)":
        st.latex(r"V = I \cdot R")
        st.caption(t("calculator_ohm_law_explanation"))
    elif formula_choice == "נוסחת מהירות (פיזיקה)":
        st.latex(r"v = \frac{\Delta x}{\Delta t}")
        st.caption(t("calculator_velocity_formula_explanation"))
    elif formula_choice == "ריכוז מולרי (כימיה)":
        st.latex(r"C = \frac{n}{V}")
        st.caption(t("calculator_molar_concentration_explanation"))
