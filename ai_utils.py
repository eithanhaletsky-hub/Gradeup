import os
import io
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()


# ── API Key ───────────────────────────────────────────────────────────────
def get_api_key() -> str | None:
    """
    מחזיר את ה-Gemini API Key.
    מעדיף מפתח שהוזן על ידי המשתמש (נשמר ב-session_state),
    אחרת משתמש במפתח מקובץ ה-.env.
    מחזיר None אם אף מפתח לא נמצא.
    """
    # 1. בדוק אם המשתמש הזין API Key ושמור אותו ב-session_state
    user_key = st.session_state.get("gemini_key")
    if user_key:
        return user_key

    # 2. אם אין מפתח מהמשתמש, בדוק אם קיים בקובץ ה-env
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        # חשוב: אל תשמור את המפתח מה-env ב-session_state כדי למנוע חשיפה
        return env_key

    # 3. אם אין מפתח בשני המקרים, החזר None
    return None


def api_key_widget(label_he="⚙️ הגדרות", label_en="⚙️ Settings"):
    """
    ווידג'ט בסרגל הצד לשמירת Gemini API Key.
    תומך בשמירת מפתח מהמשתמש ב-session_state
    או שימוש במפתח מה-env.
    """
    lang = st.session_state.get("lang", "he")
    lbl  = label_he if lang == "he" else label_en

    # קביעת מצב ה-expanded של ה-expander
    # אם יש מפתח מה-env או מה-session_state, נרצה שה-expander יהיה סגור כברירת מחדל
    is_key_available = bool(get_api_key())

    with st.sidebar.expander(lbl, expanded=not is_key_available):
        # הודעה אם המפתח נטען מה-env
        if os.getenv("GEMINI_API_KEY"):
            st.success("✅ " + ("מפתח נטען מקובץ ה-.env" if lang=="he" else "Key loaded from .env file"))

        # שדה קלט ל-API Key של המשתמש
        user_key_input = st.text_input(
            "הזן את ה-Gemini API Key שלך (מועדף)", # "Enter your Gemini API Key (preferred)"
            type="password",
            value=st.session_state.get("gemini_key", ""),
            help="ניתן למצוא אותו ב-aistudio.google.com", # "You can find it at aistudio.google.com"
            key="user_gemini_key_input" # שינוי ה-key למניעת התנגשות
        )

        # כפתור שמירה למפתח המשתמש
        if st.button("💾 " + ("שמור מפתח משתמש" if lang=="he" else "Save User Key"), key="save_user_api_key"):
            st.session_state["gemini_key"] = user_key_input # שמירה אך ורק ב-session_state
            st.success("✅ מפתח המשתמש נשמר.") # "✅ User key saved."
            st.rerun()

        # אם יש מפתח מה-env ואין מפתח משתמש שמור, נציג הודעה
        if os.getenv("GEMINI_API_KEY") and not st.session_state.get("gemini_key"):
            st.info("ℹ️ נעשה שימוש במפתח מה-`.env`.") # "ℹ️ Using key from .env"


# ── DuckDuckGo ────────────────────────────────────────────────────────────
def ddg_search(query: str, max_results: int = 5) -> list[dict]:
    """
    מבצע חיפוש באינטרנט באמצעות DuckDuckGo.
    """
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            st.error("Please install the 'ddgs' library: pip install ddgs")
            return [{"title": "Error", "body": "ddgs library not found.", "href": ""}]

        with DDGS() as d:
            results = list(d.text(query, max_results=max_results))
            if not results:
                 return [{"title": "No results found", "body": f"Could not find results for query: '{query}'", "href": ""}]
            return results
    except Exception as e:
        return [{"title": "Search error", "body": f"An error occurred during search: {e}", "href": ""}]


# ── Pillow ────────────────────────────────────────────────────────────────
def process_image(uploaded) -> Image.Image | None:
    """
    מעבד תמונה שהועלתה: פותח, ממיר ל-RGB ומשנה גודל אם צריך.
    """
    if not uploaded:
        return None
    try:
        img = Image.open(uploaded)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        max_dim = 1024
        if max(img.size) > max_dim:
            r = max_dim / max(img.size)
            new_size = (int(img.width * r), int(img.height * r))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None


def pil_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    """
    ממיר אובייקט Pillow Image למערך בתים.
    """
    buf = io.BytesIO()
    try:
        img.save(buf, format=fmt)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Error converting image to bytes: {e}")
        return b""


# ── Gemini ────────────────────────────────────────────────────────────────
def call_gemini(
    *,
    system_prompt: str,
    user_text: str,
    history: list[dict] | None = None,
    image: Image.Image | None = None,
    search_results: list[dict] | None = None,
    max_tokens: int = 1200,
    temperature: float = 0.7,
) -> str:
    """
    קורא ל-Gemini API עם הלוגיקה החדשה של API Key.
    זורק ValueError אם אין API Key זמין.
    """
    key = get_api_key()
    if not key:
        # הצגת שגיאה למשתמש אם אין מפתח API
        raise ValueError("Gemini API Key is missing. Please set it in the settings or in your .env file.")

    try:
        client = genai.Client(api_key=key)

        history_contents = []
        for msg in (history or []):
            if msg["role"] not in ("user", "assistant"):
                continue
            role = "user" if msg["role"] == "user" else "model"
            # ודא שכל חלק בתוכן הוא טקסט (או נתון אחר ש-parts מקבל)
            parts = [types.Part.from_text(text=item) if isinstance(item, str) else item for item in msg.get("content", [])]
            history_contents.append(types.Content(role=role, parts=parts))

        current_parts = []
        if image:
            image_bytes = pil_to_bytes(image)
            if image_bytes: # ודא שהמרת התמונה הצליחה
                 current_parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            else:
                 st.warning("Could not process image for Gemini call.")

        if search_results:
            # סינון תוצאות חיפוש ריקות או שגויות
            valid_results = [r for r in search_results if r.get("body")]
            if valid_results:
                ctx = "\n\n".join(f"[{r.get('title','')}]\n{r.get('body','')}" for r in valid_results)
                current_parts.append(types.Part.from_text(text=f"Search results:\n{ctx}\n---\n"))
            else:
                # אם אין תוצאות חיפוש תקפות, אל תוסיף קטע זה
                pass

        current_parts.append(types.Part.from_text(text=user_text))

        all_contents = history_contents + [types.Content(role="user", parts=current_parts)]

        # הגדרת model config
        generation_config = types.GenerationConfig(
            system_instruction=system_prompt,
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

        resp = client.models.generate_content(
            model="gemini-2.0-flash", # או דגם אחר לפי הצורך
            generation_config=generation_config,
            contents=all_contents,
        )

        # בדיקה אם התשובה חסומה או ריקה
        if not resp.candidates or not resp.candidates[0].content.parts:
            # נסה להחזיר את סיבת החסימה אם קיימת
            finish_reason = resp.candidates[0].finish_reason if resp.candidates else "unknown"
            safety_ratings = resp.candidates[0].safety_ratings if resp.candidates else []
            return f"Error: Content generation failed. Reason: {finish_reason}. Safety ratings: {safety_ratings}"

        return resp.text

    except ValueError as ve: # לוכד את השגיאה של get_api_key()
        raise ve # מעביר את השגיאה הלאה
    except Exception as e:
        # לכידת שגיאות כלליות של ה-API
        st.error(f"An error occurred while calling Gemini API: {e}")
        return f"Error: Could not generate content. Please check your API key and try again. Details: {e}"
