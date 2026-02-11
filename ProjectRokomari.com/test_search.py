import time
import pytest
from PageObject.rokomari_home_page import HomePage


@pytest.mark.usefixtures("setup_and_teardown")
class TestSearch:

    def test_search_valid_keyword_bangla(self):
        home = HomePage(self.driver)
        home.search("পথের পাঁচালী")
        time.sleep(2)

        assert home.is_title_present("পথের পাঁচালী")

    def test_search_valid_keyword_english_enter(self):
        home = HomePage(self.driver)
        home.search("Pather Panchali")
        time.sleep(2)

        titles = home.get_result_titles()
        assert any("panchali" in t.lower() for t in titles)

    def test_search_partial_bangla_keyword(self):
        home = HomePage(self.driver)
        home.search("পথের")
        time.sleep(2)

        assert home.is_title_present("পথের")


    def test_search_invalid_bangla_keyword(self):
        home = HomePage(self.driver)

        home.search("আসদফঘহজ")
        time.sleep(2)

        no_result_text = home.get_no_result_text()
        assert "no result found" in no_result_text.lower()


    def test_search_empty_input(self):
        home = HomePage(self.driver)
        home.empty_search()
        time.sleep(1)

        assert home.get_validation_message() == "Please fill out this field."

    def test_search_special_chars(self):
        home = HomePage(self.driver)
        home.search("&")
        time.sleep(2)

        titles = home.get_result_titles()
        if titles:
            assert True
        else:
            msg = home.get_no_result_text()
            assert "no result found" in msg.lower()
