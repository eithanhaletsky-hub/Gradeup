"""
ai_utils.py — עוזר Gemini + DuckDuckGo
"""
import os
import io
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()


# ── API Key ──────────────────────────────────────────────────────────────────
def get_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or st.session_state.get("gemini_key") or None


def api_key_widget(t_fn):
    """רכיב sidebar להזנת API Key — מוצג רק אם אין מפתח ב-.env"""
    env_key = os.getenv("GEMINI_API_KEY")
    with st.sidebar.expander(t_fn("settings_title"), expanded=not bool(get_api_key())):
        if env_key:
            st.success(t_fn("api_from_env"))
        else:
            val = st.text_input(
                t_fn("api_key_label"),
                type="password",
                value=st.session_state.get("gemini_key", ""),
                help=t_fn("api_key_help"),
            )
            if st.button(t_fn("save"), key="save_api_key"):
                st.session_state.gemini_key = val
                st.success(t_fn("api_saved"))
                st.rerun()


# ── DuckDuckGo ───────────────────────────────────────────────────────────────
def ddg_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return [{"title": "חיפוש נכשל", "body": str(e), "href": ""}]


# ── Pillow helpers ────────────────────────────────────────────────────────────
def process_uploaded_image(uploaded_file) -> Image.Image | None:
    """קורא קובץ שהועלה, כווץ אם גדול, ממיר ל-RGB"""
    if uploaded_file is None:
        return None
    img = Image.open(uploaded_file)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    max_px = 1024
    if max(img.size) > max_px:
        ratio = max_px / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    return img


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


# ── Gemini ────────────────────────────────────────────────────────────────────
def call_gemini(
    *,
    system_prompt: str,
    user_text: str,
    history: list[dict] | None = None,
    image: Image.Image | None = None,
    search_results: list[dict] | None = None,
    max_tokens: int = 1500,
    temperature: float = 0.7,
) -> str:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Missing Gemini API Key")

    client = genai.Client(api_key=api_key)

    # היסטוריה
    history_contents: list[types.Content] = []
    for msg in (history or []):
        if msg["role"] not in ("user", "assistant"):
            continue
        role = "user" if msg["role"] == "user" else "model"
        history_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    # הודעה נוכחית
    current_parts: list = []

    if image is not None:
        img_bytes = pil_to_bytes(image)
        current_parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))

    if search_results:
        ctx = "\n\n".join(
            f"[{r.get('title','')}]\n{r.get('body','')}"
            for r in search_results if r.get("body")
        )
        current_parts.append(types.Part.from_text(text=f"תוצאות חיפוש:\n{ctx}\n\n---\n"))

    current_parts.append(types.Part.from_text(text=user_text))

    all_contents = history_contents + [
        types.Content(role="user", parts=current_parts)
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
        contents=all_contents,
    )
    return response.text