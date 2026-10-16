import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["pet_sitter_db"]
pets_collection = db["pets"]

def get_pet_list():
    """Returns a list of dicts with pet names and IDs for UI dropdowns."""
    pets = pets_collection.find({}, {"name": 1, "pet_id": 1, "_id": 0})
    return list(pets)

def get_pet_profile(pet_id: str) -> dict:
    """Retrieves a single pet's details by pet_id."""
    return pets_collection.find_one({"pet_id": pet_id}, {"_id": 0})

if __name__ == "__main__":
    # Verification check
    print("Connected. Pet list:", get_pet_list())