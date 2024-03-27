cd ../

python -m unittest test/test_config_parser.py
python -m unittest test/test_csv_parser.py
python -m unittest test/test_downloader.py
python -m unittest test/test_env_util.py
python -m unittest test/test_file_logger.py
python -m unittest test/test_file_util.py
python -m unittest test/test_output_generator.py
python -m unittest test/test_wordcloud_generator.py

$SHELL