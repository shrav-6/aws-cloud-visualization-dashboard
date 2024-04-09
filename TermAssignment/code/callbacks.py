# Import necessary modules and functions from Dash
from dash.dependencies import Input, Output
from dash import dcc, html

# Import other required libraries
import plotly.graph_objs as go
import plotly.express as px
import calendar
import json

# Import AWS SDK
import boto3

# Import colorlover for color scales
import colorlover as cl
# Define callbacks for updating graphs based on user input
def register_callbacks(app):
    @app.callback(
        Output('supplier-count', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_counts(selected_year):
        from app import filtered_df
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]
        num_suppliers = filtered_df_year['SupplierName'].nunique()

        return dcc.Markdown(f"**Suppliers:** {num_suppliers}")


    @app.callback(
        Output('car-maker-count', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_counts(selected_year):
        from app import filtered_df
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]
        num_carmakers = filtered_df_year['CarMaker'].nunique()

        return dcc.Markdown(f"**Carmakers:** {num_carmakers}")


    @app.callback(
        Output('customer-count', 'children'),
        Input('year-dropdown', 'value')
    )
    def update_counts(selected_year):
        from app import filtered_df
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]
        num_customers = filtered_df_year['CustomerID'].nunique()

        return dcc.Markdown(f"**Customers:** {num_customers}")

    # Define callback to update the graph
    @app.callback(
        [Output('top5carmakers-line-chart', 'figure'),
        Output('popular-colors','figure'),
        Output('carmodel-sales','figure')],
        Input('year-dropdown', 'value')
    )
    def update_car_graph(selected_year):
        from app import filtered_df
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]

        # Group the data by month and CarMaker, and sum the sales
        sales_by_month_carmaker = filtered_df_year.groupby(['Month', 'CarMaker'])['Sales'].sum().reset_index()

        # Sort the data by sales in descending order
        sorted_sales = sales_by_month_carmaker.sort_values(by='Sales', ascending=False)

        # Get the top 5 carmakers with the highest sales
        top5_carmakers = sorted_sales['CarMaker'].unique()[:5]

        # Filter the data for the top 5 carmakers
        top5_sales = sales_by_month_carmaker[sales_by_month_carmaker['CarMaker'].isin(top5_carmakers)]

        # Set the x-axis labels to the month names
        top5_sales['Month'] = top5_sales['Month'].apply(lambda x: calendar.month_abbr[x])

        # Create line chart using Plotly Express
        fig = px.line(top5_sales, x='Month', y='Sales', color='CarMaker',
                    title=f'Sales of Top 5 Carmakers in {selected_year}')
        fig.update_layout(xaxis_title='Month', yaxis_title='Sales')
        #print(fig)
        
        
        car_color_counts = filtered_df_year['CarColor'].value_counts().head(10)
        if selected_year == 2018:
            colors = cl.interp(['rgb(0,128,128)', 'rgb(220,240,240)'], 10)
        else:
            colors = cl.interp(['rgb(0,0,128)', 'rgb(135,206,250)'], 10)
        # Predefined colors for the pie chart, add more as needed
        trace = go.Pie(labels=car_color_counts.index, values=car_color_counts.values,
                    marker=dict(colors=colors))  # Using the 'Viridis' color scale for gradient colors
        layout = go.Layout(title=f'Top 10 Most Popular Car Colors for {selected_year}', showlegend=True)

        fig_colors = go.Figure(data=[trace], layout=layout)
        
        carmodel_sales_year = filtered_df_year.groupby('CarModel')['Sales'].sum().reset_index()

        # Sort the results in descending order of Sales
        carmodel_sales_year = carmodel_sales_year.sort_values(by='Sales', ascending=False).head(10)
        
        # Create a bar chart using Plotly# Create a bar chart using Plotly with gradient pink color
        fig_car = go.Figure(data=[go.Bar(
            x=carmodel_sales_year['CarModel'], 
            y=carmodel_sales_year['Sales'],
            marker=dict(color=carmodel_sales_year['Sales'],  # Use Sales values for coloring
                        colorscale='RdBu',  # Choose a color scale (you can adjust this)
                        colorbar=dict(title='Sales'))  # Add a color bar with title
        )])
        fig_car.update_layout(
            title=f'Top 10 Best Selling Car Models for {selected_year}',
            xaxis_title='Car Model',
            yaxis_title='Sales',
            xaxis_tickangle=-45  # Rotate x-axis labels for better readability
        )

        return fig, fig_colors, fig_car

    # Define callback to update the graph
    @app.callback(
        [Output('jobtitle-carprice-graph', 'figure'),
        Output('gender-analysis','figure'),
        Output('shipments-analysis','figure')],
        [Input('year-dropdown', 'value')]
    )
    def update_customer_graph(selected_year):
        from app import filtered_df
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]
        # Create bar chart using Plotly Express
        jobtitle_avg_carprice = filtered_df_year.groupby('JobTitle')['Sales'].mean().reset_index()

        # Sort the results in descending order of mean CarPrice
        jobtitle_avg_carprice = jobtitle_avg_carprice.sort_values(by='Sales', ascending=False).head(10)

        color_palette = px.colors.qualitative.Plotly
        job_fig = px.bar(jobtitle_avg_carprice, x='JobTitle', y='Sales', labels={'JobTitle': 'Job Title', 'Sales': 'Average Car Price'},color='JobTitle', color_discrete_sequence=color_palette)
        job_fig.update_layout(title='Jobs of customers who bought the most expensive cars', xaxis_tickangle=-40, bargap=0.2)
        job_fig.update_yaxes(range=[800000, 1000000])
        
        
        gender_counts = filtered_df_year['Gender'].value_counts()

        # Calculate percentage
        gender_percentage = gender_counts / gender_counts.sum() * 100

        # Create Doughnut chart data
        data = go.Pie(labels=gender_counts.index, values=gender_counts, hole=0.4,marker=dict(colors=['rgb(255,192,203)','rgb(173,216,230)']))

        # Create layout
        layout = go.Layout(title='Gender Distribution in Car Sales')
        gender_fig = {
            'data': [data],
            'layout': layout
        }
        
        
        shipments_by_month = filtered_df_year.groupby('Month')['Quantity'].sum().reset_index()

        # Set the x-axis labels to the month names
        shipments_by_month['Month'] = shipments_by_month['Month'].apply(lambda x: calendar.month_abbr[x])

        # Create traces for line chart
        trace = go.Scatter(x=shipments_by_month['Month'], y=shipments_by_month['Quantity'], mode='lines+markers')
        
        # Define layout for the chart
        layout = go.Layout(title=f'Shipments by Month for {selected_year}',
                        xaxis={'title': 'Month'},
                        yaxis={'title': 'Quantity Shipped'},
                        hovermode='closest')
        line_fig = {'data': [trace], 'layout': layout}
        
        return job_fig, gender_fig, line_fig

    # Define callbacks for updating graphs based on user input
    @app.callback(
        [Output('sales-bar-chart', 'figure'),
        Output('choropleth-map', 'figure'),
        Output('alert-container', 'children'),
        Output('suppliers-line-chart', 'figure')],
        [Input('year-dropdown', 'value'),
        Input('btn-notify', 'n_clicks')]
    )
    def update_supplier_graphs(selected_year, n_clicks):
        from app import filtered_df, lambda_function_name, topic_substring
        print('inside callbacks')
        filtered_df_year = filtered_df[filtered_df['Year'] == selected_year]
        sorted_df = filtered_df_year.sort_values(by='Sales', ascending=False).head(10)[['SupplierName','Sales']][::-1]
        #colorscales = px.colors.named_colorscales()

        color_scale_teal = [[0.0, 'rgb(220,240,220)'],[1.0, 'rgb(0,128,128)']]    

        # Update bar chart
        sales_bar_chart_fig = {
            'data': [{'x': sorted_df['SupplierName'], 'y': sorted_df['Sales'], 'type': 'bar','marker': {
                'color': sorted_df['Sales'],  # Use Sales values for coloring
                'colorscale': color_scale_teal,  # Set the color scale
                'colorbar': {'title': 'Sales'}  # Add a color bar with title
            }}],
            'layout': {
                'title': {'text': f'Top Suppliers Based on Sales for the year {selected_year}'},
                'xaxis': {'title': 'Supplier Name', 'tickangle': 45},
                'yaxis': {'title': 'Sales', 'range': [sorted_df['Sales'].min()-100, sorted_df['Sales'].max()+100]},
                'bargap': 0.1,
                'height': 500
            }
        }
        
        # Update choropleth map
        sales_by_state = filtered_df_year[['State','Sales']]
        choropleth_map_fig = px.choropleth(sales_by_state,
                                        locations='State',
                                        locationmode='USA-states',
                                        color='Sales',
                                        scope='usa',
                                        color_continuous_scale='OrRd',
                                        title=f'Sales Intensity by State in the USA in {selected_year}')
        choropleth_map_fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

        message = None
        if n_clicks is not None and n_clicks > 0:
            message = generate_report(filtered_df_year,selected_year)
            print(message)
            send_sns_email_lambda(lambda_function_name,message,topic_substring)
            html.Script(f'alert("{message}")')
            
        # Group the data by 'SupplierName' and 'Month', and sum the 'Sales'
        sales_by_supplier_month = filtered_df_year.groupby(['SupplierName', 'Month'])['Sales'].sum().reset_index()

        # Sort the data by 'Sales' in descending order
        sorted_sales = sales_by_supplier_month.sort_values(by='Sales', ascending=False)

        # Get the top 5 selling suppliers
        top5_suppliers = sorted_sales['SupplierName'].unique()[:5]

        # Filter the data for the top 5 suppliers
        top5_sales = sales_by_supplier_month[sales_by_supplier_month['SupplierName'].isin(top5_suppliers)]

        # Set the x-axis labels to the month names
        top5_sales['Month'] = top5_sales['Month'].apply(lambda x: calendar.month_abbr[x])
        
        # Create the line chart using Plotly graph objects
        line_chart = go.Figure()
        for supplier in top5_suppliers:
            data = top5_sales[top5_sales['SupplierName'] == supplier]
            line_chart.add_trace(go.Scatter(x=data['Month'], y=data['Sales'], mode='lines+markers', name=supplier))
        
        # Update layout of the chart
        line_chart.update_layout(
            title='Sales of Top 5 Suppliers Over the Months',
            xaxis_title='Month',
            yaxis_title='Sales',
            xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
            legend_title='Supplier Name'
        )
        
        return sales_bar_chart_fig, choropleth_map_fig, message, line_chart

def generate_report(filtered_df,selected_year):
    message = "This is the weekly progress report"
    num_suppliers = filtered_df['SupplierName'].nunique()
    num_carmakers = filtered_df['CarMaker'].nunique()

    supplier_sales = filtered_df.groupby('SupplierName')['Sales'].sum().reset_index()
    sorted_supplier_sales = supplier_sales.sort_values(by='Sales', ascending=False)
    top5_suppliers = sorted_supplier_sales['SupplierName'].unique()[:5]
    carmaker_sales = filtered_df.groupby('CarMaker')['Sales'].sum().reset_index()
    sorted_carmaker_sales = carmaker_sales.sort_values(by='Sales', ascending=False)
    top5_carmakers = sorted_carmaker_sales['CarMaker'].unique()[:5]
    model_sales = filtered_df.groupby('CarModel')['Sales'].sum().reset_index()
    sorted_model_sales = model_sales.sort_values(by='Sales', ascending=False)
    top5_models = sorted_model_sales['CarModel'].unique()[:5]
    state_sales = filtered_df.groupby('State')['Sales'].sum().reset_index()
    sorted_state_sales = state_sales.sort_values(by='Sales', ascending=False)

    # Get the top 5 selling states
    top5_states = sorted_state_sales['State'].unique()[:5]
    overall_sales = filtered_df['Sales'].sum()

    # Generate the text
    message = f"""
    Year: {selected_year}

    Suppliers:
    - Total: {num_suppliers}
    - Top 5 by Sales:
        {', '.join([f'{supplier} ({sales})' for supplier, sales in zip(top5_suppliers, sorted_supplier_sales['Sales'][:5])])}

    Carmakers:
    - Total: {num_carmakers}
    - Top 5 by Sales:
        {', '.join([f'{carmaker} ({sales})' for carmaker, sales in zip(top5_carmakers, sorted_carmaker_sales['Sales'][:5])])}

    Car Models:
    - Top 5 by Sales:
        {', '.join([f'{model} ({sales})' for model, sales in zip(top5_models, sorted_model_sales['Sales'][:5])])}

    States:
    - Top 5 by Sales:
        {', '.join([f'{state} ({sales})' for state, sales in zip(top5_states, sorted_state_sales['Sales'][:5])])}

    Overall Revenue for {selected_year}:
    - {overall_sales}
    """
    return message

def send_sns_email_lambda(function_name,message,substring):
    lambda_client = boto3.client('lambda',region_name='us-east-1')
    payload = {
    "message": message,
    "substring": substring
    }
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Change as needed (e.g., 'Event' for asynchronous invocation)
        Payload=json.dumps(payload)
    )
    print(json.loads(json.loads(response['Payload'].read().decode('utf-8'))['body']))
