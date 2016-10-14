import sys
from time import sleep
from selenium import webdriver


def check_error_in_log(driver):
    print('  Checking log...')

    errors = []
    for entry in driver.get_log('browser'):
        # accept errors only (without message about favicon.ico)
        if entry['level'] == 'SEVERE' and entry['message'].find('favicon.ico') == -1:
            errors.append('      Source: {0[source]}, Message: {0[message]}'.format(entry))

    if len(errors) != 0:
        print('    Has error(s):')
        for error in errors:
            print(error)

        return False

    return True


SLEEP_TIME_SEC = 3


def main():
    assert(len(sys.argv) > 1)

    success = True
    urls = sys.argv[1:]

    for url in urls:
        try:
            print('Loading "{0}"'.format(url))

            driver = webdriver.Chrome()
            driver.get(url)

            # wait until JavaScript do self dirty work at load page
            print('  Sleeping {0} sec...'.format(SLEEP_TIME_SEC))
            sleep(SLEEP_TIME_SEC)

            success = check_error_in_log(driver) and success
        finally:
            driver.close()

    exit(0 if success else 1)


if __name__ == '__main__':
    main()
