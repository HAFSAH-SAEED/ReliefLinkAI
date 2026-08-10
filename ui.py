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
                align-items: center;
                padding: 2rem;
                border-radius: 28px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(242, 234, 217, 0.96));
                border: 1px solid rgba(58, 42, 32, 0.12);
                box-shadow: 0 24px 70px rgba(58, 42, 32, 0.08);
                margin-bottom: 1.5rem;
                max-width: 100%;
                box-sizing: border-box;
            }

            .hero-copy {
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 1rem;
                min-width: 0;
                max-width: 100%;
            }

            .hero-kicker {
                font-size: 0.86rem;
                font-weight: 700;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: var(--clay);
                margin-bottom: 0.25rem;
            }

            .hero-title {
                font-family: 'Fraunces', Georgia, Cambria, 'Times New Roman', serif;
                font-size: clamp(2.7rem, 4.8vw, 4.7rem);
                line-height: 0.92;
                margin: 0;
                color: var(--deep-umber);
                letter-spacing: -0.02em;
            }

            .hero-subtitle {
                font-size: 1.08rem;
                color: var(--deep-umber);
                max-width: 650px;
                margin: 0;
                line-height: 1.7;
            }

            .hero-copy p {
                color: #4a382f;
                font-size: 1rem;
                line-height: 1.8;
                max-width: 660px;
                margin: 0;
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-top: 0.25rem;
            }

            .hero-pill {
                display: inline-flex;
                align-items: center;
                padding: 0.6rem 0.95rem;
                border-radius: 999px;
                background: rgba(179, 85, 47, 0.12);
                color: var(--clay);
                font-weight: 700;
                font-size: 0.82rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .hero-visual {
                min-height: 430px;
                width: 100%;
                max-width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                min-width: 0;
            }

            .hero-visual-shell {
                position: relative;
                width: 100%;
                max-width: 470px;
                min-height: 430px;
                border-radius: 28px;
                background: linear-gradient(145deg, rgba(58, 42, 32, 0.96), rgba(92, 107, 71, 0.92));
                border: 1px solid rgba(255, 255, 255, 0.14);
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), 0 20px 45px rgba(58, 42, 32, 0.2);
                overflow: hidden;
                padding: 1rem;
                box-sizing: border-box;
            }

            .hero-visual-shell::after {
                content: '';
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at top right, rgba(232, 169, 76, 0.18), transparent 32%);
                pointer-events: none;
            }

            .hero-map-panel {
                position: relative;
                width: 100%;
                height: 100%;
                border-radius: 22px;
                background: linear-gradient(180deg, rgba(242, 234, 217, 0.97), rgba(224, 213, 186, 0.96));
                border: 1px solid rgba(58, 42, 32, 0.12);
                overflow: hidden;
                min-width: 0;
                box-sizing: border-box;
            }

            .hero-map-panel::before {
                content: '';
                position: absolute;
                inset: 0;
                background-image: linear-gradient(rgba(58, 42, 32, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(58, 42, 32, 0.05) 1px, transparent 1px);
                background-size: 26px 26px;
                opacity: 0.45;
            }

            .hero-map-panel svg {
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
            }

            .hero-map-panel .map-route {
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at 26% 28%, rgba(255, 255, 255, 0.7), transparent 14%),
                    radial-gradient(circle at 72% 74%, rgba(255, 244, 219, 0.65), transparent 12%);
            }

            .hero-map-panel .map-pin {
                position: absolute;
                top: 26%;
                left: 63%;
                width: 76px;
                height: 76px;
                border-radius: 50%;
                border: 2px solid rgba(179, 85, 47, 0.28);
                background: rgba(179, 85, 47, 0.16);
                transform: translate(-50%, -50%);
                animation: pulse 3.2s ease-in-out infinite;
            }

            .hero-map-panel .map-pin::after {
                content: '';
                position: absolute;
                inset: 16px;
                border-radius: 50%;
                background: var(--clay);
                box-shadow: 0 0 0 6px rgba(179, 85, 47, 0.16);
            }

            .hero-map-panel .map-signal {
                position: absolute;
                bottom: 14%;
                left: 16%;
                width: 180px;
                height: 180px;
                border: 1px dashed rgba(143, 166, 163, 0.38);
                border-radius: 50%;
            }

            .hero-report-card {
                position: absolute;
                left: 1.2rem;
                bottom: 1.2rem;
                width: min(72%, 270px);
                padding: 1rem 1rem 0.95rem;
                border-radius: 18px;
                background: rgba(255, 248, 236, 0.94);
                border: 1px solid rgba(58, 42, 32, 0.12);
                box-shadow: 0 16px 32px rgba(58, 42, 32, 0.12);
                backdrop-filter: blur(6px);
                min-width: 0;
                box-sizing: border-box;
            }

            .hero-report-card .report-label {
                font-size: 0.74rem;
                font-weight: 800;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: var(--clay);
                margin-bottom: 0.3rem;
            }

            .hero-report-card .report-title {
                font-size: 1.02rem;
                font-weight: 800;
                color: var(--deep-umber);
                margin-bottom: 0.35rem;
            }

            .hero-report-card .report-meta,
            .hero-report-card .report-copy {
                font-size: 0.9rem;
                color: #5c4d3d;
                line-height: 1.6;
                margin: 0 0 0.25rem 0;
                overflow-wrap: anywhere;
            }

            .hero-report-card .report-button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-top: 0.7rem;
                padding: 0.58rem 0.95rem;
                border-radius: 999px;
                background: var(--clay);
                color: #fff;
                font-weight: 700;
                font-size: 0.82rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }

            .hero-title,
            .hero-subtitle,
            .hero-actions {
                opacity: 0;
                transform: translateY(8px);
                animation: fade-up 450ms ease-out forwards;
            }

            .hero-title {
                animation-delay: 0ms;
            }

            .hero-subtitle {
                animation-delay: 100ms;
            }

            .hero-actions {
                animation-delay: 200ms;
            }

            @media (prefers-reduced-motion: reduce) {
                .hero-map-panel .map-pin,
                .hero-title,
                .hero-subtitle,
                .hero-actions {
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
                    transform: scale(1.12);
                    opacity: 0.26;
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
                box-shadow: 0 18px 40px rgba(58, 42, 32, 0.06);
                max-width: 100%;
                box-sizing: border-box;
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

            .feature-strip {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1.35rem;
                width: 100%;
                box-sizing: border-box;
            }

            .feature-strip-card {
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
                padding: 1rem 1rem 1.1rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(58, 42, 32, 0.08);
                min-width: 0;
                box-sizing: border-box;
            }

            .feature-strip-card h3 {
                color: var(--deep-umber);
                font-size: 1rem;
                margin: 0;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }

            .feature-strip-card p {
                color: #5c4d3d;
                font-size: 0.94rem;
                line-height: 1.65;
                margin: 0;
                overflow-wrap: anywhere;
            }

            .impact-strip {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1.2rem;
                width: 100%;
                box-sizing: border-box;
                padding: 1.2rem;
                border-radius: 22px;
                background: linear-gradient(135deg, rgba(92, 107, 71, 0.96), rgba(58, 42, 32, 0.96));
                color: #f8efe2;
            }

            .impact-item {
                display: flex;
                flex-direction: column;
                gap: 0.35rem;
                min-width: 0;
                box-sizing: border-box;
            }

            .impact-item strong {
                font-size: 0.98rem;
                font-weight: 800;
                color: #fff8e9;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }

            .impact-item span {
                color: rgba(248, 239, 226, 0.82);
                font-size: 0.92rem;
                line-height: 1.6;
                overflow-wrap: anywhere;
            }

            .feature-icon {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: rgba(179, 85, 47, 0.12);
                color: var(--clay);
                flex-shrink: 0;
            }

            .feature-icon svg {
                width: 24px;
                height: 24px;
                stroke: currentColor;
                fill: none;
                stroke-width: 1.8;
                stroke-linecap: round;
                stroke-linejoin: round;
            }

            .capability-grid,
            .feature-grid {
                display: grid;
                gap: 1rem;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                margin-top: 1.4rem;
                width: 100%;
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
                width: 100%;
                box-sizing: border-box;
                min-width: 0;
                overflow-wrap: anywhere;
            }

            .capability-card h3,
            .feature-card h3 {
                color: var(--deep-umber);
                font-size: 1.1rem;
                margin: 0 0 0.65rem 0;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }

            .capability-card p,
            .feature-card p {
                color: #5c4d3d;
                font-size: 0.98rem;
                line-height: 1.75;
                margin: 0;
                overflow-wrap: anywhere;
            }

            .feature-mark {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: rgba(179, 85, 47, 0.12);
                color: var(--clay);
                margin-bottom: 0.9rem;
                flex-shrink: 0;
            }

            .feature-mark svg {
                width: 24px;
                height: 24px;
                stroke: currentColor;
                fill: none;
                stroke-width: 1.8;
                stroke-linecap: round;
                stroke-linejoin: round;
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
                width: 100%;
            }

            .roadmap-item {
                padding: 1.2rem 1.3rem;
                border-radius: 18px;
                background: #ffffff;
                border: 1px solid rgba(58, 42, 32, 0.08);
                display: grid;
                gap: 0.45rem;
                width: 100%;
                box-sizing: border-box;
                min-width: 0;
            }

            .roadmap-item strong {
                color: var(--deep-umber);
                font-size: 1rem;
                font-weight: 800;
                line-height: 1.35;
                overflow-wrap: anywhere;
            }

            .roadmap-item span {
                color: #5c4d3d;
                font-size: 0.95rem;
                overflow-wrap: anywhere;
            }

            .roadmap-label {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: fit-content;
                max-width: 100%;
                padding: 0.4rem 0.75rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                color: #ffffff;
                transition: transform 150ms ease, box-shadow 150ms ease;
                transform-origin: center;
                white-space: normal;
                text-align: center;
                line-height: 1.3;
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

                .feature-strip,
                .impact-strip {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
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

                .section,
                .chat-section {
                    padding: 1.3rem;
                }

                .capability-grid,
                .feature-grid {
                    grid-template-columns: 1fr;
                }

                .feature-strip,
                .impact-strip {
                    grid-template-columns: 1fr;
                }

                .roadmap-item {
                    padding: 1rem 1rem;
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
    """Render the Field Documentary hero section with an editorial humanitarian visual."""
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-copy">
                <div class="hero-kicker">Field documentary • ReliefLink AI</div>
                <h1 class="hero-title">AI-POWERED<br/>RELIEF.<br/>REAL IMPACT.</h1>
                <p class="hero-subtitle">Turning urgent situations into coordinated action through intelligence, memory, and collaboration.</p>
                <p>{APP_DESCRIPTION}</p>
                <div class="hero-actions">
                    <span class="hero-pill">Humanitarian field ops</span>
                    <span class="hero-pill">Trusted coordination</span>
                    <span class="hero-pill">Memory-aware support</span>
                </div>
            </div>
            <div class="hero-visual" aria-hidden="true">
                <div class="hero-visual-shell">
                    <div class="hero-map-panel">
                        <div class="map-route"></div>
                        <div class="map-pin"></div>
                        <div class="map-signal"></div>
                        <svg viewBox="0 0 320 320" role="img">
                            <path d="M48 240 C92 216 112 150 164 138 C216 126 256 92 278 56" fill="none" stroke="#8fa6a3" stroke-width="3" stroke-linecap="round" opacity="0.72"/>
                            <path d="M48 158 C88 152 118 162 154 182 C188 202 208 220 240 228" fill="none" stroke="#8fa6a3" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
                            <path d="M118 84 C130 90 148 90 162 84" fill="none" stroke="#5c6b47" stroke-width="4" stroke-linecap="round" opacity="0.95"/>
                            <circle cx="180" cy="132" r="20" fill="#b3552f" opacity="0.96"/>
                            <circle cx="180" cy="132" r="9" fill="#f2ead9"/>
                            <path d="M174 152 L178 172 L182 152" stroke="#3a2a20" stroke-width="3" stroke-linecap="round"/>
                            <circle cx="86" cy="232" r="12" fill="#5c6b47" opacity="0.9"/>
                            <path d="M88 226 L98 218 L104 232" fill="none" stroke="#fff8ec" stroke-width="3" stroke-linecap="round"/>
                        </svg>
                        <div class="hero-report-card">
                            <div class="report-label">ReliefLink AI</div>
                            <div class="report-title">Incident Report</div>
                            <p class="report-meta">Location: Flood / affected area</p>
                            <p class="report-copy">People trapped, need immediate rescue.</p>
                            <div class="report-button">Send Report</div>
                        </div>
                    </div>
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
    """Render the platform capability overview in a concise editorial tone."""
    st.markdown(
        """
        <section class="section">
            <div class="section-kicker">Editorial approach</div>
            <h2 class="section-title">Built for trust, clarity, and field-ready coordination</h2>
            <p class="section-copy">
                ReliefLink AI turns urgent observations into coordinated action through incident
                capture, memory-aware context, and stronger collaboration across the response chain.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_feature_report() -> None:
    """Render the editorial feature strip and impact strip."""
    st.markdown(
        """
        <section class="section section-soft">
            <div class="section-kicker">Field capabilities</div>
            <h2 class="section-title">What ReliefLink AI brings into view</h2>
            <div class="feature-strip">
                <div class="feature-strip-card">
                    <div class="feature-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                            <path d="M4 8.5h8l3-2.5v11l-3-2.5H4z" />
                            <path d="M13 10.5v3" />
                            <path d="M17 10.5c1.3 0 2.3 1 2.3 2.3S18.3 15 17 15" />
                            <path d="M4 8.5v7" />
                        </svg>
                    </div>
                    <h3>Report Disaster</h3>
                    <p>Document urgent incidents clearly so response teams can act quickly.</p>
                </div>
                <div class="feature-strip-card">
                    <div class="feature-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                            <path d="M8 8.5c0-2.2 1.8-4 4-4h1.2c1.5 0 2.7 1 3.3 2.4" />
                            <path d="M13.8 7.8c1.4.2 2.5 1.3 2.8 2.7" />
                            <path d="M9.5 10.8c0 2.8 1.5 4.7 3.5 5.6" />
                            <path d="M16.5 10.8c0 2.8-1.5 4.7-3.5 5.6" />
                            <path d="M11 7.3c0-.7.6-1.3 1.3-1.3h1.4c.7 0 1.3.6 1.3 1.3v1.2" />
                        </svg>
                    </div>
                    <h3>AI Memory</h3>
                    <p>Keep important details available across the conversation for continuity.</p>
                </div>
                <div class="feature-strip-card">
                    <div class="feature-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                            <path d="M7 8.5l3-3h2l-2 4H8l-2 2" />
                            <path d="M14 6.5l3-3h2l-2 4h-1l-2 2" />
                            <path d="M8.5 10.5l2 2 2-2" />
                            <path d="M10.5 12.5v3" />
                            <path d="M14.5 12.5v3" />
                        </svg>
                    </div>
                    <h3>NGO Coordination</h3>
                    <p>Create a foundation for future relief partner workflows and shared response.</p>
                </div>
                <div class="feature-strip-card">
                    <div class="feature-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                            <path d="M6 5.5h12" />
                            <path d="M6 12h12" />
                            <path d="M6 18.5h12" />
                            <path d="M9 4.5v15" />
                            <path d="M15 4.5v15" />
                            <path d="M12 7.2c1.7 0 3.1 1.3 3.1 2.9S13.7 13 12 13s-3.1-1.3-3.1-2.9S10.3 7.2 12 7.2z" />
                            <path d="M12 11.7v4.8" />
                        </svg>
                    </div>
                    <h3>Situation Awareness</h3>
                    <p>Bring scattered details into a more actionable field picture.</p>
                </div>
            </div>
            <div class="impact-strip">
                <div class="impact-item">
                    <strong>Faster Response</strong>
                    <span>Help reaches sooner</span>
                </div>
                <div class="impact-item">
                    <strong>Smarter Coordination</strong>
                    <span>NGOs working together</span>
                </div>
                <div class="impact-item">
                    <strong>Persistent Memory</strong>
                    <span>No important detail gets lost</span>
                </div>
                <div class="impact-item">
                    <strong>Better Decisions</strong>
                    <span>Data-driven field action</span>
                </div>
            </div>
        </section>
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
        ("Phase 3 — AI Assistant", "✓ DONE", "status-complete"),
        ("Phase 4 — Persistent Memory", "✓ DONE", "status-complete"),
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
