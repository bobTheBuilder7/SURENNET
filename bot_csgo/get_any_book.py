import asyncio
from pyppeteer import launch
from aiohttp import ClientSession
from lxml import html
from lxml.html.clean import clean_html

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.1 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru', 'dnt': '1', "Connection": "keep-alive"}


async def fetch_freebookspot(bookname):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('http://www.freebookspot.club', timeout=0, waitUntil='domcontentloaded')
    await page.waitForSelector('#TTitleSearch')
    await page.evaluate('''(bookname) => {
            document.getElementById('TTitleSearch').value = bookname
            document.getElementById('BSearch').click()
        }''', bookname)
    await asyncio.sleep(1)
    urls = []
    try:
        for i in range(2, 100):
            text = await page.Jeval(f'#GridView2 > tbody > tr:nth-child({i}) > td:nth-child(6) > a', 'el => el.href')
            urls.append(text)
    except:
        pass
    await browser.close()
    return urls


async def fetch_libgen(bookname):
    async with ClientSession(headers=headers) as session:
        async with session.get(
                f'http://libgen.rs/search.php?req={bookname}&open=0&res=50&view=simple&phrase=1&column=def') as response:
            content = await response.text()
            urls = []
            tree = html.document_fromstring(clean_html(content))
            for j in tree.iterlinks():
                if 'index.php?md5' in j[2]:
                    urls.append('https://libgen.rs/' + j[2])
            return urls


async def fetch_epdf(bookname):
    async with ClientSession(headers=headers) as session:
        async with session.get(f'https://epdf.pub/search/{bookname}') as response:
            content = await response.text()
            urls = []
            tree = html.document_fromstring(clean_html(content))
            if len(tree.find_class('more-link')) > 0:
                for i in tree.find_class('more-link'):
                    for j in i.iterlinks():
                        urls.append(j[2])
            return urls


async def fetch_zlib(bookname):
    async with ClientSession(headers=headers) as session:
        async with session.get(
                f'https://3lib.net/s/{bookname}') as response:
            content = await response.text()
            urls = []
            tree = html.document_fromstring(clean_html(content))
            for j in tree.iterlinks():
                if '/book/' in j[2]:
                    urls.append('https://3lib.net' + j[2])
            return urls


async def fetch_openlibrary(bookname):
    async with ClientSession(headers=headers) as session:
        async with session.get(
                f'https://openlibrary.org/search?q={bookname}&mode=ebooks&has_fulltext=true') as response:
            content = await response.text()
            urls = []
            tree = html.document_fromstring(clean_html(content))
            for j in tree.iterlinks():
                if '/borrow/ia/' in j[2] and '_autoReadAloud=show' not in j[2]:
                    urls.append('https://openlibrary.org/' + j[2])
            return urls


async def fetch_manybooks(bookname):
    async with ClientSession(headers=headers) as session:
        async with session.get(f'https://manybooks.net/search-book?search={bookname}') as response:
            content = await response.text()
            urls = []
            tree = html.document_fromstring(clean_html(content))
            for j in tree.iterlinks():
                if '/titles/' in j[2]:
                    urls.append('https://manybooks.net' + j[2])
            return urls


async def main(booky):
    suren = await asyncio.gather(fetch_libgen(booky),
                                 fetch_zlib(booky),
                                 fetch_epdf(booky),
                                 fetch_openlibrary(booky),
                                 fetch_freebookspot(booky),
                                 fetch_manybooks(booky))
    print(suren)


asyncio.run(main("Бен-Гурион - создатель Израиля"))
