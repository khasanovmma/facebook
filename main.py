# import  facebook
#
# graph = facebook.GraphAPI(access_token="EAAJ1ls7S6TgBAGBcZCl35ncEiQwwzdGtmZCoKuOn8IL3cqRTtj6NWM5nqcs3EZApk2LXUKsJc48QSMZB2xDZBfHQ3GxKuCRB8XE4m9PZAbxs94OUoUh0f1TWcWVlxwqefu3ZB1aT1TKVoOtLykwUusXliFtAdGTjx2hGuZAMt2yEgbG4GDrVFMbhqXRTajWgXU7DnfG6uFy3G7ZCyH6S5qOSC1AgDB3kZBUR8ZD", version="2.12")
# places = graph.search(type='group', fields='Berlin')
#
# print(places)
import os
import sys

try:
    from facepy import GraphAPI

    graph = GraphAPI('EAAJ1ls7S6TgBACrSvIRNWvuzffZAxIESXcnQ3oULrBkM8xsjDZBDkkDCWQNEYBA7gb4aLbYO283YarshkwEQQgLEC4SDhoPCpthTVl5urFIlgZAIgnD8CxctuqZALZCblbytSwjbZBMsyDHZCRNsZCVnuI37giEYCjySL7dy4G50fyTBJ56iDtfoGSN2nTuDuYY9mtgrNzpD3NksTU4j3NlMyTOwjaI00aWPGMwIiZAVcCxO6XiLvbAES04t03asP9r0ZD')

    search_result = graph.get('https://www.facebook.com/rf')
    print(search_result)
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


# from facebooktoken import FacebookTokenRefresher
#
# ftr = FacebookTokenRefresher(
#     app_id=692240528894264,
#     app_secret="a12dd027aa3f1b5defea652e018caa09",
#     short_access_token="EAAJ9Xx55SZA0BAHmtrLHE3mvthKHW5mbBDXpkW6haI62UBevj8bZB1DWdoGKKtYhevbZBvtyOBHVdC7i3cFmxbO7PaUpjS2yovRO4BWPsNcmRqLzUCcAcU70dkl3WrdrqZAvG1jPWrdcnVJZANKiZCJmqf44vXfNU9kAzA9uqRM0FTzYZBk6P6QYlpQJ2LJiNQZD"
# )
#
# results = ftr.refresh()
# print(results)

# from proxycrawl.proxycrawl_api import ProxyCrawlAPI
#
# api = ProxyCrawlAPI({'token': 'EAAJ1ls7S6TgBACrSvIRNWvuzffZAxIESXcnQ3oULrBkM8xsjDZBDkkDCWQNEYBA7gb4aLbYO283YarshkwEQQgLEC4SDhoPCpthTVl5urFIlgZAIgnD8CxctuqZALZCblbytSwjbZBMsyDHZCRNsZCVnuI37giEYCjySL7dy4G50fyTBJ56iDtfoGSN2nTuDuYY9mtgrNzpD3NksTU4j3NlMyTOwjaI00aWPGMwIiZAVcCxO6XiLvbAES04t03asP9r0ZD'})
#
# response = api.get('https://www.facebook.com/groups/search/groups/?q=berlin',
#                    {'scraper': 'facebook-group', 'scroll': 'true', 'scroll_interval': 20})
#
# print(response)

