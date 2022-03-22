import asyncio

from arsenic import services, browsers, get_session, keys


class ArsenicApi:
    def __init__(self, loop, path_to_driver):
        self.loop = loop
        self.GECKODRIVER = f'{path_to_driver}'

    async def main_config(self):
        service = services.Chromedriver(binary=self.GECKODRIVER)
        browser = browsers.Chrome()
        # browser.capabilities = {"goog:chromeOptions": {
        #     "args": ["--headless", "--no-sandbox", "--disable-dev-shm-usage", "--log-path", "/dev/null"]}}
        return get_session(service, browser)
