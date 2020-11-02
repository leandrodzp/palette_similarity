import scrapy
import re

URL='https://www.saatchiart.com'


class PaintingsSpider(scrapy.Spider):
    name = "paintings"

    start_urls = [
        f'{URL}/paintings'
    ]

    def parse(self, response):
        for painting in response.css('div.cygeUL'):
            product_path = painting.css('div.jDvrtz a::attr(href)')[0].get()
            try:
              painting.css('p.kcNkMy::text')[0].get()
              yield {
                  'title': painting.css('p.kcNkMy a::text')[0].get(),
                  'artist': re.match(r"<a\b[^>]*>(.*?)<\/a>", painting.css('p.kcNkMy a')[1].get()).group(1).replace("<!-- -->", ""),
                  'price': painting.css('p.kcNkMy::text')[0].get().strip("$").replace(',', ''),
                  'image_url': painting.css('div.jDvrtz a img::attr(src)')[0].get(),
                  'url': f'{URL}/{product_path}',
              }
            except IndexError:
              print('sorry')
        next_page = int(response.css("a.cMuFQi::text").get()) + 1
        next_url = f'{URL}/paintings?page={next_page}'
        if next_page < 200:
          yield scrapy.Request(next_url, callback=self.parse)