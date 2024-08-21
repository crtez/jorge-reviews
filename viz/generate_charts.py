import plotly.express as px
import pandas as pd
import json
from jinja2 import Environment, FileSystemLoader
import webbrowser

env = Environment(
    loader=FileSystemLoader(
        "templates/template.html"
    )
)

# Load data from a JSON file encoded in UTF-8
with open('final_for_real.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Convert ratingValue to a numeric type (handling comma as decimal point)
df['ratingValue'] = df['ratingValue'].str.replace(',', '.').astype(float)

# Extract the year from the datetime field
df['year'] = pd.to_datetime(df['datetime']).dt.year

all_charts = []
# Group the DataFrame by year and create a scatter plot for each year
for year, group in df.groupby('year'):
    # Calculate the average rating for the year
    avg_rating = group['ratingValue'].mean()

    fig = px.scatter(
        group,
        x='review_name',
        y='ratingValue',
        hover_data={
            'datetime': True,
            'headline': True,
            'href': True,
            'imdb': True
        },
        labels={'review_name': 'Review Name', 'ratingValue': 'Rating Value'},
        title=f'Scatter Plot of Review Ratings for {year}'
    )
    # Rotate x-axis labels by 45 degrees
    fig.update_xaxes(tickangle=45)

    # Add a horizontal line at the average rating
    fig.add_hline(y=avg_rating, line_dash="dash", line_color="red",
                  annotation_text=f"Avg: {avg_rating:.2f}",
                  annotation_position="top right")

    all_charts.append(fig)

env = Environment(
    loader=FileSystemLoader(
        'templates'
    )
)
template = env.get_template('template.html')
html = template.render({
    'table1': all_charts[0].to_html(),
    'table2': all_charts[1].to_html(),
    'table3': all_charts[2].to_html(),
    'table4': all_charts[3].to_html(),
    'table5': all_charts[4].to_html(),
    'table6': all_charts[5].to_html(),
    'table7': all_charts[6].to_html(),
    'table8': all_charts[7].to_html(),
    'table9': all_charts[8].to_html(),
    'table10': all_charts[9].to_html(),
    'table11': all_charts[10].to_html(),
    'table12': all_charts[11].to_html(),
    'table13': all_charts[12].to_html(),
    'table14': all_charts[13].to_html(),
    'table15': all_charts[14].to_html(),
    'table16': all_charts[15].to_html(),
    'table17': all_charts[16].to_html(),
    'table18': all_charts[17].to_html(),
    'table19': all_charts[18].to_html(),
    'table20': all_charts[19].to_html(),
})

# Define the output file path
output_file = 'out_filepath.html'

# Write the HTML to the file
with open(output_file, 'w', encoding="utf-8") as f:
    f.write(html)

# Open the HTML file in the default web browser
webbrowser.open(output_file)
