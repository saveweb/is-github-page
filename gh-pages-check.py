# coding: utf-8

import argparse
import ipaddress
import json
import logging
import os
import urllib.parse
import urllib.request

import dns.resolver

logger = logging.getLogger(__name__)


def get_pages_ip():
    api = "https://api.github.com/meta"
    meta = urllib.request.urlopen(api)

    pages_network = json.loads(meta.read()).get("pages", [])
    pages_ip = [i for n in pages_network for i in ipaddress.ip_network(n)]

    return pages_ip


def check_domain(domain: str, resolver: dns.resolver.Resolver, pages_ip: list):
    if domain.endswith("github.io"):
        return True

    for rdtype in ["A", "CNAME", "AAAA"]:
        try:
            answers = resolver.resolve(domain, rdtype=rdtype)
        except dns.resolver.NoAnswer:
            logger.debug(
                f"The DNS response does not contain an answer to the question: {domain} IN {rdtype}")
            continue
        except dns.resolver.Timeout:
            logger.debug(f"The DNS operation has timed out to {domain}")
            continue
        except dns.resolver.NoNameservers:
            logger.debug(
                f"All nameservers failed to answer the query {domain}")
            continue
        except dns.resolver.NXDOMAIN:
            logger.debug(f"{domain} does not exist")
            continue

        for answer in answers.rrset:
            if rdtype in ["A", "AAAA"]:
                if answer.to_text() in pages_ip:
                    return True
            else:
                if "github.io" in answer.to_text():
                    return True

    return False


def csv_lines_to_dict_list(csv_lines: list):
    header = ["intro", "url", "rss", "tags"]

    csv_list = []
    for line in csv_lines[1:]:
        line_dict = {}
        for k, v in zip(header, [i.strip() for i in line.split(",")]):
            if k == "tags":
                v = [t.strip() for t in v.split(";")]
            line_dict.update({k: v})
        csv_list.append(line_dict)

    return csv_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nameservers", default="8.8.8.8,1.0.0.1",
                        help="comma split nameservers, default: %(default)s")
    parser.add_argument("-u", "--urls", nargs="+",
                        metavar="URL", help="urls to check")
    parser.add_argument(
        "-c", "--csv", help="use remote/local csv file as input")
    parser.add_argument("-o", "--output", help="output file to write")
    args = parser.parse_args()

    urls = []
    if args.urls and len(args.urls) > 0:
        urls.extend(args.urls)

    if args.csv and args.csv.startswith("http"):
        resp = urllib.request.urlopen(args.csv)
        csv_lines = resp.read().decode().splitlines()
        csv_list = csv_lines_to_dict_list(csv_lines)
        urls.extend([item["url"] for item in csv_list])

    if args.csv and os.path.exists(os.path.expanduser(args.csv)):
        with open(os.path.expanduser(args.csv)) as f:
            csv_lines = f.readlines()
        csv_list = csv_lines_to_dict_list(csv_lines)
        urls.extend([item["url"] for item in csv_list])

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ns.strip() for ns in args.nameservers.split(",")]
    pages_ip = get_pages_ip()

    for url in urls:
        domain = urllib.parse.urlparse(url).netloc
        result = check_domain(domain, resolver, pages_ip)

        print(f"{result}, {url}")
        if args.output:
            with open(args.output, "a") as f:
                f.write(f"{result}, {url}\n")


if __name__ == "__main__":
    main()
