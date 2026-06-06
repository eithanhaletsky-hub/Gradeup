"""pages/home.py — דף ראשי של Gradeup"""
import streamlit as st


# כל הדפים עם מטא-דאטה
ALL_PAGES = [
    # (icon, page_id, name_he, name_en, desc_he, desc_en, accent, group_he, group_en)
    ("🗓️","schedule",
     "מערכת שעות",      "Schedule",
     "שיעורים, מבחנים, חוגים ואירועים אישיים — לוח שבועי עם Plotly + AI מנתח עומס",
     "Classes, exams, clubs & personal events — Plotly weekly view + AI load analysis",
     "#6ee7b7","📚 לימודים","📚 Study"),

    ("📚","homework",
     "עוזר שיעורי בית", "Homework Bot",
     "שאל שאלות, העלה תמונות של תרגילים, חפש מידע עדכני עם DuckDuckGo",
     "Ask questions, upload exercise photos, search fresh info with DuckDuckGo",
     "#38bdf8","📚 לימודים","📚 Study"),

    ("🃏","flashcards",
     "כרטיסיות לימוד",  "Flashcards",
     "AI מייצר כרטיסיות מכל טקסט. תרגל במצב הפוך-ובדוק — כרטיסיות שנכשלו חוזרות",
     "AI generates cards from any text. Flip-and-check mode — missed cards repeat",
     "#f472b6","📚 לימודים","📚 Study"),

    ("📝","summarizer",
     "מסכם חומר חכם",   "Smart Summarizer",
     "הדבק פרק שלם — AI מחזיר נקודות, שאלות מבחן, מושגים. ייצוא PDF",
     "Paste a chapter — AI returns bullets, exam Qs, key terms. PDF export",
     "#facc15","📚 לימודים","📚 Study"),

    ("🔬","science",
     "מחשבון מדעי",     "Science Calculator",
     "sympy פותר משוואות, נגזרות, אינטגרלים. גרף Plotly + הסבר AI צעד-אחר-צעד",
     "sympy solves equations, derivatives, integrals. Plotly graph + AI step-by-step",
     "#34d399","📚 לימודים","📚 Study"),

    ("🌍","translator",
     "מתרגם חכם",       "Smart Translator",
     "תרגום עם הסבר דקדוקי ודוגמאות. שמור תרגומים ישירות לכרטיסיות הלימוד",
     "Translation with grammar notes & examples. Save directly to flashcards",
     "#a78bfa","📚 לימודים","📚 Study"),

    ("📊","grades",
     "מעקב ציונים",     "Grade Tracker",
     "הכנס ציונים לפי מקצוע — AI מזהה מגמות, מציין חולשות, גרפי plotly",
     "Log grades by subject — AI spots trends, flags weaknesses, plotly charts",
     "#fb923c","📊 מעקב","📊 Track"),

    ("🎓","bagrut",
     "מחשבון בגרות",    "Bagrut Calc",
     "חישוב ממוצע משוקלל לפי יחידות. סימולציה 'מה אני צריך' + ייצוא PDF",
     "Weighted average by units. 'What do I need' simulation + PDF export",
     "#6ee7b7","📊 מעקב","📊 Track"),

    ("🎯","goals",
     "מעקב יעדים",      "Goals Tracker",
     "יעדי ציון, הרגל, חיסכון — progress bars, דוח שבועי PDF + ניתוח AI",
     "Grade, habit, saving goals — progress bars, weekly PDF + AI coaching",
     "#a78bfa","📊 מעקב","📊 Track"),

    ("💼","earn",
     "הכנסה & Ikigai",  "Earn & Ikigai",
     "גלה כישרונות עם מבחן Ikigai, מצא דרכים להרוויח, צור כרטיס כישרון PNG",
     "Discover talents with Ikigai, find ways to earn, create skill card PNG",
     "#f472b6","💼 קריירה וכסף","💼 Career & Money"),

    ("💰","budget",
     "תקציב חודשי",     "Monthly Budget",
     "מעקב הכנסות/הוצאות עם גרף עוגה. AI נותן טיפ חיסכון. ייצוא CSV",
     "Track income/expenses with pie chart. AI saving tip. CSV export",
     "#facc15","💼 קריירה וכסף","💼 Career & Money"),

    ("🏆","scholarships",
     "מלגות וקורסים",   "Scholarships",
     "DuckDuckGo מחפש מלגות וקורסים חינמיים. AI מדרג לפי התאמה אישית",
     "DuckDuckGo finds scholarships & free courses. AI ranks by personal fit",
     "#38bdf8","💼 קריירה וכסף","💼 Career & Money"),

    ("💡","projects",
     "מחולל פרויקטים",  "Project Generator",
     "AI מייצר 3 רעיונות לפרויקט שנתי עם תוכנית עבודה. DuckDuckGo + PDF",
     "AI generates 3 annual project ideas with work plan. DuckDuckGo + PDF",
     "#fb923c","💼 קריירה וכסף","💼 Career & Money"),

    ("💆","wellness",
     "רווחה נפשית",     "Wellness",
     "מעקב מצב רוח, מד סטרס עם AI, תרגיל נשימה 4-7-8, 8 טיפים מבוססי מחקר",
     "Mood tracking, AI stress support, 4-7-8 breathing, 8 research-backed tips",
     "#a78bfa","💆 רווחה","💆 Wellness"),

    ("👥","qa",
     "לוח שאלות ותשובות","Q&A Board",
     "שאל שאלות, קבל תשובות מתלמידים ומ-AI. DuckDuckGo לפני פרסום",
     "Ask questions, get answers from peers & AI. DuckDuckGo before posting",
     "#6ee7b7","💆 רווחה","💆 Wellness"),
]


def render(t):
    lang = st.session_state.lang

    # ── Hero ──────────────────────────────────────────────────────
    col_h, col_img = st.columns([3, 2], gap="large")
    with col_h:
        st.markdown(
            '<div class="sf-hero-title">Gradeup</div>'
            f'<div class="sf-hero-sub">{t("home_hero_sub")}</div>',
            unsafe_allow_html=True,
        )
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"🚀 {t('home_get_started')}", type="primary", use_container_width=True, key="hero_start"):
                st.session_state.page = "schedule"; st.rerun()
        with b2:
            if st.button(f"🎓 {t('nav_bagrut')}", use_container_width=True, key="hero_bagrut"):
                st.session_state.page = "bagrut"; st.rerun()

        # Stats
        s1, s2, s3, s4 = st.columns(4)
        for col, num, lbl in [
            (s1, str(len(ALL_PAGES)), "דפים" if lang=="he" else "Pages"),
            (s2, "∞",                 "AI"),
            (s3, "3–5₪",             "לחודש" if lang=="he" else "/month"),
            (s4, "14–18",             "גילאים" if lang=="he" else "Ages"),
        ]:
            with col:
                st.markdown(
                    f'<div class="sf-stat"><div class="sf-stat-num">{num}</div>'
                    f'<div class="sf-stat-label">{lbl}</div></div>',
                    unsafe_allow_html=True,
                )

    with col_img:
        st.markdown(
            '<div class="sf-card sf-card-glow" style="height:100%;display:flex;'
            'flex-direction:column;justify-content:center;align-items:center;'
            'padding:2rem;min-height:220px">'
            '<div style="font-size:4rem">🎓</div>'
            '<div style="font-weight:800;color:#6ee7b7;margin-top:.8rem;font-size:1.1rem">'
            + ("לתלמידי חטיבה ותיכון" if lang=="he" else "Middle & High School")
            + '</div><div style="color:var(--muted);font-size:.85rem;margin-top:.3rem">'
            + ("ארגן · למד · הרוויח · תרגיש טוב" if lang=="he" else "Organize · Study · Earn · Feel good")
            + '</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── All pages by group ────────────────────────────────────────
    groups_he = ["📚 לימודים", "📊 מעקב", "💼 קריירה וכסף", "💆 רווחה"]
    groups_en = ["📚 Study",   "📊 Track", "💼 Career & Money","💆 Wellness"]
    groups    = groups_he if lang=="he" else groups_en

    name_idx  = 2 if lang=="he" else 3
    desc_idx  = 4 if lang=="he" else 5
    group_idx = 7 if lang=="he" else 8

    for group in groups:
        group_pages = [p for p in ALL_PAGES if p[group_idx] == group]
        if not group_pages:
            continue

        st.markdown(
            f'<div class="sf-section-title">{group}</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(3)
        for i, page in enumerate(group_pages):
            icon, page_id, _, _, _, _, accent = page[0], page[1], page[2], page[3], page[4], page[5], page[6]
            name = page[name_idx]
            desc = page[desc_idx]

            with cols[i % 3]:
                st.markdown(
                    f'<div class="sf-feature-tile" style="border-color:{accent}33;min-height:130px">'
                    f'<div class="sf-feature-icon">{icon}</div>'
                    f'<div class="sf-feature-name" style="color:{accent}">{name}</div>'
                    f'<div class="sf-feature-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    ("→ פתח" if lang=="he" else "→ Open"),
                    key=f"home_open_{page_id}",
                    use_container_width=True,
                ):
                    st.session_state.page = page_id
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # ── Pricing ───────────────────────────────────────────────────
    st.markdown(f'<div class="sf-section-title">{t("home_pricing_title")}</div>', unsafe_allow_html=True)

    free_col, pro_col, _ = st.columns([1, 1, .3])

    free_f = [
        ("✅", "מערכת שעות + אירועים אישיים"   if lang=="he" else "Schedule + personal events"),
        ("✅", "AI — 10 שאלות/יום"              if lang=="he" else "AI — 10 questions/day"),
        ("✅", "כרטיסיות (20)"                  if lang=="he" else "Flashcards (20)"),
        ("✅", "מחשבון בגרות"                   if lang=="he" else "Bagrut calculator"),
        ("✅", "מסכם — 3/יום"                   if lang=="he" else "Summarizer — 3/day"),
        ("✅", "תקציב חודשי"                    if lang=="he" else "Monthly budget"),
        ("✅", "מעקב 3 יעדים"                   if lang=="he" else "Track 3 goals"),
        ("✅", "לוח Q&A — קריאה ושאילה"         if lang=="he" else "Q&A board"),
        ("❌", "DuckDuckGo בכל הדפים"           if lang=="he" else "DuckDuckGo across all pages"),
        ("❌", "AI ללא הגבלה"                   if lang=="he" else "Unlimited AI"),
        ("❌", "ייצוא PDF/CSV"                   if lang=="he" else "PDF/CSV export"),
    ]
    pro_f = [
        ("✅", "הכל שבחינמי"                    if lang=="he" else "Everything in Free"),
        ("✅", "AI ללא הגבלה בכל הדפים"         if lang=="he" else "Unlimited AI on all pages"),
        ("✅", "DuckDuckGo — כל הדפים"          if lang=="he" else "DuckDuckGo — all pages"),
        ("✅", "ייצוא PDF — סיכומים, יעדים, בגרות" if lang=="he" else "PDF export — summaries, goals, bagrut"),
        ("✅", "ייצוא CSV — ציונים, תקציב"      if lang=="he" else "CSV export — grades, budget"),
        ("✅", "כרטיסיות ללא הגבלה"             if lang=="he" else "Unlimited flashcards"),
        ("✅", "יעדים ללא הגבלה"                if lang=="he" else "Unlimited goals"),
        ("✅", "העלאת תמונות ל-AI"              if lang=="he" else "Image uploads to AI"),
        ("✅", "כרטיס כישרון PNG"               if lang=="he" else "Skill card PNG"),
        ("✅", "עדיפות תמיכה"                   if lang=="he" else "Priority support"),
    ]

    with free_col:
        items_html = "".join(
            f'<div class="sf-price-feature"><span style="color:{"#6ee7b7" if mark=="✅" else "#f87171"}">{mark}</span> <b>{text}</b></div>'
            for mark, text in free_f
        )
        st.markdown(
            f'<div class="sf-price-card">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">{t("home_free")}</div>'
            f'<div class="sf-price-amount">0</div>'
            f'<div class="sf-price-label">₪</div>'
            f'<div style="margin:1rem 0">{items_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with pro_col:
        items_html = "".join(
            f'<div class="sf-price-feature"><span style="color:#6ee7b7">{mark}</span> <b>{text}</b></div>'
            for mark, text in pro_f
        )
        st.markdown(
            f'<div class="sf-price-card featured">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">{t("home_pro")} ⭐</div>'
            f'<div class="sf-price-amount">3–5</div>'
            f'<div class="sf-price-label">{t("home_pro_price")}</div>'
            f'<div style="margin:1rem 0">{items_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────
    st.markdown(
        f'<div class="sf-card sf-card-accent" style="text-align:center;padding:1.5rem">'
        f'<div style="font-size:1.2rem;font-weight:800;margin-bottom:.4rem">'
        + ("מוכן להתחיל?" if lang=="he" else "Ready to start?")
        + f'</div><div style="color:var(--muted);font-size:.88rem">'
        + ("בחר דף מהתפריט הצדדי — מחולק לפי קטגוריות" if lang=="he" else "Choose a page from the sidebar — organized by category")
        + "</div></div>",
        unsafe_allow_html=True,
    )

    # Quick access row
    quick = [
        ("🗓️","schedule"), ("🎓","bagrut"), ("🃏","flashcards"),
        ("🔬","science"),  ("💰","budget"), ("🏆","scholarships"),
    ]
    cols = st.columns(len(quick))
    for col, (icon, pid) in zip(cols, quick):
        with col:
            if st.button(icon, key=f"cta_{pid}", use_container_width=True):
                st.session_state.page = pid; st.rerun()
