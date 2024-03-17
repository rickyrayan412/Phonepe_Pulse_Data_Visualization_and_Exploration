import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#dataframe creation
#sql connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "ricky412",
                        database = "phonepe_data",
                        port = "5432")
cursor = mydb.cursor()

#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table1 = cursor.fetchall()
Aggre_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table2 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table3 = cursor.fetchall()
Aggre_user = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table4 = cursor.fetchall()
Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table5 = cursor.fetchall()
Map_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table6 = cursor.fetchall()
Map_user = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table7 = cursor.fetchall()
Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table8 = cursor.fetchall()
Top_transaction = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table9 = cursor.fetchall()
Top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

def Transaction_amount_count_Y(df,year):
    tacy= df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)
    
    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount=px.funnel(tacyg, x="States", y="Transaction_amount", title=f"{year} Transaction Amount",
                         color_discrete_sequence=px.colors.sequential.Bluered, height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.funnel(tacyg, x="States", y="Transaction_count", title=f"{year} Transaction Count",
                         color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1=json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()
        
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_amount", color_continuous_scale="hsv",
                                 range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} Transaction Amount",
                                 fitbounds= "locations",height=600 ,width=600)
        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_count", color_continuous_scale="hsv_r",
                                 range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} Transaction Count",
                                 fitbounds= "locations",height=600 ,width=600)
        fig_india_2.update_geos(visible =False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df,quarter):
        tacy=df[df["Quarter"] == quarter]
        tacy.reset_index(drop=True, inplace=True)
        
        tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
        tacyg.reset_index(inplace=True)

        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} Year,  {quarter} Quarter Transaction Amount",
                             color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
            st.plotly_chart(fig_amount)
        with col2:
            fig_count=px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} Year,  {quarter} Quarter Transaction Count",
                             color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
            st.plotly_chart(fig_count)
        
        col1,col2=st.columns(2)
        with col1:
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1=json.loads(response.content)
            states_name = []
            for feature in data1["features"]:
                states_name.append(feature["properties"]["ST_NM"])
                
            states_name.sort()
            
            fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                     color="Transaction_amount", color_continuous_scale="hot_r",
                                     range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                     hover_name= "States",title = f"{tacy['Years'].min()} Year,  {quarter} Quarter Transaction Amount",
                                     fitbounds= "locations",height=600 ,width=600)
            fig_india_1.update_geos(visible =False)
            st.plotly_chart(fig_india_1)
        with col2:
            fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                     color="Transaction_count", color_continuous_scale="rainbow_r",
                                     range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                     hover_name= "States",title = f"{tacy['Years'].min()} Year,  {quarter} Quarter Transaction Count",
                                     fitbounds= "locations",height=600 ,width=600)
            fig_india_2.update_geos(visible =False)
            st.plotly_chart(fig_india_2)

        return tacy

def Aggre_Tran_Transaction_type(df, state):
    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)
    
    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount",
                        width = 600, title=f"Transaction Amount for {state}", hole= 0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count",
                        width = 600, title=f"Transaction Count for {state}", hole= 0.5)
        st.plotly_chart(fig_pie_2)

def Aggre_user_plot_1(df, year):
    aguy=df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)
    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year}  Brands And Transaction Count",
                       width=1000, color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

def Aggre_user_plot_2(df, quarter):
    aguyq=df[df["Quarter"]== quarter ]
    aguyq.reset_index(drop= True, inplace= True)
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} Quarter, Brands And Transaction Count",
                           width=1000, color_discrete_sequence=px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)
    
    fig_line_1= px.line(auyqs, x="Brands", y="Transaction_count", hover_data=["Percentage"],
                        title= f"Brands, Transaction Count and Percentage for  {state}", width= 1000, markers=True)
    st.plotly_chart(fig_line_1)

def Map_insur_District(df, state):
    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)
    
    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x= "Transaction_amount", y= "Districts",
                                  width=600, height=800, title= f"Transaction Amount for Districts in {state}",
                                  color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg, x= "Transaction_count", y= "Districts",
                                  width=600, height=800, title= f"Transaction Count for Districts in {state}",
                                  color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

#Map_user_plot_1
def map_user_plot_1(df, year):
    muy=df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)
    
    muyg = pd.DataFrame(muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum())
    muyg.reset_index(inplace = True)
    
    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                    width=1000,height=800,title= f"AppOpens and Registered User for {year}", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

#Map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()} Year, {quarter} Quarter Registered User and AppOpens",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

#Map_user_plot_3
def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"Registered User from {state} ",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"AppOpens from {state}",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_2)

#top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy=df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1=px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= ["Pincodes"],
                                        width= 600, height=650, title= f"Transaction Amount for {state}",
                                      color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= ["Pincodes"],
                                        width= 600, height=650, title= f"Transaction Count for {state}",
                                      color_discrete_sequence= px.colors.sequential.Agsunset)
        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "RegisteredUser",hover_data=["Pincodes"],
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

#top_chart

def ques1():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.pie(sa2, values='AppOpens', names='States', title="Map_user's Top 10 States With AppOpens",width=800, height=600, hole=0.30)
    return st.plotly_chart(fig_sa)

def ques2():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa = px.line(sa2, x="States", y="AppOpens", title="Map_user's Least 10 States With AppOpens",
                     color_discrete_sequence=px.colors.sequential.dense_r, markers =  True)
    return st.plotly_chart(fig_sa)

def ques3():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Aggregation_user's Top Mobile Brands for Transaction_count", hole=0.30)
    return st.plotly_chart(fig_brands)
    
def ques4():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "States with Largest Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques5():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "States with Least Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques6():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.line(dt2, x= "Districts", y= "Transaction_amount", title= "Top 50 Districts with Largest Transaction Amount",
                color_discrete_sequence= px.colors.sequential.Mint_r, markers=True, width=800, height=600)
    return st.plotly_chart(fig_dt)

def ques7():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="Top 10 Disticts of Highest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Emrld_r, hole=0.25)
    return st.plotly_chart(fig_htd)

def ques8():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="Top 10 Disticts of Lowest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Greens_r,hole=0.25)
    return st.plotly_chart(fig_htd)

def ques9():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "States with Highest Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques10():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "States with Lowest Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)



#streamlit part
st.set_page_config(layout= "wide")


# Display the main header: Using Markdown with HTML for center alignment
st.markdown("<h1 style='text-align: center; color: #6F36AD;'>Phonepe Pulse Data Visualization and Exploration</h1>", unsafe_allow_html=True)
st.markdown("##")

select = option_menu(
    menu_title = None,
    options = ["Home","Data Exploration","Top Charts"],
    icons =["house","bar-chart","toggles"],
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "#F7bCF6","size":"cover", "width": "200"},
        "icon": {"color": "black", "font-size": "25px"},
            
        "nav-link": {"font-size": "25px", "text-align": "center", "margin": "-2px", "--hover-color": "#C8A6ED"},
        "nav-link-selected": {"background-color": "#7644AD",  "font-family": "YourFontFamily"}})
#Home_Screen
if select == "Home":
    col1,col2,col3= st.columns(3)
    with col2:
        img1 = Image.open(r"C:\Users\Admin\Downloads\PhonePe-Logo.png")
        st.image(img1, width=450)
        
    st.markdown('<h2 style="text-align: center; color: #BD09BB;">Data Visualization and Exploration</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #BD09BB;">A User-Friendly Tool Using Streamlit and Plotly</h2>', unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #6F36AD;'>", unsafe_allow_html=True)
    col1,col2,col3,= st.columns(3)
    with col1:
        st.markdown("### :globe_with_meridians: Domain :")
        st.markdown("- Fintech")
    with col2:
        st.markdown("### :desktop_computer: Technologies Used :")
        st.markdown("- Github Cloning")
        st.markdown("- Python")
        st.markdown("- Pandas")
        st.markdown("- PostgreSQL")
        st.markdown("- Streamlit")
        st.markdown("- Plotly")
    with col3: 
        st.markdown("### :chart_with_upwards_trend: Overview :")
        st.markdown("In this Streamlit web app, you can visualize the PhonePe Pulse data and gain a lot of insights on transactions, number of users, top 10 state, district, pincode, and which brand has the most number of users and so on. Bar charts, Pie charts, and Geo map visualization are used to get some insights.")
    st.markdown("<hr style='border: 2px solid #6F36AD;'>", unsafe_allow_html=True)

#Data Exploration
if select == "Data Exploration":
    st.markdown("<h1 style='text-align: center; color: #BD09BB;'>Data Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #6F36AD;'>", unsafe_allow_html=True)
    
    select = option_menu(
        menu_title = None,
        options = ["Aggregated Analysis","Map Analysis","Top Analysis"],
        default_index=0,
        icons=["signal", "pie-chart", "globe"],
        orientation="horizontal",
        styles={"container": {"padding": "0!important", "background-color": "#F7bCF6","size":"cover", "width": "200"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#C8A6ED"},
                "nav-link-selected": {"background-color": "#7644AD",  "font-family": "YourFontFamily"}})
    
    if select == "Aggregated Analysis":
        st.markdown("<h2 style='text-align: center; color: #7644AD;'>Aggregated Analysis</h2>", unsafe_allow_html=True)
                
        select = option_menu(
        menu_title = None,
        options = ["Aggregated Insurance","Aggregated Transaction","Aggregated User"],
        default_index=0,
        orientation="horizontal",
        styles={"container": {"padding": "0!important", "background-color": "#F7bCF6","size":"cover", "width": "200"},
                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#C8A6ED"},
                "nav-link-selected": {"background-color": "#7644AD",  "font-family": "YourFontFamily"}})
        
        if select == "Aggregated Insurance":
            st.markdown("<h3 style='text-align: center;'>Aggregated Insurance Analysis</h3>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year**", Aggre_insurance["Years"].unique())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)
            
            st.markdown("<h4 style='text-align: center;'>Analysis of Quarterly Aggregated Insurance</h4>", unsafe_allow_html=True)
            
            col1,col2,col3= st.columns(3)
            with col1:
                quarters= st.selectbox("**Select the Quarter**", tac_Y["Quarter"].unique())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
        
        elif select == "Aggregated Transaction":
            st.markdown("<h3 style='text-align: center;'>Aggregated Transaction Analysis</h3>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year**", Aggre_transaction["Years"].unique())
            Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the States**", Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            st.markdown("<h4 style='text-align: center;'>Analysis of Quarterly Aggregated Transactions</h4>", unsafe_allow_html=True)
            
            col1,col2,col3= st.columns(3)
            with col1:
                quarters= st.selectbox("**Select the Quarter**", Aggre_tran_tac_Y["Quarter"].unique())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Quaterly Analysis**", Aggre_tran_tac_Y_Q["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)

        elif select == "Aggregated User":
            st.markdown("<h3 style='text-align: center;'>Aggregated User Analysis</h3>", unsafe_allow_html=True)
            
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Aggregated User Analysis**", Aggre_user["Years"].unique())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)

            col1,col2,col3= st.columns(3)
            with col1:
                quarters= st.selectbox("**Select the Quarter for Aggregated User Analysis**", Aggre_user_Y["Quarter"].unique())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Aggregated User Analysis**", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    
    elif select == "Map Analysis":
        st.markdown("<h2 style='text-align: center; color: #7644AD;'>Map Analysis</h2>", unsafe_allow_html=True)
        select = option_menu(
        menu_title = None,
        options = ["Map Insurance","Map Transaction","Map User"],
        default_index=0,
        orientation="horizontal",
        styles={"container": {"padding": "0!important", "background-color": "#F7bCF6","size":"cover", "width": "200"},
                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#C8A6ED"},
                "nav-link-selected": {"background-color": "#7644AD",  "font-family": "YourFontFamily"}})
        if select == "Map Insurance":
            st.markdown("<h2 style='text-align: center;'>Map Insurance Analysis</h2>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Map Insurance Analysis**", Map_insurance["Years"].unique())
            map_insur_tac_Y = Transaction_amount_count_Y(Map_insurance, years)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the States for Map Insurance Analysis**", map_insur_tac_Y["States"].unique())
            Map_insur_District(map_insur_tac_Y, states)

            col1,col2,col3= st.columns(3)
            with col1:
                quarters= st.selectbox("**Select the Quarter for Map Insurance Analysis**", map_insur_tac_Y["Quarter"].unique())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Quaterly Analysis of Map Insurance**", map_insur_tac_Y_Q["States"].unique())
            Map_insur_District(map_insur_tac_Y_Q, states)

        elif select == "Map Transaction":
            st.markdown("<h2 style='text-align: center;'>Map Transaction Analysis</h2>", unsafe_allow_html=True)

            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Map Transaction Analysis**", Map_transaction["Years"].unique())
            map_tran_tac_Y = Transaction_amount_count_Y(Map_transaction, years)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the States for Map Transaction Analysis**", map_tran_tac_Y["States"].unique())
            Map_insur_District(map_tran_tac_Y, states)

            col1,col2,col3= st.columns(3)
            with col1:
                quarters= st.selectbox("**Select the Quarter for Map Transaction Analysis**", map_tran_tac_Y["Quarter"].unique())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Quaterly Analysis of Map Transaction**", map_tran_tac_Y_Q["States"].unique())
            Map_insur_District(map_tran_tac_Y_Q, states)

        elif select == "Map User":
            st.markdown("<h2 style='text-align: center;'>Map User Analysis</h2>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Map User Analysis**", Map_user["Years"].unique())
            map_user_Y = map_user_plot_1(Map_user, years)

            col1,col2,col3= st.columns(3)
            with col1:
                quarter= st.selectbox("**Select the Quarter for Map User Analysis**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter)

            col1,col2,col3= st.columns(3)
            with col1:
                state= st.selectbox("**Select the State for Map User Analysis**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state)

    elif select == "Top Analysis":
        st.markdown("<h2 style='text-align: center; color: #7644AD;'>Top Analysis</h2>", unsafe_allow_html=True)
        select = option_menu(
        menu_title = None,
        options = ["Top Insurance","Top Transaction","Top User"],
        default_index=0,
        orientation="horizontal",
        styles={"container": {"padding": "0!important", "background-color": "#F7bCF6","size":"cover", "width": "200"},
                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#C8A6ED"},
                "nav-link-selected": {"background-color": "#7644AD",  "font-family": "YourFontFamily"}})
        if select == "Top Insurance":
            st.markdown("<h2 style='text-align: center;'>Top Insurance Analysis</h2>", unsafe_allow_html=True)
            
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Top Insurance Analysis**", Top_insurance["Years"].unique())
            top_insur_tac_Y = Transaction_amount_count_Y(Top_insurance, years)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Quaterly Analysis of Top Insurance**", top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2,col3= st.columns(3)
            with col1:
                quarter= st.selectbox("**Select the Quarter for Top Insurance Analysis**",top_insur_tac_Y["Quarter"].unique())
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y,quarter)
              
        elif select == "Top Transaction":
            st.markdown("<h2 style='text-align: center;'>Top Transaction Analysis</h2>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Top Transaction Analysis**", Top_transaction["Years"].unique())
            top_tran_tac_Y = Transaction_amount_count_Y(Top_transaction, years)

            col1,col2,col3= st.columns(3)
            with col1:
                states= st.selectbox("**Select the State for Quaterly Analysis of Top Transaction**", top_tran_tac_Y["States"].unique())
            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2,col3= st.columns(3)
            with col1:
                quarter= st.selectbox("**Select the Quarter for Top Transaction Analysis**",top_tran_tac_Y["Quarter"].unique())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y,quarter)

        elif select == "Top User":
            st.markdown("<h2 style='text-align: center;'>Top User Analysis</h2>", unsafe_allow_html=True)
            col1,col2,col3= st.columns(3)
            with col1:
                years= st.selectbox("**Select the Year for Top User Analysis**", Top_user["Years"].unique())

            top_user_Y= top_user_plot_1(Top_user, years)

            col1,col2,col3= st.columns(3)
            with col1:
                state= st.selectbox("**Select the State for Top User Analysis**", top_user_Y["States"].unique())

            top_user_Y_S= top_user_plot_2(top_user_Y, state)

if select == "Top Charts":
    st.markdown("<h1 style='text-align: center; color: #BD09BB;'>Top Insights</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #6F36AD;'>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        ques = st.selectbox("**Select the Question**", [
            'States Ranking 1–10 With AppOpens',
            'At Least ten States Having AppOpens',
            'Leading Mobile Phone Brands Used Phones',
            'States Having The Largest Transaction Value',
            'States Having The Smallest Transaction Value',
            'Top 50 Districts With largest Transaction Amount',
            'Districts With The Largest Volume of Transactions',
            'Districts with the least amount of transactions',
            'States Having the Most Transactions',
            'States Having the Fewest Transactions',])
    
    
        if ques=="States Ranking 1–10 With AppOpens":
            ques1()           
    
        elif ques=="At Least ten States Having AppOpens":
            ques2()
    
        elif ques=="Leading Mobile Phone Brands Used Phones":
            ques3()
    
        elif ques=="States Having The Largest Transaction Value":
            ques4()
    
        elif ques=="States Having The Smallest Transaction Value":
            ques5()
    
        elif ques=="Top 50 Districts With largest Transaction Amount":
            ques6()
    
        elif ques=="Districts With The Largest Volume of Transactions":
            ques7()
    
        elif ques=="Districts with the least amount of transactions":
            ques8()
    
        elif ques=="States Having the Most Transactions":
            ques9()
    
        elif ques=="States Having the Fewest Transactions":
            ques10()






    