from prefect import flow, task, get_run_logger, Task
import logging
import requests
import asyncio
import aiohttp
import time


from prefect.filesystems import RemoteFileSystem
remote_file_system_block = RemoteFileSystem.load("minio")

#@task
#def check_url(url_name):
#    logger = get_run_logger()
#    response = requests.get(f'http://www.{url_name}')
#    logger.info(f'================================================')
#    url = url_name.split(".")[0]
#    try:
#        if response.status_code == 200:
#            print(f'Web site: {url_name} exists')
#            logger.info(f'Web site: {url_name} exists')
#            return url
#        else:
#            print(f'Web site: {url_name} does not exist') 
#            logger.info(f'Web site: {url_name} does not exist')
#            return url
#    except:
#        logger.error(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

@task
async def check(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{name}.com') as response:
            if response.status == 200:
                print("Status:", response.status)
                logger = get_run_logger()
                logger.info(f'status is: {str} for {name} site!')
                return response
            else:
                print("Status:", response.status)
                logger.info(f'status is: {str} for {name} site!')
                return response

# function which return reverse of a string
@task  # (name="palindrome")
async def isPalindrome(str):
    logger = get_run_logger()
    logger.info(f'&&&&&&&& {str} &&&&&&&&&&&&')
    # Run loop from 0 to len/2
    for i in range(0, int(len(str)/2)):
        if str[i] != str[len(str)-i-1]:
            print("is not palindrome")
            logger.info(f"{str} is not palindrome :(")
            return False
    print("is palindrome")
    logger.info(f"{str} is palindrome :)")
    return True

#@flow(name="sub flow test")
#def websites(names=["walla.com", "google.com", "one.co.il", "wix.com", "balbal.co"]):
#    for name in names:
#        site = check_url(name)
#        isPalindrome(site)




start_time = time.time()

@flow
async def rest():

    async with aiohttp.ClientSession() as session:
        logger = get_run_logger()
        for number in range(1, 5):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                print(pokemon['name'])
                logger.info(f"{pokemon['name']} !!!!!!!")
                #isPalindrome(pokemon['name'])
                name = pokemon['name']
                pal = await isPalindrome(name)
                site = await check(name)
                if site.status == 200:
                    print("Status:", site.status)
                    logger.info(f'status is: {str} for {name} site!')
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "main":
    asyncio.run(rest())

