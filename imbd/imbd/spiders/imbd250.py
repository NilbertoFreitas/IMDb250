import scrapy
import os
import pathlib
import csv

class Imbd250Spider(scrapy.Spider):
    name = 'imbd250'
    # abre o arquivo local, com todos os links
    start_urls = ['https://www.imdb.com/chart/top/']
    #delimiter = ';'

    # Apaga o arquivo caso exista, para evitar sobreposição
    if os.path.exists("imbd250.json"):
        os.remove("imbd250.json")

    def parse(self, response):       
        for links in response.css('.titleColumn').css('a::attr(href)').getall():
            text_page = f"https://www.imdb.com{links}"
            #text_page = f"https://www.imdb.com/title/tt0034583/"
            yield scrapy.Request(text_page, callback=self.parse_text)

  
    def parse_text(self, response):
        rnk = response.css('.Awards__List-sc-1qdt65t-1').css('a::text').get()
        rnk = rnk.split()[-1]
        rnk = rnk.replace('#', '')
        rnk = int(rnk)
        director = response.css(".ipc-metadata-list-item__content-container").css('a::text').get()
        title = response.css('h1::text').get()
        
        #Em alguns filmes o título original é o mesmo traduzido e portanto não tem a classe no html
        if not response.css('.OriginalTitle__OriginalTitleText-jz9bzr-0::text').get():
            original_title = title
        else:
            original_title = response.css('.OriginalTitle__OriginalTitleText-jz9bzr-0::text').get()[16:]
            
        year = response.css('.TitleBlockMetaData__ListItemText-sc-12ein40-2::text').get()
        rating = response.css('.AggregateRatingButton__RatingScore-sc-1ll29m0-1::text').get()
        award = response.css('.Awards__Wrapper-sc-1qdt65t-0').css('li').css('a::text').get()
        genre = response.css('.Storyline__StorylineMetaDataList-sc-1b58ttw-1').css('li').css('div').css('ul').css('li').css('a::text').get()
        age = response.css('.Storyline__StorylineMetaDataList-sc-1b58ttw-1').css('li').css('div').css('ul').css('li').css('span::text').getall()[-1]
        writer = response.css('.ipc-inline-list__item').css('a').css('.ipc-metadata-list-item__list-content-item::text').getall()[1]
        release = response.css('.styles__MetaDataContainer-sc-12uhu9s-0').css('div').css('ul').css('li').css('div').css('ul').css('li').css('a::text').get()
        storyline = response.css('.Storyline__StorylineWrapper-sc-1b58ttw-0').css('div').css('div').css('div::text').get()
        
       
        yield{
             'Ranking':rnk,
             'Title BR': title,
             'Original Title': original_title,
             'Year':year,
             'Director':director,   
             'Rating IMBd':rating,
             'Award':award,
             'Genre':genre,
             'Age':age,
             'Writer':writer,
             'Release':release,
             'Storyline':storyline
        }

#scrapy crawl imbd250 -o imbd250.json