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
def emo_ratio_single_session_tl_features(df_tl, session_time, numeric_cols):
    df_tl['visitStartTime'] = convert_to_datetime(df_tl, 'visitStartTime')
    df_tl = convert_multiple_columns_to_numeric(df_tl, cols=numeric_cols)

    # create tl feature df
    df = pd.DataFrame()
    df['trafficSourceRatio'] = 1 if df_tl['trafficSource.source'][0] in traffic_source_values else 0
    df['trafficSourceSocialRatio'] = 1 if df_tl['trafficSource.source'].str.contains(social_source_values, case=False, regex = False)[0] else 0
    df['trafficSourceSeRatio'] = 1 if df_tl['trafficSource.source'].str.contains(se_source_values, case=False)[0] else 0
    df['mediumSourceFbRatio'] = 1 if df_tl['trafficSource.medium'].str.contains(medium_fb_values, case=False)[0] else 0
    df['mediumSourceCpcRatio'] = 1 if df_tl['trafficSource.medium'].str.contains('cpc', case=False)[0] else 0
    df['mediumSourceOrganicRatio'] =  1 if df_tl['trafficSource.source'][0] in organic_source_values else 0
    df['avg_hits'] = df_tl['totals.hits'] if 'totals.hits' in df_tl.columns.to_list() else 0
    df['avg_page_views'] = df_tl['totals.pageviews'] if 'totals.pageviews' in df_tl.columns.to_list() else 0
    df['avg_time_on_site'] = session_time 
    df['end_of_month_ratio'] = 1 if df_tl['visitStartTime'].dt.day[0] > 15 else 0
    return df_tl['fullVisitorId'][0], df.fillna(0)



def emo_ratio_single_session_hit_features(df_hit, numeric_cols):
    df_hit['visitStartTime'] = convert_to_datetime(df_hit, 'visitStartTime')
    df_hit = convert_multiple_columns_to_numeric(df_hit, cols=numeric_cols)

    # create hits feature df
    df = pd.DataFrame()
    df['products_per_session'] = pd.Series(np.mean(df_hit['numOfProducts']))
    df['avg_viewd_product'] = pd.Series(len(df_hit[df_hit['hits.eCommerceAction.action_type'].isin([2])]))
    df['avg_time2hit'] = pd.Series(np.mean(df_hit['hits.deltaTimeMS']))
    df['avg_time_add_prod'] = pd.Series(df_hit[df_hit['hits.eCommerceAction.action_type'].isin([2])]['hits.time'].agg('mean'))
    df['avg_time_rmv_prod'] = pd.Series(df_hit[df_hit['hits.eCommerceAction.action_type'].isin([3])]['hits.time'].agg('mean'))
    df['support_page'] = pd.Series(df_hit.loc[df_hit['hits.contentGroup.contentGroup1'] == 'Support Page']['hits.contentGroup.contentGroup1'].agg('count'))
    df['article_page'] = pd.Series(df_hit.loc[df_hit['hits.contentGroup.contentGroup1'] == 'Article Page']['hits.contentGroup.contentGroup1'].agg('count'))
    df['search_keyword'] = pd.Series(df_hit.loc[df_hit['hits.contentGroup.contentGroup1'] == 'Thank you Page']['hits.contentGroup.contentGroup1'].agg('count'))
    df['product_page'] = pd.Series(df_hit.loc[df_hit['hits.contentGroup.contentGroup1'] == 'Product Page']['hits.contentGroup.contentGroup1'].agg('count'))
    df['category_page'] = pd.Series(df_hit.loc[df_hit['hits.contentGroup.contentGroup1'] == 'Category Page']['hits.contentGroup.contentGroup1'].agg('count'))
    return df.fillna(0)



def emotional_rational_hits_features(df_hits):
    # AVG_PRODUCTS_IN_SESSION
    df0 = df_group_by_mul_col(df_hits, 'numOfProducts', ['fullVisitorId', 'visitStartTime'], 'sum').reset_index(level=1)
    df1 = df_by_group_by_single_column(df0, 'fullVisitorId', 'numOfProducts' , 'mean')
    df =  df1['numOfProducts'].to_frame('hits.products_per_session')
    # AVG_VIEW_PRD
    df0 = df_filter_and_group_by_mul_col(df_hits, 'hits.eCommerceAction.action_type', [2], ['fullVisitorId', 'visitStartTime'], 'count').reset_index(level=1)
    df1 = df_by_group_by_single_column(df0, 'fullVisitorId', 'hits.eCommerceAction.action_type', 'mean')
    df['hits.avg_viewd_product'] = df1['hits.eCommerceAction.action_type']
    # AVG_AVG_TIMETOHIT
    df0 = df_group_by_mul_col(df_hits, 'hits.deltaTimeMS', ['fullVisitorId', 'visitStartTime'], 'mean').reset_index(level=1)
    df1 = df_by_group_by_single_column(df0, 'fullVisitorId', 'hits.deltaTimeMS', 'mean')
    df['hits.avg_time2hit'] = df1['hits.deltaTimeMS']
    # AVG_TIME_ADD_PRD / RMV_PRD
    df0 = df_filter_and_agg_by_diff_col(df_hits, 'hits.eCommerceAction.action_type', [3], ['fullVisitorId', 'visitStartTime'], 'hits.time', 'mean').reset_index(level=1)
    df1 = df_by_group_by_single_column(df0, 'fullVisitorId', 'hits.time', 'mean')
    df['hits.avg_time_add_prod'] = df1['hits.time']
    #
    df0 = df_filter_and_agg_by_diff_col(df_hits, 'hits.eCommerceAction.action_type', [4], ['fullVisitorId', 'visitStartTime'], 'hits.time', 'mean').reset_index(level=1)
    df1 = df_by_group_by_single_column(df0, 'fullVisitorId', 'hits.time', 'mean')
    df['hits.avg_time_rmv_prod'] = df1['hits.time']
    
    # 
    df0 = df_hits.groupby(['fullVisitorId', 'hits.contentGroup.contentGroup1'])['hits.contentGroup.contentGroup1'].agg('count').to_frame('contentGroupCount').reset_index(level=1)
    # SUPPORT_PAGE
    df1 = df0.loc[df0['hits.contentGroup.contentGroup1'] ==  'Support Page']
    df['hits.support_page'] = df1['contentGroupCount']
    #  Article_PAGE
    df1 = df0.loc[df0['hits.contentGroup.contentGroup1'] ==  'Article Page']
    df['hits.article_page'] = df1['contentGroupCount']
    # Thank you page
    df1 = df0.loc[df0['hits.contentGroup.contentGroup1'] ==  'Thank you Page']
    df['hits.search_keyword'] = df1['contentGroupCount']
    # product page
    df1 = df0.loc[df0['hits.contentGroup.contentGroup1'] ==  'Product Page']
    df['hits.product_page'] = df1['contentGroupCount']
     # Category Page
    df1 = df0.loc[df0['hits.contentGroup.contentGroup1'] ==  'Category Page']
    df['hits.category_page'] = df1['contentGroupCount']

    return df



def emotional_rational_toplvl_features(df_top_lvl):
    # tenen source ratio :
    sr = df_top_lvl.groupby('fullVisitorId').apply(lambda x : filter_in_columns_func(x, 'trafficSource.source', len, traffic_source_values))
    df = sr.to_frame('trafficSourceRatio')
    # social source ratio :
    sr= df_top_lvl.groupby('fullVisitorId').apply(lambda x : filter_str_columns_func(x, 'trafficSource.source', len, social_source_values))
    df['trafficSourceSocialRatio'] = sr
    # se source ratio :
    sr = df_top_lvl.groupby('fullVisitorId').apply(lambda x: filter_str_columns_func(x, 'trafficSource.source', len, se_source_values))
    df['trafficSourceSeRatio'] = sr
    # SOURCE_MEDIUM_FB_RATIO
    sr= df_top_lvl.groupby('fullVisitorId').apply(lambda x : filter_str_columns_func(x, 'trafficSource.medium', len, medium_fb_values))
    df['mediumSourceFbRatio'] = sr
    # SOURCE_MEDIUM_CPC_RATIO
    sr = df_top_lvl.groupby('fullVisitorId').apply(lambda x: filter_str_columns_func(x, 'trafficSource.medium', len, 'cpc'))
    df['mediumSourceCpcRatio'] = sr
    # SOURCE_MEDIUM_ORGANIC_RATIO
    sr = df_top_lvl.groupby('fullVisitorId').apply(lambda x: filter_in_columns_func(x, 'trafficSource.medium', len, organic_source_values))
    df['mediumSourceOrganicRatio'] = sr
    # MEAN FOR TOTALS VIEWS
    df0 = df_by_group_by_single_column(df_top_lvl, 'fullVisitorId', 'totals.hits', 'mean')
    df['avg_hits'] = df0['totals.hits']
    #
    df0 = df_by_group_by_single_column(df_top_lvl, 'fullVisitorId', 'totals.pageviews', 'mean')
    df['avg_page_views'] = df0['totals.pageviews']
    #
    df0 = df_by_group_by_single_column(df_top_lvl, 'fullVisitorId', 'totals.timeOnSite', 'mean') 
    df['avg_time_on_site'] = df0['totals.timeOnSite']
    # end of month ratio
    sr = group_by_start_or_end_of_month(df_top_lvl, 'visitStartTime', 'fullVisitorId', 'clientId', 'SM')
    df['end_of_month_ratio'] = sr
    
    return df