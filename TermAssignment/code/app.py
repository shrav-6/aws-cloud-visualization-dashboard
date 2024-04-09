from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from views import supplier_layout, customer_layout, car_layout
import pandas as pd
import boto3
import os
from io import StringIO
from callbacks import register_callbacks


server = Flask(__name__)

app = dash.Dash(__name__, server=server)

#resource names given in cloudformation
topic_substring = os.environ["SNS_TOPIC_NAME"]
lambda_function_name = os.environ["LAMBDA_FUNCTION_NAME"]
bucket_name = os.environ["S3_BUCKET_NAME"]
csv_file_name = os.environ["S3_CSV_FILE_NAME"]

#set up my session and read from s3
session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ["AWS_SESSION_TOKEN"],
)
# Test it on a service (yours may be different)
s3 = session.resource('s3')

# Print out bucket names
bucket=s3.Bucket(bucket_name)
#for item in s3.buckets.all():
#    bucket=item

for obj in bucket.objects.all():
    key = obj.key
    if(key==csv_file_name):
        body = obj.get()['Body'].read().decode('utf-8')
        break
    
filtered_df = pd.read_csv(StringIO(body))

#comment this line before dockerizing
#filtered_df = pd.read_csv('dataset.csv')


available_years = filtered_df['Year'].unique()


# Define the layout of your Dash app
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Button('Supplier', id='btn-supplier', n_clicks=0, className='button'),
            html.Button('Customer', id='btn-customer', n_clicks=0, className='button'),
            html.Button('Car', id='btn-car', n_clicks=0, className='button'),
        ], className='button-container'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in available_years],
            value=available_years[0],  # Default value is the first year in the dataset
            clearable=False,
            style={'width': '25%', 'display': 'inline-block', 'float': 'left', 'margin-left': '20px'}
        ),
    ], className='navbar'),
    html.Div(id='page-content'),
    html.Div(id='alert-container')
])

# Callback to update page content based on button clicks
@app.callback(Output('page-content', 'children'),
              [Input('btn-supplier', 'n_clicks'),
               Input('btn-customer', 'n_clicks'),
               Input('btn-car', 'n_clicks')])
def display_page(btn_supplier, btn_customer, btn_car):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-supplier' in changed_id:
        return supplier_layout()
    elif 'btn-customer' in changed_id:
        return customer_layout()
    elif 'btn-car' in changed_id:
        return car_layout()
    else:
        return supplier_layout()  # Default to supplier stats layout

register_callbacks(app)

if __name__ == '__main__':
    server.run(host="0.0.0.0", debug=True, port=8000)
