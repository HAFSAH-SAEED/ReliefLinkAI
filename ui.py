"""Streamlit UI rendering for ReliefLink AI.

This file owns the visual presentation layer for the humanitarian landing page
and the Streamlit chat surface that connects to the Backboard service layer.
"""

import streamlit as st

from config import APP_DESCRIPTION, APP_SUBTITLE, APP_TITLE, PROJECT_STATUS, PROJECT_VERSION
from services.backboard_client import (
    AssistantCreationError,
    AssistantStoreError,
    BackboardConfigurationError,
    MessageSendError,
    ThreadCreationError,
    create_or_load_assistant,
    create_thread,
    send_message,
)


def render_homepage(page_config: dict[str, str]) -> None:
    """Render the Field Documentary-themed ReliefLink AI homepage."""
    st.set_page_config(**page_config)
    _render_styles()
    _render_sidebar()
    _render_status_strip()
    _render_hero()
    _render_about_section()
    _render_capabilities_section()
    _render_feature_report()
    _render_workflow_section()
    _render_chat_section()
    _render_roadmap_section()
    _render_footer()


def _render_styles() -> None:
    """Apply the Field Documentary visual system."""
    st.markdown(
        """
        <style>
            :root {
                --sand: #f2ead9;
                --clay: #b3552f;
                --olive: #5c6b47;
                --deep-umber: #3a2a20;
                --sky-dust: #8fa6a3;
                --sunlit: #e8a94c;
                --paper: rgba(242, 234, 217, 0.96);
            }

            @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700;900&family=Inter:wght@400;500;600;700&display=swap');

            .stApp {
                background: linear-gradient(180deg, #f6efe2 0%, #efe4cf 100%);
                color: var(--deep-umber);
                font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .block-container {
                max-width: 1180px;
                padding-top: 1.5rem;
                padding-bottom: 2.5rem;
            }

            [data-testid="stSidebar"] {
                background: #3a2a20;
                color: #f7ede0;
            }

            [data-testid="stSidebar"] * {
                color: #f7ede0;
            }

            .sidebar-title {
                display: inline-flex;
                align-items: center;
                gap: 0.65rem;
                font-size: 1.1rem;
                font-weight: 800;
                letter-spacing: 0.03em;
                margin-bottom: 0.15rem;
            }

            .sidebar-logo {
                width: 28px;
                height: 28px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }

            .sidebar-logo svg {
                width: 100%;
                height: 100%;
            }

            .sidebar-subtitle {
                color: #d8c5b1;
                margin-bottom: 1.05rem;
            }

            .sidebar-chip {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.65rem 0.85rem;
                border-radius: 999px;
                background: rgba(243, 219, 188, 0.16);
                border: 1px solid rgba(255, 255, 255, 0.12);
                color: #f7ede0;
                font-size: 0.85rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }

            .sidebar-divider {
                border-top: 1px solid rgba(255, 255, 255, 0.12);
                margin: 1rem 0 1rem 0;
            }

            .sidebar-nav-item {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                padding: 0.75rem 0.85rem;
                border-radius: 12px;
                margin-bottom: 0.5rem;
                color: #f7ede0;
                font-size: 0.95rem;
                font-weight: 600;
                background: rgba(255, 255, 255, 0.04);
            }

            .sidebar-nav-item:hover {
                background: rgba(255, 255, 255, 0.08);
                cursor: pointer;
            }

            .sidebar-meta {
                margin-top: 1.5rem;
                padding-top: 0.9rem;
                border-top: 1px solid rgba(255, 255, 255, 0.12);
                color: #d8c5b1;
                font-size: 0.88rem;
                line-height: 1.6;
            }

            .sidebar-meta span {
                display: block;
            }

            .status-strip {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 0.9rem;
                padding: 1rem 1.2rem;
                border-radius: 18px;
                background: rgba(58, 42, 32, 0.08);
                border: 1px solid rgba(58, 42, 32, 0.12);
                color: var(--deep-umber);
                font-size: 0.95rem;
                margin-bottom: 1.5rem;
            }

            .status-strip strong {
                font-weight: 700;
            }

            .status-separator {
                color: var(--sky-dust);
            }

            .hero {
                display: grid;
                grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
                gap: 2rem;
                padding: 2rem;
                border-radius: 28px;
                background: var(--paper);
                border: 1px solid rgba(58, 42, 32, 0.12);
                box-shadow: 0 24px 70px rgba(58, 42, 32, 0.08);
                margin-bottom: 2rem;
            }

            .hero-copy {
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 1rem;
            }

            .hero-kicker {
                font-size: 0.9rem;
                font-weight: 700;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: var(--clay);
                margin-bottom: 0.25rem;
            }

            .hero-title {
                font-family: 'Fraunces', Georgia, Cambria, 'Times New Roman', serif;
                font-size: clamp(2.8rem, 5vw, 4.6rem);
                line-height: 0.98;
                margin: 0;
                color: var(--deep-umber);
            }

            .hero-subtitle {
                font-size: 1.1rem;
                color: var(--deep-umber);
                max-width: 620px;
                margin: 0;
                line-height: 1.6;
            }

            .hero-copy p {
                color: #4a382f;
                font-size: 1rem;
                line-height: 1.8;
                max-width: 660px;
                margin: 0;
            }

            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 0.8rem;
                margin-top: 1rem;
            }

            .hero-tag {
                padding: 0.7rem 1rem;
                border-radius: 999px;
                background: rgba(179, 85, 47, 0.12);
                color: var(--clay);
                font-weight: 700;
                font-size: 0.85rem;
                letter-spacing: 0.08em;
            }

            .hero-image {
                position: relative;
                min-height: 420px;
                border-radius: 24px;
                background: linear-gradient(0deg, rgba(242, 234, 217, 0.88), rgba(242, 234, 217, 0.88)),
                    linear-gradient(135deg, #efe4cf 12%, #f7eee0 54%, #e6d1b0 100%);
                border: 1px solid rgba(58, 42, 32, 0.14);
                display: grid;
                place-items: center;
                color: var(--deep-umber);
                overflow: hidden;
                padding: 1.25rem;
            }

            .hero-map {
                width: 100%;
                max-width: 420px;
                aspect-ratio: 1 / 1;
                border-radius: 22px;
                background: #f2ead9;
                border: 1px solid rgba(58, 42, 32, 0.12);
                box-shadow: inset 0 0 0 1px rgba(58, 42, 32, 0.04);
                position: relative;
                overflow: hidden;
            }

            .hero-map::before {
                content: '';
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at 20% 25%, rgba(255, 255, 255, 0.35), transparent 12%),
                    radial-gradient(circle at 80% 70%, rgba(255, 249, 227, 0.35), transparent 12%);
                opacity: 0.7;
            }

            .hero-map .terrain-line,
            .hero-map .water-line {
                position: absolute;
                width: 240px;
                height: 240px;
                border-radius: 999px;
                border: 1px solid rgba(58, 42, 32, 0.08);
                left: 18%;
                top: 16%;
            }

            .hero-map .water-line {
                border-color: rgba(143, 166, 163, 0.24);
            }

            .hero-map .path {
                position: absolute;
                width: 110%;
                height: 110%;
                left: -5%;
                top: -4%;
                background: radial-gradient(circle at 65% 76%, transparent 12px, rgba(255, 255, 255, 0.68) 14px, transparent 18px);
            }

            .hero-map svg {
                position: relative;
                width: 100%;
                height: 100%;
            }

            .hero-map .pulse {
                animation: pulse 3s ease-out infinite;
                transform-origin: center;
                transform-box: fill-box;
            }

            .hero-title,
            .hero-subtitle,
            .hero-tags {
                opacity: 0;
                transform: translateY(8px);
                animation: fade-up 400ms ease-out forwards;
            }

            .hero-title {
                animation-delay: 0ms;
            }

            .hero-subtitle {
                animation-delay: 100ms;
            }

            .hero-tags {
                animation-delay: 200ms;
            }

            @media (prefers-reduced-motion: reduce) {
                .hero-map .pulse,
                .hero-title,
                .hero-subtitle,
                .hero-tags {
                    animation: none !important;
                    transform: none !important;
                    opacity: 1 !important;
                }
            }

            @keyframes fade-up {
                from {
                    opacity: 0;
                    transform: translateY(8px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes pulse {
                0% {
                    transform: scale(1);
                    opacity: 0.7;
                }
                50% {
                    transform: scale(1.18);
                    opacity: 0.24;
                }
                100% {
                    transform: scale(1);
                    opacity: 0.7;
                }
            }

            .timeline {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1.4rem;
                counter-reset: step;
                min-width: 0;
                width: 100%;
                box-sizing: border-box;
            }

            .timeline-step {
                position: relative;
                display: grid;
                grid-template-columns: 42px minmax(0, 1fr);
                gap: 1rem;
                padding: 1.3rem 1.4rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(58, 42, 32, 0.08);
                min-width: 0;
                max-width: none;
                box-sizing: border-box;
                overflow-wrap: normal !important;
                word-break: normal !important;
                hyphens: none !important;
            }

            .timeline-step > * {
                min-width: 0;
                width: 100%;
                max-width: none;
                box-sizing: border-box;
            }

            .timeline-step:not(:last-child)::after {
                content: '';
                position: absolute;
                top: 50%;
                right: -16px;
                width: 32px;
                height: 1px;
                background: rgba(58, 42, 32, 0.12);
                transform: translateY(-50%);
            }

            .timeline-step::before {
                content: counter(step);
                counter-increment: step;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: var(--sand);
                color: var(--deep-umber);
                font-weight: 800;
                border: 1px solid rgba(58, 42, 32, 0.1);
            }

            .timeline-step h3 {
                margin: 0 0 0.45rem 0;
                color: var(--deep-umber);
                font-size: 1rem;
            }

            .timeline-step p {
                margin: 0;
                color: #5c4d3d;
                line-height: 1.75;
                font-size: 0.96rem;
                width: 100%;
                max-width: none;
                white-space: normal !important;
                overflow-wrap: normal !important;
                word-break: normal !important;
            }

            .timeline-connector {
                display: block;
                position: relative;
                height: 100%;
            }

            .timeline-connector::after {
                content: '';
                position: absolute;
                left: 50%;
                top: 0;
                bottom: 0;
                width: 1px;
                background: rgba(58, 42, 32, 0.08);
                transform: translateX(-50%);
            }

            .timeline-row {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
            }

            @media (max-width: 980px) {
                .timeline {
                    grid-template-columns: repeat(2, minmax(220px, 1fr));
                }
            }

            @media (max-width: 640px) {
                .hero {
                    grid-template-columns: 1fr;
                }

                .timeline {
                    grid-template-columns: 1fr;
                }

                .timeline-step:not(:last-child)::after {
                    display: none;
                }

                .timeline-step {
                    grid-template-columns: 42px minmax(0, 1fr);
                }
            }

            .section {
                margin: 2rem 0;
                padding: 2rem;
                border-radius: 24px;
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid rgba(58, 42, 32, 0.12);
            }

            .section-soft {
                background: rgba(242, 234, 217, 0.9);
            }

            .section-title {
                font-family: 'Fraunces', Georgia, Cambria, 'Times New Roman', serif;
                font-size: clamp(1.8rem, 3vw, 2.4rem);
                margin: 0 0 0.85rem 0;
                color: var(--deep-umber);
                line-height: 1.1;
            }

            .section-copy {
                color: #4a382f;
                font-size: 1rem;
                line-height: 1.8;
                margin: 0;
                max-width: 780px;
            }

            .capability-grid,
            .feature-grid {
                display: grid;
                gap: 1rem;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                margin-top: 1.4rem;
            }

            .capability-card,
            .feature-card {
                padding: 1.35rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(58, 42, 32, 0.08);
                min-height: 170px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .capability-card h3,
            .feature-card h3 {
                color: var(--deep-umber);
                font-size: 1.1rem;
                margin: 0 0 0.65rem 0;
            }

            .capability-card p,
            .feature-card p {
                color: #5c4d3d;
                font-size: 0.98rem;
                line-height: 1.75;
                margin: 0;
            }

            .feature-mark {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 12px;
                background: rgba(179, 85, 47, 0.12);
                color: var(--clay);
                font-weight: 700;
                font-size: 1rem;
                margin-bottom: 0.9rem;
            }

            .chat-section {
                padding: 2rem;
                border-radius: 24px;
                background: rgba(242, 234, 217, 0.96);
                border: 1px solid rgba(58, 42, 32, 0.12);
                margin: 2rem 0;
            }

            .chat-header {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: flex-start;
                gap: 1rem;
                margin-bottom: 1rem;
            }

            .chat-title {
                margin: 0;
                font-family: 'Fraunces', Georgia, Cambria, 'Times New Roman', serif;
                font-size: clamp(1.7rem, 3vw, 2.4rem);
                color: var(--deep-umber);
                line-height: 1.05;
            }

            .chat-subtitle {
                margin: 0.35rem 0 0 0;
                color: #5c4d3d;
                font-size: 1rem;
                line-height: 1.75;
                max-width: 680px;
            }

            .chat-status {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.65rem 0.9rem;
                border-radius: 999px;
                background: rgba(91, 107, 71, 0.14);
                border: 1px solid rgba(91, 107, 71, 0.2);
                color: var(--olive);
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
            }

            .chat-helper {
                color: #5c4d3d;
                font-size: 1rem;
                line-height: 1.75;
                margin-bottom: 1.5rem;
            }

            [data-testid="stChatMessage"] {
                border-radius: 18px;
                padding: 0.85rem 1rem;
                background: #fbf4e8;
                border: 1px solid rgba(58, 42, 32, 0.08);
                color: var(--deep-umber) !important;
            }

            [data-testid="stChatMessage"] * {
                color: var(--deep-umber) !important;
            }

            [data-testid="stChatMessage"] p,
            [data-testid="stChatMessage"] div,
            [data-testid="stChatMessage"] span,
            [data-testid="stChatMessage"] li {
                color: var(--deep-umber) !important;
            }

            [data-testid="stChatInput"] textarea {
                background: #3a2a20 !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                color: #f7ede0 !important;
                caret-color: #f7ede0 !important;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: #d8c5b1 !important;
                opacity: 1;
            }

            [data-testid="stChatInput"] button {
                color: #f7ede0 !important;
            }

            .roadmap-list {
                display: grid;
                gap: 1rem;
                margin-top: 1.4rem;
            }

            .roadmap-item {
                padding: 1.2rem 1.3rem;
                border-radius: 18px;
                background: #ffffff;
                border: 1px solid rgba(58, 42, 32, 0.08);
                display: grid;
                gap: 0.45rem;
            }

            .roadmap-item strong {
                color: var(--deep-umber);
                font-size: 1rem;
                font-weight: 800;
            }

            .roadmap-item span {
                color: #5c4d3d;
                font-size: 0.95rem;
            }

            .roadmap-label {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: fit-content;
                padding: 0.4rem 0.75rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                color: #ffffff;
                transition: transform 150ms ease, box-shadow 150ms ease;
                transform-origin: center;
            }

            .roadmap-label:hover {
                transform: scale(1.03);
            }

            .status-complete {
                background: var(--olive);
            }

            .status-live {
                background: var(--clay);
            }

            .status-next {
                background: #8fa6a3;
            }

            .status-future {
                background: rgba(58, 42, 32, 0.18);
            }

            .footer {
                margin-top: 2rem;
                padding: 1.5rem;
                text-align: center;
                color: #5c4d3d;
                font-weight: 600;
                border-top: 1px solid rgba(58, 42, 32, 0.12);
            }

            .stButton > button {
                background: var(--clay);
                border: 0;
                color: #fff;
                border-radius: 999px;
                padding: 0.85rem 1.6rem;
                font-weight: 700;
            }

            .stButton > button:hover {
                background: #9b4f2d;
            }

            @media (max-width: 980px) {
                .hero,
                .capability-grid,
                .feature-grid,
                .roadmap-list {
                    grid-template-columns: 1fr;
                }

                .timeline {
                    grid-template-columns: repeat(2, minmax(220px, 1fr));
                }

                .hero {
                    grid-template-columns: 1fr;
                }

                .timeline-step:not(:last-child)::after {
                    display: none;
                }
            }

            @media (max-width: 640px) {
                .hero {
                    padding: 1.5rem;
                }

                .hero-title {
                    font-size: 2.6rem;
                }

                .sidebar-nav-item {
                    padding: 0.65rem 0.75rem;
                }

                .timeline {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar() -> None:
    """Render the ReliefLink AI sidebar in the field documentary style."""
    with st.sidebar:
        st.markdown(
            """
            <div>
                <div class="sidebar-title">
                    <span class="sidebar-logo" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="9" r="3" fill="#b3552f" />
                            <path d="M12 2C8.134 2 5 5.134 5 9c0 4.25 5.5 11 7 13 1.5-2 7-8.75 7-13 0-3.866-3.134-7-7-7Z" fill="none" stroke="#b3552f" stroke-width="1.8" />
                            <circle cx="12" cy="9" r="6.5" stroke="#b3552f" stroke-width="1.1" opacity="0.35" />
                        </svg>
                    </span>
                    <span>ReliefLink AI</span>
                </div>
                <div class="sidebar-subtitle">Disaster Response</div>
                <div class="sidebar-chip">SYSTEM ONLINE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown("### Navigation")
        st.markdown(
            """
            <div class="sidebar-nav-item"><span>Overview</span></div>
            <div class="sidebar-nav-item"><span>AI Assistant</span></div>
            <div class="sidebar-nav-item"><span>Memory</span></div>
            <div class="sidebar-nav-item"><span>Reporting</span></div>
            <div class="sidebar-nav-item"><span>Roadmap</span></div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="sidebar-meta">
                <span>Version {PROJECT_VERSION}</span>
                <span>{PROJECT_STATUS}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_status_strip() -> None:
    """Render the warm field report status strip."""
    st.markdown(
        """
        <div class="status-strip">
            <div><strong>Status:</strong> Field report mode</div>
            <div class="status-separator">•</div>
            <div>Last sync 00:02:14</div>
            <div class="status-separator">•</div>
            <div>Memory active</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    """Render the Field Documentary hero section."""
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-copy">
                <div class="hero-kicker">Field documentary report</div>
                <h1 class="hero-title">{APP_TITLE}</h1>
                <p class="hero-subtitle">{APP_SUBTITLE}</p>
                <p>{APP_DESCRIPTION}</p>
                <div class="hero-tags">
                    <span class="hero-tag">humanitarian</span>
                    <span class="hero-tag">field reporting</span>
                    <span class="hero-tag">memory-aware</span>
                </div>
            </div>
            <div class="hero-image">
                <div class="hero-map" role="img" aria-label="Map-inspired field coordination illustration showing terrain, water areas, a rescue point, and a route.">
                    <div class="terrain-line"></div>
                    <div class="water-line"></div>
                    <svg viewBox="0 0 320 320" aria-hidden="true" role="img">
                        <path d="M48 240 C92 216 110 148 162 137 C218 126 260 88 276 56" fill="none" stroke="#8fa6a3" stroke-width="3" stroke-linecap="round" opacity="0.72"/>
                        <path d="M48 158 C86 150 118 162 154 180 C186 196 210 218 240 228" fill="none" stroke="#8fa6a3" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
                        <path d="M120 82 C132 88 150 87 164 82" fill="none" stroke="#5c6b47" stroke-width="4" stroke-linecap="round" opacity="0.9"/>
                        <circle cx="180" cy="132" r="22" fill="#b3552f" opacity="0.96"/>
                        <circle cx="180" cy="132" r="10" fill="#f2ead9"/>
                        <path d="M174 152 L178 172 L182 152" stroke="#3a2a20" stroke-width="3" stroke-linecap="round"/>
                        <circle class="pulse" cx="180" cy="132" r="34" fill="none" stroke="rgba(179, 85, 47, 0.24)" stroke-width="3"/>
                        <circle cx="82" cy="232" r="12" fill="#5c6b47" opacity="0.9"/>
                        <path d="M84 226 L94 218 L100 232" fill="none" stroke="#fff8ec" stroke-width="3" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_about_section() -> None:
    """Render the prototype introduction as a field report."""
    st.markdown(
        """
        <section class="section section-soft">
            <div class="section-kicker">About the prototype</div>
            <h2 class="section-title">A quiet, grounded approach to relief reporting</h2>
            <p class="section-copy">
                ReliefLink AI is built to help field teams collect urgent disaster information
                with dignity and clarity. The experience is designed to feel like a trusted
                field report — warm, human, and focused on the people and places that need help.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_capabilities_section() -> None:
    """Render the platform capability overview."""
    st.markdown(
        """
        <section class="section">
            <div class="section-kicker">Platform capabilities</div>
            <h2 class="section-title">Built for resilient reporting and humanitarian context</h2>
            <p class="section-copy">
                The current prototype brings together AI-assisted incident capture, persistent
                memory, and future coordination support for on-the-ground responders.
            </p>
            <div class="capability-grid">
                <div class="capability-card">
                    <h3>Report disaster events</h3>
                    <p>Capture what happened, where it happened, and what kind of support is needed.</p>
                </div>
                <div class="capability-card">
                    <h3>Persistent AI memory</h3>
                    <p>Keep conversation context across exchanges so the assistant stays aligned
                    with ongoing relief priorities.</p>
                </div>
                <div class="capability-card">
                    <h3>Situation awareness</h3>
                    <p>Turn unstructured field details into clearer, response-ready updates.</p>
                </div>
                <div class="capability-card">
                    <h3>NGO coordination</h3>
                    <p>Prepare the groundwork for later integrations with relief partners and teams.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_feature_report() -> None:
    """Render the feature grid as a field report summary."""
    st.markdown(
        """
        <section class="section section-soft">
            <div class="section-kicker">Feature summary</div>
            <h2 class="section-title">What ReliefLink AI does today</h2>
        </section>
        """,
        unsafe_allow_html=True,
    )

    card_1, card_2 = st.columns(2, gap="large")

    with card_1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-mark">?</div>
                <h3>Report Disaster</h3>
                <p>Document urgent incidents clearly so response teams can act quickly.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-mark">?</div>
                <h3>Persistent AI Memory</h3>
                <p>Hold onto important details across the conversation for continuity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-mark">?</div>
                <h3>Future NGO Coordination</h3>
                <p>Create a foundation for future relief partner workflows and shared response.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-mark">??</div>
                <h3>Better Situation Awareness</h3>
                <p>Transform descriptions into actionable context that supports field decisions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_workflow_section() -> None:
    """Render the workflow as an editorial field-response timeline."""
    st.markdown(
        """
        <section class="section">
            <div class="section-kicker">How it works</div>
            <h2 class="section-title">From first report to sustained coordination</h2>
            <div class="timeline">
                <div class="timeline-step">
                    <h3>Report Situation</h3>
                    <p>Describe the incident as you see it on the ground.</p>
                </div>
                <div class="timeline-step">
                    <h3>AI Understands Context</h3>
                    <p>The assistant reads the situation and responds with clarity.</p>
                </div>
                <div class="timeline-step">
                    <h3>Remembers Important Information</h3>
                    <p>Key details stay available across the conversation.</p>
                </div>
                <div class="timeline-step">
                    <h3>Future Relief Coordination</h3>
                    <p>Build toward better handoff and shared response with aid partners.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_chat_section() -> None:
    """Render the Streamlit chat UI and preserve Backboard chat behavior."""
    st.markdown(
        """
        <section class="chat-section">
            <div class="chat-header">
                <div>
                    <div class="hero-kicker">Start a relief conversation</div>
                    <h1 class="chat-title">Report with care and clarity</h1>
                    <p class="chat-subtitle">
                        Share the situation in plain language, and ReliefLink AI will reply using
                        the existing Backboard-powered assistant and session memory.
                    </p>
                </div>
                <div class="chat-status">Active conversation</div>
            </div>
            <p class="chat-helper">
                Continue using the working assistant. This chat panel remains connected to the
                same thread and memory logic as before.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if not _initialize_chat_session():
        return

    for message in st.session_state.relief_chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input("Describe the situation or ask for guidance...")
    if not user_message:
        return

    st.session_state.relief_chat_messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("ReliefLink AI is reviewing your message..."):
            try:
                assistant_reply = send_message(st.session_state.relief_thread, user_message)
            except MessageSendError as exc:
                assistant_reply = (
                    "I could not send your message to ReliefLink AI right now. "
                    f"Details: {exc}"
                )
                st.error(assistant_reply)
            else:
                st.markdown(assistant_reply)

    st.session_state.relief_chat_messages.append(
        {"role": "assistant", "content": assistant_reply}
    )


def _initialize_chat_session() -> bool:
    """Load the persistent assistant and create one fresh in-memory thread."""
    if "relief_chat_messages" not in st.session_state:
        st.session_state.relief_chat_messages = []

    if "relief_thread" in st.session_state:
        return True

    try:
        assistant = create_or_load_assistant()
        st.session_state.relief_thread = create_thread(assistant)
    except BackboardConfigurationError as exc:
        st.warning(str(exc))
        return False
    except (AssistantCreationError, AssistantStoreError, ThreadCreationError) as exc:
        st.error(f"ReliefLink AI could not start a Backboard chat session. {exc}")
        return False

    return True


def _render_roadmap_section() -> None:
    """Render the editorial roadmap timeline."""
    roadmap_items = [
        ("Phase 1 — Interface", "✓ DONE", "status-complete"),
        ("Phase 2 — Disaster Reporting", "✓ DONE", "status-complete"),
        ("Phase 3 — AI Assistant", "→ ✓ DONE", "status-complete"),
        ("Phase 4 — Persistent Memory", "→ ✓ DONE", "status-complete"),
        ("Phase 5 — NGO Integration", "→ SOON", "status-live"),
    ]

    roadmap_html = "\n".join(
        f"<div class=\"roadmap-item\"><strong>{title}</strong><span class=\"roadmap-label {status}\">{label}</span></div>"
        for title, label, status in roadmap_items
    )

    st.markdown(
        f"""
        <section class="section section-soft">
            <div class="section-kicker">Roadmap</div>
            <h2 class="section-title">Current status and next phases</h2>
            <div class="roadmap-list">
                {roadmap_html}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_footer() -> None:
    """Render the homepage footer."""
    st.markdown(
        """
        <footer class="footer">
            Prototype built during MLH Global Hack Week: Agents.
        </footer>
        """,
        unsafe_allow_html=True,
    )
