# AutoSpec Deployment & Cloud Database Migration Guide

This guide details how to migrate the local MySQL database to a cloud-hosted relational database and deploy the Streamlit web application to **Streamlit Community Cloud** with zero localhost dependency errors.

---

## 1. Cloud Database Options

### Recommended: TiDB Cloud Serverless (Free Forever, Instant MySQL Setup)
TiDB Cloud Serverless provides a 100% MySQL-compatible database with 5 GB free storage, automatic scaling, and built-in TLS/SSL. It requires **no credit card** and takes 2 minutes to set up.

1. Go to [TiDB Cloud](https://tidbcloud.com) and create a free account.
2. Click **Create Cluster** and select **Serverless**.
3. Choose your nearest region (e.g., AWS / Singapore or US East).
4. After cluster creation, click **Connect**:
   - Choose **Connect with: General / MySQL CLI / Python**.
   - Note down: `Host`, `Port` (usually `4000`), `User`, and `Password`.
5. Run the schema & sample data:
   - In the TiDB Cloud web console, open **SQL Editor**.
   - Paste the SQL script generated via AutoSpec Admin Mode's **"Export Database Backup (.sql)"** button (or let AutoSpec auto-initialize on first connection!).

---

### Alternative: AWS RDS MySQL
1. Log in to AWS Console -> **RDS** -> **Create Database**.
2. Select **MySQL** (Community Edition).
3. Choose the **Free tier** template.
4. Set DB instance identifier (e.g. `autospec-db`), Master username (`admin`), and Master password.
5. In **Connectivity**:
   - Set **Public access** to **Yes** (so Streamlit Cloud can reach it).
   - In the VPC Security Group, add an Inbound Rule for MySQL/Aurora (Port 3306) allowing connections from `0.0.0.0/0` (or Streamlit Cloud IP range).
6. Copy the RDS Endpoint once available.

---

## 2. Deploying to Streamlit Community Cloud

### Step 1: Push Project to GitHub
Initialize git and push your repository to GitHub:
```bash
git init
git add .
git commit -m "feat: AutoSpec with dynamic booking and cloud database support"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### Step 2: Connect to Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository, branch (`main`), and main file path (`app.py`).

### Step 3: Configure Secrets in Streamlit Cloud
1. In the deployment settings (or under **App settings -> Secrets**), paste your cloud database configuration in TOML format:

```toml
[mysql]
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000
user = "xxxxxx.root"
password = "your-database-password"
database = "AutoSpec_Database_System"
ssl_verify_cert = true
```

2. Click **Save**.
3. AutoSpec will automatically connect to your cloud database, initialize the tables if needed, and run with full dynamic booking and administrative controls!

---

## 3. Local Development vs. Cloud Deployment Summary

| Environment | Host | Port | Configuration Source |
| :--- | :--- | :--- | :--- |
| **Local Development** | `localhost` | `3306` | Built-in fallback (`root` / `Arnav@1909`) |
| **Local with Secrets** | Any | Any | `.streamlit/secrets.toml` |
| **Streamlit Community Cloud** | TiDB / AWS RDS | 4000 / 3306 | Streamlit Cloud Dashboard Secrets |
| **Docker / Container** | Any | Any | Environment Variables (`MYSQL_HOST`, `MYSQL_PORT`, etc.) |
