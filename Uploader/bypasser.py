import requests
import re
from bs4 import BeautifulSoup
from httpx import AsyncClient, Timeout


class Httpx:

    @staticmethod
    async def get(url: str, headers: dict = None, red: bool = True):
        async with AsyncClient() as ses:
            try:
                return await ses.get(url, headers=headers, follow_redirects=red, timeout=Timeout(10.0))
            except BaseException:
                pass


async def streamtape_bypass(url: str) -> str:
    
        response = await Httpx.get(url)
        if videolink := re.findall(r"document.*((?=id\=)[^\"']+)", response.text):
            return f"https://streamtape.com/get_video?{videolink[-1]}"
        return ""
    

async def mdisk_bypass(url: str) -> str:
    
        url = url[:-1] if url[-1] == "/" else url
        token = url.split("/")[-1]
        api = f"https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={token}"
        response = (await Httpx.get(api)).json()
        
        return response["download"].replace(" ", "%20")
    


async def mediafire_bypass(mediafire_url: str) -> str:
    
        link = re.search(r"\bhttps?://.*mediafire\.com\S+", mediafire_url)[0]
        page = BeautifulSoup((await Httpx.get(link)).content, "html.parser")
        return page.find("a", {"aria-label": "Download file"}).get("href")
    


async def anonfiles_bypass(anonfiles_url: str) -> str:
    soup = BeautifulSoup((await Httpx.get(anonfiles_url)).content, "html.parser")
    return dlurl["href"] if (dlurl := soup.find(id="download-url")) else ""
  

async def final_url(url: str) -> str:
        if 'https://anonfiles.com' in url:
            final_link = await anonfiles_bypass(url)
        elif '//bayfiles.com' in url:
            final_link = await anonfiles_bypass(url)
        elif 'mdisk.me' in url:
            final_link = await mdisk_bypass(url)
        elif 'streamtape' in url:
            final_link = await streamtape_bypass(url)
        elif 'mediafire.com' in url:
            final_link = await mediafire_bypass(url)
        else:
            final_link = url

        
        return final_link
    



import os

async def get_details(url):
    response = requests.head(url)
    if "Content-Disposition" in response.headers:
        try:
            filename = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
        except:
            filename = "Untitled"
    else:
        filename = url.split("/")[-1]

    # Extract the file size 
    if "Content-Length" in response.headers:
        file_size = int(response.headers["Content-Length"]) / 1024 / 1024
    else:
        file_size = None

   

    # Extract the file extension
    file_ext = os.path.splitext(filename)[1]

    # Strip double quotes and leading period from file extension
    file_ext = file_ext.strip('"').lstrip('.')

    # Set default file extension for PDF files
    if not file_ext:
        file_ext = "zip"

    
    filename = filename.strip('"')
    filename = filename+'.'+file_ext
   

    if file_size is not None:
        file_size = f"{file_size:.2f} MB"
    else:
        file_size = "00.0"

    return filename, file_size
