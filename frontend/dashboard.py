import pandas as pd
import streamlit as st
import requests
import backend

st.set_page_config(
    page_title="Smart City Toll Dashboard",
    page_icon="🚦",
    layout="wide"
)

st.title("Smart City Automated Toll Enforcement Portal")
st.subheader("Connected Vehicle Telemetry Core Scanner & Billing Interface")
st.markdown("---")

# Sidebar
st.sidebar.header("Toll Station Controls")

vehicle_id = st.sidebar.text_input(
    "Scan Vehicle License Plate ID:",
    value="MH-12-NX-4567"
)

st.sidebar.markdown("""
### Operator Guidance:
1. Input the vehicle registration ID scanned at the gate.
2. Upload the extracted internal `.csv` telemetry log file.
3. Click **Process Invoice** to initiate the AI reasoning loop.
""")

# Main Layout
col1, col2 = st.columns(2)

# Left Column
with col1:
    st.header("Step 1: Extract Telemetry Data - Smart Toll")

    uploaded_file = st.file_uploader(
        "Choose a file (.csv)",
        type="csv"
    )

    if uploaded_file is not None:
        st.success("File uploaded successfully")

        df_preview = pd.read_csv(uploaded_file)
        st.dataframe(df_preview, use_container_width=True)

        # Reset file pointer
        uploaded_file.seek(0)

# Right Column
with col2:
    st.header("Step 2: Process Telemetry Data - Smart Toll")

    if uploaded_file is not None:

        if st.button("Process Toll & Run Deduction", type="primary"):

            with st.spinner(
                "Agent evaluating laws, processing logs, running calculations..."
            ):

                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "text/csv"
                        )
                    }

                    params = {
                        "vehicle_id": vehicle_id
                    }

                    backend_api_url = "http://localhost:8000/process-toll/"

                    api_response = requests.post(
                        backend_api_url,
                        params=params,
                        files=files
                    )

                    if api_response.status_code == 200:

                        data = api_response.json()

                        if data.get("status") == "Success":

                            st.success(
                                "Toll Processing Workflow Completed"
                            )

                            st.markdown(
                                "### Official Toll Audit Log Report:"
                            )

                            st.info(data.get("report"))

                        else:
                            st.error(
                                f"Backend Engine Refusal: "
                                f"{data.get('message')}"
                            )

                    else:
                        st.error(
                            f"HTTP Connection Failure "
                            f"Code: {api_response.status_code}"
                        )

                except Exception as e:
                    st.error(
                        "Could not connect to the FastAPI backend service. "
                        f"Is it offline?\n\nDetails: {e}"
                    )

    else:
        st.info(
            "Awaiting sensor telemetry log upload data "
            "from the left input panel."
        )