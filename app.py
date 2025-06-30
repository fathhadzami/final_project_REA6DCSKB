import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_router import StreamlitRouter
from controllers.bill_controller import BillController

load_dotenv(dotenv_path="./.env")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = os.environ.get("OPENROUTER_API_BASE")

if not OPENROUTER_API_KEY:
	st.error("OPENROUTER_API_KEY tidak ditemukan. Harap tambahkan di file .env Anda.")
	st.stop()
if not OPENROUTER_API_BASE:
	st.error("OPENROUTER_API_BASE tidak ditemukan. Harap tambahkan di file .env Anda.")
	st.stop()

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Poppins', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

router = StreamlitRouter()
bill_controller = BillController()

@router.map("/")
def index(router: StreamlitRouter):
	bill_controller.index(router)

router.serve()