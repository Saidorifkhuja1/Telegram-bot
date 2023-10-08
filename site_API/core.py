from locale import currency

import destination as destination
import length as length
import origin as origin

from settings import SiteSettings

from site_API.utils.site_api_handler import SiteApiInterface

site = SiteSettings


url = "https://" + site.host_api

params = {origin: 'LED', destination: ' MOW', currency: 'RUB', length: '3'}

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
}

site_api = SiteApiInterface()

if __name__=='__main__':
	site_api()

