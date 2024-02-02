import requests
import streamlit as st

from utils.queries import QUERY_LINEAGE

from .schemas import LineageDiscoResponse


@st.cache_data
def query_lineage(api_token: str, metadata_url: str, env_id: int, after_cursor=None):
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    json_data = {
        "query": QUERY_LINEAGE,
        "variables": {"environmentId": env_id, "filter": {"types": "Model"}},
    }
    response = requests.post(metadata_url, headers=headers, json=json_data).json()
    if response.get("errors"):
        st.write(
            "Error querying the Discovery API: ",
            response.get("errors")[0].get("message"),
        )
        st.stop()

    return LineageDiscoResponse.model_validate(response["data"])
