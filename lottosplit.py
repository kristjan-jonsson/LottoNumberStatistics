#!/usr/bin/env python

from gazpacho import get, Soup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

def urlInUse( month, year = '2019' ):
    url = "https://games.lotto.is/result/lotto?productId=1#/%s-%s" % ( year,month )
    #print(url)
    return url

def getLottoNumbers( month, year = '2019' ):
  options = Options()
  options.headless = True
  browser = Firefox( executable_path='/usr/local/bin/geckodriver', options=options )
  url = urlInUse( month, year )
  #print(url)
  browser.get( url )
  html = browser.page_source
  soup = Soup( html )
  results = soup.find( 'li', {"class":"number listed"} )

  dags = soup.find( 'time', {"class":"title has-divider"} ).text

  lottoNumbers = []
  for r in results:
    lottoNumbers.append( r.find( 'span' ).text )
  
  lottoNumbers.insert( 0, dags )
  return lottoNumbers

def main( year ):
  for month in range( 52 ):
    lottoResult = getLottoNumbers( month + 1, year)
    print ( "Week %s, Year %s, lottonumbers %s" % ( month+1, year, lottoResult[0:6] ) )
    
  
if __name__== "__main__":
  import argparse
  parser = argparse.ArgumentParser(description='Get Lotto numbers from Icelandi Lotto')
  parser.add_argument('--year', required=True,
                        help='scrape numbers from year')
  args = parser.parse_args()
  main(year=args.year)
