# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:43:34 2020

@author: ktifler
"""

from bs4 import BeautifulSoup
import requests
import os
import youtube_dl
#import re
class scrapper:
    DOWNLOAD_DIRECTORY="X:\\Videos\\Movies"
    def init(self, domain, search_query,type_query):
        self.domain = domain
        self.search_query = search_query
        self.type_query = type_query
    def make_url(self,name):
    #    serachtype=str(input('if serie press s else anything : '))
        URL = "http://akwam.co/"
        search_query = "search?q="
        movie_name = name
        section_serie="&section=series"
        section = '&section=movie'
    #    if serachtype=='s':
    #        section=section_serie
        final_url = URL + search_query + movie_name + section
        return final_url

    def get_page(self,url):
        page=requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        return page,soup

    def get_movies_names(self,name):
        result_dict=dict()
        page,soup = self.get_page(self.make_url(name))
        query_results = soup.find_all("h3",class_="entry-title")
        for entity in query_results:
            result_dict[entity.find_next(string=True)]=entity.find_next("a")['href']
        return result_dict


    def get_redirect_link(self,url):
        res=dict()
        page, soup = self.get_page(url)
        result=soup.find_all("div",class_="tab-content quality")
        for quality in result:
            a=quality.find("a",class_="link-btn link-download d-flex align-items-center px-3")
            seize=a.find("span",class_="font-size-14 mr-auto").string
            res[seize]=a["href"]


        return res


    def get_finalAK_url(self,url):

        page, soup = self.get_page(url)
        a=soup.find("a",class_="download-link")
        return a["href"]


    def get_file_url(self,url):

        page,soup = self.get_page(url)
        a = soup.find("a",class_="link btn btn-light")
        return a["href"]


    def to_video(self,v,directory=DOWNLOAD_DIRECTORY):
        """
        v: media urls from youtube or facebook
        """

        ydl_opts1 = {
                'format': 'bestvideo/best'

        }

        with youtube_dl.YoutubeDL(ydl_opts1) as ydl:
            os.chdir(directory)
            ydl.download([v])
            ydl.params
            ydl.format_resolution
        return None

def main():
    s = scrapper()
    name = str(input("enter a movie name : "))
    res = s.get_movies_names(name)
    # name='Dolittle0'
    print("{:152}".format("-"*152))
    print("{:2} {:50} {:100}".format("n","name","url"))
    for i,(n,u) in enumerate(res.items()):
        print("{:2} {:50} {:100}".format(i,n,u))
    q=1
    qq=9
    urls=list(res.values())
    while q != 96 or qq != 96:
        q=int(input("choose a number to fetch download links : "))
        if q==96:
            break
        url=urls[q]
        format_link_dict=s.get_redirect_link(url)

        print("{:80}".format("-"*80))
        print("{:2} {:10} {:68}".format("n","seize","url"))
        for i,(sieze,u) in enumerate(format_link_dict.items()):
            print("{:2} {:50} {:100}".format(i,sieze,u))

        qq=int(input("choose a number to fetch download links : "))
        if qq==96:
            break
        urlss=list(format_link_dict.values())[qq]
        file_link=s.get_file_url(s.get_finalAK_url(urlss))
        print("file link : ",file_link)
        question=str(input("do you want to donwload file press y or yes"))
        if question =='y' or question == 'yes' :
            s.to_video(file_link)
            
            

if __name__=='__main__':
    main()


