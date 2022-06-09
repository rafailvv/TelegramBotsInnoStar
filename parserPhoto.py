import requests
import lxml, bs4
import pprint
from PIL import Image
import os



class Parser(object):

    def __init__(self, inquiry: str):
        total_inquiry = str("+".join(inquiry.split()))
        self.pre = "https://www.google.com"
        if self.pre not in inquiry:
            self.inquiry = f"""https://www.google.com/search?q={total_inquiry}"""
        else:
            self.inquiry = inquiry
        self.headers = {
            "Accept": "* / *",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }

        self.html_text = requests.get(self.inquiry, self.headers).text
        self.soup = bs4.BeautifulSoup(self.html_text, "lxml")  # полученный код штмл странички


class MainPage(Parser):
    def __init__(self, inquiry: str):
        super().__init__(inquiry)
        self.up_tools = []
        self.up_link = []
        self.content = {}

    def main_page_tools(self):
        self.up_tools = self.soup.find_all("a", class_="eZt8xd")
        self.up_link = [i.get("href") for i in self.up_tools]
        itog = []
        for i in self.up_link:
            itog.append(self.pre + i)

        return itog

    def main_page_content(self):
        link = self.soup.find_all("div", class_="egMi0 kCrYT")
        head = self.soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")
        out = {}

        for i in range(len(link)):
            out[(str(link[i])[str(link[i]).rfind('href="/url?q='): str(link[i]).find('"><h3 class="zBAuLc l97dzf">')])[13:]] = str(head[i])[34:-6]

        return out


class ImageParsing(MainPage):
    """ It downloads images """

    def __init__(self, inquiry: str):
        super().__init__(inquiry)
        inquiry = inquiry
        parser = MainPage(inquiry)

        for _ in parser.main_page_tools():
            if "tbm=isch" in _:
                self.image_link = _
        self.image_parser = Parser(str(self.image_link))
        self.image_soup = self.image_parser.soup
        self.links = [i.get("src") for i in self.image_soup.find_all("img", class_="yWs4tf")]

    def parse_links(self):
        return self.links


    def download_image(self, url, name):

        """it works. Sorry, mr Trump, I regret that my code is so bad"""
        img = requests.get(url)
        img_file = open(name, 'wb')
        img_file.write(img.content)
        img_file.close()
        dog_jpg = Image.open(name)
        dog_jpg.save(f'images/{name}.png', format='PNG')
        try:
            os.remove(name)
        except: pass
        return open(f'images/{name}.png', 'rb')


if __name__ == "__main__":

    impa = ImageParsing(input())
    pprint.pprint(impa.parse_links())
    for image in range(1):
        impa.download_image(impa.parse_links()[image], "image" + str(image))