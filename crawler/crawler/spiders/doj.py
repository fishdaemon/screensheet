import scrapy
from html2text import html2text


class DojSpider(scrapy.Spider):
    name = "doj"
    start_urls = ["https://www.justice.gov/news"]

    def parse(self, response):
        # Extracting links with CSS class "news-item"
        news_items = response.css("div.views-row")
        for item in news_items:
            link = item.css("a::attr(href)").get()
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Converting HTML to Markdown
        #.page-title
        # .body-content
        title = response.css("#node-title").get()
        if title is None :
            title = response.css(".node-title").get()
        content = response.css("div.field:nth-child(5) > div:nth-child(1) > div:nth-child(1)").get()
        if content is None :
            content = response.css(".field--name-field-pr-body").get()
        markdown_title = html2text(title).strip()
        markdown_content = html2text(content).strip()

        # Saving the Markdown content as a file
        filename = f"../input/{response.url.split('/')[-1]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {markdown_title}\n\n{markdown_content}")
        self.log(f"Saved file {filename}")
