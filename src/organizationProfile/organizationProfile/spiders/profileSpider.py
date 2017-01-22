from scrapy.spiders import Spider
from organizationProfile.organizationProfile.items import OrganizationProfileItem
from scrapy.http import Request

name       = "organizationProfiles"
allowed_domains = ["101-elektro.ch"]
start_urls  = ["http://101-elektro.ch"]

# First always read the meta tags

