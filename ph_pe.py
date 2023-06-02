import mysql.connector
import pandas as pd
import streamlit as st 
import PIL
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import requests

conn = mysql.connector.connect(user = "root", password = "sriram@2898" ,host = "127.0.0.1",database = "phonepe_pulse" )

cursor = conn.cursor()
 
SELECT = option_menu(
    menu_title = None,
    options = ["About" ,"Home" , "Basic insights" , "contact" ],
    icons = ["bar-chart", "house", "toggles","at"],
    default_index=2,
    operation = "horizontal",
    styles={
        "container" :{"padding":"0!important","background-color" : "white","size":"cover","width" :"100%"},
        "icons" :{"color": "black","font-size":"20px"},
        "nav-link":{"font-size":"20px","text-align":"center","margin":"-2px","--hover-color":"#6F36AD"},
        "nav-link-selected":{"background-color":"#6F36AD"}
    })

if SELECT == "Basic insights":
    st.title("Basic insights")
    st.write("----")
    st.subheader("let's know some basic insights about the data ")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registerd-user based on States and District",
               "Top 10 Districts based on states and count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_count based on Districts and states",
               "top 10 RegisterdUsers based onstates and District"]
#1    
Select = st.selectbox("select the option",options)
if Select == "Top 10 states based on year and amount of transaction":
    cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_tran GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10"); 
    
    df = pd.DataFrame(cursor.fetchall(),columns=["States","Transaction_year","Transaction_Amount"])
    col1,col2 = st.columns(2)
    with col1:
        st.write(df)
    with col2:
        st.title("Top 10 states and amount of transaction")
        st.bar_chart(data = df, x = "Transaction_Amount",y = "States")
        
#2
elif Select == "List 10 states based on type and amount of transaction":   
     cursor.execute("SELECT DISTINCT States, SUM(Transaction_Count) as Total FROM top_tran GROUP BY States ORDER BY Total ASC LIMIT 10"); 
     df = pd.DataFrame(cursor.fetchall(),columns=["States","Total_Transaction"])
     col1,col2 = st.columns(2)
     with col1:
         st.write(df)
     with col2:
         st.title("List 10 states based on type and amount of transaction")
         st.bar_chart(data = df , x= "Total_Transaction",y = "States")
         
#3         
elif Select == "Top 5 Transaction_Type based on Transaction_Amount":
    cursor.execute("SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Amount FROM agg_user GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5");
    df = pd.DataFrame(cursor.fetchall(),columns=["Transaction_Type","Transaction_Amount"])
    col1,col2 = st.columns(2)
    with col1:
        st.write(df)
    with col2:
        st.title("Top 5 Transaction_Type based on Transaction_Amount")
        st.bar_chart(data = df,x = "Transaction_Type",y = "Amount")    

#4
elif Select == "Top 10 Registerd-user based on States and District":
    cursor.execute("SELECT DISTINCT State, District, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY State, District ORDER BY Users DESC LIMIT 10");
    df = pd.DataFrame(cursor.execute(),columns=["State","District","RegisteredUser "])   
    col1,col2 = st.columns(2)
    with col1:
        st.write(df)
    with col2:
        st.title("Top 10 Registerd-user based on States and District")
        st.bar_chart(data = df, x = "State",y="RegisteredUsers")
                
#5
elif Select == "Top 10 Districts based on states and count of transaction":
    cursor.execute("SELECT DISTINCT States,District,SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
    df = pd.DataFrame(cursor.execute(),columns=['States','District','Transaction_Count'])
    col1,col2 = st.columns(2)
    with col1:
        st.write(df)
    with col2:
        st.title("Top 10 Districts based on states and count of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Count")
               
#6               
elif Select=="List 10 Districts based on states and amount of transaction":
    cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Amount FROM agg_trans GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
    df = pd.DataFrame(cursor.execute(),columns=['States','Transaction_year','Transaction_Amount'])
    col1,col2 = st.columns(2)
    with col1:
        st.write(df)
    with col2:
        st.title("List 10 Districts based on states and amount of transaction")
        st.bar_chart(data = df,x="States",y="Transaction_Amount")  
#7
elif Select== "List 10 Transaction_count based on Districts and states":
     cursor.execute("SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
     df = pd.DataFrame(cursor.execute(),columns=['States','District','Transaction_Count'])
     col1,col2 = st.columns(2)
     with col1:
         st.write(df)
     with col2:
         st.title("List 10 Transaction_count based on Districts and states")
         st.bar_chart(data = df,x="States",y="Transaction_Count")       
#8           
elif Select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT States,District, SUM(RegisteredUsers) AS Users FROM map_user GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 RegisteredUsers based on states and District")
            st.bar_chart(data=df,x="States",y="RegisteredUsers")


#Home
cursor = conn.cursor()

cursor.execute("SELECT * From agg_trans")

rows = cursor.fetchall()

if SELECT == "Home":
    col1 = st.columns(1)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
        
    df = pd.DataFrame(rows, columns=['States', 'Transaction_Year', 'Quarters', 'Transaction_Type', 'Transaction_Count','Transaction_Amount'])
    fig = px.choropleth(df, locations="States", scope="asia", color="States", hover_name="States",
        title="Live Geo Visualization of India")
    st.plotly_chart(fig)
    
    
#About
if SELECT == "About":
    col1 = st.columns(1)
    with col1:
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1 = st.columns(1)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        with open("C:\Users\srira\Downloads\annual report.pdf","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
        
        
#Contact

if SELECT == "Contact":
    name = "Sriram"
    mail = (f'{"Mail :"}  {"sriramjr28@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        "GITHUB": "https://github.com/starboyjr",
        "LINKEDIN": "https://www.linkedin.com/in/sriram-r-905585266/"}
    
    col1, col2 = st.columns(2)
    with col2:
        st.title('Phonepe Pulse data visualisation')
        st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        st.subheader(mail)
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")        
        
    