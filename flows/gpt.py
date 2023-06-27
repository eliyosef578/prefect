import prefect
from prefect import task, Flow, flow, get_run_logger
import aiohttp
import asyncio
import wikipediaapi
import whois
import s3fs
from datetime import datetime

@task
async def get_current_time():
    logger = get_run_logger()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logger.info(f'time is: {current_time}')
    return current_time

@task
async def check_website(url):
    logger = get_run_logger()
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                logger.info(f'website: {url} is exists')
                return resp.status == 200
        except:
            logger.info(f'website: {url} doesnot exists')
            return False
@task
async def find_owners(url):
    # code to find owners of the website goes here
    logger = get_run_logger()
    details = whois.whois(url)
    logger.info(details['org'])
    return details['org']

@flow
async def check_wikipedia(owner):
    
    logger = get_run_logger()
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(owner)
    if page_py.exists():
        logger.info(f'owner {owner} is exists')
        return True
    logger.info(f'!!!!!!!!!!!!!!!!!!')
    get_current_time()
    logger.info(f'$$$$$$$$$$$$$$$$$$$$$$$')
    return False

@flow(name="gpt")
async def gpt(websites = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.facebook.com",
    "https://www.baidu.com",
    "https://www.wikipedia.org",
    "https://www.qq.com",
    "https://www.amazon.com",
    "https://www.taobao.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.sohu.com",
    "https://www.reddit.com",
    "https://www.linkedin.com",
    "https://www.yahoo.com",
    "https://www.bing.com",
    "https://www.aliexpress.com",
    "https://www.netflix.com",
    "https://www.microsoft.com",
    "https://www.office.com"
]):
#with Flow("gpt") as flow:
    logger = get_run_logger()
    for web in websites:
        logger.info(f'start check {web}')
        #websites = prefect.Parameter("websites")
        website_status = await check_website(web)
        owner = await find_owners(web)
        wikipedia_status = await check_wikipedia(owner)

    #website_status | owners | wikipedia_status

#flow.run(websites=["https://www.google.com", "https://www.facebook.com"])
# if __name__ == "main":
#     asyncio.run(gpt())