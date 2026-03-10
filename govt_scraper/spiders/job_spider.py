import scrapy
from scrapy.crawler import CrawlerProcess

class GovtJobSpider(scrapy.Spider):
    name = 'govt_jobs'
    
    # We start with a popular job listing page
    start_urls = ['https://www.sarkariresult.com/latestjob.php']

    def parse(self, response):
        # This CSS selector finds the specific links in the job table
        # We look for all anchor (a) tags inside the main content table
        for job in response.css('div#post tr td a'):
            job_title = job.css('::text').get()
            job_link = job.css('::attr(href)').get()
            
            # Filter out empty or irrelevant links
            if job_title and "2026" in job_title:
                yield {
                    'post_name': job_title.strip(),
                    'official_url': response.urljoin(job_link),
                    'source': 'Sarkari Result',
                    'category': 'Government'
                }

# --- This part runs the spider and saves it to jobs.json ---
process = CrawlerProcess(settings={
    "FEEDS": {
        "jobs.json": {"format": "json", "indent": 4},
    },
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "LOG_LEVEL": "INFO"
})

process.crawl(GovtJobSpider)
process.start()
