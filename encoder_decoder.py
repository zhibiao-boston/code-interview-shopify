class Codec:
    def __init__(self):
        self.url_to_code = {}
        self.code_to_url = {}
        self.counter = 0
        self.base = "http://tinyurl.com/"
    
    def encode(self, longUrl):
        if longUrl in self.url_to_code:
            return self.base + self.url_to_code[longUrl]
        
        code = str(self.counter)
        self.counter += 1
        self.url_to_code[longUrl] = code
        self.code_to_url[code] = longUrl

        return self.base + code

    def decode(self, shortUrl):
        code = shortUrl.replace(self.base, '')
        return self.code_to_url[code]


