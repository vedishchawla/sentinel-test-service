class AuthService:
    def parse_auth_header(self, auth_header: str) -> dict:
        # BUG: If auth_header is None or missing Bearer prefix, crashes with AttributeError or ValueError
        parts = auth_header.split(" ")
        token_type = parts[0]
        token = parts[1]
        if token_type.lower() != "bearer":
            raise ValueError("Only Bearer tokens are supported")
        return {"token": token, "valid": True}
