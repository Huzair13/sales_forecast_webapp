import logging

from flask_pymongo import pymongo
from flask import jsonify, request,session,make_response
from pandas.tseries.offsets import DateOffset

import pandas as pd
import bcrypt
import json
from statsmodels.tsa.stattools import adfuller
from pandas.tseries.offsets import DateOffset
import io
import matplotlib.dates as mdates
import base64
import statsmodels.api as sm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import pickle

con_string = "mongodb+srv://huzair13:huz2002@cluster0.7927yqz.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('databasef')



user_collection = pymongo.collection.Collection(db, 'collectionf') #(<database_name>,"<collection_name>")

users=pymongo.collection.Collection(db,'userList')


print("MongoDB connected Successfully")

# with open('finalized_model.pkl', 'rb') as f:
#     model, params = pickle.load(f)


def project_api_routes(endpoints):

    @endpoints.after_request
    def add_header(response):
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 0
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        print("Hello world Hellow")
        print(res)
        return res

    @endpoints.route('/register- user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    @endpoints.route('/register-user2', methods=['POST'])
    def register_user_new2():
        resp = {}
        try:
            req_body = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            users.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    

    
    @endpoints.route('/register-user1', methods=['POST'])
    def register_user_new():
        resp = {}
        try:
            data = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            result = user_collection.find_one({'id': data['id'], 'name': data['name'], 'email': data['email']})

            if result:
                print("Data Already Exists")
                status = {
                    "statusCode":"400",
                    "statusMessage":"User Data Stored NOT Successfully in the Database."
                }
            else:
                user_collection.insert_one(data)
                print("User Data Stored Successfully in the Database.")
                status = {
                    "statusCode":"200",
                    "statusMessage":"User Data Stored Successfully in the Database."
                }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    
    @endpoints.route('/login_users',methods=['POST'])
    def login_user():
        resp={}
        data = request.json

        result = users.find_one({'name': data['name'], 'password': data['password']})
        # data = request.get_json()
        # username = data.get('name')
        # password = data.get('password')

        # user = db.users.find_one({'name': username, 'password': password})

        if result:
            response = {
                'statusCode': 400,
                'statusMessage': 'Invalid username or password'
            }
        else:
            response = {
                'statusCode': 200,
                'statusMessage': 'Login successful',
            }
        resp["status"] =response
        return resp



    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp = {}
        try:
            users_list = users.find({})
            print(users)
            users_list = list(users_list)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'Name' : user['name'], 'Email' : user['email']} for user in users_list]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update-users',methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"id":req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    
        


    #USER SIGNIN AND SIGNUP

    @endpoints.route('/signup', methods=['POST'])
    def signup():
        try:
            username = request.json['name']
            email=request.json['email']
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(request.json['password'].encode('utf-8'), salt)
            user = {'name': username, 'password': password,'email':email}

            if users.find_one({'name': username}) or users.find_one({'email':email}):
                status = {
                "statusCode":"400",
                "statusMessage":"Username or email alread exists"
                }

            else :
                users.insert_one(user)
                print("User Data Stored Successfully in the Database.")
                status = {
                    "statusCode":"200",
                    "statusMessage":"User Data Stored Successfully in the Database."
                    }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }

        return jsonify(status)

    @endpoints.route('/signin', methods=['POST'])
    def signin():
        username = request.json['name']
        password = request.json['password']

        user = users.find_one({'name': username})

        if user and bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
            session['user'] = username
            response = {'statusCode': 200, 'statusMessage': 'User logged in successfully'}
        else:
            response = {'statusCode': 400, 'statusMessage': 'Invalid credentials'}
    
        return jsonify(response)




    @endpoints.route('/logout',methods=['DELETE'])
    def logout():
        session.pop('user', None)
        return jsonify({'statusCode': 200, 'statusMessage': 'User logged out successfully'})


    
    #FORECAST
    
    @endpoints.route('/forecast', methods=['POST'])
    def forecast():
        try:

            selected_option = request.form['selectedOption']
            number = int(request.form['number'])
            # Load the SARIMAX model from the pickle file
            with open('sarimax_model.pkl', 'rb') as f:
                model = pickle.load(f)

            offset_map = {
                'years': 'years',
                'weeks': 'weeks',
                'months': 'months',
                'days' : 'days'
                # Add more options as needed
            }
        
            # Read the uploaded CSV file into a Pandas DataFrame
            file = request.files.get('file')
            df = pd.read_csv(file)
        
            # Clean up the data and prepare it for prediction
            df.columns = ["Month", "Passengers"]
            df['Month'] = pd.to_datetime(df['Month'])
            df.set_index('Month', inplace=True)
            df.index.freq = 'MS'  # Set the frequency of the time series to monthly
        
            # Make predictions for the next 48 months
            # offset_s = pd.DateOffset(**{offset_map[selected_option]: 1})
            # offset = pd.DateOffset(**{offset_map[selected_option]: number})
            # start_date = df.index[-1] + offset_s
            # end_date = start_date + offset

            
            offset_s = pd.DateOffset(**{offset_map[selected_option]: 1})
            offset = pd.DateOffset(**{offset_map[selected_option]: number})
            last_date = df.index[-1]
            start_date = last_date + offset_s

            if selected_option == 'days':
                end_date = last_date + offset
            elif selected_option == 'weeks':
                end_date = last_date + offset_s * 7 * number
            elif selected_option == 'months':
                end_date = last_date + pd.offsets.MonthBegin(n=number)
                end_date = end_date + offset_s
                end_date = end_date - pd.offsets.Day(n=1)
            else:
                end_date = last_date + pd.offsets.YearBegin(n=number)
                end_date = end_date + offset_s
                end_date = end_date - pd.offsets.Month(n=1)

            predictions = model.predict(start=start_date, end=end_date, dynamic=True)
            
        
            # Combine the historical data with the predicted values
            df_forecast = pd.DataFrame({'Passengers': predictions}, index=predictions.index)
            df_all = pd.concat([df, df_forecast])
            df_all['forecast']=predictions

            #plot graphs
            fig, ax = plt.subplots(figsize=(12, 8))
            df_all[['Passengers', 'forecast']].plot(ax=ax)
            plt.title('Passenger Traffic Forecast')
            plt.xlabel('Date')
            plt.ylabel('Passengers')
            plt.grid()
            plt.tight_layout()

            # Save the plot to a bytes buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
        
            # Convert the data to JSON format and return it to the client
            data = {'dates': df_all.index.strftime('%Y-%m-%d').tolist(), 'passengers': df_all['Passengers'].tolist()}
            resp = {
                'status': {
                    'statusCode': '200', 
                    'statusMessage': 'Success'
                }, 
                'data': data,
                'image': base64.b64encode(buffer.read()).decode('utf-8')
            }
        
        except Exception as e:
            resp = {'status': {'statusCode': '400', 'statusMessage': str(e)}}
    
        return jsonify(resp)


    @endpoints.route('/salesforecast', methods=['POST'])
    def salesforecast():
        try:

            selected_option = request.form['selectedOption']
            number = int(request.form['number'])

            with open('sales_forecasting_jp.pkl', 'rb') as f:
                model = pickle.load(f)

            offset_map = {
                'years': 'years',
                'weeks': 'weeks',
                'months': 'months',
                'days' : 'days'
            }

            file = request.files.get('file')
            df = pd.read_csv(file)
        
            df.columns = ["Month", "Sales"]
            df=df.dropna()
            df['Month'] = pd.to_datetime(df['Month'])
            df.set_index('Month', inplace=True)
            df.index.freq = 'MS' 
        
            
            offset_s = pd.DateOffset(**{offset_map[selected_option]: 1})
            offset = pd.DateOffset(**{offset_map[selected_option]: number})

            last_date = df.index[-1]
            start_date = last_date + offset_s

            # if selected_option == 'days':
            #     df = df.asfreq('D', method='ffill')
            #     start_date = last_date + pd.DateOffset(days=1)
            #     end_date = last_date + pd.DateOffset(days=number)
            # elif selected_option == 'weeks':
            #     end_date = last_date + offset_s * 7 * number
            # elif selected_option == 'months':
            #     end_date = last_date + pd.offsets.MonthBegin(n=number)
            #     end_date = end_date + offset_s
            #     end_date = end_date - pd.offsets.Day(n=1)
            # else:
            #     end_date = pd.Timestamp(year=last_date.year, month=1, day=1) + pd.offsets.DateOffset(years=number)
            #     end_date = end_date + offset_s
            #     end_date = end_date - pd.offsets.MonthEnd(n=1)
            
            fig, ax = plt.subplots(figsize=(12, 8))

            if selected_option == 'days':
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  
                # df = df.asfreq('D', method='ffill')
                start_date = last_date + pd.DateOffset(days=1)
                end_date = last_date + pd.DateOffset(days=number)
            elif selected_option == 'weeks':
                ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))  # set x-axis tick frequency to every 1 week starting on Monday
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  # set x-axis tick format to month/day/year
                end_date = last_date + pd.DateOffset(weeks=number)
                
                # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) 
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  
                # start_date = last_date + pd.DateOffset(weeks=1)
                # end_date = last_date + offset_s * 7 * number
            elif selected_option == 'months':
                ax.xaxis.set_major_locator(mdates.MonthLocator()) 
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  
                end_date = last_date + pd.offsets.MonthBegin(n=number)
                end_date = end_date + offset_s
                end_date = end_date - pd.offsets.Day(n=1)
            else:
                ax.xaxis.set_major_locator(mdates.YearLocator()) 
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) 
                end_date = pd.Timestamp(year=last_date.year, month=1, day=1) + pd.offsets.DateOffset(years=number)
                end_date = end_date + offset_s
                end_date = end_date - pd.offsets.MonthEnd(n=1)


            
            model1 = sm.tsa.statespace.SARIMAX(df['Sales'], order=(1,1,1), seasonal_order=(1,1,1,12))

            results = model1.fit()

            predictions = results.predict(start=start_date, end=end_date,dynamic=True)
            
        
            df_forecast = pd.DataFrame({'Sales': predictions}, index=predictions.index)
            df_forecast['forecast']=predictions

            df_all = pd.concat([df, df_forecast])
            df_all['forecast']=predictions

            # fig, ax = plt.subplots(figsize=(12, 8))
            # ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            # if selected_option == 'days':
            #     ax.xaxis.set_major_locator(pd.tseries.offsets.Day(1))
            df_all[['Sales', 'forecast']].plot(ax=ax, color=['#0077c2', '#ff6361'])
            plt.title('History & Future')
            plt.xlabel('Date')
            plt.ylabel('Sales')
            plt.grid()
            plt.tight_layout()


            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)


            
            df_forecast.plot(figsize=(10,6),color='purple')
            plt.title('Future Forecasting')

            buffer2=io.BytesIO()
            plt.savefig(buffer2,format='png')
            buffer2.seek(0)
        
            data = {'dates': df_forecast.index.strftime('%Y-%m-%d').tolist(), 'Sales': df_forecast['Sales'].tolist()}
            resp = {
                'status': {
                    'statusCode': '200', 
                    'statusMessage': 'Success'
                }, 
                'data': data,
                'image': base64.b64encode(buffer.read()).decode('utf-8'),
                'image2' : base64.b64encode(buffer2.read()).decode('utf-8')
            }
        
        except Exception as e:
            resp = {'status': {'statusCode': '400', 'statusMessage': str(e)}}
    
        return jsonify(resp)

    
    @endpoints.route('/download_prediction',methods=['POST','GET'])
    def download():

        json_data = request.get_json()
        df = pd.DataFrame(json_data)
        csv_string = df.to_csv(index=False)
        response = make_response(csv_string)
        response.headers.set('Content-Disposition', 'attachment', filename='data.csv')
        response.headers.set('Content-Type', 'text/csv')

        return response



    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            df = pd.read_csv(file)
            print(df)
            print(df.head())
            print(df.columns)

            ## Cleaning up the data
            df.columns=["Month","Passengers"]
            df['Month']=pd.to_datetime(df['Month'])
            df.set_index('Month',inplace=True)
            test_result=adfuller(df['Passengers'])
            adfuller_test(df['Passengers'])
            df['Sales First Difference'] = df['Passengers'] - df['Passengers'].shift(1)
            adfuller_test(df['Sales First Difference'].dropna())
            df['Seasonal First Difference']=df['Passengers']-df['Passengers'].shift(12)
            adfuller_test(df['Seasonal First Difference'].dropna())
            future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,48)]
            future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)
            future_df=pd.concat([df,future_datest_df])

            #predict
             # Load the trained SARIMAX model
            with open('finalized_model.pkl', 'rb') as f:
                model, params = pickle.load(f)
                future_df['forecast'] = model.predict(start = 145, end = 175, dynamic= True,params=params)

            data = {'forecast': future_df['forecast'].tolist()}

            # # Convert the dataframe to a JSON string
            # json_data = df.to_json(orient='records')
            # status = {
            #     "statusCode":"200",
            #     "statusMessage":"File uploaded Successfully."
            # }

            # # data = json.loads(json_data)
            # resp = {
            #     "status": status,
            #     "data": data
            # }

            # Combine the historical data with the predicted values
            future_df["Passengers"] = forecast
            df = pd.concat([df, future_df])

            # Convert the data to JSON format and return it to the client
            data = {"dates": df.index.strftime("%Y-%m-%d").tolist(), "passengers": df["Passengers"].tolist()}

            resp= {"status": {"statusCode": "200", "statusMessage": "Success"}, "data": data}
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
            resp["status"] =status
        return json.dumps(resp)




    def adfuller_test(sales):
        #Ho: It is non stationary
        #H1: It is stationary
        result=adfuller(sales)
        labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
        for value,label in zip(result,labels):
            print(label+' : '+str(value) )
        if result[1] <= 0.05:
            print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
        else:
            print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")
    


    return endpoints