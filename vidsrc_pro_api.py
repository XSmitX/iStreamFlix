import aiohttp
from bs4 import BeautifulSoup

class VidSrcProAPI:
    async def check_html_class(self, url, class_name):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    return bool(soup.find('html', class_=class_name))
                else:
                    return False

    async def check_class_sync(self, url, class_name):
        return await self.check_html_class(url, class_name)
