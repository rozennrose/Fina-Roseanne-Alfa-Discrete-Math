import streamlit as st

st.title("Team Profile")

# Data anggota
members = [
    {
        "name": "Fina Nailatul Fadhilah",
        "program": "Actuarial Science",
        "image": "images/fina.jpg",
        "contribution": [
            "Designed and implemented the Streamlit user interface and multi-page navigation.",
            "Developed the 'Team Profile' page content and styling.",
            "Created the Graph Visualization page (showing the graph, node degrees, and adjacency matrix).",
            "Participated in documenting UI design and results in the final report."
        ]
    },
    {
        "name": "Roseanne Nugraheni",
        "program": "Actuarial Science",
        "image": "images/anne.jpg",
        "contribution": [
            "Implemented the shortest-route algorithm between cities and processed route data.",
            "Created the 'Full Province Graph' page for West Java.",
            "Conducted testing and debugging of graph algorithms and dataset accuracy.",
            "Documented technical methods (algorithms & data sources).",
            "Collected and prepared dataset of city connections for Java."
        ]
    },
    {
        "name": "Rega Alfarizi",
        "program": "Actuarial Science",
        "image": "images/alfa.jpg",
        "contribution": [
            "Led project planning, timeline, and coordination.",
            "Coordinated integration of the shortest-route algorithm into the app.",
            "Managed code repository, GitHub deployment, and Streamlit Cloud deployment.",
        ]
    }
]

# Layout 3 kolom
cols = st.columns(3)

# Generate content
for col, member in zip(cols, members):
    with col:
        # FIX: gunakan parameter baru
        st.image(member["image"], width="content")

        st.markdown(
            f"""
            **Name:** {member['name']}  
            **Program:** {member['program']}
            """
        )

        with st.expander("📌 Contribution"):
            for point in member["contribution"]:
                st.markdown(f"- {point}")
