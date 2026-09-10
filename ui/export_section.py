import streamlit as st
import pandas as pd

from screening.ranking_engine import rank_candidates
from screening.comparison_engine import compare_candidates


def show_export(match_results):

    if not match_results:
        return

    st.divider()

    st.header("📥 Export Results")

    ranked_candidates = rank_candidates(
        match_results
    )

    comparison = compare_candidates(
        ranked_candidates,
        match_results
    )

    dataframe = pd.DataFrame(
        comparison
    )

    csv_data = dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Screening Results",
        data=csv_data,
        file_name="prehier_screening_results.csv",
        mime="text/csv"
    )