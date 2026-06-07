"""
translations.py — מערכת תרגום דו-לשונית מלאה ל-Gradeup
שימוש:
    from translations import T
    text = T("home_title")          # לפי st.session_state.lang
    text = T("home_title", "en")   # כפיית שפה
"""
import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════
#  TRANSLATIONS DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════
TRANSLATIONS: dict[str, dict[str, str]] = {

    # ─── App / General ────────────────────────────────────────────────────
    "app_name":             {"he": "Gradeup",                        "en": "Gradeup"},
    "app_tagline":          {"he": "לומדים חכם, עולים קדימה",        "en": "Study smart, level up"},
    "app_target":           {"he": "לתלמידי חטיבה ותיכון",           "en": "For middle & high school students"},
    "app_footer":           {"he": "Gradeup v1.0 © 2025 | gradeup.co.il", "en": "Gradeup v1.0 © 2025 | gradeup.co.il"},

    # ─── Common actions ───────────────────────────────────────────────────
    "add":                  {"he": "הוסף",            "en": "Add"},
    "save":                 {"he": "שמור",            "en": "Save"},
    "delete":               {"he": "מחק",             "en": "Delete"},
    "clear":                {"he": "נקה",             "en": "Clear"},
    "clear_all":            {"he": "נקה הכל",         "en": "Clear all"},
    "search":               {"he": "חפש",             "en": "Search"},
    "send":                 {"he": "שלח",             "en": "Send"},
    "cancel":               {"he": "בטל",             "en": "Cancel"},
    "back":                 {"he": "חזרה",            "en": "Back"},
    "next":                 {"he": "הבא",             "en": "Next"},
    "open":                 {"he": "פתח",             "en": "Open"},
    "close":                {"he": "סגור",            "en": "Close"},
    "export":               {"he": "ייצוא",           "en": "Export"},
    "download":             {"he": "הורד",            "en": "Download"},
    "upload":               {"he": "העלה",            "en": "Upload"},
    "generate":             {"he": "צור",             "en": "Generate"},
    "analyze":              {"he": "נתח",             "en": "Analyze"},
    "reset":                {"he": "אפס",             "en": "Reset"},
    "edit":                 {"he": "ערוך",            "en": "Edit"},
    "confirm":              {"he": "אשר",             "en": "Confirm"},

    # ─── Common status ────────────────────────────────────────────────────
    "success":              {"he": "בוצע בהצלחה!",   "en": "Done!"},
    "error":                {"he": "שגיאה",           "en": "Error"},
    "loading":              {"he": "טוען…",           "en": "Loading…"},
    "thinking":             {"he": "חושב…",           "en": "Thinking…"},
    "no_data":              {"he": "אין נתונים עדיין","en": "No data yet"},
    "optional":             {"he": "(אופציונלי)",     "en": "(optional)"},
    "required":             {"he": "שדה חובה",        "en": "Required field"},

    # ─── Common labels ────────────────────────────────────────────────────
    "subject":              {"he": "מקצוע",           "en": "Subject"},
    "date":                 {"he": "תאריך",           "en": "Date"},
    "time":                 {"he": "שעה",             "en": "Time"},
    "day":                  {"he": "יום",             "en": "Day"},
    "name":                 {"he": "שם",              "en": "Name"},
    "description":          {"he": "תיאור",           "en": "Description"},
    "note":                 {"he": "הערה",            "en": "Note"},
    "type":                 {"he": "סוג",             "en": "Type"},
    "category":             {"he": "קטגוריה",         "en": "Category"},
    "score":                {"he": "ציון",            "en": "Score"},
    "average":              {"he": "ממוצע",           "en": "Average"},
    "total":                {"he": "סה\"כ",           "en": "Total"},
    "amount":               {"he": "סכום",            "en": "Amount"},
    "priority":             {"he": "עדיפות",          "en": "Priority"},
    "status":               {"he": "סטטוס",           "en": "Status"},
    "progress":             {"he": "התקדמות",         "en": "Progress"},
    "target":               {"he": "יעד",             "en": "Target"},
    "result":               {"he": "תוצאה",           "en": "Result"},
    "history":              {"he": "היסטוריה",        "en": "History"},
    "all":                  {"he": "הכל",             "en": "All"},
    "other":                {"he": "אחר",             "en": "Other"},
    "filter":               {"he": "סנן",             "en": "Filter"},
    "sort":                 {"he": "מיין",            "en": "Sort"},

    # ─── Days of week ─────────────────────────────────────────────────────
    "day_sun":              {"he": "ראשון",   "en": "Sunday"},
    "day_mon":              {"he": "שני",     "en": "Monday"},
    "day_tue":              {"he": "שלישי",   "en": "Tuesday"},
    "day_wed":              {"he": "רביעי",   "en": "Wednesday"},
    "day_thu":              {"he": "חמישי",   "en": "Thursday"},
    "day_fri":              {"he": "שישי",    "en": "Friday"},
    "day_sat":              {"he": "שבת",     "en": "Saturday"},

    # ─── Priority levels ──────────────────────────────────────────────────
    "priority_high":        {"he": "🔴 גבוהה",   "en": "🔴 High"},
    "priority_med":         {"he": "🟡 בינונית",  "en": "🟡 Medium"},
    "priority_low":         {"he": "🟢 נמוכה",   "en": "🟢 Low"},

    # ─── Auth ─────────────────────────────────────────────────────────────
    "auth_login":           {"he": "כניסה",                                "en": "Log In"},
    "auth_signup":          {"he": "הרשמה",                               "en": "Sign Up"},
    "auth_logout":          {"he": "התנתק",                               "en": "Log Out"},
    "auth_username":        {"he": "שם משתמש",                           "en": "Username"},
    "auth_email":           {"he": "אימייל",                             "en": "Email"},
    "auth_password":        {"he": "סיסמה",                              "en": "Password"},
    "auth_confirm_pw":      {"he": "אימות סיסמה",                        "en": "Confirm password"},
    "auth_grade":           {"he": "כיתה",                               "en": "Grade"},
    "auth_agree_terms":     {"he": "אני מאשר את תנאי השימוש",           "en": "I agree to the terms of service"},
    "auth_wall_sub":        {"he": "הרשם או התחבר כדי להמשיך",          "en": "Sign up or log in to continue"},
    "auth_pw_hint":         {"he": "לפחות 6 תווים + ספרה",              "en": "At least 6 chars + digit"},
    "auth_err_short_user":  {"he": "שם משתמש חייב להכיל לפחות 2 תווים","en": "Username must be at least 2 characters"},
    "auth_err_email":       {"he": "אימייל לא תקין",                    "en": "Invalid email address"},
    "auth_err_taken":       {"he": "שם המשתמש תפוס",                    "en": "Username already taken"},
    "auth_err_email_taken": {"he": "האימייל כבר רשום",                  "en": "Email already registered"},
    "auth_err_pw_mismatch": {"he": "הסיסמאות לא תואמות",               "en": "Passwords do not match"},
    "auth_err_wrong":       {"he": "שם משתמש או סיסמה שגויים",         "en": "Incorrect username or password"},
    "auth_plan_free":       {"he": "🆓 Free",  "en": "🆓 Free"},
    "auth_plan_pro":        {"he": "⭐ Pro",   "en": "⭐ Pro"},

    # ─── Settings / API ───────────────────────────────────────────────────
    "settings_title":       {"he": "⚙️ הגדרות",                        "en": "⚙️ Settings"},
    "api_key_label":        {"he": "Gemini API Key",                    "en": "Gemini API Key"},
    "api_key_help":         {"he": "קבל מפתח חינמי: aistudio.google.com","en": "Get free key: aistudio.google.com"},
    "api_saved":            {"he": "✅ מפתח נשמר",                     "en": "✅ Key saved"},
    "api_from_env":         {"he": "✅ מפתח נטען מ-.env",              "en": "✅ Key loaded from .env"},
    "api_missing":          {"he": "יש להזין Gemini API Key בהגדרות", "en": "Please add a Gemini API Key in Settings"},

    # ─── Navigation ───────────────────────────────────────────────────────
    "nav_home":             {"he": "🏠 ראשי",                "en": "🏠 Home"},
    "nav_group_study":      {"he": "📚 לימודים",             "en": "📚 Study"},
    "nav_schedule":         {"he": "🗓️ מערכת שעות",          "en": "🗓️ Schedule"},
    "nav_homework":         {"he": "📚 עוזר שיעורי בית",     "en": "📚 Homework Bot"},
    "nav_flashcards":       {"he": "🃏 כרטיסיות",            "en": "🃏 Flashcards"},
    "nav_summarizer":       {"he": "📝 מסכם חומר",           "en": "📝 Summarizer"},
    "nav_science":          {"he": "🔬 מחשבון מדעי",         "en": "🔬 Science Calc"},
    "nav_translator":       {"he": "🌍 מתרגם חכם",           "en": "🌍 Translator"},
    "nav_group_track":      {"he": "📊 מעקב",                "en": "📊 Track"},
    "nav_grades":           {"he": "📊 מעקב ציונים",         "en": "📊 Grade Tracker"},
    "nav_bagrut":           {"he": "🎓 מחשבון בגרות",        "en": "🎓 Bagrut Calc"},
    "nav_goals":            {"he": "🎯 מעקב יעדים",          "en": "🎯 Goals"},
    "nav_group_career":     {"he": "💼 קריירה וכסף",         "en": "💼 Career & Money"},
    "nav_earn":             {"he": "💼 הכנסה & Ikigai",      "en": "💼 Earn & Ikigai"},
    "nav_budget":           {"he": "💰 תקציב חודשי",         "en": "💰 Budget"},
    "nav_scholarships":     {"he": "🏆 מלגות וקורסים",       "en": "🏆 Scholarships"},
    "nav_projects":         {"he": "💡 מחולל פרויקטים",      "en": "💡 Projects"},
    "nav_group_wellness":   {"he": "💆 רווחה",               "en": "💆 Wellness"},
    "nav_wellness":         {"he": "💆 רווחה נפשית",         "en": "💆 Wellness"},
    "nav_qa":               {"he": "👥 לוח שאלות",           "en": "👥 Q&A Board"},

    # ─── Home page ────────────────────────────────────────────────────────
    "home_hero_sub":        {"he": "הכלי שתמיד רצית — לומד, עוקב, מרוויח, מרגיש טוב",
                             "en": "The tool you always wanted — study, track, earn, feel good"},
    "home_get_started":     {"he": "בואו נתחיל",             "en": "Get Started"},
    "home_pages_count":     {"he": "דפים",                   "en": "Pages"},
    "home_ages":            {"he": "גילאים",                 "en": "Ages"},
    "home_per_month":       {"he": "לחודש",                  "en": "/month"},
    "home_libs_title":      {"he": "ספריות שבשימוש:",        "en": "Libraries used:"},
    "home_ready":           {"he": "מוכן להתחיל?",           "en": "Ready to start?"},
    "home_sidebar_hint":    {"he": "בחר דף מהתפריט הצדדי — מחולק לפי קטגוריות",
                             "en": "Choose a page from the sidebar — organized by category"},
    "home_pricing_title":   {"he": "💳 תמחור",               "en": "💳 Pricing"},
    "home_plan_free":       {"he": "חינמי",                  "en": "Free"},
    "home_plan_pro":        {"he": "Pro ⭐",                  "en": "Pro ⭐"},
    "home_plan_pro_price":  {"he": "₪ לחודש",               "en": "₪ / month"},
    "home_open_page":       {"he": "→ פתח",                  "en": "→ Open"},

    # ─── Schedule ─────────────────────────────────────────────────────────
    "sched_title":          {"he": "מערכת שעות חכמה",            "en": "Smart Schedule"},
    "sched_tab_view":       {"he": "📊 לוח שבועי",               "en": "📊 Weekly View"},
    "sched_tab_school":     {"he": "🏫 שיעורים/מבחנים",          "en": "🏫 School"},
    "sched_tab_personal":   {"he": "🎯 אירועים אישיים",          "en": "🎯 Personal Events"},
    "sched_tab_tasks":      {"he": "📋 משימות",                  "en": "📋 Tasks"},
    "sched_tab_ai":         {"he": "🤖 ניתוח AI",                "en": "🤖 AI Analysis"},
    "sched_start":          {"he": "שעת התחלה",                  "en": "Start time"},
    "sched_end":            {"he": "שעת סיום",                   "en": "End time"},
    "sched_teacher":        {"he": "מורה",                       "en": "Teacher"},
    "sched_room":           {"he": "חדר",                        "en": "Room"},
    "sched_location":       {"he": "מיקום",                      "en": "Location"},
    "sched_class":          {"he": "שיעור",                      "en": "Class"},
    "sched_exam":           {"he": "מבחן",                       "en": "Exam"},
    "sched_activity":       {"he": "חוג / פעילות",              "en": "Activity"},
    "sched_personal_event": {"he": "אירוע אישי",                 "en": "Personal event"},
    "sched_social":         {"he": "חברתי",                      "en": "Social"},
    "sched_medical":        {"he": "רפואי",                      "en": "Medical"},
    "sched_filter_type":    {"he": "סנן לפי סוג",               "en": "Filter by type"},
    "sched_filter_day":     {"he": "ימים",                       "en": "Days"},
    "sched_export_json":    {"he": "📥 ייצא JSON",               "en": "📥 Export JSON"},
    "sched_no_items":       {"he": "אין פריטים — הוסף בטאבים",  "en": "No items — add in tabs above"},
    "sched_ai_prompt":      {"he": "נתח את מערכת השעות שלי",     "en": "Analyze my schedule"},

    # ─── Homework Bot ─────────────────────────────────────────────────────
    "hw_title":             {"he": "עוזר שיעורי בית",          "en": "Homework Bot"},
    "hw_subject":           {"he": "בחר מקצוע",               "en": "Choose subject"},
    "hw_mode":              {"he": "סוג עזרה",                 "en": "Help mode"},
    "hw_mode_explain":      {"he": "הסבר נושא",               "en": "Explain topic"},
    "hw_mode_solve":        {"he": "עזור לפתור",              "en": "Help solve"},
    "hw_mode_summary":      {"he": "סכם חומר",                "en": "Summarize"},
    "hw_mode_exam":         {"he": "שאלות מבחן",              "en": "Exam questions"},
    "hw_image_upload":      {"he": "📸 העלה תמונה של השאלה",   "en": "📸 Upload question image"},
    "hw_ddg_toggle":        {"he": "🔍 חיפוש DuckDuckGo",     "en": "🔍 DuckDuckGo search"},
    "hw_placeholder":       {"he": "שאל שאלה, הדבק תרגיל…",  "en": "Ask a question, paste exercise…"},
    "hw_welcome":           {"he": "שלום! שאל אותי כל שאלה בלימודים 📖", "en": "Hi! Ask me anything about your studies 📖"},
    "hw_clear_chat":        {"he": "🗑️ נקה שיחה",             "en": "🗑️ Clear Chat"},
    "hw_you":               {"he": "אתה",                     "en": "You"},
    "hw_ai_label":          {"he": "🤖 Gradeup AI",           "en": "🤖 Gradeup AI"},
    "hw_search_results":    {"he": "תוצאות DuckDuckGo",       "en": "DuckDuckGo results"},
    "hw_quick_prompts":     {"he": "שאלות מהירות:",           "en": "Quick prompts:"},

    # ─── Flashcards ───────────────────────────────────────────────────────
    "fc_title":             {"he": "כרטיסיות לימוד",          "en": "Flashcards"},
    "fc_tab_study":         {"he": "📖 תרגול",                "en": "📖 Study"},
    "fc_tab_create":        {"he": "➕ צור כרטיסייה",         "en": "➕ Create Card"},
    "fc_tab_ai":            {"he": "🤖 AI מייצר",             "en": "🤖 AI Generate"},
    "fc_tab_manage":        {"he": "🗂️ ניהול",               "en": "🗂️ Manage"},
    "fc_question":          {"he": "שאלה",                    "en": "Question"},
    "fc_answer":            {"he": "תשובה",                   "en": "Answer"},
    "fc_flip":              {"he": "🔄 הפוך",                 "en": "🔄 Flip"},
    "fc_knew":              {"he": "✅ ידעתי",                "en": "✅ Got it"},
    "fc_missed":            {"he": "❌ לא ידעתי",             "en": "❌ Missed it"},
    "fc_shuffle":           {"he": "🔀 ערבב",                 "en": "🔀 Shuffle"},
    "fc_restart":           {"he": "🔁 התחל מחדש",           "en": "🔁 Restart"},
    "fc_done":              {"he": "🎉 סיימת את כל הכרטיסיות!", "en": "🎉 You finished all cards!"},
    "fc_score":             {"he": "תוצאה",                   "en": "Score"},
    "fc_cards":             {"he": "כרטיסיות",               "en": "cards"},
    "fc_no_cards":          {"he": "אין כרטיסיות — צור או ייצר עם AI", "en": "No cards — create or generate with AI"},
    "fc_ai_paste":          {"he": "הדבק טקסט — AI יצור כרטיסיות", "en": "Paste text — AI will generate cards"},
    "fc_ai_generate":       {"he": "🤖 צור כרטיסיות",        "en": "🤖 Generate Cards"},
    "fc_ai_count":          {"he": "כמה כרטיסיות?",          "en": "How many cards?"},
    "fc_deck_select":       {"he": "בחר חפיסה",              "en": "Select deck"},

    # ─── Summarizer ───────────────────────────────────────────────────────
    "sum_title":            {"he": "מסכם חומר חכם",               "en": "Smart Summarizer"},
    "sum_tab_text":         {"he": "📋 הדבק טקסט",               "en": "📋 Paste Text"},
    "sum_tab_history":      {"he": "📚 היסטוריה",                 "en": "📚 History"},
    "sum_paste_label":      {"he": "הדבק טקסט לסיכום:",          "en": "Paste text to summarize:"},
    "sum_subject_label":    {"he": "מקצוע (לכותרת)",             "en": "Subject (for title)"},
    "sum_style":            {"he": "סגנון סיכום",                 "en": "Summary style"},
    "sum_style_bullets":    {"he": "נקודות מרכזיות",             "en": "Key bullets"},
    "sum_style_narrative":  {"he": "סיפורי / קריא",              "en": "Narrative / readable"},
    "sum_style_exam":       {"he": "שאלות מבחן",                 "en": "Exam questions"},
    "sum_style_terms":      {"he": "מושגי מפתח",                 "en": "Key terms"},
    "sum_go":               {"he": "📝 סכם!",                    "en": "📝 Summarize!"},
    "sum_export_pdf":       {"he": "📥 ייצא PDF",                "en": "📥 Export PDF"},
    "sum_chars":            {"he": "תווים",                      "en": "chars"},
    "sum_words":            {"he": "מילים",                      "en": "words"},
    "sum_no_history":       {"he": "אין סיכומים עדיין",          "en": "No summaries yet"},
    "sum_history_count":    {"he": "סיכומים שמורים",             "en": "Saved summaries"},
    "sum_avg_words":        {"he": "ממוצע מילים",                "en": "Avg words"},
    "sum_top_subject":      {"he": "מקצוע מוביל",               "en": "Top subject"},

    # ─── Science Calculator ───────────────────────────────────────────────
    "sci_title":            {"he": "מחשבון מדעי",              "en": "Science Calculator"},
    "sci_tab_calc":         {"he": "🧮 חישוב",                 "en": "🧮 Calculate"},
    "sci_tab_formulas":     {"he": "📐 נוסחאות",              "en": "📐 Formulas"},
    "sci_tab_history":      {"he": "📚 היסטוריה",             "en": "📚 History"},
    "sci_input":            {"he": "הכנס ביטוי או משוואה",    "en": "Enter expression or equation"},
    "sci_placeholder":      {"he": "x**2 - 5*x + 6 = 0  |  sin(x)*x  |  x**3", "en": "x**2 - 5*x + 6 = 0  |  sin(x)*x  |  x**3"},
    "sci_mode_solve":       {"he": "פתור משוואה",             "en": "Solve equation"},
    "sci_mode_derive":      {"he": "נגזרת",                   "en": "Derivative"},
    "sci_mode_integrate":   {"he": "אינטגרל",                 "en": "Integral"},
    "sci_mode_simplify":    {"he": "פשט ביטוי",              "en": "Simplify"},
    "sci_mode_graph":       {"he": "שרטט גרף",               "en": "Plot graph"},
    "sci_calculate":        {"he": "🔬 חשב",                  "en": "🔬 Calculate"},
    "sci_ai_explain":       {"he": "🤖 הסבר AI",              "en": "🤖 AI Explain"},
    "sci_step_by_step":     {"he": "פתרון צעד-אחר-צעד",      "en": "Step-by-step solution"},
    "sci_no_history":       {"he": "אין חישובים עדיין",      "en": "No calculations yet"},
    "sci_calcs_count":      {"he": "חישובים",                 "en": "calculations"},

    # ─── Translator ───────────────────────────────────────────────────────
    "tr_title":             {"he": "מתרגם חכם",               "en": "Smart Translator"},
    "tr_tab_translate":     {"he": "🔄 תרגום",                "en": "🔄 Translate"},
    "tr_tab_history":       {"he": "📚 היסטוריה",             "en": "📚 History"},
    "tr_from":              {"he": "משפה",                    "en": "From"},
    "tr_to":                {"he": "לשפה",                    "en": "To"},
    "tr_swap":              {"he": "⇄ החלף",                  "en": "⇄ Swap"},
    "tr_text_label":        {"he": "טקסט לתרגום",            "en": "Text to translate"},
    "tr_placeholder":       {"he": "הכנס טקסט כאן…",         "en": "Enter text here…"},
    "tr_grammar":           {"he": "📖 דקדוק",               "en": "📖 Grammar"},
    "tr_examples":          {"he": "💬 דוגמאות",             "en": "💬 Examples"},
    "tr_formal":            {"he": "🎩 פורמלי",              "en": "🎩 Formal"},
    "tr_translate_btn":     {"he": "🔄 תרגם",                "en": "🔄 Translate"},
    "tr_save_flashcard":    {"he": "🃏 שמור ככרטיסייה",      "en": "🃏 Save as flashcard"},
    "tr_no_history":        {"he": "אין תרגומים עדיין",      "en": "No translations yet"},
    "tr_translations_count":{"he": "תרגומים",                "en": "Translations"},
    "tr_most_common":       {"he": "שכיח",                   "en": "Most common"},
    "tr_avg_chars":         {"he": "ממוצע תווים",            "en": "Avg chars"},
    "tr_input_label":       {"he": "קלט",                    "en": "Input"},

    # ─── Grade Tracker ────────────────────────────────────────────────────
    "grades_title":         {"he": "מעקב ציונים",             "en": "Grade Tracker"},
    "grades_tab_enter":     {"he": "✏️ הכנס ציון",           "en": "✏️ Enter Grade"},
    "grades_tab_overview":  {"he": "📈 סקירה",               "en": "📈 Overview"},
    "grades_tab_ai":        {"he": "🤖 ניתוח AI",            "en": "🤖 AI Analysis"},
    "grades_score":         {"he": "ציון",                   "en": "Score"},
    "grades_max":           {"he": "מתוך",                   "en": "Out of"},
    "grades_type_test":     {"he": "מבחן",                   "en": "Test"},
    "grades_type_quiz":     {"he": "בוחן",                   "en": "Quiz"},
    "grades_type_hw":       {"he": "שיעורי בית",             "en": "Homework"},
    "grades_type_project":  {"he": "פרויקט",                 "en": "Project"},
    "grades_type_oral":     {"he": "בעל-פה",                 "en": "Oral"},
    "grades_overall_avg":   {"he": "ממוצע כללי",             "en": "Overall avg"},
    "grades_strongest":     {"he": "הכי חזק",               "en": "Strongest"},
    "grades_weakest":       {"he": "צריך חיזוק",            "en": "Needs work"},
    "grades_no_data":       {"he": "אין ציונים עדיין — הכנס ציון ראשון!", "en": "No grades yet — add your first grade!"},
    "grades_ai_prompt":     {"he": "נתח את הציונים שלי",    "en": "Analyze my grades"},
    "grades_trend_up":      {"he": "מגמה עולה ✅",          "en": "Trending up ✅"},
    "grades_trend_down":    {"he": "מגמה יורדת ⚠️",         "en": "Trending down ⚠️"},
    "grades_avg_by_subject":{"he": "ממוצע לפי מקצוע",       "en": "Average by subject"},
    "grades_trend_over_time":{"he": "מגמה לאורך זמן",       "en": "Trend over time"},

    # ─── Bagrut Calculator ────────────────────────────────────────────────
    "bag_title":            {"he": "מחשבון בגרות",            "en": "Bagrut Calculator"},
    "bag_tab_calc":         {"he": "🧮 חישוב",               "en": "🧮 Calculate"},
    "bag_tab_sim":          {"he": "🎯 סימולציה",            "en": "🎯 Simulation"},
    "bag_tab_export":       {"he": "📥 ייצוא",               "en": "📥 Export"},
    "bag_units":            {"he": "יחידות לימוד",           "en": "Study units"},
    "bag_school_grade":     {"he": "ציון בית ספר",           "en": "School grade"},
    "bag_bagrut_grade":     {"he": "ציון בגרות",             "en": "Bagrut grade"},
    "bag_combined":         {"he": "משוקלל",                 "en": "Combined"},
    "bag_overall_avg":      {"he": "ממוצע כולל",             "en": "Overall average"},
    "bag_target_avg":       {"he": "יעד ממוצע",             "en": "Target average"},
    "bag_needed_grade":     {"he": "ציון נדרש",              "en": "Required grade"},
    "bag_add_subject":      {"he": "הוסף מקצוע",            "en": "Add subject"},
    "bag_improve_subject":  {"he": "מקצוע לשיפור",          "en": "Subject to improve"},
    "bag_impossible":       {"he": "בלתי אפשרי",            "en": "Impossible"},
    "bag_lower_target":     {"he": "הורד את היעד או שפר מקצועות נוספים", "en": "Lower the target or improve multiple subjects"},
    "bag_no_subjects":      {"he": "הוסף מקצועות לחישוב",  "en": "Add subjects to calculate"},
    "bag_current_grade":    {"he": "ציון נוכחי",            "en": "Current grade"},

    # ─── Goals ────────────────────────────────────────────────────────────
    "goals_title":          {"he": "מעקב יעדים",              "en": "Goals Tracker"},
    "goals_tab_active":     {"he": "🎯 יעדים פעילים",        "en": "🎯 Active Goals"},
    "goals_tab_add":        {"he": "➕ הוסף יעד",            "en": "➕ Add Goal"},
    "goals_tab_report":     {"he": "📊 דוח שבועי",           "en": "📊 Weekly Report"},
    "goals_name":           {"he": "שם היעד",                "en": "Goal name"},
    "goals_type":           {"he": "סוג יעד",                "en": "Goal type"},
    "goals_type_grade":     {"he": "📊 ציון מינימום",        "en": "📊 Minimum grade"},
    "goals_type_habit":     {"he": "🔄 הרגל יומי",          "en": "🔄 Daily habit"},
    "goals_type_money":     {"he": "💰 חיסכון כסף",         "en": "💰 Money saving"},
    "goals_type_study":     {"he": "📚 שעות לימוד",         "en": "📚 Study hours"},
    "goals_type_exercise":  {"he": "🏃 פעילות גופנית",      "en": "🏃 Exercise"},
    "goals_type_other":     {"he": "🎯 אחר",                "en": "🎯 Other"},
    "goals_target":         {"he": "יעד",                   "en": "Target"},
    "goals_current":        {"he": "התקדמות נוכחית",        "en": "Current progress"},
    "goals_unit":           {"he": "יחידה",                  "en": "Unit"},
    "goals_deadline":       {"he": "תאריך יעד",             "en": "Deadline"},
    "goals_update":         {"he": "עדכן התקדמות",          "en": "Update progress"},
    "goals_mark_done":      {"he": "🏆 סמן כהושלם",         "en": "🏆 Mark done"},
    "goals_completed":      {"he": "🏆 הושלם!",            "en": "🏆 Completed!"},
    "goals_active_count":   {"he": "פעילים",                "en": "active"},
    "goals_done_count":     {"he": "הושלמו",                "en": "completed"},
    "goals_no_goals":       {"he": "אין יעדים פעילים — הוסף יעד ראשון!", "en": "No active goals — add your first!"},
    "goals_ai_report":      {"he": "🤖 קבל דוח AI שבועי",  "en": "🤖 Get AI Weekly Report"},
    "goals_avg_progress":   {"he": "ממוצע התקדמות",         "en": "Avg progress"},
    "goals_in_progress":    {"he": "בתהליך",                "en": "In progress"},

    # ─── Earn & Ikigai ────────────────────────────────────────────────────
    "earn_title":           {"he": "הכנסה & Ikigai",              "en": "Earn & Ikigai"},
    "earn_tab_ideas":       {"he": "💡 רעיונות הכנסה",           "en": "💡 Income Ideas"},
    "earn_tab_ikigai":      {"he": "🌸 מבחן Ikigai",             "en": "🌸 Ikigai Test"},
    "earn_tab_search":      {"he": "🔍 חיפוש הזדמנויות",        "en": "🔍 Search Opportunities"},
    "earn_tab_card":        {"he": "🪪 כרטיס כישרון",           "en": "🪪 Skill Card"},
    "earn_skill_select":    {"he": "מה הכישרון שלך?",           "en": "What's your skill?"},
    "earn_how_to_start":    {"he": "איך מתחילים?",              "en": "How to get started?"},
    "ikigai_q1":            {"he": "במה אתה טוב? (3-5 דברים)",  "en": "What are you good at? (3-5 things)"},
    "ikigai_q2":            {"he": "מה אתה אוהב לעשות?",        "en": "What do you love doing?"},
    "ikigai_q3":            {"he": "מה העולם צריך?",            "en": "What does the world need?"},
    "ikigai_q4":            {"he": "על מה אנשים ישלמו לך?",     "en": "What would people pay you for?"},
    "ikigai_analyze":       {"he": "🌸 נתח את ה-Ikigai שלי",    "en": "🌸 Analyze my Ikigai"},
    "ikigai_what_is":       {"he": "מה זה Ikigai?",             "en": "What is Ikigai?"},
    "earn_search_btn":      {"he": "🔍 חפש הזדמנויות",          "en": "🔍 Search Opportunities"},
    "earn_card_name":       {"he": "השם שלך",                   "en": "Your name"},
    "earn_generate_card":   {"he": "🎨 צור כרטיס",             "en": "🎨 Generate Card"},
    "earn_download_png":    {"he": "📥 הורד PNG",               "en": "📥 Download PNG"},

    # ─── Budget ───────────────────────────────────────────────────────────
    "bud_title":            {"he": "תקציב חודשי",              "en": "Monthly Budget"},
    "bud_tab_enter":        {"he": "✏️ הוסף עסקה",            "en": "✏️ Add Transaction"},
    "bud_tab_overview":     {"he": "📊 סקירה",                 "en": "📊 Overview"},
    "bud_tab_ai":           {"he": "🤖 טיפ AI",               "en": "🤖 AI Tip"},
    "bud_income":           {"he": "💚 הכנסה",                "en": "💚 Income"},
    "bud_expense":          {"he": "🔴 הוצאה",                "en": "🔴 Expense"},
    "bud_amount_label":     {"he": "סכום (₪)",               "en": "Amount (₪)"},
    "bud_balance":          {"he": "יתרה",                    "en": "Balance"},
    "bud_total_income":     {"he": "הכנסות",                  "en": "Income"},
    "bud_total_expenses":   {"he": "הוצאות",                  "en": "Expenses"},
    "bud_saving_goal":      {"he": "יעד חיסכון חודשי (₪)",   "en": "Monthly saving goal (₪)"},
    "bud_saving_label":     {"he": "חיסכון",                  "en": "Savings"},
    "bud_no_data":          {"he": "הוסף עסקה ראשונה",       "en": "Add your first transaction"},
    "bud_expenses_by_cat":  {"he": "הוצאות לפי קטגוריה",    "en": "Expenses by category"},
    "bud_ai_btn":           {"he": "🤖 קבל טיפ חיסכון",      "en": "🤖 Get saving tip"},
    "bud_transactions":     {"he": "עסקאות",                  "en": "Transactions"},

    # ─── Scholarships ─────────────────────────────────────────────────────
    "sch_title":            {"he": "מלגות וקורסים חינמיים",   "en": "Scholarships & Free Courses"},
    "sch_tab_search":       {"he": "🔍 חיפוש",               "en": "🔍 Search"},
    "sch_tab_saved":        {"he": "⭐ שמורים",               "en": "⭐ Saved"},
    "sch_field":            {"he": "תחום עניין",              "en": "Field of interest"},
    "sch_age":              {"he": "גיל",                     "en": "Age"},
    "sch_type_all":         {"he": "הכל",                    "en": "All"},
    "sch_type_scholarship": {"he": "מלגה",                   "en": "Scholarship"},
    "sch_type_course":      {"he": "קורס חינמי",            "en": "Free course"},
    "sch_search_btn":       {"he": "🔍 חפש",                 "en": "🔍 Search"},
    "sch_rank_ai":          {"he": "🤖 דרג עם AI",           "en": "🤖 Rank with AI"},
    "sch_save_btn":         {"he": "⭐ שמור",                 "en": "⭐ Save"},
    "sch_results_count":    {"he": "תוצאות",                 "en": "results"},
    "sch_saved_count":      {"he": "שמורים",                 "en": "saved"},
    "sch_no_saved":         {"he": "אין פריטים שמורים עדיין","en": "No saved items yet"},
    "sch_ai_ranking":       {"he": "דירוג מומלץ",            "en": "Recommended ranking"},

    # ─── Projects ─────────────────────────────────────────────────────────
    "proj_title":           {"he": "מחולל פרויקטים",          "en": "Project Generator"},
    "proj_tab_generate":    {"he": "✨ צור רעיון",            "en": "✨ Generate idea"},
    "proj_tab_saved":       {"he": "📁 שמורים",              "en": "📁 Saved"},
    "proj_interests":       {"he": "תחומי עניין",            "en": "Interests"},
    "proj_subjects":        {"he": "מקצועות חזקים",         "en": "Strong subjects"},
    "proj_duration":        {"he": "משך הפרויקט",           "en": "Project duration"},
    "proj_level":           {"he": "רמת קושי",              "en": "Difficulty level"},
    "proj_extra_info":      {"he": "מידע נוסף (אופציונלי)", "en": "Additional info (optional)"},
    "proj_ddg_toggle":      {"he": "🔍 הוסף דוגמאות מהאינטרנט", "en": "🔍 Add real-world examples"},
    "proj_generate_btn":    {"he": "✨ צור 3 רעיונות לפרויקט",  "en": "✨ Generate 3 Project Ideas"},
    "proj_save_btn":        {"he": "💾 שמור",                "en": "💾 Save"},
    "proj_export_pdf":      {"he": "📥 PDF",                 "en": "📥 PDF"},
    "proj_saved_count":     {"he": "פרויקטים שמורים",       "en": "saved projects"},
    "proj_no_saved":        {"he": "אין פרויקטים שמורים עדיין", "en": "No saved projects yet"},
    "proj_select_interest": {"he": "בחר לפחות תחום עניין אחד",  "en": "Select at least one interest"},

    # ─── Wellness ─────────────────────────────────────────────────────────
    "wellness_title":       {"he": "רווחה נפשית",             "en": "Mental Wellness"},
    "wellness_tab_mood":    {"he": "😊 מצב רוח",             "en": "😊 Mood"},
    "wellness_tab_stress":  {"he": "😓 סטרס",                "en": "😓 Stress"},
    "wellness_tab_breath":  {"he": "🌬️ נשימות",              "en": "🌬️ Breathing"},
    "wellness_tab_tips":    {"he": "💡 טיפים",               "en": "💡 Tips"},
    "wellness_mood_q":      {"he": "איך אתה מרגיש היום?",   "en": "How are you feeling today?"},
    "wellness_save_mood":   {"he": "💾 שמור מצב רוח",        "en": "💾 Save mood"},
    "wellness_mood_saved":  {"he": "נשמר! 💾",               "en": "Saved! 💾"},
    "wellness_stress_q":    {"he": "כמה אתה לחוץ?",         "en": "How stressed are you?"},
    "wellness_ai_help":     {"he": "🤖 קבל עצות מותאמות",   "en": "🤖 Get personalized advice"},
    "wellness_breath_title":{"he": "תרגיל נשימה 4-7-8",     "en": "4-7-8 Breathing Exercise"},
    "wellness_inhale":      {"he": "שאף…",                   "en": "Inhale…"},
    "wellness_hold":        {"he": "עצור…",                  "en": "Hold…"},
    "wellness_exhale":      {"he": "נשוף…",                  "en": "Exhale…"},
    "wellness_start_ex":    {"he": "▶ התחל תרגיל",          "en": "▶ Start Exercise"},
    "wellness_done_ex":     {"he": "כל הכבוד! 🎉",          "en": "Well done! 🎉"},
    "wellness_mood_history":{"he": "היסטוריית מצב רוח",     "en": "Mood history"},
    "wellness_tips_title":  {"he": "💡 טיפים לשמירה על שפיות", "en": "💡 Tips to stay sane"},
    "wellness_custom_tip":  {"he": "ספר על המצב שלך עכשיו:", "en": "Describe your situation now:"},
    "wellness_get_tip":     {"he": "🤖 קבל טיפ",            "en": "🤖 Get Tip"},

    # ─── Q&A Board ────────────────────────────────────────────────────────
    "qa_title":             {"he": "לוח שאלות ותשובות",       "en": "Q&A Board"},
    "qa_tab_feed":          {"he": "📰 פיד שאלות",           "en": "📰 Questions Feed"},
    "qa_tab_ask":           {"he": "❓ שאל שאלה",            "en": "❓ Ask Question"},
    "qa_tab_my":            {"he": "👤 השאלות שלי",          "en": "👤 My Questions"},
    "qa_question_label":    {"he": "השאלה שלך:",             "en": "Your question:"},
    "qa_post_btn":          {"he": "📤 פרסם שאלה",          "en": "📤 Post Question"},
    "qa_answer_placeholder":{"he": "כתוב תשובה…",           "en": "Write an answer…"},
    "qa_submit_answer":     {"he": "📨 שלח תשובה",          "en": "📨 Submit Answer"},
    "qa_get_ai_answer":     {"he": "🤖 תשובת AI",           "en": "🤖 AI Answer"},
    "qa_upvote":            {"he": "👍 עזר לי",             "en": "👍 Helpful"},
    "qa_answers_count":     {"he": "תשובות",                 "en": "answers"},
    "qa_asked_by":          {"he": "שאל:",                   "en": "Asked by:"},
    "qa_no_questions":      {"he": "אין שאלות עדיין — היה הראשון!", "en": "No questions yet — be the first!"},
    "qa_search_first":      {"he": "🔍 חפש קודם ב-DuckDuckGo", "en": "🔍 Search DuckDuckGo first"},
    "qa_posted":            {"he": "שאלה פורסמה! ✅",       "en": "Question posted! ✅"},
    "qa_my_questions":      {"he": "לא שאלת שאלות עדיין",  "en": "You haven't asked any questions yet"},
    "qa_sort_new":          {"he": "חדש",                   "en": "New"},
    "qa_sort_popular":      {"he": "פופולרי",               "en": "Popular"},
}


# ═══════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def T(key: str, lang: str | None = None, **kwargs) -> str:
    """
    מחזיר טקסט מתורגם לפי המפתח.

    Args:
        key:    מפתח מ-TRANSLATIONS
        lang:   "he" | "en" — אם None נלקח מ-st.session_state.lang
        kwargs: משתנים לפורמט (e.g. T("greeting", name="דני"))

    Returns:
        מחרוזת מתורגמת. אם המפתח לא נמצא — מחזיר את המפתח עצמו.
    """
    if lang is None:
        lang = st.session_state.get("lang", "he")

    row = TRANSLATIONS.get(key)
    if row is None:
        return key  # fallback גלוי — קל לאתר מפתחות חסרים

    text = row.get(lang, row.get("he", key))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass

    return text


def get_all_keys() -> list[str]:
    """מחזיר רשימת כל המפתחות — שימושי לבדיקות."""
    return list(TRANSLATIONS.keys())


def missing_translations(lang: str = "en") -> list[str]:
    """מחזיר מפתחות שחסר להם תרגום בשפה נתונה."""
    return [k for k, v in TRANSLATIONS.items() if lang not in v]