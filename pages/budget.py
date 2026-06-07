"""pages/budget.py — תקציב חודשי + pandas + plotly + AI טיפ"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from ai_utils import call_gemini, get_api_key

IN_CATS_HE  = ["שיעורים פרטיים","עבודה","קצבה","מתנה","אחר"]
IN_CATS_EN  = ["Tutoring","Work","Allowance","Gift","Other"]
OUT_CATS_HE = ["אוכל","בילויים","בגדים","תחבורה","לימודים","חיסכון","אחר"]
OUT_CATS_EN = ["Food","Entertainment","Clothes","Transport","Studies","Savings","Other"]

CAT_COLORS = {
    "שיעורים פרטיים":"#6ee7b7","Tutoring":"#6ee7b7","עבודה":"#34d399","Work":"#34d399",
    "קצבה":"#38bdf8","Allowance":"#38bdf8","מתנה":"#a78bfa","Gift":"#a78bfa",
    "אוכל":"#f87171","Food":"#f87171","בילויים":"#fb923c","Entertainment":"#fb923c",
    "בגדים":"#f472b6","Clothes":"#f472b6","תחבורה":"#facc15","Transport":"#facc15",
    "לימודים":"#38bdf8","Studies":"#38bdf8","חיסכון":"#6ee7b7","Savings":"#6ee7b7",
    "אחר":"#94a3b8","Other":"#94a3b8",
}

def render():
    lang = st.session_state.lang; he = lang=="he"
    st.markdown('<div class="section-title">💰 ' + ("תקציב חודשי" if he else "Monthly Budget") + '</div>', unsafe_allow_html=True)

    if "bud_items" not in st.session_state:
        st.session_state.bud_items = [
            {"type":"in","cat":"שיעורים פרטיים","amount":200,"desc":"שיעור מתמטיקה","date":"01/06"},
            {"type":"in","cat":"קצבה",           "amount":150,"desc":"דמי כיס",       "date":"01/06"},
            {"type":"out","cat":"אוכל",           "amount":80, "desc":"מסעדה עם חברים","date":"03/06"},
            {"type":"out","cat":"בילויים",        "amount":60, "desc":"סרט",           "date":"05/06"},
            {"type":"out","cat":"חיסכון",         "amount":50, "desc":"קופת חיסכון",   "date":"01/06"},
        ]
    if "bud_goal" not in st.session_state: st.session_state.bud_goal = 100
    if "bud_ai"   not in st.session_state: st.session_state.bud_ai   = None

    tab_enter, tab_view, tab_ai = st.tabs([
        "✏️ " + ("הוסף עסקה" if he else "Add Transaction"),
        "📊 " + ("סקירה" if he else "Overview"),
        "🤖 " + ("טיפ AI" if he else "AI Tip"),
    ])
    with tab_enter: _enter(he)
    with tab_view:  _view(he)
    with tab_ai:    _ai(he)


def _enter(he):
    in_cats  = IN_CATS_HE  if he else IN_CATS_EN
    out_cats = OUT_CATS_HE if he else OUT_CATS_EN

    with st.form("bud_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1:
            tx = st.radio("", [("💚 הכנסה" if he else "💚 Income"), ("🔴 הוצאה" if he else "🔴 Expense")],
                          horizontal=True, key="bud_tx", label_visibility="collapsed")
        with c2:
            amt = st.number_input("סכום (₪)" if he else "Amount (₪)", min_value=0.0, value=50.0, step=5.0)
        is_in = "הכנסה" in tx or "Income" in tx
        c3,c4 = st.columns(2)
        with c3: cat  = st.selectbox("קטגוריה" if he else "Category", in_cats if is_in else out_cats)
        with c4: desc = st.text_input("תיאור" if he else "Description", placeholder="(אופציונלי)")
        if st.form_submit_button("✅ " + ("הוסף" if he else "Add"), type="primary", use_container_width=True):
            if amt > 0:
                st.session_state.bud_items.append({
                    "type":"in" if is_in else "out", "cat":cat,
                    "amount":amt, "desc":desc or cat,
                    "date":datetime.now().strftime("%d/%m"),
                })
                st.success("✅")
                st.rerun()

    st.markdown("---")
    st.session_state.bud_goal = st.number_input(
        "🎯 " + ("יעד חיסכון חודשי (₪)" if he else "Monthly saving goal (₪)"),
        min_value=0, value=st.session_state.bud_goal, step=10
    )

    items = st.session_state.bud_items
    if not items: return
    st.markdown("---")
    st.markdown('<div class="section-title">' + ("עסקאות" if he else "Transactions") + '</div>', unsafe_allow_html=True)
    for i, item in enumerate(reversed(items)):
        idx = len(items)-1-i
        is_in = item["type"]=="in"
        c1,c2,c3,c4 = st.columns([2.5,1.2,1,.4])
        with c1:
            dot = CAT_COLORS.get(item["cat"],"#94a3b8")
            st.markdown(f'<span style="color:{dot}">■</span> <b>{item["desc"]}</b> <span style="color:var(--muted);font-size:.78rem">[{item["cat"]}]</span>', unsafe_allow_html=True)
        with c2:
            col = "#6ee7b7" if is_in else "#f87171"
            sign= "+" if is_in else "-"
            st.markdown(f'<span style="color:{col};font-weight:700">{sign}{item["amount"]:.0f} ₪</span>', unsafe_allow_html=True)
        with c3: st.caption(item["date"])
        with c4:
            if st.button("🗑️", key=f"bdel_{idx}"):
                items.pop(idx); st.rerun()


def _view(he):
    items = st.session_state.bud_items
    if not items: st.info("הוסף עסקה ראשונה" if he else "Add your first transaction"); return

    df = pd.DataFrame(items)
    total_in  = df[df["type"]=="in"]["amount"].sum()
    total_out = df[df["type"]=="out"]["amount"].sum()
    balance   = total_in - total_out
    goal      = st.session_state.bud_goal
    savings   = df[df["cat"].isin(["חיסכון","Savings"])]["amount"].sum()
    goal_pct  = min(100, int(savings/goal*100)) if goal else 0
    bal_col   = "#6ee7b7" if balance>=0 else "#f87171"

    c1,c2,c3,c4 = st.columns(4)
    for col, val, lbl, color in [
        (c1, f"{total_in:.0f}₪",  "הכנסות" if he else "Income",   "#6ee7b7"),
        (c2, f"{total_out:.0f}₪", "הוצאות" if he else "Expenses",  "#f87171"),
        (c3, f"{balance:.0f}₪",   "יתרה"   if he else "Balance",   bal_col),
        (c4, f"{goal_pct}%",       "חיסכון" if he else "Savings",   "#facc15"),
    ]:
        with col:
            st.markdown(f'<div class="stat"><div class="stat-num" style="color:{color};font-size:1.3rem">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    # Pie chart
    exp_df = df[df["type"]=="out"].groupby("cat")["amount"].sum().reset_index()
    if not exp_df.empty:
        fig = go.Figure(go.Pie(
            labels=exp_df["cat"], values=exp_df["amount"],
            marker=dict(colors=[CAT_COLORS.get(c,"#94a3b8") for c in exp_df["cat"]], line=dict(color="#080b12",width=2)),
            hole=.5, textfont=dict(color="#e8edf5"),
        ))
        fig.update_layout(
            title=dict(text="הוצאות לפי קטגוריה" if he else "Expenses by category", font=dict(color="#e8edf5")),
            plot_bgcolor="#10151f", paper_bgcolor="#080b12",
            font=dict(color="#e8edf5",family="Heebo"),
            legend=dict(font=dict(color="#e8edf5")),
            height=310, margin=dict(l=20,r=20,t=40,b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Savings progress
    st.markdown(
        f'<div style="color:var(--muted);font-size:.83rem;margin:.5rem 0 .3rem">'
        f'{savings:.0f} / {goal:.0f} ₪</div>'
        f'<div class="prog-wrap"><div class="prog-fill" style="background:#facc15;width:{goal_pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 CSV", csv, "gradeup_budget.csv", "text/csv", key="bud_csv")


def _ai(he):
    items = st.session_state.bud_items
    if not items: st.info("הוסף עסקאות קודם" if he else "Add transactions first"); return
    if not get_api_key(): st.warning("Gemini API Key required"); return

    df       = pd.DataFrame(items)
    total_in = df[df["type"]=="in"]["amount"].sum()
    total_out= df[df["type"]=="out"]["amount"].sum()
    summary  = "\n".join(f"{i['type']} | {i['cat']} | {i['amount']}₪ | {i['desc']}" for i in items)

    if st.button("🤖 " + ("קבל טיפ חיסכון" if he else "Get saving tip"), type="primary", key="bud_ai_btn"):
        sys = (
            "אתה יועץ כלכלי לתלמיד תיכון. הכנסות: {ti}₪, הוצאות: {to}₪. "
            "1) ציין חוזקה. 2) טיפ ספציפי לחיסכון. 3) אחוז חיסכון מומלץ. עברית, 3 משפטים."
            if he else
            "You advise a high school student. Income: {ti}₪, Expenses: {to}₪. "
            "1) Highlight a strength. 2) Specific saving tip. 3) Recommended saving %. English, 3 sentences."
        ).format(ti=total_in, to=total_out)
        with st.spinner("🤖…"):
            try:
                st.session_state.bud_ai = call_gemini(system_prompt=sys, user_text=summary, max_tokens=250, temperature=.7)
            except Exception as e: st.error(str(e))

    if st.session_state.bud_ai:
        st.markdown(
            f'<div class="bubble-ai"><div class="bubble-label">🤖 Gradeup AI</div>'
            f'{st.session_state.bud_ai}</div>',
            unsafe_allow_html=True,
        )
        if st.button("🗑️ " + ("נקה" if he else "Clear"), key="bud_ai_clr"):
            st.session_state.bud_ai = None; st.rerun()