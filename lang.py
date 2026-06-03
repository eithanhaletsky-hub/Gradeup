"""
lang.py – מערכת תרגום דו-לשונית (עברית / English)
שימוש:  from lang import t, init_lang
"""
import streamlit as st

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ─── כללי ───────────────────────────────────────────────────
    "app_name":         {"he": "Gradeup", "en": "Gradeup"},
    "tagline":         {"he": "לומדים חכם, חיים טוב", "en": "Study smart, level up"},
    "lang_toggle":      {"he": "English", "en": "עברית"},
    "save":             {"he": "שמור", "en": "Save"},
    "cancel":           {"he": "בטל", "en": "Cancel"},
    "add":              {"he": "הוסף", "en": "Add"},
    "delete":           {"he": "מחק", "en": "Delete"},
    "search":           {"he": "חפש", "en": "Search"},
    "loading":          {"he": "טוען…", "en": "Loading…"},
    "error":            {"he": "שגיאה", "en": "Error"},
    "success":          {"he": "בוצע!", "en": "Done!"},
    "tip":              {"he": "טיפ:", "en": "Tip:"},
    "back":             {"he": "חזרה", "en": "Back"},
    "next":             {"he": "הבא", "en": "Next"},
    "send":             {"he": "שלח", "en": "Send"},
    "clear":            {"he": "נקה", "en": "Clear"},
    "download":         {"he": "הורד", "en": "Download"},
    "you":              {"he": "אתה", "en": "You"},
    "ai_label":         {"he": "🤖 Gradeup AI", "en": "🤖 Gradeup AI"},
    "sunday":           {"he": "ראשון", "en": "Sun"},
    "monday":           {"he": "שני",   "en": "Mon"},
    "tuesday":          {"he": "שלישי", "en": "Tue"},
    "wednesday":        {"he": "רביעי", "en": "Wed"},
    "thursday":         {"he": "חמישי", "en": "Thu"},
    "friday":           {"he": "שישי",  "en": "Fri"},
    "saturday":         {"he": "שבת",   "en": "Sat"},
    # ─── ניווט ───────────────────────────────────────────────────
    "nav_home":         {"he": "🏠 ראשי",             "en": "🏠 Home"},
    "nav_schedule":     {"he": "🗓️ מערכת שעות",       "en": "🗓️ Schedule"},
    "nav_homework":     {"he": "📚 עזרה בשיעורים",    "en": "📚 Homework Bot"},
    "nav_earn":         {"he": "💼 הכנסה & Ikigai",   "en": "💼 Earn & Ikigai"},
    "nav_grades":       {"he": "📊 מעקב ציונים",      "en": "📊 Grade Tracker"},
    "nav_wellness":     {"he": "💆 רווחה נפשית",      "en": "💆 Wellness"},
    # ─── Home ────────────────────────────────────────────────────
    "home_hero_sub":    {"he": "הכלי שתמיד רצית — מערכת שעות, עזרה בלימודים, ומסלול להכנסה", "en": "The tool you always wanted — schedule, homework help & income path"},
    "home_get_started": {"he": "בואו נתחיל", "en": "Get Started"},
    "home_pricing_title":{"he": "💳 תמחור", "en": "💳 Pricing"},
    "home_free":        {"he": "חינמי", "en": "Free"},
    "home_pro":         {"he": "Pro", "en": "Pro"},
    "home_free_desc":   {"he": "מערכת שעות בסיסית\nעזרה AI (10 שאלות/יום)\nIkigai", "en": "Basic schedule\nAI help (10 q/day)\nIkigai"},
    "home_pro_price":   {"he": "3–5 ₪ / חודש", "en": "~$1 / month"},
    "home_pro_desc":    {"he": "כל מה שבחינמי\nAI ללא הגבלה\nחיפוש DuckDuckGo\nייצוא PDF", "en": "Everything in Free\nUnlimited AI\nDuckDuckGo search\nPDF export"},
    "home_features":    {"he": "✨ מה כלול?", "en": "✨ What's included?"},
    # ─── Schedule ─────────────────────────────────────────────────
    "sched_title":      {"he": "🗓️ מערכת שעות חכמה", "en": "🗓️ Smart Schedule"},
    "sched_tab_view":   {"he": "📊 לוח שבועי", "en": "📊 Weekly View"},
    "sched_tab_add":    {"he": "➕ הוסף פריט", "en": "➕ Add Item"},
    "sched_tab_tasks":  {"he": "📋 משימות יומיות", "en": "📋 Daily Tasks"},
    "sched_tab_ai":     {"he": "🤖 AI מסכם", "en": "🤖 AI Summary"},
    "sched_day":        {"he": "יום", "en": "Day"},
    "sched_start":      {"he": "שעת התחלה", "en": "Start"},
    "sched_end":        {"he": "שעת סיום", "en": "End"},
    "sched_subject":    {"he": "מקצוע", "en": "Subject"},
    "sched_teacher":    {"he": "מורה", "en": "Teacher"},
    "sched_room":       {"he": "חדר", "en": "Room"},
    "sched_type":       {"he": "סוג", "en": "Type"},
    "sched_class":      {"he": "שיעור", "en": "Class"},
    "sched_activity":   {"he": "חוג/פעילות", "en": "Activity"},
    "sched_exam":       {"he": "מבחן", "en": "Exam"},
    "sched_other":      {"he": "אחר", "en": "Other"},
    "sched_no_items":   {"he": "אין פריטים עדיין — הוסף פריטים בטאב 'הוסף פריט'", "en": "No items yet — use the 'Add Item' tab"},
    "sched_ai_prompt":  {"he": "נתח את מערכת השעות שלי ותן המלצות לניהול זמן", "en": "Analyze my schedule and give time management tips"},
    "task_name":        {"he": "שם המשימה", "en": "Task name"},
    "task_due":         {"he": "מועד הגשה", "en": "Due date"},
    "task_priority":    {"he": "עדיפות", "en": "Priority"},
    "task_high":        {"he": "🔴 גבוהה", "en": "🔴 High"},
    "task_med":         {"he": "🟡 בינונית", "en": "🟡 Medium"},
    "task_low":         {"he": "🟢 נמוכה", "en": "🟢 Low"},
    "task_done":        {"he": "הושלם", "en": "Done"},
    "task_pending":     {"he": "ממתין", "en": "Pending"},
    # ─── Homework ─────────────────────────────────────────────────
    "hw_title":         {"he": "📚 עוזר שיעורי בית", "en": "📚 Homework Bot"},
    "hw_subject":       {"he": "בחר מקצוע", "en": "Choose subject"},
    "hw_mode":          {"he": "סוג עזרה", "en": "Help mode"},
    "hw_mode_explain":  {"he": "הסבר נושא", "en": "Explain topic"},
    "hw_mode_solve":    {"he": "עזור לפתור", "en": "Help solve"},
    "hw_mode_summary":  {"he": "סכם חומר", "en": "Summarize material"},
    "hw_mode_exam":     {"he": "שאלות מבחן", "en": "Exam questions"},
    "hw_placeholder":   {"he": "שאל שאלה, הדבק תרגיל, או העלה תמונה…", "en": "Ask a question, paste an exercise, or upload an image…"},
    "hw_search_toggle": {"he": "🔍 חיפוש DuckDuckGo", "en": "🔍 DuckDuckGo search"},
    "hw_image_upload":  {"he": "📸 העלה תמונה של השאלה", "en": "📸 Upload image of question"},
    "hw_thinking":      {"he": "חושב…", "en": "Thinking…"},
    "hw_clear":         {"he": "🗑️ נקה שיחה", "en": "🗑️ Clear Chat"},
    "hw_api_missing":   {"he": "יש להזין Gemini API Key בהגדרות", "en": "Please enter a Gemini API Key in Settings"},
    "hw_welcome":       {"he": "שלום! שאל אותי כל שאלה בלימודים 📖", "en": "Hi! Ask me anything about your studies 📖"},
    # ─── Earn / Ikigai ───────────────────────────────────────────
    "earn_title":       {"he": "💼 הכנסה & Ikigai", "en": "💼 Earn & Ikigai"},
    "earn_tab_ideas":   {"he": "💡 רעיונות הכנסה", "en": "💡 Income Ideas"},
    "earn_tab_ikigai":  {"he": "🌸 מבחן Ikigai", "en": "🌸 Ikigai Test"},
    "earn_tab_search":  {"he": "🔍 חיפוש הזדמנויות", "en": "🔍 Search Opportunities"},
    "earn_tab_card":    {"he": "🪪 כרטיס הכישרון שלי", "en": "🪪 My Skill Card"},
    "ikigai_q1":        {"he": "במה אתה טוב? (רשום 3-5 דברים)", "en": "What are you good at? (list 3-5 things)"},
    "ikigai_q2":        {"he": "מה אתה אוהב לעשות?", "en": "What do you love doing?"},
    "ikigai_q3":        {"he": "במה העולם צריך עזרה? (לדעתך)", "en": "What does the world need help with?"},
    "ikigai_q4":        {"he": "על מה אנשים מוכנים לשלם לך?", "en": "What would people pay you for?"},
    "ikigai_analyze":   {"he": "🌸 נתח את ה-Ikigai שלי", "en": "🌸 Analyze my Ikigai"},
    "ikigai_thinking":  {"he": "מנתח…", "en": "Analyzing…"},

    # ─── Grades ───────────────────────────────────────────────────
    "grades_title":         {"he": "📊 מעקב ציונים", "en": "📊 Grade Tracker"},
    "grades_tab_enter":     {"he": "✏️ הכנס ציון", "en": "✏️ Enter Grade"},
    "grades_tab_overview":  {"he": "📈 סקירה", "en": "📈 Overview"},
    "grades_tab_ai":        {"he": "🤖 ניתוח AI", "en": "🤖 AI Analysis"},
    "grades_subject":       {"he": "מקצוע", "en": "Subject"},
    "grades_score":         {"he": "ציון", "en": "Score"},
    "grades_max":           {"he": "מתוך", "en": "Out of"},
    "grades_type":          {"he": "סוג הערכה", "en": "Assessment type"},
    "grades_test":          {"he": "מבחן", "en": "Test"},
    "grades_quiz":          {"he": "בוחן", "en": "Quiz"},
    "grades_hw":            {"he": "שיעורי בית", "en": "Homework"},
    "grades_project":       {"he": "פרויקט", "en": "Project"},
    "grades_oral":          {"he": "בעל-פה", "en": "Oral"},
    "grades_date":          {"he": "תאריך", "en": "Date"},
    "grades_note":          {"he": "הערה", "en": "Note"},
    "grades_avg":           {"he": "ממוצע", "en": "Average"},
    "grades_trend_up":      {"he": "מגמה עולה ✅", "en": "Trending up ✅"},
    "grades_trend_down":    {"he": "מגמה יורדת ⚠️", "en": "Trending down ⚠️"},
    "grades_trend_stable":  {"he": "יציב 📊", "en": "Stable 📊"},
    "grades_ai_prompt":     {"he": "נתח את הציונים שלי ותן המלצות", "en": "Analyze my grades and give recommendations"},
    "grades_no_data":       {"he": "אין ציונים עדיין — הכנס ציון ראשון!", "en": "No grades yet — add your first grade!"},
    # ─── Wellness ─────────────────────────────────────────────────
    "wellness_title":       {"he": "💆 רווחה נפשית", "en": "💆 Mental Wellness"},
    "wellness_tab_mood":    {"he": "😊 מצב רוח", "en": "😊 Mood"},
    "wellness_tab_stress":  {"he": "😓 סטרס ומבחנים", "en": "😓 Exam Stress"},
    "wellness_tab_breath":  {"he": "🌬️ נשימות", "en": "🌬️ Breathing"},
    "wellness_tab_tips":    {"he": "💡 טיפים", "en": "💡 Tips"},
    "wellness_mood_q":      {"he": "איך אתה מרגיש היום?", "en": "How are you feeling today?"},
    "wellness_mood_save":   {"he": "שמור מצב רוח", "en": "Save mood"},
    "wellness_mood_saved":  {"he": "נשמר! 💾", "en": "Saved! 💾"},
    "wellness_stress_q":    {"he": "כמה אתה לחוץ מהמבחנים?", "en": "How stressed are you about exams?"},
    "wellness_ai_help":     {"he": "🤖 קבל עצות מותאמות אישית", "en": "🤖 Get personalized advice"},
    "wellness_breath_title":{"he": "תרגיל נשימה 4-7-8", "en": "4-7-8 Breathing Exercise"},
    "wellness_inhale":      {"he": "שאף…", "en": "Inhale…"},
    "wellness_hold":        {"he": "עצור…", "en": "Hold…"},
    "wellness_exhale":      {"he": "נשוף…", "en": "Exhale…"},
    "wellness_start":       {"he": "התחל תרגיל", "en": "Start Exercise"},
    # ─── Settings (sidebar) ──────────────────────────────────────
    "settings_title":   {"he": "⚙️ הגדרות", "en": "⚙️ Settings"},
    "api_key_label":    {"he": "Gemini API Key", "en": "Gemini API Key"},
    "api_key_help":     {"he": "קבל מפתח חינמי: aistudio.google.com", "en": "Get free key: aistudio.google.com"},
    "api_saved":        {"he": "✅ מפתח נשמר", "en": "✅ Key saved"},
    "api_from_env":     {"he": "✅ מפתח נטען מ-.env", "en": "✅ Key loaded from .env"},
}


def init_lang():
    if "lang" not in st.session_state:
        st.session_state.lang = "he"


def t(key: str, **kwargs) -> str:
    """מחזיר מחרוזת בשפה הנוכחית. תומך ב-f-string עם kwargs."""
    lang = st.session_state.get("lang", "he")
    row = TRANSLATIONS.get(key)
    if row is None:
        return key  # fallback — מחזיר את המפתח עצמו
    text = row.get(lang, row.get("he", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text