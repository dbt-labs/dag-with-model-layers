import os
import streamlit as st


def set_variables():

    # set variables we always want to seed
    if not "dbt_metadata_url" in st.session_state:
        st.session_state["dbt_metadata_url"] = (
            "https://metadata.cloud.getdbt.com/beta/graphql"
        )

    DBT_API_TOKEN = st.sidebar.text_input(
        "dbt API Token",
        st.session_state.dbt_api_token if "dbt_api_token" in st.session_state else "",
        type="password",
    )
    DBT_ENV_ID = st.sidebar.text_input(
        "dbt Environment ID",
        st.session_state.dbt_env_id if "dbt_env_id" in st.session_state else "1",
    )

    # store variables in session state
    for variable in [
        {"key": "dbt_api_token", "value": DBT_API_TOKEN},
        {"key": "dbt_env_id", "value": int(DBT_ENV_ID)},
    ]:
        st.session_state[variable["key"]] = variable["value"]


def check_variables():
    if not check_session_state():
        st.warning("Please set all values shown in the sidebar on the homepage.")
        st.stop()


def check_session_state():
    return st.session_state.dbt_api_token and st.session_state.dbt_env_id
