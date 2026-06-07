"""pages/bagrut.py — מחשבון בגרות משוקלל + סימולציה + PDF"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime


SUBJECTS_HE = ["מתמטיקה","אנגלית","עברית","ספרות","היסטוריה","אזרחות",
               "פיזיקה","כימיה","ביולוגיה","מדעי המחשב","גיאוגרפיה","תנ\"ך","אחר"]
SUBJECTS_EN = ["Math","English","Hebrew","Literature","History","Civics",
               "Physics","Chemistry","Biology","CS","Geography","Bible","Other"]


def _avg(subs):
    tu = sum(s["u"] for s in subs)
    if not tu: return 0.0
    return sum((s["school"]*0.4 + s["bag"]*0.6)*s["u"] for s in subs) / tu

def _color(v):
    if v>=90: return "#6ee7b7"
    if v>=75: return "#38bdf8"
    if v>=60: return "#facc15"
    return "#f87171"

def _make_pdf(subs, avg):
    pdf = FPDF(); pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica","B",20)
    pdf.set_text_color(110,231,183)
    pdf.cell(0,12,"Gradeup — Bagrut Report",ln=True,align="C")
    pdf.set_font("Helvetica","",10); pdf.set_text_color(150,160,180)
    pdf.cell(0,7,datetime.now().strftime("%d/%m/%Y"),ln=True,align="C")
    pdf.ln(5); pdf.line(10,pdf.get_y(),200,pdf.get_y()); pdf.ln(5)
    for s in subs:
        c = s["school"]*0.4+s["bag"]*0.6
        pdf.set_font("Helvetica","B",11); pdf.set_text_color(232,237,245)
        pdf.cell(100,8,s["name"],ln=False)
        r,g,b = (110,231,183) if c>=90 else (56,189,248) if c>=75 else (251,196,60)
        pdf.set_text_color(r,g,b)
        pdf.cell(0,8,f"{c:.1f}  ({s['u']} yrs)",ln=True)
    pdf.ln(4); pdf.line(10,pdf.get_y(),200,pdf.get_y()); pdf.ln(4)
    pdf.set_font("Helvetica","B",15); pdf.set_text_color(110,231,183)
    pdf.cell(0,10,f"Average: {avg:.2f}",ln=True,align="C")
    pdf.set_font("Helvetica","I",8); pdf.set_text_color(40,60,80)
    pdf.cell(0,6,"gradeup.co.il",ln=True,align="C")
    return bytes(pdf.output())

def render():
    lang = st.session_state.lang
    he   = lang == "he"
    st.markdown('<div class="section-title">🎓 ' + ("מחשבון בגרות" if he else "Bagrut Calculator") + '</div>', unsafe_allow_html=True)

    if "bag_subs" not in st.session_state:
        st.session_state.bag_subs = [
            {"name":"מתמטיקה","u":5,"school":82,"bag":78},
            {"name":"אנגלית",  "u":5,"school":90,"bag":88},
            {"name":"עברית",   "u":5,"school":76,"bag":74},
            {"name":"פיזיקה",  "u":5,"school":85,"bag":80},
            {"name":"היסטוריה","u":5,"school":79,"bag":77},
        ]

    tab_calc, tab_sim, tab_exp = st.tabs([
        "🧮 " + ("חישוב" if he else "Calculate"),
        "🎯 " + ("סימולציה" if he else "Simulation"),
        "📥 " + ("ייצוא" if he else "Export"),
    ])

    with tab_calc: _calc(he)
    with tab_sim:  _sim(he)
    with tab_exp:  _export(he)


def _calc(he):
    subjs = SUBJECTS_HE if he else SUBJECTS_EN
    with st.expander("➕ " + ("הוסף מקצוע" if he else "Add subject")):
        c1,c2,c3,c4 = st.columns(4)
        with c1: name  = st.selectbox("מקצוע" if he else "Subject", subjs, key="bn")
        with c2: u     = st.selectbox("יחידות" if he else "Units", [1,2,3,4,5], index=4, key="bu")
        with c3: sch   = st.number_input("בית ספר" if he else "School", 0, 100, 80, key="bsc")
        with c4: bag   = st.number_input("בגרות" if he else "Bagrut", 0, 100, 80, key="bbg")
        if st.button("✅ " + ("הוסף" if he else "Add"), type="primary", key="badd"):
            st.session_state.bag_subs.append({"name":name,"u":u,"school":sch,"bag":bag})
            st.rerun()

    subs = st.session_state.bag_subs
    if not subs: st.info("הוסף מקצועות לחישוב" if he else "Add subjects to calculate"); return

    avg = _avg(subs)
    col = _color(avg)
    st.markdown(
        f'<div class="card" style="text-align:center;padding:2rem;border-color:{col}55">'
        f'<div style="color:var(--muted);font-size:.88rem">{"ממוצע כולל" if he else "Overall average"}</div>'
        f'<div style="font-size:4rem;font-weight:800;color:{col};font-family:Space Grotesk,monospace">{avg:.2f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Editable table
    st.markdown("<br>", unsafe_allow_html=True)
    for i, s in enumerate(subs):
        comb = s["school"]*0.4+s["bag"]*0.6
        cc   = _color(comb)
        c1,c2,c3,c4,c5,c6 = st.columns([2.5,1,1.2,1.2,1.2,.45])
        with c1:
            nv = st.text_input("", value=s["name"], key=f"bn_{i}", label_visibility="collapsed")
            subs[i]["name"] = nv
        with c2:
            uv = st.number_input("", 1, 5, s["u"], key=f"bu_{i}", label_visibility="collapsed")
            subs[i]["u"] = uv
        with c3:
            sv = st.number_input("", 0, 100, s["school"], key=f"bsc_{i}", label_visibility="collapsed")
            subs[i]["school"] = sv
        with c4:
            bv = st.number_input("", 0, 100, s["bag"], key=f"bbg_{i}", label_visibility="collapsed")
            subs[i]["bag"] = bv
        with c5:
            st.markdown(f'<div style="text-align:center;padding:.45rem 0;color:{cc};font-weight:700">{comb:.1f}</div>', unsafe_allow_html=True)
        with c6:
            if st.button("🗑️", key=f"bdel_{i}"):
                subs.pop(i); st.rerun()

    # Bar chart
    names  = [s["name"] for s in subs]
    sc_v   = [s["school"] for s in subs]
    bg_v   = [s["bag"]    for s in subs]
    cb_v   = [s["school"]*0.4+s["bag"]*0.6 for s in subs]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="בית ספר" if he else "School", x=names, y=sc_v, marker_color="#38bdf8", opacity=.7))
    fig.add_trace(go.Bar(name="בגרות"   if he else "Bagrut", x=names, y=bg_v, marker_color="#6ee7b7", opacity=.7))
    fig.add_trace(go.Scatter(name="משוקלל" if he else "Combined", x=names, y=cb_v,
                              mode="lines+markers", line=dict(color="#f472b6",width=2.5), marker=dict(size=8,color="#f472b6")))
    fig.update_layout(barmode="group", plot_bgcolor="#10151f", paper_bgcolor="#080b12",
                      font=dict(color="#e8edf5",family="Heebo"),
                      legend=dict(font=dict(color="#e8edf5")),
                      yaxis=dict(range=[0,105],showgrid=True,gridcolor="#1e2a3d"),
                      xaxis=dict(showgrid=False),
                      height=320, margin=dict(l=20,r=20,t=20,b=40))
    st.plotly_chart(fig, use_container_width=True)


def _sim(he):
    subs = st.session_state.bag_subs
    if not subs: st.info("הוסף מקצועות" if he else "Add subjects"); return

    cur  = _avg(subs)
    trgt = st.slider("יעד ממוצע" if he else "Target average", 60, 100, min(int(cur)+5,100), key="btrgt")
    names = [s["name"] for s in subs]
    chosen= st.selectbox("מקצוע לשיפור" if he else "Subject to improve", names, key="bsim_sub")
    cs    = next(s for s in subs if s["name"]==chosen)

    other_score = sum((s["school"]*.4+s["bag"]*.6)*s["u"] for s in subs if s["name"]!=chosen)
    total_u     = sum(s["u"] for s in subs)
    needed_comb = (trgt*total_u - other_score) / cs["u"]
    needed_bag  = (needed_comb - cs["school"]*.4) / .6

    ok  = 0 <= needed_bag <= 100
    col = _color(needed_bag) if ok else "#f87171"
    st.markdown(
        f'<div class="card" style="text-align:center;padding:2rem;border-color:{col}55">'
        f'<div style="color:var(--muted);font-size:.88rem">{"ציון בגרות נדרש ב" if he else "Required bagrut in"} {chosen}</div>'
        f'<div style="font-size:3.5rem;font-weight:800;color:{col};font-family:Space Grotesk,monospace">'
        f'{"בלתי אפשרי" if not ok else f"{needed_bag:.1f}"}</div>'
        + (f'<div style="color:var(--muted);font-size:.82rem">{"ציון נוכחי:" if he else "Current:"} {cs["bag"]}</div>' if ok else "")
        + "</div>",
        unsafe_allow_html=True,
    )
    if not ok:
        st.warning("הורד את היעד או שפר מספר מקצועות" if he else "Lower the target or improve multiple subjects")


def _export(he):
    subs = st.session_state.bag_subs
    if not subs: st.info("הוסף מקצועות" if he else "Add subjects"); return

    avg = _avg(subs)
    df  = pd.DataFrame([{
        ("מקצוע" if he else "Subject"): s["name"],
        ("יחידות" if he else "Units"):  s["u"],
        ("בית ספר" if he else "School"):s["school"],
        ("בגרות" if he else "Bagrut"):  s["bag"],
        "Combined": round(s["school"]*.4+s["bag"]*.6,1),
    } for s in subs])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.metric("ממוצע" if he else "Average", f"{avg:.2f}")

    c1,c2 = st.columns(2)
    with c1:
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSV", csv, "gradeup_bagrut.csv", "text/csv", key="b_csv")
    with c2:
        if st.button("📥 PDF", type="primary", key="b_pdf_btn"):
            pdf_b = _make_pdf(subs, avg)
            st.download_button("⬇️ Download PDF", pdf_b,
                f"gradeup_bagrut_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf", key="b_pdf_dl")