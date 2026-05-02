import json
from pathlib import Path

PROFILES_FILE = Path(__file__).resolve().parent / "profiles.json"


def load_profiles():
    if not PROFILES_FILE.exists():
        return {}

    with open(PROFILES_FILE, "r") as file:
        return json.load(file)


def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file, indent=4)


def add_profile(profile_name):
    profiles = load_profiles()

    if profile_name not in profiles:
        profiles[profile_name] = {}
        save_profiles(profiles)

    return profiles


def add_rating(profile_name, movie_title, rating):
    profiles = load_profiles()

    if profile_name not in profiles:
        profiles[profile_name] = {}

    profiles[profile_name][movie_title] = rating
    save_profiles(profiles)

    return profiles