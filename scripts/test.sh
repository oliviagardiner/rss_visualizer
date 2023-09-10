cd ../

python -m unittest tests.config_parser_test
python -m unittest tests.csv_parser_test
python -m unittest tests.downloader_test
python -m unittest tests.env_util_test
python -m unittest tests.file_logger_test
python -m unittest tests.file_util_test
python -m unittest tests.output_generator_test

$SHELL