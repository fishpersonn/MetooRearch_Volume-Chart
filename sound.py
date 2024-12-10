# streamlit run sound.py
import streamlit as st
import pandas as pd
from scipy.signal import find_peaks
import plotly.graph_objects as go

st.set_page_config(page_title="聲量分析", layout="wide")
st.title("社群聲量分析")

uploaded_file = st.file_uploader("選擇檔案", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        daily_volume = df.groupby('date').agg({
            'text': list,  # 改為 text
            'date': 'size'
        }).rename(columns={'date': 'volume'}).reset_index()
        
        daily_volume['date'] = pd.to_datetime(daily_volume['date'])
        daily_volume = daily_volume.sort_values('date')
        
        # 找出峰值
        peaks, _ = find_peaks(daily_volume['volume'].values, distance=5)
        
        # 使用 Plotly 繪製圖表
        fig = go.Figure()
        
        # 添加主線
        fig.add_trace(go.Scatter(
            x=daily_volume['date'],
            y=daily_volume['volume'],
            mode='lines',
            name='聲量',
            line=dict(color='red', width=2)
        ))
        
        # 添加峰值點
        fig.add_trace(go.Scatter(
            x=daily_volume['date'].iloc[peaks],
            y=daily_volume['volume'].iloc[peaks],
            mode='markers',
            name='峰值',
            marker=dict(color='red', size=10)
        ))
        
        # 設定圖表樣式
        fig.update_layout(
            title='聲量走勢圖',
            xaxis_title='日期',
            yaxis_title='聲量',
            hovermode='x unified',
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig, use_container_width=True)

         # 顯示前十大聲量資料
        st.subheader("前十大聲量日期")
        top_10 = daily_volume.nlargest(10, 'volume')
        for _, row in top_10.iterrows():
            st.markdown(f"**日期：** {row['date'].strftime('%Y-%m-%d')} | **聲量：** {row['volume']}")
        
        
    except Exception as e:
        st.error(f"錯誤: {str(e)}")