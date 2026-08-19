import streamlit as st
from backend.ai.rag import build_rag_chain, ask
# from auth import sign_in, sign_up, reset_password, sign_out, is_authenticated

# ---------------------------------------------------
# PAGE CONFIG (must be first Streamlit command)
# ---------------------------------------------------
st.set_page_config(
    page_title="GovAssist AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# CUSTOM CSS (optional polish)
# ---------------------------------------------------

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Anton&family=Poppins:wght@500;600;700&display=swap');

    /* Base font for everything */
    * {
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
    }

    /* Subheadings (st.subheader, st.header) */
    h2, h3, div[data-testid="stMarkdownContainer"] h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #f5f5f5 !important;
    }

    /* App background */
    .stApp {
        background: radial-gradient(circle at top left, #1a1a2e 0%, #0f0f1a 60%);
    }

    /* Main page titles */
    .main-title {
        font-size: 2.3rem;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #facc15, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        color: #a0a0b8;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #14141f;
        border-right: 1px solid #2a2a3a;
    }
    .sidebar-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 400;
        color: #f5f5f5;
        letter-spacing: 0.5px;
    }
    .sidebar-subtext {
        font-family: 'Montserrat', sans-serif;
        color: #8e8ea8;
        font-size: 0.88rem;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        background-color: transparent;
        border: none;
        color: #cfcfe0;
        text-align: left;
        width: 100%;
        padding: 0.6rem 0.9rem;
        border-radius: 10px;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 3px;
        transition: all 0.15s ease-in-out;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        background-color: #26263a;
        color: #facc15;
        transform: translateX(2px);
    }

    /* Buttons everywhere else */
    .stButton button {
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        border: 1px solid #33334a;
        background-color: #1e1e2e;
        color: #f5f5f5;
        transition: all 0.15s ease-in-out;
    }
    .stButton button:hover {
        border-color: #facc15;
        color: #facc15;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #17172a;
        border: 1px solid #2a2a3f;
        border-radius: 12px;
        padding: 1rem;
    }
    div[data-testid="stMetricValue"] {
        color: #facc15;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif;
        color: #cfcfe0;
    }

    /* Scheme cards */
    .scheme-card {
        background-color: #17172a;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid #2a2a3f;
        margin-bottom: 0.9rem;
        transition: all 0.15s ease-in-out;
        font-family: 'Montserrat', sans-serif;
    }
    .scheme-card:hover {
        border-color: #facc15;
        transform: translateY(-2px);
    }

    /* Containers (used in Government Schemes page cards) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #17172a;
        border-radius: 12px;
        border: 1px solid #2a2a3f !important;
    }

    /* Text inputs / selects / number inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #17172a;
        color: #f5f5f5;
        border-radius: 10px;
        border: 1px solid #2a2a3f;
        font-family: 'Montserrat', sans-serif;
    }

    /* Dividers */
    hr {
        border-color: #2a2a3f !important;
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        background-color: #17172a;
        border-radius: 12px;
        border: 1px solid #2a2a3f;
    }

    /* Caption text */
    .stCaption, div[data-testid="stCaptionContainer"] {
        font-family: 'Montserrat', sans-serif;
        color: #8e8ea8;
    }
    </style>
""", unsafe_allow_html=True)

# # ---------------------------------------------------
# # LOGIN PAGE FUNCTION
# # ---------------------------------------------------

# def show_login_page():
#     """Render the full-screen login page with email/password authentication."""

#     # Hide sidebar on login page
#     st.markdown("""
#         <style>
#         section[data-testid="stSidebar"] { display: none; }
#         header[data-testid="stHeader"] { display: none; }
#         .block-container { padding-top: 0 !important; max-width: 100% !important; }
#         </style>
#     """, unsafe_allow_html=True)

#     # Login page specific styles
#     st.markdown("""
#         <style>
#         @keyframes gradientShift {
#             0% { background-position: 0% 50%; }
#             50% { background-position: 100% 50%; }
#             100% { background-position: 0% 50%; }
#         }
#         @keyframes float {
#             0%, 100% { transform: translateY(0px); }
#             50% { transform: translateY(-8px); }
#         }
#         @keyframes fadeInUp {
#             from { opacity: 0; transform: translateY(30px); }
#             to { opacity: 1; transform: translateY(0); }
#         }
#         @keyframes pulse {
#             0%, 100% { opacity: 1; }
#             50% { opacity: 0.7; }
#         }

#         .login-bg {
#             position: fixed;
#             top: 0; left: 0;
#             width: 100vw; height: 100vh;
#             background: linear-gradient(-45deg, #0a0a1a, #1a1a2e, #0f1628, #16213e, #0a0a1a);
#             background-size: 400% 400%;
#             animation: gradientShift 15s ease infinite;
#             z-index: -1;
#         }

#         .login-wrapper {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             min-height: 60vh;
#             animation: fadeInUp 0.8s ease-out;
#         }

#         /* Style Streamlit's native bordered container to look like the login card */
#         div[data-testid="stVerticalBlockBorderWrapper"] {
#             background: rgba(20, 20, 35, 0.85) !important;
#             backdrop-filter: blur(24px);
#             -webkit-backdrop-filter: blur(24px);
#             border: 1px solid rgba(250, 204, 21, 0.15) !important;
#             border-radius: 24px !important;
#             padding: 1rem 1.5rem !important;
#             box-shadow:
#                 0 8px 32px rgba(0, 0, 0, 0.4),
#                 0 0 80px rgba(250, 204, 21, 0.03),
#                 inset 0 1px 0 rgba(255, 255, 255, 0.05);
#         }

#         .login-logo {
#             font-size: 3.2rem;
#             text-align: center;
#             margin-bottom: 0.3rem;
#             animation: float 3s ease-in-out infinite;
#         }

#         .login-title {
#             font-family: 'Montserrat', sans-serif;
#             font-weight: 700;
#             font-size: 1.8rem;
#             text-align: center;
#             background: linear-gradient(135deg, #facc15, #f59e0b, #d97706);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             background-clip: text;
#             margin-bottom: 0.3rem;
#         }

#         .login-subtitle {
#             font-family: 'Montserrat', sans-serif;
#             color: #8e8ea8;
#             font-size: 0.92rem;
#             text-align: center;
#             margin-bottom: 2rem;
#         }

#         .login-divider {
#             height: 1px;
#             background: linear-gradient(90deg, transparent, rgba(250, 204, 21, 0.3), transparent);
#             margin: 1.5rem 0;
#         }

#         .login-footer {
#             font-family: 'Montserrat', sans-serif;
#             color: #5a5a7a;
#             font-size: 0.78rem;
#             text-align: center;
#             margin-top: 1.5rem;
#         }

#         .login-label {
#             font-family: 'Montserrat', sans-serif;
#             color: #cfcfe0;
#             font-size: 0.88rem;
#             margin-bottom: 0.3rem;
#             font-weight: 500;
#         }

#         .success-badge {
#             background: rgba(34, 197, 94, 0.12);
#             border: 1px solid rgba(34, 197, 94, 0.3);
#             border-radius: 12px;
#             padding: 0.7rem 1rem;
#             color: #4ade80;
#             font-family: 'Montserrat', sans-serif;
#             font-size: 0.88rem;
#             text-align: center;
#             margin-bottom: 1rem;
#         }

#         /* Style the login form inputs */
#         .stTextInput input {
#             background-color: rgba(23, 23, 42, 0.9) !important;
#             color: #f5f5f5 !important;
#             border: 1px solid #2a2a3f !important;
#             border-radius: 12px !important;
#             padding: 0.75rem 1rem !important;
#             font-family: 'Montserrat', sans-serif !important;
#             font-size: 1rem !important;
#             transition: border-color 0.2s ease !important;
#         }
#         .stTextInput input:focus {
#             border-color: #facc15 !important;
#             box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.1) !important;
#         }

#         /* Style login buttons */
#         .stButton button {
#             width: 100%;
#             background: linear-gradient(135deg, #facc15, #f59e0b) !important;
#             color: #0a0a1a !important;
#             border: none !important;
#             border-radius: 12px !important;
#             padding: 0.75rem 1.5rem !important;
#             font-family: 'Poppins', sans-serif !important;
#             font-weight: 600 !important;
#             font-size: 1rem !important;
#             cursor: pointer !important;
#             transition: all 0.2s ease !important;
#             box-shadow: 0 4px 15px rgba(250, 204, 21, 0.2) !important;
#         }
#         .stButton button:hover {
#             transform: translateY(-1px) !important;
#             box-shadow: 0 6px 20px rgba(250, 204, 21, 0.35) !important;
#             color: #0a0a1a !important;
#         }

#         /* Tab styling */
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 0;
#             background: rgba(15, 15, 25, 0.5);
#             border-radius: 14px;
#             padding: 4px;
#             border: 1px solid #2a2a3f;
#         }
#         .stTabs [data-baseweb="tab"] {
#             border-radius: 10px;
#             font-family: 'Poppins', sans-serif;
#             font-weight: 500;
#             font-size: 0.92rem;
#             color: #8e8ea8;
#             padding: 0.6rem 1.2rem;
#             background: transparent;
#             border: none;
#         }
#         .stTabs [aria-selected="true"] {
#             background: rgba(250, 204, 21, 0.12) !important;
#             color: #facc15 !important;
#             border: none !important;
#         }
#         .stTabs [data-baseweb="tab-highlight"] {
#             display: none;
#         }
#         .stTabs [data-baseweb="tab-border"] {
#             display: none;
#         }

#         /* Orb decorations */
#         .orb {
#             position: fixed;
#             border-radius: 50%;
#             filter: blur(80px);
#             opacity: 0.15;
#             pointer-events: none;
#             z-index: -1;
#         }
#         .orb-1 {
#             width: 400px; height: 400px;
#             background: #facc15;
#             top: -100px; right: -100px;
#             animation: float 6s ease-in-out infinite;
#         }
#         .orb-2 {
#             width: 300px; height: 300px;
#             background: #3b82f6;
#             bottom: -80px; left: -80px;
#             animation: float 8s ease-in-out infinite reverse;
#         }
#         .orb-3 {
#             width: 200px; height: 200px;
#             background: #8b5cf6;
#             top: 50%; left: 50%;
#             transform: translate(-50%, -50%);
#             animation: pulse 4s ease-in-out infinite;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # Background + orbs
#     st.markdown("""
#         <div class="login-bg"></div>
#         <div class="orb orb-1"></div>
#         <div class="orb orb-2"></div>
#         <div class="orb orb-3"></div>
#     """, unsafe_allow_html=True)

#     # Initialize login session state
#     if "login_error" not in st.session_state:
#         st.session_state.login_error = ""
#     if "login_success" not in st.session_state:
#         st.session_state.login_success = ""

#     # Center the login card using columns
#     col_left, col_center, col_right = st.columns([1, 1.2, 1])

#     with col_center:
#         st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

#         with st.container(border=True):
#             # Branding
#             st.markdown('<div class="login-logo">🏛️</div>', unsafe_allow_html=True)
#             st.markdown('<div class="login-title">GovAssist AI</div>', unsafe_allow_html=True)
#             st.markdown('<div class="login-subtitle">Your Government Scheme Assistant</div>', unsafe_allow_html=True)
#             st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

#             # Tabs: Login | Sign Up
#             tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Sign Up"])

#             # ─── LOGIN TAB ───
#             with tab_login:
#                 if st.session_state.login_success:
#                     st.markdown(f'<div class="success-badge">{st.session_state.login_success}</div>', unsafe_allow_html=True)
#                     st.session_state.login_success = ""

#                 st.markdown('<p class="login-label">✉️ Email</p>', unsafe_allow_html=True)
#                 login_email = st.text_input(
#                     "Email",
#                     placeholder="you@example.com",
#                     label_visibility="collapsed",
#                     key="login_email"
#                 )

#                 st.markdown('<p class="login-label">🔑 Password</p>', unsafe_allow_html=True)
#                 login_password = st.text_input(
#                     "Password",
#                     type="password",
#                     placeholder="Enter your password",
#                     label_visibility="collapsed",
#                     key="login_password"
#                 )

#                 if st.session_state.login_error:
#                     st.error(st.session_state.login_error)
#                     st.session_state.login_error = ""

#                 st.markdown("<div style='height: 0.3rem'></div>", unsafe_allow_html=True)

#                 if st.button("Login →", key="login_btn", use_container_width=True):
#                     if not login_email or not login_password:
#                         st.session_state.login_error = "Please enter both email and password."
#                         st.rerun()
#                     else:
#                         with st.spinner("Logging in..."):
#                             result = sign_in(login_email.strip(), login_password)

#                         if result["success"]:
#                             st.session_state.authenticated = True
#                             st.session_state.user = result.get("user")
#                             st.session_state.user_email = login_email.strip()
#                             st.rerun()
#                         else:
#                             st.session_state.login_error = result["error"]
#                             st.rerun()

#             # ─── SIGN UP TAB ───
#             with tab_signup:
#                 st.markdown('<p class="login-label">✉️ Email</p>', unsafe_allow_html=True)
#                 signup_email = st.text_input(
#                     "Email",
#                     placeholder="you@example.com",
#                     label_visibility="collapsed",
#                     key="signup_email"
#                 )

#                 st.markdown('<p class="login-label">🔑 Password</p>', unsafe_allow_html=True)
#                 signup_password = st.text_input(
#                     "Password",
#                     type="password",
#                     placeholder="Min. 6 characters",
#                     label_visibility="collapsed",
#                     key="signup_password"
#                 )

#                 st.markdown('<p class="login-label">🔑 Confirm Password</p>', unsafe_allow_html=True)
#                 signup_confirm = st.text_input(
#                     "Confirm Password",
#                     type="password",
#                     placeholder="Re-enter your password",
#                     label_visibility="collapsed",
#                     key="signup_confirm"
#                 )

#                 st.markdown("<div style='height: 0.3rem'></div>", unsafe_allow_html=True)

#                 if st.button("Create Account →", key="signup_btn", use_container_width=True):
#                     if not signup_email or not signup_password or not signup_confirm:
#                         st.error("Please fill in all fields.")
#                     elif len(signup_password) < 6:
#                         st.error("Password must be at least 6 characters.")
#                     elif signup_password != signup_confirm:
#                         st.error("Passwords do not match.")
#                     else:
#                         with st.spinner("Creating your account..."):
#                             result = sign_up(signup_email.strip(), signup_password)

#                         if result["success"]:
#                             st.session_state.login_success = "✅ Account created! Please check your email to confirm, then log in."
#                             st.rerun()
#                         else:
#                             st.error(result["error"])

#             # Footer
#             st.markdown("""
#                 <div class="login-footer">
#                     🔒 Secured by Supabase Authentication<br>
#                     Your data is encrypted and protected
#                 </div>
#             """, unsafe_allow_html=True)

#         st.markdown('</div>', unsafe_allow_html=True)  # close login-wrapper

#     st.stop()  # Prevent any app content from rendering

# # ---------------------------------------------------
# # AUTH GATE — Show login page if not authenticated
# # ---------------------------------------------------
# if not is_authenticated():
#     show_login_page()

# # ---------------------------------------------------
# # SESSION STATE INIT (only for authenticated users)
# # ---------------------------------------------------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "saved_schemes" not in st.session_state:
#     st.session_state.saved_schemes = []


# # ---------------------------------------------------
# # SIDEBAR NAVIGATION
# # ---------------------------------------------------

# st.markdown("""
#     <style>
#     section[data-testid="stSidebar"] {
#         background-color: #171717;
#     }
#     .sidebar-header {
#         font-size: 1.3rem;
#         font-weight: 700;
#         color: #f5f5f5;
#         margin-bottom: 0.1rem;
#     }
#     .sidebar-subtext {
#         color: #8e8e8e;
#         font-size: 0.9rem;
#         margin-bottom: 1rem;
#     }
#     section[data-testid="stSidebar"] div[data-testid="stButton"] button {
#         background-color: transparent;
#         border: none;
#         color: #d1d1d1;
#         text-align: left;
#         width: 100%;
#         padding: 0.6rem 0.8rem;
#         border-radius: 8px;
#         font-size: 0.95rem;
#         font-weight: 400;
#         margin-bottom: 2px;
#     }
#     section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
#         background-color: #2a2a2a;
#         color: white;
#     }
#     section[data-testid="stSidebar"] div[data-testid="stButton"] button:focus {
#         box-shadow: none;
#     }
#     </style>
# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "saved_schemes" not in st.session_state:
    st.session_state.saved_schemes = []

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

nav_items = [
    "🏠 Home",
    "🤖 AI Chat",
    "📜 Government Schemes",
    "✅ Eligibility Checker",
    "📄 Document Checklist",
    "⭐ Saved Schemes",
    "⚙️ Settings",
]

with st.sidebar:
    st.markdown('<div class="sidebar-header">🏛️ GovAssist AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtext">Your Government Scheme Assistant</div>', unsafe_allow_html=True)
    st.divider()

    for item in nav_items:
        is_active = st.session_state.page == item
        label = f"**{item}**" if is_active else item
        if st.button(label, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()

    # # ── User info & Logout (Commented out for now) ──
    # user_email = st.session_state.get("user_email", "User")
    # st.markdown(f"""
    #     <div style="
    #         background: rgba(250, 204, 21, 0.06);
    #         border: 1px solid rgba(250, 204, 21, 0.15);
    #         border-radius: 12px;
    #         padding: 0.8rem 1rem;
    #         margin-top: 0.5rem;
    #     ">
    #         <div style="font-family: 'Montserrat', sans-serif; color: #8e8ea8; font-size: 0.75rem; margin-bottom: 0.3rem;">
    #             Logged in as
    #         </div>
    #         <div style="font-family: 'Montserrat', sans-serif; color: #facc15; font-size: 0.9rem; font-weight: 600;">
    #             ✉️ {user_email}
    #         </div>
    #     </div>
    # """, unsafe_allow_html=True)

    # st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

    # if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
    #     sign_out()
    #     st.rerun()

# ---------------------------------------------------
# GLOBAL RESOURCES
# ---------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_rag_chain():
    return build_rag_chain()

page = st.session_state.page

# ---------------------------------------------------
# HOME PAGE
#----------------------------------------------------
if page == "🏠 Home":
    st.markdown('<div class="main-title">Government Scheme Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ask questions about government schemes, eligibility, and application steps — answered directly from official documents.</div>', unsafe_allow_html=True)

    search_query = st.text_input("🔍 Search schemes", placeholder="e.g. PM Awas Yojana, farmer schemes...")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Schemes Indexed", "15")
    with col2:
        st.metric("Categories", "6")
    with col3:
        st.metric("Documents Loaded", "15 PDFs")

    st.subheader("Current Schemes")
    popular = ["PM-KISAN", "PM Awas Yojana", "Ayushman Bharat",]
    cols = st.columns(3)
    for i, scheme in enumerate(popular):
        with cols[i % 3]:
            st.markdown(f'<div class="scheme-card"><b>{scheme}</b><br><span style="color:#888">Tap AI Chat to ask about this</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------
# AI CHAT PAGE
# ---------------------------------------------------
elif page == "🤖 AI Chat":

    # Build / load the chain with a friendly spinner
    with st.spinner("🔄 Loading knowledge base... (first run may take a minute)"):
        rag_chain = get_rag_chain()

    # Empty state — centered, ChatGPT style
    if not st.session_state.chat_history:
        st.markdown("""
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 55vh;
                text-align: center;
            ">
                <div style="font-size: 2rem; font-weight: 600; color: #e5e5e5;">
                    Ready when you are.
                </div>
                <div style="color: #8e8ea8; font-size: 0.95rem; margin-top: 0.5rem;">
                    Ask anything about PM-KISAN, PM Awas Yojana, Ayushman Bharat and more.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Render existing chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("📄 Sources"):
                    for src in msg["sources"]:
                        st.write(f"• {src}")

    # Chat input — always pinned at bottom like ChatGPT
    user_input = st.chat_input("Ask about a government scheme...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask(user_input, chain=rag_chain)
            answer = result["answer"]
            sources = result["sources"]
            st.markdown(answer)
            if sources:
                with st.expander("📄 Sources"):
                    for src in sources:
                        st.write(f"• {src}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })
# ---------------------------------------------------
# GOVERNMENT SCHEMES PAGE
# ---------------------------------------------------
elif page == "📜 Government Schemes":
    st.markdown('<div class="main-title">Government Schemes</div>', unsafe_allow_html=True)

    category = st.selectbox("Filter by category", ["All", "Agriculture", "Health", "Education"])
    # st.text_input("Search by scheme name")

    # Placeholder scheme data — replace with data pulled from your vector DB / metadata store
    schemes = [
        {"name": "PM-KISAN", "category": "Agriculture", "desc": "Income support of ₹6,000/year for eligible farmer families."},
        {"name": "Ayushman Bharat", "category": "Health", "desc": "Health insurance cover up to ₹5 lakh per family per year."},
        {"name": "PM Poshan Shakti Nirman (PM-POSHAN)", "category": "Education", "desc": "Scheme of the Government of India that provides one hot cooked nutritious meal to children studying in Government and Government-aided schools. It was earlier known as the Mid-Day Meal Scheme and was renamed PM-POSHAN in 2021."},
    ]

    for s in schemes:
        with st.container(border=True):
            st.markdown(f"**{s['name']}**  \n*{s['category']}*")
            st.write(s["desc"])
            c1, c2 = st.columns([1, 1])
            with c1:
                st.button("View Details", key=f"view_{s['name']}")
            with c2:
                if st.button("⭐ Save", key=f"save_{s['name']}"):
                    if s["name"] not in st.session_state.saved_schemes:
                        st.session_state.saved_schemes.append(s["name"])
                        st.success(f"Saved {s['name']}")

# ---------------------------------------------------
# ELIGIBILITY CHECKER PAGE
# ---------------------------------------------------
elif page == "✅ Eligibility Checker":
    st.markdown('<div class="main-title">Eligibility Checker</div>', unsafe_allow_html=True)
    st.caption("Fill in your details to find schemes you may be eligible for.")

    with st.form("eligibility_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
            state = st.selectbox("State", ["Punjab", "Haryana", "Delhi", "Uttar Pradesh", "Other"])
        with col2:
            occupation = st.selectbox("Occupation", ["Farmer", "Student", "Unemployed", "Self-employed", "Salaried", "Other"])
            income = st.number_input("Annual Income (₹)", min_value=0, value=200000, step=10000)

        submitted = st.form_submit_button("Check Eligibility")

    if submitted:
        with st.spinner("Analyzing eligibility using AI..."):
            rag_chain = get_rag_chain()
            prompt = f"Based on the following profile: Age {age}, State {state}, Occupation {occupation}, Annual Income ₹{income}, which government schemes are they eligible for and what are the specific criteria?"
            result = ask(prompt, chain=rag_chain)
            
        st.success("Eligibility Evaluation Complete:")
        st.markdown(result["answer"])
        if result.get("sources"):
            with st.expander("📄 Sources"):
                for src in result["sources"]:
                    st.write(f"• {src}")

# ---------------------------------------------------
# DOCUMENT CHECKLIST PAGE
# ---------------------------------------------------
elif page == "📄 Document Checklist":
    st.markdown('<div class="main-title">Document Checklist</div>', unsafe_allow_html=True)

    scheme_choice = st.selectbox("Select a scheme", ["PM-KISAN", "PM Awas Yojana", "Ayushman Bharat"])

    checklists = {
        "PM-KISAN": ["Aadhaar Card", "Bank Passbook", "Land Records", "Mobile Number"],
        "PM Awas Yojana": ["Aadhaar Card", "Income Certificate", "BPL Card (if applicable)", "Bank Passbook"],
        "PM Poshan Shakti Nirman (PM-POSHAN)": ["UDISE code and school details,Student enrolment register,Daily attendance register,Bank account passbook/details,Cooking cost expenditure records,Food grain stock register,Stock register for pulses, oil, vegetables, etc.,Cook-cum-helper payment records,Meal tasting register,School Management Committee (SMC) meeting records,Monthly MIS reports,Account statements and utilization records"],
    }

    st.subheader(f"Documents required for {scheme_choice}")
    for doc in checklists[scheme_choice]:
        st.checkbox(doc, key=f"doc_{scheme_choice}_{doc}")

# ---------------------------------------------------
# SAVED SCHEMES PAGE
# ---------------------------------------------------
elif page == "⭐ Saved Schemes":
    st.markdown('<div class="main-title">Saved Schemes</div>', unsafe_allow_html=True)

    if not st.session_state.saved_schemes:
        st.info("No schemes saved yet. Go to 'Government Schemes' and click ⭐ Save.")
    else:
        for s in st.session_state.saved_schemes:
            st.markdown(f'<div class="scheme-card"><b>{s}</b></div>', unsafe_allow_html=True)

# # ---------------------------------------------------
# # SETTINGS PAGE
# # ---------------------------------------------------
elif page == "⚙️ Settings":
    st.markdown('<div class="main-title">Settings & Developer Tools</div>', unsafe_allow_html=True)

    st.subheader("RAG Pipeline Testing")

    if st.button("📄 Test Document Loader"):
        from backend.ai.document_loader import load_documents

        docs = load_documents()

        st.success(f"Loaded {len(docs)} pages")
        st.write(docs[0].metadata)
        st.text(docs[0].page_content[:300])

    if st.button("✂️ Test Text Splitter"):
        from backend.ai.text_splitter import split_documents

        chunks = split_documents()

        st.success(f"Created {len(chunks)} chunks")
        st.write(chunks[0].metadata)
        st.text(chunks[0].page_content[:300])

    if st.button("🧠 Test Embeddings"):
        from backend.ai.embeddings import get_embeddings
        from backend.ai.text_splitter import split_documents

        chunks = split_documents()

        embedder = get_embeddings()

        vector = embedder.embed_query(chunks[0].page_content)

        st.success("Embeddings generated successfully!")
        st.write(f"Dimension: {len(vector)}")
        st.write(vector[:10])