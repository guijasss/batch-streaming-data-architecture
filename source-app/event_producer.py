from datetime import datetime
from typing import Any
from uuid import uuid4
from random import choice, randint

from confluent_kafka import Producer


def generate_purchase_steps() -> list:
	events = ["READ_DESCRIPTION", "ADD_TO_CART", "FILL_PERSONAL_INFO", "FILL_BILLING_INFO", "FINISH_FLOW"]
	n_events = randint(0, len(events))
	return ["START_FLOW"] + events[0:n_events]

def generate_device_info(platform: str) -> dict:
	if platform == "web":
		browser = choice(["chrome", "safari", "edge", "firefox", "opera"])
		version = choice(["1.0", "1.1", "1.2", "1.3"])
		return {
			"browser": browser,
			"version": version
		}
	elif platform == "mobile":
		os = choice(["android", "ios"])
		version = choice(["10", "11", "12", "13"])
		return {
			"os": os,
			"version": version
		}
	else:
		raise ValueError(f"Invalid value for platform: {platform}! It should be web or mobile.")

def generate_event_sequence() -> dict:
	"""
	onboarding example event
	{
		"session_id": "abc123def456",
		"step": "START_FLOW",
		"timestamp": "2024-03-01 00:00:00.000",	
		"user_info": {
			"platform": "web",
			"country": "Brazil",
			"device_info": {
				"browser": "chrome",
				"version": "12.0" 
			}
		}
	}
	steps:
	START_FLOW, READ_DESCRIPTION, ADD_TO_CART, FILL_PERSONAL_INFO, FILL_BILLING_INFO, FINISH_FLOW
	"""
	session_id = str(uuid4())
	user_info_platform = choice(["web", "mobile"])
	user_info_country = choice(["Brazil", "Mexico", "USA", "Argentina"])

	steps = generate_purchase_steps()
	device_info = generate_device_info(user_info_platform)

	events = []
	for step in steps:
		events.append({
			"session_id": session_id,
			"step": step,
			"timestamp": datetime.now().isoformat(),
			"user_info": {
				"platform": user_info_platform,
				"country": user_info_country,
				"device_info": device_info
			}
		})

	return events


conf_dict = {
  "bootstrap.servers": "localhost:9092"
}

producer = Producer(conf_dict)

for event in generate_event_sequence():
	producer.produce("purchase-journey", key=str(uuid4()), value=str(event))
producer.flush()
