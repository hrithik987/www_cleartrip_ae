import json
from datetime import datetime, timedelta
import os
# from networkx.classes import is_directed
import pandas as pd
# import secret_details
from curl_cffi import requests
import pydash as _
# from currency_converter import CurrencyConverter


# proxy = secret_details.proxies



def remove_extra_space(column):
    # Remove any extra spaces or newlines created by this replacement
    column = column.replace(r'\s+', ' ', regex=True)
    # column = column.str.strip()
    # Update the cleaned value back in row_data
    return column



def df_cleaning(df):
    # Drop Unnamed columns
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    # Replace empty strings with 'N/A'
    df = df.replace('', 'N/A').replace('None', 'N/A')
    df.fillna('N/A', inplace=True)
    # Add id column
    df.insert(0, 'id', range(1, len(df) + 1))
    # Convert column headers to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

def calculate_duration(start_time: str, end_time: str) -> str:
    fmt = "%H:%M"
    start_dt = datetime.strptime(start_time, fmt)
    end_dt = datetime.strptime(end_time, fmt)

    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    diff = end_dt - start_dt
    hours, remainder = divmod(diff.seconds, 3600)
    minutes = remainder // 60

    return f"{hours}h {minutes}m"

cookies = {
    'ct_statsig_experiments': '{"search_v3":"b"}',
    'rbzid': 'dYSaQix4CV1d7B/hb228ds3snG13CdNp7Bg63rG8GHcAcWNp2XXUpJdGVkJriPNeObPWkcwG4qiqupsiRpws3LM5BwZSYTfVMBNTIyH7JUaEGd3ufAFYU+rwHlPtS87eJYSDw2oNsfCNHN1DC3eh69t1/atrotT5NXXPjTKwqRUVgUNZ66hdTs89SzCfbD7vI9y9rsH1N2UYN11ItMfcvYFFdd/3JgoVFQVPW9+8Hzo=',
    'rbzsessionid': 'dea2043114895a80731c32fd9009b8bc',
    'ffEnabled': 'false',
    'noncleartrip': 'false',
    'statsig-stableid': '8f86ddfd-1b7c-42b2-ab19-c2470a2185ad',
    '_gcl_au': '1.1.954040344.1752648355',
    'WZRK_G': '083dc21351bc4f7eab686760fcc2d64e',
    '_ga': 'GA1.1.668103182.1752648365',
    'mfKey': '1udqp4u.1752648369279',
    '35BS11281-ref': 'direct|direct|direct|direct|1752648369572',
    '35BS11281': '1427b55054-1752648369573',
    '35BS11281-cp': '1427b55054-1752648369573',
    '_hsu': 'hs.1752648374152.3cf97099d6',
    '_hscl': '',
    '_fbp': 'fb.1.1752648377323.976700870754674655',
    'mf_visitid': '1fxbod9.1752648435948',
    'mf_utms': '%7B%22adults%22%3A%221%22%2C%22childs%22%3A%220%22%2C%22infants%22%3A%220%22%2C%22class%22%3A%22Economy%22%2C%22depart_date%22%3A%2226%2F07%2F2025%22%2C%22from%22%3A%22MCT%22%2C%22to%22%3A%22KWI%22%2C%22intl%22%3A%22y%22%2C%22origin%22%3A%22MCT%2520-%2520Muscat%2C%2520OM%22%2C%22destination%22%3A%22KWI%2520-%2520Kuwait%2C%2520KW%22%2C%22sft%22%3A%22%22%2C%22sd%22%3A%221752648434646%22%2C%22rnd_one%22%3A%22O%22%2C%22isCfw%22%3A%22false%22%7D',
    '_uetsid': '8e9a6620621011f0919b110a0d15161c',
    '_uetvid': '8e9a7a20621011f0aea0eff73fe3ffde',
    'ct-dvId': 'KfvJwL7IuZOd%2FPyTW8X%2Fb98m9%2Fnb4cNMdbvkLOmYKy0pZR4ixmpD3znxOMpeNigmcEsY2jtTZq%2BK0WEUFg8wVWSFlkSwQ25uWZOO42eo4HE%3D',
    'ct-ab': '%7B%22h_exp16%22%3A%22b%22%2C%22h_exp15%22%3A%22b%22%2C%22axisLoyalty%22%3A%22b%22%2C%22h_exp13%22%3A%22b%22%2C%22ghFlexMax%22%3A%22a%22%2C%22EMI_SRP_Exp%22%3A%22a%22%2C%22h_exp_dom%22%3A%22v3_meetbeat%22%2C%22freeway_smb%22%3A%22d%22%2C%22h_exp17%22%3A%22b%22%2C%22clevertapDTInlineBanner%22%3A%22a%22%2C%22offer_banner%22%3A%22b%22%2C%22bus_supercoin%22%3A%22b%22%2C%22h_exp12%22%3A%22b%22%2C%22h_exp10%22%3A%22b%22%2C%22ff_Nudges%22%3A%22a%22%2C%22sc_right_rail%22%3A%22a%22%2C%22split%22%3A%22a%22%2C%22h_exp_7%22%3A%22b%22%2C%22alternate_refund%22%3A%22a%22%2C%22vasExp7%22%3A%22b%22%2C%22saved_vpa%22%3A%22a%22%2C%22vasExp6%22%3A%22b%22%2C%22exp%22%3A%22c%22%2C%22clevertapSrpBanner%22%3A%22a%22%2C%22bentoSrp%22%3A%22a%22%2C%22wallet_display%22%3A%22b%22%2C%22idParameter%22%3A%22IP%22%2C%22identifier%22%3A%22190.93.96.18-Wed+Jul+16+12%3A17%3A26+IST+2025%22%2C%22card_tokenization%22%3A%22b%22%2C%22supercoins%22%3A%22a%22%2C%22e_srp%22%3A%22a%22%2C%22h_searchorder%22%3A%22b%22%2C%22bus_cc_max%22%3A%22b%22%2C%22New_Coupon_Experience%22%3A%22a%22%2C%22modify_search%22%3A%22a%22%2C%22hi_five%22%3A%22b%22%2C%22room_category_details_page%22%3A%22a%22%2C%22ff_Intl%22%3A%22c%22%2C%22EMI_Itin_Exp%22%3A%22a%22%2C%22h_exp_intl%22%3A%22v3_exploit_gbr%22%2C%22sortordermobile%22%3A%22a%22%2C%22RNIFlowType%22%3A%22b%22%2C%22h_exp1%22%3A%22a%22%2C%22h_exp2%22%3A%22b%22%2C%22h_exp8%22%3A%22b%22%2C%22trains_pwa%22%3A%22b%22%2C%22tuple%22%3A%22b%22%2C%22gh66%22%3A%22b%22%2C%22per_adult_price%22%3A%22b%22%2C%22sorting%22%3A%22a%22%2C%22scV3%22%3A%22b%22%2C%22sortorder%22%3A%22a%22%2C%22testGlobal%22%3A%22d%22%2C%22scV4%22%3A%22b%22%2C%22upi-intent%22%3A%22a%22%2C%22ptb%22%3A%22b%22%2C%22EMI_SRP_Dom%22%3A%22a%22%2C%22h_itin%22%3A%22b%22%2C%22highRps%22%3A%22b%22%2C%22clevertapTopBanner%22%3A%22a%22%2C%22intlflexmax%22%3A%22b%22%2C%22vasExp1%22%3A%22c%22%2C%22bus_conv_fee%22%3A%22b%22%2C%22bus_perf_coupon%22%3A%22b%22%2C%22hashValue%22%3A%225a0d68d94038268b7b2abb92335a44cac1d1ee62d861b66c60a9eb78a79c1efe%22%2C%22plm%22%3A%22b%22%2C%22mediCancel%22%3A%22b%22%2C%22h_itin_dt%22%3A%22b%22%2C%22tk_home%22%3A%22b%22%2C%22seatCallout%22%3A%22b%22%2C%22clevertapPwaInlineBanner%22%3A%22a%22%2C%22clevertapDThomeBanner%22%3A%22a%22%2C%22login_init%22%3A%22a%22%7D',
    'cto_bundle': '-2QKzV9aWktXT09JZlJSV20yZmF4SXNLOWhsQjklMkJxNkRHcTdqMFNieTBrQW1zaE1yTWRNOHRoc1ZTNGVVTHFzbUl5Wnc3VzJWOXg2WXFJNnFXbU5BdDh3aDd6SldVS2F5ZE04dGtGWmRlYUNTb1JsNTMxdFJCZjA3UVFSeklmSHVDaG9KTWpyejNRWVBNcUtsRkE4Z1lyeDUlMkJkTFhEcSUyRmdjYUhrQ3liVmR1UEIlMkZoZTVkQ0lUclZTVUI1dFZiM1E5N0VyeVJSRHhtNUV6ZGhMJTJCTWhYb2hYd3FYdyUzRCUzRA',
    '_ga_5CWGPF7QB9': 'GS2.1.s1752648364$o1$g1$t1752648567$j18$l0$h0',
    '_ga_M9WKWY8MDB': 'GS2.1.s1752648453$o1$g1$t1752648574$j60$l0$h0',
    'WZRK_S_W8R-KK8-W74Z': '%7B%22p%22%3A3%2C%22s%22%3A1752648361%2C%22t%22%3A1752648563%7D',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'app-agent': 'DESKTOP',
    'cache-control': 'no-cache',
    'expires': '0',
    # 'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE4MzU4NjEiLCJhcCI6IjExMDMyMDc4MzkiLCJpZCI6Ijc1NzJhYzE1M2FlNjUyZDUiLCJ0ciI6IjdiYTk1NzUzMGIzNTYwMjIyZDRkMzg1ODNiMDczOGMwIiwidGkiOjE3NTI2NDg1NzY1OTR9fQ==',
    # 'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE4MzU4NjEiLCJhcCI6IjExMDMyMDc4MzkiLCJpZCI6Ijc1NzJhYzE1M2FlNjUyZDUiLCJ0ciI6IjdiYTk1NzUzMGIzNTYwMjIyZDRkMzg1ODNiMDczOGMwIiwidGkiOjE3NTI2NDg1NzY1OTR9fQ==',
    'pragma': 'no-cache',
    'preferred-language': '',
    'priority': 'u=1, i',
    'r_lang': '',
    # 'referer': 'https://www.cleartrip.com/flights/international/results?adults=1&childs=0&infants=0&class=Economy&depart_date=26/07/2025&from=MCT&to=KWI&intl=y&origin=MCT%20-%20Muscat,%20OM&destination=KWI%20-%20Kuwait,%20KW&sft=&sd=1752648434646&rnd_one=O&isCfw=false',
    # 'referer': 'https://www.cleartrip.com/',
    'referer': 'https://www.cleartrip.ae/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    # 'traceparent': '00-7ba957530b3560222d4d38583b0738c0-7572ac153ae652d5-01, 00-b62ddcee671db09dd58d9097aac85cb9-0ee55e5ee2d140df-01',
    # 'tracestate': '1835861@nr=0-1-1835861-1103207839-7572ac153ae652d5----1752648576594',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-newrelic-id': 'undefined',
    # 'cookie': 'ct_statsig_experiments={"search_v3":"b"}; rbzid=dYSaQix4CV1d7B/hb228ds3snG13CdNp7Bg63rG8GHcAcWNp2XXUpJdGVkJriPNeObPWkcwG4qiqupsiRpws3LM5BwZSYTfVMBNTIyH7JUaEGd3ufAFYU+rwHlPtS87eJYSDw2oNsfCNHN1DC3eh69t1/atrotT5NXXPjTKwqRUVgUNZ66hdTs89SzCfbD7vI9y9rsH1N2UYN11ItMfcvYFFdd/3JgoVFQVPW9+8Hzo=; rbzsessionid=dea2043114895a80731c32fd9009b8bc; ffEnabled=false; noncleartrip=false; statsig-stableid=8f86ddfd-1b7c-42b2-ab19-c2470a2185ad; _gcl_au=1.1.954040344.1752648355; WZRK_G=083dc21351bc4f7eab686760fcc2d64e; _ga=GA1.1.668103182.1752648365; mfKey=1udqp4u.1752648369279; 35BS11281-ref=direct|direct|direct|direct|1752648369572; 35BS11281=1427b55054-1752648369573; 35BS11281-cp=1427b55054-1752648369573; _hsu=hs.1752648374152.3cf97099d6; _hscl=; _fbp=fb.1.1752648377323.976700870754674655; mf_visitid=1fxbod9.1752648435948; mf_utms=%7B%22adults%22%3A%221%22%2C%22childs%22%3A%220%22%2C%22infants%22%3A%220%22%2C%22class%22%3A%22Economy%22%2C%22depart_date%22%3A%2226%2F07%2F2025%22%2C%22from%22%3A%22MCT%22%2C%22to%22%3A%22KWI%22%2C%22intl%22%3A%22y%22%2C%22origin%22%3A%22MCT%2520-%2520Muscat%2C%2520OM%22%2C%22destination%22%3A%22KWI%2520-%2520Kuwait%2C%2520KW%22%2C%22sft%22%3A%22%22%2C%22sd%22%3A%221752648434646%22%2C%22rnd_one%22%3A%22O%22%2C%22isCfw%22%3A%22false%22%7D; _uetsid=8e9a6620621011f0919b110a0d15161c; _uetvid=8e9a7a20621011f0aea0eff73fe3ffde; ct-dvId=KfvJwL7IuZOd%2FPyTW8X%2Fb98m9%2Fnb4cNMdbvkLOmYKy0pZR4ixmpD3znxOMpeNigmcEsY2jtTZq%2BK0WEUFg8wVWSFlkSwQ25uWZOO42eo4HE%3D; ct-ab=%7B%22h_exp16%22%3A%22b%22%2C%22h_exp15%22%3A%22b%22%2C%22axisLoyalty%22%3A%22b%22%2C%22h_exp13%22%3A%22b%22%2C%22ghFlexMax%22%3A%22a%22%2C%22EMI_SRP_Exp%22%3A%22a%22%2C%22h_exp_dom%22%3A%22v3_meetbeat%22%2C%22freeway_smb%22%3A%22d%22%2C%22h_exp17%22%3A%22b%22%2C%22clevertapDTInlineBanner%22%3A%22a%22%2C%22offer_banner%22%3A%22b%22%2C%22bus_supercoin%22%3A%22b%22%2C%22h_exp12%22%3A%22b%22%2C%22h_exp10%22%3A%22b%22%2C%22ff_Nudges%22%3A%22a%22%2C%22sc_right_rail%22%3A%22a%22%2C%22split%22%3A%22a%22%2C%22h_exp_7%22%3A%22b%22%2C%22alternate_refund%22%3A%22a%22%2C%22vasExp7%22%3A%22b%22%2C%22saved_vpa%22%3A%22a%22%2C%22vasExp6%22%3A%22b%22%2C%22exp%22%3A%22c%22%2C%22clevertapSrpBanner%22%3A%22a%22%2C%22bentoSrp%22%3A%22a%22%2C%22wallet_display%22%3A%22b%22%2C%22idParameter%22%3A%22IP%22%2C%22identifier%22%3A%22190.93.96.18-Wed+Jul+16+12%3A17%3A26+IST+2025%22%2C%22card_tokenization%22%3A%22b%22%2C%22supercoins%22%3A%22a%22%2C%22e_srp%22%3A%22a%22%2C%22h_searchorder%22%3A%22b%22%2C%22bus_cc_max%22%3A%22b%22%2C%22New_Coupon_Experience%22%3A%22a%22%2C%22modify_search%22%3A%22a%22%2C%22hi_five%22%3A%22b%22%2C%22room_category_details_page%22%3A%22a%22%2C%22ff_Intl%22%3A%22c%22%2C%22EMI_Itin_Exp%22%3A%22a%22%2C%22h_exp_intl%22%3A%22v3_exploit_gbr%22%2C%22sortordermobile%22%3A%22a%22%2C%22RNIFlowType%22%3A%22b%22%2C%22h_exp1%22%3A%22a%22%2C%22h_exp2%22%3A%22b%22%2C%22h_exp8%22%3A%22b%22%2C%22trains_pwa%22%3A%22b%22%2C%22tuple%22%3A%22b%22%2C%22gh66%22%3A%22b%22%2C%22per_adult_price%22%3A%22b%22%2C%22sorting%22%3A%22a%22%2C%22scV3%22%3A%22b%22%2C%22sortorder%22%3A%22a%22%2C%22testGlobal%22%3A%22d%22%2C%22scV4%22%3A%22b%22%2C%22upi-intent%22%3A%22a%22%2C%22ptb%22%3A%22b%22%2C%22EMI_SRP_Dom%22%3A%22a%22%2C%22h_itin%22%3A%22b%22%2C%22highRps%22%3A%22b%22%2C%22clevertapTopBanner%22%3A%22a%22%2C%22intlflexmax%22%3A%22b%22%2C%22vasExp1%22%3A%22c%22%2C%22bus_conv_fee%22%3A%22b%22%2C%22bus_perf_coupon%22%3A%22b%22%2C%22hashValue%22%3A%225a0d68d94038268b7b2abb92335a44cac1d1ee62d861b66c60a9eb78a79c1efe%22%2C%22plm%22%3A%22b%22%2C%22mediCancel%22%3A%22b%22%2C%22h_itin_dt%22%3A%22b%22%2C%22tk_home%22%3A%22b%22%2C%22seatCallout%22%3A%22b%22%2C%22clevertapPwaInlineBanner%22%3A%22a%22%2C%22clevertapDThomeBanner%22%3A%22a%22%2C%22login_init%22%3A%22a%22%7D; cto_bundle=-2QKzV9aWktXT09JZlJSV20yZmF4SXNLOWhsQjklMkJxNkRHcTdqMFNieTBrQW1zaE1yTWRNOHRoc1ZTNGVVTHFzbUl5Wnc3VzJWOXg2WXFJNnFXbU5BdDh3aDd6SldVS2F5ZE04dGtGWmRlYUNTb1JsNTMxdFJCZjA3UVFSeklmSHVDaG9KTWpyejNRWVBNcUtsRkE4Z1lyeDUlMkJkTFhEcSUyRmdjYUhrQ3liVmR1UEIlMkZoZTVkQ0lUclZTVUI1dFZiM1E5N0VyeVJSRHhtNUV6ZGhMJTJCTWhYb2hYd3FYdyUzRCUzRA; _ga_5CWGPF7QB9=GS2.1.s1752648364$o1$g1$t1752648567$j18$l0$h0; _ga_M9WKWY8MDB=GS2.1.s1752648453$o1$g1$t1752648574$j60$l0$h0; WZRK_S_W8R-KK8-W74Z=%7B%22p%22%3A3%2C%22s%22%3A1752648361%2C%22t%22%3A1752648563%7D',
}


# c = CurrencyConverter()

for itr in range(1000):

    response = requests.get(
        # 'https://www.cleartrip.com/node/flight/search?adults=1&childs=0&infants=0&class=&airline=&carrier=&sd=&page=&sellingCountry=IN&ssfi=&flexi_search=&ssfc=&origin=&destination=&intl=y&sft=&depart_date=26/07/2025&return_date=&from=MCT&to=KWI',
        'https://www.cleartrip.ae/node/flight/search?adults=1&childs=0&infants=0&class=&airline=&carrier=&sd=&page=&sellingCountry=IN&ssfi=&flexi_search=&ssfc=&origin=&destination=&intl=y&sft=&depart_date=26/07/2025&return_date=&from=MCT&to=KWI',
        headers=headers,
        impersonate='chrome120',
        # proxies=proxy,
        # verify=False,
        timeout=60,
    )



    # print(response.text)
    print(response.status_code)
    # print(response.headers)
    data = _.get(json.loads(response.text), "sectors.MCT_KWI_260720250155_KU-6643.flights.segments[0].flightNumber", 'N/A')

    print(data)
    print('\n')
    # break


    main_json = json.loads(response.text)
    flights_dict = _.get(main_json, 'sectors', {})

    keys = flights_dict.keys()

    flights_list = _.get(main_json, 'jsons.airline_names', {})

    fare = []

    price_list = _.get(main_json, f'cards[0]', [])
    price_dict = {}
    stops = {}
    for price in price_list:
        key = _.get(price, 'sectorKeys', 'N/A')
        pr = _.get(price, 'priceBreakup.pr', 'N/A')
        stp = _.get(price, 'maxStopsInSectors', 'N/A')

        if stp == 0:
            stops[key[0]] = True
        else:
            stops[key[0]] = False

        price_dict[key[0]] = pr






    for key in keys:
        trip1 = {}
        _dict = _.get(flights_dict, f'{key}', 'N/A')


        flight_number = _.get(_dict,f"flights.segments[0].flightNumber","")

        # source_airportCode = _.get(_dict, f'flights.segments[0].arrival.airportCode', '')
        source_airportCode = _.get(_dict, f'lastArrival.airportCode', '')
        # source_city = _.get(_dict, f'flights.segments[0].arrival.airportName.c', '')
        # source_city = _.get(_dict, f'lastArrival.airportName.c', '')
        # source_country = _.get(_dict, f'flights.segments[0].arrival.airportName.cc', '')
        arrival_time_check = _.get(_dict, f'flights.segments[0].arrival.time', '')
        arrival_date_check = _.get(_dict, f'flights.segments[0].arrival.date', '')
        arrival_time = f"{arrival_date_check}T{arrival_time_check}:00"

        departure_time_check = _.get(_dict, f'flights.segments[0].departure.time', '')
        departure_date_check = _.get(_dict, f'flights.segments[0].departure.date', '')
        departure_time = f"{arrival_date_check}T{arrival_time_check}:00"

        arrival = f'{source_airportCode}' #- {source_city} - {source_country}'
        # arrival = f'{source_city}' #- {source_city} - {source_country}'

        # departure_airportCode = _.get(_dict, f'flights.segments[0].departure.airportCode', '')
        departure_airportCode = _.get(_dict, f'firstDeparture.airportCode', '')
        # departure_city = _.get(_dict, f'flights.segments[0].departure.airportName.c', '')
        # departure_city = _.get(_dict, f'firstDeparture.airportName.c', '')
        # departure_country = _.get(_dict, f'flights.segments[0].departure.airportName.cc', '')

        departure = f'{departure_airportCode}' # - {departure_city} - {departure_country}'
        # departure = f'{departure_city}' # - {departure_city} - {departure_country}'

        flight_type = 'ONE_WAY'

        airlines = _.get(_dict, f'flights.segments[0].flightNumber', 'N/A')

        try:
            airlines = airlines.split('-')[0]
            airlines = flights_list[airlines]
        except:
            airlines = 'N/A'

        # airline_list = []
        # for airline in airlines:
        #     airline_name = flights_list[airline]
        #     airline_list.append(airline_name)

        airline_price = price_dict[key]

        hh = _.get(_dict, f'flights.segments[0].durationTime.hh', 'N/A')
        mm = _.get(_dict, f'flights.segments[0].durationTime.mm', 'N/A')

        _class = _.get(_dict, f'flights.segments[0].flightClass', 'N/A')

        is_direct_flight = stops[key]

        # try:
        #     airline_price = round(c.convert(airline_price, 'INR', 'USD'))
        # except:
        #     airlines = 'N/A'

        journey_time = f'{hh}h {mm}m'
        trip1['url'] = 'https://www.cleartrip.ae/node/flight/search?adults=1&childs=0&infants=0&class=&airline=&carrier=&sd=&page=&sellingCountry=IN&ssfi=&flexi_search=&ssfc=&origin=&destination=&intl=y&sft=&depart_date=26/07/2025&return_date=&from=MCT&to=KWI'
        trip1['flight_number'] = flight_number.replace("-","")
        trip1['source'] = departure
        trip1['destination'] = arrival
        trip1['arrival_time'] = arrival_time
        trip1['departure_time'] = departure_time
        trip1['flight_type'] = flight_type
        trip1['airline_name'] = airlines
        trip1['airline_price'] = airline_price
        trip1['currency'] = 'AED'
        trip1['journey_time'] = journey_time
        trip1['is_direct_flight'] = is_direct_flight
        trip1['tags'] = 'N/A'
        trip1['class'] = str(_class).upper()
        trip1['date'] = arrival_date_check.replace("/","-")

        fare.append(trip1)

    break

df = pd.DataFrame(fare)

for column in df.columns.tolist():
    df[column] = remove_extra_space(df[column])


df = df_cleaning(df)

file_name = f"\\www_cleartrip_com_{datetime.now().strftime('%Y%m%d')}.xlsx"
input_file_path = os.getcwd() + f"\\files"

os.makedirs(input_file_path, exist_ok=True)
path = input_file_path + file_name

df.to_excel(path, index=False)

# 'scrape.do-request-cost': '1'
