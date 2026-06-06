import streamlit as st
from ddgs import DDGS
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ודא שמפתח ה-API מוגדר אצלך
# from ai_utils import get_api_key
# API_KEY = get_api_key()


def render_scholarships_courses(t):
    st.markdown(
        f'<div class="sf-section-title">{t("scholarships_courses_title")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="sf-subtitle">{t("career")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="sf-description">{t("scholarships_courses_description")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="sf-libraries-title">{t("libraries")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sf-library">ddgs</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-library">google-genai</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="sf-connected-pages-title">{t("connected_pages")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sf-connected-page">💼 Earn</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-connected-page">🎯 יעדים</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="sf-features-title">{t("features")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div>- {t("scholarships_ddg_search")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div>- {t("scholarships_filter_by_field_age")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div>- {t("scholarships_ai_ranking")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div>- {t("scholarships_save_favorites")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        f'<div class="sf-sub-section-title">{t("scholarships_search_form")}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        interest = st.text_input(
            t("scholarships_interest_field"),
            key="scholarships_interest",
        )

    with col2:
        age = st.number_input(
            t("scholarships_age"),
            min_value=15,
            max_value=100,
            value=16,
            key="scholarships_age",
        )

    country = st.selectbox(
        t("scholarships_country"),
        ["ישראל", "עולם"],
        key="scholarships_country",
    )

    location_query = "בישראל" if country == "ישראל" else "בעולם"

    if "saved_scholarships" not in st.session_state:
        st.session_state.saved_scholarships = []

    if st.button(
        t("scholarships_search_btn"),
        key="search_scholarships_btn",
    ):

        if not interest.strip():
            st.warning(t("scholarships_enter_interest"))
            return

        search_query = (
            f"מלגות וקורסים חינם בתחום {interest} "
            f"לגיל {age} {location_query}"
        )

        st.info(f'{t("searching_for")} "{search_query}"')

        try:
            with st.spinner(t("searching_web")):
                results = list(
                    DDGS().text(
                        search_query,
                        max_results=10,
                    )
                )

            if not results:
                st.warning(t("no_results_found"))
                return

            prompt_text = (
                f"הבאתי לך רשימת תוצאות חיפוש עבור מלגות וקורסים חינם "
                f"בתחום '{interest}' לגיל {age} {location_query}.\n\n"
            )

            prompt_text += "תוצאות החיפוש:\n"

            for result in results:
                prompt_text += (
                    f"- {result.get('title', '')}: "
                    f"{result.get('body', '')}\n"
                )

            prompt_text += (
                "\nסכם את המלגות והקורסים הרלוונטיים ביותר. "
                "דרג אותם לפי התאמה לגיל ולתחום העניין. "
                "הדגש את החינמיות, תנאי הקבלה, ואפשרויות הלימוד. "
                "ענה בעברית."
            )

            summary = ""

            try:
                if "GEMINI_API_KEY" in globals() and GEMINI_API_KEY:

                    client = genai.Client(
                        api_key=GEMINI_API_KEY
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_text,
                    )

                    summary = response.text

                else:
                    summary = (
                        t("gemini_unavailable_tip")
                        + "\n\n"
                    )

                    for result in results:
                        summary += (
                            f"• {result.get('title', '')}\n"
                            f"{result.get('body', '')}\n\n"
                        )

            except Exception as gemini_error:

                summary = (
                    f"שגיאה ביצירת סיכום AI: {gemini_error}\n\n"
                )

                for result in results:
                    summary += (
                        f"• {result.get('title', '')}\n"
                        f"{result.get('body', '')}\n\n"
                    )

            st.markdown("---")

            st.markdown(
                f'<div class="sf-sub-section-title">{t("scholarships_results")}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="sf-bubble-ai">{summary}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("---")

            st.markdown(
                f'<div class="sf-sub-section-title">{t("scholarships_favorites")}</div>',
                unsafe_allow_html=True,
            )

            selected_result_index = st.selectbox(
                t("scholarships_select_to_save"),
                options=list(range(len(results))),
                format_func=lambda i: results[i].get(
                    "title",
                    f"Result {i + 1}",
                ),
            )

            if st.button(
                t("scholarships_save_favorite_btn"),
                key="save_scholarship_btn",
            ):

                selected = results[selected_result_index]

                exists = any(
                    s.get("title") == selected.get("title")
                    for s in st.session_state.saved_scholarships
                )

                if not exists:
                    st.session_state.saved_scholarships.append(selected)

                    st.success(
                        t("scholarship_saved_successfully")
                    )
                else:
                    st.info(
                        t("scholarship_already_saved")
                    )

        except Exception as e:
            st.error(
                f"{t('error_searching')}: {e}"
            )

    if st.session_state.saved_scholarships:

        st.markdown("---")

        st.markdown(
            f'<div class="sf-label">{t("scholarships_your_favorites")}</div>',
            unsafe_allow_html=True,
        )

        for favorite in st.session_state.saved_scholarships:

            title = favorite.get(
                "title",
                "ללא כותרת",
            )

            link = (
                favorite.get("href")
                or favorite.get("url")
                or ""
            )

            body = favorite.get(
                "body",
                "",
            )

            st.markdown(f"### {title}")

            if body:
                st.write(body)

            if link:
                st.markdown(
                    f"[🔗 פתח קישור]({link})"
                )

            st.markdown("---")