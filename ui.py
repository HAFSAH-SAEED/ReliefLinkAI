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
    """Render the Phase 3 humanitarian landing page."""
    st.set_page_config(**page_config)
    _render_styles()
    _render_sidebar()
    _render_status_strip()
    _render_hero()
    _render_about_section()
    _render_feature_cards()
    _render_workflow_section()
    _render_chat_section()
    _render_roadmap_section()
    _render_footer()


def _render_styles() -> None:
    """Apply the humanitarian visual system for the landing page."""
    st.markdown(
        """
        <style>
            :root {
                --ink: #0b1215;
                --panel: #101c22;
                --signal-amber: #f2a341;
                --relief-teal: #2ea89a;
                --alert-red: #d94f4f;
                --paper: #eef2ee;
                --muted-fog: #7d919a;
            }

            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            .stApp {
                background: var(--paper);
                color: var(--ink);
                font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .block-container {
                max-width: 1180px;
                padding-top: 1.5rem;
                padding-bottom: 2.5rem;
            }

            [data-testid="stSidebar"] {
                background: var(--panel);
            }

            [data-testid="stSidebar"] * {
                color: #eef2ee;
            }

            .sidebar-brand {
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                margin-bottom: 1.25rem;
            }

            .sidebar-logo {
                width: 46px;
                height: 46px;
                display: grid;
                place-items: center;
                border-radius: 8px;
                background: rgba(46, 168, 154, 0.16);
                color: #eef2ee;
                font-size: 1.1rem;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }

            .sidebar-title {
                font-size: 1rem;
                font-weight: 800;
                letter-spacing: 0.02em;
                margin-bottom: 0.15rem;
            }

            .sidebar-subtitle {
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.72);
            }

            .sidebar-status {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.7rem 0.9rem;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.06);
                color: #d2f1eb;
                font-size: 0.85rem;
                font-weight: 700;
                margin-bottom: 1.2rem;
            }

            .status-dot {
                width: 0.55rem;
                height: 0.55rem;
                border-radius: 50%;
                background: var(--relief-teal);
                box-shadow: 0 0 0 4px rgba(46, 168, 154, 0.15);
            }

            .sidebar-nav-item {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                padding: 0.7rem 0.85rem;
                margin: 0.2rem 0;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.04);
                color: #dbeafe;
                font-size: 0.95rem;
                font-weight: 600;
            }

            .sidebar-nav-item:hover {
                cursor: pointer;
                background: rgba(255, 255, 255, 0.09);
            }

            .sidebar-index {
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                color: var(--relief-teal);
                font-size: 0.85rem;
            }

            .sidebar-footer {
                margin-top: 1.5rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255, 255, 255, 0.12);
                color: rgba(255, 255, 255, 0.72);
                font-size: 0.88rem;
            }

            .sidebar-version,
            .sidebar-prototype {
                display: block;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            }

            .status-strip {
                display: inline-flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 0.8rem;
                padding: 0.9rem 1rem;
                border-radius: 10px;
                border: 1px solid rgba(16, 28, 34, 0.12);
                background: #ffffff;
                color: var(--ink);
                font-size: 0.9rem;
                margin-bottom: 1.4rem;
            }

            .status-strip strong {
                font-weight: 700;
            }

            .status-separator {
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                color: var(--muted-fog);
            }

            .hero {
                padding: clamp(1.8rem, 3vw, 3rem);
                border-radius: 10px;
                background: #ffffff;
                border: 1px solid rgba(16, 28, 34, 0.12);
                color: var(--ink);
                margin-bottom: 1.75rem;
            }

            .hero-grid {
                display: grid;
                grid-template-columns: minmax(0, 1.35fr) minmax(260px, 0.75fr);
                gap: 1.5rem;
                align-items: center;
            }

            .hero h1 {
                font-size: clamp(2.7rem, 6vw, 4rem);
                line-height: 1.05;
                margin: 0 0 0.55rem 0;
                letter-spacing: -0.04em;
            }

            .hero h2 {
                font-size: clamp(1.05rem, 2.4vw, 1.5rem);
                font-weight: 700;
                margin: 0 0 1rem 0;
                color: var(--muted-fog);
            }

            .hero p {
                max-width: 620px;
                font-size: 1rem;
                line-height: 1.75;
                color: #475569;
                margin: 0 0 1rem 0;
            }

            .hero-status {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-bottom: 1rem;
            }

            .hero-pill {
                padding: 0.6rem 0.85rem;
                border-radius: 999px;
                background: rgba(46, 168, 154, 0.12);
                border: 1px solid rgba(46, 168, 154, 0.22);
                color: var(--relief-teal);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                text-transform: uppercase;
            }

            .hero-pill.alert {
                background: rgba(217, 79, 79, 0.12);
                border-color: rgba(217, 79, 79, 0.2);
                color: var(--alert-red);
            }

            .relief-illustration {
                min-height: 320px;
                border-radius: 10px;
                background: var(--panel);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 1.1rem;
            }

            .relief-illustration svg {
                width: min(100%, 320px);
                height: auto;
            }

            .section {
                margin: 2rem 0;
                padding: clamp(1.4rem, 3vw, 2.2rem);
                border-radius: 10px;
                background: #ffffff;
                border: 1px solid rgba(16, 28, 34, 0.12);
            }

            .section-soft {
                background: #f4f6f4;
            }

            .section-title {
                color: var(--ink);
                font-size: clamp(1.5rem, 3vw, 2rem);
                font-weight: 700;
                letter-spacing: -0.03em;
                margin: 0 0 0.75rem 0;
            }

            .section-kicker {
                color: var(--relief-teal);
                font-size: 0.84rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin-bottom: 0.55rem;
            }

            .section-copy {
                color: var(--muted-fog);
                font-size: 1rem;
                line-height: 1.75;
                max-width: 780px;
            }

            .feature-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1.4rem;
            }

            .feature-card {
                min-height: 170px;
                padding: 1.2rem;
                border-radius: 6px;
                background: #ffffff;
                border: 1px solid rgba(16, 28, 34, 0.12);
            }

            .feature-card h3 {
                color: var(--ink);
                font-size: 1rem;
                margin-bottom: 0.65rem;
                letter-spacing: -0.01em;
            }

            .feature-card p {
                color: #475569;
                line-height: 1.7;
                margin: 0;
            }

            .workflow {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.85rem;
                margin-top: 1.4rem;
            }

            .workflow-step {
                padding: 1rem;
                border-radius: 6px;
                background: #f4f6f4;
                border: 1px solid rgba(16, 28, 34, 0.12);
                text-align: center;
                color: var(--ink);
                font-weight: 700;
                letter-spacing: 0.01em;
                position: relative;
            }

            .workflow-step:not(:last-child)::after {
                content: '→';
                position: absolute;
                right: -0.65rem;
                top: 50%;
                transform: translateY(-50%);
                color: var(--muted-fog);
                font-size: 1rem;
            }

            .roadmap {
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 0.85rem;
                margin-top: 1.4rem;
            }

            .roadmap-item {
                padding: 1.1rem;
                border-radius: 6px;
                background: #ffffff;
                border: 1px solid rgba(16, 28, 34, 0.12);
                color: var(--ink);
                font-weight: 700;
                min-height: 110px;
            }

            .roadmap-item span {
                display: block;
                margin-top: 0.55rem;
                color: var(--muted-fog);
                font-size: 0.9rem;
                font-weight: 600;
            }

            .roadmap-complete {
                border-color: rgba(46, 168, 154, 0.28);
                background: rgba(46, 168, 154, 0.08);
            }

            .roadmap-live {
                border-color: rgba(242, 163, 65, 0.28);
                background: rgba(242, 163, 65, 0.08);
            }

            .roadmap-next {
                border-color: rgba(16, 28, 34, 0.18);
                background: #f7f7f7;
            }

            .roadmap-future {
                border-color: rgba(125, 145, 154, 0.2);
                background: #fafafa;
            }

            .chat-section {
                margin: 2rem 0;
                padding: clamp(1.4rem, 3vw, 2.4rem);
                border-radius: 10px;
                background: #f4f6f4;
                border: 1px solid rgba(16, 28, 34, 0.12);
                position: relative;
                padding-bottom: 5rem;
            }

            .chat-header {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }

            .chat-header-title {
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--ink);
            }

            .chat-header-status {
                display: inline-flex;
                align-items: center;
                gap: 0.55rem;
                padding: 0.55rem 0.85rem;
                border-radius: 999px;
                background: rgba(46, 168, 154, 0.12);
                border: 1px solid rgba(46, 168, 154, 0.18);
                color: var(--relief-teal);
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
            }

            .chat-helper {
                color: var(--muted-fog);
                font-size: 0.95rem;
                line-height: 1.7;
                margin-bottom: 1rem;
                max-width: 750px;
            }

            [data-testid="stChatMessage"] {
                border-radius: 10px;
                padding: 0.55rem 0.85rem;
                background: #ffffff;
                border: 1px solid rgba(16, 28, 34, 0.12);
                color: var(--ink) !important;
            }

            [data-testid="stChatMessage"] * {
                color: var(--ink) !important;
            }

            [data-testid="stChatMessage"] p,
            [data-testid="stChatMessage"] div,
            [data-testid="stChatMessage"] span,
            [data-testid="stChatMessage"] li {
                color: var(--ink) !important;
            }

            [data-testid="stChatInput"] {
                position: relative !important;
                z-index: 1;
                margin-top: 1rem;
            }

            [data-testid="stChatInput"] textarea {
                background: var(--panel) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                color: #eef2ee !important;
                caret-color: #eef2ee !important;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: rgba(255, 255, 255, 0.72) !important;
                opacity: 1;
            }

            [data-testid="stChatInput"] button {
                color: #eef2ee !important;
            }

            .footer {
                margin-top: 2rem;
                padding: 1.5rem;
                text-align: center;
                color: var(--muted-fog);
                border-top: 1px solid rgba(16, 28, 34, 0.12);
                font-weight: 600;
            }

            .stButton > button {
                background: var(--relief-teal);
                border: 0;
                color: #ffffff;
                border-radius: 999px;
                padding: 0.85rem 1.6rem;
                font-weight: 700;
                box-shadow: none;
            }

            .stButton > button:hover {
                background: #278f82;
                color: #ffffff;
                border: 0;
            }

            @media (max-width: 900px) {
                .hero-grid,
                .workflow,
                .roadmap,
                .feature-grid {
                    grid-template-columns: 1fr;
                }

                .workflow-step:not(:last-child)::after {
                    right: 50%;
                    top: auto;
                    bottom: -1.2rem;
                    transform: translateX(50%);
                }
            }

            @media (max-width: 640px) {
                .hero {
                    padding: 1.4rem 1rem;
                }

                .hero h1 {
                    font-size: 2.4rem;
                }

                .sidebar-nav-item {
                    padding: 0.65rem 0.75rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar() -> None:
    """Render the ReliefLink AI product sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">✚</div>
                <div>
                    <div class="sidebar-title">ReliefLink AI</div>
                    <div class="sidebar-subtitle">Disaster Response</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-status">
                <span class="status-dot"></span>
                SYSTEM ONLINE
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown("### Navigation")

        st.markdown(
            """
            <div class="sidebar-nav-item"><span class="sidebar-index">01</span> Overview</div>
            <div class="sidebar-nav-item"><span class="sidebar-index">AI</span> AI Assistant</div>
            <div class="sidebar-nav-item"><span class="sidebar-index">MEM</span> Memory</div>
            <div class="sidebar-nav-item"><span class="sidebar-index">RP</span> Reporting</div>
            <div class="sidebar-nav-item"><span class="sidebar-index">RM</span> Roadmap</div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            f"""
            <div class="sidebar-footer">
                <div class="sidebar-version">v{PROJECT_VERSION}</div>
                <div class="sidebar-prototype">{PROJECT_STATUS}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_status_strip() -> None:
    """Render the instrument-style application status strip."""
    st.markdown(
        """
        <div class="status-strip">
            <span class="status-dot"></span>
            <strong>SYSTEM ONLINE</strong>
            <span class="status-separator">·</span>
            <span>LAST SYNC 00:02:14</span>
            <span class="status-separator">·</span>
            <span>MEMORY: ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    """Render the homepage hero section."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-grid">
                <div>
                    <div class="section-kicker">Field operations console</div>
                    <h1>{APP_TITLE}</h1>
                    <h2>{APP_SUBTITLE}</h2>
                    <div class="hero-status">
                        <div class="hero-pill">AI ASSISTANT ONLINE</div>
                        <div class="hero-pill">MEMORY ACTIVE</div>
                    </div>
                    <p>
                        ReliefLink AI helps first responders report urgent incidents with calm,
                        operational guidance and situational context.
                    </p>
                </div>
                <div class="relief-illustration">
                    {_relief_svg()}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_about_section() -> None:
    """Render the landing page about section."""
    st.markdown(
        """
        <section class="section">
            <div class="section-kicker">Operations brief</div>
            <h2 class="section-title">Mission-ready incident reporting</h2>
            <p class="section-copy">
                ReliefLink AI is built to support faster, clearer disaster reporting during floods,
                medical emergencies, displacement, and infrastructure failures. The interface
                is designed to feel calm, precise, and reliable.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_feature_cards() -> None:
    """Render professional feature cards for the landing page."""
    st.markdown(
        """
        <section class="section section-soft">
            <div class="section-kicker">Core capabilities</div>
            <h2 class="section-title">Operational features available now</h2>
            <p class="section-copy">
                These modules describe the current console capabilities and planned next steps.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    card_1, card_2, card_3, card_4 = st.columns(4, gap="large")

    with card_1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>AI Disaster Assistant</h3>
                <p>Guided incident reporting that turns urgent events into clear updates.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Persistent AI Memory</h3>
                <p>Maintains context across the session so the assistant stays aligned.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Structured Reporting</h3>
                <p>Converts free-form details into concise response-ready incident summaries.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with card_4:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Future NGO Coordination</h3>
                <p>Planned integrations that connect relief organizations and field teams.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_workflow_section() -> None:
    """Render the horizontal disaster-reporting workflow preview."""
    st.markdown(
        """
        <section class="section">
            <div class="section-kicker">Workflow</div>
            <h2 class="section-title">Describe ? Understand ? Remember ? Coordinate</h2>
            <p class="section-copy">
                This sequence shows the operational path from first report to sustained response.
            </p>
            <div class="workflow">
                <div class="workflow-step">Describe</div>
                <div class="workflow-step">Understand</div>
                <div class="workflow-step">Remember</div>
                <div class="workflow-step">Coordinate</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_chat_section() -> None:
    """Render the Streamlit chat UI and send messages to Backboard.

    Streamlit reruns the script after each user interaction, so the assistant,
    fresh thread, and visible chat history are stored in st.session_state. This
    creates one thread for the user's current app session while preserving the
    existing persistent assistant from reliefLink.json.
    """
    st.markdown(
        """
        <section class="chat-section">
            <div class="chat-header">
                <div class="chat-header-title">ReliefLink Communications</div>
                <div class="chat-header-status">
                    <span class="status-dot"></span>
                    ACTIVE
                </div>
            </div>
            <div class="section-kicker">AI Chat</div>
            <h2 class="section-title">Report the incident in plain language</h2>
            <p class="chat-helper">
                Share what happened, where you are, and what help is needed. ReliefLink AI
                will respond using the persistent Backboard assistant with memory enabled.
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
    """Load the persistent assistant and create one fresh in-memory thread.

    The assistant is reused from reliefLink.json. The thread is created once per
    Streamlit browser session and never saved to disk, which keeps each app
    session separate while still allowing Backboard memory to work through the
    persistent assistant.
    """
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
    """Render the future product roadmap timeline."""
    st.markdown(
        """
        <section class="section section-soft">
            <div class="section-kicker">Roadmap</div>
            <h2 class="section-title">Current status and next phases</h2>
            <div class="roadmap">
                <div class="roadmap-item roadmap-complete">Phase 1 – Interface<span>COMPLETE</span></div>
                <div class="roadmap-item roadmap-live">Phase 2 – AI Assistant<span>LIVE</span></div>
                <div class="roadmap-item roadmap-live">Phase 3 – Persistent Memory<span>LIVE</span></div>
                <div class="roadmap-item roadmap-next">Phase 4 – Disaster Reporting<span>NEXT</span></div>
                <div class="roadmap-item roadmap-future">Phase 5 – NGO Integration<span>FUTURE</span></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_footer() -> None:
    """Render the landing page footer."""
    st.markdown(
        """
        <footer class="footer">
            Prototype built during MLH Global Hack Week: Agents.
        </footer>
        """,
        unsafe_allow_html=True,
    )


def _relief_svg() -> str:
    """Return inline open SVG artwork for humanitarian relief."""
    return """
    <svg viewBox="0 0 420 420" role="img" aria-label="Operations radar illustration" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#101c22"/>
                <stop offset="1" stop-color="#0e1620"/>
            </linearGradient>
        </defs>
        <rect x="10" y="10" width="400" height="400" rx="18" fill="url(#bg)"/>
        <circle cx="210" cy="210" r="128" fill="none" stroke="#2ea89a" stroke-width="6" opacity="0.2"/>
        <circle cx="210" cy="210" r="88" fill="none" stroke="#2ea89a" stroke-width="4" opacity="0.18"/>
        <circle cx="210" cy="210" r="44" fill="none" stroke="#2ea89a" stroke-width="3" opacity="0.22"/>
        <circle cx="210" cy="210" r="10" fill="#2ea89a"/>
        <path d="M210 140 c18 0 32 14 32 32 c0 18 -32 40 -32 40 s-32 -22 -32 -40 c0 -18 14 -32 32 -32 z" fill="#d94f4f"/>
        <circle cx="210" cy="172" r="8" fill="#ffffff"/>
        <line x1="86" y1="210" x2="334" y2="210" stroke="#2ea89a" stroke-width="2" opacity="0.2"/>
        <line x1="210" y1="86" x2="210" y2="334" stroke="#2ea89a" stroke-width="2" opacity="0.2"/>
        <circle cx="270" cy="160" r="6" fill="#2ea89a"/>
        <circle cx="145" cy="255" r="6" fill="#2ea89a"/>
        <rect x="92" y="312" width="120" height="10" rx="5" fill="#2ea89a" opacity="0.16"/>
        <rect x="92" y="292" width="70" height="6" rx="3" fill="#2ea89a" opacity="0.12"/>
    </svg>
    """
