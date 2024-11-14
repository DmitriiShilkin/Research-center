# Маркетплейсы для поиска
URLS = {
    "wildberries": "https://www.wildberries.ru",
    "ozon": "https://www.ozon.ru",
    "yandex": "https://market.yandex.ru"
}
# Ключевые слова для поиска
KEY_WORDS = ["копье", "дуршлаг", "красные носки", "леска для спиннинга"]
# Максимальное время ожидания веб-драйвером загрузки элемента страницы (секунды)
WEB_DRIVER_WAIT_MAX_TIMEOUT = 15
# Максимальное время ожидания загрузки страницы (секунды)
PAGE_LOAD_WAIT_MAX_TIMEOUT = 10
# Пауза между загрузкой формы и отправкой поискового запроса (секунды)
KEYWORD_SEND_TIMEOUT = 1
# Selenium Grid hub URL
GRID_HUB_URL = "http://selenium-hub:4444/wd/hub"
