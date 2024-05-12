
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# 데이터 로드 함수
@st.cache_data
def load_data():
    orders = pd.read_csv('./datas/List of Orders.csv')
    details = pd.read_csv('./datas/Order Details.csv')
    ## 결측치는 Inner Join을 시행하면 자동으로 사라짐
    data = pd.merge(orders,details,on='Order ID',how='inner')

    return data


# 전처리 함수
def pre_process():
    data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d-%m-%Y')
    data['year'] = data['Order Date'].dt.year
    data['month'] = data['Order Date'].dt.month
    data['date_ym'] = data['Order Date'].astype('str').str.slice(0,7)

    return data

# 라인차트 만드는 함수
def make_line_chart(data,x,y,title):
    df_temp = data.groupby(x).agg({y:'sum'}).reset_index()
    fig = px.line(df_temp, x=x, y=y, title=title)
    fig.show()

    return df_temp, fig

# 막대차트(바차트) 그리는 함수
def make_bar_graph(data,x,y,color=None):
    if color is not None:
        index = [x, color]
    else:
        index = x
    df_temp = data.pivot_table(index=index,values=y,aggfunc='sum').reset_index()
    fig = px.bar(df_temp,x=x,y=y,color=color)
    fig.show()
    return fig

# 히트맵 그리는 함수
def make_heatmap(data,z,title=None):
    df_temp = data.groupby(['State','Sub-Category'])[['Quantity','Amount','Profit']].sum().reset_index()
    fig = px.density_heatmap(df_temp, x='State',y='Sub-Category',z=z,title=title)
    fig.show()

    return fig

if __name__ == '__main__':

    st.title('E-Commerce 데이터 분석 및 Streamlit을 통한 웹 대시보드 작성')
    st.write('streamlit을 이용한 이커머스 대시보드 만들기')

    # 데이터 로드
    data = load_data()
    # 데이터 전처리
    data = pre_process()

st.subheader('월별 판매량 분석')

with st.form('form', clear_on_submit=True):
    col1, col2 = st.columns(2)

    submitted1 = col1.form_submit_button('판매량 그래프')
    submitted2 = col2.form_submit_button('매출액 그래프')

    if submitted1:
        df1, fig1 = make_line_chart(data, 'date_ym','Quantity','Sales Quantity by month(월별 판매량 그래프)')
        st.dataframe(df1.T)
        st.plotly_chart(fig1, theme='streamlit',use_container_width = True)

    elif submitted2:
        df2, fig2 = make_line_chart(data, 'date_ym','Amount','Sales Amount by month(월별 매출액 그래프)')
        st.dataframe(df2.T)
        st.plotly_chart(fig2, theme='streamlit',use_container_width = True)

st.subheader('품목별(Sub-Category) 판매량')
col1, col2 = st.columns(2)
with col1:
    col1.subheader('카테고리별 판매량')
    fig3 = make_bar_graph(data,'Category','Quantity')
    st.plotly_chart(fig3, theme='streamlit',use_container_width = True)

with col2:
    col2.subheader('월별 카테고리별 누적 판매량')
    fig4 = make_bar_graph(data,'date_ym','Quantity','Category')
    st.plotly_chart(fig4, theme='streamlit',use_container_width = True)

st.subheader('지역별 주력 판매상품')

tab1, tab2 = st.tabs(['Quantity heat map by region','Amount heat map by region'])
with tab1:
    fig5 = make_heatmap(data,'Quantity','Quantity heat map by region')
    st.plotly_chart(fig5,theme='streamlit',use_container_width=True)

with tab2:
    fig6 = make_heatmap(data,'Amount','Amount heat map by region')
    st.plotly_chart(fig6, theme='streamlit',use_container_width=True)
