"""pages/home.py — דף ראשי + תמחור"""
import streamlit as st


def render(t):
    lang = st.session_state.lang

    # ── Hero ─────────────────────────────────────────────────────
    col_hero, col_img = st.columns([3, 2], gap="large")
    with col_hero:
        st.markdown(
            f'<div class="sf-hero-title">Gradeup</div>'
            f'<div class="sf-hero-sub">{t("home_hero_sub")}</div>',
            unsafe_allow_html=True,
        )
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"🚀 {t('home_get_started')}", type="primary", use_container_width=True):
                st.session_state.page = "schedule"; st.rerun()
        with b2:
            if st.button(f"📚 {t('nav_homework')}", use_container_width=True):
                st.session_state.page = "homework"; st.rerun()

        s1, s2, s3, s4 = st.columns(4)
        stats = [
            ("10", "דפים" if lang=="he" else "Pages"),
            ("∞", "AI"),
            ("3–5₪", "לחודש" if lang=="he" else "/month"),
            ("14–18", "גילאים" if lang=="he" else "Ages"),
        ]
        for col, (num, lbl) in zip([s1,s2,s3,s4], stats):
            with col:
                st.markdown(
                    f'<div class="sf-stat"><div class="sf-stat-num">{num}</div>'
                    f'<div class="sf-stat-label">{lbl}</div></div>',
                    unsafe_allow_html=True,
                )

    with col_img:
        st.markdown(
            '<div class="sf-card sf-card-glow" style="height:100%;display:flex;'
            'flex-direction:column;justify-content:center;padding:2rem;min-height:240px">'
            '<div style="font-size:3.5rem;text-align:center">🎓</div>'
            '<div style="text-align:center;margin-top:1rem">'
            '<div style="font-size:1.05rem;font-weight:700;color:#6ee7b7">'
            + ("לתלמידי חטיבה ותיכון" if lang=="he" else "Middle & High School")
            + '</div><div style="font-size:.88rem;color:#5a6a82;margin-top:.4rem">'
            + ("ארגן · למד · הרוויח · תרגיש טוב" if lang=="he" else "Organize · Study · Earn · Feel good")
            + "</div></div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── All 6 features ───────────────────────────────────────────
    st.markdown(f'<div class="sf-section-title">{t("home_features")}</div>', unsafe_allow_html=True)

    features = [
        ("🗓️", "nav_schedule",
         "מערכת שעות חכמה" if lang=="he" else "Smart Schedule",
         "שיעורים, מבחנים, חוגים ואירועים אישיים — הכל בלוח שבועי אחד עם Plotly" if lang=="he"
         else "Classes, exams, clubs & personal events — all in one Plotly weekly view",
         "#6ee7b7", "schedule"),

        ("📚", "nav_homework",
         "עוזר שיעורי בית AI" if lang=="he" else "Homework Bot",
         "שאל שאלות, העלה תמונות של תרגילים, חפש מידע עדכני עם DuckDuckGo" if lang=="he"
         else "Ask questions, upload exercise photos, search fresh info with DuckDuckGo",
         "#38bdf8", "homework"),

        ("📊", "nav_grades",
         "מעקב ציונים" if lang=="he" else "Grade Tracker",
         "הכנס ציונים לפי מקצוע, ראה גרפים של מגמות, וקבל ניתוח AI על חוזקות וחולשות" if lang=="he"
         else "Log grades by subject, view trend charts, get AI analysis of strengths & weaknesses",
         "#fb923c", "grades"),

        ("🔍", None,
         "DuckDuckGo + Gemini AI",
         "כל הדפים מחוברים לחיפוש DuckDuckGo ולמודל Gemini 2.0 Flash לתשובות עדכניות" if lang=="he"
         else "All pages connect to DuckDuckGo search & Gemini 2.0 Flash for fresh answers",
         "#34d399", None),

        ("🃏", "nav_flashcards",
         "כרטיסיות לימוד" if lang=="he" else "Flashcards",
         "AI מייצר כרטיסיות מכל טקסט שתדביק. תרגל במצב 'הפוך ובדוק' עם מעקב ניקוד" if lang=="he"
         else "AI generates cards from any pasted text. Practice in flip-and-check mode with score tracking",
         "#f472b6", "flashcards"),

        ("📝", "nav_summarizer",
         "מסכם חומר חכם" if lang=="he" else "Smart Summarizer",
         "הדבק פרק שלם — AI מחזיר סיכום, מושגים, שאלות. ייצוא PDF עם fpdf2" if lang=="he"
         else "Paste a full chapter — AI returns summary, terms, questions. Export to PDF with fpdf2",
         "#facc15", "summarizer"),

        ("👥", "nav_qa",
         "לוח שאלות ותשובות" if lang=="he" else "Q&A Board",
         "שאל שאלות בלימודים, קבל תשובות מתלמידים אחרים ומה-AI. מחובר ל-DuckDuckGo" if lang=="he"
         else "Ask study questions, get answers from peers and AI. Connected to DuckDuckGo",
         "#38bdf8", "qa"),

        ("🎯", "nav_goals",
         "מעקב יעדים" if lang=="he" else "Goals Tracker",
         "הגדר יעדים (ציון, הרגל, חיסכון), עקוב אחרי התקדמות, קבל דוח שבועי PDF" if lang=="he"
         else "Set goals (grade, habit, saving), track progress, get weekly PDF report",
         "#a78bfa", "goals"),
    ]

    cols = st.columns(3)
    for i, (icon, nav_key, name, desc, accent, page_id) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f'<div class="sf-feature-tile" style="border-color:{accent}22;cursor:{"pointer" if page_id else "default"}">'
                f'<div class="sf-feature-icon">{icon}</div>'
                f'<div class="sf-feature-name" style="color:{accent}">{name}</div>'
                f'<div class="sf-feature-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if page_id:
                if st.button(
                    ("→ פתח" if lang=="he" else "→ Open"),
                    key=f"feat_btn_{page_id}",
                    use_container_width=True,
                ):
                    st.session_state.page = page_id; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pricing ───────────────────────────────────────────────────
    st.markdown(f'<div class="sf-section-title">{t("home_pricing_title")}</div>', unsafe_allow_html=True)

    free_col, pro_col, _ = st.columns([1, 1, 0.4])
    with free_col:
        free_f = [
            "✅ " + ("מערכת שעות + אירועים אישיים" if lang=="he" else "Schedule + personal events"),
            "✅ " + ("עוזר AI — 10 שאלות/יום"       if lang=="he" else "AI assistant — 10 q/day"),
            "✅ " + ("מבחן Ikigai + רעיונות הכנסה"   if lang=="he" else "Ikigai test + income ideas"),
            "✅ " + ("מעקב ציונים (5 מקצועות)"       if lang=="he" else "Grade tracker (5 subjects)"),
            "✅ " + ("רווחה נפשית בסיסית"             if lang=="he" else "Basic wellness"),
            "✅ " + ("כרטיסיות לימוד (20 כרטיסיות)"  if lang=="he" else "Flashcards (20 cards)"),
            "✅ " + ("מסכם חומר (3/יום)"              if lang=="he" else "Summarizer (3/day)"),
            "✅ " + ("לוח Q&A — קריאה ושאילה"         if lang=="he" else "Q&A board — read & ask"),
            "✅ " + ("מעקב 3 יעדים"                   if lang=="he" else "Track 3 goals"),
            "❌ " + ("DuckDuckGo בכל הדפים"           if lang=="he" else "DuckDuckGo across all pages"),
            "❌ " + ("AI ללא הגבלה"                   if lang=="he" else "Unlimited AI"),
            "❌ " + ("ייצוא PDF"                       if lang=="he" else "PDF export"),
            "❌ " + ("ייצוא CSV / Excel"               if lang=="he" else "CSV / Excel export"),
        ]
        st.markdown(
            f'<div class="sf-price-card">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">{t("home_free")}</div>'
            f'<div class="sf-price-amount">0</div>'
            f'<div class="sf-price-label">₪</div>'
            f'<div style="margin:1rem 0">'
            + "".join(f'<div class="sf-price-feature">{f}</div>' for f in free_f)
            + "</div></div>",
            unsafe_allow_html=True,
        )
    with pro_col:
        pro_f = [
            "✅ " + ("הכל שבחינמי"                        if lang=="he" else "Everything in Free"),
            "✅ " + ("AI ללא הגבלה בכל הדפים"             if lang=="he" else "Unlimited AI on all pages"),
            "✅ " + ("DuckDuckGo — כל הדפים"              if lang=="he" else "DuckDuckGo — all pages"),
            "✅ " + ("העלאת תמונות ל-AI (שיעורי בית)"     if lang=="he" else "Image uploads to AI (homework)"),
            "✅ " + ("מעקב ציונים ללא הגבלה"              if lang=="he" else "Unlimited grade tracking"),
            "✅ " + ("כרטיסיות ללא הגבלה + ייצוא"         if lang=="he" else "Unlimited flashcards + export"),
            "✅ " + ("מסכם ללא הגבלה + PDF"               if lang=="he" else "Unlimited summaries + PDF"),
            "✅ " + ("יעדים ללא הגבלה + דוח PDF שבועי"    if lang=="he" else "Unlimited goals + weekly PDF"),
            "✅ " + ("ייצוא CSV/Excel לציונים ויעדים"      if lang=="he" else "CSV/Excel export for grades & goals"),
            "✅ " + ("מערכת שעות PDF להורדה"               if lang=="he" else "Schedule PDF download"),
            "✅ " + ("כרטיס כישרון PNG להורדה"             if lang=="he" else "Skill card PNG download"),
            "✅ " + ("עדיפות תמיכה"                        if lang=="he" else "Priority support"),
        ]
        st.markdown(
            f'<div class="sf-price-card featured">'
            f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:.8rem">{t("home_pro")} ⭐</div>'
            f'<div class="sf-price-amount">3–5</div>'
            f'<div class="sf-price-label">{t("home_pro_price")}</div>'
            f'<div style="margin:1rem 0">'
            + "".join(f'<div class="sf-price-feature">{f}</div>' for f in pro_f)
            + "</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────
    st.markdown(
        f'<div class="sf-card sf-card-accent" style="text-align:center;padding:1.8rem">'
        f'<div style="font-size:1.3rem;font-weight:800;margin-bottom:.4rem">'
        + ("מוכן להתחיל?" if lang=="he" else "Ready to start?")
        + f'</div><div style="color:var(--muted);font-size:.9rem">'
        + ("בחר דף מהתפריט או לחץ על אחד מהכפתורים" if lang=="he" else "Choose a page from the sidebar or click a button below")
        + "</div></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, icon, label, page_id in [
        (c1, "🗓️", t("nav_schedule"),   "schedule"),
        (c2, "📚", t("nav_homework"),   "homework"),
        (c3, "🃏", t("nav_flashcards"), "flashcards"),
        (c4, "📝", t("nav_summarizer"), "summarizer"),
        (c5, "🎯", t("nav_goals"),      "goals"),
    ]:
        with col:
            if st.button(f"{icon} {label}", use_container_width=True, type="primary", key=f"cta_{page_id}"):
                st.session_state.page = page_id; st.rerun()
