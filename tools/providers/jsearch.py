#
#  Copyright (c) 2026
#  Minh NGUYEN <vnguyen9@lakeheadu.ca>
#
from __future__ import annotations

import json
import os

import requests

from typing import Any, Dict, List, Optional
from enum import Enum


class DatePostedEnum(str, Enum):
    ALL = "all"
    TODAY = "today"
    THREE_DAYS = "3days"
    WEEK = "week"
    MONTH = "month"


def jsearch_tool(
    query: str,
    page: int = 1,
    num_pages: int = 1,
    country: str = "ca",
    location: Optional[str] = None,
    date_posted: str | DatePostedEnum = DatePostedEnum.THREE_DAYS,
    work_from_home: bool = True,
    employment_types: Optional[List[str] | str] = None,
    job_requirements: Optional[str] = None,  # "under_3_years_experience", v.v.
    fields: Optional[str] = None
) -> Dict[str, Any] | str:
    """
    Search for job postings globally using the JSearch API.

    This method aggregates job listings from 100+ sources including LinkedIn, Indeed,
    and Glassdoor. It is highly optimized for finding real-time employment opportunities.

    Args:
        query (str): The primary search string. For best results, combine job title,
            skills, and location.
            Examples: "Frontend Developer in Toronto", "Python AWS via LinkedIn".
        page (int): The specific results page to retrieve. Each page contains 10 jobs.
            Range: 1 to 50. Default: 1.
        num_pages (int): Total number of pages to fetch starting from `page`.
            Note: Each page consumed counts as 1 API credit. Default: 1.
        country (str): Two-letter ISO 3166-1 alpha-2 country code.
            Essential for localized results (e.g., 'ca' for Canada, 'us' for USA).
        location (str, optional): Geographical context for the search (Google UULE).
            Useful if not already specified in the query.
        date_posted (Union[DatePostedEnum, str]): Temporal filter for listings.
            Options: 'all', 'today', '3days', 'week', 'month'. Default: '3days'.
        work_from_home (bool): Filter for remote positions. If True, returns only
            Work-From-Home roles. Default: True.
        employment_types (Union[List[str], str], optional): Filter by job nature.
            Allowed values: FULLTIME, CONTRACTOR, PARTTIME, INTERN.
            Can be a list or a comma-separated string.
        job_requirements (Union[List[str], str], optional): Filter by experience or
            education. Allowed values: 'no_experience', 'under_3_years_experience',
            'more_than_3_years_experience', 'no_degree'.
        fields (str, optional): A comma-separated list of specific data fields to
            include in the response (e.g., 'job_title,employer_name,job_apply_link').

    Returns:
        Dict[str, Any]: A dictionary containing a list of job objects under the 'data' key
            or error details if the request fails.
    """
    jsearch_api_key = os.environ.get("RAPIDAPI_API_KEY")
    host: str = "jsearch.p.rapidapi.com"
    url: str = f"https://{host}/search-v2"

    headers = {
        "x-rapidapi-key": jsearch_api_key,
        "x-rapidapi-host": host,
        "Content-Type": "application/json"
    }

    params = {
        "query": query,
        "page": str(page),
        "num_pages": str(num_pages),
        "country": country,
        "location": location,
        "date_posted": date_posted,
        "work_from_home": str(work_from_home).lower(),
        "fields": fields
    }

    if employment_types and isinstance(employment_types, list):
        params["employment_types"] = ",".join(employment_types)

    if job_requirements and isinstance(job_requirements, list):
        params["job_requirements"] = ",".join(job_requirements)

    try:
        response = requests.get(
            url=url,  params=params, headers=headers)

        if response.status_code == 200:
            return json.dumps(response.json(), indent=2)
        else:
            return {"error": f"Error {response.status_code}", "detail": response.text}
    except Exception as e:
        return {"error": "Connection Error", "detail": str(e)}


JSEARCH_SCHEMA = {
    "name": "jsearch",
    "description": (
        "Search for job postings globally using the JSearch API. "
        "This method aggregates job listings from 100+ sources including LinkedIn, Indeed, "
        "and Glassdoor. It is highly optimized for finding real-time employment opportunities."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Free-form jobs search query. It is highly recommended to include job title and location as part of the query. Examples: 'web development jobs in chicago', 'marketing manager in new york via linkedin'."
            },
            "page": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 1,
                "description": "The specific results page to retrieve. Each page contains 10 jobs. Range: 1 to 50."
            },
            "num_pages": {
                "type": "integer",
                "minimum": 1,
                "maximum": 20,
                "default": 1,
                "description": "Maximum number of pages to return starting from page. Each page (containing up to 10 results) returned by the API consumes one request credit."
            },
            "country": {
                "type": "string",
                "default": "ca",
                "description": "Country code of the country from which to return job postings. Must be set to get jobs in a specific country. Example: 'ca' for Canada, 'us' for USA, 'de' for Germany. See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 for allowed values."
            },
            "location": {
                "type": ["string", "null"],
                "default": None,
                "description": "The location from which the search is made (Google's UULE parameter) - e.g., 'New York, United State'."
            },
            "date_posted": {
                "type": ["string", "null"],
                "enum": ["all", "today", "3days", "week", "month"],
                "default": "3days",
                "description": "Find jobs posted within the time you specify. Allowed values: all, today, 3days, week, month."
            },
            "work_from_home": {
                "type": "boolean",
                "default": True,
                "description": "Only return work from home / remote jobs."
            },
            "employment_types": {
                "oneOf": [
                    {"type": "array", "items": {"type": "string", "enum": ["FULLTIME", "CONTRACTOR", "PARTTIME", "INTERN"]}},
                    {"type": "string"}
                ],
                "default": None,
                "description": "Find jobs of particular employment types, specified as a comma delimited list of the following values: FULLTIME, CONTRACTOR, PARTTIME, INTERN."
            },
            "job_requirements": {
                "type": ["string", "null"],
                "enum": ["no_experience", "under_3_years_experience", "more_than_3_years_experience", "no_degree"],
                "default": None,
                "description": "Find jobs with specific requirements, specified as a comma delimited list of the following values: under_3_years_experience, more_than_3_years_experience, no_experience, no_degree."
            },
            "fields": {
                "type": ["string", "null"],
                "default": None,
                "description": "A comma separated list of job fields to include in the response (field projection). By default all fields are returned."
            }
        },
        "required": ["query"]
    }
}

if __name__ == "__main__":
    from hermes_cli.config import reload_env
    reload_env()
    print(jsearch_tool(
        query="AI Interns",
        country="Canada"
    ))
