"""ai_utils.py — Gemini + DuckDuckGo + Pillow utilities"""
import os, io
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()


# ── API Key ───────────────────────────────────────────────────────────────
def get_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or st.session_state.get("gemini_key") or None


def api_key_widget(label_he="⚙️ הגדרות", label_en="⚙️ Settings"):
    lang = st.session_state.get("lang", "he")
    lbl  = label_he if lang == "he" else label_en
    with st.sidebar.expander(lbl, expanded=not bool(get_api_key())):
        if os.getenv("GEMINI_API_KEY"):
            st.success("✅ " + ("מפתח נטען מ-.env" if lang=="he" else "Key loaded from .env"))
        else:
            val = st.text_input(
                "Gemini API Key",
                type="password",
                value=st.session_state.get("gemini_key",""),
                help="aistudio.google.com",
            )
            if st.button("💾 " + ("שמור" if lang=="he" else "Save"), key="save_api_key"):
                st.session_state.gemini_key = val
                st.success("✅")
                st.rerun()


# ── DuckDuckGo ────────────────────────────────────────────────────────────
def ddg_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS() as d:
            return list(d.text(query, max_results=max_results))
    except Exception as e:
        return [{"title": "Search error", "body": str(e), "href": ""}]


# ── Pillow ────────────────────────────────────────────────────────────────
def process_image(uploaded) -> Image.Image | None:
    if not uploaded:
        return None
    img = Image.open(uploaded)
    if img.mode not in ("RGB","RGBA"):
        img = img.convert("RGB")
    if max(img.size) > 1024:
        r = 1024 / max(img.size)
        img = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
    return img


def pil_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


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
    key = get_api_key()
    if not key:
        raise ValueError("Missing Gemini API Key")

    client = genai.Client(api_key=key)

    history_contents = []
    for msg in (history or []):
        if msg["role"] not in ("user","assistant"):
            continue
        role = "user" if msg["role"]=="user" else "model"
        history_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    current_parts = []
    if image:
        current_parts.append(types.Part.from_bytes(data=pil_to_bytes(image), mime_type="image/png"))
    if search_results:
        ctx = "\n\n".join(f"[{r.get('title','')}]\n{r.get('body','')}" for r in search_results if r.get("body"))
        current_parts.append(types.Part.from_text(text=f"Search results:\n{ctx}\n---\n"))
    current_parts.append(types.Part.from_text(text=user_text))

    all_contents = history_contents + [types.Content(role="user", parts=current_parts)]

    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
        contents=all_contents,
    )
    return resp.text