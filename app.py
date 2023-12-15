"""How to run this application

Install pipenv (if you don't have it):
$ pip install pipenv

Install required packages with pipenv:

Installs all packages from Pipfile
$ pipenv install

Installs all packages specified in Pipfile.lock
$ pipenv sync

Installs all packages from requirements.txt
$ pipenv install -r ./requirements.txt

Run the application:
$ pipenv run app
or
$ pipenv run streamlit run app.py

Memo:
Activate the virtual environment
$ pipenv shell

Deactivate the virtual environment
$ exit

Delete the virtual environment
$ pipenv --rm

Check the path of the virtual environment
$ pipenv --venv

Show dependencies between packages
$ pipenv graph

Uninstalls all packages not specified in Pipfile.lock
$ pipenv clearn

Memo:
When the path of streamlit is not found, try the following VSCode setting:
-Go to "Python › Analysis: Extra Paths"
-Add the path of streamlit to the Extra Paths

How to find the path of streamlit:
yosuke@Yosuke-Hanaoka streamlit-dashboard % pipenv shell
Launching subshell in virtual environment...
 . /Users/yosuke/.local/share/virtualenvs/streamlit-dashboard-BOgLDBT6/bin/activate
yosuke@Yosuke-Hanaoka streamlit-dashboard %  . /Users/yosuke/.local/share/virtualenvs/streamlit-dashboard-BOgLDBT6/bin/activate
(streamlit-dashboard) yosuke@Yosuke-Hanaoka streamlit-dashboard % python 
Python 3.9.7 (default, Sep 19 2021, 20:48:10) 
[Clang 12.0.5 (clang-1205.0.22.9)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import streamlit
>>> print(streamlit.__file__)
/Users/yosuke/.local/share/virtualenvs/streamlit-dashboard-BOgLDBT6/lib/python3.9/site-packages/streamlit/__init__.py
>>> 

"""

import re
import streamlit as st
import pandas as pd
import altair as alt

st.title("Streamlit による売上データの分析例")

text = """本稿では [Kaggle](https://www.kaggle.com/aungpyaeap/supermarket-sales?select=supermarket_sales+-+Sheet1.csv) に登録されている売上原価の集計・可視化に取り組む。このデータセットにはある会社の支店 A、B、C の売上原価（三ヶ月分）が含まれている。需要予測等のデータ分析実務に近づけるため、支店間の売上原価を比較するダッシュボードの作成を目的とする。今回は [streamlit](https://qiita.com/keisuke-ota/items/a18f158389f1585a9aa0) を用いて、集計時のパラメータを GUI で操作できる interactive な図を作成する。

詳細は[Qiita](https://qiita.com/keisuke-ota/items/87448cdb9479d14240f4)にある。"""

st.markdown(text)

df = pd.read_csv("supermarket_sales - Sheet1.csv")

st.markdown("# データの形式")

st.table(df.head(10))

text = """# 前処理
売上の時系列変化を調べるために購入時期を表す列 week を追加し、売上の周期性を調べるために曜日列 day 時間帯列 time を追加する。
"""
st.markdown(text)

date = []
week = []
for c in df["Date"]:
    c = re.findall(r"\d+", c)
    m, d = int(c[0]), int(c[1])

    if m == 3:
        d += 31 + 28
    elif m == 2:
        d += 31

    d += -1

    if d % 7 == 6:
        tmp = "Mon"
    elif d % 7 == 0:
        tmp = "Tue"
    elif d % 7 == 1:
        tmp = "Wed"
    elif d % 7 == 2:
        tmp = "Thr"
    elif d % 7 == 3:
        tmp = "Fri"
    elif d % 7 == 4:
        tmp = "Sat"
    elif d % 7 == 5:
        tmp = "Sun"
    date.append(tmp)

    if d // 14 == 0:
        tmp = "1/1~1/14"
    elif d // 14 == 1:
        tmp = "1/15~1/28"
    elif d // 14 == 2:
        tmp = "1/29~2/11"
    elif d // 14 == 3:
        tmp = "2/12~2/25"
    elif d // 14 == 4:
        tmp = "2/26~3/11"
    elif d // 14 == 5:
        tmp = "3/12~3/25"
    elif d // 14 == 6:
        tmp = "3/26~3/31"
    week.append(tmp)

df["day"] = date
df["week"] = week

time = []
for c in df["Time"]:
    c = re.findall(r"\d+", c)
    t = c[0] + ":00~" + c[0] + ":59"
    time.append(t)

df["time"] = time

st.table(df.head(10))

st.markdown("# 支店別売上推移")

stacked_bar = (
    alt.Chart(df)
    .mark_bar(size=35)
    .encode(
        x=alt.X(
            "sum(cogs)",
            axis=alt.Axis(labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0),
        ),
        y=alt.Y(
            "week",
            axis=alt.Axis(labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0),
            sort=[
                "1/1~1/14",
                "1/15~1/28",
                "1/29~2/11",
                "2/12~2/25",
                "2/26~3/11",
                "3/12~3/25",
                "3/26~3/31",
            ],
        ),
        color="Product line",
        row=alt.Row("Branch", header=alt.Header(labelFontSize=20, titleFontSize=20)),
        tooltip=["week", "cogs"],
    )
    .properties(
        width=800,
        height=420,
    )
)

st.write(stacked_bar)

st.markdown("# 支店間の品目別売上比較")

cond = st.selectbox("層別条件を選ぶ", ("Gender", "Customer type", "Payment"))

boxplot = (
    alt.Chart(df)
    .mark_boxplot(
        size=50,
        ticks=alt.MarkConfig(width=20),
        median=alt.MarkConfig(color="black", size=50),
    )
    .encode(
        x=alt.X(
            "Branch",
            sort=alt.Sort(["A", "B", "C"]),
            axis=alt.Axis(labelFontSize=15, ticks=True, titleFontSize=18),
        ),
        y=alt.Y(
            "cogs",
            axis=alt.Axis(
                labelFontSize=15,
                ticks=True,
                titleFontSize=18,
                grid=False,
                domain=True,
                title="Firmicutes",
            ),
        ),
        column=alt.Column(
            "Product line", header=alt.Header(labelFontSize=20, titleFontSize=20)
        ),
        row=alt.Row(cond, header=alt.Header(labelFontSize=20, titleFontSize=20)),
    )
    .properties(
        width=300,
        height=300,
    )
)

st.write(boxplot)

st.markdown("# 詳細な売上原価の比較")

options = st.multiselect(
    "製造ラインを選択してください", list(set(df["Product line"])), list(set(df["Product line"]))
)

df = df[df["Product line"].isin(options)]


values = st.slider(
    "集計する cogs の最小値と最大値を決める",
    min(df["cogs"]),
    max(df["cogs"]),
    (min(df["cogs"]), max(df["cogs"])),
)

df = df[(values[0] <= df["cogs"]) & (values[1] >= df["cogs"])]

norm = st.radio("標準化するか？", ("No", "Yes"))

axis = st.radio("集計方法を選ぶ", ("week", "day", "time"))

if axis == "week":
    sort = [
        "1/1~1/14",
        "1/15~1/28",
        "1/29~2/11",
        "2/12~2/25",
        "2/26~3/11",
        "3/12~3/25",
        "3/26~3/31",
    ]
elif axis == "day":
    sort = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
elif axis == "time":
    sort = [
        "10:00~10:59",
        "11:00~11:59",
        "12:00~12:59",
        "13:00~13:59",
        "14:00~14:59",
        "14:00~14:59",
        "15:00~15:59",
        "16:00~16:59",
        "17:00~17:59",
        "18:00~18:59",
        "19:00~19:59",
        "20:00~20:59",
    ]

st.markdown("## 組成の可視化")

if norm == "Yes":
    stacked_bar = (
        alt.Chart(df)
        .mark_bar(size=35)
        .encode(
            x=alt.X(
                "sum(cogs)",
                axis=alt.Axis(
                    labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0
                ),
                stack="normalize",
                scale=alt.Scale(domain=[0, 1, 0]),
            ),
            y=alt.Y(
                axis,
                axis=alt.Axis(
                    labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0
                ),
                sort=sort,
            ),
            color="Product line",
            column=alt.Column(
                cond, header=alt.Header(labelFontSize=20, titleFontSize=20)
            ),
            row=alt.Row(
                "Branch", header=alt.Header(labelFontSize=20, titleFontSize=20)
            ),
            tooltip=[axis, "cogs"],
        )
        .properties(
            width=800,
            height=420,
        )
    )
else:
    stacked_bar = (
        alt.Chart(df)
        .mark_bar(size=35)
        .encode(
            x=alt.X(
                "sum(cogs)",
                axis=alt.Axis(
                    labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0
                ),
            ),
            y=alt.Y(
                axis,
                axis=alt.Axis(
                    labelFontSize=20, ticks=True, titleFontSize=20, labelAngle=0
                ),
                sort=sort,
            ),
            color="Product line",
            column=alt.Column(
                cond, header=alt.Header(labelFontSize=20, titleFontSize=20)
            ),
            row=alt.Row(
                "Branch", header=alt.Header(labelFontSize=20, titleFontSize=20)
            ),
            tooltip=[axis, "cogs"],
        )
        .properties(
            width=800,
            height=420,
        )
    )

st.write(stacked_bar)

st.markdown("## 分布の可視化")

line = (
    alt.Chart()
    .mark_point()
    .encode(
        x=alt.X(
            axis,
            axis=alt.Axis(labelFontSize=20, ticks=True, titleFontSize=20, grid=False),
            sort=sort,
        ),
        y=alt.Y(
            "cogs:Q",
            aggregate="mean",
            axis=alt.Axis(
                labelFontSize=20, ticks=True, titleFontSize=20, grid=False, domain=True
            ),
        ),
        color=alt.Color("Product line"),
    )
    .properties(width=400, height=400)
)

band = (
    alt.Chart()
    .mark_errorbar(extent="stderr", ticks=True, orient="vertical")
    .encode(
        x=alt.X(
            axis,
            axis=alt.Axis(labelFontSize=20, ticks=True, titleFontSize=20, grid=False),
            sort=sort,
        ),
        y=alt.Y(
            "cogs",
            type="quantitative",
            axis=alt.Axis(
                labelFontSize=20, ticks=True, titleFontSize=20, grid=False, domain=True
            ),
        ),
        color=alt.Color("Product line"),
    )
    .properties(width=400, height=400)
)

chart = alt.layer(line, band, data=df).facet(
    column=alt.Column(cond, header=alt.Header(labelFontSize=20, titleFontSize=20)),
    row=alt.Row("Branch", header=alt.Header(labelFontSize=20, titleFontSize=20)),
)

st.write(chart)
