#
#  Copyright (c) 2026
#  Minh NGUYEN <vnguyen9@lakeheadu.ca>
#
from __future__ import annotations

import json
import requests
import httpx

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, ConfigDict, model_validator, SecretStr


class LinkedInWrapper(BaseModel):
    """Wrapper for LinkedIn API."""
    linkedin_api_key: SecretStr
    days_7_url: str = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
    hours_24_url: str = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-24h"
    host: str = "linkedin-job-search-api.p.rapidapi.com"

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def validate_environments(cls, values: Dict) -> Any:
        linkedin_api_key = get_from_dict_or_env(
            values, "linkedin_api_key", "LINKEDIN_API_KEY"
        )

        values['linkedin_api_key'] = linkedin_api_key

    def get_jobs_in_duration(
        self,
        title: str,
        location: str = "Canada",
        limit: int = 10,
        offset: int = 0,
        remote_only: bool = False,
        employment_types: Optional[List[str]] = None,  # Ví dụ: ["FULL_TIME", "CONTRACTOR"]
        experience_level: Optional[str] = None,  # Ví dụ: "0-2" hoặc "5-10"
        duration: str = 'days',
    ):

        if duration == 'hours':
            url = self.hours_24_url
        else:
            url = self.days_7_url

        headers = {
            "X-RapidAPI-Key": self.linkedin_api_key.get_secret_value(),
            "X-RapidAPI-Host": self.host,
            "Content-Type": "application/json"
        }

        # 2. Xây dựng Query Params dựa trên tài liệu bạn gửi
        params = {
            "title_filter": title,
            "location_filter": location,
            "limit": limit,
            "offset": offset,
            "remote": str(remote_only).lower(),  # Chuyển True/False thành 'true'/'false'
            "include_ai": "true"  # Bật tính năng AI để dùng được experience_level
        }

        # Xử lý lọc loại hình công việc (nếu có)
        if employment_types:
            params["type_filter"] = ",".join(employment_types)

        # Xử lý lọc kinh nghiệm bằng AI (BETA)
        if experience_level:
            params["ai_experience_level_filter"] = experience_level

        try:
            # Lưu ý: Theo tài liệu RapidAPI, đôi khi params được gửi qua GET
            # nhưng một số provider yêu cầu gửi qua POST body.
            # Ở đây mình dùng GET params theo đúng định nghĩa "Query Params".
            response = requests.get(
                url, headers=headers, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error {response.status_code}", "detail": response.text}
        except Exception as e:
            return {"error": "Connection Error", "detail": str(e)}
