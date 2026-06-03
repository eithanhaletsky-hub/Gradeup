"""pages/wellness.py — רווחה נפשית: מצב רוח, סטרס, נשימות, טיפים"""
import streamlit as st
from datetime import date, datetime
from ai_utils import call_gemini, get_api_key

MOODS_HE = ["😄 מצוין", "🙂 טוב", "😐 בסדר", "😔 קשה", "😰 לחוץ מאוד"]
MOODS_EN = ["😄 Great", "🙂 Good", "😐 Okay", "😔 Rough", "😰 Very stressed"]

STRESS_HE = ["😌 אפס סטרס", "🟡 קצת", "🟠 בינוני", "🔴 גבוה", "🆘 קריסה"]
STRESS_EN = ["😌 No stress", "🟡 A little", "🟠 Medium", "🔴 High", "🆘 Breaking point"]

TIPS_HE = [
    ("🧠", "כלל ה-5 שניות",         "כשאתה לחוץ — תספור 5,4,3,2,1 ועשה פעולה אחת קטנה. זה שובר את מעגל החרדה."),
    ("💤", "שינה = ביצועים",         "שינה של 8 שעות משפרת ציונים ב-20% בממוצע. אל תוותר על שינה לפני מבחן."),
    ("🏃", "20 דקות תנועה",          "פעילות גופנית קצרה מפחיתה קורטיזול (הורמון הסטרס) ומשפרת ריכוז."),
    ("📵", "Digital detox",          "שעה אחת ללא מסך לפני שינה משפרת את איכות השינה משמעותית."),
    ("✏️", "כתיבה חופשית 5 דקות",   "כתוב מה מטריד אותך. הוצאת המחשבות לנייר מפחיתה חרדה ב-30%."),
    ("🎵", "מוזיקה ולימוד",          "מוזיקה ללא מילים (לו-פי, קלאסי) מסייעת לריכוז. עם מילים — מפריעה."),
    ("🍎", "אכלת היום?",             "המוח צורך 20% מהאנרגיה של הגוף. דלג על ארוחות = פגיעה בריכוז ובזיכרון."),
    ("🤝", "דבר עם מישהו",           "שיתוף עם חבר, הורה או יועץ מפחית לחץ. אתה לא צריך לעבור את זה לבד."),
]
TIPS_EN = [
    ("🧠", "The 5-second rule",      "When stressed — count 5,4,3,2,1 and take one small action. It breaks the anxiety loop."),
    ("💤", "Sleep = performance",    "8 hours of sleep improves grades by 20% on average. Don't skip sleep before exams."),
    ("🏃", "20 min of movement",     "Short exercise lowers cortisol (stress hormone) and improves focus."),
    ("📵", "Digital detox",          "One screen-free hour before bed significantly improves sleep quality."),
    ("✏️", "5-min free writing",     "Write what's bothering you. Getting thoughts on paper reduces anxiety by 30%."),
    ("🎵", "Music & studying",       "Wordless music (lo-fi, classical) aids concentration. Music with lyrics — distracts."),
    ("🍎", "Did you eat today?",     "The brain uses 20% of the body's energy. Skip meals = hurt focus & memory."),
    ("🤝", "Talk to someone",        "Sharing with a friend, parent or counselor reduces stress. You don't have to go through it alone."),
]


def render(t):
    lang = st.session_state.lang
    st.markdown(
        f'<div class="sf-section-title">{t("wellness_title")}</div>',
        unsafe_allow_html=True,
    )

    # session defaults
    if "mood_log"   not in st.session_state: st.session_state.mood_log   = []
    if "stress_log" not in st.session_state: st.session_state.stress_log = []

    tab_mood, tab_stress, tab_breath, tab_tips = st.tabs([
        t("wellness_tab_mood"),
        t("wellness_tab_stress"),
        t("wellness_tab_breath"),
        t("wellness_tab_tips"),
    ])

    # ── Tab 1: Mood tracker ───────────────────────────────────────
    with tab_mood:
        moods = MOODS_HE if lang == "he" else MOODS_EN
        st.markdown(
            f'<div class="sf-section-title">{t("wellness_mood_q")}</div>',
            unsafe_allow_html=True,
        )
        selected_mood = st.radio("", moods, horizontal=True, key="mood_select", label_visibility="collapsed")

        mood_note = st.text_input(
            "מה עובר עליך היום? (אופציונלי)" if lang == "he" else "What's on your mind today? (optional)",
            key="mood_note_input", placeholder="(אופציונלי)"
        )

        if st.button(t("wellness_mood_save"), type="primary", key="btn_save_mood"):
            st.session_state.mood_log.append({
                "date":  str(date.today()),
                "time":  datetime.now().strftime("%H:%M"),
                "mood":  selected_mood,
                "note":  mood_note,
            })
            st.success(t("wellness_mood_saved"))
            st.rerun()

        # Mood history
        if st.session_state.mood_log:
            st.markdown("---")
            st.markdown(
                f'<div class="sf-section-title">{"היסטוריית מצב רוח" if lang=="he" else "Mood History"}</div>',
                unsafe_allow_html=True,
            )
            for entry in reversed(st.session_state.mood_log[-10:]):
                st.markdown(
                    f'<div class="sf-card" style="padding:.8rem;margin-bottom:.4rem">'
                    f'<b>{entry["mood"]}</b>'
                    f'<span style="color:var(--muted);font-size:.8rem"> — {entry["date"]} {entry["time"]}</span>'
                    + (f'<br><span style="color:var(--muted);font-size:.85rem">{entry["note"]}</span>' if entry.get("note") else "")
                    + "</div>",
                    unsafe_allow_html=True,
                )

    # ── Tab 2: Exam stress ────────────────────────────────────────
    with tab_stress:
        stress_opts = STRESS_HE if lang == "he" else STRESS_EN
        st.markdown(
            f'<div class="sf-section-title">{t("wellness_stress_q")}</div>',
            unsafe_allow_html=True,
        )
        stress_level = st.select_slider("", options=stress_opts, key="stress_slider", label_visibility="collapsed")
        stress_idx   = stress_opts.index(stress_level)

        # Visual stress meter
        meter_colors = ["#6ee7b7","#34d399","#facc15","#fb923c","#f87171"]
        meter_col    = meter_colors[stress_idx]
        filled       = "█" * (stress_idx + 1) + "░" * (4 - stress_idx)
        st.markdown(
            f'<div class="sf-card" style="border-color:{meter_col};text-align:center;padding:1.2rem">'
            f'<div style="font-family:monospace;font-size:1.5rem;color:{meter_col}">{filled}</div>'
            f'<div style="color:{meter_col};font-weight:700;margin-top:.4rem">{stress_level}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Context input
        context = st.text_area(
            "ספר קצת — מה גורם ללחץ?" if lang == "he" else "Tell me more — what's causing the stress?",
            key="stress_context", height=80,
            placeholder="מבחן מחר, לא הספקתי לחזור…" if lang == "he" else "Exam tomorrow, haven't studied enough…"
        )

        if st.button(t("wellness_ai_help"), type="primary", key="btn_stress_ai"):
            if not get_api_key():
                st.warning(t("hw_api_missing"))
            else:
                user_text = (
                    f"רמת לחץ: {stress_level} ({stress_idx+1}/5)\n"
                    f"הקשר: {context or 'לא פורט'}"
                    if lang == "he" else
                    f"Stress level: {stress_level} ({stress_idx+1}/5)\n"
                    f"Context: {context or 'Not specified'}"
                )
                sys = (
                    "אתה תומך רגשי לתלמיד תיכון שלחוץ ממבחנים. "
                    "תן: 1) הכרה בתחושה (אמפתיה), 2) טיפ פרקטי אחד ספציפי לסיטואציה, "
                    "3) תרגיל קצר לעכשיו (30 שניות). אל תטיף מוסר. ענה בעברית, קצר ואנושי."
                    if lang == "he" else
                    "You are an emotional support companion for a stressed high school student. "
                    "Give: 1) Acknowledge the feeling (empathy), 2) One specific practical tip for the situation, "
                    "3) A short exercise for right now (30 seconds). No lecturing. Reply in English, brief and human."
                )
                with st.spinner("🤖 " + ("חושב…" if lang == "he" else "Thinking…")):
                    try:
                        result = call_gemini(system_prompt=sys, user_text=user_text, max_tokens=600, temperature=0.8)
                        st.session_state.stress_ai = result
                    except Exception as e:
                        st.error(str(e))

        if "stress_ai" in st.session_state:
            st.markdown(
                f'<div class="sf-bubble-ai">'
                f'<div class="sf-bubble-label">{t("ai_label")}</div>'
                f'{st.session_state.stress_ai}</div>',
                unsafe_allow_html=True,
            )

    # ── Tab 3: Breathing exercise ─────────────────────────────────
    with tab_breath:
        st.markdown(
            f'<div class="sf-section-title">{t("wellness_breath_title")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sf-card sf-card-accent" style="margin-bottom:1.2rem">'
            f'<span style="color:var(--muted);font-size:.88rem">'
            + ("טכניקת 4-7-8: שאף 4 שניות → עצור 7 שניות → נשוף 8 שניות. "
               "3 מחזורים מפחיתים את קצב הלב תוך 2 דקות."
               if lang == "he" else
               "4-7-8 technique: Inhale 4 sec → Hold 7 sec → Exhale 8 sec. "
               "3 cycles reduce heart rate within 2 minutes.")
            + "</span></div>",
            unsafe_allow_html=True,
        )

        # JavaScript breathing animation
        st.markdown(
            f"""
            <div id="breath-card" style="text-align:center;padding:2.5rem;
              background:var(--surface);border:1px solid var(--border);border-radius:14px">
              <div id="breath-circle" style="
                width:120px;height:120px;border-radius:50%;
                background:radial-gradient(circle,#6ee7b722,#0d0f14);
                border:3px solid #6ee7b7;margin:0 auto 1.2rem;
                transition:all 0.5s ease;display:flex;align-items:center;justify-content:center;
                font-size:2rem">🌬️</div>
              <div id="breath-label" style="font-size:1.3rem;font-weight:700;color:#6ee7b7;
                margin-bottom:.5rem">{t("wellness_inhale")}</div>
              <div id="breath-counter" style="font-size:3rem;font-family:Space Grotesk,monospace;
                color:#e8edf5;font-weight:700">4</div>
              <div id="breath-cycles" style="color:#5a6a82;font-size:.85rem;margin:.8rem 0">
                {"מחזור" if lang=="he" else "Cycle"} <span id="cycle-num">0</span>/3
              </div>
              <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem">
                <button id="breath-btn" onclick="startBreath()"
                  style="background:linear-gradient(135deg,#064e3b,#0c4a6e);color:#6ee7b7;
                  border:1px solid #6ee7b7;padding:.6rem 2rem;border-radius:8px;
                  font-size:1rem;cursor:pointer;font-family:Heebo,sans-serif">
                  ▶ {t("wellness_start")}
                </button>
                <button onclick="resetBreath()"
                  style="background:#1e2636;color:#e8edf5;border:1px solid #2d3748;
                  padding:.6rem 1.2rem;border-radius:8px;font-size:1rem;cursor:pointer">
                  ↺
                </button>
              </div>
            </div>

            <script>
            let bInterval=null, bPhase=0, bCount=0, bCycles=0, bRunning=false;
            const phases=[
              {{dur:4, label:"{t("wellness_inhale")}", scale:"scale(1.35)", col:"#6ee7b7"}},
              {{dur:7, label:"{t("wellness_hold")}",   scale:"scale(1.35)", col:"#38bdf8"}},
              {{dur:8, label:"{t("wellness_exhale")}", scale:"scale(0.85)", col:"#f472b6"}},
            ];

            function startBreath(){{
              if(bRunning)return;
              bRunning=true;
              document.getElementById("breath-btn").disabled=true;
              runPhase();
            }}
            function runPhase(){{
              if(bCycles>=3){{ resetBreath(); return; }}
              const p=phases[bPhase];
              document.getElementById("breath-label").innerText=p.label;
              document.getElementById("breath-label").style.color=p.col;
              document.getElementById("breath-circle").style.transform=p.scale;
              document.getElementById("breath-circle").style.borderColor=p.col;
              bCount=p.dur;
              document.getElementById("breath-counter").innerText=bCount;
              bInterval=setInterval(()=>{{
                bCount--;
                document.getElementById("breath-counter").innerText=bCount;
                if(bCount<=0){{
                  clearInterval(bInterval);
                  bPhase=(bPhase+1)%3;
                  if(bPhase===0) bCycles++;
                  document.getElementById("cycle-num").innerText=bCycles;
                  if(bCycles<3) runPhase();
                  else resetBreath(true);
                }}
              }},1000);
            }}
            function resetBreath(done=false){{
              clearInterval(bInterval);
              bRunning=false; bPhase=0; bCount=0;
              if(!done) bCycles=0;
              document.getElementById("breath-circle").style.transform="scale(1)";
              document.getElementById("breath-circle").style.borderColor="#6ee7b7";
              document.getElementById("breath-label").innerText=done
                ? "{'כל הכבוד! 🎉' if lang=='he' else 'Well done! 🎉'}"
                : "{t('wellness_inhale')}";
              document.getElementById("breath-counter").innerText=done ? "✓" : "4";
              document.getElementById("breath-btn").disabled=false;
              if(!done) document.getElementById("cycle-num").innerText="0";
            }}
            </script>
            """,
            unsafe_allow_html=True,
        )

    # ── Tab 4: Tips ───────────────────────────────────────────────
    with tab_tips:
        tips = TIPS_HE if lang == "he" else TIPS_EN
        st.markdown(
            f'<div class="sf-section-title">'
            + ("💡 טיפים לשמירה על שפיות" if lang == "he" else "💡 Tips to Stay Sane")
            + "</div>",
            unsafe_allow_html=True,
        )
        for icon, title, desc in tips:
            st.markdown(
                f'<div class="sf-card sf-card-accent2" style="padding:1rem;margin-bottom:.6rem;'
                f'display:flex;gap:1rem;align-items:flex-start">'
                f'<span style="font-size:1.6rem">{icon}</span>'
                f'<div><b>{title}</b><br>'
                f'<span style="color:var(--muted);font-size:.87rem">{desc}</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        # AI personalized tip
        st.markdown("---")
        st.markdown(
            f'<div class="sf-section-title">'
            + ("🤖 טיפ מותאם אישית" if lang == "he" else "🤖 Personalized Tip")
            + "</div>",
            unsafe_allow_html=True,
        )
        situation = st.text_input(
            "ספר על המצב שלך עכשיו:" if lang == "he" else "Describe your current situation:",
            placeholder="לחוץ ממבחן מחר, לא ישנתי טוב…" if lang == "he" else "Stressed about tomorrow's test, didn't sleep well…",
            key="wellness_custom_tip",
        )
        if st.button("🤖 " + ("קבל טיפ" if lang == "he" else "Get Tip"), type="primary", key="btn_custom_tip"):
            if not get_api_key():
                st.warning(t("hw_api_missing"))
            elif not situation.strip():
                st.warning("ספר קצת על המצב שלך" if lang == "he" else "Please describe your situation")
            else:
                sys = (
                    "אתה חבר תומך לתלמיד תיכון. תן טיפ אחד קצר, ספציפי ומעשי לסיטואציה. "
                    "לא יותר מ-3 משפטים. אנושי ולא מדקדקני. ענה בעברית."
                    if lang == "he" else
                    "You are a supportive friend to a high school student. Give one short, specific and practical tip for the situation. "
                    "No more than 3 sentences. Human and non-preachy. Reply in English."
                )
                with st.spinner("🤖…"):
                    try:
                        tip = call_gemini(system_prompt=sys, user_text=situation, max_tokens=250, temperature=0.85)
                        st.markdown(
                            f'<div class="sf-bubble-ai">'
                            f'<div class="sf-bubble-label">{t("ai_label")}</div>'
                            f'{tip}</div>',
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.error(str(e))