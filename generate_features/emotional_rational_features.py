from operator import contains
import numpy as np
from generate_features.features_functions import *
from generate_features.common_columns_lists import *

'''
REM : List of features :

pr_TENENG_SOURCE_RATIO
pr_SOCIAL_SOURCE_RATIO
pr_SE_SOURCE_RATIO
pr_SOURCE_MEDIUM_FB_RATIO
pr_SOURCE_MEDIUM_CPC_RATIO
pr_SOURCE_MEDIUM_ORGANIC_RATIO
#
pr_AVG_VIEW_PRD                             : hits.eCommerceAction.action_type = 2
pr_AVG_PRODUCTS_IN_SESSION  
pr_AVG_AVG_TIMETOHIT                        : hits.deltaTimeMS
pr_AVG_TIME_ADD_PRD                          
pr_AVG_PAYMENT_PAGE                         : hits.contentGroup.contentGroup1   
pr_AVG_DROPDOWN_CLICK                       : hits.contentGroup.contentGroup1    
pr_AVG_SUPPORT_PAGE                         : hits.contentGroup.contentGroup1    
pr_AVG_FEEDBACK_PAGE                        : hits.contentGroup.contentGroup1    
pr_AVG_SHOPPING_CART                        : hits.contentGroup.contentGroup1    
pr_AVG_DROP_FILTER_CLICK                    : hits.contentGroup.contentGroup1    
pr_AVG_CNT_SEARCHKEYWORD                    : hits.contentGroup.contentGroup1    
#
pr_weekend_ratio                            : Sat-Sun ratio   
pr_endmonth_ratio                           : end of month 15-30 in the month 
pr_HOUR_CAT1_ratio                          : night time 20:00 to 04:00

'''
