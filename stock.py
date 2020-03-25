import urllib.request as request
from bs4 import BeautifulSoup
import pandas as pd
import os

class Stock():
    def __init__(self):

        # URL of the page to be scraped
        self.url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9'

    def get_HTML(self, get_response = False):

        response = request.Request(self.url,headers={'User-Agent': 'Mozilla/5.0'})

        content_obj = request.urlopen(response)

        response_code = content_obj.getcode()

        html_content = content_obj.read()

        # returns tuple of html and response code
        if(get_response):
            return(html_content, response_code)  
        else:
            return(html_content)

    # Method to get stock data from the page
    def get_stock_data(self, columns = None):

        html_content = self.get_HTML()

        soup_html_content = BeautifulSoup(html_content,features="lxml")

        table_element = soup_html_content.find('table', class_='tbldata14 bdrtpg')
        
        #List of all rows
        t_rows = [tr for tr in table_element.find_all('tr')]

        table_headers = [header.text.strip() for header in t_rows[0].find_all('th')]

        Data = list()

        Data.append(table_headers)

        # the first row is header and We have already grabed that one
        for tr in t_rows[1::]:  

            data = list()
            
            # list of all the columns
            tds = tr.find_all('td')

            # Extracting columns data
            for i, td in enumerate(tds):

                # We have to extract name from first column as it has unneccessary characters
                if(i==0):

                    industry = td.text.split('\n')[0]

                    data.append((industry))

                # Converting all the numeric values into float
                elif(i>=2):

                    data.append(float(td.text.strip().replace(',','')))

                else:

                    data.append(td.text.strip())
            
            Data.append(data)

        all_stock = pd.DataFrame(Data[1::], columns = Data[0])

        all_stock.index = range(1, len(all_stock)+1)

        if(columns == None):

            return(all_stock)

        else:

            column_data_type = str(type(columns)).split()[1].replace('>','')

            error_message = "Method get_stock_data expected a list of columns "+ column_data_type + " given."

            # assertion Error when the input is not a list
            assert type(columns) ==list, error_message

            return(all_stock[columns])

    # Method to extract all the saved close data from fiven list of CSV files
    def get_close_data(self, csv_files):

        # Interating through all the csv files
        for i, file in enumerate(csv_files):

            file_path = os.path.join('stock_data', file)

            stock_data = pd.read_csv(file_path)

            # Extract Company names in first iteration
            if(i == 0):

                company_names = stock_data['Company Name']

                all_close_data = [list() for c in range(len(company_names))]

                file_path = os.path.join('stock_data', file)

            # Renameing columne LastPrice to close as stockstats requires close column
            stock_data.rename(columns={"LastPrice" : "close"}, inplace = True)

            # Storing all close values of all companies in all_close_data
            [all_close_data[i].append(data) for i,data in enumerate(stock_data['close'])]


        # Return 2D array of close values  [n_companies x [n_close_observations]
        return(all_close_data)

