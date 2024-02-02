from copy import deepcopy
import streamlit as st
from utils.query_models import query_lineage
from utils.queries import QUERY_LINEAGE
from utils.set_variables import set_variables, check_variables


st.set_page_config(
    page_title="dbt Model layers",
    page_icon="🪄",
)

st.write("# Welcome to my website")
st.write(
    "This page tries to see how well we can guess model layers based on naming conventions and filepaths"
)
st.write("Enter all variables on the sidebar to query your project data")

set_variables()
check_variables()

st.write("Select a model and spell below to get started!")
project_name = st.text_input("Project Name", "fishtown_internal_analytics")
col1, col2 = st.columns(2)
with col1:
    layer_option = st.radio("Categorize layes by", ["prefix", "folder", "both"])
with col2:
    model_option = st.radio("Models Considered", ["all", "my project only"])

lineage = query_lineage(
    api_token=st.session_state.dbt_api_token,
    metadata_url=st.session_state.dbt_metadata_url,
    env_id=st.session_state.dbt_env_id,
)

st.write(
    f"{len(lineage.environment.applied.lineage)} models returned by the lineage request"
)

counter = {
    "staging": 0,
    "intermediate": 0,
    "marts": 0,
    "report": 0,
    "base": 0,
    "other": 0,
}
results = {
    "prefix": deepcopy(counter),
    "folder": deepcopy(counter),
    "both": deepcopy(counter),
}
records = []


def get_layer(string_list):
    if "stg" in string_list or "staging" in string_list:
        return "staging"
    elif "int" in string_list or "intermediate" in string_list:
        return "intermediate"
    elif "dim" in string_list or "fct" in string_list or "marts" in string_list:
        return "marts"
    else:
        return None


rollup = st.radio("See Results as", ["summary", "records"])

for model in lineage.environment.applied.lineage:
    package_name = model.uniqueId.split(".")[1]
    if model_option == "my project only":
        if package_name != project_name:
            continue
    model_name = model.name
    folders = model.filePath.split("/")
    model_name_parts = model_name.split("_")
    layer_by_folder = get_layer(folders)
    layer_by_prefix = get_layer(model_name_parts)
    layer_by_both = layer_by_prefix or layer_by_folder
    results["prefix"][(layer_by_prefix or "other")] = (
        results["prefix"].get((layer_by_prefix or "other")) + 1
    )
    results["folder"][(layer_by_folder or "other")] = (
        results["folder"].get((layer_by_folder or "other")) + 1
    )
    results["both"][(layer_by_both or "other")] = (
        results["both"].get((layer_by_both or "other")) + 1
    )
    records.append(
        {
            **model.model_dump(),
            "layer_by_prefix": layer_by_prefix,
            "layer_by_folder": layer_by_folder,
            "layer_by_both": layer_by_both,
        }
    )

if rollup == "summary":
    st.dataframe(results.get(layer_option))
else:
    st.dataframe(records)
