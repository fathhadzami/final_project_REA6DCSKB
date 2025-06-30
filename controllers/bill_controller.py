import streamlit as st
import pandas as pd
from streamlit import session_state as ss
from PIL import Image

from services.ai_service import AIService

class BillController:

	def __init__(self):
		self.name_steps = ["📸 Upload", "📝 Sesuaikan", "🤑 Teman", "🧾 Split", "🌟 Result"]
		self.ai_service = AIService()

	def index(self, router) -> None:
		default_session_states = {
			'current_step': 1,
			'form_data': {},
			'completed_steps': set(),
			'bill_data': None,
			'friends': [{"name": "Aku"}],
			'split_method': None,
			'results': [],
			'item_assignment': None
		}

		for key, default_session_state in default_session_states.items():
			if key not in ss:
				ss[key] = default_session_state

		st.set_page_config(
			layout="centered",
			page_title="PatunganApp",
			page_icon="💸"
		)
		st.markdown("""
			<style>
				/* Hide the Streamlit menu and footer for a cleaner look */
				#MainMenu {visibility: hidden;}
				footer {visibility: hidden;}

				/* Adjust button width for mobile */
				button {
					width: 100%;
					margin-bottom: 0.5rem;
				}

				/* Further refine block container padding on small screens */
				@media (max-width: 600px) {
					.block-container {
						padding-top: 2rem;
						padding-bottom: 2rem;
						padding-left: 1rem;
						padding-right: 1rem;
					}
				}
			</style>
		""", unsafe_allow_html=True)

		if ss.current_step > 1 and ss.current_step <= len(self.name_steps):
			self._display_progress_bar(ss.current_step)

		if ss.current_step == 1:
			self._upload_bill()
		elif ss.current_step == 2:
			self._edit_bill()
		elif ss.current_step == 3:
			self._friends_list()
		elif ss.current_step == 4:
			self._splitting_bill()
		elif ss.current_step == 5:
			self._result_bill()

	def _display_progress_bar(self, current_step: int) -> None:
		if ss.current_step <= len(self.name_steps):
			total_steps = len(self.name_steps)
			progress = (current_step - 1) / (total_steps - 1) if total_steps > 1 else 1
			st.progress(progress)

			cols = st.columns(total_steps)
			for i in range(total_steps):
				with cols[i]:
					step_num = i + 1
					if step_num < current_step or step_num in ss.completed_steps:
						st.markdown(f"<div style='text-align: center; color: green;'>{self.name_steps[i]} ✅</div>", unsafe_allow_html=True)
					elif step_num == current_step:
						st.markdown(f"<div style='text-align: center; color: #4663AC; font-weight: bold;'>{self.name_steps[i]}</div>", unsafe_allow_html=True)
					else:
						st.markdown(f"<div style='text-align: center; color: gray;'>{self.name_steps[i]}</div>", unsafe_allow_html=True)

			st.markdown

	def _upload_bill(self):
		st.markdown(f"<h2>Selamat Datang di <br /> 💸 PatunganApp</h2>", unsafe_allow_html=True)
		st.subheader("Aplikasi untuk Split Bill")
		st.divider()

		st.markdown("📷 Silahkan Upload Bill Belanjamu")
		uploaded_file = st.file_uploader("Pilih gambar struk (JPG, PNG)", type=["jpg", "jpeg", "png"])

		if uploaded_file is not None:
			image = Image.open(uploaded_file)
			st.image(image=image, caption="Struk Terunggah", use_container_width=True)

			if st.button(label="Next", disabled=not self.ai_service.is_api_ready, type="primary"):
				with st.spinner("Menganalisis gambar..."):
					bill_data, error = self.ai_service.extract_bill_data(image)

					if error:
						st.error(f"Error: {error}")
					else:
						ss.bill_data = bill_data
						st.success("Data berhasil diekstrak!")
						ss.completed_steps.add(1)
						ss.current_step = 2
						st.rerun()

	def _edit_bill(self):
		st.subheader("📝 Sesuaikan data bill")
		merchant_name = st.text_input(
			"Nama Resto/Toko",
			key="merchant_name",
			value=ss.bill_data["merchant_name"]
		)

		with st.expander("Tambah Item", expanded=True):
			col1, col2, col3 = st.columns(3)
			with col1:
				new_item_name = st.text_input("Nama Item")
			with col2:
				new_item_qty = st.number_input("Qty", min_value=0)
			with col3:
				new_item_price = st.number_input("Harga Satuan (Rp)", min_value=0)
			if st.button("Tambah Item"):
				if new_item_name and new_item_qty > 0 and new_item_qty > 0:
					ss.bill_data["items"].append({"name": new_item_name, "quantity": new_item_qty, "unit_price": new_item_price, "total_price": new_item_qty * new_item_price})

		if ss.bill_data["items"]:
			edited_df = st.data_editor(
				pd.DataFrame(ss.bill_data["items"]),
				use_container_width=True,
				num_rows="dynamic",
				column_config={
					"name": st.column_config.TextColumn("Nama Item"),
					"quantity": st.column_config.NumberColumn("Qty."),
					"unit_price": st.column_config.NumberColumn("Harga Satuan (Rp)"),
					"total_price": st.column_config.NumberColumn("Total Harga (Rp)"),
				}
			)
			ss.bill_data["items"] = edited_df.to_dict(orient="records")

			tax_amount = st.number_input(
				"Pajak",
				key="tax_amount",
				value=ss.bill_data["tax_amount"]
			)
			service_charge = st.number_input(
				"Service Charge",
				key="service_charge",
				value=ss.bill_data["service_charge"]
			)
			total_amount = sum(item['total_price'] for item in ss.bill_data["items"]) + tax_amount + service_charge

			ss.bill_data["merchant_name"] = merchant_name
			ss.bill_data["tax_amount"] = tax_amount
			ss.bill_data["service_charge"] = service_charge
			ss.bill_data["total_amount"] = total_amount

		if st.button(label="Lanjutkan", type="primary"):
			ss.completed_steps.add(2)
			ss.current_step = 3
			st.rerun()

		if st.button(label="Kembali", type="secondary"):
			ss.completed_steps.remove(1)
			ss.current_step = 1
			st.rerun()

	def _friends_list(self):
		st.header("🤑 Siapa saja nih yang ikut patungan?")
		with st.expander("Tambah Teman", expanded=True):
			new_friend_name = st.text_input("Nama Teman")
			if st.button("Tambah Teman"):
				ss.friends.append({"name": new_friend_name})

		friends_df = st.data_editor(
			pd.DataFrame(ss.friends),
			num_rows="dynamic",
			use_container_width=True,
			column_config={
				"name": st.column_config.TextColumn("Nama")
			}
		)
		ss.friends = friends_df.to_dict(orient="records")

		if st.button(label="Lanjutkan", type="primary"):
			ss.completed_steps.add(3)
			ss.current_step = 4
			st.rerun()

		if st.button(label="Kembali", type="secondary"):
			ss.completed_steps.remove(2)
			ss.current_step = 2
			st.rerun()

	def _splitting_bill(self):
		st.subheader("🧾 Yuk kita buat patungannya")
		results = {}
		item_assignment = {}
		name_friends = []
		for friend in ss.friends:
			name_friends.append(friend["name"])

		if ss.bill_data["total_amount"] > 0 and len(ss.friends) > 0:
			split_method = st.radio("Pilih metode pembagian:", ("Bagi Rata", "Berdasarkan Item"))
			if split_method == "Berdasarkan Item":
				st.subheader("Bayar apa aja nih?")

				for item in ss.bill_data["items"]:
					item_name = item["name"]
					item_qty = item["quantity"]
					item_price = item["total_price"]
					selected_friends = st.multiselect(
						f"Siapa yang membayar '{item_name} ({item_qty})' (Rp {item_price})?",
						name_friends,
						key=f"item_assign_{item_name}"
					)
					item_assignment[item_name] = selected_friends

		if st.button(label="Lanjutkan", type="primary"):
			if split_method == "Bagi Rata":
				if ss.bill_data["total_amount"] > 0 and len(ss.friends) > 0:
					amount_per_person = ss.bill_data["total_amount"] / len(ss.friends)
					for friend in name_friends:
						results[friend] = amount_per_person
			elif split_method == "Berdasarkan Item":
				for friend in name_friends:
					results[friend] = 0.0
				for item in ss.bill_data["items"]:
					item_name = item["name"]
					item_qty = item["quantity"]
					item_price = item["total_price"]
					payers = item_assignment.get(item_name, [])
					if not payers:
						st.warning(f"Item '{item_name}' belum ditugaskan ke siapa pun.")
						continue
					amount_per_payer = item_price / len(payers)
					for payer in payers:
						results[payer] += amount_per_payer

			ss.results = results
			ss.item_assignment = item_assignment
			ss.completed_steps.add(4)
			ss.current_step = 5
			st.rerun()

		if st.button(label="Kembali", type="secondary"):
			ss.completed_steps.remove(3)
			ss.current_step = 3
			st.rerun()

	def _result_bill(self):
		if ss.results:
			st.subheader("🌟 Yeay, ini adalah hasil patungannya!")

			df_results = pd.DataFrame(ss.results.items(), columns=["Nama Teman", "Jumlah Dibayar (Rp)"])
			df_results["Jumlah Dibayar (Rp)"] = df_results["Jumlah Dibayar (Rp)"].map("{:,.2f}".format)
			st.dataframe(df_results, use_container_width=True, hide_index=True)

			st.success(f"Total tagihan yang dibagi: Rp {sum(item['total_price'] for item in ss.bill_data["items"]):,.2f}")

		if st.button(label="Kembali", type="secondary"):
			ss.completed_steps.remove(4)
			ss.current_step = 4
			st.rerun()

		if st.button("🔄 Buat Patungan Baru"):
			for key in ['current_step', 'form_data', 'completed_steps', 'bill_data', 'friends', 'split_method', 'results', 'item_assignment']:
				if key in ss:
					del ss[key]
			st.rerun()
