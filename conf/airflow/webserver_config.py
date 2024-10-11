from __future__ import annotations

import os

import jwt
import requests
import logging
from http import HTTPStatus
import json
from base64 import b64decode
from cryptography.hazmat.primitives import serialization
from airflow.www.security import AirflowSecurityManager


basedir = os.path.abspath(os.path.dirname(__file__))
log = logging.getLogger(__name__)

WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None


class CustomSecurityManager(AirflowSecurityManager):
    def oauth_user_info(self, provider, response):
        if provider == "keycloak":
            token = response["access_token"]
            me = jwt.decode(token, public_key, algorithms=["HS256", "RS256"])
            log.info("me: {0}".format(me))
            log.debug("response: {0}".format(response))
            iss = me.get("iss", {})
            userinfo_endpoint = "{0}/protocol/openid-connect/userinfo".format(iss)

            headers = {
                "Accept": "application/json",
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
            }
            res = requests.get(userinfo_endpoint, headers=headers, timeout=10, verify=False, auth=None)
            log.info("response {0}: {1}".format(res.status_code, res.text))

            if res.status_code == HTTPStatus.OK:
                groups = json.loads(res.text).get("isMemberOf", [])
                log.info("user groups: {0}".format(groups))
            else:
                groups = []

            userinfo = {
                "username": me.get("preferred_username"),
                "email": me.get("email"),
                # "first_name": me.get("given_name"),
                # "last_name": me.get("family_name"),
                "role_keys": groups,
            }

            log.info("user info: {0}".format(userinfo))

            return userinfo
        else:
            return {}

#######################################
# Actual `webserver_config.py`
#######################################
from flask_appbuilder.security.manager import AUTH_OAUTH

AUTH_TYPE = AUTH_OAUTH
SECURITY_MANAGER_CLASS = CustomSecurityManager

# if we should replace ALL the user's roles each login, or only on registration
AUTH_ROLES_SYNC_AT_LOGIN = True

# force users to re-auth after 30min of inactivity (to keep roles in sync)
PERMANENT_SESSION_LIFETIME = 1800

# registration configs
AUTH_USER_REGISTRATION = True  # allow users who are not already in the FAB DB
AUTH_USER_REGISTRATION_ROLE = "Public"  # this role will be given in addition to any AUTH_ROLES_MAPPING

OIDC_ISSUER = "http://nginx:7777/realms/test"

OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": "airflow",
            "client_secret": "dcQn2qiwsSHG3AHB8XQ8dxFEbpDXsVvS",
            "server_metadata_url": f"{OIDC_ISSUER}/.well-known/openid-configuration",
            "api_base_url": f"{OIDC_ISSUER}/protocol/openid-connect",
            "client_kwargs": {
                "scope": "openid email profile isMemberOf"
            },
            "access_token_url": f"{OIDC_ISSUER}/protocol/openid-connect/token",
            "authorize_url": f"{OIDC_ISSUER}/protocol/openid-connect/auth",
            "request_token_url": None,
        },
    },
]

AUTH_ROLES_MAPPING = {
    "g:infn:sysinfo:dev::ag:m": ["Viewer"],
    "g:infn:sysinfo:ops::ag:m": ["Admin"],
}

# Fetch public key
try:
    req = requests.get(OIDC_ISSUER)
    key_der_base64 = req.json()["public_key"]
    key_der = b64decode(key_der_base64.encode())
    public_key = serialization.load_der_public_key(key_der)
except requests.RequestException as error:
    log.error(f"Fetch public key: {error}")
    raise
