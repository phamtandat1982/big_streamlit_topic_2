import streamlit as st
import pandas as pd
import numpy as np 
from pandas_profiling import profile_report
import pandas_profiling as pp
import streamlit.components.v1 as components
import pydeck as pdk 
import altair as alt
import plotly.express as px
st.cache(persist=True)
#read data
data=pd.read_csv("OnlineRetail.csv",encoding='latin1')
data1=pd.read_csv('rfm_segments.csv')
#menu
menu = ['Introduction','Business Objective','Build project','Interaction 1','Interaction 2']
choice = st.sidebar.selectbox('Menu',menu)
if choice == 'Introduction':
    st.subheader('Topic 2: Phân khúc khách hàng')
    st.write('''
    ##### Họ và tên: PHẠM TẤN ĐẠT 
    ###### Lớp: LDS0_K271
    ''')
    st.subheader('Customer_segment')
    st.image('customer_segment.jpg')

elif choice == 'Business Objective':
    st.subheader('Business Objective')
    st.write('''
    ##### Vấn đề: Công ty X chủ yếu bán các sản phẩm là quà tặng dành cho những dịp đặc biệt. Nhiều khách hàng của công ty là khách hàng bán buôn. Công ty X mong muốn có thể bán được nhiều sản phẩm hơn cũng như giới thiệu sản phẩm đến đối tượng khách hàng, chăm sóc làm hài lòng khách hàng. Tìm ra giải pháp giúp cải thiện hiệu quả quảng bá, từ đó tăng doanh thu bán hàng, cải thiện mức độ hài lòng của khách hàng''')
    
    st.image('segmentation_approach.jpg')

    st.write('''
    ##### Mục tiêu của dự án: xây dựng hệ thống phân cụm khách hàng dựa trên các thông tin do công ty cung cấp từ đó có thể giúp công ty xác định các nhóm khách hàng khác nhau để có thể có chiến lược kinh doanh, chăm sóc khách hàng phù hợp.''')
elif choice == 'Build project':
    st.subheader ('Exploring dataset')
    report = pp.ProfileReport(data, title="Exploring dataset").to_html()
    components.html(report, height=1000, width=950,scrolling=True)
    st.subheader('Data preprocessing')
    mydata=pd.read_pickle('rfm_dp')
    st.dataframe(mydata)
    st.subheader('Rescaling the Attribute')
    mydata1=pd.read_pickle('rfm_scaled')
    st.dataframe(mydata1)
    st.subheader ('Build model')
    st.write('#### RFM model')
    st.image('RFM_SegmentsTopic2.png')
    st.image('scatter_plot_RFM.png')
    st.write('#### Kmean Cluster with Elbow method model')
    st.image('Kmean_SegmentsTopic2.png')
    st.image('scatter_plot_Kmean.png')
    st.write('#### Hierachy Clustering')
    st.image('HC_SegmentsTopic2.png')
    st.image('scatter_plot_HC.png')
    st.subheader ('Model selection')
    st.write('##### RFM model selected due to its simple, easy to understand, high accuracy')
elif choice == 'Interaction 1':
    st.markdown('Interactive Plot to Analysis Final RFM Segments')
    segments=data1['RFM_Level'].unique()
    #build app filters
    column = st.sidebar.multiselect('Select Segments', segments)
    recency = st.sidebar.number_input('Smaller Than Recency', 0, 373, 373)
    frequency= st.sidebar.number_input('Smaller Than Frequency', 0, 710, 710)
    monetary = st.sidebar.number_input('Smaller Than Monetary ', 0, 14389, 14389)
    data1 = data1[(data1['Recency']<=recency) & (data1['Frequency']<=frequency) & (data1['Monetary']<=monetary)]
    
#manage the multiple field filter
    if column == []:
        data1 = data1
    else:
        data1 = data1[data1['RFM_Level'].isin(column)]

    data1
    st.subheader('RFM Scatter Plot')
#scatter plot
    fig_scatter = px.scatter(data1, x="Recency", y="Frequency", color="RFM_Level",
                 size='Monetary')

    st.plotly_chart(fig_scatter)

#show distribution of values
#recency
    fig_r = px.histogram(data1, x="Recency", y="Customer_ID", marginal="box", # or violin, rug
                   hover_data=data1.columns, title='Recency Plot')
    st.plotly_chart(fig_r)

#frequency
    fig_f = px.histogram(data1, x="Frequency", y="Customer_ID", marginal="box", # or violin, rug
                   hover_data=data1.columns, title='Frequency Plot')
    st.plotly_chart(fig_f)

#monetary value
    fig_m = px.histogram(data1, x="Monetary", y="Customer_ID", marginal="box", # or violin, rug
                   hover_data=data1.columns, title='Monetary Value Plot')
    st.plotly_chart(fig_m)
elif choice == 'Interaction 2':
    #build app filters_Customer_ID_segment
    st.markdown('Finding information on which segment a Customer ID belong to')
    data1.round({'Customer_ID':0})
    cust_id_list= data1['Customer_ID'].unique()
    cus_id= st.sidebar.multiselect('Select customer ID', cust_id_list)
    #manage the multiple field filter
    if cus_id==[]:
        data1=data1
    else:
        data1=data1[data1['Customer_ID'].isin(cus_id)]
    
    data1

