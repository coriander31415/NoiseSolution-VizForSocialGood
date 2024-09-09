# Noise Solution Well-being Dashboard

This project is a volunteer-led initiative of [**Viz For Social Good**](https://www.vizforsocialgood.com/) to help [**Noise Solution**](https://www.noisesolution.org/) build an insightful dashboard. The aim is to visualise the impact of Noise Solution’s music mentoring program on participant well-being.

## About Viz For Social Good

[**Viz For Social Good**](https://www.vizforsocialgood.com/) connects data enthusiasts with mission-driven organizations globally. Nonprofit charities are working to change the world for the better, and Viz For Social Good enable these organizations to communicate their impact through data storytelling. 


## About Noise Solution

[**Noise Solution**](https://www.noisesolution.org/) is a social purpose organisation based in the East of England that engages youth at risk through informal music mentoring. By working with young people referred from alternative education, mental health, or social services, they aim to positively impact well-being and intrinsic motivation.

Noise Solution pairs young people with non-formal professional musicians, and together, they co-create music projects in the participant’s preferred genres. Throughout each session, the highlights — including audio, video, photos, and text — are captured and posted to a secure, cloud-based infrastructure, forming a private ‘digital story’. This story is shared with the participant's chosen community (such as family and professionals), who can like and comment on the content.

The goal of NoiseSolution is to bring data to life, demonstrating the impact on well-being in interactive and engaging ways. They use the [Shortened Edinburgh Mental Wellbeing Scale (SWEMWBS)](https://www.corc.uk.net/outcome-experience-measures/short-warwick-edinburgh-mental-wellbeing-scale-swemwbs/), developed by Warwick and Edinburgh Universities and the NHS, which allows comparison with national well-being datasets.

## Project Overview

The **Noise Solution Well-being Dashboard** uses the Bokeh library to present demographic and well-being improvement data. The dashboard provides an interactive way to visualise the impact of Noise Solution’s music mentoring programme on participants’ well-being.

The project currently includes:

- **Demographic Bar Charts**: Display participant distribution by age, gender, and referring organisation industry.
- **Demographic Pie Charts**: Provide a visual breakdown of participant demographics.
- **Impact Scatter Plot Chart**: Show changes in well-being scores impact, highlighting the effectiveness of Noise Solution’s programmes.

## Live Dashboard

You can view the live dashboard by clicking [here](<https://coriander31415.github.io/NoiseSolution-VizForSocialGood/NS_VFSG.html>).

Or you can download and view the dashboard [here](<https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/NS_VFSG.html>).

## Screenshots

### Main Dashboard View
![Main Dashboard View](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/screenshots/NS_screenshot_main_view.png)

### Demographic Bar Charts
![Demographic Bar Charts](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/screenshots/NS_screenshot_demographic_bar_charts.png)

### Demographic Pie Charts
![Demographic Pie Charts](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/screenshots/NS_screenshot_demographic_pie_charts.png)

### Impact of Noise Solution Initiatives on Participants' Well-being
![Impact Scatter Plot](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/assets/screenshots/NS_screenshot_impact_scatter_plot.png)

## Data Sources

- [NS_Data.xls](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/data/NS_Data.xls): Contains anonymised participant data, including demographics and well-being scores.
- [postcode_to_region_mapping.csv](https://raw.githubusercontent.com/coriander31415/NoiseSolution-VizForSocialGood/main/data/postcode_to_region_mapping.csv): Used to map participant postcodes to regions. *Note: This dataset will be used in future versions of the dashboard.*

## Key Features

- **Interactive Visualisation**: Built using Bokeh, the dashboard allows users to explore data with tooltips and dynamic layouts.
- **Custom Colour Palette**: A clear and accessible colour scheme ensures that the visualisations are easy to understand.
- **Future Plans**: Upcoming features include geo-mapping to show participant distribution across regions.

### Why Bokeh?

I chose **Bokeh** for this project due to its interactive features, which align well with my previous experience in **Tableau**, my favourite visualisation tool. This project allowed me to practice building interactive, custom dashboards using Python3, and Bokeh provided a great way to bring that to life.

## Running the Project

### Requirements

To run this project, ensure the following libraries are installed:

```bash
pip3 install pandas bokeh requests xlrd scipy
```

### Steps

### Run the project in the Jupyter Notebook or Google Colab 

1. Clone the repository:
    
    ```bash
    git clone https://github.com/coriander31415/NoiseSolution-VizForSocialGood.git
    ```
    
2. Open the project in Jupyter Notebook:
    
    ```bash
    jupyter notebook NS_VFSG.ipynb
    ```
    
3. Run the notebook to generate the dashboard.

### Or run the Project in VS Code:

1. Ensure you have the required libraries installed:
    
    ```bash
    pip3 install -r requirements.txt
    ```
    
2. Open the project in VS Code and run the Python file:
    
    ```bash
    python3 NS_VFSG.py
    ```
    
This will generate the HTML dashboard, which you can then open in your browser.

## Contributing

As this is a learning project, I welcome contributions, especially those focused on improving the visualisations or adding new features. Please feel free to create an issue or submit a pull request.