import requests
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def create_notion_page(title: str, url: str) -> None:
    create_url = "https://api.notion.com/v1/pages"

    properties = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": url
            }
        }
    }

    try:
        res = requests.post(create_url, headers=headers, json=properties)
        if res.status_code == 200:
            logger.info(f"{res.status_code}: Page created successfully")
        else:
            logger.error(f"{res.status_code}: Error during page creation")
        return
    except Exception as e:
        logger.error(e)
