import streamlit as st

TRANSLATIONS = {
    "he": {

        # ── Common ─────────────────────────────────────────────
        "add": "הוסף",
        "success": "נוסף בהצלחה",
        "clear": "נקה",
        "error": "שגיאה",
        "you": "אתה",
        "ai_label": "AI",

        # ── Homework ───────────────────────────────────────────
        "hw_title": "עוזר שיעורי בית",
        "hw_api_missing": "חסר Gemini API Key",
        "hw_subject": "מקצוע",
        "hw_mode": "מצב עזרה",
        "hw_search_toggle": "חיפוש באינטרנט",
        "hw_image_upload": "העלה תמונה",
        "hw_welcome": "ברוך הבא לעוזר שיעורי הבית",
        "hw_placeholder": "כתוב את השאלה שלך כאן...",
        "hw_thinking": "חושב...",
        "hw_clear": "נקה שיחה",

        # ── Flashcards ─────────────────────────────────────────
        "fc_title": "כרטיסיות לימוד",

        "fc_tab_study": "📖 לימוד",
        "fc_tab_create": "➕ יצירה",
        "fc_tab_ai": "🤖 AI",
        "fc_tab_manage": "🗂️ ניהול",

        "fc_subject": "נושא",

        "fc_no_cards": "אין כרטיסיות עדיין",

        "fc_done": "כל הכבוד!",
        "fc_score": "ציון",
        "fc_restart": "התחל מחדש",

        "fc_card_count": "כרטיסיות",

        "fc_question": "שאלה",
        "fc_answer": "תשובה",

        "fc_flip": "הפוך כרטיס",
        "fc_knew": "ידעתי",
        "fc_didnt": "לא ידעתי",

        "fc_ai_prompt": "הדבק חומר לימוד ליצירת כרטיסיות",
        "fc_ai_generate": "צור כרטיסיות",

        # ── Summarizer ─────────────────────────────────────────
        "sum_title": "מסכם חומר חכם",

        "sum_tab_text": "📝 סיכום",
        "sum_tab_history": "📚 היסטוריה",

        "sum_subject": "מקצוע",
        "sum_style": "סגנון סיכום",

        "sum_paste_label": "הדבק טקסט לסיכום",

        "sum_chars": "תווים",

        "sum_go": "צור סיכום",

        "sum_export_pdf": "ייצא ל-PDF",

        "sum_no_history": "אין סיכומים שמורים",

        # ── Schedule ───────────────────────────────────────────
        "sched_title": "מערכת שעות",

        "sched_tab_view": "📅 תצוגה",
        "sched_tab_tasks": "✅ משימות",
        "sched_tab_ai": "🤖 ניתוח AI",

        "sched_filter": "סינון לפי סוג",

        "sched_day": "יום",
        "sched_start": "שעת התחלה",
        "sched_end": "שעת סיום",

        "sched_subject": "מקצוע",
        "sched_type": "סוג",
        "sched_teacher": "מורה",
        "sched_location": "מיקום",

        "task_name": "שם המשימה",
        "task_priority": "עדיפות",
        "task_due": "תאריך יעד",

        "sched_ai_prompt": "נתח את מערכת השעות",
    },

    "en": {

        # ── Common ─────────────────────────────────────────────
        "add": "Add",
        "success": "Added successfully",
        "clear": "Clear",
        "error": "Error",
        "you": "You",
        "ai_label": "AI",

        # ── Homework ───────────────────────────────────────────
        "hw_title": "Homework Bot",
        "hw_api_missing": "Gemini API Key is missing",
        "hw_subject": "Subject",
        "hw_mode": "Help Mode",
        "hw_search_toggle": "Web Search",
        "hw_image_upload": "Upload Image",
        "hw_welcome": "Welcome to Homework Bot",
        "hw_placeholder": "Type your question here...",
        "hw_thinking": "Thinking...",
        "hw_clear": "Clear Chat",

        # ── Flashcards ─────────────────────────────────────────
        "fc_title": "Flashcards",

        "fc_tab_study": "📖 Study",
        "fc_tab_create": "➕ Create",
        "fc_tab_ai": "🤖 AI",
        "fc_tab_manage": "🗂️ Manage",

        "fc_subject": "Subject",

        "fc_no_cards": "No flashcards yet",

        "fc_done": "Great Job!",
        "fc_score": "Score",
        "fc_restart": "Restart",

        "fc_card_count": "cards",

        "fc_question": "Question",
        "fc_answer": "Answer",

        "fc_flip": "Flip Card",
        "fc_knew": "I Knew It",
        "fc_didnt": "Didn't Know",

        "fc_ai_prompt": "Paste study material to generate flashcards",
        "fc_ai_generate": "Generate Flashcards",

        # ── Summarizer ─────────────────────────────────────────
        "sum_title": "Smart Summarizer",

        "sum_tab_text": "📝 Summarize",
        "sum_tab_history": "📚 History",

        "sum_subject": "Subject",
        "sum_style": "Summary Style",

        "sum_paste_label": "Paste text to summarize",

        "sum_chars": "characters",

        "sum_go": "Generate Summary",

        "sum_export_pdf": "Export PDF",

        "sum_no_history": "No saved summaries",

        # ── Schedule ───────────────────────────────────────────
        "sched_title": "Schedule",

        "sched_tab_view": "📅 View",
        "sched_tab_tasks": "✅ Tasks",
        "sched_tab_ai": "🤖 AI Analysis",

        "sched_filter": "Filter by Type",

        "sched_day": "Day",
        "sched_start": "Start Time",
        "sched_end": "End Time",

        "sched_subject": "Subject",
        "sched_type": "Type",
        "sched_teacher": "Teacher",
        "sched_location": "Location",

        "task_name": "Task Name",
        "task_priority": "Priority",
        "task_due": "Due Date",

        "sched_ai_prompt": "Analyze Schedule",
    }
}


def t(key: str) -> str:
    lang = st.session_state.get("lang", "he")
    return TRANSLATIONS.get(lang, {}).get(key, key)