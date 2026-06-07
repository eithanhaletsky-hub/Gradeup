"""pages/science_calc.py — מחשבון מדעי: sympy + plotly + הסבר AI"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from ai_utils import call_gemini, get_api_key

# ── sympy import ─────────────────────────────────────────────────────────
try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations,
        implicit_multiplication_application,
    )
    SYMPY_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
    SYMPY_OK = True
except ImportError:
    SYMPY_OK = False

# ── Formulas reference ────────────────────────────────────────────────────
FORMULAS = {
    "פיזיקה / Physics": [
        ("תנועה","v = v₀ + at","מהירות סופית / Final velocity"),
        ("תנועה","x = v₀t + ½at²","תזוזה / Displacement"),
        ("כוחות","F = ma","חוק שני ניוטון / Newton 2nd"),
        ("אנרגיה","Eₖ = ½mv²","אנרגיה קינטית / Kinetic energy"),
        ("גלים","v = fλ","מהירות גל / Wave speed"),
        ("חשמל","V = IR","חוק אוהם / Ohm's law"),
        ("גרביטציה","F = Gm₁m₂/r²","כוח גרביטציה / Gravity"),
    ],
    "כימיה / Chemistry": [
        ("גזים","PV = nRT","גז אידיאלי / Ideal gas"),
        ("מולים","n = m/M","כמות חומר / Amount of substance"),
        ("pH","pH = -log[H⁺]","חומציות / Acidity"),
        ("חום","Q = mcΔT","חום ספציפי / Specific heat"),
        ("ריכוז","C = n/V","ריכוז / Concentration"),
    ],
    "מתמטיקה / Math": [
        ("משוואות","x = (-b±√(b²-4ac))/2a","נוסחת השורשים / Quadratic"),
        ("גיאומטריה","A = πr²","שטח עיגול / Circle area"),
        ("גיאומטריה","c² = a² + b²","פיתגורס / Pythagorean"),
        ("סטטיסטיקה","σ = √(Σ(x-μ)²/n)","סטיית תקן / Std deviation"),
        ("לוגריתמים","log_b(x) = ln(x)/ln(b)","החלפת בסיס / Change of base"),
        ("טריגונומטריה","sin²θ + cos²θ = 1","זהות פיתגורס / Pythagorean identity"),
    ],
}

MODES_HE = ["פתור משוואה","נגזרת","אינטגרל","פשט ביטוי","שרטט גרף"]
MODES_EN = ["Solve equation","Derivative","Integral","Simplify","Plot graph"]


# ── sympy solver ──────────────────────────────────────────────────────────
def _solve(expr_str: str, mode_he: str, lang: str) -> tuple[str, object | None]:
    if not SYMPY_OK:
        return "sympy not installed — run: pip install sympy", None

    x = sp.Symbol("x")
    local = {"x":x,"e":sp.E,"pi":sp.pi,"i":sp.I,
             "sin":sp.sin,"cos":sp.cos,"tan":sp.tan,
             "sqrt":sp.sqrt,"log":sp.log,"exp":sp.exp,"abs":sp.Abs}

    def parse(s):
        return parse_expr(s, local_dict=local, transformations=SYMPY_TRANSFORMS)

    try:
        if mode_he in ("פתור משוואה","Solve equation"):
            if "=" in expr_str:
                lhs_s, rhs_s = expr_str.split("=",1)
                eq = parse(lhs_s.strip()) - parse(rhs_s.strip())
            else:
                eq = parse(expr_str)
            sols = sp.solve(eq, x)
            if not sols:
                return ("אין פתרון" if lang=="he" else "No solution"), None
            return "x = " + ", ".join(str(sp.nsimplify(s,rational=True)) for s in sols), eq

        elif mode_he in ("נגזרת","Derivative"):
            expr = parse(expr_str)
            return f"f'(x) = {sp.simplify(sp.diff(expr,x))}", expr

        elif mode_he in ("אינטגרל","Integral"):
            expr = parse(expr_str)
            return f"∫f(x)dx = {sp.integrate(expr,x)} + C", expr

        elif mode_he in ("פשט ביטוי","Simplify"):
            expr = parse(expr_str)
            return str(sp.simplify(expr)), expr

        elif mode_he in ("שרטט גרף","Plot graph"):
            expr = parse(expr_str)
            return f"f(x) = {expr}", expr

        return "מצב לא מוכר", None
    except Exception as e:
        return str(e), None


def _plot(expr_obj, lang: str) -> go.Figure | None:
    if not SYMPY_OK or expr_obj is None:
        return None
    import numpy as np
    x = sp.Symbol("x")
    try:
        f  = sp.lambdify(x, expr_obj, modules=["numpy"])
        xs = np.linspace(-10, 10, 500)
        ys = f(xs)
        ys = np.where(np.isfinite(ys), ys, np.nan)
    except Exception:
        return None

    fig = go.Figure(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#6ee7b7",width=2.5)))
    fig.update_layout(
        plot_bgcolor="#10151f", paper_bgcolor="#080b12",
        font=dict(color="#e8edf5",family="Heebo"),
        xaxis=dict(showgrid=True,gridcolor="#1e2a3d",zeroline=True,zerolinecolor="#2d3a4f"),
        yaxis=dict(showgrid=True,gridcolor="#1e2a3d",zeroline=True,zerolinecolor="#2d3a4f"),
        height=300, margin=dict(l=30,r=20,t=20,b=30),
    )
    return fig


# ── Main render ───────────────────────────────────────────────────────────
def render():
    lang = st.session_state.lang
    he   = lang == "he"
    st.markdown(
        '<div class="section-title">🔬 ' +
        ("מחשבון מדעי" if he else "Science Calculator") +
        '</div>',
        unsafe_allow_html=True,
    )

    if not SYMPY_OK:
        st.error("sympy is not installed. Run: pip install sympy"); return

    if "sci_hist" not in st.session_state: st.session_state.sci_hist = []

    tab_calc, tab_formulas, tab_hist = st.tabs([
        "🧮 " + ("חישוב"    if he else "Calculate"),
        "📐 " + ("נוסחאות" if he else "Formulas"),
        "📚 " + ("היסטוריה" if he else "History"),
    ])

    with tab_calc:     _calc(he, lang)
    with tab_formulas: _formulas(he)
    with tab_hist:     _history(he)


# ── Calculate tab ─────────────────────────────────────────────────────────
def _calc(he, lang):
    modes    = MODES_HE if he else MODES_EN

    st.markdown(
        f'<div class="card card-g" style="margin-bottom:1rem">'
        f'<span style="color:var(--muted);font-size:.86rem">'
        + ("הכנס ביטוי מתמטי — sympy פותר צעד-אחר-צעד, plotly מציג גרף, AI מסביר בעברית."
           if he else
           "Enter a math expression — sympy solves step-by-step, plotly graphs, AI explains.")
        + "</span></div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([3,1])
    with c1:
        expr_input = st.text_input(
            "הכנס ביטוי / משוואה" if he else "Enter expression / equation",
            placeholder="x**2 - 5*x + 6 = 0  |  sin(x)*x  |  x**3 - 2*x",
            key="sci_expr",
        )
    with c2:
        mode = st.selectbox("", modes, key="sci_mode", label_visibility="collapsed")

    col_calc, col_ai = st.columns(2)
    with col_calc:
        calc_btn = st.button("🔬 " + ("חשב" if he else "Calculate"), type="primary", use_container_width=True, key="sci_calc")
    with col_ai:
        ai_btn   = st.button("🤖 " + ("הסבר AI" if he else "AI Explain"), use_container_width=True, key="sci_ai",
                             disabled=not st.session_state.sci_hist)

    # Perform calculation
    if calc_btn and expr_input.strip():
        mode_he = mode if he else (MODES_HE[MODES_EN.index(mode)] if mode in MODES_EN else mode)
        result_str, plot_expr = _solve(expr_input.strip(), mode_he, lang)

        entry = {
            "expr":   expr_input.strip(),
            "mode":   mode,
            "result": result_str,
            "time":   datetime.now().strftime("%H:%M"),
            "plot_str": str(plot_expr) if plot_expr is not None else None,
        }
        st.session_state.sci_hist.insert(0, entry)
        st.rerun()

    # Show latest result
    if not st.session_state.sci_hist:
        return

    latest = st.session_state.sci_hist[0]
    ok     = "שגיאה" not in latest["result"] and "error" not in latest["result"].lower() and "not" not in latest["result"].lower()
    res_col= "#6ee7b7" if ok else "#f87171"

    st.markdown(
        f'<div class="card" style="border-color:{res_col}44;padding:1.5rem;text-align:center;margin-top:1rem">'
        f'<div style="color:var(--muted);font-size:.8rem;margin-bottom:.4rem">'
        f'{latest["mode"]}  ·  <code style="color:#38bdf8">{latest["expr"]}</code></div>'
        f'<div style="font-size:1.6rem;font-weight:700;color:{res_col};font-family:Space Grotesk,monospace">'
        f'{latest["result"]}</div></div>',
        unsafe_allow_html=True,
    )

    # Plot if applicable
    if latest.get("plot_str") and latest["mode"] in (
        "שרטט גרף","Plot graph","נגזרת","Derivative","אינטגרל","Integral"
    ):
        try:
            x = sp.Symbol("x")
            plot_obj = sp.sympify(latest["plot_str"])
            fig = _plot(plot_obj, lang)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass

    # AI explanation
    if ai_btn:
        if not get_api_key():
            st.warning("Gemini API Key required")
        else:
            sys = (
                "אתה מורה למתמטיקה/מדעים לתלמיד תיכון. "
                "הסבר את הפתרון צעד-אחר-צעד בעברית פשוטה עם דוגמה אם רלוונטי. מקסימום 5 שלבים."
                if he else
                "You are a math/science teacher for a high school student. "
                "Explain the solution step-by-step in simple English with an example if relevant. Max 5 steps."
            )
            user_text = (
                f"ביטוי: {latest['expr']}\n"
                f"פעולה: {latest['mode']}\n"
                f"תוצאה: {latest['result']}"
                if he else
                f"Expression: {latest['expr']}\n"
                f"Operation: {latest['mode']}\n"
                f"Result: {latest['result']}"
            )
            with st.spinner("🤖…"):
                try:
                    explanation = call_gemini(
                        system_prompt=sys, user_text=user_text,
                        max_tokens=600, temperature=0.5,
                    )
                    st.markdown(
                        f'<div class="bubble-ai" style="margin-top:1rem">'
                        f'<div class="bubble-label">🤖 Gradeup AI — '
                        + ("פתרון צעד-אחר-צעד" if he else "Step-by-step")
                        + f'</div>{explanation.replace(chr(10),"<br>")}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(str(e))


# ── Formulas tab ──────────────────────────────────────────────────────────
def _formulas(he):
    for subject, formula_list in FORMULAS.items():
        st.markdown(f'<div class="section-title">{subject}</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        colors = {"פיזיקה":"#38bdf8","כימיה":"#fb923c","מתמטיקה":"#6ee7b7"}
        col_key = next((k for k in colors if k in subject), "מתמטיקה")
        accent  = colors[col_key]
        for i, (cat, formula, desc) in enumerate(formula_list):
            with cols[i % 3]:
                st.markdown(
                    f'<div class="formula-card" style="border-color:{accent}33;margin-bottom:.6rem">'
                    f'<div class="formula-cat" style="color:{accent}">{cat}</div>'
                    f'<div class="formula-text">{formula}</div>'
                    f'<div class="formula-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)


# ── History tab ───────────────────────────────────────────────────────────
def _history(he):
    hist = st.session_state.sci_hist
    if not hist:
        st.info("אין חישובים עדיין" if he else "No calculations yet")
        return

    st.markdown(
        f'<div class="section-title">'
        + (f"{len(hist)} חישובים" if he else f"{len(hist)} calculations")
        + "</div>",
        unsafe_allow_html=True,
    )
    for i, entry in enumerate(hist[:25]):
        c1, c2 = st.columns([5.5, .5])
        with c1:
            ok  = "error" not in entry["result"].lower() and "not" not in entry["result"].lower()
            col = "#6ee7b7" if ok else "#f87171"
            st.markdown(
                f'<div class="card" style="padding:.75rem;margin-bottom:.35rem">'
                f'<span style="color:var(--muted);font-size:.76rem">{entry["time"]} · {entry["mode"]}</span><br>'
                f'<code style="color:#38bdf8">{entry["expr"]}</code>'
                f'<span style="color:var(--muted)"> = </span>'
                f'<span style="color:{col};font-weight:600">{entry["result"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c2:
            if st.button("🗑️", key=f"sci_del_{i}"):
                st.session_state.sci_hist.pop(i); st.rerun()

    if st.button("🗑️ " + ("נקה הכל" if he else "Clear all"), key="sci_clr_all"):
        st.session_state.sci_hist = []; st.rerun()