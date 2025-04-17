import os

def download_data_drive(file_id, output_path):
  import gdown
  url = f"https://drive.google.com/uc?id={file_id}"
  gdown.download(url, ouput_path, quiet=False)

if __name__ = "__main__":
  os.makedirs("Data", exist_ok=True)

download_from_drive("1NHhAml7ANGbHGf6XPaJYuvylXMTDjDXK", "Data/PM2.5/V5GL0502.HybridPM25.201501-201501.nc")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.shp")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.shx")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.dbf")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.sbx")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.sbn")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.prj")
download_from_drive("152ADBAVlhMKDwEEEhf_VK0miF_RZS3Qv", "Data/RBI_Indonesia/RBI_PROV_KAB6.cpg")
