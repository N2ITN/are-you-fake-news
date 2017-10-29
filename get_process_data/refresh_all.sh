cd ..
python3 newscraper/get_process_data/mongo_driver.py --kill articles
python3 newscraper/get_process_data/webcrawler.py
python3 newscraper/get_process_data/group_articles_by_flag.py
python3 newscraper/get_process_data/lemmatize_articles.py
python3 newscraper/get_process_data/NLP_machine.py
cd newscraper