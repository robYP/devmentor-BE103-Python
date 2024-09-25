from sqlalchemy.orm import Session
from repository.user import UserRepository
from database.user import User
from config.config import LINE_CHANNEL_ID, LINE_CALLBACK_URL, LINE_CHANNEL_SECRET
import requests
from requests.exceptions import RequestException


class LineLoginService:
    def __init__(self, db:Session) -> None:
        self.user_repository = UserRepository(db)
        pass
    
    def get_line_access_token(self, code):
        token_url = "https://api.line.me/oauth2/v2.1/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LINE_CALLBACK_URL,
            "client_id": LINE_CHANNEL_ID,
            "client_secret": LINE_CHANNEL_SECRET
        }
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to get access token")
    
    
    def verify_token(self, access_token):
        verify_token_url = "https://api.line.me/oauth2/v2.1/verify"
        param = {
            "access_token":access_token,
        }
        response = requests.get(verify_token_url, params=param)
        if response.status_code == 200:
            return response.json()
        return None
    
    
    def get_line_user_profile(self, access_token):
        profile_url = "https://api.line.me/v2/profile"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def create_user_by_line_id(self, line_user):
        user = self.user_repository.get_user_by_line_id(line_user["userId"])
        
        if user:
            return user
        if not user:
            user = User(
                line_user_id = line_user["userId"],
                language = "EN"
            )
            return self.user_repository.create(user)            