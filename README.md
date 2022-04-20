# Programming for data science

This project is the implementation of the final project for UPM Programming for Data Science course.

Project contains three directories:
        
<ul>
    <li><b>Analysis</b> - this part covers data analysis part and it contains only Portfolio_data_analysis.ipynb notebook file</li>
    <li><b>Portfolio</b> - here we covered the data generation part, it contains portfolio.py, portfolio_performance.py and test for portfolio performance, as well two csv files generated after running portfolio_performance.py file.</li>
    <li><b>Scraping</b> - this directory contains data_scraping.py file with the scrip for the first part of the assigment as well as chromedriver.exe required to run selenium code. More than that after executing data_scraping.py there should appear csv files with the data scraped.</li>
</ul>

In order to run the  code it's needed to run the python files: data_scraping.py for scraping part,
portfolio_performance.py for data generation part and open the Portfolio_data_analysis.ipynb 
notebook file and run it in jupyter.

The following anaconda environment with python 3.10 version, and the following packages installed are required:

Package              Version
-------------------- ---------
jsonschema           4.4.0
jupyter-client       7.1.2
jupyter-core         4.9.2
jupyterlab-pygments  0.1.2
lxml                 4.8.0
matplotlib           3.5.1
matplotlib-inline    0.1.2
notebook             6.4.8
numpy                1.21.5
pandas               1.4.1
pip                  21.2.4
pipenv               2021.5.29
scipy                1.7.3
seaborn              0.11.2
selenium             3.141.0
virtualenv           20.4.7
webdriver-manager    3.5.4



