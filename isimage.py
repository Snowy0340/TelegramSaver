import requests
from parsel import Selector
import argparse
import os
from tqdm import tqdm
from concurrent import futures
import re
import json
import jmespath

def download_v3(link):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'HX-Request': 'true',
    'HX-Trigger': 'search-btn',
    'HX-Target': 'tiktok-parse-result',
    'HX-Current-URL': 'https://tiktokio.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://tiktokio.com',
    'Connection': 'keep-alive',
    'Referer': 'https://tiktokio.com/'
    }


    _, file_name, content_type = extract_video_id(link)

    with requests.Session() as s:
        try:
            r = s.get("https://tiktokio.com/", headers=headers)

            selector = Selector(text=r.text)

            prefix = selector.css('input[name="prefix"]::attr(value)').get()

            data = {
                'prefix': prefix,
                'vid': link,
            }

            response = requests.post('https://tiktokio.com/api/v1/tk-htmx', headers=headers, data=data)

            selector = Selector(text=response.text)

            if content_type == "video":
                download_link_index = 2 if args.watermark else 0
                download_link = selector.css('div.tk-down-link a::attr(href)').getall()[download_link_index]

                response = s.get(download_link, stream=True, headers=headers)

                downloader(file_name, link, response, extension="mp4")
            else:
                download_links = selector.xpath('//div[@class="media-box"]/img/@src').getall()
                
                for index, download_link in enumerate(download_links):
                    response = s.get(download_link, stream=True, headers=headers)
                    downloader(f"{file_name}_{index}", link, response, extension="jpeg")

        except Exception as e:
            print(f"\033[91merror\033[0m: {link} - {str(e)}")
            with open("errors.txt", 'a') as error_file:
                error_file.write(link + "\n")
