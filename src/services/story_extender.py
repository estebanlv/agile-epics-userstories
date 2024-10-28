import os
import openai
from typing import Dict
from src.schemas.extended_user_story import ExtendedUserStorySchema
from pydantic import ValidationError
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
logger = logging.getLogger(__name__)

# Initialize OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

async def extend_user_story(description: str) -> Dict:
    logger.info(f"Extending user story with description: {description}")
    
    # Define the messages for the ChatCompletion
    messages = [
    {
        "role": "system",
        "content": (
            "You are an Agile coach. Given a user story description, expand it by adding a detailed description, "
            "subtasks, acceptance criteria, and a definition of done. Provide the output strictly in JSON format "
            "following the specified schema."
        ),
    },
    {
        "role": "user",
        "content": (
            f"Extend the following user story description.\n\nDescription:\n{description}\n\n"
            "Example of desired output:\n"
            "{\n"
            "  \"extended_user_story\": {\n"
            "    \"story\": \"Implement search functionality\",\n"
            "    \"description\": \"As a user, I can enter keywords into a search bar to find relevant products.\",\n"
            "    \"effort_points\": 5,\n"
            "    \"subtasks\": [\n"
            "      {\"subtask\": \"Design search bar UI\"},\n"
            "      {\"subtask\": \"Implement search algorithm\"},\n"
            "      {\"subtask\": \"Integrate search with product database\"}\n"
            "    ],\n"
            "    \"acceptance_criteria\": [\n"
            "      {\"criterion\": \"Search bar is visible on all product pages\"},\n"
            "      {\"criterion\": \"Search returns relevant results within 2 seconds\"},\n"
            "      {\"criterion\": \"User can filter search results by category and price\"}\n"
            "    ],\n"
            "    \"definition_of_done\": \"All subtasks are completed, and the search functionality passes all acceptance criteria tests.\"\n"
            "  }\n"
            "}"
        ),
    },
    ]

    # Define the JSON schema for the response
    json_schema = {
        "type": "object",
        "properties": {
            "extended_user_story": {
                "type": "object",
                "properties": {
                    "story": {"type": "string"},
                    "description": {"type": "string"},
                    "effort_points": {"type": "integer"},
                    "subtasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "subtask": {"type": "string"},
                            },
                            "required": ["subtask"],
                            "additionalProperties": False
                        },
                    },
                    "acceptance_criteria": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "criterion": {"type": "string"},
                            },
                            "required": ["criterion"],
                            "additionalProperties": False
                        },
                    },
                    "definition_of_done": {"type": "string"}
                },
                "required": ["story", "description", "effort_points", "subtasks", "acceptance_criteria", "definition_of_done"],
                "additionalProperties": False
            }
        },
        "required": ["extended_user_story"],
        "additionalProperties": False
    }

    try:
        # Make the API call with response_format as json_schema
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ensure this model is available; otherwise, use "gpt-4o-mini"
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "extended_user_story_response",
                    "strict": True,
                    "schema": json_schema
                }
            },
            max_tokens=15000,
            temperature=0.7,
        )

        # Extract the message object
        message = response.choices[0].message

        # Check for refusal
        if message.get('refusal'):
            logger.warning(f"Refusal message: {message['refusal']}")
            return {}


        # Extract the JSON response
        gpt_response = message['content']
        logger.info(f"Received response from OpenAI: {gpt_response}")

        # Parse and validate the JSON response using Pydantic
        parsed_response = json.loads(gpt_response)
        validated_response = ExtendedUserStorySchema(**parsed_response)

        return validated_response.extended_user_story.dict()

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {}
    except json.JSONDecodeError as je:
        logger.error(f"JSON decode error: {je}")
        return {}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {}
