import streamlit as st


def show_candidate_profiles(candidate_profiles):

    if not candidate_profiles:
        return

    st.divider()

    st.header("👥 Candidate Profiles")

    for candidate_name, candidate_profile in candidate_profiles.items():

        with st.expander(
            f"👤 {candidate_name}"
        ):
            st.json(candidate_profile)


def show_screening_results(match_results):

    if not match_results:
        return

    st.divider()

    st.header("📊 Screening Results")

    for candidate_name, result in match_results.items():

        st.subheader(
            f"📄 {candidate_name}"
        )

        st.metric(
            "Overall Match Score",
            f"{result['overall_score']}%"
        )

        st.write("### Score Breakdown")

        st.write(
            f"Required Skills: "
            f"**{result['required_skills']['score']}%**"
        )

        st.write(
            f"Preferred Skills: "
            f"**{result['preferred_skills']['score']}%**"
        )

        st.write(
            f"Experience: "
            f"**{result['experience_score']}%**"
        )

        st.write(
            f"Education: "
            f"**{result['education_score']}%**"
        )

        st.write(
            f"Project Relevance: "
            f"**{result['project_relevance_score']}%**"
        )

        st.write("### 🎯 Skill Screening")

        required_result = result["required_skills"]

        st.write(
            "**Matched Required Skills**"
        )

        if required_result["matched_skills"]:
            st.write(
                required_result["matched_skills"]
            )
        else:
            st.write(
                "No required skills matched."
            )

        st.write(
            "**Missing Required Skills**"
        )

        if required_result["missing_skills"]:
            st.write(
                required_result["missing_skills"]
            )
        else:
            st.write(
                "No required skills are missing."
            )

        preferred_result = result["preferred_skills"]

        st.write(
            "**Matched Preferred Skills**"
        )

        if preferred_result["matched"]:
            st.write(
                preferred_result["matched"]
            )
        else:
            st.write(
                "No preferred skills matched."
            )

        st.write(
            "**Missing Preferred Skills**"
        )

        if preferred_result["missing"]:
            st.write(
                preferred_result["missing"]
            )
        else:
            st.write(
                "No preferred skills are missing."
            )

        st.write("### 🧠 Requirement Evidence")

        evidence_result = result["evidence"]

        if "requirements" in evidence_result:

            for requirement in evidence_result["requirements"]:

                skill = requirement.get(
                    "skill",
                    ""
                )

                level = requirement.get(
                    "evidence_level",
                    "none"
                )

                evidence = requirement.get(
                    "evidence",
                    ""
                )

                st.write(
                    f"**{skill} — "
                    f"{level.upper()}**"
                )

                if evidence:
                    st.caption(
                        f"Evidence: {evidence}"
                    )
                else:
                    st.caption(
                        "No evidence found."
                    )

        else:
            st.warning(
                "Could not evaluate candidate evidence."
            )

        st.write("### 📁 Project Relevance")

        project_result = result["projects"]

        if "projects" in project_result:

            st.write(
                f"**Overall Project Relevance: "
                f"{project_result.get(
                    'overall_relevance',
                    'unknown'
                ).upper()}**"
            )

            for project in project_result["projects"]:

                title = project.get(
                    "title",
                    "Unnamed Project"
                )

                relevance = project.get(
                    "relevance",
                    "none"
                )

                reason = project.get(
                    "reason",
                    ""
                )

                st.write(
                    f"**{title} — "
                    f"{relevance.upper()}**"
                )

                if reason:
                    st.caption(
                        f"Reason: {reason}"
                    )

        else:
            st.warning(
                "Could not evaluate project relevance."
            )


def show_results(candidate_profiles, match_results):

    show_candidate_profiles(
        candidate_profiles
    )

    show_screening_results(
        match_results
    )