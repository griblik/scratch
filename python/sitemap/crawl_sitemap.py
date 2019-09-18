from bs4 import BeautifulSoup
import requests, sys

url_list = []

def find_content_urls(base_sitemap):
    ''' Find the sitemaps linked from the sitemapindex and extract content locations from them '''
    
    # Find all the sitemap links from the sitemapindex 
    resp = requests.get(base_sitemap)
    xml = resp.text
    soup = BeautifulSoup(xml, features='lxml')
    sitemaps = soup.find_all("sitemap")
    
    # extract content URLs from the sitemaps therein
    for sitemap in sitemaps:
        print("Getting {0}".format(sitemap.loc.text))
        resp = requests.get(sitemap.loc.text)
        xml = resp.text
        soup = BeautifulSoup(xml, features='lxml')
        
        for loc in soup.find_all("loc"):
            url_list.append(loc.text)

def export_url_list(filename=export_filename):
    ''' Save the known url list to a text file '''
    with open(filename, 'w') as wf:
        for url in url_list:
            wf.write(url + '\n')

# python3 crawl_sitemap.py http://site/sitemap.xml output-file.txt
if __name__ == "__main__":
    if sys.argv:
        base_sitemap = sys.argv[1]
        export_filename = sys.argv[2]
        
    find_content_urls(base_sitemap)
    export_url_list(export_filename)