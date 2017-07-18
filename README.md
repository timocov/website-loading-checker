# website-loading-checker
This is simple tool for web pages availability checking.
Using Selenium WebDriver (via Selenium Hub) for open pages and check logs.

## Requirements:
### Python:
see `requirements.txt`

### Binary
```
chromedriver in PATH
```

## Usage
```
pip install -r requirements.txt
export HUB_URL=my-selenium-hub.hostname.com
python checker.py http://google.com https://github.com/timocov https://translate.google.ru
```
