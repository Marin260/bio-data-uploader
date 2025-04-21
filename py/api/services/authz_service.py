import os
from datetime import datetime

import requests
from authlib.jose import jwt
from fastapi import Request


class AuthorizationService:
    HEADER = {"alg": "HS256"}

    def generate_access_token(self, user_identifier: str):
        payload_access = {
            "sub": user_identifier,
            "exp": datetime.now().timestamp() + 3600,
            "iat": datetime.now().timestamp(),
        }

        access_token = jwt.encode(
            header=self.HEADER,
            payload=payload_access,
            key=os.getenv("AUTHZ_SECRET_KEY"),
        )
        return access_token

    def verify_token(self, token):
        decoded_token = jwt.decode(token, os.getenv("AUTHZ_SECRET_KEY"))
        return decoded_token

    def google_id_token_is_valid(self, auth_response_token) -> bool:
        verification_response = requests.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={auth_response_token["id_token"]}"
        )
        if verification_response.status_code == 200:
            return True
        else:
            return False

    def get_loged_in_user(self, request: Request) -> str:
        token = request.headers.get("Authorization").split(" ")

        assert len(token) == 2

        decoded_token = jwt.decode(token, os.getenv("AUTHZ_SECRET_KEY"))
        # Return sub claim: user email
        return decoded_token["sub"]
