from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    # 读取数据
    data = pd.read_csv('data/A_replaced.csv', encoding='gb2312')  # 替换为你的数据文件路径

    # 按国家和年份进行分组，并计算每个组的旅游人数总和
    grouped_data = data.groupby(['旅游到达国家', '年份'])['国际旅游人数'].sum().reset_index()

    # 创建地图
    fig = px.choropleth(grouped_data,
                        locations="旅游到达国家",
                        locationmode="country names",
                        color="国际旅游人数",
                        hover_name="旅游到达国家",
                        animation_frame="年份",  # 按年份添加动画效果
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection="natural earth")

    fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")
    fig.update_layout(autosize=False, width=1200, height=800, title="International Tourism by Country and Year")

    # 获取地图的 HTML 内容
    map_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
