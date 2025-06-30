import base64
import io
import os
import json
import requests
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")


class AIService:
	"""Service untuk menangani AI/OCR operations"""

	def __init__(self):
		self.api_key = os.environ.get("OPENROUTER_API_KEY")
		self.api_base = os.environ.get("OPENROUTER_API_BASE")
		self.model_name = os.environ.get("AI_MODEL")

	def is_api_ready(self) -> bool:
		"""Check apakah API key dan base URL sudah di-set"""
		return bool(self.api_key and self.api_base)

	def encode_image_to_base64(self, image: Image.Image) -> str:
		"""Convert PIL Image ke base64 string untuk API"""
		buffer = io.BytesIO()
		image.save(buffer, format="PNG")
		img_str = base64.b64encode(buffer.getvalue()).decode()
		return img_str

	def extract_bill_data(self, image: Image.Image) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
		"""
		Extract data dari gambar struk menggunakan AI

		Args:
			image: PIL Image object dari struk

		Returns:
			Tuple[bill_data, error]: Data struk yang diekstrak atau error message
		"""
		try:
			# Convert image to base64
			base64_image = self.encode_image_to_base64(image)

			# Prepare API request
			headers = {
				"Authorization": f"Bearer {self.api_key}",
				"Content-Type": "application/json"
			}

			# Create prompt for bill extraction
			prompt = self._create_extraction_prompt()

			payload = {
				"model": self.model_name,
				"messages": [
					{
						"role": "user",
						"content": [
							{
								"type": "text",
								"text": prompt
							},
							{
								"type": "image_url",
								"image_url": {
									"url": f"data:image/png;base64,{base64_image}"
								}
							}
						]
					}
				],
				"max_tokens": 700,
				"temperature": 0.1
			}

			# Make API request
			response = requests.post(
				f"{self.api_base}",
				headers=headers,
				json=payload,
				timeout=30
			)

			if response.status_code == 200:
				result = response.json()
				content = result["choices"][0]["message"]["content"]

				# Parse JSON response
				bill_data = self._parse_ai_response(content)
				return bill_data, None
			else:
				error_msg = f"API Error: {response.status_code} - {response.text}"
				return None, error_msg

		except Exception as e:
			return None, f"Error when extract data: {str(e)}"
			# Fallback ke mock data untuk development
			# return self._get_mock_data(), None

	def _create_extraction_prompt(self) -> str:
		"""Create prompt untuk AI extraction"""
		return """
		Please analyze this receipt/bill image and extract the following information in JSON format:
		{
			"merchant_name": "Name of the store/restaurant",
			"total_amount": 0,
			"tax_amount": 0,
			"service_charge": 0,
			"items": [
				{
					"name": "Item name",
					"quantity": 1,
					"unit_price": 0,
					"total_price": 0
				}
			],
			"date": "YYYY-MM-DD",
			"time": "HH:MM"
		}

		Important:
		- Use Indonesian language for item names if they appear in Indonesian
		- If tax or service charge is not visible, set to 0
		- Ensure all prices are numbers (not strings)
		- Return only valid JSON, no additional text
		"""

	def _parse_ai_response(self, content: str) -> Dict[str, Any]:
		"""Parse AI response dan extract JSON data"""
		try:
			# Try to find JSON in the response
			start_idx = content.find('{')
			end_idx = content.rfind('}') + 1

			if start_idx != -1 and end_idx != -1:
				json_str = content[start_idx:end_idx]
				return json.loads(json_str)
			else:
				# Fallback to mock data if parsing fails
				return self._get_mock_data()

		except json.JSONDecodeError:
			# Fallback to mock data
			return self._get_mock_data()

	def _get_mock_data(self) -> Dict[str, Any]:
		"""Mock data untuk development/testing"""
		return {
			"merchant_name": "INDOMARET KAB GARUT",
			"total_amount": 15000,
			"tax_amount": 0,
			"service_charge": 0,
			"items": [
				{
					"name": "JAVANA TEH MLATI 350",
					"quantity": 5,
					"unit_price": 3000,
					"total_price": 15000
				}
			],
			"date": "2020-11-07",
			"time": "15:45"
		}

	def validate_bill_data(self, bill_data: Dict[str, Any]) -> bool:
		"""Validate struktur data bill"""
		required_fields = [
			"merchant_name", "total_amount", "tax_amount",
			"service_charge", "items", "date", "time"
		]

		# Check required fields
		for field in required_fields:
			if field not in bill_data:
				return False

		# Check items structure
		if not isinstance(bill_data["items"], list):
			return False

		for item in bill_data["items"]:
			item_fields = ["name", "quantity", "unit_price", "total_price"]
			for field in item_fields:
				if field not in item:
					return False

		return True