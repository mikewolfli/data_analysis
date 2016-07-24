#!/usr/bin/python3
#-*- coding:utf-8 -*-
'''
Created on 2016年7月21日

@author: mikewolfli
'''

tree_items=['数据同步','历史数据','走势图','数据分析']

#历史行情-表头对照
his_data_para_dic={
              'code': '股票代码', #即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
              'start': '开始日期', #格式YYYY-MM-DD
              'end': '结束日期', #格式YYYY-MM-DD
              'ktype': '数据类型', #D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
              'retry_count':'当网络异常后重试次数', #默认为3
              'pause': '重试时停顿秒数',# 默认为0
              }

his_data_dic = {
                       'date': '日期',
                       'open':'开盘价',
                       'high':'最高价',
                       'close':'收盘价',
                       'low':'最低价',
                       'volume':'成交量',
                       'price_change':'价格变动',
                       'p_change':'涨跌幅',
                       'ma5':'5日均价',
                       'ma10':'10日均价',
                       'ma20':'20日均价',
                       'v_ma5':'5日均量',
                       'v_ma10':'10日均量',
                       'v_ma20':'20日均量',
                       'turnover':'换手率',#[注:指数无此项]
                       }

#复权数据
h_data_para_dic = {
                   'code':'股票代码',# string, e.g. 600848
                   'start':'开始日期',# string, format:YYYY-MM-DD 为空时取当前日期
                   'end':'结束日期', #string, format:YYYY-MM-DD 为空时取去年今日
                   'autype':'复权类型',#string,，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
                   'index':'是否是大盘指数',#Boolean，，默认为False
                   'retry_count':'如遇网络等问题重复执行的次数',# int, 默认3,
                   'pause':'重复请求数据过程中暂停的秒数',#int, 默认 0,，防止请求间隔时间太短出现的问题
                   }

h_data_dic = {
              'date':'交易日期',# (index)
              'open':'开盘价',
              'high':'最高价',
              'close':'收盘价',
              'low':'最低价',
              'volume':'成交量',
              'amount':'成交金额',
              }

#实时行情 一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
real_price_all_dic = {
                      'code':'代码',
                      'name':'名称',
                      'changepercent':'涨跌幅',
                      'trade':'现价',
                      'open':'开盘价',
                      'high':'最高价',
                      'low':'最低价',
                      'settlement':'昨日收盘价',
                      'volume':'成交量',
                      'turnoverratio':'换手率',
              }

'''
历史分笔
获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取。
'''
tick_data_para_dic = {
                      'code':'股票代码',#即6位数字代码
                      'date':'日期',#格式YYYY-MM-DD
                      'retry_count':'重复次数',#int, 默认3,如遇网络等问题重复执行的次数
                      'pause':'暂停的秒数', #int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
                      }

tick_data_dic = {
                 'time':'时间',
                 'price':'成交价格',
                 'change':'价格变动',
                 'volume':'成交手',
                 'amount':'成交金额(元)',
                 'type':'买卖类型',#【买盘、卖盘、中性盘】
                 
                 }

'''
实时分笔
获取实时分笔数据，可以实时取得股票当前报价和成交信息，其中一种场景是，写一个python定时程序来调用本接口（可两三秒执行一次，性能与行情软件基本一致），然后通过DataFrame的矩阵计算实现交易监控，可实时监测交易量和价格的变化。
请求多个股票方法（一次最好不要超过30个）：
'''
realtime_quotes_para_dic = { 'symbols':'股票代码'}#6位数字股票代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板） 可输入的类型：str、list、set或者pandas的Series对象


realtime_quotes_dic = {'name':'股票名字',
                       'open':'今日开盘价',
                       'pre_close':'昨日收盘价',
                       'price':'当前价格',
                       'high':'今日最高价',
                       'low':'今日最低价',
                       'bid':'竞买价', #即“买一”报价
                       'ask':'竞卖价', #即“卖一”报价
                       'volume':'成交量',# maybe you need do volume/100
                       'amount':'成交金额', #（元 CNY）
                       'b&_v':'委买笔数',#委买一（笔数 bid volume）
                       'b&_p':'委买价格',  #（价格 bid price）
                       'a&_v':'委卖笔数',#委卖一（笔数 ask volume）
                       'a&_p':'委卖价格',#委卖一（价格 ask price）
                       'date':'日期',
                       'time':'时间',                       
                       
                       }

'''
当日历史分笔
获取当前交易日（交易进行中使用）已经产生的分笔明细数据。
'''
today_ticks_para_dic = {
                   'code':'股票代码', #即6位数字代码
                   'retry_count':'重复执行的次数',#int, 默认3,如遇网络等问题重复执行的次数
                   'pause':'暂停的秒数',# int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题                  
                   }

today_ticks_dic = {
                   'time':'时间',
                   'price':'当前价格',
                   'pchange':'涨跌幅',
                   'change':'价格变动',
                   'volume':'成交手',
                   'amount':'成交金额(元)',
                   'type':'买卖类型' #【买盘、卖盘、中性盘】                  
                   }


#大盘指数实时行情列表-表头对照
index_dic={
             'code':'指数代码',
             'name':'指数名称',
             'change':'涨跌幅',
             'open':'开盘点位',
             'preclose':'昨日收盘点位',
             'close':'收盘点位',
             'high':'最高点位',
             'low':'最低点位',
             'volume':'成交量(手)',
             'amount':'成交金额（亿元）',
             }

'''
大单交易数据¶
获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。
'''
sina_dd_para_dic = {
                    'code':'股票代码',#即6位数字代码
                    'date':'日期',#格式YYYY-MM-DD
                    'vol':'手数',#默认为400手，输入数值型参数
                    'retry_count':'重复执行的次数',#int, 默认3,如遇网络等问题重复执行的次数
                    'pause':'暂停的秒数',# int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
               }

sina_dd_dic={
             'code':'代码',
             'name':'名称',
             'time':'时间',
             'price':'当前价格',
             'volume':'成交手',
             'preprice':'上一笔价格',
             'type':'买卖类型' #【买盘、卖盘、中性盘】             
             }

'''
分配预案
每到季报、年报公布的时段，就经常会有上市公司利润分配预案发布，而一些高送转高分红的股票往往会成为市场炒作的热点。及时获取和统计高送转预案的股票是参与热点炒作的关键，TuShare提供了简洁的接口，能返回股票的送转和分红预案情况。
'''
profit_data_para_dic = {
                        'year':'年份',#预案公布的年份，默认为2014
                        'top':'取最新n条数据',#默认取最近公布的25条
                        'retry_count':'重试次数', #当网络异常后重试次数，默认为3
                        'pause':'停顿秒数',#重试时停顿秒数，默认为0
                        }

profit_data_dic = {
                   'code':'股票代码',
                   'name':'股票名称',
                   'year':'分配年份',
                   'report_date':'公布日期',
                   'divi':'分红金额（每10股）',
                   'shares':'转增和送股数（每10股）',                   
                   }

'''
业绩预告
按年度、季度获取业绩预告数据，接口提供从1998年以后每年的业绩预告数据，需指定年度、季度两个参数。数据在获取的过程中，会打印进度信息(下同)。
'''
forecast_data_para_dic = {
                          'year':'年度',#int 年度 e.g:2014
                          'quarter':'季度',#int 季度 :1、2、3、4，只能输入这4个季度                         
                          }

forecast_data_dic = {
                     'code':'代码',
                     'name':'名称',
                     'type':'业绩变动类型',#【预增、预亏等】
                     'report_date':'发布日期',
                     'pre_eps':'上年同期每股收益',
                     'range':'业绩变动范围',                    
                     }
'''
限售股解禁
以月的形式返回限售股解禁情况，通过了解解禁股本的大小，判断股票上行的压力。可通过设定年份和月份参数获取不同时段的数据。
'''
xsg_data_para_dic = {
                     'year':'年份',# 年份,默认为当前年
                     'month':'解禁月份',#默认为当前月
                     'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                     'pause':'停顿秒数',#重试时停顿秒数，默认为0                    
                     }

xsg_data_dic = {
                'code':'股票代码',
                'name':'股票名称',
                'date':'解禁日期',
                'count':'解禁数量（万股）',
                'ratio':'占总盘比率',
                }

'''
基金持股
获取每个季度基金持有上市公司股票的数据。
'''
fund_holdings_para_dic= {
                         'year':'年份',#默认为当前年
                         'quarter':'季度',#（只能输入1，2，3，4这个四个数字）
                         'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                         'pause':'停顿秒数',#重试时停顿秒数，默认为0                        
                         }

fund_holdings_dic = {
                     'code':'股票代码',
                     'name':'股票名称',
                     'date':'报告日期',
                     'nums':'基金家数',
                     'nlast':'与上期相比',#（增加或减少了）
                     'count':'基金持股数（万股）',
                     'clast':'与上期相比',
                     'amount':'基金持股市值',
                     'ratio':'占流通盘比率',                    
                     }

'''
新股数据
获取IPO发行和上市的时间列表，包括发行数量、网上发行数量、发行价格已经中签率信息等。
'''
new_stocks_para_dic={
                     'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                     'pause':'停顿秒数',#重试时停顿秒数，默认为0                    
                     }

new_stocks_dic = {
                  'code':'股票代码',
                  'name':'股票名称',
                  'ipo_date':'上网发行日期',
                  'issue_date':'上市日期',
                  'amount':'发行数量(万股)',
                  'markets':'上网发行数量(万股)',
                  'price':'发行价格(元)',
                  'pe':'发行市盈率',
                  'limit':'个人申购上限(万股)',
                  'funds':'募集资金(亿元)',
                  'ballot':'网上中签率(%)',
                  }

'''
融资融券（沪市）
沪市的融资融券数据从上海证券交易所网站直接获取，提供了有记录以来的全部汇总和明细数据。根据上交所网站提示：数据根据券商申报的数据汇总，由券商保证数据的真实、完整、准确。

本日融资融券余额＝本日融资余额＋本日融券余量金额
本日融资余额＝前日融资余额＋本日融资买入额－本日融资偿还额；
本日融资偿还额＝本日直接还款额＋本日卖券还款额＋本日融资强制平仓额＋本日融资正权益调整－本日融资负权益调整；
本日融券余量=前日融券余量+本日融券卖出数量-本日融券偿还量；
本日融券偿还量＝本日买券还券量＋本日直接还券量＋本日融券强制平仓量＋本日融券正权益调整－本日融券负权益调整－本日余券应划转量；
融券单位：股（标的证券为股票）/份（标的证券为基金）/手（标的证券为债券）。
明细信息中仅包含当前融资融券标的证券的相关数据，汇总信息中包含被调出标的证券范围的证券的余额余量相关数据。
'''
#沪市融资融券汇总数据

sh_margins_para_dic = {
                       'start':'开始日期',# format：YYYY-MM-DD 为空时取去年今日
                       'end':'结束日期',# format：YYYY-MM-DD 为空时取当前日期
                       'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                       'pause':'停顿秒数',#重试时停顿秒数，默认为0                       
                       }
sh_margins_dic = {
                  'opDate':'信用交易日期',
                  'rzye':'本日融资余额(元)',
                  'rzmre':'本日融资买入额(元)',
                  'rqyl':'本日融券余量',
                  'rqylje':'本日融券余量金额(元)',
                  'rqmcl':'本日融券卖出量',
                  'rzrqjyzl':'本日融资融券余额(元)'                 
                  }

#沪市融资融券明细数据
sh_margin_details_para_dic = {
                              'date':'日期',# format：YYYY-MM-DD 默认为空’‘,数据返回最近交易日明细数据
                              'symbol':'标的代码',#6位数字e.g.600848，默认为空’‘
                              'start':'开始日期',# format：YYYY-MM-DD 默认为空’‘
                              'end':'结束日期',# format：YYYY-MM-DD 默认为空’‘
                              'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                              'pause':'停顿秒数',#重试时停顿秒数，默认为0                             
                              }

sh_margin_details_dic = {
                         'opDate':'信用交易日期',
                         'stockCode':'标的证券代码',
                         'securityAbbr':'标的证券简称',
                         'rzye':'本日融资余额(元)',
                         'rzmre':'本日融资买入额(元)',
                         'rzche':'本日融资偿还额(元)',
                         'rqyl':'本日融券余量',
                         'rqmcl':'本日融券卖出量',
                         'rqchl':'本日融券偿还量',                     
                         }
'''
融资融券（深市）
深市的融资融券数据从深圳证券交易所网站直接获取，提供了有记录以来的全部汇总和明细数据。在深交所的网站上，对于融资融券的说明如下：

说明：

本报表基于证券公司报送的融资融券余额数据汇总生成，其中：

本日融资余额(元)=前日融资余额＋本日融资买入-本日融资偿还额
本日融券余量(股)=前日融券余量＋本日融券卖出量-本日融券买入量-本日现券偿还量
本日融券余额(元)=本日融券余量×本日收盘价
本日融资融券余额(元)=本日融资余额＋本日融券余额；
2014年9月22日起，“融资融券交易总量”数据包含调出标的证券名单的证券的融资融券余额。
'''
#深市融资融券汇总数据
sz_margins_para_dic ={
                      'start':'开始日期',# format：YYYY-MM-DD 为空时取去年今日
                      'end':'结束日期',# format：YYYY-MM-DD 为空时取当前日期
                      'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                      'pause':'停顿秒数',#重试时停顿秒数，默认为0                     
                      }

sz_margins_dic ={
                 'opDate':'信用交易日期(index)',
                 'rzmre':'融资买入额(元)',
                 'rzye':'融资余额(元)',
                 'rqmcl':'融券卖出量',
                 'rqyl':'融券余量',
                 'rqye':'融券余量(元)',
                 'rzrqye':'融资融券余额(元)',
                                 
                 }
#深市融资融券明细数据
sz_margin_details_para_dic = {
                              'date':'日期',# format：YYYY-MM-DD 默认为空’‘,数据返回最近交易日明细数据
                              'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                              'pause':'停顿秒数',# 重试时停顿秒数，默认为0                              
                              }

sz_margin_details_dic = {
                         'stockCode':'标的证券代码',
                         'securityAbbr':'标的证券简称',
                         'rzmre':'融资买入额(元)',
                         'rzye':'融资余额(元)',
                         'rqmcl':'融券卖出量',
                         'rqyl':'融券余量',
                         'rqye':'融券余量(元)',
                         'rzrqye':'融资融券余额(元)',
                         'opDate':'信用交易日期',                    
                     }

'''
行业分类
'''
industry_classified_dic={
                         'code':'股票代码',
                         'name':'股票名称',
                         'c_name':'行业名称',
                         }
'''
概念分类
'''
concept_classified_dic  = {
                           'code':'股票代码',
                           'name':'股票名称',
                           'c_name':'概念名称',
}

'''
地域分类
'''
area_classified_dic = {
                       'code':'股票代码',
                       'name':'股票名称',
                       'area':'地域名称',                    
                       }

'''
中小板分类¶
获取中小板股票数据，即查找所有002开头的股票

创业板分类
获取创业板股票数据，即查找所有300开头的股票

风险警示板分类¶
获取风险警示板股票数据，即查找所有st股票

上证50成份股
获取上证50成份股

中证500成份股
获取中证500成份股
'''
five_classified_dic = {
                      'code':'股票代码',
                      'name':'股票名称',                     
                      }

'''
沪深300成份及权重
获取沪深300当前成份股及所占权重
'''
hs300s_dic={
            'code':'股票代码',
            'name':'股票名称',
            'date':'日期',
            'weight':'权重',           
            }

'''
终止上市股票列表
获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。
'''
terminated_dic = {
                  'code':'股票代码',
                  'name':'股票名称',
                  'oDate':'上市日期',
                  'tDate':'终止上市日期',                 
                  }

#基本面数据
'''
股票列表
'''
stoc_basics_dic = {
                   'code':'代码',
                   'name':'名称',
                   'industry':'所属行业',
                   'area':'地区',
                   'pe':'市盈率',
                   'outstanding':'流通股本',
                   'totals':'总股本(万)',
                   'totalAssets':'总资产(万)',
                   'liquidAssets':'流动资产',
                   'fixedAssets':'固定资产',
                   'reserved':'公积金',
                   'reservedPerShare':'每股公积金',
                   'eps':'每股收益',
                   'bvps':'每股净资',
                   'pb':'市净率',
                   'timeToMarket':'市日期',                  
                   }

'''
业绩报告（主表）
'''
report_data_dic = {
                   'code':'代码',
                   'name':'名称',
                   'eps':'每股收益',
                   'eps_yoy':'每股收益同比(%)',
                   'bvps':'每股净资产',
                   'roe':'净资产收益率(%)',
                   'epcf':'每股现金流量(元)',
                   'net_profits':'净利润(万元)',
                   'profits_yoy':'净利润同比(%)',
                   'distrib':'分配方案',
                   'report_date':'发布日期',                  
                   }

'''
盈利能力
'''
profit_data_dic = {
                   'code':'代码',
                   'name':'名称',
                   'roe':'净资产收益率(%)',
                   'net_profit_ratio':'净利率(%)',
                   'gross_profit_rate':'毛利率(%)',
                   'net_profits':'净利润(万元)',
                   'eps':'每股收益',
                   'business_income':'营业收入(百万元)',
                   'bips':'每股主营业务收入(元)',                   
                   }

'''
营运能力
'''
operation_data_dic = {
                      'code':'代码',
                      'name':'名称',
                      'arturnover':'应收账款周转率(次)',
                      'arturndays':'应收账款周转天数(天)',
                      'inventory_turnover':'存货周转率(次)',
                      'inventory_days':'存货周转天数(天)',
                      'currentasset_turnover':'流动资产周转率(次)',
                      'currentasset_days':'流动资产周转天数(天) ',                    
                      }

'''
成长能力
'''
growth_data_dic = {
                   'code':'代码',
                   'name':'名称',
                   'mbrg':'主营业务收入增长率(%)',
                   'nprg':'净利润增长率(%)',
                   'nav':'净资产增长率',
                   'targ':'总资产增长率',
                   'epsg':'每股收益增长率',
                   'seg':'股东权益增长率',                  
                   }

'''
偿债能力
'''
debpaying_data_dic = {
                      'code':'代码',
                      'name':'名称',
                      'currentratio':'流动比率',
                      'quickratio':'速动比率',
                      'cashratio':'现金比率',
                      'icratio':'利息支付倍数',
                      'sheqratio':'股东权益比率',
                      'adratio':'股东权益增长率',                     
                      }

'''
现金流量
'''
cashflow_data_dic = {
                     'code':'代码',
                     'name':'名称',
                     'cf_sales':'经营现金净流量对销售收入比率',
                     'rateofreturn':'资产的经营现金流量回报率',
                     'cf_nm':'经营现金净流量与净利润的比率',
                     'cf_liabilities':'经营现金净流量对负债比率',
                     'cashflowratio':'现金流量比率',                    
                     }

#宏观经济数据
'''
存款利率
------
import tushare as ts
ts.get_deposit_rate()
'''
deposit_rate_dic = {
                    'date':'变动日期',
                    'deposit_type':'存款种类',
                    'rate':'利率（%）',                   
                    }

'''
贷款利率
-------
import tushare as ts
ts.get_loan_rate()
'''
loan_rate_dic = {
                 'date':'执行日期',
                 'loan_type':'存款种类',
                 'rate':'利率（%）',                 
                 }

'''
存款准备金率
-----

import tushare as ts

ts.get_rrr()
'''
rrr_dic = {
           'date':'变动日期',
           'before':'调整前存款准备金率(%)',
           'now':'调整后存款准备金率(%)',
           'changed':'调整幅度(%)',
           }

'''
货币供应量
-------
import tushare as ts
ts.get_money_supply()
'''
money_supply_dic = {
                    'month':'统计时间',
                    'm2':'货币和准货币（广义货币M2）(亿元)',
                    'm2_yoy':'货币和准货币（广义货币M2）同比增长(%)',
                    'm1':'货币(狭义货币M1)(亿元)',
                    'm1_yoy':'货币(狭义货币M1)同比增长(%)',
                    'm0':'流通中现金(M0)(亿元)',
                    'm0_yoy':'流通中现金(M0)同比增长(%)',
                    'cd':'活期存款(亿元)',
                    'cd_yoy':'活期存款同比增长(%)',
                    'qm':'准货币(亿元)',
                    'qm_yoy':'准货币同比增长(%)',
                    'ftd':'定期存款(亿元)',
                    'ftd_yoy':'定期存款同比增长(%)',
                    'sd':'储蓄存款(亿元)',
                    'sd_yoy':'储蓄存款同比增长(%)',
                    'rests':'其他存款(亿元)',
                    'rests_yoy':'其他存款同比增长(%)',                   
                    }

'''
货币供应量(年底余额)
--------
import tushare as ts
ts.get_money_supply_bal()
'''
money_suppliy_bal_dic = {
                         'year':'统计年度',
                         'm2':'货币和准货币(亿元)',
                         'm1':'货币(亿元)',
                         'm0':'流通中现金(亿元)',
                         'cd':'活期存款(亿元)',
                         'qm':'准货币(亿元)',
                         'ftd':'定期存款(亿元)',
                         'sd':'储蓄存款(亿元)',
                         'rests':'其他存款(亿元)',                        
                         }

'''
国内生产总值(年度)
------
import tushare as ts
ts.get_gdp_year()
'''
gdp_year_dic={
              'year':'统计年度',
              'gdp':'国内生产总值(亿元)',
              'pc_gdp':'人均国内生产总值(元)',
              'gnp':'国民生产总值(亿元)',
              'pi':'第一产业(亿元)',
              'si':'第二产业(亿元)',
              'industry':'工业(亿元)',
              'cons_industry':'建筑业(亿元)',
              'ti':'第三产业(亿元)',
              'trans_industry':'交通运输仓储邮电通信业(亿元)',
              'lbdy':'批发零售贸易及餐饮业(亿元)',
              }
'''
国内生产总值(季度)¶
--------
import tushare as ts
ts.get_gdp_quarter()
'''
gdp_quarter_dic = {
                   'quarter':'季度',
                   'gdp':'国内生产总值(亿元)',
                   'gdp_yoy':'国内生产总值同比增长(%)',
                   'pi':'第一产业增加值(亿元)',
                   'pi_yoy':'第一产业增加值同比增长(%)',
                   'si':'第二产业增加值(亿元)',
                   'si_yoy':'第二产业增加值同比增长(%)',
                   'ti':'第三产业增加值(亿元)',
                   'ti_yoy':'第三产业增加值同比增长(%)',                  
                   }

'''
三大需求对GDP贡献
-----------
import tushare as ts
ts.get_gdp_for()
'''
gdp_for_dic = {
               'year':'统计年度',
               'end_for':'最终消费支出贡献率(%)',
               'for_rate':'最终消费支出拉动(百分点)',
               'asset_for' :'资本形成总额贡献率(%)',
               'asset_rate':'资本形成总额拉动(百分点)',
               'goods_for' :'货物和服务净出口贡献率(%)',
               'goods_rate':'货物和服务净出口拉动(百分点)',              
               }

'''
三大产业对GDP拉动
-----------
import tushare as ts
ts.get_gdp_pull()
'''
gdp_pull_dic = {
                'year':'统计年度',
                'gdp_yoy':'国内生产总值同比增长(%)',
                'pi':'第一产业拉动率(%)',
                'si' :'第二产业拉动率(%)',
                'industry':'其中工业拉动(%)',
                'ti' :'第三产业拉动率(%)',                
                }

'''
三大产业贡献率
------------
import tushare as ts
ts.get_gdp_contrib()
'''
gdp_contrib_dic = {
                   'year':'统计年度',
                   'gdp_yoy':'国内生产总值',
                   'pi':'第一产业献率(%)',
                   'si':'第二产业献率(%)',
                   'industry':'其中工业献率(%)',
                   'ti':'第三产业献率(%)',                  
                   }

'''
居民消费价格指数
---------
import tushare as ts
ts.get_cpi()
'''
cpi_dic = {
           'month':'统计月份',
           'cpi':'价格指数',
           }

'''
工业品出厂价格指数
------------
import tushare as ts
ts.get_ppi()
'''
ppi_dic = {
           'month':'统计月份',
           'ppiip':'工业品出厂价格指数',
           'ppi' :'生产资料价格指数',
           'qm':'采掘工业价格指数',
           'rmi':'原材料工业价格指数',
           'pi':'加工工业价格指数',
           'cg':'生活资料价格指数',
           'food':'食品类价格指数',
           'clothing':'衣着类价格指数',
           'roeu':'一般日用品价格指数',
           'dcg':'耐用消费品价格指数',         
           }



#新闻事件数据
'''
即时新闻
获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。数据更新较快，使用过程中可用定时任务来获取。
---------------------
import tushare as ts
ts.get_latest_news() #默认获取最近80条新闻数据，只提供新闻类型、链接和标题
ts.get_latest_news(top=5,show_content=True) #显示最新5条新闻，并打印出新闻内容
'''
latest_news_para_dic = {
                        'top':'最新消息的条数',#int，显示最新消息的条数，默认为80条
                        'show_content':'是否显示新闻内容',# boolean,是否显示新闻内容，默认False
                        }

latest_news_dic = {
                   'classify':'新闻类别',
                   'title':'新闻标题',
                   'time':'发布时间',
                   'url':'新闻链接',
                   'content':'新闻内容',#（在show_content为True的情况下出现）                  
                   }

'''
信息地雷
----
import tushare as ts

ts.get_notices()
'''
notices_para_dic = {
                    'code':'股票代码',
                    'date':'信息公布日期',
                    }

notices_dic = {
               'title':'信息标题',
               'type':'信息类型',
               'date':'公告日期',
               'url':'信息内容URL',              
               }

'''
新浪股吧
获取sina财经股吧首页的重点消息。股吧数据目前获取大概17条重点数据，可根据参数设置是否显示消息内容，默认情况是不显示。
-------
import tushare as ts
ts.guba_sina()
'''
guba_sina_para_dic = {
                      'show_content':'是否显示内容',#boolean,是否显示内容，默认False
                      }

guba_sina_dic = {
                 'title':'消息标题',
                 'content':'消息内容',#（show_content=True的情况下）
                 'ptime':'发布时间',
                 'rcounts':'阅读次数',                
                 }

#龙虎榜数据
'''
每t日龙虎榜列表
按日期获取历史当日上榜的个股数据，如果一个股票有多个上榜原因，则会出现该股票多条数据。
-----
import tushare as ts
ts.top_list('2016-06-12')
'''
top_list_para_dic = {
                     'date':'日期',#格式YYYY-MM-DD
                     'retry_count':'重试次数',#当网络异常后重试次数，默认为3
                     'pause':'停顿秒数',#重试时停顿秒数，默认为0                    
                     }

top_list_dic = {
                'code':'代码',
                'name':'名称',
                'pchange':'当日涨跌幅',
                'amount':'龙虎榜成交额(万)',
                'buy':'买入额(万)',
                'bratio':'买入占总成交比例',
                'sell':'卖出额(万)',
                'sratio':'卖出占总成交比例',
                'reason':'上榜原因',
                'date':'日期',                
                }

'''
个股上榜统计
获取近5、10、30、60日个股上榜统计数据,包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数。
--------
import tushare as ts
ts.cap_tops()
'''
cap_tops_dic={
              'code':'代码',
              'name':'名称',
              'count':'上榜次数',
              'bamount':'累积购买额(万)',
              'samount':'累积卖出额(万)',
              'net':'净额(万)',
              'bcount':'买入席位数',
              'scount':'卖出席位数',             
              }

'''
营业部上榜统计
获取营业部近5、10、30、60日上榜次数、累积买卖等情况。
-------
import tushare as ts
ts.broker_tops()
'''
broker_tops_dic = {
                   'broker':'营业部名称',
                   'count':'上榜次数',
                   'bamount':'累积购买额(万)',
                   'bcount':'买入席位数',
                   'samount':'累积卖出额(万)',
                   'scount':'卖出席位数',
                   'top3':'买入前三股票',                   
                   }

'''
机构席位追踪
获取机构近5、10、30、60日累积买卖次数和金额等情况。
-------
import tushare as ts
ts.inst_tops()
'''
ins_tops_dic = {
                'code':'代码',
                'name':'名称',
                'bamount':'累积买入额(万)',
                'bcount':'买入次数',
                'samount':'累积卖出额(万)',
                'scount':'卖出次数',
                'net':'净额(万)',                
                }

'''
机构成交明细
获取最近一个交易日机构席位成交明细统计数据
--------
import tushare as ts
ts.inst_detail()
'''
inst_detail_dic = {
                   'code':'代码',
                   'name':'名称',
                   'date':'交易日期',
                   'bamount':'机构席位买入额(万)',
                   'samount':'机构席位卖出额(万)',
                   'type':'类型',                   
                   }

#银行间同业拆放利率
'''
Shibor拆放利率
获取银行间同业拆放利率数据，目前只提供2006年以来的数据。
--------
import tushare as ts
df = ts.shibor_data() #取当前年份的数据
#df = ts.shibor_data(2014) #取2014年的数据
df.sort('date', ascending=False).head(10)
'''
shibor_data_dic = {
                   'date':'日期',
                   'ON':'隔夜拆放利率',
                   '1W':'1周拆放利率',
                   '2W':'2周拆放利率',
                   '1M':'1个月拆放利率',
                   '3M':'3个月拆放利率',
                   '6M':'6个月拆放利率',
                   '9M':'9个月拆放利率',
                   '1Y':'1年拆放利率',                   
                   }

'''
Shibor均值数据
获取Shibor均值数据，目前只提供2006年以来的数据。
----------

import tushare as ts
df = ts.shibor_ma_data() #取当前年份的数据
#df = ts.shibor_ma_data(2014) #取2014年的数据
df.sort('date', ascending=False).head(10)
'''
shibor_ma_data_dic = {
                      
                      }

'''
贷款基础利率（LPR）
获取贷款基础利率（LPR）数据，目前只提供2013年以来的数据。
--------------
import tushare as ts
df = ts.lpr_data() #取当前年份的数据
#df = ts.lpr_data(2014) #取2014年的数据
df.sort('date', ascending=False).head(10)
'''
lpr_data_dic = {
                'date':'日期',
                '1Y':'1年贷款基础利率',                
                }

'''
LPR均值数据
获取贷款基础利率均值数据，目前只提供2013年以来的数据。
--------------
import tushare as ts
df = ts.lpr_ma_data() #取当前年份的数据
#df = ts.lpr_ma_data(2014) #取2014年的数据
df.sort('date', ascending=False).head(10)
'''
lpr_ma_data_dic = {
                   'date':'日期',
                   '1Y_5':'5日均值',
                   '1Y_10':'10日均值',
                   '1Y_20':'20日均值',                   
                   }

#电影票房
'''
实时票房
获取实时电影票房数据，30分钟更新一次票房数据，可随时调用。
---------------------
import tushare as ts
df = ts.realtime_boxoffice()
print(df)
'''
realtime_boxoffice_dic = {
                          'BoxOffice':'实时票房（万）',
                          'Irank':'排名',
                          'MovieName':'影片名',
                          'boxPer':'票房占比 （%）',
                          'movieDay':'上映天数',
                          'sumBoxOffice':'累计票房（万）',
                          'time':'数据获取时间',                          
                          }

'''
每日票房
获取单日电影票房数据，默认为上一日的电影票房，可输入参数获取指定日期的票房。
-------------
import tushare as ts
df = ts.day_boxoffice() #取上一日的数据
#df = ts.day_boxoffice('2015-12-24')  #取指定日期的数据
'''
day_boxoffice_dic= {                   
                    'AvgPrice':'平均票价',
                    'AvpPeoPle':'场均人次',
                    'BoxOffice':'单日票房（万）',
                    'BoxOffice_Up':'环比变化 （%）',
                    'IRank':' 排名',
                    'MovieDay':'上映天数',
                    'MovieName':'影片名',
                    'SumBoxOffice':'累计票房（万）',
                    'WomIndex':'口碑指数',                   
                     }

'''
月度票房¶
获取单月电影票房数据，默认为上一月，可输入月份参数获取指定月度的数据。
---------------
import tushare as ts
df = ts.month_boxoffice() #取上一月票房数据
#df = ts.month_boxoffice('2015-10') #取2015年10月的数据
'''
month_boxoffice_dic = {
                       'Irank':'排名',
                       'MovieName':'电影名称',
                       'WomIndex':'口碑指数',
                       'avgboxoffice':'平均票价',
                       'avgshowcount':'场均人次',
                       'box_pro':'月度占比',
                       'boxoffice':'单月票房(万)',
                       'days':'月内天数',
                       'releaseTime':'上映日期',                      
                       }

'''
影院日度票房
获取全国影院单日票房排行数据，
默认为上一日，可输入日期参数获取指定日期的数据。
-----------------------
import tushare as ts
df = ts.day_cinema() #取上一日全国影院票房排行数据
#df = ts.day_cinema('2015-12-24') #取指定日期的数据
df.head(10)
'''
day_cinemal_dic = {
                   'Attendance':'上座率',
                   'AvgPeople':'场均人次',
                   'CinemaName':'影院名称',
                   'RowNum':'排名',
                   'TodayAudienceCount':'当日观众人数',
                   'TodayBox':'当日票房',
                   'TodayShowCount':'当日场次',
                   'price':'场均票价（元）'                   
                   }