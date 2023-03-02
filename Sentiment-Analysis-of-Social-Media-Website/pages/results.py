import dash
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# TODO add the channel comparison pie chart and a dropdown that will allow the user to select among the three collections (amazon, google, and microsoft)

MONGO_HOST='mongodb+srv://mongoDBUser:OO8dZkHpFII3OX4v@cluster0.mg5dk.mongodb.net/?retryWrites=true&w=majority'
percentage_error = 0.1

dash.register_page(__name__)

# MongoDB connection
client = MongoClient(MONGO_HOST)
db = client["sentiment_analysis_result_db"]

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
layout = lambda: dbc.Container([

    dbc.Row(
        dbc.Col(
            [html.H1("Results of Sentiment Analysis",
                    className='text-center')],
            width=6
        ), justify='center', className='mt-5'
    ),

    # Dropdown Row
    dbc.Row(
        [dbc.Col(
            [html.H3("Select Collection")],
            width={'size': 6, 'offset': 1}
        ),
        dbc.Col(
            dcc.Dropdown(
                id="sentiment-analysis-engine",
                options = [
                            {
                            'label':'Google Layoffs',
                            'value':'google layoffs',
                            },
                            {
                            'label':'Amazon Layoffs',
                            'value':'amazon layoffs',
                            },
                            {
                            'label':'Microsoft Layoffs',
                            'value':'microsoft layoffs',
                            }
                        ],
                value='google layoffs',
                style={'color':'black'}
            ),
            width={'size': 4}
        )], className="mt-5"
    ),

    # Engine Comparison - All Channels
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='engine-all-graph')
        ), className="mt-5"
    ),

    # Engine Comparison - Twitter Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='engine-twitter-graph')
        ), className="mt-5"
    ),

    # Engine Comparison - Reddit Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='engine-reddit-graph')
        ), className="mt-5"
    ),

    # Engine Comparison - Tumblr Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='engine-tumblr-graph')
        ), className="mt-5"
    ),

    # Channel Comparison - All Engines
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='channel-all-graph')
        ), className="mt-5"
    ),

], fluid=True, className="mb-5")

@callback(
    Output('engine-all-graph', 'figure'),
    Output('engine-twitter-graph', 'figure'),
    Output('engine-reddit-graph', 'figure'),
    Output('engine-tumblr-graph', 'figure'),
    Output('channel-all-graph', 'figure'),
    Input('sentiment-analysis-engine', 'value'),
)

def populate_pie_chart(value):
    global collection
    collection = db[value]
    return query_engine_all_mongo_db(), query_engine_twitter_mongo_db(), query_engine_reddit_mongo_db(), query_engine_tumblr_mongo_db(), query_channel_all_mongo_db()

# ##################################################################################
# Query All SMP in MongoDB - Engine Comparison
def query_engine_all_mongo_db():
    result = collection.find({}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0})
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)

    MTA_GCNLA_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    MTA_IWNLU_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['IWNLU Sentiment Document Score']) <= percentage_error)
    IWNLU_GCNLA_filter = (abs(df_local['IWNLU Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    
    all_engines_sum =  (MTA_GCNLA_filter & MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    MTA_GCNLA_sum = (MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    MTA_IWNLU_sum = (~MTA_GCNLA_filter & MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    IWNLU_GCNLA_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    no_engines_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()

    data = {
        'Sentiment Analysis Engines': ['All Engines', 'MTA & GCNLA', 'MTA & IWNLU', 'IWNLU & GCNLA', 'No Engines'],
        'Number of Posts': [all_engines_sum, MTA_GCNLA_sum, MTA_IWNLU_sum, IWNLU_GCNLA_sum, no_engines_sum]
    }   
    df_final = pd.DataFrame(data=data)
    fig = px.pie(df_final, values='Number of Posts', names='Sentiment Analysis Engines', color_discrete_sequence=px.colors.sequential.RdBu, title='Comparison of Sentiment Analysis Engines for All Platforms')
    return fig

# ##################################################################################
# Query Twitter posts in MongoDB - Engine Comparison
def query_engine_twitter_mongo_db():
    result = collection.find({'social_media_platform': "b'Twitter'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0})
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)

    MTA_GCNLA_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    MTA_IWNLU_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['IWNLU Sentiment Document Score']) <= percentage_error)
    IWNLU_GCNLA_filter = (abs(df_local['IWNLU Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    
    all_engines_sum =  (MTA_GCNLA_filter & MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    MTA_GCNLA_sum = (MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    MTA_IWNLU_sum = (~MTA_GCNLA_filter & MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    IWNLU_GCNLA_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    no_engines_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()

    data = {
        'Sentiment Analysis Engines': ['All Engines', 'MTA & GCNLA', 'MTA & IWNLU', 'IWNLU & GCNLA', 'No Engines'],
        'Number of Posts': [all_engines_sum, MTA_GCNLA_sum, MTA_IWNLU_sum, IWNLU_GCNLA_sum, no_engines_sum]
    }   
    df_final = pd.DataFrame(data=data)
    fig = px.pie(df_final, values='Number of Posts', names='Sentiment Analysis Engines', color_discrete_sequence=px.colors.sequential.RdBu, title='Comparison of Sentiment Analysis Engines for Twitter')
    return fig

##################################################################################
# Query Reddit posts in MongoDB - Engine Comparison
def query_engine_reddit_mongo_db():
    result = collection.find({'social_media_platform': "b'Reddit'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0})
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True) 
    df_local = df_local.astype(float)

    MTA_GCNLA_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    MTA_IWNLU_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['IWNLU Sentiment Document Score']) <= percentage_error)
    IWNLU_GCNLA_filter = (abs(df_local['IWNLU Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)

    all_engines_sum =  (MTA_GCNLA_filter & MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    MTA_GCNLA_sum = (MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    MTA_IWNLU_sum = (~MTA_GCNLA_filter & MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    IWNLU_GCNLA_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    no_engines_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()

    data = {
        'Sentiment Analysis Engines': ['All Engines', 'MTA & GCNLA', 'MTA & IWNLU', 'IWNLU & GCNLA', 'No Engines'],
        'Number of Posts': [all_engines_sum, MTA_GCNLA_sum, MTA_IWNLU_sum, IWNLU_GCNLA_sum, no_engines_sum]
    }   
    df_final = pd.DataFrame(data=data)
    fig = px.pie(df_final, values='Number of Posts', names='Sentiment Analysis Engines', color_discrete_sequence=px.colors.sequential.RdBu, title='Comparison of Sentiment Analysis Engines for Reddit')
    return fig

##################################################################################
# Query Tumblr posts in MongoDB - Engine Comparison
def query_engine_tumblr_mongo_db():
    result = collection.find({'social_media_platform': "b'Tumblr'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0})
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    
    MTA_GCNLA_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    MTA_IWNLU_filter = (abs(df_local['MTA Sentiment Document Score'] - df_local['IWNLU Sentiment Document Score']) <= percentage_error)
    IWNLU_GCNLA_filter = (abs(df_local['IWNLU Sentiment Document Score'] - df_local['GCNLA Sentiment Document Score']) <= percentage_error)
    
    all_engines_sum =  (MTA_GCNLA_filter & MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    MTA_GCNLA_sum = (MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    MTA_IWNLU_sum = (~MTA_GCNLA_filter & MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()
    IWNLU_GCNLA_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & IWNLU_GCNLA_filter).sum()
    no_engines_sum = (~MTA_GCNLA_filter & ~MTA_IWNLU_filter & ~IWNLU_GCNLA_filter).sum()

    data = {
        'Sentiment Analysis Engines': ['All Engines', 'MTA & GCNLA', 'MTA & IWNLU', 'IWNLU & GCNLA', 'No Engines'],
        'Number of Posts': [all_engines_sum, MTA_GCNLA_sum, MTA_IWNLU_sum, IWNLU_GCNLA_sum, no_engines_sum]
    }   
    df_final = pd.DataFrame(data=data)
    fig = px.pie(df_final, values='Number of Posts', names='Sentiment Analysis Engines', color_discrete_sequence=px.colors.sequential.RdBu, title='Comparison of Sentiment Analysis Engines for Tumblr')
    return fig

##################################################################################
# Query All Engines - Channel Comparison
def query_channel_all_mongo_db():
    twitter_result = collection.find({'social_media_platform': "b'Twitter'"}, {'id': 1, '_id': 0})
    reddit_result = collection.find({'social_media_platform': "b'Reddit'"}, {'id': 1, '_id': 0})
    tumblr_result = collection.find({'social_media_platform': "b'Tumblr'"}, {'id': 1, '_id': 0})

    twitter_col = list(twitter_result)
    reddit_col = list(reddit_result)
    tumblr_col = list(tumblr_result)

    df_twitter = pd.DataFrame(twitter_col)
    df_twitter.dropna(inplace=True)
    df_reddit = pd.DataFrame(reddit_col)
    df_reddit.dropna(inplace=True)
    df_tumblr = pd.DataFrame(tumblr_col)
    df_tumblr.dropna(inplace=True)

    twitter_num_posts = df_twitter['id'].count()
    reddit_num_posts = df_reddit['id'].count()
    tumblr_num_posts = df_tumblr['id'].count()

    data = {
        'Social Media Platforms': ['Twitter', 'Reddit', 'Tumblr'],
        'Number of Posts': [twitter_num_posts, reddit_num_posts, tumblr_num_posts]
    }   
    df_final = pd.DataFrame(data=data)
    fig = px.pie(df_final, values='Number of Posts', names='Social Media Platforms', color_discrete_sequence=px.colors.sequential.RdBu, title='Number of Posts collected for each Social Media Platform')
    return fig
