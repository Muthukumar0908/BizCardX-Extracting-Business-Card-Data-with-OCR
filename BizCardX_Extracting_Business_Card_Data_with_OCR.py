import easyocr
import PIL
from PIL import Image
from PIL import ImageDraw
import pandas as pd
# import pytesseract
import cv2
import re
import mysql.connector
# import pymysql
import streamlit as st
from sqlalchemy import create_engine


dic=[]
    
#sql data base
host = 'localhost'
user = 'root'
password = ''
database = 'bizcard'
mydb=mysql.connector.connect(host=host, user=user, password=password, database=database)
# print(mydb)
mycursor=mydb.cursor(buffered=True)

# create_engine
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')



def collect_data():
    st.title('Image Text Recognition')
    image = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png']) 

    if image is not None:
        st.image(image, use_column_width=True)
        with st.spinner('Recognizing text...'):
    
            image_data = image.read()
            result = reader.readtext(image_data,paragraph="False")
            if result:
                # st.write(result)
                for i in result:
                        a=str(i[-1])
                    #     print(type(a))
                        dic.append(a)
                        data1= ', '.join([str(item) for item in dic])
                st.markdown("#### first step: :ok_hand:")
                st.write(data1)
                
                sql_data={}
                
                
                name=re.findall(r'^(\w+)',data1)
                sql_data['name']=name
                # sql_data_dic.append(name)
                # print(sql_data)
                


                email=re.findall(r'\w+@\w+.\w+',data1)
                sql_data['email']=email
                # sql_data_dic.append(email)
                # print(sql_data)

                website=re.findall(r'WWW \w+.\w+',data1) or re.findall(r'wWW.\w+.\w+',data1) or re.findall(r"www.\w+.\w+",data1) or re.findall(r'WWW.\w+.\w+',data1)
                sql_data['website']=website
                # sql_data_dic.append(website)
                # print(sql_data)


                phonenumber=re.findall(r'\+\d+-\d+-\d+ ',data1) or re.findall(r"\d+-\d+-\d+",data1)
                sql_data['phonenumber']=phonenumber
                # sql_data_dic.append(phonenumber)
                # print(sql_data)


                state=re.findall(r'TamilNadu',data1)
                sql_data['state']=state
                # sql_data_dic.append(state)
                # print(sql_data)

                city=re.findall(r'\d+ \w+ \w+',data1)
                sql_data['city']=city
                # sql_data_dic.append(city)
                # print(sql_data)
                
                pincode=re.findall(r'\d{6}',data1)
                sql_data['pincode']=pincode
                # sql_data_dic.append(pincode)
                # print(sql_data)

                
                                
                company_name=re.findall(r'([^,]+)$',data1)
                sql_data['company_name']=company_name
                # sql_data_dic.append(city)
                # print(sql_data)

                designation=re.findall(r'[A-Z]{3}+ & +[A-Z]+',data1) or re.findall(r'[A-Z]{4} [A-Z]{7}+',data1) or re.findall(r'[A-Za-z]{9} [A-Za-z]{9}+',data1) or re.findall(r'[A-Za-z]{9} [A-Za-z]{7}+',data1)
                # designation=re.findall(r'[A-Z0-9& ]',data1)
                sql_data['designation']=designation
                # # # sql_data.append(city)
                # print(type(sql_data))
            st.markdown("#### second step:  :ok_hand: ")
            st.table(sql_data)
            a=sql_data.keys()
            listq=[]
            for i in sql_data.values():
                listq.extend(i)
            h=listq[0]
            df=pd.DataFrame(sql_data)
            df1=pd.DataFrame(columns=a)
            table_name ='card_data'
            df1.to_sql(table_name,if_exists="append" ,con=engine, index=False)
            if st.button('import to sql'):
                query="""SELECT name FROM card_data"""
                mycursor.execute(query)
                data =mycursor.fetchall()
                # print(data)
                mydb.commit()
                # df1= pd.DataFrame(data,columns=mycursor.column_names)
                # df1
                # st.write(df)
                a=[]
                for i in data:
                    # print(i)
                    a.append(i[0])
                # st.write(a)
                if h in a:
                    # print(listq)
                    st.success('card data all ready exist !! :-1:')
                else:
                    table_name ='card_data'
                    df.to_sql(table_name,if_exists="append" ,con=engine, index=False)
                    st.success("new_card !!  :+1: ")
                    # st.table(sql_data)

def table_create():
    mycursor.execute('USE bizcard')
    mycursor.execute("""create table card_data """)
    mydb.commit()
# Initialize easyocr Reader
reader = easyocr.Reader(['en']) 
with st.sidebar:
    selected = st.selectbox("**Menu**", ["collect_data","edit_data"])
if selected=="collect_data":
    collect_data()
            
if selected=='edit_data':
    try:
        mycursor.execute("SELECT name,company_name FROM card_data")
        result = mycursor.fetchall()
        cards = {}
            # print(business_cards)
        for i in result:
            cards[i[0]] = i[0]
            # st.write(row[0])
        selected_card = st.selectbox("Select a card holder name to update", list(cards.keys()))
        st.markdown("#### Update or modify any data below")
        colum4,colum6 = st.columns([0.5,0.5],gap="large")

        with colum4:

            
            mycursor.execute("select * from card_data WHERE name=%s",
                            (selected_card,))
            result = mycursor.fetchone()
            name = st.text_input("name", result[0])
            email= st.text_input("email", result[1])                             
            website= st.text_input("website", result[2])
            phonenumber=st.text_input("phonenumber", result[3])
            pincode=st.text_input("pincode", result[6])
        with colum6:
            
            state=st.text_input("state", result[4],)
            city=st.text_input("address", result[5])
            company_name=st.text_input("company_name", result[7])
            designation=st.text_input("designation", result[8])
            st.markdown("####")
            
            st.markdown("####")
        
            st.markdown("####")
        
        if st.button("insert"):
                sq1l="update card_data set email=%s, website=%s,phonenumber=%s,pincode=%s,state=%s,city=%s,company_name=%s,designation=%s where name=%s"
                values=(email,website,phonenumber,pincode,state,city,company_name,designation,name)
                mycursor.execute(sq1l,values)
                mydb.commit()
                st.success("data was updated!! :+1:")
        if st.button("drop"):
                dic=[]
                sq1l="delete from card_data where name=%s"
                dic.append(name)
                values=(dic)
                mycursor.execute(sq1l,values)
                mydb.commit()
                st.success("data was deleted !! :unamused:")
    except:
        st.success('no data added!!!!')            
        
    
    
    
    