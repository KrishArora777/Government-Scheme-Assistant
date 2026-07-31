import streamlit as st

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
# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "saved_schemes" not in st.session_state:
    st.session_state.saved_schemes = []

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #171717;
    }
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f5f5f5;
        margin-bottom: 0.1rem;
    }
    .sidebar-subtext {
        color: #8e8e8e;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        background-color: transparent;
        border: none;
        color: #d1d1d1;
        text-align: left;
        width: 100%;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 2px;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        background-color: #2a2a2a;
        color: white;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:focus {
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

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

    st.divider()

page = st.session_state.page

# ---------------------------------------------------
# HOME PAGE
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

    # Empty state — centered, ChatGPT style
    if not st.session_state.chat_history:
        st.markdown("""
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 60vh;
                text-align: center;
            ">
                <div style="font-size: 2rem; font-weight: 600; color: #e5e5e5;">
                    Ready when you are.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Render existing chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("source"):
                with st.expander("📄 Source"):
                    st.write(msg["source"])

    # Chat input — always pinned at bottom like ChatGPT
    user_input = st.chat_input("Ask about a government scheme...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        answer = "This is a placeholder answer. Connect this to your LangChain RAG pipeline (rag.py) to generate real responses."
        source = "PM-KISAN_Guidelines.pdf, Page 4"

        st.session_state.chat_history.append({"role": "assistant", "content": answer, "source": source})
        with st.chat_message("assistant"):
            st.markdown(answer)
            with st.expander("📄 Source"):
                st.write(source)
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
        # --- Placeholder logic — replace with real rule engine or RAG-based eligibility check ---
        st.success("Based on your details, you may be eligible for:")
        st.markdown("- **PM-KISAN** (if you own agricultural land)")
        st.markdown("- **PM Jan Dhan Yojana** (open to all citizens)")
        st.info("This is placeholder logic — connect it to your eligibility rules or LLM-based checker.")

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
# elif page == "⚙️ Settings":
#     st.markdown('<div class="main-title">Settings</div>', unsafe_allow_html=True)

#     st.selectbox("LLM Provider", ["Ollama (Local)", "Gemini"])
#     st.selectbox("Embedding Model", ["qwen3-embedding:0.6b", "OllamaEmbeddings (default)"])
#     st.text_input("Vector Store Path", value="vectorstore/chroma_db")
#     st.button("Save Settings")
