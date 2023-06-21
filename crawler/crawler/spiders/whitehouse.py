import scrapy
from html2text import html2text


class WhiteHouseSpider(scrapy.Spider):
    name = "whitehouse"
    start_urls = ["https://www.whitehouse.gov/briefing-room/"]

    def parse(self, response):
        # Extracting links with CSS class "news-item"
        news_items = response.css(".news-item")
        for item in news_items:
            link = item.css("a::attr(href)").get()
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Converting HTML to Markdown
        #.page-title
        # .body-content
        title = response.css(".page-title").get()
        content = response.css(".body-content").get()
        markdown_title = html2text(title).strip()
        markdown_content = html2text(content).strip()

        # Saving the Markdown content as a file
        filename = response.url.split("/")[-2] + ".md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {markdown_title}\n\n{markdown_content}")
        self.log(f"Saved file {filename}")
