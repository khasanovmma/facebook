from arsenic import services, browsers, get_session


class ArsenicApi:
    def __init__(self, loop, path_to_driver):
        self.loop = loop
        self.GECKODRIVER = f'{path_to_driver}'

    async def main_config(self):
        service = services.Chromedriver(binary=self.GECKODRIVER)
        browser = browsers.Chrome()

        browser.capabilities = {
            "browserName": "chrome",
            "chromeOptions": {
                "args": ["--disable-extensions", "--disable-gpu","--no-sandbox", "--headless", "--disable-notifications"]
            }
        }
        return get_session(service, browser)
