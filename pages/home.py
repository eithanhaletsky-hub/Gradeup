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
            ("10", "דפים" if lang=="he" else "Pages"), # עודכן מ-"6" ל-"10"
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

    # ── All N features ───────────────────────────────────────────
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

        ("💼", "nav_earn",
         "הכנסה & Ikigai" if lang=="he" else "Earn & Ikigai",
         "גלה את הכישרונות שלך עם מבחן Ikigai ולמד איך להרוויח מהם כבר עכשיו" if lang=="he"
         else "Discover your talents with the Ikigai test and learn to monetize them now",
         "#f472b6", "earn"),

        ("📊", "nav_grades",
         "מעקב ציונים" if lang=="he" else "Grade Tracker",
         "הכנס ציונים לפי מקצוע, ראה גרפים של מגמות, וקבל ניתוח AI על חוזקות וחולשות" if lang=="he"
         else "Log grades by subject, view trend charts, get AI analysis of strengths & weaknesses",
         "#fb923c", "grades"),

        ("💆", "nav_wellness",
         "רווחה נפשית" if lang=="he" else "Mental Wellness",
         "מעקב מצב רוח, עזרה בסטרס ממבחנים, תרגיל נשימה 4-7-8 וטיפים מעשיים" if lang=="he"
         else "Mood tracking, exam stress help, 4-7-8 breathing & practical mental health tips",
         "#a78bfa", "wellness"),

        # תכונות חדשות נוספו כאן
        ("🎴", "nav_flashcards",
         "כרטיסיות למידה" if lang=="he" else "Flashcards",
         "צור, למד וחזור על מושגים בקלות עם כרטיסיות למידה אינטראקטיביות." if lang=="he"
         else "Create, study, and review concepts easily with interactive flashcards.",
         "#ffbe0b", "flashcards"), # צבע מבליט חדש

        ("🎯", "nav_goals",
         "הגדרת יעדים אישיים" if lang=="he" else "Personal Goals",
         "הגדר יעדים אקדמיים ואישיים, עקוב אחר ההתקדמות שלך וקבל תמיכה להשגתם." if lang=="he"
         else "Set academic and personal goals, track your progress, and get support to achieve them.",
         "#14b8a6", "goals"), # צבע מבליט חדש

        ("📝", "nav_summarizer",
         "כלי לסיכום טקסטים" if lang=="he" else "Text Summarizer",
         "קצר טקסטים ארוכים במהירות באמצעות AI כדי לחסוך זמן לימוד יקר." if lang=="he"
         else "Quickly shorten long texts using AI to save valuable study time.",
         "#84cc16", "summarizer"), # צבע מבליט חדש

        ("❓", "nav_qa_board",
         "לוח שאלות ותשובות קהילתי" if lang=="he" else "Community Q&A Board",
         "שאל שאלות, ענה לאחרים ושתף ידע עם קהילת Gradeup." if lang=="he"
         else "Ask questions, answer others, and share knowledge with the Gradeup community.",
         "#c084fc", "qa_board"), # צבע מבליט חדש
        # סוף התכונות החדשות

        ("🔍", None,
         "DuckDuckGo + Gemini AI" if True else "DuckDuckGo + Gemini AI",
         "כל הדפים מחוברים לחיפוש DuckDuckGo ולמודל Gemini 2.0 Flash לתשובות עדכניות" if lang=="he"
         else "All pages connect to DuckDuckGo search & Gemini 2.0 Flash for fresh answers",
         "#34d399", None),
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

    # ── New pages highlight ───────────────────────────────────────
    st.markdown(
        f'<div class="sf-section-title">{"✨ חדש ב-Gradeup" if lang=="he" else "✨ New in Gradeup"}</div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="sf-card sf-card-accent4" style="padding:1.3rem">'
            f'<div style="font-size:1.8rem">📊</div>'
            f'<div style="font-weight:800;font-size:1.05rem;margin:.4rem 0">'
            + ("מעקב ציונים חכם" if lang=="he" else "Smart Grade Tracker")
            + f'</div><div style="color:var(--muted);font-size:.87rem">'
            + ("הכנס ציונים לפי מקצוע וסוג הערכה. ה-AI מזהה מגמות, מציין חולשות וממליץ על מה להשקיע זמן."
               if lang=="he" else
               "Log grades by subject & assessment type. AI spots trends, flags weaknesses & recommends where to invest time.")
            + f'</div><div style="margin-top:.8rem">'
            + ("גרפים: עמודות לפי מקצוע + קו מגמה לאורך זמן" if lang=="he" else "Charts: bar by subject + trend line over time")
            + "</div></div>",
            unsafe_allow_html=True,
        )
        if st.button(f"📊 {'פתח מעקב ציונים' if lang=='he' else 'Open Grade Tracker'}", key="home_grades", use_container_width=True, type="primary"):
            st.session_state.page = "grades"; st.rerun()

    with c2:
        st.markdown(
            f'<div class="sf-card sf-card-accent3" style="padding:1.3rem">'
            f'<div style="font-size:1.8rem">💆</div>'
            f'<div style="font-weight:800;font-size:1.05rem;margin:.4rem 0">'
            + ("רווחה נפשית לתלמידים" if lang=="he" else "Student Mental Wellness")
            + f'</div><div style="color:var(--muted);font-size:.87rem">'
            + ("עוקב אחרי מצב הרוח שלך, עוזר בלחץ ממבחנים, ומלמד טכניקות נשימה. הכל עם תמיכת AI אישית."
               if lang=="he" else
               "Tracks your mood, helps with exam stress, and teaches breathing techniques. All with personal AI support.")
            + f'</div><div style="margin-top:.8rem">'
            + ("כולל: מד סטרס • נשימה 4-7-8 • 8 טיפים מבוססי מחקר" if lang=="he" else "Includes: stress meter • 4-7-8 breathing • 8 research-based tips")
            + "</div></div>",
            unsafe_allow_html=True,
        )
        if st.button(f"💆 {'פתח רווחה נפשית' if lang=='he' else 'Open Wellness'}", key="home_wellness", use_container_width=True, type="primary"):
            st.session_state.page = "wellness"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pricing ───────────────────────────────────────────────────
    st.markdown(f'<div class="sf-section-title">{t("home_pricing_title")}</div>', unsafe_allow_html=True)

    free_col, pro_col, _ = st.columns([1, 1, 0.4])
    with free_col:
        free_f = [
            "✅ " + ("מערכת שעות בסיסית" if lang=="he" else "Basic schedule"),
            "✅ " + ("עוזר AI — 10 שאלות/יום" if lang=="he" else "AI — 10 q/day"),
            "✅ " + ("מבחן Ikigai" if lang=="he" else "Ikigai test"),
            "✅ " + ("מעקב ציונים (5 מקצועות)" if lang=="he" else "Grade tracker (5 subjects)"),
            "✅ " + ("רווחה נפשית בסיסית" if lang=="he" else "Basic wellness"),
            "❌ " + ("DuckDuckGo חיפוש" if lang=="he" else "DuckDuckGo search"),
            "❌ " + ("AI ללא הגבלה" if lang=="he" else "Unlimited AI"),
            "❌ " + ("ייצוא PDF" if lang=="he" else "PDF export"),
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
            "✅ " + ("הכל שבחינמי" if lang=="he" else "Everything in Free"),
            "✅ " + ("AI ללא הגבלה" if lang=="he" else "Unlimited AI"),
            "✅ " + ("DuckDuckGo חיפוש" if lang=="he" else "DuckDuckGo search"),
            "✅ " + ("העלאת תמונות ל-AI" if lang=="he" else "Image uploads to AI"),
            "✅ " + ("מעקב ציונים — ללא הגבלה" if lang=="he" else "Unlimited grade tracking"),
            "✅ " + ("ייצוא מערכת שעות PDF" if lang=="he" else "PDF schedule export"),
            "✅ " + ("כרטיס כישרון להורדה" if lang=="he" else "Skill card download"),
            "✅ " + ("עדיפות תמיכה" if lang=="he" else "Priority support"),
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

    # רשימת כל הכפתורים עבור אזור ה-CTA התחתון
    all_cta_buttons = [
        {"icon": "🗓️", "text_key": "nav_schedule", "page_id": "schedule"},
        {"icon": "📚", "text_key": "nav_homework", "page_id": "homework"},
        {"icon": "📊", "text_key": "nav_grades", "page_id": "grades"},
        {"icon": "💆", "text_key": "nav_wellness", "page_id": "wellness"},
        {"icon": "🎴", "text_key": "nav_flashcards", "page_id": "flashcards"},
        {"icon": "🎯", "text_key": "nav_goals", "page_id": "goals"},
        {"icon": "📝", "text_key": "nav_summarizer", "page_id": "summarizer"},
        {"icon": "❓", "text_key": "nav_qa_board", "page_id": "qa_board"},
    ]

    # הצגת הכפתורים בשתי שורות: 4 כפתורים בכל שורה
    buttons_per_row = 4
    num_buttons = len(all_cta_buttons)

    for i in range(0, num_buttons, buttons_per_row):
        row_buttons = all_cta_buttons[i : i + buttons_per_row]
        cols = st.columns(len(row_buttons)) # יצירת עמודות בהתאם למספר הכפתורים בשורה הנוכחית
        for j, button_data in enumerate(row_buttons):
            with cols[j]:
                # שימוש ב-t(text_key) עבור הטקסט של הכפתור
                if st.button(f"{button_data['icon']} {t(button_data['text_key'])}", use_container_width=True, type="primary", key=f"cta_btn_{button_data['page_id']}"):
                    st.session_state.page = button_data['page_id']; st.rerun()
