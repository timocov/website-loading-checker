import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def check_error_in_log(driver):
    print('  Checking log...')

    logs = []
    errors = []
    for entry in driver.get_log('browser'):
        source = entry.get('source', '')
        message = entry.get('message', '')
        logs.append('       {0}: {1}'.format(source, message))

        # accept errors only (without message about favicon.ico)
        if entry['level'] == 'SEVERE' and entry['message'].find('favicon.ico') == -1:
            errors.append('      Source: {0}, Message: {1}'.format(source, message))

    if len(errors) != 0:
        print('    Has error(s):')
        print('\n'.join(errors))
        print('    Full logs:')
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
