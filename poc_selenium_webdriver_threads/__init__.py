import app
from threading import Thread

if __name__ == "__main__":
    # Browser and home page url
    data = {
        "chrome": "https://apps.crengland.com/portal/",
    }

    """data = {
        "safari": "https://apps.crengland.com/portal/",
        "firefox": "https://apps.crengland.com/portal/",
        "chrome": "https://apps.crengland.com/portal/",
    }"""

    # Build thread
    threads = []
    for b, url in data.items():
        t = Thread(target=app.test_career_portal_yes_violations_path, args=(b, url))
        threads.append(t)

    # Start all threads
    for thr in threads:
        thr.start()
