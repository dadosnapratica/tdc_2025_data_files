# 🚀 Git Repository Sync with Large File Support

This project provides a Python script to **sync a directory with a Git repository**, supporting **large files** via **Git LFS** and authentication via **SSH**. It runs on both **Windows and Linux** and uses a **`.env` configuration file** for customization.

---

## 📌 Features
- ✅ **Cross-platform support** (Windows & Linux)
- ✅ **Automates Git LFS tracking** for large files
- ✅ **Uses SSH for secure authentication**
- ✅ **Environment variable support via `.env`**
- ✅ **Handles large files like `.csv`, `.zip`, `.mp4` efficiently**
- ✅ **Automated cloning, committing, and pushing to GitHub**

---

## 📦 Installation

### **1️⃣ Clone the Repository**
```bash
# Clone the project
git clone git@github.com:dadosnapratica/tdc_2025_data_files.git
cd tdc_2025_data_files
```

### **2️⃣ Create a Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file in the project root and customize as needed:
```ini
REPO_URL=git@github.com:dadosnapratica/tdc_2025_data_files.git
BRANCH=main
REPO_DIR=/home/ubuntu/tdc_2025_data_files  # Use C:\tdc_2025_data_files on Windows
WATCH_DIR=data
LFS_TRACKED_EXTENSIONS=csv,zip,mp4,json
```

### **5️⃣ Ensure SSH Authentication is Set Up**
```bash
ssh -T git@github.com
```
This should return: `Hi <username>! You've successfully authenticated.`

---

## 🛠️ Usage

### **Manually Upload a File**
```bash
python upload_to_git.py data/sample.csv
```

### **Automated Sync of All Changes** (Coming soon!)
The script can be modified to automatically detect and sync all file changes in `WATCH_DIR`.

---

## 🚀 How It Works
1. **Checks SSH authentication** before performing Git operations.
2. **Clones or pulls the latest repository state**.
3. **Sets up Git LFS and tracks large files**.
4. **Copies modified files into the repository**.
5. **Commits and pushes updates automatically**.

---

## ⚠️ Troubleshooting

**SSH Authentication Issues?**
```bash
ssh-add ~/.ssh/id_rsa  # Ensure your SSH key is loaded
ssh -T git@github.com  # Test connection
```

**Git LFS Not Tracking Files?**
```bash
git lfs ls-files  # Check if large files are managed by LFS
git lfs track "*.csv"  # Manually track file types
```

**Windows Path Issues?**
Use `C:\tdc_2025_data_files` instead of `/home/ubuntu/tdc_2025_data_files` in `.env`.

---

## 🤝 Contributing
Feel free to submit pull requests or report issues!

---

## 📜 License
This project is open-source under the **MIT License**.

---

Happy Coding! 🚀

