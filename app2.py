# app.py
import streamlit as st
import tempfile
import os
import pandas as pd
from batch_extractor_2_3_final import extract_from_file

st.set_page_config(page_title="Result Extractor", layout="centered")
st.title("📄 Result Extractor Web App")
st.markdown("Upload PDF/image result files to extract Name, Roll No., and SGPA values.")

uploaded_files = st.file_uploader(
    "Upload one or more result PDFs or images", 
    type=["pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

show_raw_text = st.checkbox("🔍 Show OCR text (for debugging)")

if uploaded_files:
    data_records = []

    with st.spinner("Extracting data from uploaded files..."):
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix="." + file.name.split(".")[-1]) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            try:
                result = extract_from_file(tmp_path)

                data_records.append({
                    "File": file.name,
                    "Name": result["name"],
                    "Roll Number": result["roll"],
                    "SGPA List": ', '.join(map(str, result["sgpas"]))
                })

                if show_raw_text:
                    st.subheader(f"OCR Text for {file.name}")
                    st.text(result.get("raw_text", "[No OCR text]"))

                if show_raw_text and result.get("raw_text"):
                    raw_filename = file.name + "_ocr.txt"
                    st.download_button(f"Download OCR Text for {file.name}", result["raw_text"], file_name=raw_filename)


            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {e}")

            finally:
                os.remove(tmp_path)

    df = pd.DataFrame(data_records)
    st.success("✅ Extraction completed!")
    st.dataframe(df)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv_data, file_name="results.csv", mime="text/csv")

else:
    st.info("Please upload at least one result PDF/image file.")
