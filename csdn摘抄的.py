import requests
from bs4 import BeautifulSoup


class ScienceDirect:

    def __init__(self, journal):
        self.subject = journal
        self.base_url = 'https://www.sciencedirect.com'

    def latest_issue(self):
        content = ''
        url = self.base_url + '/journal/' + self.subject
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

        re = requests.get(url, headers=headers)
        soup = BeautifulSoup(re.text, 'html.parser')

        real_url = self.base_url + soup.find_all('div', class_='u-margin-s-top issue')[2].find('a')['href']
        real_re = requests.get(real_url, headers=headers)
        real_soup = BeautifulSoup(real_re.text, 'html.parser')

        articles = real_soup.find_all('li', class_='js-article-list-item article-item u-padding-xs-top u-margin-l-bottom')
        volume = real_soup.find('h2', class_='u-text-light u-h1 js-vol-issue').text
        dates = real_soup.find('h3', class_='js-issue-status text-s').text
        subject = '{} {} {}'.format(self.subject, volume, dates)

        for article in articles:
            title = article.find('span', class_='js-article-title').text
            link = self.base_url + article.find('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom')['href']
            content += '{}\n{}\n'.format(title, link)
        return subject, content


if __name__ == '__main__':
    s, c = ScienceDirect('earth-science-reviews').latest_issue()
    print(s)
    print(c)
