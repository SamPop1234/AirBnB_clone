#!/usr/bin/python3
"""
Unit tests for models/state.py
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Test cases for State class instantiation."""

    def test_no_args_instantiates(self):
        """Test instantiation of State class with no arguments."""
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        """Test if a new instance of State is stored in the objects."""
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if the 'id' attribute of State is a string."""
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        """Test if 'created_at' attribute of State is a datetime object."""
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test if 'updated_at' attribute of State is a datetime object."""
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        """Test if 'name' is a public class attribute of State."""
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_two_states_unique_ids(self):
        """Test if two instances of State have unique IDs."""
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_two_states_different_created_at(self):
        """Test if two instances of State have different 'created_at' values."""
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_two_states_different_updated_at(self):
        """Test if two instances of State have different 'updated_at' values."""
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_str_representation(self):
        """Test the string representation of State."""
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        state_str = state.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    def test_args_unused(self):
        """Test if State instantiation ignores unused arguments."""
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test State instantiation with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test State instantiation with None keyword arguments."""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Test cases for State class save method."""

    @classmethod
    def setUp(cls):
        """Set up for the test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(cls):
        """Clean up after the test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test saving a single State object."""
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def test_two_saves(self):
        """Test saving multiple State objects."""
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def test_save_with_arg(self):
        """Test saving with an argument."""
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self):
        """Test if saving updates the file."""
        state = State()
        state.save()
        state_id = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Test cases for State class to_dict method."""

    def test_to_dict_type(self):
        """Test the type of the returned dictionary."""
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test if the dictionary contains correct keys."""
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if the dictionary contains added attributes."""
        state = State()
        state.middle_name = "Holberton"
        state.my_number = 98
        self.assertEqual("Holberton", state.middle_name)
        self.assertIn("my_number", state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if datetime attributes are strings in the dictionary."""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        dt = datetime.today()
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test the contrast between to_dict and __dict__."""
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self):
        """Test to_dict method with an argument."""
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
