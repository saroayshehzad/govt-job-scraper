def parse(self, response):
        # We are using a broader selector to find ANY link that looks like a job
        # This looks for all links (a) inside any table cell (td)
        jobs = response.css('td a') 
        
        for job in jobs:
            title = job.css('::text').get()
            link = job.css('::attr(href)').get()
            
            # This filter ensures we only grab links that actually have text
            if title and len(title.strip()) > 10: 
                yield {
                    'post_name': title.strip(),
                    'official_url': response.urljoin(link),
                    'source': 'https://www.freejobalert.com/',
                    'scraped_at': '2026-03-11'
                }
