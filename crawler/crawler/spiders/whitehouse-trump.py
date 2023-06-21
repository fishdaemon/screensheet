import scrapy
from html2text import html2text
import re

class WhiteHouseSpider(scrapy.Spider):
    name = "whitehouse-trump"
    start_urls = ["https://trumpwhitehouse.archives.gov/news/"]

    def parse(self, response):
        # Extracting links with CSS class "news-item"
        news_items = response.css(".presidential-action")
        for item in news_items:
            link = item.css("a::attr(href)").get()
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Converting HTML to Markdown
        #.page-title
        # .body-content
        title = response.css(".page-header").get()
        paragraphs = response.css(".page-content__content").get()
        #print(paragraphs)
        #exit(0)
        #content = re.sub(r'<aside[^>]*>', '', paragraphs)
        content = paragraphs
        #content = [paragraph.strip() for paragraph in paragraphs]
        markdown_title = html2text(title).strip()
        markdown_content = html2text(content).strip()

        # Saving the Markdown content as a file
        filename = response.url.split("/")[-2] + ".md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {markdown_title}\n\n{markdown_content}")
        self.log(f"Saved file {filename}")
