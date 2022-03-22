import asyncio

from arsenic import services, browsers, get_session, keys


class ArsenicApi:
    def __init__(self, loop):
        self.loop = loop
        self.GECKODRIVER = './chromedriver'

    async def main_config(self):
        print(self.GECKODRIVER)
        service = services.Chromedriver(binary=self.GECKODRIVER)
        browser = browsers.Chrome()
        browser.capabilities = {"goog:chromeOptions": {
            "args": ["--headless", "--no-sandbox", "--disable-dev-shm-usage", "--log-path", "/dev/null"]}}
        return get_session(service, browser)
