from selenium import webdriver

# from selenium.webdriver.chrome.service import Service as ChromeService


class Browser(object):
    def __init__(self, envision_port, init_pause_state=True):
        if envision_port is None:
            envision_port = 8081
        self._port = envision_port
        self._paused = init_pause_state

        options = webdriver.ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
        )
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=0")
        options.add_argument("--window-size=1400x1080")

        # service = ChromeService(executable_path'/usr/local/bin/chromedriver')

        self._driver = webdriver.Chrome(options=options)
        self._driver.get(f"http://localhost:{envision_port}")

    def get_paused(self):
        for entry in self._driver.get_log("browser"):
            if entry["source"] == "console-api":
                # print(entry)
                if (
                    entry["message"]
                    == f"http://localhost:{envision_port}/main.js 384:88417 true"
                ):
                    self._paused = True
                    return self._paused
                elif (
                    entry["message"]
                    == f"http://localhost:{envision_port}/main.js 384:88417 false"
                ):
                    self._paused = False
                    return self._paused

        return self._paused