import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PARKING_LOT_URL = 'http://www.ahuzot.co.il/Parking/ParkingDetails/?ID={parking_id}'
PARKING_LIST_URL = 'http://www.ahuzot.co.il/Parking/All/'


def getParkingLotExtraData(lot):
  soup = BeautifulSoup(requests.get(
      lot['url']).content, features="html.parser")
  lot['status'] = getParkingLotStatus(soup)
  lot['location'] = getParkingLotLocation(soup)
  return lot


def getParkingLotLocation(lot_soup):
  location_div = lot_soup.find_all("div", {"class": "ParkingIcon2"})
  location_url = location_div[0]['onclick'].replace(
      'location.href=', '').replace('\'', '')
  parsed_url = urlparse(location_url)
  parsed_query_str = parse_qs(parsed_url.query)
  if 'c1' in parsed_query_str:
    x_value = parsed_query_str['c1'][0]
    y_value = parsed_query_str['c2'][0]
    return {'type': 'Point', 'coordinates': [float(x_value), float(y_value)]}
  return None


def getParkingLotStatus(lot_soup):
  status = lot_soup.find_all("td", {"class": "ParkingDetailsTable"})
  if not status:
    return "unknown"
  imgs = status[0].find_all("img")
  if not imgs:
    return "unknown"
  return imgs[0]['src'].split("/")[-1].split(".")[0]


def getAvailableParkingLots():
  soup = BeautifulSoup(requests.get(
      PARKING_LIST_URL).content, features="html.parser")
  parkings = []
  for link in soup.find_all("a", {"class": "ParkingLinkX"}):
    name, url = link.text, link['href']
    parkings.append({'name': name, 'url': url})
  return parkings


def getAllLotsStatus(lots):
  pool = ThreadPool(10)
  results = pool.map(getParkingLotExtraData, lots)
  pool.close()
  pool.join()
  return results
