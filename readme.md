This takes LinkedIn person results (site:linkedin.com/in/) from Google and cleans and formats them to make them useful for large scale prospecting as LinkedIn has taken a very hard stance against unauthorized scrapers, extensions, crawlers, etc.

Use the Google search API (https://developers.google.com/custom-search/json-api/v1/overview) as Google's robots.txt does not allow scraping of their results either.

In essence this script takes a CSV or results that look like this and several other LinkedIn formats:

https://www.linkedin.com/in/redacted-lastname-88b2c858, James Edward Jones | LinkedIn,Indianapolis, IN Area - Vice President @ Cummins

And turns it into this:

Indianapolis, James,Jones, Edward, "Indianapolis, Indiana", https://www.linkedin.com/in/redacted-lastname-88b2c858, Cummins, Vice President

This can be super useful when it is paired with custom search operators from Google in order to extract people and companies with keywords specific to your target customer persona.

Find me on twitter at: https://twitter.com/SaggeseNicholas
