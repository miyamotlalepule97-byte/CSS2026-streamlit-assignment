# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 19:23:24 2026

@author: miyam
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# --- Load the Excel file ---
df = pd.read_excel("Streamlit assignment.xlsx")

# --- App Title ---
st.title("The Physicochemical Properties Dashboard of The 3 Bimetallic Nanoparticles")

st.write("Explore the Taguchi L9 experimental design results interactively!")

# --- Sidebar for BMNP selection ---
bmnp_choice = st.sidebar.selectbox(
    "Choose a Bimetallic Nanoparticle (BMNP):",
    df["BMNPs"].unique()
)

# Filter data for the selected BMNP
filtered_df = df[df["BMNPs"] == bmnp_choice]

# --- Tabs for different views ---
tab1, tab2, tab3 = st.tabs(["📑 Data Table", "🕸 Radar Chart", "📊 Scatterplots"])

# --- Tab 1: Data Table ---
# --- Tab 1: Data Table ---
with tab1:
    st.subheader(f"Data for {bmnp_choice}")

    # Define background colors for each BMNP type
    def highlight_bmnp(row):
        if row["BMNPs"] == "Au-Pd":
            return ["background-color: lightgreen; color: black"] * len(row)
        elif row["BMNPs"] == "Au-Cu":
            return ["background-color: lightblue; color: black"] * len(row)
        elif row["BMNPs"] == "Au-Ni":
            return ["background-color: lightcoral; color: black"] * len(row)  # light orange tone
        else:
            return [""] * len(row)

    styled_df = filtered_df.style.apply(highlight_bmnp, axis=1)

    st.dataframe(styled_df)

# --- Tab 2: Radar Chart ---
with tab2:
    st.subheader("Radar Chart Comparison of BMNPs")

    properties = ["SPR average", "HD size average", "PDI average", "ZP average"]
    bmnp_means = df.groupby("BMNPs")[properties].mean()

    labels = properties
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Use a vibrant color palette
    colors = sns.color_palette("Set2", n_colors=len(bmnp_means))

    for (bmnp, row), color in zip(bmnp_means.iterrows(), colors):
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, label=bmnp, color=color, linewidth=2)
        ax.fill(angles, values, color=color, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Radar Chart of Average Physicochemical Properties")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    st.pyplot(fig)

# --- Tab 3: Scatterplots ---
with tab3:
    st.subheader("Interactive Scatterplot")

    x_axis = st.selectbox("Select X-axis property:", properties)
    y_axis = st.selectbox("Select Y-axis property:", properties)

    fig2, ax2 = plt.subplots()
    sns.scatterplot(
        data=filtered_df,
        x=x_axis,
        y=y_axis,
        hue="Exp No.",
        palette="Spectral",
        s=120,
        ax=ax2
    )
    ax2.set_title(f"{bmnp_choice}: {x_axis} vs {y_axis}")
    st.pyplot(fig2)

    st.info("💡 Tip: Switch BMNP types in the sidebar to compare different nanoparticles.")