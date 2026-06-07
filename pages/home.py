"""pages/home.py — דף הבית של Gradeup"""
import streamlit as st


PAGES = [
    # (icon, page_id, name_he, name_en, desc_he, desc_en, accent, group_he, group_en)
    ("🗓️","schedule","מערכת שעות","Schedule",
     "שיעורים, מבחנים, חוגים ואירועים אישיים בלוח שבועי Plotly. AI מנתח עומס ומאזן.",
     "Classes, exams, clubs & events in a Plotly weekly board. AI analyzes workload.",
     "#6ee7b7","📚 לימודים","📚 Study"),

    ("📚","homework","עוזר שיעורי בית","Homework Bot",
     "שאל שאלות, העלה תמונות של תרגילים, חפש מידע עדכני עם DuckDuckGo.",
     "Ask questions, upload exercise photos, search fresh info with DuckDuckGo.",
     "#38bdf8","📚 לימודים","📚 Study"),

    ("🃏","flashcards","כרטיסיות לימוד","Flashcards",
     "AI מייצר כרטיסיות מכל טקסט שתדביק. תרגל בהפוך-ובדוק, כרטיסיות שנכשלו חוזרות.",
     "AI generates flashcards from pasted text. Flip-and-check — missed cards repeat.",
     "#f472b6","📚 לימודים","📚 Study"),

    ("📝","summarizer","מסכם חומר","Summarizer",
     "הדבק פרק שלם — AI מחזיר נקודות / שאלות מבחן / מושגים / סיפורי. ייצוא PDF.",
     "Paste a chapter — AI returns bullets / exam Qs / terms / narrative. PDF export.",
     "#facc15","📚 לימודים","📚 Study"),

    ("🔬","science","מחשבון מדעי","Science Calc",
     "sympy פותר משוואות, נגזרות, אינטגרלים צעד-אחר-צעד. גרף Plotly + הסבר AI.",
     "sympy solves equations, derivatives, integrals step-by-step. Plotly graph + AI.",
     "#34d399","📚 לימודים","📚 Study"),

    ("🌍","translator","מתרגם חכם","Translator",
     "תרגום + הסבר דקדוקי + דוגמאות. שמור ישירות לכרטיסיות הלימוד. היסטוריה בפנדס.",
     "Translation + grammar notes + examples. Save to flashcards. History via pandas.",
     "#a78bfa","📚 לימודים","📚 Study"),

    ("📊","grades","מעקב ציונים","Grade Tracker",
     "הכנס ציונים לפי מקצוע — גרפי Plotly, AI מזהה מגמות וממליץ על מה להשקיע זמן.",
     "Log grades by subject — Plotly charts, AI spots trends & recommends focus areas.",
     "#fb923c","📊 מעקב","📊 Track"),

    ("🎓","bagrut","מחשבון בגרות","Bagrut Calc",
     "ממוצע משוקלל לפי יחידות. סימולציה 'מה אני צריך' לפי יעד. ייצוא PDF + CSV.",
     "Weighted average by units. 'What do I need' simulation by target. PDF + CSV.",
     "#6ee7b7","📊 מעקב","📊 Track"),

    ("🎯","goals","מעקב יעדים","Goals Tracker",
     "יעדי ציון / הרגל / חיסכון עם progress bars. דוח שבועי PDF + ניתוח AI.",
     "Grade / habit / saving goals with progress bars. Weekly PDF report + AI.",
     "#a78bfa","📊 מעקב","📊 Track"),

    ("💰","budget","תקציב חודשי","Monthly Budget",
     "מעקב הכנסות/הוצאות עם גרף עוגה Plotly. pandas מנתח. AI נותן טיפ חיסכון.",
     "Income/expense tracking with Plotly pie. pandas analysis. AI saving tip.",
     "#facc15","💼 קריירה וכסף","💼 Career & Money"),

    ("🏆","scholarships","מלגות וקורסים","Scholarships",
     "DuckDuckGo מחפש מלגות וקורסים חינמיים עדכניים. AI מדרג לפי התאמה אישית.",
     "DuckDuckGo finds current scholarships & free courses. AI ranks by personal fit.",
     "#38bdf8","💼 קריירה וכסף","💼 Career & Money"),

    ("💡","projects","מחולל פרויקטים","Projects",
     "AI מייצר 3 רעיונות לפרויקט שנתי עם תוכנית עבודה שלבית. DuckDuckGo + PDF.",
     "AI generates 3 annual project ideas with step-by-step plan. DuckDuckGo + PDF.",
     "#fb923c","💼 קריירה וכסף","💼 Career & Money"),

    ("👥","qa","לוח שאלות ותשובות","Q&A Board",
     "שאל שאלות, קבל תשובות מתלמידים ומ-AI. DuckDuckGo מחפש לפני פרסום.",
     "Ask questions, get answers from peers & AI. DuckDuckGo searches before posting.",
     "#6ee7b7","💆 רווחה","💆 Wellness"),
]

GROUPS_HE = ["📚 לימודים","📊 מעקב","💼 קריירה וכסף","💆 רווחה"]
GROUPS_EN = ["📚 Study","📊 Track","💼 Career & Money","💆 Wellness"]

LIBS_USED = [
    ("🤖","Gemini 2.0 Flash","google-genai"),
    ("🔍","DuckDuckGo","ddgs"),
    ("🐼","Data Analysis","pandas"),
    ("📄","PDF Export","fpdf2"),
    ("🧮","Math Solver","sympy"),
    ("🖼️","Image Process","Pillow"),
    ("🔐","Auth","bcrypt"),
    ("📊","Charts","plotly"),
]


def render():
    lang = st.session_state.lang
    he   = lang == "he"
    groups = GROUPS_HE if he else GROUPS_EN

    # ── Hero ──────────────────────────────────────────────────────
    col_h, col_v = st.columns([3, 2], gap="large")
    with col_h:
        st.markdown('<div class="hero-title">Gradeup</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hero-sub">'
            + ("הכלי שתמיד רצית — לומד, עוקב, מרוויח, מרגיש טוב. "
               "לתלמידי חטיבה ותיכון."
               if he else
               "The tool you always wanted — study, track, earn, feel good. "
               "For middle & high school students.")
            + "</div>",
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns(2)
        with b1:
            if st.button("🚀 " + ("בואו נתחיל" if he else "Get Started"), type="primary", use_container_width=True, key="hero_go"):
                st.session_state.page = "schedule"; st.rerun()
        with b2:
            if st.button("🎓 " + ("מחשבון בגרות" if he else "Bagrut Calc"), use_container_width=True, key="hero_bag"):
                st.session_state.page = "bagrut"; st.rerun()

        # Stats row
        s1,s2,s3,s4 = st.columns(4)
        for col, num, lbl in [
            (s1, str(len(PAGES)), "דפים" if he else "Pages"),
            (s2, "∞",             "Gemini AI"),
            (s3, "3–5₪",         "לחודש" if he else "/month"),
            (s4, "14–18",         "גילאים" if he else "Ages"),
        ]:
            with col:
                st.markdown(
                    f'<div class="stat"><div class="stat-num">{num}</div>'
                    f'<div class="stat-label">{lbl}</div></div>',
                    unsafe_allow_html=True,
                )

    with col_v:
        st.markdown(
            '<div class="card card-glow" style="height:100%;display:flex;flex-direction:column;'
            'justify-content:center;align-items:center;padding:2.5rem;min-height:230px">'
            '<div style="font-size:4.5rem">🎓</div>'
            '<div style="font-weight:800;color:#6ee7b7;font-size:1.15rem;margin:.8rem 0 .3rem">'
            + ("לתלמידי חטיבה ותיכון" if he else "Middle & High School")
            + '</div><div style="color:var(--muted);font-size:.85rem;text-align:center">'
            + ("ארגן · למד · הרוויח · תרגיש טוב" if he else "Organize · Study · Earn · Feel good")
            + '</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tech stack strip ──────────────────────────────────────────
    st.markdown(
        f'<div style="text-align:center;color:var(--muted);font-size:.75rem;margin-bottom:.5rem">'
        + ("ספריות שבשימוש:" if he else "Libraries used:")
        + "</div>",
        unsafe_allow_html=True,
    )
    libs_html = " &nbsp; ".join(
        f'<span style="background:#181f2e;border:1px solid #1e2a3d;border-radius:99px;'
        f'padding:3px 12px;font-size:.74rem;color:#5a6a82">'
        f'{icon} <b style="color:#e8edf5">{lib}</b> <span style="opacity:.6">({pkg})</span></span>'
        for icon, lib, pkg in LIBS_USED
    )
    st.markdown(f'<div style="text-align:center;margin-bottom:1.5rem">{libs_html}</div>', unsafe_allow_html=True)

    # ── Pages by group ────────────────────────────────────────────
    ni = 2 if he else 3   # name index
    di = 4 if he else 5   # desc index
    gi = 7 if he else 8   # group index

    for group in groups:
        group_pages = [p for p in PAGES if p[gi] == group]
        if not group_pages: continue

        st.markdown(f'<div class="section-title">{group}</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, page in enumerate(group_pages):
            icon, pid, accent = page[0], page[1], page[6]
            name, desc = page[ni], page[di]
            with cols[i % 3]:
                st.markdown(
                    f'<div class="page-tile" style="border-color:{accent}33">'
                    f'<div class="tile-icon">{icon}</div>'
                    f'<div class="tile-name" style="color:{accent}">{name}</div>'
                    f'<div class="tile-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    ("→ פתח" if he else "→ Open"),
                    key=f"hp_{pid}",
                    use_container_width=True,
                ):
                    st.session_state.page = pid; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # ── Pricing ───────────────────────────────────────────────────
    st.markdown(
        f'<div class="section-title">{"💳 תמחור" if he else "💳 Pricing"}</div>',
        unsafe_allow_html=True,
    )

    free_items = [
        ("✅","מערכת שעות + אירועים","Schedule + personal events"),
        ("✅","AI — 10 שאלות/יום","AI — 10 questions/day"),
        ("✅","כרטיסיות (20)","Flashcards (20)"),
        ("✅","מחשבון בגרות","Bagrut calculator"),
        ("✅","מסכם — 3/יום","Summarizer — 3/day"),
        ("✅","מעקב 3 יעדים","Track 3 goals"),
        ("✅","תקציב חודשי","Monthly budget"),
        ("✅","לוח Q&A","Q&A board"),
        ("❌","DuckDuckGo בכל הדפים","DuckDuckGo everywhere"),
        ("❌","AI ללא הגבלה","Unlimited AI"),
        ("❌","ייצוא PDF/CSV","PDF/CSV export"),
    ]
    pro_items = [
        ("✅","הכל שבחינמי","Everything in Free"),
        ("✅","AI ללא הגבלה","Unlimited AI"),
        ("✅","DuckDuckGo — כל הדפים","DuckDuckGo — all pages"),
        ("✅","ייצוא PDF — סיכומים, יעדים, בגרות","PDF export — all pages"),
        ("✅","ייצוא CSV — ציונים, תקציב","CSV export — grades, budget"),
        ("✅","כרטיסיות + יעדים ללא הגבלה","Unlimited flashcards & goals"),
        ("✅","העלאת תמונות ל-AI","Image uploads to AI"),
        ("✅","כרטיס כישרון PNG","Skill card PNG"),
        ("✅","עדיפות תמיכה","Priority support"),
    ]

    def _price_row(mark, he_txt, en_txt):
        txt  = he_txt if he else en_txt
        col  = "#6ee7b7" if mark=="✅" else "#f87171"
        return (f'<div class="price-row"><span style="color:{col}">{mark}</span> <b>{txt}</b></div>')

    fc, pc, _ = st.columns([1, 1, .25])
    with fc:
        rows = "".join(_price_row(m,h,e) for m,h,e in free_items)
        st.markdown(
            f'<div class="price-card">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">{"חינמי" if he else "Free"}</div>'
            f'<div class="price-amount">0</div>'
            f'<div class="price-period">₪</div>'
            f'<div style="margin:1rem 0;text-align:right">{rows}</div></div>',
            unsafe_allow_html=True,
        )
    with pc:
        rows = "".join(_price_row(m,h,e) for m,h,e in pro_items)
        st.markdown(
            f'<div class="price-card pro">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">Pro ⭐</div>'
            f'<div class="price-amount">3–5</div>'
            f'<div class="price-period">{"₪ לחודש" if he else "₪ / month"}</div>'
            f'<div style="margin:1rem 0;text-align:right">{rows}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick access ──────────────────────────────────────────────
    st.markdown(
        f'<div class="card card-g" style="text-align:center;padding:1.4rem">'
        f'<div style="font-size:1.15rem;font-weight:800;margin-bottom:.4rem">'
        + ("מוכן להתחיל? בחר דף מהתפריט הצדדי" if he else "Ready? Choose a page from the sidebar")
        + f'</div><div style="color:var(--muted);font-size:.85rem">'
        + ("הניווט מחולק לפי קטגוריות — לימודים / מעקב / קריירה / רווחה"
           if he else
           "Navigation grouped by category — Study / Track / Career / Wellness")
        + "</div></div>",
        unsafe_allow_html=True,
    )

    quick = [("🗓️","schedule"),("🎓","bagrut"),("🃏","flashcards"),
             ("🔬","science"),("💰","budget"),("🏆","scholarships")]
    qcols = st.columns(len(quick))
    for col, (icon, pid) in zip(qcols, quick):
        with col:
            if st.button(icon, key=f"qk_{pid}", use_container_width=True):
                st.session_state.page = pid; st.rerun()