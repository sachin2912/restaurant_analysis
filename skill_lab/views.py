from django.shortcuts import render,redirect
from django.utils.html import strip_tags

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
import matplotlib.pyplot as plt
pd.set_option("display.max_columns",500)

from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.models import load_model
from sklearn.externals import joblib
import keras


def home(request):
    
    if request.method == "POST":
        form1=request.POST
        
        establishment = form1['est']
        establishment=establishment.replace("\r\n","")
        locality= form1['locality']
        locality=locality.replace("\r\n","")
        cuisines=[]
        for i in form1.getlist('cuisines[]'):
            cuisines.append(i.replace("\r\n",""))
        operating_time_start = form1['fromtime']
        operating_time_end = form1['totime']
        highlights=[]
        for i in form1.getlist('highlights[]'):
            highlights.append(i.replace("\r\n",""))
        Home_delivery = form1['customRadioInline1']
        cost = form1['cost']
        cost=cost.replace("\r\n","")
        rating = form1['rating']
        rating=rating.replace("\r\n","")
        if Home_delivery=="on":
            Home_delivery=1
        elif Home_delivery=="off":
            Home_delivery=-1

        start=""
        for i in range(0,len(operating_time_start)):
            if operating_time_start[i]!=":":
                if i==0 and operating_time_start[i]!="0":
                    start+=operating_time_start[i]
                else:
                    start+=operating_time_start[i]
                
        end=""
        for i in range(0,len(operating_time_end)):
            if operating_time_end[i]!=":":
                if i==0 and operating_time_end[i]!="0":
                    end+=operating_time_end[i]
                else:
                    end+=operating_time_end[i]
        if rating=="":
            call=1
            res_value=cost
            what_is="cost"
            result=deafult_call(call,cuisines,highlights,establishment,locality,Home_delivery,int(start),int(end),int(cost))
        elif cost=="":
            call=2
            res_value=rating
            what_is="rating"
            result=deafult_call(call,cuisines,highlights,establishment,locality,Home_delivery,int(start),int(end),rating)
        result_1={
            "result" : result[0],
            "est" : establishment,
            "locality" : locality,
            "cuisines" : cuisines,
            "Home_delivery" : Home_delivery,
            "st_timing" : operating_time_start,
            "end_timing" : operating_time_end,
            "res_value" : res_value,
            "what_is" : what_is,
            "highlights" : highlights,
        }
        return render(request,"results.html",result_1)
    return render(request,"index.html",{})
    


def deafult_call(call,cuisine_inputs,highlight_inputs,establishment,locality,delivery,start,end,rating_cost):
    cuisines_list = []
    with open('/home/sachin/Desktop/skill_lab/static/text/cuisines.txt') as f:
        for line in f.readlines():
            cuisines_list.append(line.strip(',\n'))

    highlights_list = []
    with open('/home/sachin/Desktop/skill_lab/static/text/highlights.txt') as f:
        for line in f.readlines():
            highlights_list.append(line.strip(',\n'))

    establishment_list = []
    with open('/home/sachin/Desktop/skill_lab/static/text/establishment.txt') as f:
        for line in f.readlines():
            establishment_list.append(line.strip(',\n'))

    locality_list = []
    with open('/home/sachin/Desktop/skill_lab/static/text/locality.txt') as f:
        for line in f.readlines():
            locality_list.append(line.strip(',\n'))

    # ---------------------------------------------------------------------------------------

    PC_data_columns = ['establishment', 'locality_verbose', 'aggregate_rating', 'delivery', 'cuisine_1', 'cuisine_2', 'cuisine_3', 'cuisine_4', 'cuisine_5', 'cuisine_6', 'cuisine_7', 'cuisine_8', 'cuisine_9', 'cuisine_10', 'cuisine_11', 'cuisine_12', 'cuisine_13',
                    'cuisine_14', 'cuisine_15', 'cuisine_16', 'cuisine_17', 'cuisine_18', 'cuisine_19', 'cuisine_20', 'cuisine_21', 'cuisine_22', 'cuisine_23', 'cuisine_24', 'cuisine_25', 'cuisine_26', 'cuisine_27', 'cuisine_28', 'cuisine_29', 'cuisine_30', 'cuisine_31', 'cuisine_32', 'cuisine_33',
                    'cuisine_34', 'cuisine_35', 'cuisine_36', 'cuisine_37', 'cuisine_38', 'cuisine_39', 'cuisine_40', 'cuisine_41', 'cuisine_42', 'cuisine_43', 'cuisine_44', 'cuisine_45', 'cuisine_46', 'cuisine_47', 'cuisine_48', 'cuisine_49', 'cuisine_50', 'cuisine_51', 'cuisine_52', 'cuisine_53',
                    'cuisine_54', 'cuisine_55', 'cuisine_56', 'cuisine_57', 'cuisine_58', 'cuisine_59', 'cuisine_60', 'cuisine_61', 'cuisine_62', 'cuisine_63', 'cuisine_64', 'cuisine_65', 'cuisine_66', 'cuisine_67', 'cuisine_68', 'cuisine_69', 'cuisine_70', 'cuisine_71', 'cuisine_72', 'cuisine_73',
                    'cuisine_74', 'cuisine_75', 'cuisine_76', 'cuisine_77', 'cuisine_78', 'cuisine_79', 'cuisine_80', 'cuisine_81', 'cuisine_82', 'cuisine_83', 'cuisine_84', 'cuisine_85', 'cuisine_86', 'cuisine_87', 'cuisine_88', 'cuisine_89', 'cuisine_90', 'cuisine_91', 'cuisine_92', 'cuisine_93',
                    'cuisine_94', 'cuisine_95', 'cuisine_96', 'cuisine_97', 'cuisine_98', 'cuisine_99', 'cuisine_100', 'cuisine_101', 'cuisine_102', 'cuisine_103', 'cuisine_104', 'cuisine_105', 'cuisine_106', 'cuisine_107', 'cuisine_108', 'cuisine_109', 'cuisine_110', 'cuisine_111', 'cuisine_112', 'cuisine_113',
                    'cuisine_114', 'cuisine_115', 'cuisine_116', 'cuisine_117', 'cuisine_118', 'cuisine_119', 'cuisine_120', 'cuisine_121', 'cuisine_122', 'cuisine_123', 'cuisine_124', 'cuisine_125', 'cuisine_126', 'cuisine_127', 'cuisine_128', 'cuisine_129', 'cuisine_130', 'cuisine_131', 'cuisine_132', 'cuisine_133',
                    'highlight_1', 'highlight_2', 'highlight_3', 'highlight_4', 'highlight_5', 'highlight_6', 'highlight_7', 'highlight_8', 'highlight_9', 'highlight_10', 'highlight_11', 'highlight_12', 'highlight_13', 'highlight_14', 'highlight_15', 'highlight_16', 'highlight_17', 'highlight_18', 'highlight_19', 'highlight_20',
                    'highlight_21', 'highlight_22', 'highlight_23', 'highlight_24', 'highlight_25', 'highlight_26', 'highlight_27', 'highlight_28', 'highlight_29', 'highlight_30', 'highlight_31', 'highlight_32', 'highlight_33', 'highlight_34', 'highlight_35', 'highlight_36', 'highlight_37', 'highlight_38', 'highlight_39', 'highlight_40',
                    'highlight_41', 'highlight_42', 'highlight_43', 'highlight_44', 'highlight_45', 'highlight_46', 'highlight_47', 'highlight_48', 'highlight_49', 'highlight_50', 'highlight_51', 'highlight_52', 'highlight_53', 'highlight_54', 'highlight_55', 'highlight_56', 'highlight_57', 'highlight_58', 'highlight_59', 'highlight_60',
                    'highlight_61', 'highlight_62', 'highlight_63', 'highlight_64', 'highlight_65', 'highlight_66', 'highlight_67', 'highlight_68', 'highlight_69', 'highlight_70', 'highlight_71', 'highlight_72', 'highlight_73', 'highlight_74', 'highlight_75', 'highlight_76', 'highlight_77', 'highlight_78', 'highlight_79', 'highlight_80',
                    'highlight_81', 'highlight_82', 'highlight_83', 'highlight_84', 'highlight_85', 'highlight_86', 'highlight_87', 'highlight_88', 'highlight_89', 'highlight_90', 'highlight_91', 'highlight_92', 'highlight_93', 'highlight_94', 'highlight_95', 'highlight_96', 'highlight_97', 'highlight_98', 'highlight_99', 'highlight_100',
                    'highlight_101', 'highlight_102', 'highlight_103', 'highlight_104',
                    'start', 'end']
    PR_data_columns = ['establishment', 'locality_verbose', 'average_cost_for_two', 'delivery', 'cuisine_1', 'cuisine_2', 'cuisine_3', 'cuisine_4', 'cuisine_5', 'cuisine_6', 'cuisine_7', 'cuisine_8', 'cuisine_9', 'cuisine_10', 'cuisine_11', 'cuisine_12', 'cuisine_13',
                    'cuisine_14', 'cuisine_15', 'cuisine_16', 'cuisine_17', 'cuisine_18', 'cuisine_19', 'cuisine_20', 'cuisine_21', 'cuisine_22', 'cuisine_23', 'cuisine_24', 'cuisine_25', 'cuisine_26', 'cuisine_27', 'cuisine_28', 'cuisine_29', 'cuisine_30', 'cuisine_31', 'cuisine_32', 'cuisine_33',
                    'cuisine_34', 'cuisine_35', 'cuisine_36', 'cuisine_37', 'cuisine_38', 'cuisine_39', 'cuisine_40', 'cuisine_41', 'cuisine_42', 'cuisine_43', 'cuisine_44', 'cuisine_45', 'cuisine_46', 'cuisine_47', 'cuisine_48', 'cuisine_49', 'cuisine_50', 'cuisine_51', 'cuisine_52', 'cuisine_53',
                    'cuisine_54', 'cuisine_55', 'cuisine_56', 'cuisine_57', 'cuisine_58', 'cuisine_59', 'cuisine_60', 'cuisine_61', 'cuisine_62', 'cuisine_63', 'cuisine_64', 'cuisine_65', 'cuisine_66', 'cuisine_67', 'cuisine_68', 'cuisine_69', 'cuisine_70', 'cuisine_71', 'cuisine_72', 'cuisine_73',
                    'cuisine_74', 'cuisine_75', 'cuisine_76', 'cuisine_77', 'cuisine_78', 'cuisine_79', 'cuisine_80', 'cuisine_81', 'cuisine_82', 'cuisine_83', 'cuisine_84', 'cuisine_85', 'cuisine_86', 'cuisine_87', 'cuisine_88', 'cuisine_89', 'cuisine_90', 'cuisine_91', 'cuisine_92', 'cuisine_93',
                    'cuisine_94', 'cuisine_95', 'cuisine_96', 'cuisine_97', 'cuisine_98', 'cuisine_99', 'cuisine_100', 'cuisine_101', 'cuisine_102', 'cuisine_103', 'cuisine_104', 'cuisine_105', 'cuisine_106', 'cuisine_107', 'cuisine_108', 'cuisine_109', 'cuisine_110', 'cuisine_111', 'cuisine_112', 'cuisine_113',
                    'cuisine_114', 'cuisine_115', 'cuisine_116', 'cuisine_117', 'cuisine_118', 'cuisine_119', 'cuisine_120', 'cuisine_121', 'cuisine_122', 'cuisine_123', 'cuisine_124', 'cuisine_125', 'cuisine_126', 'cuisine_127', 'cuisine_128', 'cuisine_129', 'cuisine_130', 'cuisine_131', 'cuisine_132', 'cuisine_133',
                    'highlight_1', 'highlight_2', 'highlight_3', 'highlight_4', 'highlight_5', 'highlight_6', 'highlight_7', 'highlight_8', 'highlight_9', 'highlight_10', 'highlight_11', 'highlight_12', 'highlight_13', 'highlight_14', 'highlight_15', 'highlight_16', 'highlight_17', 'highlight_18', 'highlight_19', 'highlight_20',
                    'highlight_21', 'highlight_22', 'highlight_23', 'highlight_24', 'highlight_25', 'highlight_26', 'highlight_27', 'highlight_28', 'highlight_29', 'highlight_30', 'highlight_31', 'highlight_32', 'highlight_33', 'highlight_34', 'highlight_35', 'highlight_36', 'highlight_37', 'highlight_38', 'highlight_39', 'highlight_40',
                    'highlight_41', 'highlight_42', 'highlight_43', 'highlight_44', 'highlight_45', 'highlight_46', 'highlight_47', 'highlight_48', 'highlight_49', 'highlight_50', 'highlight_51', 'highlight_52', 'highlight_53', 'highlight_54', 'highlight_55', 'highlight_56', 'highlight_57', 'highlight_58', 'highlight_59', 'highlight_60',
                    'highlight_61', 'highlight_62', 'highlight_63', 'highlight_64', 'highlight_65', 'highlight_66', 'highlight_67', 'highlight_68', 'highlight_69', 'highlight_70', 'highlight_71', 'highlight_72', 'highlight_73', 'highlight_74', 'highlight_75', 'highlight_76', 'highlight_77', 'highlight_78', 'highlight_79', 'highlight_80',
                    'highlight_81', 'highlight_82', 'highlight_83', 'highlight_84', 'highlight_85', 'highlight_86', 'highlight_87', 'highlight_88', 'highlight_89', 'highlight_90', 'highlight_91', 'highlight_92', 'highlight_93', 'highlight_94', 'highlight_95', 'highlight_96', 'highlight_97', 'highlight_98', 'highlight_99', 'highlight_100',
                    'highlight_101', 'highlight_102', 'highlight_103', 'highlight_104',
                    'start', 'end']
    with keras.backend.get_session().graph.as_default():
        if (call==2):
            predict_cost = load_model('/home/sachin/Desktop/skill_lab/static/text/predict_cost.h5')
            scaler_cost = joblib.load('/home/sachin/Desktop/skill_lab/static/text/scaler_cost.save')

            df = pd.DataFrame(columns=PC_data_columns)
            df.loc[0] = [0] * (len(PC_data_columns))

            # Inputs
            for cuisine in cuisine_inputs:          # cuisine_list is list of cuisines taken from user
                cuisine_index = cuisines_list.index(cuisine) + 1
                df['cuisine_'+str(cuisine_index)] = 1

            for highlight in highlight_inputs:          # highlight_list is list of highlights taken from user
                highlight_index = highlights_list.index(highlight) + 1
                df['highlight_'+str(highlight_index)] = 1

            df['establishment'] = establishment_list.index(
                establishment) - 1        # establishment is taken from user

            df['locality_verbose'] = locality_list.index(
                locality+';')         # locality is taken from user

            # start time is taken from user --> TODO: convert input to int (Ex: 08:30 to 830)
            df['start'] = start
            # end time is taken from user --> TODO: convert input to int (Ex: 08:30 to 830)
            df['end'] = end

            df['delivery'] = delivery       # delivery value taken from user  (-1 or 1)

            df['aggregate_rating'] = rating_cost     # rating taken from user

            
            df = scaler_cost.transform(df)
            
            result=predict_cost.predict(df)[0]


    # ---------------------------------------------------------------------------------------
    # To predict Rating:
        if call==1:
            predict_rating = load_model('/home/sachin/Desktop/skill_lab/static/text/predict_rating.h5')
            scaler_rating = joblib.load('/home/sachin/Desktop/skill_lab/static/text/scaler_rating.save')

            df = pd.DataFrame(columns=PR_data_columns)
            df.loc[0] = [0] * (len(PR_data_columns))

            # Inputs
            for cuisine in cuisine_inputs:          # cuisine_list is list of cuisines taken from user
                cuisine_index = cuisines_list.index(cuisine) + 1
                df['cuisine_'+str(cuisine_index)] = 1

            for highlight in highlight_inputs:          # highlight_list is list of highlights taken from user
                highlight_index = highlights_list.index(highlight) + 1
                df['highlight_'+str(highlight_index)] = 1

            df['establishment'] = establishment_list.index(
                establishment) - 1        # establishment is taken from user

            df['locality_verbose'] = locality_list.index(
                locality+';')         # locality is taken from user

            # start time is taken from user --> TODO: convert input to int (Ex: 08:30 to 830)
            df['start'] = start
            # end time is taken from user --> TODO: convert input to int (Ex: 08:30 to 830)
            df['end'] = end

            df['delivery'] = delivery       # delivery value taken from user  (-1 or 1)

            df['average_cost_for_two'] = rating_cost     # cost taken from user

            df = scaler_rating.transform(df)
            result=predict_rating.predict(df)[0]
    return result    