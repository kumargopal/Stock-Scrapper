from stock import Stock
import time
import numpy as np
from datetime import datetime

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})


def main():

    stock_obj = Stock()

    # Running the 200 time with sleep time = 30 sec
    for i in range(200):

        if(i == 0):
            # Initial stock data
            curr_stock = stock_obj.get_stock_data()

        time.sleep(30)
        
        # Updated stok after 30 sec
        new_stock = stock_obj.get_stock_data()       

        is_same = np.array(new_stock) == np.array(curr_stock) 

        # If the stock data has changed
        if not is_same.all():

            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")

            # Saving the csv file with name time(replaced ':' by '_').csv
            csv_file_name = 'stock_data/'+current_time.replace(':','_')+'.csv'

            curr_stock.to_csv(csv_file_name)

            # As the stock data has changed, let's update the curr_stock as new_stock
            curr_stock = new_stock

            print('Stock data has changed at : ',current_time)

        else:

            print('No change in Data!')
        break

if __name__ == '__main__':
    print('Initialising...')
    main()

    