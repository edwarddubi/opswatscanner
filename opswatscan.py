import requests


class OPSWATSCAN:
    def __init__(self) -> None:
        pass

    def __init__(self, api_key, filename) -> None:
        self.api_key = api_key
        self.filename = filename

    def read_file(self):
        data=None
        try:
            f= open(self.filename,'r')
            data = f.read()
        except FileNotFoundError as e:
            print("File does not exist.\n")
        finally:
            f.close()

        return data

    def test_api(self):
        link = "https://api.metadefender.com/v4/hash/66DA1A91E1ED5D59BECFAD85F53C05F9"
        m_params = {
            "apikey":self.api_key
        }

        res = requests.post(url=link, params=m_params)
        print(res.json())


    def scan_file(self):
        content = self.read_file()
        #print(content)