# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 22:59:15 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 8

@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import MLforTrading as ml #custom library

class portifolio(ml.df_4_trading):
    
    def allocate(self, columns, percentage, date_of_allocation, volume_allocated=1):
        """"Creates a dataframe with the allocation for each stock.
        Input:
            columns: [["ABC","XYZ","GGG","LOVE"]] stocks where there is some 
                allocation;
            percentages: {"ABC": 0.1,"XYZ: 0.3","GGG": 0.2,"LOVE": 0.4} a dict 
                with the percentages for each stock.
            date_of_allocation: date in which the stocks were bought.
            volume_allocated: total ammount allocated, if not filled the 
                dataframe self.allocation shows the percentages of allocation.
        """
        self.date_of_allocation = date_of_allocation
        if sum(percentage.values()) != 1:
            print (f"Percentages sum up to {sum(percentages.values())} != 1.")
            print ("Please correct the percentages and call callocate again")

        else:
            self.allocation = self.normalize_data(self.df[date_of_allocation:self.end_date][columns].copy())
            for symbol in percentage:
                self.allocation[symbol] *= percentage[symbol]
            self.invested_dates = pd.date_range(date_of_allocation, self.end_date)
            total = pd.DataFrame(data = self.allocation.sum(axis=1), columns = ["Total"])
            self.allocation = self.allocation.join(total)
            self.allocation *=volume_allocated
            self.add_daily_return()
            
    def add_daily_return(self):
        daily_returns = pd.DataFrame(index = self.allocation.index)
        daily_returns["Daily R"] = self.allocation["Total"].copy()
                                     
        daily_returns["Daily R"].iloc[1:] = (self.allocation["Total"]/self.allocation["Total"].shift()) -1
        daily_returns["Daily R"].iloc[0] = 0

        self.allocation = self.allocation.join(daily_returns)
    
    def portifolio_statistics(self, date):
        cumulative_daily_return = self.allocation[self.date_of_allocation]["Daily R"]/self.allocation[date]["Daily R"]
        
        average_daily_return = self.allocation["Daily R"].mean()
        
    
def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    p = portifolio(symbols, start_date, end_date)
    investments = {"HCP": 0.1, "IBM": 0.2, "AAPL":0.7}
    p.allocate(list(investments.keys()), investments, "2014-01-01", 100)

    #print(p.df.head())
    print(p.allocation.head(10))
    #p.add_daily_return()
    #print("portifolio \n", p.allocation.head(10))
    
    #df = p.allocation["Total"].copy()
    #df.iloc[1:]  = (p.allocation["Total"]/p.allocation["Total"].shift()) -1
    #df.iloc[0] = 0
    #print(df.head())
    

    
if __name__ == "__main__":
    test_run()