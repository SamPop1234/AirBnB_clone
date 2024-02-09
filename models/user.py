#!/usr/bin/python3
"""Defines a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user objects"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
