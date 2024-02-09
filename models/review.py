#!/usr/bin/python3
"""Defines a Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review objects"""

        place_id = ""
        user_id = ""
        text = ""
