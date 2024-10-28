import os
import openai
from typing import List, Dict
from src.schemas.user_story import UserStorySchema
from pydantic import ValidationError
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_user_stories(epic: str) -> List[Dict]:
    # Define the messages for the ChatCompletion
    messages = [
        {
            "role": "system",
            "content": (
                "You are an Agile coach specialized in breaking down epics into user stories. "
                "Provide the output strictly in JSON format following the specified schema."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Break down the following epic into a set of user stories. For each user story, "
                f"provide a very detailed description and estimate the effort points (1-13) required to complete it.\n\n"
                f"Epic:\n{epic}"
            ),
        },
    ]

    # Define the JSON schema for the response
    json_schema = {
        "type": "object",
        "properties": {
            "user_stories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "story": {"type": "string"},
                        "description": {"type": "string"},
                        "effort_points": {"type": "integer"}
                    },
                    "required": ["story", "description", "effort_points"],
                    "additionalProperties": False  # Ensure no extra properties
                },
            }
        },
        "required": ["user_stories"],
        "additionalProperties": False  # Ensure no extra properties at root
    }

    try:
        # Make the API call with response_format as json_schema
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ensure this model is available; otherwise, use "gpt-4o-mini"
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "user_stories_response",
                    "strict": True,
                    "schema": json_schema
                }
            },
            max_tokens=10000,
            temperature=0.7,
        )

        # Extract the JSON response
        gpt_response = response.choices[0].message['content']

        # Parse and validate the JSON response using Pydantic
        parsed_response = json.loads(gpt_response)
        validated_response = UserStorySchema(**parsed_response)

        return validated_response.user_stories

    except ValidationError as ve:
        print(f"Validation error: {ve}")
        return []
    except json.JSONDecodeError as je:
        print(f"JSON decode error: {je}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
