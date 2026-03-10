import scrapy

class GovtJobSpider(scrapy.Spider):
    name = 'govt_jobs'
    start_urls = ['https://www.sarkariresult.com/latestjob.php']

    def parse(self, response):
        # STEP 1: Scrape all jobs on the CURRENT page
        # This targets the anchor tags within the table rows of the main post div
        for job in response.css('div#post table tr td a'):
            job_title = job.css('::text').get()
            job_link = job.css('::attr(href)').get()
            
            if job_title:
                yield {
                    'post_name': job_title.strip(),
                    'official_url': response.urljoin(job_link),
                    'source': 'Sarkari Result',
                    'scraped_date': '2026-03-11'
                }

        # STEP 2: Find the "Next Page" link and follow it
        # On many sites, this is a link with text like 'Next' or 'More'
        # For Sarkari Result, jobs are often on one long page, but if you 
        # use other sites with 'Next' buttons, this line is the key:
        next_page = response.css('a.next::attr(href)').get() or \
                    response.xpath("//a[contains(text(), 'Next')]/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
