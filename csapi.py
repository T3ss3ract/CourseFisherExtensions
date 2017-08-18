import aiohttp
from time import localtime
import xml.etree.ElementTree as ElementTree

import re

_url_format = "https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{season}/{subject}/{course}/{crn}.xml"
_year = str(localtime().tm_year)
_season_resolver = {
    1: "spring",
    2: "spring",
    3: "fall",
    4: "fall",
    5: "fall",
    6: "fall",
    7: "fall",
    8: "fall",
    9: "fall",
    10: "spring",
    11: "spring",
    12: "spring",
    "FA": "fall",
    "SP": "spring",
    "SU": "summer",
    "WN": "winter"
}

async def get_crn_status(course: str) -> str:
    return (await get_course(course)).find("enrollmentStatus").text

async def get_course(course: str) -> ElementTree:
    """
    Get basic information about a course.
    Accepts a course string formatted like so:
    CS 374 FA17 CRN66445
    """
    url = _parse_course_string_to_url(course)
    return await _get_tree(url)


async def _get_tree(url: str) -> ElementTree:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return ElementTree.fromstring(await response.text())


def _parse_course_string_to_url(course: str)->str:
    """
    Get the URL for information about a course, given a course string.
    Accepts a course string formatted like so:
    CS 374 FA17 CRN66445
    :param course: The course string.
    :return: The information on the course
    """
    season, year = _extract_course_time(course)
    crn = _extract_crn(course)
    subject, course = _extract_course_name(course)
    url = _url_format.format(year=year, season=season, subject=subject, course=course, crn=crn)
    return url


def _extract_course_name(course_string:str)->(str,str):
    return re.sub("((FA|SP)[0-9]{2}|CRN[0-9]{5})", "", course_string).strip().split(" ")


def _extract_crn(course_string: str) -> str:
    res = re.search("CRN[0-9]{5}", course_string)
    crn = res.group(0)[3:]
    return crn


def _extract_course_time(course_string: str) -> (str, str):
    global _season_resolver
    res = re.search("(FA|SP)[0-9][0-9]", course_string)
    if res is not None:
        time = res.group(0)
        season = _season_resolver[time[0:2]]
        year = "20" + time[2:]
    else:
        season = _season_resolver[localtime().tm_mon]
        year = _year
    return season, year


