import requests
import sys
import os
import re
import json
import time
from lxml import html, etree


def download(url):
    """Returns the HTML source code from the given URL
        :param url: URL to get the source from.
    """
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("! Error {} retrieving url {}\n".format(r.status_code, url))
        return None
    
    return r

    
def parse_new_urls(tree, done_urls, pattern=None):
    results = tree.xpath('//a/@href')
    if pattern:
        results = filter(lambda u: any([p.match(u) for p in pattern]), results)

    new_urls = set()
    for r in results:
        r = r.rsplit("#", 1)[0]
        r = r.rsplit("?", 1)[0]
        if r not in done_urls:
            new_urls.add(r)
    return new_urls


def parse_content(tree, filename=None, meta=None):
    # XPath strings are adapted for a detail view @ El Mundo 
    data = {}
    xpath_string = {'title': "//article/h1[@itemprop='headline']/text()",
                    'summary': "//article/div[@itemprop='articleBody']/p[@class='summary-lead']//text()",
                    'author': "//footer/ul/li[@itemprop='name']//text()",
                    'location': "//footer/ul/li[@itemprop='address']//text()",
                    'datetime': "//article/div[@itemprop='articleBody']/time//text()",
                    'content': "//article/div[@itemprop='articleBody']/p[not(@class='summary-lead')]//text()",
                    }
               
    for key,value in xpath_string.iteritems():
        try:
            item = tree.xpath(value)
            if not isinstance(item, basestring):
                if key == 'summary':
                    item = '. '.join(item).strip()
                else:
                    item = ''.join(item).strip()
            data[key] = item.strip()
        except Exception:
            pass
    
    if filename and any(data.values()):
        data.update(meta)
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf8'))
    
    return data


def parse_recursive(init_url, content_pattern=None, visit_pattern=None, output_dir=None):
    urls = set([init_url])
    done = []
    i = 1
    while len(urls):
        url = urls.pop()
        sys.stdout.write("[{}/{}] - {}\n".format(i, len(urls)+len(done), url))
        try:
            # Download content
            page = download(url)
            
            # Get new URLs
            tree = html.fromstring(page.content)
            new_urls = parse_new_urls(tree, done, visit_pattern)
            urls.update(new_urls)
            
            if not content_pattern or any([p.match(url) for p in content_pattern]):
                # Data from url
                url_pattern = re.compile('https?:\/\/(www.)?elmundo.es\/internacional\/(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<uuid>[\d\w]+).html')
                meta = url_pattern.match(url).groupdict()
                filename = os.path.join(output_dir, meta['uuid'] + '.json')
                # Parse content
                parse_content(tree, filename, meta)

        except KeyboardInterrupt:
            sys.stdout.write(">> User interrupt! Exit gracefully.")
            return
            
        except Exception as e:
            sys.stderr.write("\t error: {}\n".format(str(e)))
        
        time.sleep(0.100)
        i += 1
        done.append(url)


def test_content(url):
    page = download(url)
    tree = html.fromstring(page.content)
            
    with open('test_content.html', 'w') as f:
        f.write(etree.tostring(tree, pretty_print=True))
    data = parse_content(tree)
    sys.stdout.write(json.dumps(data, indent=4))
    


if __name__ == '__main__':
    sys.stdout.write("=============================\n")
    sys.stdout.write("== Lingwars - Scrape XPath ==\n")
    sys.stdout.write("=============================\n")
    
    #test_content('http://www.elmundo.es/internacional/2016/04/12/570d6235ca47413f1c8b45d9.html')
    
    url = "http://www.elmundo.es/internacional.html"
    
    content_pattern = [re.compile('https?:\/\/(www.)?elmundo.es\/internacional\/(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})\/(?P<uuid>[\d\w]+).html'),]
    visit_pattern = [re.compile('https?:\/\/(www.)?elmundo.es\/internacional.*'),]
    output_dir = os.path.join(os.path.dirname(__file__), 'done')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    parse_recursive(url, content_pattern, visit_pattern, output_dir)
    
