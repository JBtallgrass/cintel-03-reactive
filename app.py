import plotly.express as px
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly
import pandas as pd
import seaborn as sns
import palmerpenguins  # This package provides the Palmer Penguins dataset
from shiny import reactive  

# built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Page name
ui.page_opts(title="JB Penguins Data", fillable=True)

# sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of plotly bins", 30)

    # Creates slider input for Seaborn bins
    ui.input_slider(
        "seaborn_bin_slider",
        "Number of Bins",
        1,
        50,
        10,
    )

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "Species in Scatterplot",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

# Use ui.a() to add a hyperlink to the sidebar
ui.a(
    "JBTallgrass GitHub",
    href="https://github.com/JBtallgrass/cintel-02-data",
    target="_blank",
)

# Data table showing the penguin dataset Include 2 cards with a table and a grid
with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True):  # Full screen option
        ui.h3("Penguins Data Table")

        @render.data_frame
        def render_penguins_table():
            return filtered_data()

    with ui.card(full_screen=True):
        ui.h3("Penguins Data Grid")

        @render.data_frame
        def render_penguins_grid():
            return filtered_data()


# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr()

# Creates a Plotly Histogram showing all species
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h3("All Species Histogram-Plotly")

        @render_plotly
        def plotly_histogram():
            return px.histogram(filtered_data(), x="species")

    with ui.card(full_screen=True):
        ui.h3("All Species ScatterPlot-plotly")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
            filtered_data(),
            title="All Species ScatterPlot-plotly",
            x="body_mass_g",
            y="bill_length_mm",
            color="species",
            symbol="species",
        )
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df
