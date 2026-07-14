import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=st.secrets["NVIDIA_API_KEY"]
)

st.set_page_config(page_title="Customer 360 AI", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    h1 {
        font-size: 3rem !important;
        padding-bottom: 0.5rem;
    }
    .subtitle {
        color: #A0AEC0; 
        font-size: 24px; 
        margin-bottom: 50px;
    }
    div.stButton {
        display: flex;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    div.stButton > button:first-child {
        background-color: #00E5FF;
        color: #000000;
        font-size: 22px !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 20px 50px !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    }
    div.stButton > button:first-child:hover {
        background-color: #00B8D4;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.8);
    }
    .metric-card {
        background-color: #1E2329;
        border-left: 8px solid #00E5FF;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        margin-bottom: 20px;
        min-height: 280px;
    }
    .metric-card h4 {
        font-size: 28px !important;
        margin-top: 0;
        margin-bottom: 25px;
    }
    .metric-card p {
        font-size: 22px;
        margin: 12px 0;
    }
    .insight-card {
        background-color: #161A1F;
        padding: 35px;
        border-radius: 12px;
        border: 1px solid #2D3748;
        margin-bottom: 25px;
    }
    .insight-card h4 {
        font-size: 28px !important;
        margin-bottom: 20px;
        margin-top: 0;
    }
    .insight-card p {
        font-size: 24px;
        line-height: 1.6;
    }
    .action-card {
        background-color: #1A202C; 
        border: 2px solid #00E5FF; 
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.15);
        padding: 45px;
        border-radius: 15px;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .action-card h3 {
        color: #00E5FF !important; 
        font-size: 36px !important;
        margin-top: 0;
        margin-bottom: 25px;
    }
    .action-card p {
        color: #FFF; 
        font-size: 30px; 
        font-weight: bold; 
        margin-bottom: 0;
        line-height: 1.5;
    }
    h1, h2, h3, h4 {
        color: #E2E8F0 !important;
    }
    .streamlit-expanderContent {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 Unified Customer Intelligence View")
st.markdown("<p class='subtitle'>Automated multi-agent synthesis of cross-platform customer telemetry.</p>", unsafe_allow_html=True)

crm_data = {
    "source": "Zoho CRM",
    "account_name": "Grand Horizon Hotels & Resorts",
    "mrr": "$125,000",
    "tier": "Global Enterprise (50+ Properties)",
    "renewal_date": "2026-08-28 (45 Days)",
    "active_products": ["Hospitality Analytics Engine", "Dynamic Pricing API", "Central Reservations Sync"],
    "account_health_score": "42/100 (Critical Drop)",
    "key_stakeholders": [
        {"name": "Marcus Vance", "role": "VP of Revenue Management", "sentiment": "Detractor"},
        {"name": "Elena Rostova", "role": "Chief Operating Officer", "sentiment": "Neutral"}
    ]
}

support_data = {
    "source": "Support System",
    "recent_tickets": [
        {
            "ticket_id": "INC-00192",
            "status": "SLA BREACHED",
            "priority": "P0 - System Outage",
            "issue": "Real-time occupancy sync failing across 12 resort locations. Dynamic pricing API cannot pull live inventory.",
            "dev_notes": "Root cause identified as a rate-limiting conflict with their legacy Property Management System (PMS). We need their IT to whitelist our new routing endpoints."
        },
        {
            "ticket_id": "TSK-11405",
            "status": "Open",
            "priority": "High",
            "issue": "Data discrepancy: Revenue forecasting dashboard showing 4% variance compared to internal audits."
        }
    ]
}

slack_data = {
    "source": "Internal Slack",
    "channel": "#ent-grandhorizon-warroom",
    "thread": [
        {"user": "@csm_alex", "message": "Marcus just called me screaming. The occupancy sync failure is costing them thousands in missed dynamic pricing surges this weekend. He's threatening to block the $1.5M annual renewal."},
        {"user": "@sales_director", "message": "DO NOT let this churn. I have backchannel intel from procurement. Grand Horizon is in late-stage acquisition talks with a massive global hospitality group. If we secure this renewal, we have a foot in the door to pitch the parent company for a $10M+ contract."},
        {"user": "@tech_lead", "message": "I can't fix the sync until their IT team applies the patch, but Marcus keeps escalating to our CEO instead of letting his engineers work with us."}
    ]
}

st.markdown("## 📊 Active Data Streams")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4>🏢 CRM Data</h4>
        <p style="color:#A0AEC0;">Account: <b style="color:#FFF;">{crm_data.get('account_name')}</b></p>
        <p style="color:#A0AEC0;">MRR: <b style="color:#FFF;">{crm_data.get('mrr')}</b></p>
        <p style="color:#A0AEC0;">Renewal: <b style="color:#FFF;">{crm_data.get('renewal_date')}</b></p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("View Raw JSON Payload"):
        st.json(crm_data)

with col2:
    ticket_id = support_data.get('recent_tickets', [{}])[0].get('ticket_id', 'N/A')
    issue = support_data.get('recent_tickets', [{}])[0].get('issue', 'N/A')
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FF3D00;">
        <h4>🎫 Support System</h4>
        <p style="color:#A0AEC0;">Latest Ticket: <b style="color:#FFF;">{ticket_id}</b></p>
        <p style="color:#FF3D00; font-weight:bold;">Status: Escalated / Urgent</p>
        <p style="color:#A0AEC0; font-style:italic; font-size:16px;">"{issue}"</p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("View Raw JSON Payload"):
        st.json(support_data)

with col3:
    slack_channel = slack_data.get('channel', 'N/A')
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #651FFF;">
        <h4>💬 Internal Slack</h4>
        <p style="color:#FFF; font-weight:bold;">Channel: {slack_channel}</p>
        <p style="color:#A0AEC0; font-style:italic; line-height: 1.6; font-size:16px;">Active thread discussing stakeholder changes, competitor risk, and billing disputes.</p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("View Raw JSON Payload"):
        st.json(slack_data)

def analyze_customer_data():
    combined_data = {
        "crm": crm_data,
        "support": support_data,
        "slack": slack_data
    }
    
    prompt = f"""
    You are a data analyst multi-agent AI system. Analyze the following customer telemetry from multiple sources:
    {json.dumps(combined_data)}
    
    Return a JSON object with exactly these keys:
    - "summary": A one sentence overview of the customer context.
    - "risks": A short string detailing any churn or technical risks.
    - "opportunities": A short string detailing potential upsells or positive signals.
    - "next_best_action": A direct command on what the team should do next.
    
    Do not output any markdown formatting, just the raw JSON object.
    """

    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)

st.markdown("<br><br>", unsafe_allow_html=True)

if st.button("Initialize AI Synthesis"):
    st.markdown("---")
    with st.spinner("Compiling cross-platform telemetry..."):
        try:
            insights = analyze_customer_data()
            
            st.markdown("## 🧠 Synthesized Intelligence")
            
            st.markdown(f"""
            <div class="insight-card" style="border-top: 5px solid #00E5FF;">
                <h4 style="color: #00E5FF;">Context Summary</h4>
                <p style="color: #E2E8F0;">{insights.get("summary", "")}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-card" style="border-top: 5px solid #FF3D00;">
                <h4 style="color: #FF3D00;">⚠️ Identified Risks</h4>
                <p style="color: #E2E8F0;">{insights.get("risks", "")}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="insight-card" style="border-top: 5px solid #00E676;">
                <h4 style="color: #00E676;">💡 Growth Opportunities</h4>
                <p style="color: #E2E8F0;">{insights.get("opportunities", "")}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="action-card">
                <h3>🎯 Next Best Action</h3>
                <p>{insights.get("next_best_action", "")}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"System diagnostic error parsing response: {e}")