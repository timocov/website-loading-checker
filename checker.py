import os
import sys
from pytz import utc
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def is_error_entry(entry):
    level = entry.get('level', '')
    message = entry.get('message', '')

    # message about missing favicon.ico is not an error :-)
    return level == 'SEVERE' and message.find('favicon.ico') == -1


def timestamp_to_str(timestamp):
    return datetime.fromtimestamp(timestamp, tz=utc).isoformat('T')


def entry_to_str(entry):
    return '{0} - {1}'.format(
        timestamp_to_str(entry.get('timestamp', 0L) / 1000),
        entry.get('message', '')
    )


def check_error_in_log(driver):
    print('  Checking browser log...')

    logs = []
    has_errors = False

    for entry in driver.get_log('browser'):
        log_message = entry_to_str(entry)

        if is_error_entry(entry):
            log_message = 'ERROR: {0}'.format(log_message)
            has_errors = True

        logs.append('      {0}'.format(log_message))

    if has_errors:
        print('    Browser logs has error(s):')
        print('\n'.join(logs))
        return False

    return True


SLEEP_TIME_SEC = 3


def enable_all_browser_logs(capabilities):
    logging_preferences_key = 'loggingPrefs'

    logging_preferences = capabilities.get(logging_preferences_key, {})
    logging_preferences['browser'] = 'ALL'
    capabilities[logging_preferences_key] = logging_preferences


def main():
    assert(len(sys.argv) > 1)
    hub_url = os.environ['HUB_URL']

    assert(hub_url is not None and len(hub_url) != 0)

    success = True
    urls = sys.argv[1:]

    driver = None
    for url in urls:
        try:
            print('Loading "{0}"'.format(url))

            capabilities = DesiredCapabilities.CHROME.copy()
            enable_all_browser_logs(capabilities)

            driver = webdriver.Remote(
                command_executor=hub_url,
                desired_capabilities=capabilities)

            driver.get(url)

            # wait until JavaScript do self dirty work at load page
            print('  Sleeping {0} sec...'.format(SLEEP_TIME_SEC))
            sleep(SLEEP_TIME_SEC)

            success = check_error_in_log(driver) and success
        finally:
            if driver:
                driver.close()

    exit(0 if success else 1)


if __name__ == '__main__':
    main()
