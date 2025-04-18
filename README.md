# 🛰️ Illegal Mining Detection in the Brazilian Amazon Using Satellite Imagery

This is an **applied data science project** focused on **environmental monitoring** and **automatic detection of illegal mining** in the Brazilian Amazon. The pipeline uses **Sentinel-2 satellite imagery** to collect, process, and organize georeferenced samples, which are then used to train **convolutional neural networks (CNNs)**.

---

## 🎯 Objective

- Collect geospatial samples of areas with and without illegal mining.
- Download high-resolution RGB imagery (10m) from Sentinel-2 using Google Earth Engine.
- Organize samples into a balanced, labeled dataset.
- Train deep learning models to detect illegal mining based on satellite imagery.

---

## 🛰️ Data Sources

- **Sentinel-2** imagery from the `COPERNICUS/S2_SR_HARMONIZED` collection via [Google Earth Engine](https://earthengine.google.com/)
- **Shapefiles** provided by Instituto Socioambiental (ISA):
  - `MineriaIlegal_pol.shp`: polygonal regions with mining activity
  - `MineriaIlegal_pt.shp`: individual mining occurrence points

---

## 🛠️ Technologies Used

- Google Earth Engine API
- Python libraries: `geemap`, `geopandas`, `shapely`, `pandas`, `numpy`
- TensorFlow (for model training)
- Jupyter Notebooks for data exploration and visualization

---

## 📁 Project Structure

```
.
├── main.py                         # Main script
├── utils/
│   └── sample_collector.py        # Function for sample generation and image download
├── MineriaIlegal_2022/            # Mining occurrence shapefiles
├── dataset/                       # Output dataset
│   ├── mining/
│   └── control/
└── README.md
```

---

## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Authenticate with Google Earth Engine

```bash
earthengine authenticate
```

### 3. Generate the dataset

```python
from utils.sample_collector import generate_samples_and_download_images

samples = generate_samples_and_download_images(
    shp_pol_path="MineriaIlegal_2022/MineriaIlegal_pol.shp",
    shp_pt_path="MineriaIlegal_2022/MineriaIlegal_pt.shp",
    n_samples_mining=100,
    n_samples_control=100,
    dataset_dir="dataset"
)
```

---

## 📂 Dataset Structure

Images will be saved in the following folder structure:

```
dataset/
├── mining/
│   ├── img_0000.png
│   ├── img_0001.png
│   └── ...
├── control/
│   ├── img_0000.png
│   ├── img_0001.png
│   └── ...
```

---

## 🧠 Potential Applications

- Automated illegal mining detection in the Amazon
- Binary classification using convolutional neural networks (CNNs)
- Integration with environmental monitoring dashboards
- Support for inspection and policy enforcement

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Willian Pina**  
Data Scientist  
🔗 [LinkedIn profile](https://www.linkedin.com/in/willianbotelho/)

---

## 🤝 Contributions

Contributions are welcome! Feel free to open an issue, suggest improvements, or submit a pull request.

---
