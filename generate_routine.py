import os
import requests
from  dotenv import load_dotenv


# Load environment variables
load_dotenv()

#get mistral api from environment variables
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("No API key provided")

#Define agent's profile
agent_profile = {
    "name": "Agent1",
    "age": 28,
    "gender": "Female",
    "occupation": "Software Engineer",
    "income_level": "High",
    "commute_mode": "Car",
    "commute_duration": "30 minutes",
    "work_hours": "9:00 AM - 5:00 PM",
    "exercise": "Gym at 6:00 PM for 1 hour",
    "social_interaction": "Meeting friends for dinner",
    "meals": "Home cooking for lunch, eating out for dinner",
    "home_location": "29.7604, -95.3698",  # Houston, TX
    "work_location": "29.7615, -95.3700"  # Downtown office, Houston
}
# Function to generate a dynamic prompt using the agent's profile
def generate_prompt(agent_profile):
    prompt = f"""
    Generate a detailed daily routine for an agent based on the following profile:

    - **Name**: {agent_profile['name']}
    - **Age**: {agent_profile['age']}
    - **Gender**: {agent_profile['gender']}
    - **Occupation**: {agent_profile['occupation']}
    - **Income Level**: {agent_profile['income_level']}
    - **Commute Mode**: {agent_profile['commute_mode']}
    - **Commute Duration**: {agent_profile['commute_duration']}
    - **Work Hours**: {agent_profile['work_hours']}
    - **Exercise**: {agent_profile['exercise']}
    - **Social Interaction**: {agent_profile['social_interaction']}
    - **Meals**: {agent_profile['meals']}
    - **Home Location**: {agent_profile['home_location']}
    - **Work Location**: {agent_profile['work_location']}

    Generate the agent's detailed schedule as follows:
    - **Wake-up time**: [Agent’s wake-up time]
    - **Morning routine**: [How does the agent spend the morning?]
    - **Commute to work**: [Commute mode and time]
    - **Work-related activities**: [Work tasks and meetings]
    - **Lunch break**: [What do they eat? Where do they eat?]
    - **Post-work**: [Gym or other activities]
    - **Socializing**: [Social interaction details]
    - **Evening routine**: [Leisure activities like TV, reading, etc.]
    - **Bedtime**: [When does the agent go to bed?]
    """
    return prompt

# Function to make the API call to Mistral AI
def generate_routine(agent_profile):
    url = "https://api.mistral.ai/v1/chat/completions"  # Correct Mistral API endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = generate_prompt(agent_profile)  # Create the prompt using agent data
    
    # Payload for the API request according to Mistral's format
    payload = {
        "model": "mistral-large-latest",  # Use the correct model identifier
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000  # Adjust token length as needed
    }

    # Send the request to Mistral AI
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]  # Extract the routine from the response
    else:
        print(f"Error: {response.status_code}")
        if response.text:
            print(f"Response: {response.text}")
        return None


# Generate routine for the agent and print it
routine = generate_routine(agent_profile)
if routine:
    print("Generated Routine:", routine)
