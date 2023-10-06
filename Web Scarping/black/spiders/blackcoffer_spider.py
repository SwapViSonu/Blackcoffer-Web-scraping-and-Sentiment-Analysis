import scrapy
import pandas as pd

class BlackcofferSpider(scrapy.Spider):
    name = "blackcoffer"

    # Read URLs and IDs from an Excel file
    def start_requests(self):
        excel_path = r"C:\Users\rajat\Downloads\Input.xlsx" # Replace with the actual path
        df = pd.read_excel(excel_path)
        for index, row in df.iterrows():
            url = row['URL']
            identifier = row['URL_ID']
            yield scrapy.Request(url=url, meta={'identifier': identifier}, callback=self.parse_page)

    # Parse individual pages
    def parse_page(self, response):
        identifier = response.meta['identifier']

        # Extract title
        title = response.xpath('//h1/text()').get()

        # Extract content from multiple paths
        content_paths = ['//div[@class="td-post-content tagdiv-type"]/p/text()','//div[@class="tdb-block-inner td-fix-index"]/p/text()']  # Customize the XPath expressions
        content_text = []

        for path in content_paths:
            content = response.xpath(path).getall()
            content_text.extend(content)

        # #Extract content (customize the XPath accordingly)
        # content = response.xpath('//div[@class="td-post-content tagdiv-type"]/p/text()').getall()
        # Join the content into a single string
        content_text = '\n'.join(content_text).strip()
        # Create the content to be saved in the text file
        file_content = f"Title: {title}\n\n{content_text}"

        # Save content in a text file
        if file_content:
            filename = f"{identifier}.txt"
            with open(filename, 'w',encoding='utf-8') as file:
                file.write(file_content)
