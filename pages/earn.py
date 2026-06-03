"""pages/earn.py — הכנסה + מבחן Ikigai + חיפוש + כרטיס Pillow"""
import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
from ai_utils import call_gemini, get_api_key, ddg_search

# ── Data ──────────────────────────────────────────────────────────────────
SKILLS_HE = ["מתמטיקה", "אנגלית", "תכנות", "מוזיקה", "ציור/עיצוב",
              "כתיבה", "ספורט/כושר", "שפות", "מדעים", "בישול", "אחר"]
SKILLS_EN = ["Math", "English", "Coding", "Music", "Art/Design",
              "Writing", "Sports/Fitness", "Languages", "Sciences", "Cooking", "Other"]

IDEAS = {
    "he": {
        "מתמטיקה":    ("📐", "מורה פרטי",          "שיעורים לחברים וילדים קטנים",          "30–80 ₪/שעה",  "#6ee7b7"),
        "אנגלית":     ("🗣️", "שיעורי אנגלית",      "שיחה, קריאה, הכנה לבגרות",             "30–70 ₪/שעה",  "#38bdf8"),
        "תכנות":      ("💻", "Freelance",           "אתרים, בוטים, Fiverr / Upwork",         "50–200 ₪/שעה", "#a78bfa"),
        "מוזיקה":     ("🎵", "שיעורי נגינה",        "גיטרה, פסנתר, שירה",                   "40–90 ₪/שעה",  "#f472b6"),
        "ציור/עיצוב": ("🎨", "עיצוב גרפי",          "לוגואים, פוסטרים, רשתות חברתיות",      "50–150 ₪/פרוי","#fb923c"),
        "כתיבה":      ("✍️", "כתיבת תוכן",          "בלוגים, תיאורים, סיכומים",             "20–60 ₪/1000", "#facc15"),
        "ספורט/כושר": ("🏋️", "מאמן אישי",          "אימונים אישיים וקבוצתיים",             "40–100 ₪/שעה", "#34d399"),
        "שפות":       ("🌍", "תרגום ושיעורי שפה",   "ספרדית, צרפתית, ערבית",                "30–80 ₪/שעה",  "#60a5fa"),
        "מדעים":      ("🔬", "עזרה בביולוגיה/כימיה","שיעורים פרטיים ועבודות חקר",           "35–80 ₪/שעה",  "#6ee7b7"),
        "בישול":      ("🍳", "שיעורי בישול",        "הכנת ארוחות לשכנים, סדנאות בישול",     "50–120 ₪/שעה", "#f472b6"),
        "אחר":        ("⭐", "הכישרון הייחודי שלך", "מצא מה אתה טוב בו — שאל את ה-AI!",    "משתנה",        "#facc15"),
    },
    "en": {
        "Math":         ("📐", "Tutor",            "Lessons for peers & younger kids",      "$8–22/hr",     "#6ee7b7"),
        "English":      ("🗣️", "English Lessons",  "Conversation, reading, exam prep",       "$8–20/hr",     "#38bdf8"),
        "Coding":       ("💻", "Freelance Dev",    "Websites, bots — Fiverr / Upwork",       "$15–60/hr",    "#a78bfa"),
        "Music":        ("🎵", "Music Lessons",    "Guitar, piano, vocals",                  "$12–25/hr",    "#f472b6"),
        "Art/Design":   ("🎨", "Graphic Design",   "Logos, posters, social media content",   "$15–50/proj",  "#fb923c"),
        "Writing":      ("✍️", "Content Writing",  "Blogs, descriptions, summaries",         "$6–18/1k",     "#facc15"),
        "Sports/Fitness":("🏋️","Personal Trainer", "Personal & group training sessions",     "$12–28/hr",    "#34d399"),
        "Languages":    ("🌍", "Language Tutor",   "Spanish, French, Arabic & more",         "$10–22/hr",    "#60a5fa"),
        "Sciences":     ("🔬", "Science Tutor",    "Biology, chemistry, research papers",    "$10–22/hr",    "#6ee7b7"),
        "Cooking":      ("🍳", "Cooking Lessons",  "Cook for neighbors, workshops",           "$14–35/hr",    "#f472b6"),
        "Other":        ("⭐", "Your Unique Skill","Find what you're good at — ask the AI!", "Varies",       "#facc15"),
    }
}

STEPS_HE = [
    ("1️⃣", "קבע מחיר", "התחל נמוך כדי לבנות לקוחות, העלה עם הניסיון"),
    ("2️⃣", "פרסם בווצאפ/פייסבוק", "קבוצות שכונה, הורים, בית ספר"),
    ("3️⃣", "הצטרף ל-Fiverr/Upwork", "לתכנות, עיצוב, כתיבה"),
    ("4️⃣", "בקש ביקורות", "המלצות = עוד לקוחות"),
    ("5️⃣", "חסוך 20%", "קרן חירום / השקעה עתידית"),
]
STEPS_EN = [
    ("1️⃣", "Set a price", "Start low to build clients, raise as you gain experience"),
    ("2️⃣", "Post on WhatsApp/Facebook", "Neighborhood, parent & school groups"),
    ("3️⃣", "Join Fiverr/Upwork", "For coding, design, writing"),
    ("4️⃣", "Ask for reviews", "Testimonials = more clients"),
    ("5️⃣", "Save 20%", "Emergency fund / future investment"),
]


# ── Pillow card ───────────────────────────────────────────────────────────
def _make_card(name: str, skill: str, role: str, earn: str, icon: str, accent: str) -> bytes:
    W, H = 540, 280
    img  = Image.new("RGB", (W, H), color=(8, 11, 18))
    draw = ImageDraw.Draw(img)

    # accent bar top + left
    draw.rectangle([0, 0, W, 7], fill=accent)
    draw.rectangle([0, 0, 7, H], fill=accent)

    # bg rect
    draw.rectangle([7, 7, W - 1, H - 1], fill=(16, 21, 31))

    # icon
    draw.text((24, 22), icon, fill=accent)

    # name
    draw.text((24, 65), name or "Student", fill=(232, 237, 245))

    # role / skill
    draw.text((24, 105), f"{role}  ·  {skill}", fill=(90, 106, 130))

    # earn box
    draw.rectangle([24, 150, 210, 195], fill=(24, 31, 46), outline=accent, width=1)
    draw.text((34, 161), f"💰  {earn}", fill=accent)

    # studyflow watermark
    draw.text((W - 105, H - 26), "StudyFlow", fill=(30, 42, 61))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── Main render ───────────────────────────────────────────────────────────
def render(t):
    st.markdown(f'<div class="sf-section-title">{t("earn_title")}</div>', unsafe_allow_html=True)

    lang   = st.session_state.lang
    skills = SKILLS_HE if lang == "he" else SKILLS_EN
    ideas  = IDEAS[lang]
    steps  = STEPS_HE if lang == "he" else STEPS_EN

    selected = st.selectbox(
        "מה הכישרון שלך?" if lang == "he" else "What's your skill?",
        skills, key="earn_skill",
    )
    idea = ideas.get(selected)

    tab_ideas, tab_ikigai, tab_search, tab_card = st.tabs([
        t("earn_tab_ideas"),
        t("earn_tab_ikigai"),
        t("earn_tab_search"),
        t("earn_tab_card"),
    ])

    # ── Tab 1: Ideas ──────────────────────────────────────────────
    with tab_ideas:
        if idea:
            icon, role, desc, earn, accent = idea
            st.markdown(
                f'<div class="sf-card sf-card-glow" style="border-color:{accent}33;padding:1.8rem;text-align:center">'
                f'<div style="font-size:3rem">{icon}</div>'
                f'<div style="font-size:1.3rem;font-weight:800;color:{accent};margin:.5rem 0">{role}</div>'
                f'<div style="color:var(--muted)">{desc}</div>'
                f'<div style="font-family:Space Grotesk,monospace;font-size:1.4rem;'
                f'font-weight:700;color:{accent};margin-top:1rem">{earn}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="sf-section-title">{"איך מתחילים?" if lang=="he" else "How to start?"}</div>',
            unsafe_allow_html=True,
        )
        for ico, title, desc in steps:
            st.markdown(
                f'<div class="sf-card" style="padding:.9rem;margin-bottom:.5rem;display:flex;gap:1rem;align-items:flex-start">'
                f'<span style="font-size:1.3rem">{ico}</span>'
                f'<div><b>{title}</b><br><span style="color:var(--muted);font-size:.87rem">{desc}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Tab 2: Ikigai ─────────────────────────────────────────────
    with tab_ikigai:
        _render_ikigai(t, lang)

    # ── Tab 3: DuckDuckGo search ──────────────────────────────────
    with tab_search:
        st.markdown(
            f'<div style="color:var(--muted);margin-bottom:1rem">'
            + (f"חיפוש הזדמנויות הכנסה עדכניות עבור: <b>{selected}</b>"
               if lang == "he"
               else f"Searching latest earning opportunities for: <b>{selected}</b>")
            + "</div>",
            unsafe_allow_html=True,
        )
        if st.button(f"🔍 {'חפש הזדמנויות' if lang=='he' else 'Search Opportunities'}", type="primary", key="btn_earn_ddg"):
            q = (f"כיצד תלמיד יכול להרוויח כסף עם {selected} בישראל 2025"
                 if lang == "he"
                 else f"how student can earn money with {selected} online 2025")
            with st.spinner("🔍 DuckDuckGo…"):
                st.session_state.earn_ddg = ddg_search(q, max_results=5)
            st.rerun()

        if "earn_ddg" in st.session_state:
            for r in st.session_state.earn_ddg:
                href  = r.get("href", "")
                title = r.get("title", "")
                body  = r.get("body", "")
                st.markdown(
                    f'<div class="sf-card" style="padding:1rem;margin-bottom:.5rem">'
                    f'<b>{title}</b><br>'
                    f'<span style="color:var(--muted);font-size:.86rem">{body[:220]}…</span><br>'
                    + (f'<a href="{href}" target="_blank" style="color:var(--accent2);font-size:.8rem">🔗 {href[:60]}…</a>' if href else "")
                    + "</div>",
                    unsafe_allow_html=True,
                )

    # ── Tab 4: Skill Card (Pillow) ────────────────────────────────
    with tab_card:
        st.markdown(
            f'<div style="color:var(--muted);margin-bottom:1rem">'
            + ("צור כרטיס PNG אישי לשיתוף ברשתות החברתיות"
               if lang == "he"
               else "Generate a personal PNG card to share on social media")
            + "</div>",
            unsafe_allow_html=True,
        )
        name_input = st.text_input(
            "השם שלך" if lang == "he" else "Your name",
            placeholder="ישראל ישראלי" if lang == "he" else "Jane Doe",
            key="card_name",
        )
        if st.button(
            f"🎨 {'צור כרטיס' if lang=='he' else 'Generate Card'}",
            type="primary", key="btn_gen_card"
        ):
            icon, role, _, earn, accent = idea if idea else ("⭐", selected, "", "?", "#6ee7b7")
            with st.spinner("Pillow…"):
                png = _make_card(name_input, selected, role, earn, icon, accent)
            st.image(png, caption="📥 " + ("לחץ ימני לשמירה" if lang == "he" else "Right-click to save"))
            st.download_button(
                label=f"📥 {'הורד PNG' if lang=='he' else 'Download PNG'}",
                data=png,
                file_name=f"studyflow_skill_{selected.lower().replace(' ','_')}.png",
                mime="image/png",
                key="dl_card",
            )


# ── Ikigai sub-section ────────────────────────────────────────────────────
def _render_ikigai(t, lang):
    st.markdown(
        f'<div class="sf-card sf-card-accent3" style="margin-bottom:1.2rem">'
        f'<b>{"מה זה Ikigai?" if lang=="he" else "What is Ikigai?"}</b><br>'
        f'<span style="color:var(--muted);font-size:.88rem">'
        + ("מושג יפני שמשמעותו 'הסיבה לקום בבוקר'. המבחן עוזר לך למצוא את נקודת החיתוך בין: מה שאתה אוהב, מה שאתה טוב בו, מה שהעולם צריך, ומה שמשלמים עליו."
           if lang == "he" else
           "A Japanese concept meaning 'reason for being'. The test helps you find the intersection of: what you love, what you're good at, what the world needs, and what you can be paid for.")
        + "</span></div>",
        unsafe_allow_html=True,
    )

    st.markdown(f'<div style="font-size:2rem;text-align:center">🌸</div>', unsafe_allow_html=True)

    q1 = st.text_area(
        t("ikigai_q1"),
        placeholder="לדוגמה: מתמטיקה, תכנות, ציור" if lang == "he" else "e.g. Math, coding, drawing",
        key="iki_q1", height=80
    )
    q2 = st.text_area(
        t("ikigai_q2"),
        placeholder="לדוגמה: לשחק גיטרה, לעזור לחברים" if lang == "he" else "e.g. Playing guitar, helping friends",
        key="iki_q2", height=80
    )
    q3 = st.text_area(
        t("ikigai_q3"),
        placeholder="לדוגמה: חינוך, סביבה, בריאות" if lang == "he" else "e.g. Education, environment, health",
        key="iki_q3", height=80
    )
    q4 = st.text_area(
        t("ikigai_q4"),
        placeholder="לדוגמה: שיעורים פרטיים, עיצוב לוגו" if lang == "he" else "e.g. Tutoring, logo design",
        key="iki_q4", height=80
    )

    if st.button(t("ikigai_analyze"), type="primary", key="btn_ikigai"):
        if not any([q1, q2, q3, q4]):
            st.warning("מלא לפחות שאלה אחת" if lang == "he" else "Please fill in at least one answer")
        elif not get_api_key():
            st.warning(t("hw_api_missing"))
        else:
            user_text = (
                f"שאלות Ikigai שלי:\n"
                f"1. במה אני טוב: {q1}\n"
                f"2. מה אני אוהב: {q2}\n"
                f"3. מה העולם צריך: {q3}\n"
                f"4. על מה ישלמו לי: {q4}"
                if lang == "he" else
                f"My Ikigai answers:\n"
                f"1. What I'm good at: {q1}\n"
                f"2. What I love: {q2}\n"
                f"3. What the world needs: {q3}\n"
                f"4. What I can be paid for: {q4}"
            )
            sys = (
                "אתה מנחה Ikigai לתלמידי תיכון. קיבלת את תשובות הנסקר. "
                "1. זהה את ה-Ikigai שלו — נקודת החיתוך. "
                "2. הצע 2-3 מסלולים קריירה/הכנסה מתאימים לגיל תיכון. "
                "3. תן 2-3 צעדים ראשונים מעשיים. ענה בעברית, ידידותי ומעשי."
                if lang == "he" else
                "You are an Ikigai guide for high school students. "
                "1. Identify their Ikigai — the intersection point. "
                "2. Suggest 2-3 career/income paths suitable for high school age. "
                "3. Give 2-3 concrete first steps. Reply in English, friendly and practical."
            )
            with st.spinner(t("ikigai_thinking")):
                try:
                    result = call_gemini(
                        system_prompt=sys,
                        user_text=user_text,
                        max_tokens=1000,
                        temperature=0.75,
                    )
                    st.session_state.ikigai_result = result
                except Exception as e:
                    st.error(f"{t('error')}: {e}")

    if "ikigai_result" in st.session_state:
        st.markdown(
            f'<div class="sf-bubble-ai" style="margin-top:1rem">'
            f'<div class="sf-bubble-label">🌸 Ikigai Analysis</div>'
            f'{st.session_state.ikigai_result}</div>',
            unsafe_allow_html=True,
        )
        if st.button("🗑️ " + ("נקה" if lang == "he" else "Clear"), key="clear_ikigai"):
            del st.session_state.ikigai_result
            st.rerun()