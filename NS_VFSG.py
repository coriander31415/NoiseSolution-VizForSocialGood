import pandas as pd
import numpy as np
import base64
from math import pi
from bokeh.models import ColumnDataSource, HoverTool, Div, Spacer, Label
from bokeh.plotting import figure, output_notebook, show, output_file
from bokeh.layouts import row, column
from bokeh.transform import factor_cmap, cumsum
from scipy.stats import gaussian_kde
import urllib3
import requests
from io import BytesIO

output_notebook()
output_file("NS_VFSG.html")

palette = {
    "Primary": "#005a70", # blue-green
    "Secondary": "#800080", # vivid purple
    "Tertiary": "#F4A261", # orange
    "Neutral": "#9FC131", # lime green
    "Other": "#979797" # grey
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_excel = 'https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/data/NS_Data.xls'
response_excel = requests.get(url_excel, verify=False)

if response_excel.status_code == 200:
    try:
        df = pd.read_excel(BytesIO(response_excel.content), engine='xlrd')
        # print("File loaded successfully.")
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
else:
    print(f"Failed to fetch file: {response_excel.status_code}")

url_csv = 'https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/data/postcode_to_region_mapping.csv'
response_csv = requests.get(url_csv, verify=False)
postcode_mapping_df = pd.read_csv(BytesIO(response_csv.content))

df['Postcode_Prefix'] = df['Postcode'].str[:2]

df = pd.merge(df, postcode_mapping_df[['Postcode', 'Region']], 
              left_on='Postcode_Prefix', 
              right_on='Postcode', 
              how='left')

df['Region'] = df['Region'].fillna('Other')
df['Participant: Industry'] = df['Participant: Industry'].fillna('Other')
df['Gender'] = df['Gender'].fillna('Other')

df = df.drop(columns=['Postcode_Prefix'])

regions = df['Region'].unique().tolist()
industries = df['Participant: Industry'].unique().tolist()
genders = df['Gender'].unique().tolist()

df["Improvement Score"] = df["SWEMWBS End Score"] - df["SWEMWBS Start Score"]

url_logo_VFSG = "https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/VFSG_logo.png"
response_logo_VFSG = requests.get(url_logo_VFSG)
if response_logo_VFSG.status_code == 200:
    b64_logo_VFSG = base64.b64encode(response_logo_VFSG.content).decode('utf-8')
    # print("Logo loaded successfully.")
else:
    print(f"Failed to fetch the logo: {response_logo_VFSG.status_code}")

url_logo_NS = "https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/NS_logo.png"
response_logo_NS = requests.get(url_logo_NS)
if response_logo_NS.status_code == 200:
    b64_logo_NS = base64.b64encode(response_logo_NS.content).decode('utf-8')
    # print("Logo loaded successfully.")
else:
    print(f"Failed to fetch the logo: {response_logo_NS.status_code}")

logo_NS = Div(text=f"""<img src="data:image/png;base64,{b64_logo_NS}" width="300" style="padding: 10px;">""")
logo_VFSG = Div(text=f"""<img src="data:image/png;base64,{b64_logo_VFSG}" width="400" style="padding: 50px;">""")

spacer = Spacer(width_policy="max") 

logos_row = row(logo_NS, spacer, logo_VFSG, sizing_mode="stretch_width")

### Viz#1 Demographic Data Bar Charts ###

def chart_demographic_bar(x_column, title, max_label_length=20):
    if x_column == 'Gender':
        df['Gender'] = df['Gender'].apply(lambda x: x if x in ['Male', 'Female'] else 'Other')

    if x_column == 'SWEMWBS Start Age':
        age_bins = [0, 13, 20, 36, np.inf]
        age_labels = ['Children\n(0-12 y.o.)'
                      , 'Teenagers\n(13-19 y.o.)'
                      , 'Young Adults\n(20-35 y.o.)'
                      , 'Adults\n(>36 y.o.)']
        df['Age Group'] = pd.cut(df['SWEMWBS Start Age'], bins=age_bins, labels=age_labels, right=False)
        x_column = 'Age Group'
        
    if isinstance(df[x_column].dtype, pd.CategoricalDtype):
        df[x_column] = df[x_column].cat.add_categories('Other')

    df[x_column] = df[x_column].fillna('Other').astype(str)

    data = df[x_column].value_counts().reset_index()
    data.columns = [x_column, 'UIN']

    if 'Other' in data[x_column].values:
        other_row = data[data[x_column] == 'Other']
        data = data[data[x_column] != 'Other']
        data = pd.concat([data, other_row], ignore_index=True)

    categories = data[x_column].tolist()
    color_palette = [palette['Primary'], palette['Secondary'], palette['Tertiary'], palette['Neutral'], palette['Other']]

    source = ColumnDataSource(data)

    p = figure(x_range=categories, title=title, x_axis_label=x_column, y_axis_label="Participants",
               width=450, height=400, toolbar_location=None)

    # Apply custom palette to the bars
    p.vbar(x=x_column, top='UIN', width=0.7, source=source, 
           color=factor_cmap(x_column, palette=color_palette, factors=categories), alpha=0.8)

    hover = HoverTool()
    hover.tooltips = [("Participants", "@UIN")]
    p.add_tools(hover)

    return p


### Viz#2 Demographic Data Pie Charts ###

def get_dynamic_palette(num_categories):
    base_palette = [palette["Primary"], palette["Secondary"], palette["Tertiary"], palette["Neutral"]]
    
    dynamic_palette = base_palette[:num_categories] 
    if len(dynamic_palette) < num_categories:
        dynamic_palette += base_palette * (num_categories // len(base_palette)) 
    
    return dynamic_palette[:num_categories]

def chart_demographic_pie(x_column, title):
    if x_column == 'Gender':
        df['Gender'] = df['Gender'].apply(lambda x: x if x in ['Male', 'Female'] else 'Other')

    if x_column == 'SWEMWBS Start Age':
        age_bins = [0, 13, 20, 36, np.inf]
        age_labels = ['Children\n(0-12 y.o.)'
                      , 'Teenagers\n(13-19 y.o.)'
                      , 'Young Adults\n(20-35 y.o.)'
                      , 'Adults\n(>36 y.o.)']
        df['Age Group'] = pd.cut(df['SWEMWBS Start Age'], bins=age_bins, labels=age_labels, right=False)
        x_column = 'Age Group'

    if isinstance(df[x_column].dtype, pd.CategoricalDtype):
        df[x_column] = df[x_column].cat.add_categories('Other')

    df[x_column] = df[x_column].fillna('Other').astype(str)

    data = df[x_column].value_counts(normalize=True).reset_index()
    data.columns = [x_column, 'Percentage']
    data['Percentage'] *= 100  
    data['angle'] = data['Percentage'] / 100 * 2 * pi
    
    if 'Other' in data[x_column].values:
        dynamic_palette = get_dynamic_palette(len(data) - 1) + [palette['Other']]  
    else:
        dynamic_palette = get_dynamic_palette(len(data))
    
    data['color'] = dynamic_palette

    p = figure(height=350, title=title, toolbar_location=None, tools="hover",
               tooltips=[ ("%", "@Percentage{0.2f}")], x_range=(-0.5, 1))

    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field=x_column, source=ColumnDataSource(data))

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p

### Viz#3 Improvement Chart ###
    
def improvement_chart(df_clean):
    df_clean = df.dropna(subset=["Improvement Score", "Likes", "SWEMWBS Start Age"]).copy()

    conditions = [
        (df_clean["Improvement Score"] <= 0.00),
        (df_clean["Improvement Score"] > 0.00) & (df_clean["Improvement Score"] <= 2.00),
        (df_clean["Improvement Score"] > 2.00) & (df_clean["Improvement Score"] <= 4.66),
        (df_clean["Improvement Score"] > 4.66)
    ]

    df_clean["Improvement Level"] = np.select(conditions,
        ["No Improvement"
         , "Low Improvement"
         , "Moderate Improvement"
         , "High Improvement"],
        default="Unknown"
    )
    
    source = ColumnDataSource(df_clean)

    color_dict = {
        "No Improvement": "#D3D3D3",
        "Low Improvement": "#F4A261",
        "Moderate Improvement": "#9FC131",
        "High Improvement": "#800080",
    }

    p = figure(
        title="Impact of Noise Solution Initiatives on Participants’ Well-being",
        width=1280,
        height=600,
        x_axis_label="Improvement Score",
        y_axis_label="Age",
        background_fill_color="white",
    )

    for level, color in color_dict.items():
        level_source = ColumnDataSource(df_clean[df_clean["Improvement Level"] == level])
        p.scatter(
            x="Improvement Score",
            y="SWEMWBS Start Age",
            size='SWEMWBS Start Age', 
            color=color,
            source=level_source,
            line_color="black",
            fill_alpha=0.7,
            legend_label=level,
        )

    improvement_scores = df_clean["Improvement Score"].dropna().values
    kde = gaussian_kde(improvement_scores)
    x_range = np.linspace(min(improvement_scores), max(improvement_scores), 100)
    kde_values = kde(x_range) * len(improvement_scores)

    p.line(x_range, kde_values, line_width=1, color='black', legend_label="KDE", name="kde_line")

    hover = HoverTool(tooltips=[
        ("Age", "@{SWEMWBS Start Age}")
        , ("Likes", "@Likes")
        , ("Posts", "@Posts")
        , ("Comments", "@Comments")
        , ("Start Score", "@{SWEMWBS Start Score}")
        , ("End Score", "@{SWEMWBS End Score}")
        , ("Overall Impact", "@{Improvement Score}")
    ], renderers=[r for r in p.renderers if r.name != "kde_line"])
    p.add_tools(hover)

    return p

def render_dashboard():

    p_improvement_chart = improvement_chart(df)

    chart_demographic_bar_age = chart_demographic_bar('SWEMWBS Start Age', 'Participants\' Age', max_label_length=20)
    chart_demographic_bar_gender = chart_demographic_bar('Gender', 'Participants\'s Gender', max_label_length=20)
    chart_demographic_bar_industry = chart_demographic_bar('Participant: Industry', 'Referring Organisation Industry', max_label_length=20)

    chart_demographic_pie_age = chart_demographic_pie('SWEMWBS Start Age', 'Age Distribution')
    chart_demographic_pie_gender = chart_demographic_pie('Gender', 'Gender Distribution')
    chart_demographic_pie_industry = chart_demographic_pie('Participant: Industry', 'Referring Organisation Industry Distribution')

    chart_width = 370
    
    chart_demographic_bar_age.width = chart_width
    chart_demographic_bar_gender.width = chart_width
    chart_demographic_bar_industry.width = chart_width
    
    chart_demographic_pie_age.width = chart_width
    chart_demographic_pie_gender.width = chart_width
    chart_demographic_pie_industry.width = chart_width

    layout = column(
        logos_row,
        row(chart_demographic_bar_age, chart_demographic_bar_gender, chart_demographic_bar_industry, sizing_mode='scale_width'),
        row(chart_demographic_pie_age, chart_demographic_pie_gender, chart_demographic_pie_industry, sizing_mode='scale_width'),
        p_improvement_chart,
        sizing_mode="scale_width",
        width_policy="max"
    )

    show(layout)

render_dashboard()
