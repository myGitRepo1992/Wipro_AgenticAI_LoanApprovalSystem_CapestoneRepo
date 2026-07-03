import streamlit as st
import requests
import json
from datetime import datetime
from config import FASTAPI_HOST, FASTAPI_PORT

st.set_page_config(
    page_title="Agentic AI Loan Approval",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}"

st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1f77b4; margin-bottom: 10px;}
    .section-header {font-size: 1.5rem; color: #ff7f0e; margin-top: 20px; margin-bottom: 10px;}
    .success-box {background-color: #d4edda; border: 1px solid #28a745; border-radius: 5px; padding: 15px; margin: 10px 0;}
    .error-box {background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 15px; margin: 10px 0;}
    .info-box {background-color: #d1ecf1; border: 1px solid #bee5eb; border-radius: 5px; padding: 15px; margin: 10px 0;}
    .metric-card {background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px; margin: 5px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🏦 Agentic AI Loan Approval System</div>", unsafe_allow_html=True)
st.markdown("*Multi-Agent Orchestration for Intelligent Loan Processing*")

tab1, tab2, tab3, tab4 = st.tabs(["📝 New Application", "📊 Application Status", "📈 Analytics", "🗄️ Database Viewer"])

with tab1:
    st.markdown("<div class='section-header'>Loan Application Form</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        applicant_name = st.text_input("Full Name *", placeholder="John Doe")
        applicant_id = st.text_input("Applicant ID *", placeholder="APP-12345")
        email = st.text_input("Email *", placeholder="john@example.com")
        phone = st.text_input("Phone Number", placeholder="+1-XXX-XXX-XXXX")

    with col2:
        annual_income = st.number_input("Annual Income ($) *", min_value=0, value=50000, step=1)
        employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Self-employed", "Contract", "Retired"])
        employment_years = st.number_input("Years of Employment", min_value=0, max_value=70, value=5)
        employment_company = st.text_input("Company/Organization", placeholder="Your Company")

    st.markdown("<div class='section-header'>Financial Information</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        credit_score = st.slider("Credit Score", 300, 850, 650)
        existing_debt = st.number_input("Existing Debt ($)", min_value=0, value=10000, step=1)

    with col4:
        loan_amount = st.number_input("Requested Loan Amount ($) *", min_value=1000, value=100000, step=1)
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Auto Purchase", "Debt Consolidation", "Business", "Education", "Other"]
        )

    st.markdown("<div class='section-header'>Loan Details</div>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        loan_tenure = st.number_input("Loan Tenure (Years) *", min_value=1, max_value=50, value=5)

    with col6:
        location = st.text_input("Location (City/State) *", placeholder="New York, NY")

    employment_status_map = {
        "Full-time": "employed",
        "Part-time": "contract",
        "Self-employed": "self-employed",
        "Contract": "contract",
        "Retired": "retired"
    }

    if st.button("🚀 Submit Application", use_container_width=True):
        if not all([applicant_name, applicant_id, email, annual_income, loan_amount, loan_tenure, location]):
            st.error("❌ Please fill in all required fields (*)")
        else:
            with st.spinner("⏳ Processing application through multi-agent system..."):
                try:
                    payload = {
                        "applicant_id": applicant_id,
                        "applicant_name": applicant_name,
                        "email": email,
                        "phone": phone,
                        "annual_income": annual_income,
                        "employment_type": employment_type,
                        "employment_years": employment_years,
                        "credit_score": credit_score,
                        "existing_debt": existing_debt,
                        "loan_amount": loan_amount,
                        "loan_purpose": loan_purpose,
                        "employment_company": employment_company,
                        "employment_status": employment_status_map[employment_type],
                        "loan_tenure": loan_tenure,
                        "location": location
                    }

                    response = requests.post(
                        f"{API_BASE_URL}/submit_application",
                        json=payload,
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_application = result
                        st.session_state.last_app_id = result.get("application_id")

                        st.markdown("<div class='success-box'>✅ <b>Application Processed Successfully!</b></div>", unsafe_allow_html=True)

                        st.markdown("### Decision Details")

                        col_decision, col_risk, col_confidence = st.columns(3)
                        with col_decision:
                            status_color = "🟢" if result["status"] == "approved" else "🔴" if result["status"] == "rejected" else "🟡"
                            st.metric("Decision", f"{status_color} {result['status'].upper()}")

                        with col_risk:
                            st.metric("Risk Score", f"{result['decision']['risk_score']:.1f}/100")

                        with col_confidence:
                            st.metric("Confidence", f"{result['decision']['confidence_level']*100:.1f}%")

                        st.markdown("### Detailed Analysis")

                        st.markdown("**Applicant Profile Assessment**")
                        profile = result["applicant_profile"]
                        col_profile1, col_profile2 = st.columns(2)
                        with col_profile1:
                            st.write(f"**Income Stability Score:** {profile['income_stability_score']:.1f}/100")
                            st.write(f"**Employment Risk:** {profile['employment_risk']}")
                        with col_profile2:
                            st.write(f"**Credit History:** {profile['credit_history_summary']}")

                        if profile["application_completeness_flags"]:
                            st.warning(f"**Flags:** {', '.join(profile['application_completeness_flags'])}")

                        st.markdown("**Financial Risk Analysis**")
                        risk = result["financial_risk"]
                        col_risk1, col_risk2 = st.columns(2)
                        with col_risk1:
                            st.write(f"**Debt-to-Income Ratio:** {risk['debt_to_income_ratio']:.2f}%")
                            st.write(f"**Credit Risk Level:** {risk['credit_score_risk_level']}")
                        with col_risk2:
                            st.write(f"**Loan Amount Risk:** {risk['loan_amount_risk']}")

                        if risk["anomaly_detection"]:
                            st.info(f"**Anomalies Detected:** {', '.join(risk['anomaly_detection'])}")

                        st.markdown("**Key Decision Factors**")
                        for factor in result["decision"]["key_decision_factors"]:
                            st.write(f"• {factor}")

                        st.markdown("**Decision Explanation**")
                        st.info(result["decision"]["explanation"])

                        st.markdown("**Compliance & Action**")
                        compliance = result["compliance_action"]
                        st.write(f"**Case ID:** `{compliance['case_id']}`")
                        st.write(f"**Action Taken:** {compliance['action_taken']}")
                        st.write(f"**Notification Sent:** {'✅ Yes' if compliance['notification_sent'] else '❌ No'}")
                        st.write(f"**Timestamp:** {compliance['timestamp']}")

                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.markdown(f"<div class='error-box'>❌ <b>Error:</b> {error_detail}</div>", unsafe_allow_html=True)

                except requests.exceptions.ConnectionError:
                    st.markdown("<div class='error-box'>❌ <b>Connection Error:</b> Ensure the microservice is running on port 8000</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<div class='error-box'>❌ <b>Error:</b> {str(e)}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section-header'>Application Status Lookup</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        app_id = st.text_input("Enter Application ID", placeholder="APP-XXXXXXXXXXXX")

    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)

    if search_button and app_id:
        with st.spinner("Fetching application status..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/application_status/{app_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()
                    data = result["data"]

                    st.markdown("<div class='success-box'>✅ Application Found</div>", unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        loan_status = data.get("loan_status", "unknown")
                        status_icon = "🟢" if loan_status == "approved" else "🔴" if loan_status == "rejected" else "🟡"
                        st.metric("Status", f"{status_icon} {loan_status.upper()}")

                    with col2:
                        st.metric("Risk Score", f"{data['decision']['risk_score']:.1f}")

                    with col3:
                        st.metric("Confidence", f"{data['decision']['confidence_level']*100:.1f}%")

                    st.json(data, expanded=False)

                else:
                    st.markdown("<div class='error-box'>❌ Application Not Found</div>", unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Error: {str(e)}</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section-header'>System Analytics</div>", unsafe_allow_html=True)

    try:
        # Fetch statistics from database
        stats_response = requests.get(f"{API_BASE_URL}/database_stats", timeout=10)
        # Fetch recent applications
        apps_response = requests.get(f"{API_BASE_URL}/applications", timeout=10)

        if stats_response.status_code == 200 and apps_response.status_code == 200:
            stats = stats_response.json().get("statistics", {})
            result = apps_response.json()
            applications = result.get("applications", [])

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Applications", stats.get("total_applications", 0))

            with col2:
                st.metric("Approved", stats.get("approved_count", 0), delta=f"{stats.get('approval_rate', 0):.1f}%")

            with col3:
                st.metric("Rejected", stats.get("rejected_count", 0), delta="negative")

            with col4:
                st.metric("Under Review", stats.get("review_count", 0))

            # Additional statistics
            st.markdown("**Additional Statistics**")
            stat_col1, stat_col2 = st.columns(2)

            with stat_col1:
                st.write(f"**Average Credit Score:** {stats.get('average_credit_score', 0):.0f}")

            with stat_col2:
                st.write(f"**Total Loan Amount:** ${stats.get('total_loan_amount', 0):,.2f}")

            # Recent applications
            if applications:
                st.markdown("**Recent Applications**")
                for app in applications:
                    status_icon = "🟢" if app.get("status") == "approved" else "🔴" if app.get("status") == "rejected" else "🟡"
                    with st.expander(f"{app['id']} - {status_icon} {app['status'].upper()}"):
                        col_exp1, col_exp2, col_exp3 = st.columns(3)
                        with col_exp1:
                            st.write(f"**Applicant:** {app.get('applicant_name', 'N/A')}")
                        with col_exp2:
                            st.write(f"**Loan Amount:** ${app.get('loan_amount', 0):,.2f}")
                        with col_exp3:
                            st.write(f"**Date:** {app.get('created_at', 'N/A')[:10]}")
            else:
                st.info("No applications processed yet.")

        else:
            st.error("Unable to fetch analytics data.")

    except Exception as e:
        st.error(f"Error fetching analytics: {str(e)}")

with tab4:
    st.markdown("<div class='section-header'>🗄️ Database Viewer & Search</div>", unsafe_allow_html=True)

    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])

    with search_col1:
        search_query = st.text_input(
            "Search by Application ID, Applicant ID, or Name",
            placeholder="APP-XXXXX or applicant name..."
        )

    with search_col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Approved", "Rejected", "Review"]
        )

    with search_col3:
        limit_records = st.number_input("Limit Results", min_value=5, max_value=500, value=50, step=5)

    col_search, col_stats = st.columns([1, 1])

    with col_search:
        search_btn = st.button("🔍 Search Database", use_container_width=True)

    with col_stats:
        stats_btn = st.button("📊 View Statistics", use_container_width=True)

    st.markdown("---")

    if stats_btn:
        with st.spinner("Loading database statistics..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/database_stats",
                    timeout=10
                )

                if response.status_code == 200:
                    stats = response.json()["statistics"]

                    stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

                    with stat_col1:
                        st.metric("Total Applications", stats["total_applications"])

                    with stat_col2:
                        st.metric("Approved", stats["approved_count"], delta=f"{stats['approval_rate']:.1f}%")

                    with stat_col3:
                        st.metric("Rejected", stats["rejected_count"])

                    with stat_col4:
                        st.metric("Under Review", stats["review_count"])

                    with stat_col5:
                        st.metric("Avg Credit Score", f"{stats['average_credit_score']:.0f}")

                    st.metric("Total Loan Amount", f"${stats['total_loan_amount']:,.2f}")

                else:
                    st.error("Failed to fetch statistics")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if search_btn or search_query:
        with st.spinner("Searching database..."):
            try:
                status_param = None if status_filter == "All" else status_filter.lower()

                response = requests.get(
                    f"{API_BASE_URL}/search_applications",
                    params={
                        "search_query": search_query if search_query else None,
                        "status_filter": status_param,
                        "limit": limit_records
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()
                    applications = result["applications"]

                    if applications:
                        st.markdown(f"### 📋 Found {result['count']} Applications")

                        display_df = []
                        for app in applications:
                            display_df.append({
                                "Application ID": app["application_id"],
                                "Applicant Name": app["applicant_name"],
                                "Status": app["status"].upper(),
                                "Loan Amount": f"${app['loan_amount']:,.2f}",
                                "Credit Score": app["credit_score"],
                                "Risk Score": f"{app['risk_score']:.1f}" if app['risk_score'] else "N/A",
                                "Date": app["created_at"][:10]
                            })

                        st.dataframe(display_df, use_container_width=True)

                        st.markdown("### 📊 Detailed View")

                        selected_app_id = st.selectbox(
                            "Select an Application for Details",
                            [app["application_id"] for app in applications],
                            key="app_selector"
                        )

                        if selected_app_id:
                            detail_response = requests.get(
                                f"{API_BASE_URL}/application_details/{selected_app_id}",
                                timeout=10
                            )

                            if detail_response.status_code == 200:
                                app_data = detail_response.json()["application"]

                                detail_tab1, detail_tab2, detail_tab3, detail_tab4 = st.tabs([
                                    "📋 Basic Info",
                                    "💰 Financial",
                                    "📊 Analysis",
                                    "✅ Decision"
                                ])

                                with detail_tab1:
                                    col_basic1, col_basic2 = st.columns(2)
                                    with col_basic1:
                                        st.write(f"**Application ID:** `{app_data['application_id']}`")
                                        st.write(f"**Applicant Name:** {app_data['applicant_name']}")
                                        st.write(f"**Email:** {app_data['email']}")
                                        st.write(f"**Phone:** {app_data.get('phone', 'N/A')}")

                                    with col_basic2:
                                        st.write(f"**Employment Type:** {app_data['employment_type']}")
                                        st.write(f"**Employment Years:** {app_data['employment_years']}")
                                        st.write(f"**Company:** {app_data.get('employment_company', 'N/A')}")
                                        st.write(f"**Status:** {app_data['loan_status']}")

                                with detail_tab2:
                                    col_fin1, col_fin2 = st.columns(2)
                                    with col_fin1:
                                        st.write(f"**Annual Income:** ${app_data['annual_income']:,.2f}")
                                        st.write(f"**Credit Score:** {app_data['credit_score']}")
                                        st.write(f"**Existing Debt:** ${app_data['existing_debt']:,.2f}")

                                    with col_fin2:
                                        st.write(f"**Loan Amount Requested:** ${app_data['loan_amount']:,.2f}")
                                        st.write(f"**Loan Purpose:** {app_data.get('loan_purpose', 'N/A')}")

                                with detail_tab3:
                                    st.write("**Applicant Profile:**")
                                    if app_data['applicant_profile']:
                                        profile = app_data['applicant_profile']
                                        st.write(f"• Income Stability Score: {profile.get('income_stability_score', 'N/A')}/100")
                                        st.write(f"• Employment Risk: {profile.get('employment_risk', 'N/A')}")
                                        st.write(f"• Credit Summary: {profile.get('credit_history_summary', 'N/A')}")

                                    st.write("**Financial Risk Analysis:**")
                                    if app_data['financial_risk']:
                                        risk = app_data['financial_risk']
                                        st.write(f"• DTI Ratio: {risk.get('debt_to_income_ratio', 'N/A')}%")
                                        st.write(f"• Credit Risk: {risk.get('credit_score_risk_level', 'N/A')}")
                                        st.write(f"• Loan Amount Risk: {risk.get('loan_amount_risk', 'N/A')}")

                                with detail_tab4:
                                    if app_data['loan_decision']:
                                        decision = app_data['loan_decision']
                                        decision_status = decision.get('classification', 'N/A').upper()
                                        status_color = "🟢" if decision_status == "APPROVED" else "🔴" if decision_status == "REJECTED" else "🟡"

                                        st.write(f"**Decision:** {status_color} {decision_status}")
                                        st.write(f"**Risk Score:** {decision.get('risk_score', 'N/A')}/100")
                                        st.write(f"**Confidence:** {decision.get('confidence_level', 'N/A')*100:.1f}%")

                                        st.write("**Key Factors:**")
                                        for factor in decision.get('key_decision_factors', []):
                                            st.write(f"• {factor}")

                                        st.write(f"**Explanation:** {decision.get('explanation', 'N/A')}")

                                st.markdown("---")
                                st.write(f"**Created:** {app_data['created_at']}")
                                st.write(f"**Updated:** {app_data['updated_at']}")

                    else:
                        st.info("📭 No applications found matching your search criteria.")

                else:
                    st.error("Failed to search database")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if not search_btn and not stats_btn and not search_query:
        st.info("👆 Use the search or statistics buttons above to query the database.")

st.sidebar.markdown("---")
st.sidebar.markdown("### System Information")
st.sidebar.write(f"**API Base URL:** {API_BASE_URL}")
st.sidebar.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.sidebar.markdown("### Multi-Agent Architecture")
st.sidebar.markdown("""
- **Applicant Profile Agent** - Income & employment analysis
- **Financial Risk Agent** - DTI & credit risk assessment
- **Decision Agent** - Final loan decision synthesis
- **Compliance Agent** - Notification & case management
""")

st.sidebar.markdown("### Orchestration Layer")
st.sidebar.markdown("LangGraph-based workflow management with parallel agent execution")
