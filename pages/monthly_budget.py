import streamlit as st
from ddgs import DDGS
from google import genai

# ודא ש-get_api_key מוגדרת להחזיר את מפתח ה-API שלך
# from ai_utils import get_api_key
# API_KEY = get_api_key()
from datetime import date

def render_monthly_budget(t):
    st.markdown(
        f'<div class="sf-section-title">{t("monthly_budget_title")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-subtitle">{t("money_for_students")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sf-description">{t("monthly_budget_description")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="sf-libraries-title">{t("libraries")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">pandas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">plotly</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">fpdf2</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">💼 Earn</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🎯 יעדים</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-features-title">{t("features")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("budget_expenses_pie_chart")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("budget_savings_goal")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("budget_ai_saving_tip")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div>- {t("budget_csv_export")}</div>', unsafe_allow_html=True)

    # --- לוגיקת התקציב החודשי ---
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("budget_main")}</div>', unsafe_allow_html=True)

    if "budget_transactions" not in st.session_state:
        st.session_state.budget_transactions = pd.DataFrame({
            'תיאור': [],
            'סכום': [],
            'קטגוריה': [], # הכנסה / הוצאה
            'תאריך': []
        })

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        description = st.text_input(t("budget_description"), key="budget_description_input")
    with c2:
        amount = st.number_input(t("budget_amount"), key="budget_amount_input")
    with c3:
        transaction_type = st.selectbox(t("budget_type"), [t("budget_income"), t("budget_expense")], key="budget_type_select")
    with c4:
        transaction_date = st.date_input(t("budget_date"), key="budget_date_input")

    if st.button(t("budget_add_transaction"), key="add_transaction_btn"):
        if description and amount is not None and transaction_date:
            new_transaction = pd.DataFrame([{
                'תיאור': description,
                'סכום': amount if transaction_type == t("budget_income") else -amount, # הוצאות שליליות
                'קטגוריה': transaction_type,
                'תאריך': transaction_date
            }])
            st.session_state.budget_transactions = pd.concat([st.session_state.budget_transactions, new_transaction], ignore_index=True)
            # איפוס שדות הקלט
            st.session_state.budget_description_input = ""
            st.session_state.budget_amount_input = 0.0
            st.session_state.budget_type_select = t("budget_income")
            st.session_state.budget_date_input = date.today()
            st.rerun()
        else:
            st.warning(t("budget_fill_all_fields"))

    # הצגת הטרנזקציות
    if not st.session_state.budget_transactions.empty:
        st.markdown("---")
        st.markdown(f'<div class="sf-sub-section-title">{t("budget_transactions_list")}</div>', unsafe_allow_html=True)
        st.data_editor(
            st.session_state.budget_transactions,
            num_rows="dynamic",
            key="edit_budget_transactions",
            column_config={
                "תיאור": st.column_config.TextColumn(t("budget_description")),
                "סכום": st.column_config.NumberColumn(t("budget_amount"), format="%.2f"),
                "קטגוריה": st.column_config.SelectboxColumn(t("budget_type"), options=[t("budget_income"), t("budget_expense")]),
                "תאריך": st.column_config.DateColumn(t("budget_date")),
            },
            use_container_width=True,
            on_change=lambda: _update_budget_transactions(t)
        )

    # סיכום תקציב
    st.markdown("---")
    st.markdown(f'<div class="sf-sub-section-title">{t("budget_summary")}</div>', unsafe_allow_html=True)

    if not st.session_state.budget_transactions.empty:
        # חישוב הכנסות והוצאות
        income = st.session_state.budget_transactions[st.session_state.budget_transactions['קטגוריה'] == t('budget_income')]['סכום'].sum()
        expenses = st.session_state.budget_transactions[st.session_state.budget_transactions['קטגוריה'] == t('budget_expense')]['סכום'].sum()
        balance = income + expenses # כי הוצאות כבר שליליות

        st.metric(t("budget_total_income"), f"{income:.2f} ₪")
        st.metric(t("budget_total_expenses"), f"{abs(expenses):.2f} ₪") # הצגה כחיובי
        st.metric(t("budget_balance"), f"{balance:.2f} ₪", delta=f"{balance:.2f} ₪")

        # גרף עוגה להוצאות
        expense_data = st.session_state.budget_transactions[st.session_state.budget_transactions['קטגוריה'] == t('budget_expense')]
        if not expense_data.empty:
            expense_by_category = expense_data.groupby('תיאור')['סכום'].sum().reset_index() # קטגוריה = תיאור ההוצאה
            expense_by_category['סכום'] = expense_by_category['סכום'].abs() # הערכים חיוביים לצורך הגרף

            fig = go.Figure(data=[go.Pie(
                labels=expense_by_category['תיאור'],
                values=expense_by_category['סכום'],
                hole=.3,
                insidetextorientation='radial'
            )])
            fig.update_layout(title_text=t("budget_expenses_distribution"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t("budget_no_expenses_to_display"))

        # יעד חיסכון (דוגמה)
        st.markdown("---")
        st.markdown(f'<div class="sf-sub-section-title">{t("budget_savings_goal")}</div>', unsafe_allow_html=True)
        savings_goal = st.number_input(t("budget_enter_savings_goal"), min_value=0.0, key="budget_savings_goal_input")
        if savings_goal > 0:
            progress = min(1, max(0, balance / savings_goal))
            st.progress(progress)
            st.caption(f"{t('budget_progress')}: {progress*100:.1f}% (₪{balance:.2f} / ₪{savings_goal:.2f})")
        else:
             st.caption(t("budget_set_savings_goal_first"))

        # טיפ AI (דוגמה פשוטה)
        st.markdown("---")
        st.markdown(f'<div class="sf-sub-section-title">{t("budget_ai_tip_title")}</div>', unsafe_allow_html=True)
        if balance < 0:
            st.warning(t("budget_ai_tip_overspending"))
        elif expenses > income * 0.7: # אם ההוצאות יותר מ-70% מההכנסה
             st.info(t("budget_ai_tip_reduce_expenses"))
        else:
             st.success(t("budget_ai_tip_good_job"))

    else:
        st.info(t("budget_no_transactions_yet"))

    # ייצוא CSV
    st.markdown("---")
    if st.button(t("budget_export_to_csv"), key="export_budget_csv_btn"):
        csv = st.session_state.budget_transactions.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=t("budget_download_csv"),
            data=csv,
            file_name="monthly_budget.csv",
            mime="text/csv",
            key="download_budget_csv"
        )


# פונקציה עזר לעדכון session state כאשר הטבלה משתנה
def _update_budget_transactions(t):
     if 'edit_budget_transactions' in st.session_state and st.session_state.edit_budget_transactions['data'] is not None:
        updated_df = pd.DataFrame(st.session_state.edit_budget_transactions['data'])
        # ודא שהסוגים מעודכנים כראוי
        updated_df['קטגוריה'] = updated_df['קטגוריה'].apply(lambda x: t("budget_income") if x == t("budget_income") else t("budget_expense"))
        st.session_state.budget_transactions = updated_df
        # st.rerun()
