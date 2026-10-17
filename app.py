import streamlit as st
import streamlit.components.v1 as components
try:
    from streamlit_plugins.components.theme_changer import st_theme_changer
except Exception:
    st_theme_changer = None
import mysql.connector
import pandas as pd
import altair as alt
import random
import string
import os
import time
import hashlib
import uuid
from datetime import datetime, timezone
# ---------- Systems Configuration ----------
st.set_page_config(
    page_title="AutoSpec Web",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ===================== DYNAMIC THEME SYSTEM (7 THEMES) =====================
THEMES = {
    "Dark Mode": {
        "base": "dark",
        "primary": "#E50914",
        "bg": "#0E1117",
        "secondary_bg": "#161B22",
        "text": "#F0F6FC",
        "text_secondary": "#8B949E",
        "border": "#30363D",
        "card_bg": "#161B22",
        "hover_bg": "#21262D"
    },
    "Light Mode": {
        "base": "light",
        "primary": "#0052CC",
        "bg": "#F8FAFC",
        "secondary_bg": "#F1F5F9",
        "text": "#0F172A",
        "text_secondary": "#475569",
        "border": "#E2E8F0",
        "card_bg": "#FFFFFF",
        "hover_bg": "#EFF6FF"
    },
    "Racing Red": {
        "base": "dark",
        "primary": "#FF1E27",
        "bg": "#0B0C10",
        "secondary_bg": "#13141A",
        "text": "#FFFFFF",
        "text_secondary": "#A1A1A6",
        "border": "#3D1B20",
        "card_bg": "#16181F",
        "hover_bg": "#28161A"
    },
    "Matcha Forest": {
        "base": "light",
        "primary": "#1B5E20",
        "bg": "#EDF3EB",
        "secondary_bg": "#E2ECE0",
        "text": "#112210",
        "text_secondary": "#2D4A2A",
        "border": "#B8CCB4",
        "card_bg": "#FFFFFF",
        "hover_bg": "#E1EFE0"
    },
    "Cyberpunk Neon": {
        "base": "dark",
        "primary": "#00F0FF",
        "bg": "#090A15",
        "secondary_bg": "#0F1222",
        "text": "#F0F4FF",
        "text_secondary": "#8E9BB5",
        "border": "#2E2A54",
        "card_bg": "#14172B",
        "hover_bg": "#1D203D"
    },
    "Monaco Luxury": {
        "base": "dark",
        "primary": "#E5C07B",
        "bg": "#0B132B",
        "secondary_bg": "#101733",
        "text": "#F8F9FA",
        "text_secondary": "#A0AAB8",
        "border": "#3A4B75",
        "card_bg": "#16203D",
        "hover_bg": "#1E2B58"
    },
    "Nordic Frost": {
        "base": "light",
        "primary": "#0369A1",
        "bg": "#F1F5F9",
        "secondary_bg": "#E2E8F0",
        "text": "#0F172A",
        "text_secondary": "#334155",
        "border": "#CBD5E1",
        "card_bg": "#FFFFFF",
        "hover_bg": "#E0F2FE"
    }
}

if "app_theme" not in st.session_state:
    st.session_state["app_theme"] = "Dark Mode"

active_theme_name = st.session_state["app_theme"]
th = THEMES.get(active_theme_name, THEMES["Dark Mode"])

# Inject Dynamic Theme CSS + Hide Developer Tools
st.markdown(f"""
    <style>
    /* Developer UI Cleanup */
    #MainMenu {{visibility: hidden; display: none;}}
    footer {{visibility: hidden; display: none;}}
    header {{visibility: hidden; display: none;}}
    [data-testid="stToolbar"] {{visibility: hidden; display: none;}}
    [data-testid="stDecoration"] {{visibility: hidden; display: none;}}
    [data-testid="stStatusWidget"] {{visibility: hidden; display: none;}}
    .viewerBadge_container__1QSob {{display: none;}}

    /* Global Dynamic Theme Variables */
    :root, .stApp, [data-testid="stAppViewContainer"] {{
        --primary-color: {th['primary']} !important;
        --background-color: {th['bg']} !important;
        --secondary-background-color: {th['secondary_bg']} !important;
        --text-color: {th['text']} !important;
    }}

    /* Global Dynamic Theme Palette */
    .stApp, [data-testid="stAppViewContainer"], section.main {{
        background-color: {th['bg']} !important;
        color: {th['text']} !important;
    }}
    [data-testid="stHeader"] {{
        background-color: {th['bg']} !important;
    }}
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {{
        background-color: {th['secondary_bg']} !important;
        border-right: 1px solid {th['border']} !important;
    }}

    /* Containers & Card Borders */
    [data-testid="stVerticalBlockBorderWrapper"] > div {{
        background-color: {th['card_bg']} !important;
        border: 1px solid {th['border']} !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
    }}
    div[data-testid="stExpander"] {{
        background-color: {th['card_bg']} !important;
        border: 1px solid {th['border']} !important;
        border-radius: 8px !important;
    }}
    div[data-testid="stExpander"] summary {{
        color: {th['text']} !important;
    }}
    div[data-testid="stExpander"] summary * {{
        color: {th['text']} !important;
    }}
    div[data-testid="stExpander"] summary svg {{
        fill: {th['text']} !important;
        stroke: {th['text']} !important;
    }}

    /* Global Typography - Headings, Paragraphs, Markdown */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown strong,
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span, [data-testid="stMarkdownContainer"] li,
    label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {{
        color: {th['text']} !important;
    }}

    /* Captions and Subtext with High Contrast */
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *, .stCaption, small {{
        color: {th.get('text_secondary', th['text'])} !important;
        opacity: 0.9 !important;
    }}

    /* Primary Accent Buttons */
    button[kind="primary"] {{
        background-color: {th['primary']} !important;
        border-color: {th['primary']} !important;
    }}
    button[kind="primary"] * {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    /* Secondary Accent Buttons */
    button[kind="secondary"] {{
        background-color: {th['card_bg']} !important;
        border: 1px solid {th['border']} !important;
    }}
    button[kind="secondary"] * {{
        color: {th['text']} !important;
        font-weight: 600 !important;
    }}

    /* Automotive Metrics */
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
        color: {th['primary']} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {{
        color: {th['text']} !important;
        opacity: 0.9 !important;
        font-weight: 600 !important;
    }}

    /* Tabs Styling */
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        color: {th['primary']} !important;
        border-bottom: 3px solid {th['primary']} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {{
        color: {th['primary']} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stTabs"] button[role="tab"] {{
        color: {th['text']} !important;
    }}
    [data-testid="stTabs"] button[role="tab"] * {{
        color: {th['text']} !important;
    }}

    /* Selectboxes and Dropdowns - The Box Itself */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {{
        background-color: {th['card_bg']} !important;
        border-color: {th['border']} !important;
        color: {th['text']} !important;
    }}
    div[data-baseweb="select"] * {{
        color: {th['text']} !important;
    }}
    div[data-baseweb="select"] svg {{
        fill: {th['text']} !important;
    }}

    /* Dropdown Menus and Popovers (Portalled to document body) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[role="listbox"],
    div[data-baseweb="menu"] {{
        background-color: {th['card_bg']} !important;
        border: 1px solid {th['border']} !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }}
    li[role="option"] {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
    }}
    li[role="option"] * {{
        color: {th['text']} !important;
        background-color: transparent !important;
    }}
    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] * {{
        background-color: {th.get('hover_bg', th['border'])} !important;
        color: {th['text']} !important;
    }}

    /* Inputs (Text, Password, Number, Textarea) */
    input, textarea,
    input[type="text"], input[type="password"], input[type="number"],
    div[data-baseweb="input"], div[data-baseweb="base-input"] {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
        border-color: {th['border']} !important;
    }}
    div[data-baseweb="input"] input {{
        color: {th['text']} !important;
        background-color: transparent !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: {th.get('text_secondary', th['text'])} !important;
        opacity: 0.65 !important;
    }}

    /* Radio Buttons & Checkboxes */
    div[data-testid="stRadio"] *,
    div[data-testid="stCheckbox"] * {{
        color: {th['text']} !important;
    }}

    /* Sliders */
    div[data-testid="stSlider"] * {{
        color: {th['text']} !important;
    }}

    /* Tables & Dataframes */
    [data-testid="stDataFrame"], [data-testid="stTable"], table {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
        border: 1px solid {th['border']} !important;
    }}
    th, td {{
        color: {th['text']} !important;
    }}

    /* Dividers */
    hr {{
        border-color: {th['border']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Globals & Credentials
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Verstappen@1")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "Arnav@1909")

def get_db_config():
    """Retrieves database configuration from secrets, environment, or localhost."""
    try:
        if hasattr(st, "secrets") and "mysql" in st.secrets:
            sec = st.secrets["mysql"]
            cfg = {
                "host": sec.get("host", "localhost"),
                "port": int(sec.get("port", 3306)),
                "user": sec.get("user", "root"),
                "passwd": sec.get("password", DB_PASSWORD),
                "database": sec.get("database", "AutoSpec_Database_System")
            }
            if "ssl_ca" in sec:
                cfg["ssl_ca"] = sec["ssl_ca"]
            if "ssl_disabled" in sec:
                cfg["ssl_disabled"] = bool(sec["ssl_disabled"])
            if "ssl_verify_cert" in sec:
                cfg["ssl_verify_cert"] = bool(sec["ssl_verify_cert"])
            return cfg, "Cloud Secrets"
    except Exception:
        pass

    if os.getenv("MYSQL_HOST"):
        cfg = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": int(os.getenv("MYSQL_PORT", 3306)),
            "user": os.getenv("MYSQL_USER", "root"),
            "passwd": os.getenv("MYSQL_PASSWORD", DB_PASSWORD),
            "database": os.getenv("MYSQL_DATABASE", "AutoSpec_Database_System")
        }
        if os.getenv("MYSQL_SSL_CA"):
            cfg["ssl_ca"] = os.getenv("MYSQL_SSL_CA")
        return cfg, "Environment Variables"

    return {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": DB_PASSWORD,
        "database": "AutoSpec_Database_System"
    }, "Localhost Server"

def get_db_connection(cfg=None):
    """Establishes database connection with automatic reconnection handling."""
    if cfg is None:
        cfg, _ = get_db_config()
    try:
        conn = mysql.connector.connect(**cfg)
        return conn
    except mysql.connector.Error as err:
        if getattr(err, "errno", None) == 1049:  # ER_BAD_DB_ERROR
            create_database(cfg)
            try:
                return mysql.connector.connect(**cfg)
            except Exception as e2:
                st.sidebar.error(f"Database Connection Error: {e2}")
                return None
        else:
            st.sidebar.error(f"Database Connection Error ({cfg.get('host')}): {err}")
            return None

def create_database(cfg=None):
    """Initializes database schema if not present on server."""
    if cfg is None:
        cfg, _ = get_db_config()
    db_name = cfg.get("database", "AutoSpec_Database_System")
    try:
        connect_kwargs = {k: v for k, v in cfg.items() if k != "database"}
        temp_conn = mysql.connector.connect(**connect_kwargs)
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        temp_cursor.execute(f"USE `{db_name}`")
    except Exception:
        try:
            temp_conn = mysql.connector.connect(**cfg)
            temp_cursor = temp_conn.cursor()
        except Exception as e:
            st.error(f"Error initializing database on {cfg.get('host')}: {e}")
            return

    try:
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS brands (
                brand_id INT AUTO_INCREMENT PRIMARY KEY, brand_name VARCHAR(50) UNIQUE NOT NULL,
                country_of_origin VARCHAR(50), year_founded INT, created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id INT AUTO_INCREMENT PRIMARY KEY, brand_id INT, model_name VARCHAR(100) NOT NULL,
                body_type VARCHAR(50), category VARCHAR(50),
                FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
            )
        """)
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INT AUTO_INCREMENT PRIMARY KEY, model_id INT, variant_name VARCHAR(150) NOT NULL,
                price_inr DECIMAL(15,2), engine VARCHAR(200), power_bhp INT, torque_nm INT,
                top_speed_kmh INT, acceleration_0_100 DECIMAL(4,2), transmission VARCHAR(100),
                drivetrain VARCHAR(50), fuel_type VARCHAR(50), mileage_range VARCHAR(50),
                seating_capacity INT, safety_rating VARCHAR(50),
                FOREIGN KEY (model_id) REFERENCES models(model_id) ON DELETE CASCADE
            )
        """)
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS features (
                feature_id INT AUTO_INCREMENT PRIMARY KEY, variant_id INT, feature_category VARCHAR(50),
                feature_description TEXT, FOREIGN KEY (variant_id) REFERENCES variants(variant_id) ON DELETE CASCADE
            )
        """)
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS colors (
                color_id INT AUTO_INCREMENT PRIMARY KEY, variant_id INT, color_name TEXT,
                color_type VARCHAR(50), FOREIGN KEY (variant_id) REFERENCES variants(variant_id) ON DELETE CASCADE
            )
        """)
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id VARCHAR(20) PRIMARY KEY, variant_id INT, customer_name VARCHAR(100),
                customer_contact VARCHAR(20), customer_email TEXT, booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'Active', FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
            )
        """)
        temp_conn.commit()
        insert_sample_data(temp_cursor, temp_conn)
        temp_cursor.close()
        temp_conn.close()
    except Exception as e:
        st.error(f"Error creating database tables: {e}")

def generate_sql_dump(cur):
    """Generates an explicit SQL dump for database backup and migration."""
    dump_lines = [
        "-- AutoSpec Database Full Export",
        f"-- Export Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "-- Database: AutoSpec_Database_System",
        "SET FOREIGN_KEY_CHECKS=0;",
        "CREATE DATABASE IF NOT EXISTS `AutoSpec_Database_System`;",
        "USE `AutoSpec_Database_System`;"
    ]
    tables = ['brands', 'models', 'variants', 'features', 'colors', 'bookings']
    for tbl in tables:
        try:
            cur.execute(f"SHOW CREATE TABLE `{tbl}`")
            create_stmt = cur.fetchone()[1]
            dump_lines.append(f"\nDROP TABLE IF EXISTS `{tbl}`;")
            dump_lines.append(f"{create_stmt};")
            cur.execute(f"SELECT * FROM `{tbl}`")
            rows = cur.fetchall()
            if rows:
                col_names = [desc[0] for desc in cur.description]
                col_list = ", ".join([f"`{c}`" for c in col_names])
                dump_lines.append(f"INSERT INTO `{tbl}` ({col_list}) VALUES")
                val_lines = []
                for row in rows:
                    row_vals = []
                    for v in row:
                        if v is None:
                            row_vals.append("NULL")
                        elif isinstance(v, (int, float)):
                            row_vals.append(str(v))
                        else:
                            clean_v = str(v).replace("'", "\\'")
                            row_vals.append(f"'{clean_v}'")
                    val_lines.append(f"  ({', '.join(row_vals)})")
                dump_lines.append(",\n".join(val_lines) + ";")
        except Exception:
            pass
    dump_lines.append("\nSET FOREIGN_KEY_CHECKS=1;\n")
    return "\n".join(dump_lines)

def insert_sample_data(cur, conn):
    print("✓ Inserting data (if not present)...")
    
    # ===================== Brands =====================
    brands = [
        # Original European Luxury
        ('BMW', 'Germany', 1916),
        ('Audi', 'Germany', 1909),
        ('Mercedes-Benz', 'Germany', 1926),
        ('Jaguar', 'United Kingdom', 1922),
        ('Volvo', 'Sweden', 1927),
        # Comprehensive Indian Market Fleet
        ('Ford', 'United States', 1903),
        ('Mahindra', 'India', 1945),
        ('Hyundai', 'South Korea', 1967),
        ('Honda', 'Japan', 1948),
        ('Maruti Suzuki', 'India', 1981),
        ('Tata Motors', 'India', 1945),
        ('Kia', 'South Korea', 1944),
        ('Toyota', 'Japan', 1937),
        ('MG Motor', 'United Kingdom', 1924),
        ('Volkswagen', 'Germany', 1937),
        ('Skoda', 'Czech Republic', 1895),
        ('Jeep', 'United States', 1941),
        ('BYD', 'China', 1995),
        ('Land Rover', 'United Kingdom', 1948),
        ('Porsche', 'Germany', 1931),
        ('Lexus', 'Japan', 1989),
        ('Ferrari', 'Italy', 1939),
        ('Lamborghini', 'Italy', 1963)
    ]
    for b in brands:
        try:
            cur.execute("INSERT INTO brands (brand_name, country_of_origin, year_founded) VALUES (%s, %s, %s)", b)
        except Exception:
            pass
    conn.commit()
    print("✓ All Brands inserted successfully!")

    # ===================== Models =====================
    models = [
        # BMW
        ('BMW', 'X1', 'SUV', 'Compact Luxury'),
        ('BMW', 'X3', 'SUV', 'Mid-size Luxury'),
        ('BMW', 'X5', 'SUV', 'Full-size Luxury'),
        ('BMW', 'X7', 'Luxury SUV', 'Full-size Luxury'),
        ('BMW', 'XM', 'SUV', 'Full-size Luxury'),
        ('BMW', 'iX1 LWB', 'SUV','Electric SUV'),
        ('BMW', 'iX', 'SUV', 'Electric SUV'),
        ('BMW', '2 Series','Gran coupé', 'Luxury'),
        ('BMW', '3 Series LWB','Sedan', 'Luxury'),
        ('BMW', '3 Series','Sedan', 'Performance'),
        ('BMW', '5 Series','Sedan', 'Luxury'),
        ('BMW', '7 Series', 'Sedan', 'Luxury'),
        ('BMW', 'i4', 'Gran Coupé', 'Electric Luxury'),
        ('BMW', 'i5', 'Gran Coupé', 'Electric Luxury'),
        ('BMW', 'i7', 'Sedan', 'Electric Luxury'),
        ('BMW', 'M2', 'Gran coupé', 'Performance'),
        ('BMW', 'M4', 'coupé', 'Performance'),
        ('BMW', 'M5', 'coupé', 'Performance'),
        ('BMW', 'M8', 'coupé', 'Performance'),
        ('BMW', 'Z4', 'Roadster', 'Performance'),
        # Audi
        ('Audi', 'A4', 'Sedan', 'Premium'),
        ('Audi', 'A6', 'Sedan', 'Luxury'),
        ('Audi', 'S5', 'SportBack', 'Performance'),
        ('Audi', 'Q3', 'SUV', 'Compact Luxury'),
        ('Audi', 'Q5', 'SUV', 'Mid-size Luxury'),
        ('Audi', 'Q7', 'SUV', 'Full-size Luxury'),
        ('Audi', 'Q8', 'SUV', 'Ultra-Luxury'),
        ('Audi', 'Q8 e-tron', 'SUV', 'Electric Luxury'),
        ('Audi', 'Q8 Sportback e-tron', 'SUV-coupé', 'Electric Luxury'),
        ('Audi', 'RS e-tron GT', 'Sedan', 'Electric Sports'),
        # Mercedes-Benz
        ('Mercedes-Benz', 'A Class', 'Sedan', 'Luxury'),
        ('Mercedes-Benz', 'C Class', 'Sedan', 'Luxury'),
        ('Mercedes-Benz', 'C Class AMG', 'Sedan', 'Performance'),
        ('Mercedes-Benz', 'E Class', 'Sedan', 'Luxury'),
        ('Mercedes-Benz', 'S Class', 'Sedan', 'Luxury'),
        ('Mercedes-Benz', 'S Class AMG', 'Sedan', 'Performance'),
        ('Mercedes-Benz', 'EQA', 'Sedan', 'Electric Luxury'),
        ('Mercedes-Benz', 'EQB', 'Sedan', 'Electric Luxury'),
        ('Mercedes-Benz', 'EQE', 'Sedan', 'Electric Luxury'),
        ('Mercedes-Benz', 'EQS', 'Sedan', 'Electric Luxury'),
        ('Mercedes-Benz', 'GLA', 'SUV', 'Mid-size Luxury'),
        ('Mercedes-Benz', 'GLA AMG', 'SUV', 'Mid-size Luxury, Performance'),
        ('Mercedes-Benz', 'GLC', 'SUV', 'Mid-size Luxury'),
        ('Mercedes-Benz', 'GLE', 'SUV', 'Mid-size Luxury'),
        ('Mercedes-Benz', 'GLE AMG', 'SUV', 'Mid-size Luxury, Performance'),
        ('Mercedes-Benz', 'GLS', 'SUV', 'Full-size Luxury'),
        ('Mercedes-Benz', 'GLS AMG', 'SUV', 'Mid-size Luxury, Performance'),
        ('Mercedes-Benz', 'G Class', 'SUV', 'Luxury Off-road'),
        ('Mercedes-Benz', 'G Class AMG', 'SUV', 'Performance Off-road'),
        ('Mercedes-Benz', 'CLE Cabriolet AMG', 'Convertible', 'Grand Tourer'),
        # Jaguar
        ('Jaguar', 'F-Pace', 'SUV', 'Mid-size Luxury'),
        # Volvo
        ('Volvo', 'EX30', 'SUV', 'Electric Compact'),
        ('Volvo', 'EX40', 'SUV', 'Electric Mid-size'),
        ('Volvo', 'EC40', 'coupé SUV', 'Electric Luxury'),
        ('Volvo', 'XC60', 'SUV', 'Mid-size Luxury'),
        ('Volvo', 'XC90', 'SUV', 'Full-size Luxury'),
        # Ford
        ('Ford', 'Endeavour', 'SUV', 'Full-size Luxury Off-Road'),
        ('Ford', 'Mustang', 'Coupé', 'American Muscle / Sports'),
        # Mahindra
        ('Mahindra', 'XUV700', 'SUV', 'Mid-size Luxury'),
        ('Mahindra', 'Scorpio-N', 'SUV', 'Rugged Mid-size Off-Road'),
        ('Mahindra', 'Thar', 'SUV', 'Iconic Off-Roader'),
        # Hyundai
        ('Hyundai', 'Creta', 'SUV', 'Compact SUV'),
        ('Hyundai', 'Venue', 'SUV', 'Sub-Compact SUV'),
        ('Hyundai', 'Verna', 'Sedan', 'Premium Sedan'),
        ('Hyundai', 'Bayon', 'Crossover', 'Urban Crossover'),
        # Honda
        ('Honda', 'City', 'Sedan', 'Executive Sedan'),
        ('Honda', 'Elevate', 'SUV', 'Mid-size SUV'),
        # Maruti Suzuki
        ('Maruti Suzuki', 'Swift', 'Hatchback', 'Compact Hatchback'),
        ('Maruti Suzuki', 'Brezza', 'SUV', 'Compact SUV'),
        ('Maruti Suzuki', 'Grand Vitara', 'SUV', 'Mid-size Hybrid SUV'),
        # Tata Motors
        ('Tata Motors', 'Nexon', 'SUV', 'Compact SUV'),
        ('Tata Motors', 'Harrier', 'SUV', 'Mid-size Premium SUV'),
        ('Tata Motors', 'Safari', 'SUV', 'Full-size Luxury SUV'),
        ('Tata Motors', 'Punch', 'SUV', 'Micro SUV'),
        ('Tata Motors', 'Sierra', 'SUV', 'Electric Luxury SUV'),
        ('Tata Motors', 'Curvv', 'Coupé SUV', 'Mid-size Coupé SUV'),
        ('Tata Motors', 'Aeris', 'Sedan', 'Smart Urban EV'),
        # Kia
        ('Kia', 'Seltos', 'SUV', 'Mid-size SUV'),
        ('Kia', 'Sonet', 'SUV', 'Compact SUV'),
        ('Kia', 'EV6', 'Crossover', 'Electric High Performance'),
        # Toyota
        ('Toyota', 'Fortuner', 'SUV', 'Full-size Luxury 4x4'),
        ('Toyota', 'Innova Hycross', 'MPV', 'Luxury Hybrid MPV'),
        ('Toyota', 'Urban Cruiser Hyryder', 'SUV', 'Mid-size Hybrid SUV'),
        # MG Motor
        ('MG Motor', 'Hector', 'SUV', 'Mid-size Internet SUV'),
        ('MG Motor', 'ZS EV', 'SUV', 'Electric Compact SUV'),
        # Volkswagen
        ('Volkswagen', 'Virtus', 'Sedan', 'Performance Sedan'),
        ('Volkswagen', 'Taigun', 'SUV', 'Compact Performance SUV'),
        # Skoda
        ('Skoda', 'Slavia', 'Sedan', 'Premium Performance Sedan'),
        ('Skoda', 'Kushaq', 'SUV', 'Compact SUV'),
        # Jeep
        ('Jeep', 'Compass', 'SUV', 'Premium 4x4 SUV'),
        ('Jeep', 'Wrangler', 'SUV', 'Trail Rated Hardcore Off-Roader'),
        # BYD
        ('BYD', 'Atto 3', 'SUV', 'Electric Compact SUV'),
        ('BYD', 'Seal', 'Sedan', 'Electric Super Sedan'),
        # Land Rover
        ('Land Rover', 'Range Rover', 'SUV', 'Ultra Luxury Flagship'),
        ('Land Rover', 'Defender', 'SUV', 'Expedition Luxury Off-Roader'),
        # Porsche
        ('Porsche', '911', 'Coupé', 'Iconic Sports Car'),
        ('Porsche', 'Macan', 'SUV', 'Performance Luxury SUV'),
        ('Porsche', 'Taycan', 'Sedan', 'Electric Super Sports'),
        # Lexus
        ('Lexus', 'RX', 'SUV', 'Executive Luxury Hybrid'),
        ('Lexus', 'ES', 'Sedan', 'Executive Hybrid Sedan'),
        # Ferrari
        ('Ferrari', 'Roma', 'Coupé', 'Grand Tourer / Supercar'),
        ('Ferrari', '296 GTB', 'Coupé', 'Plug-in Hybrid Supercar'),
        # Lamborghini
        ('Lamborghini', 'Urus', 'SUV', 'Super SUV'),
        ('Lamborghini', 'Revuelto', 'Coupé', 'HPEV V12 Flagship Supercar')
    ]
    # Strict Foreign Key Crosscheck: Verify Brand exists before inserting Model
    cur.execute("SELECT brand_id, brand_name FROM brands")
    valid_brands = {b[1]: b[0] for b in cur.fetchall()}

    for m in models:
        brand_name, model_name, body_type, category = m[0], m[1], m[2], m[3]
        if brand_name not in valid_brands:
            print(f"[DATA INTEGRITY WARNING] Model skipped: Brand '{brand_name}' does not exist in database for Model '{model_name}'.")
            continue

        brand_id = valid_brands[brand_name]
        try:
            cur.execute("""
                SELECT model_id FROM models
                WHERE brand_id = %s AND model_name = %s LIMIT 1
            """, (brand_id, model_name))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO models (brand_id, model_name, body_type, category)
                    VALUES (%s, %s, %s, %s)
                """, (brand_id, model_name, body_type, category))
        except Exception as e:
            if "Duplicate entry" not in str(e):
                print(f"[DATA INTEGRITY ERROR] Error inserting model '{model_name}' for brand '{brand_name}': {e}")
    conn.commit()
    print("✓ All Models inserted successfully!")
    
    # ===================== Variants =====================
    variants = [
        (('Mercedes-Benz', 'A Class'), 'A200','5362000', '1.3L Turbo Petrol', 163, 270, 230, 8.3, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/L', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class'), 'C200','7009000', '1.5L Turbo Petrol Mild Hybrid', 201, 300, 246, 7.3, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class'), 'C220d','7141000', '2.0L Turbo Diesel', 197, 440, 245, 7.3, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid (Electric + Diesel)', '23 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class'), 'C300','7841000', '2.0L Turbo Petrol Mild Hybrid', 255, 400, 250, 6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '22 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class AMG'), 'C 43 4MATIC','11600000', '2.0 L Turbo-Petrol + 48V e-turbo', 402, 500, 250, 4.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class AMG'), 'C 63 SE Performance','20500000', '2.0 L Turbo + PHEV 4.84 kWh battery', 469, 545, 280, 3.4, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Hybrid (Electric + Petrol)', '14.5 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E200','9515000', '2.0L Inline-4 Turbo Petrol', 201, 320, 240, 7.5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Petrol', '15km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E200d','9805000', '2.0L Inline-4 Turbo Diesel', 194, 440, 238, 7.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Diesel', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E450 4Matic','11000000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 4.5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '13 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'S Class'), 'S450 4Matic','23000000', '3.0L Turbocharged Inline-6 (M256) with EQ Boost', 375, 500, 250, 5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'S Class AMG'), 'S 63 E PERFORMANCE', '34600000', '4.0 L Twin-Turbo V8 + 13.1 kWh battery', 794, 1430, 250, 5, 'Automatic (DCT) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '9.5 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQA'), '250 Plus','7092000', '70.5 kWh Battery', 188, 385, 160, 8.6, 'Automatic - 1 Gears, Sport Mode', 'Front Wheel Drive', 'Electric', '560 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQB'), '250 Plus','7615000', '70.5 kWh Battery', 188, 385, 160, 8.9, 'Automatic - 1 Gears, Sport Mode', 'Front Wheel Drive', 'Electric', '464 km', 7, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQB'), '350 4Matic','8317000', '66.5 kWh Battery', 288, 520, 160, 6.2, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '423 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQE'), '500 4Matic','14900000', '90.56 kWh, Battery', 402, 858, 210, 4.9, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '550 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQS'), '450 5 Seater','13800000', '122 kWh Battery', 265, 800, 210, 6.1, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '650 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQS'), '580 4Matic','15300000', '122 kWh Battery', 536, 858, 210, 4.7, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '809 km', 7, 'Not Tested'),
        (('Mercedes-Benz', 'EQS'), '580 4Matic Celebration Edition','13700000', '107.8 kWh Battery', 536, 858, 210, 4.3, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '857 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLA'), 'GLA200','5920000', '1.3L Turbo Petrol', 161, 270, 210, 8.9, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLA'), '220d 4Matic','6365000', '2.0L Turbocharged Diesel', 188, 400, 219, 7.5, 'Automatic (DCT) - 8 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLA AMG'), '220d AMG Line 4Matic','6597000', '2.0L Turbocharged Diesel', 188, 400, 219, 7.5, 'Automatic (DCT) - 8 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLC'), '200d 4Matic','9120000', '2.0L Turbo Diesel', 194 ,440, 219, 8, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14.7 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLC'), '300 4Matic','9120000', '2.0L Turbo Petrol', 255, 400, 240, 6.2, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '19.5 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE'), '450 4MATIC', '13300000', '3.0L Inline-6 (M256) with EQ Boost (mild-hybrid)', 375, 500, 250, 5.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE'), '450d 4MATIC', '13900000', '3.0L OM656 Turbo I6 (diesel)', 362, 750, 250, 5.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '11 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE AMG'), '300d 4MATIC AMG Line', '11800000', '2.0L OM654 Turbo I4 (mild-hybrid)', 265, 550, 230, 6.9, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLS'), '450 4MATIC', '15900000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS'), '450d 4MATIC', '16500000', '3.0L Inline-6 Turbo Diesel', 362, 750, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS AMG'), '450 4MATIC AMG Line', '16300000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS AMG'), '450d 4MATIC AMG Line', '16600000', '3.0L Inline-6 Turbo Diesel', 362, 750, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'G Class'), 'G 580 with EQ Technology', '31000000', '4 × electric motors (1 per wheel), 116 kWh battery', 587, 1164, 180, 4.7, 'Automatic (TC) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Electric', '473 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'G Class AMG'), 'G 63', '43500000', '4.0 L Twin-Turbo V8 + 48V mild-hybrid', 577, 850, 220, 4.4, 'Automatic (DCT) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '6 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'CLE Cabriolet AMG'), 'CLE 300 CABRIOLET 4MATIC', '11700000', '2.0L Inline-4 Turbo Petrol', 255, 400, 250, 6.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '11 km/l', 4, 'Not Tested'),
        (('Jaguar', 'F-Pace'), 'S R-Dynamic 2.0 Petrol', '9237000', '2.0L Ingenium Turbocharged I4', 247, 365, 217, 7.3, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '12.9 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jaguar', 'F-Pace'), 'S R-Dynamic 2.0 Diesel', '9237000', '2.0L Ingenium Turbocharged I4', 201, 430, 210, 8, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Diesel', '19.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'EX30'), 'RWD Ultra', '4100000', '69 kWh Battery', 272, 343, 180, 5.3, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '480', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'EX40'), 'Plus', '5301000', '69 kWh Battery', 238, 420, 180, 7.3, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '475', 5, '5 Star (Euro NCAP)',),
        (('Volvo', 'EC40'), 'Ultra', '6233000', '78 kWh Battery', 408, 660, 180, 4.7, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '530', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC60'), 'B5 Ultra', '8379000', '2.0L Turbo Petrol', 250, 350, 180, 7.1, 'Automatic (TC) - 8 Gears, Manual Override, Sport Mode', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC90'), 'B5 Ultra', '12000000', '2.0L Turbo Petrol + Supercharger + 48V Mild Hybrid', 247, 360, 180, 7.7, 'Automatic (TC) - 8 Gears, Manual Override, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.38 km/l', 7, '5 Star (Euro NCAP)'),
        (('BMW', 'X1'), 'sDrive18i M Sport', '5992000', '1.5L 3-cylinder BMW TwinPower Turbo', 134, 230, 210, 9.2, '7-Speed Automatic (DCT), with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Petrol', '16.35 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X1'), 'sDrive18d M Sport', '6423000', '2.0L 4-cylinder BMW TwinPower Turbo', 148, 360, 210, 8.9, '7-Speed Automatic (DCT), with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Diesel', '20.37 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X3'), 'xDrive20i M Sport', '7120000', '2.0L 4-cylinder BMW TwinPower Turbo', 188, 310, 215, 7.8, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '13.38 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X3'), 'xDrive20d M Sport', '7310000', '2.0L 4-cylinder BMW TwinPower Turbo', 197, 197, 215, 7.7, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Diesel', '16.55 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X5'), 'xDrive40i', '9780000', '3.0L Inline-6 Cylinder BMW TwinPower Turbo', 375, 520, 250, 5.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X5'), 'xDrive30d', '9980000', '3.0L 6-cylinder BMW TwinPower Turbo', 282, 650, 233, 6.1, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Diesel', '12 km/l', 5, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40i M Sport', '15000000', '3.0L 6-cylinder BMW TwinPower Turbo', 375, 520, 250, 5.8, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11.29 km/l', 6, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40d M Sport', '15600000', '3.0L 6-cylinder BMW TwinPower Turbo', 335, 700, 250, 5.9, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Diesel)', '14.31 km/l', 6, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40i M Sport Signature Edition', '15200000', '3.0 L inline-6 turbo-petrol + 48V mild-hybrid', 375, 520, 250, 5.9, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11.29 km/l', 7, 'Not Tested'),
        (('BMW', 'XM'), 'Plug-in Hybrid', '29800000', '4.4L V8 Twin-Turbo + Electric Motor (Plug-in Hybrid)', 644, 800, 250, 4.3, 'Automatic - 8 Gears, Sport Mode', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '61.9 km/l', 5, 'Not Tested'),
        (('BMW', 'iX1 LWB'), 'eDrive20L M Sport', '5185000', '66.4 kWh Battery', 204, 250, 175, 8.6, 'Automatic - 1 Gears, Sport Mode', 'sDrive', 'Electric', '531 km', 5, 'Not Tested'),
        (('BMW', 'iX'), 'xDrive 50', '12800000', '76.6 kWh Battery', 516, 765, 200, 4.6, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '635 km', 5, 'Not Tested'),
        (('BMW', '2 Series'), '218 M Sport', '5460000', '1.5L 3-Cylinder Turbo Petrol', 154, 230, 230, 8.6, '7-speed Steptronic Dual-Clutch Automatic', 'sDrive', 'Petrol', '16.35 km/l', 4, 'Not Tested'),
        (('BMW', '2 Series'), '218 M Sport Pro', '5460000', '1.5L 3-Cylinder Turbo Petrol', 154, 230, 230, 8.6, '7-speed Steptronic Dual-Clutch Automatic', 'sDrive', 'Petrol', '16.35 km/l', 4, 'Not Tested'),
        (('BMW', 'M2'), '3.0 Petrol', '12000000', '3.0L Twin Turbo Inline-6', 473, 600, 250, 4, '6-Speed Automatic, with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Petrol', '10 km/l', 4, 'Not Tested'),
        (('BMW', '3 Series LWB'), '330 Li M Sport', '7184000', '2.0 L Twin-Turbo Inline-4 Petrol', 255, 400, 250, 6.2, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '15.4 km/l', 5, 'Not Tested'),
        (('BMW', '3 Series LWB'), '320 Ld M Sport', '7116000', '2.0 L Twin-Turbo Inline-4 Diesel', 188, 400, 250, 7.6, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '19.6 km/l', 5, 'Not Tested'),
        (('BMW', '3 Series'), 'M340i', '8703000', '3.0 L inline-6 Twin-Turbo (B58) Petrol', 369, 500, 250, 4.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '13.02 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'M4'), 'Competition', '18100000', '3.0 L Twin-Turbo Inline-6 (S58)', 523, 650, 250, 3.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '10 km/l', 4, '5★ (Euro NCAP)'),
        (('BMW', 'M4'), 'CS', '22000000', '3.0 L Twin-Turbo Inline-6 (S58)', 543, 650, 250, 3.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '10.24 km/l', 4, '5★ (Euro NCAP)'),
        (('BMW', 'i4'), 'eDrive40 M Sport', '8455000', '70.2 kWh Battery', 282, 430, 250, 6, 'Automatic - 1 Gears, Sport Mode', 'sDrive', 'Electric', '483 km', 5, 'Not Tested'),
        (('BMW', '5 Series'), '530Li M Sport', '8842000', '2.0L 4-cylinder TwinPower Turbo Petrol', 255, 400, 250, 6.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '15.7 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'M5'), 'Competition', '20900000', '4.4L M TwinPower Turbo V8', 717, 1000, 250, 3.3, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '14 km/l', 5, 'Not Tested'),
        (('BMW', 'i5'), 'M60 xDrive', '13600000', '83.9 kWh Battery', 601, 795, 230, 3.8, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '516 km', 4, 'Not Tested'),
        (('BMW', '7 Series'), '740i M Sport', '21100000', '3.0L Twin Turbo Inline-6', 375, 520, 250, 5.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '12.61 km/l', 5, 'Not Tested'),
        (('BMW', '7 Series'), '740d M Sport', '21600000', '3.0L Twin Turbo Inline-6', 282, 650, 250, 6, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Diesel', '16.55 km/l', 5, 'Not Tested'),
        (('BMW', 'i7'), 'eDrive50 M Sport', '21600000', '101.7 kWh Battery', 449, 650, 250, 5.5, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '603 km', 5, 'Not Tested'),
        (('BMW', 'i7'), 'M70 xDrive', '26300000', '101.7 kWh Battery', 650, 1015, 250, 3.7, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '560 km', 5, 'Not Tested'),
        (('BMW', 'M8'), 'Competition Coupé', '28300000', '4.4L TwinPower Turbo V8 Petrol', 617, 750, 250, 3.2, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '8.77 km/l', 4, 'Not Tested'),
        (('BMW', 'Z4'), 'M40i', '10800000', '3.0L 6-cylinder TwinPower Turbo Petrol', 335, 500, 250, 4.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '12.09 km/l', 2, '5★ (Euro NCAP)'),
        (('Audi', 'A4'), 'Premium 40 TFSI','4699000', '2.0L TFSI Petrol', 201, 320,241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A4'), 'Premium Plus 40 TFSI','5199000', '2.0L TFSI Petrol', 201, 320, 241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A4'), 'Technology 40 TFSI','5584000', '2.0L TFSI Petrol', 201, 320, 241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Premium Plus 45 TFSI','8382000', '2.0L 4-cylinder TFSI Petrol', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Technology 45 TFSI (Without Matrix)','8198000', '2.0L TFSI Petrol', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '14 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Technology 45 TFSI','9185000', '2.0L Turbocharged Inline-4 (TFSI)', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '14 km/l', 5, '5-star (Euro NCAP)'),
        (('Audi', 'Q3'), 'Premium Plus 40 TFSI quattro S tronic','6294000', '2.0 L 4-cylinder TFSI', 188, 320, 222, 7.3, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '14.93 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q3'), 'Technology 40 TFSI quattro S tronic','6987000', '2.0 L 4-cylinder TFSI', 188, 320, 222, 7.3, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '14.93 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q5'), 'Premium Plus 45 TFSI','8543000', '2.0L TFSI Turbocharged I4', 261, 370, 240, 6.1, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '13.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q5'), 'Technology 45 TFSI','9214000', '2.0L TFSI Turbocharged I4', 261, 370, 240, 6.1, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '13.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q7'), 'Premium Plus TFSI quattro tiptronic','11300000', '3.0 TFSI V6 + 48V Mild-Hybrid System', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '11.2 km/l', 7, '5-Star (Euro NCAP)'),
        (('Audi', 'Q7'), 'Technology TFSI quattro tiptronic','12500000', '3.0 TFSI V6 + 48V Mild-Hybrid System', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '11.2 km/l', 7, '5-Star (Euro NCAP)'),
        (('Audi', 'Q8'), 'TFSI quattro tiptronic','15000000', '3.0 L V6 TFSI (Turbocharged)', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift', 'All Wheel Drive', 'Petrol', '8 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q8'), 'quattro tiptronic','31700000', '4.0 L V8 Twin-Turbo (TFSI)', 648, 850, 305, 3.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '9 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'S5'), 'SportBack 3.0 TFSI Quattro','9943000', '3.0L V6 TFSI Turbocharged', 349, 500, 250, 4.8, 'Automatic (TC) - 8 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '10.6 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 e-tron'), '50 e-tron quattro','13600000', 'Battery (95 kWh Battery, 114 Volt)', 335, 664, 200, 6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (491 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 e-tron'), '55 e-tron quattro','15100000', 'Battery (114 kWh Battery, 114 Volt)', 402, 664, 200, 5.6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (582 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 Sportback e-tron'), '50 e-tron quattro','14200000', 'Battery (95 kWh)', 335, 664, 200, 6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (491 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 Sportback e-tron'), '55 e-tron quattro','15600000', 'Battery (114 kWh)', 402, 664, 200, 5.6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (582 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'RS e-tron GT'), 'e-tron quattro','23100000', 'Battery (93.4 kWh)', 637, 830, 250, 3.3, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (401 km)', 5, '5-Star (Euro NCAP)'),
        # --- Indian Market Additions ---
        # Ford
        (('Ford', 'Endeavour'), 'Titanium+ 2.0 4x4 AT', '3625000', '2.0L EcoBlue Bi-Turbo Diesel', 168, 420, 180, 10.2, 'Automatic (TC) - 10 Gears, Terrain Management', 'Four-Wheel Drive', 'Diesel', '12.4 km/l', 7, '5 Star (ANCAP)'),
        (('Ford', 'Mustang'), 'GT V8', '7461000', '5.0L Ti-VCT V8 Naturally Aspirated Petrol', 395, 515, 250, 4.8, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Rear Wheel Drive', 'Petrol', '7.9 km/l', 4, '3 Star (Euro NCAP)'),

        # Mahindra
        (('Mahindra', 'XUV700'), 'AX7 Diesel AT Luxury Pack AWD', '2699000', '2.2L mHawk Turbo Diesel', 182, 450, 200, 9.8, 'Automatic (TC) - 6 Gears', 'All-Wheel Drive', 'Diesel', '16.5 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Scorpio-N'), 'Z8L Diesel 4x4 AT', '2454000', '2.2L mHawk CRDe Turbo Diesel', 172, 400, 175, 10.5, 'Automatic (TC) - 6 Gears', 'Four-Wheel Drive', 'Diesel', '15.2 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Thar'), 'LX 4-Str Hard Top Diesel AT 4WD', '1760000', '2.2L mHawk 130 CRDe Turbo Diesel', 130, 300, 155, 12.5, 'Automatic (TC) - 6 Gears', 'Four-Wheel Drive', 'Diesel', '15.2 km/l', 4, '4 Star (Global NCAP)'),

        # Hyundai
        (('Hyundai', 'Creta'), 'SX (O) 1.5 Diesel AT', '2015000', '1.5L U2 CRDi Diesel', 114, 250, 170, 11.5, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '19.1 km/l', 5, '3 Star (Global NCAP)'),
        (('Hyundai', 'Venue'), 'SX (O) 1.0 Turbo DCT', '1338000', '1.0L Kappa Turbo GDi Petrol', 118, 172, 165, 10.9, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.3 km/l', 5, '4 Star (ANCAP)'),
        (('Hyundai', 'Verna'), 'SX (O) 1.5 Turbo DCT', '1742000', '1.5L Turbo GDi Petrol', 158, 253, 210, 8.1, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '20.6 km/l', 5, '5 Star (Global NCAP)'),
        (('Hyundai', 'Bayon'), '1.5 NA MT', '950000', '1.5L MPI Naturally Aspirated Petrol', 113, 144, 160, 11.8, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '18.5 km/l', 5, '4 Star (Euro NCAP)'),

        # Honda
        (('Honda', 'City'), 'ZX CVT', '1635000', '1.5L i-VTEC DOHC Petrol', 119, 145, 180, 10.5, 'Automatic (CVT) - 7-Speed Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.4 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('Honda', 'Elevate'), 'ZX CVT', '1620000', '1.5L i-VTEC DOHC Petrol', 119, 145, 170, 11.2, 'Automatic (CVT) - 7-Speed Paddle Shift', 'Front Wheel Drive', 'Petrol', '16.9 km/l', 5, '5 Star (Bharat NCAP)'),

        # Maruti Suzuki
        (('Maruti Suzuki', 'Swift'), 'ZXi Plus AMT', '960000', '1.2L Z12E 3-Cylinder Petrol', 80, 112, 160, 12.5, 'Automatic (AMT) - 5 Gears', 'Front Wheel Drive', 'Petrol', '25.75 km/l', 5, '4 Star (Euro NCAP)'),
        (('Maruti Suzuki', 'Brezza'), 'ZXi Plus AT', '1398000', '1.5L K15C Smart Hybrid Petrol', 102, 137, 165, 12.8, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.8 km/l', 5, '4 Star (Global NCAP)'),
        (('Maruti Suzuki', 'Grand Vitara'), 'Alpha+ Strong Hybrid e-CVT', '2009000', '1.5L Intelligent Electric Hybrid + 177.6V Li-ion', 114, 141, 175, 11.0, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '27.97 km/l', 5, '5 Star (Bharat NCAP)'),

        # Tata Motors
        (('Tata Motors', 'Nexon'), 'Fearless Plus S 1.2 DCA', '1499000', '1.2L Revotron Turbocharged Petrol', 118, 170, 170, 10.8, 'Automatic (DCA) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '17.1 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Harrier'), 'Fearless+ Dark Edition AT', '2644000', '2.0L Kryotec Turbocharged Diesel', 168, 350, 180, 9.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.8 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Safari'), 'Accomplished+ Dark Edition AT', '2734000', '2.0L Kryotec Turbocharged Diesel', 168, 350, 180, 10.1, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.3 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Punch'), 'Creative AMT', '1020000', '1.2L Revotron Naturally Aspirated Petrol', 87, 115, 150, 13.5, 'Automatic (AMT) - 5 Gears', 'Front Wheel Drive', 'Petrol', '18.8 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Sierra'), 'EV Empowered AWD', '2500000', 'Dual PMSM Motors + 69 kWh Battery', 220, 400, 180, 6.9, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '550 km', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Curvv'), 'Creative 1.5 Diesel AT', '1769000', '1.5L Kryojet Turbocharged Diesel', 116, 260, 175, 11.2, 'Automatic (DCA) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '21.5 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Aeris'), 'Smart EV', '1250000', 'Permanent Magnet AC Motor + 30.2 kWh Battery', 74, 114, 130, 11.9, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '325 km', 5, '5 Star (Bharat NCAP)'),

        # Kia
        (('Kia', 'Seltos'), 'X-Line 1.5 Diesel AT', '2035000', '1.5L CRDi VGT Diesel', 114, 250, 175, 11.4, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '19.1 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Sonet'), 'X-Line 1.0 Turbo DCT', '1475000', '1.0L Smartstream Turbo GDi Petrol', 118, 172, 168, 10.7, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.2 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'EV6'), 'GT-Line AWD', '6595000', 'Dual Motor 77.4 kWh Lithium-Ion Battery', 320, 605, 192, 5.2, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '708 km', 5, '5 Star (Euro NCAP)'),

        # Toyota
        (('Toyota', 'Fortuner'), 'GR-S 2.8 Diesel 4x4 AT', '5144000', '2.8L 1GD-FTV Turbocharged Diesel', 201, 500, 180, 9.8, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Four-Wheel Drive', 'Diesel', '14.2 km/l', 7, '5 Star (ANCAP)'),
        (('Toyota', 'Innova Hycross'), 'ZX(O) Hybrid', '3098000', '2.0L TNGA 4-Cylinder Petrol Hybrid (e-Drive)', 184, 206, 170, 9.5, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '23.24 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Urban Cruiser Hyryder'), 'V Hybrid', '1999000', '1.5L TNGA 3-Cylinder Strong Hybrid + 177.6V Li-ion', 114, 141, 170, 11.2, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '27.97 km/l', 5, '5 Star (Bharat NCAP)'),

        # MG Motor
        (('MG Motor', 'Hector'), 'Savvy Pro 1.5 CVT', '2225000', '1.5L Turbocharged Intercooled Petrol', 141, 250, 170, 11.5, 'Automatic (CVT) - 8-Step Mode', 'Front Wheel Drive', 'Petrol', '13.8 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('MG Motor', 'ZS EV'), 'Exclusive Pro', '2544000', '50.3 kWh Prismatic Battery', 174, 280, 175, 8.5, 'Automatic - 1 Gears, Sport Mode', 'Front Wheel Drive', 'Electric', '461 km', 5, '5 Star (Euro NCAP)'),

        # Volkswagen
        (('Volkswagen', 'Virtus'), 'GT Plus 1.5 TSI DSG', '1940000', '1.5L TSI EVO Turbocharged Petrol with ACT', 148, 250, 190, 8.7, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.62 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Taigun'), 'GT Plus 1.5 TSI DSG', '1970000', '1.5L TSI EVO Turbocharged Petrol with ACT', 148, 250, 185, 8.9, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.41 km/l', 5, '5 Star (Global NCAP)'),

        # Skoda
        (('Skoda', 'Slavia'), 'Style 1.5 TSI DSG', '1913000', '1.5L TSI Turbocharged Petrol with ACT', 148, 250, 190, 8.8, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.36 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Kushaq'), 'Style 1.5 TSI DSG', '1979000', '1.5L TSI Turbocharged Petrol with ACT', 148, 250, 185, 8.9, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.86 km/l', 5, '5 Star (Global NCAP)'),

        # Jeep
        (('Jeep', 'Compass'), 'Model S 4x4 Diesel AT', '3241000', '2.0L Multijet II Turbocharged Diesel', 168, 350, 190, 10.1, 'Automatic (TC) - 9 Gears, Selec-Terrain 4WD', 'Four-Wheel Drive', 'Diesel', '15.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jeep', 'Wrangler'), 'Rubicon', '7165000', '2.0L GME T4 Turbocharged Inline-4 Petrol', 268, 400, 160, 7.8, 'Automatic (TC) - 8 Gears, Rock-Trac 4x4', 'Four-Wheel Drive', 'Petrol', '10.6 km/l', 5, '4 Star (Euro NCAP)'),

        # BYD
        (('BYD', 'Atto 3'), 'Extended Range', '3399000', '60.48 kWh Blade Battery', 201, 310, 160, 7.3, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '521 km', 5, '5 Star (Euro NCAP)'),
        (('BYD', 'Seal'), 'Performance AWD', '4555000', '82.56 kWh Blade Battery (Dual Motor)', 523, 670, 180, 3.8, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '580 km', 5, '5 Star (Euro NCAP)'),

        # Land Rover
        (('Land Rover', 'Range Rover'), 'Autobiography 3.0 LWB', '31500000', '3.0L Inline-6 Turbocharged Petrol Mild Hybrid', 394, 550, 242, 5.9, 'Automatic (TC) - 8 Gears, Paddle Shift', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '10.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Defender'), '110 HSE 3.0 Diesel', '12800000', '3.0L Inline-6 D300 Twin Turbocharged Diesel', 296, 650, 191, 7.0, 'Automatic (TC) - 8 Gears, Terrain Response 2', 'All-Wheel Drive', 'Diesel', '11.5 km/l', 7, '5 Star (Euro NCAP)'),

        # Porsche
        (('Porsche', '911'), 'Carrera S', '20100000', '3.0L Twin-Turbo Flat-6 Boxer Petrol', 444, 530, 308, 3.5, 'Automatic (PDK) - 8 Gears, Paddle Shift', 'Rear Wheel Drive', 'Petrol', '9.0 km/l', 4, '5 Star (Euro NCAP)'),
        (('Porsche', 'Macan'), 'Macan S', '10500000', '2.9L Twin-Turbo V6 Petrol', 375, 520, 259, 4.6, 'Automatic (PDK) - 7 Gears, Paddle Shift', 'All-Wheel Drive', 'Petrol', '10.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Porsche', 'Taycan'), 'Turbo S', '26900000', '93.4 kWh Performance Battery Plus (Dual PMSM)', 750, 1050, 260, 2.8, 'Automatic - 2-Speed Rear Transmission', 'All-Wheel Drive', 'Electric', '452 km', 4, '5 Star (Euro NCAP)'),

        # Lexus
        (('Lexus', 'RX'), '350h Luxury', '9580000', '2.5L 4-Cylinder Petrol Hybrid + E-Four Motor', 247, 316, 200, 7.9, 'Automatic (e-CVT)', 'All-Wheel Drive', 'Hybrid (Electric + Petrol)', '18.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Lexus', 'ES'), '300h Luxury', '6970000', '2.5L 4-Cylinder Petrol Hybrid (A25A-FXS)', 215, 221, 180, 8.9, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '22.58 km/l', 5, '5 Star (Euro NCAP)'),

        # Ferrari
        (('Ferrari', 'Roma'), 'Coupe', '37600000', '3.9L Twin-Turbocharged V8 Petrol', 612, 760, 320, 3.4, 'Automatic (DCT) - 8 Gears, F1 Dual-Clutch', 'Rear Wheel Drive', 'Petrol', '8.9 km/l', 2, 'Not Tested'),
        (('Ferrari', '296 GTB'), 'Coupe', '54000000', '3.0L 120° Twin-Turbo V6 + Electric Motor (PHEV)', 819, 740, 330, 2.9, 'Automatic (DCT) - 8 Gears, F1 Dual-Clutch', 'Rear Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '13.5 km/l', 2, 'Not Tested'),

        # Lamborghini
        (('Lamborghini', 'Urus'), 'Performante', '42200000', '4.0L Twin-Turbo V8 Petrol', 657, 850, 306, 3.3, 'Automatic (TC) - 8 Gears, Paddle Shift', 'All-Wheel Drive', 'Petrol', '7.1 km/l', 5, 'Not Tested'),
        (('Lamborghini', 'Revuelto'), 'Coupe', '88900000', '6.5L Naturally Aspirated V12 + 3 Electric Motors (HPEV)', 1001, 1062, 350, 2.5, 'Automatic (DCT) - 8 Gears, Paddle Shift', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '8.4 km/l', 2, 'Not Tested'),
        # --- Additional 146 Real-World Production Variants ---
        (('Ford', 'Endeavour'), 'Titanium 4x2 AT', '3350000', '2.0L EcoBlue Turbo Diesel', 168, 420, 180, 10.8, 'Automatic (TC) - 10 Gears', 'Rear Wheel Drive', 'Diesel', '13.2 km/l', 7, '5 Star (ANCAP)'),
        (('Ford', 'Endeavour'), 'Sport Edition 4x4 AT', '3780000', '2.0L EcoBlue Bi-Turbo Diesel', 168, 420, 180, 10.1, 'Automatic (TC) - 10 Gears, Terrain Management', 'Four-Wheel Drive', 'Diesel', '12.4 km/l', 7, '5 Star (ANCAP)'),
        (('Ford', 'Mustang'), 'EcoBoost 2.3L Fastback', '5500000', '2.3L EcoBoost Twin-Scroll Turbocharged Petrol', 310, 475, 240, 5.1, 'Automatic (TC) - 10 Gears, Paddle Shift', 'Rear Wheel Drive', 'Petrol', '10.5 km/l', 4, '4 Star (Euro NCAP)'),
        (('Ford', 'Mustang'), 'Mach 1 V8', '8400000', '5.0L Ti-VCT V8 Naturally Aspirated Petrol', 480, 569, 267, 4.2, 'Automatic (TC) - 10 Gears, Rev-Matching', 'Rear Wheel Drive', 'Petrol', '7.2 km/l', 4, '3 Star (Euro NCAP)'),
        (('Mahindra', 'XUV700'), 'AX5 Petrol MT 5-Str', '1689000', '2.0L mStallion Turbo GDi Petrol', 197, 380, 195, 9.4, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '13.0 km/l', 5, '5 Star (Global NCAP)'),
        (('Mahindra', 'XUV700'), 'AX7 Petrol AT 7-Str', '2199000', '2.0L mStallion Turbo GDi Petrol', 197, 380, 200, 9.1, 'Automatic (TC) - 6 Gears', 'Front Wheel Drive', 'Petrol', '12.5 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'XUV700'), 'AX7L Diesel AT AWD 7-Str', '2649000', '2.2L mHawk Turbo Diesel', 182, 450, 200, 9.8, 'Automatic (TC) - 6 Gears', 'All-Wheel Drive', 'Diesel', '16.5 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Scorpio-N'), 'Z4 Diesel MT 7-Str', '1590000', '2.2L mHawk CRDe Turbo Diesel', 172, 370, 175, 11.2, 'Manual - 6 Gears', 'Rear Wheel Drive', 'Diesel', '16.0 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Scorpio-N'), 'Z8 Petrol AT 7-Str', '2115000', '2.0L mStallion Turbo GDi Petrol', 200, 380, 185, 9.5, 'Automatic (TC) - 6 Gears', 'Rear Wheel Drive', 'Petrol', '12.8 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Scorpio-N'), 'Z8 Select Diesel MT 7-Str', '1799000', '2.2L mHawk CRDe Turbo Diesel', 172, 370, 175, 11.0, 'Manual - 6 Gears', 'Rear Wheel Drive', 'Diesel', '15.8 km/l', 7, '5 Star (Global NCAP)'),
        (('Mahindra', 'Thar'), 'AX Opt 4-Str Diesel MT 4WD', '1485000', '2.2L mHawk 130 CRDe Turbo Diesel', 130, 300, 155, 13.0, 'Manual - 6 Gears, Shift-on-Fly Transfer Case', 'Four-Wheel Drive', 'Diesel', '15.2 km/l', 4, '4 Star (Global NCAP)'),
        (('Mahindra', 'Thar'), 'Earth Edition Petrol AT 4WD', '1715000', '2.0L mStallion 150 TGDi Petrol', 150, 320, 160, 10.2, 'Automatic (TC) - 6 Gears', 'Four-Wheel Drive', 'Petrol', '12.0 km/l', 4, '4 Star (Global NCAP)'),
        (('Mahindra', 'Thar'), 'Roxx AX7L 4x4 Diesel AT', '2249000', '2.2L mHawk Turbo Diesel Gen 2', 172, 400, 175, 10.1, 'Automatic (TC) - 6 Gears', 'Four-Wheel Drive', 'Diesel', '15.0 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Hyundai', 'Creta'), 'E 1.5 Petrol MT', '1099000', '1.5L Smartstream MPi Petrol', 113, 144, 165, 12.0, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5, '3 Star (Global NCAP)'),
        (('Hyundai', 'Creta'), 'EX 1.5 Diesel MT', '1379000', '1.5L U2 CRDi Turbo Diesel', 114, 250, 170, 11.8, 'Manual - 6 Gears', 'Front Wheel Drive', 'Diesel', '21.8 km/l', 5, '3 Star (Global NCAP)'),
        (('Hyundai', 'Creta'), 'SX Tech 1.5 Petrol IVT', '1748000', '1.5L Smartstream MPi Petrol', 113, 144, 165, 11.6, 'Automatic (IVT / CVT)', 'Front Wheel Drive', 'Petrol', '17.7 km/l', 5, '3 Star (Global NCAP)'),
        (('Hyundai', 'Creta'), 'N Line N8 1.5 Turbo DCT', '1834000', '1.5L Kappa Turbo GDi Petrol', 158, 253, 195, 8.9, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.4 km/l', 5, '3 Star (Global NCAP)'),
        (('Hyundai', 'Venue'), 'S Plus 1.2 Petrol MT', '935000', '1.2L Kappa MPi Petrol', 82, 114, 155, 13.8, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '17.5 km/l', 5, '4 Star (ANCAP)'),
        (('Hyundai', 'Venue'), 'N Line N8 1.0 Turbo DCT', '1390000', '1.0L Turbo GDi Petrol', 118, 172, 175, 10.4, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.3 km/l', 5, '4 Star (ANCAP)'),
        (('Hyundai', 'Verna'), 'S 1.5 MPi MT', '1199000', '1.5L Smartstream MPi Petrol', 113, 144, 185, 10.9, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '18.6 km/l', 5, '5 Star (Global NCAP)'),
        (('Hyundai', 'Verna'), 'SX 1.5 MPi IVT', '1435000', '1.5L Smartstream MPi Petrol', 113, 144, 185, 10.7, 'Automatic (IVT / CVT), Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.6 km/l', 5, '5 Star (Global NCAP)'),
        (('Hyundai', 'Bayon'), '1.0 T-GDi DCT', '1150000', '1.0L Turbocharged 3-Cylinder GDi Petrol', 118, 172, 185, 10.2, 'Automatic (DCT) - 7 Gears', 'Front Wheel Drive', 'Petrol', '18.8 km/l', 5, '4 Star (Euro NCAP)'),
        (('Honda', 'City'), 'V MT', '1208000', '1.5L i-VTEC DOHC Petrol with VTC', 119, 145, 185, 10.2, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '17.8 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('Honda', 'City'), 'VX CVT', '1425000', '1.5L i-VTEC DOHC Petrol with VTC', 119, 145, 180, 10.6, 'Automatic (CVT) - 7-Speed Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.4 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('Honda', 'City'), 'e:HEV Hybrid ZX', '2055000', '1.5L Atkinson Cycle Petrol + Dual Electric Motor', 125, 253, 175, 9.8, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '27.13 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('Honda', 'Elevate'), 'V MT', '1211000', '1.5L i-VTEC DOHC Petrol', 119, 145, 170, 11.5, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '15.3 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Honda', 'Elevate'), 'VX CVT', '1430000', '1.5L i-VTEC DOHC Petrol', 119, 145, 170, 11.2, 'Automatic (CVT) - 7-Speed Paddle Shift', 'Front Wheel Drive', 'Petrol', '16.9 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Honda', 'Elevate'), 'Apex Edition ZX CVT', '1650000', '1.5L i-VTEC DOHC Petrol', 119, 145, 170, 11.2, 'Automatic (CVT) - 7-Speed Paddle Shift', 'Front Wheel Drive', 'Petrol', '16.9 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Maruti Suzuki', 'Swift'), 'LXi 1.2 MT', '649000', '1.2L Z12E 3-Cylinder Petrol', 80, 112, 160, 13.0, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '24.8 km/l', 5, '4 Star (Euro NCAP)'),
        (('Maruti Suzuki', 'Swift'), 'VXi 1.2 AMT', '780000', '1.2L Z12E 3-Cylinder Petrol', 80, 112, 160, 12.8, 'Automatic (AMT) - 5 Gears', 'Front Wheel Drive', 'Petrol', '25.75 km/l', 5, '4 Star (Euro NCAP)'),
        (('Maruti Suzuki', 'Swift'), 'ZXi 1.2 MT', '830000', '1.2L Z12E 3-Cylinder Petrol', 80, 112, 160, 12.5, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '24.8 km/l', 5, '4 Star (Euro NCAP)'),
        (('Maruti Suzuki', 'Brezza'), 'LXi 1.5 MT', '834000', '1.5L K15C Smart Hybrid Petrol', 102, 137, 165, 13.2, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '19.89 km/l', 5, '4 Star (Global NCAP)'),
        (('Maruti Suzuki', 'Brezza'), 'VXi 1.5 AT', '1110000', '1.5L K15C Smart Hybrid Petrol', 102, 137, 165, 12.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.8 km/l', 5, '4 Star (Global NCAP)'),
        (('Maruti Suzuki', 'Brezza'), 'ZXi 1.5 MT', '1115000', '1.5L K15C Smart Hybrid Petrol', 102, 137, 165, 12.6, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '19.89 km/l', 5, '4 Star (Global NCAP)'),
        (('Maruti Suzuki', 'Grand Vitara'), 'Delta 1.5 AT', '1360000', '1.5L K15C Mild Hybrid Petrol', 102, 137, 170, 12.4, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '20.58 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Maruti Suzuki', 'Grand Vitara'), 'Zeta+ Strong Hybrid e-CVT', '1843000', '1.5L Strong Hybrid + Li-ion Battery', 114, 141, 175, 11.1, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '27.97 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Maruti Suzuki', 'Grand Vitara'), 'Alpha AllGrip AWD MT', '1701000', '1.5L K15C Mild Hybrid Petrol', 102, 137, 168, 12.9, 'Manual - 5 Gears, AllGrip Auto Mode', 'All-Wheel Drive', 'Petrol', '19.38 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Nexon'), 'Smart 1.2 Petrol MT', '799000', '1.2L Revotron Turbocharged Petrol', 118, 170, 165, 11.5, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '17.44 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Nexon'), 'Pure S 1.2 Petrol AMT', '1030000', '1.2L Revotron Turbocharged Petrol', 118, 170, 168, 11.2, 'Automatic (AMT) - 6 Gears', 'Front Wheel Drive', 'Petrol', '17.18 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Nexon'), 'Creative+ 1.5 Diesel AMT', '1370000', '1.5L Revotorq Turbo Diesel', 113, 260, 170, 11.4, 'Automatic (AMT) - 6 Gears', 'Front Wheel Drive', 'Diesel', '23.23 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Nexon'), 'EV Empowered Plus 45 kWh', '1699000', 'Permanent Magnet Synchronous Motor + 45 kWh Battery', 143, 215, 150, 8.9, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '489 km', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Harrier'), 'Smart MT', '1549000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 10.5, 'Manual - 6 Gears', 'Front Wheel Drive', 'Diesel', '16.8 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Harrier'), 'Adventure+ A Dark AT', '2269000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 9.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.8 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Harrier'), 'Fearless+ Stealth AT', '2644000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 9.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.8 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Safari'), 'Pure+ MT 7-Str', '1799000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 10.6, 'Manual - 6 Gears', 'Front Wheel Drive', 'Diesel', '16.3 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Safari'), 'Adventure+ Dark AT 7-Str', '2349000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 10.1, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.3 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Safari'), 'Accomplished 6-Str Captain Seats AT', '2699000', '2.0L Kryotec Turbo Diesel', 168, 350, 180, 10.1, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '16.3 km/l', 6, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Punch'), 'Pure MT', '613000', '1.2L Revotron Naturally Aspirated Petrol', 87, 115, 150, 14.1, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '20.09 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Punch'), 'Adventure Rhythm AMT', '785000', '1.2L Revotron Petrol', 87, 115, 150, 13.8, 'Automatic (AMT) - 5 Gears', 'Front Wheel Drive', 'Petrol', '18.8 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Punch'), 'Accomplished Dazzle Sunroof AMT', '920000', '1.2L Revotron Petrol', 87, 115, 150, 13.5, 'Automatic (AMT) - 5 Gears', 'Front Wheel Drive', 'Petrol', '18.8 km/l', 5, '5 Star (Global NCAP)'),
        (('Tata Motors', 'Punch'), 'EV Empowered Plus 35 kWh', '1429000', 'Permanent Magnet AC Motor + 35 kWh Battery', 120, 190, 140, 9.5, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '421 km', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Curvv'), 'Creative+ S 1.2 Hyperion Turbo DCA', '1619000', '1.2L Hyperion Direct Injection Turbo Petrol', 123, 225, 180, 9.7, 'Automatic (DCA) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '17.5 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Curvv'), 'Accomplished+ 1.5 Diesel AT', '1900000', '1.5L Kryojet Turbocharged Diesel', 116, 260, 175, 11.2, 'Automatic (DCA) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '21.5 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Curvv'), 'Curvv.ev Empowered+ 55 kWh', '2199000', 'PMSM Motor + 55 kWh Battery', 165, 215, 160, 8.6, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '585 km', 5, '5 Star (Bharat NCAP)'),
        (('Tata Motors', 'Sierra'), 'EV Adventure RWD', '2100000', 'Single PMSM Motor + 55 kWh Battery', 170, 280, 170, 7.8, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '480 km', 5, '5 Star (Bharat NCAP)'),
        (('Kia', 'Seltos'), 'HTE 1.5 Petrol MT', '1090000', '1.5L Smartstream MPi Petrol', 113, 144, 170, 11.8, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '17.0 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Seltos'), 'HTX 1.5 Turbo DCT', '1830000', '1.5L Smartstream Turbo GDi Petrol', 158, 253, 195, 8.9, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '17.9 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Seltos'), 'GTX+ 1.5 Diesel AT', '2000000', '1.5L CRDi VGT Diesel', 114, 250, 175, 11.4, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '19.1 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Sonet'), 'HTE 1.2 Petrol MT', '799000', '1.2L Smartstream MPi Petrol', 82, 115, 155, 13.5, 'Manual - 5 Gears', 'Front Wheel Drive', 'Petrol', '18.83 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Sonet'), 'HTX 1.5 Diesel AT', '1310000', '1.5L CRDi VGT Diesel', 114, 250, 170, 11.0, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Diesel', '19.0 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'Sonet'), 'GTX+ 1.0 Turbo DCT', '1455000', '1.0L Smartstream Turbo GDi Petrol', 118, 172, 168, 10.7, 'Automatic (DCT) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.2 km/l', 5, '3 Star (Global NCAP)'),
        (('Kia', 'EV6'), 'GT Performance AWD', '7000000', 'Dual PMSM Motor + 77.4 kWh Battery', 577, 740, 260, 3.5, 'Automatic - 1 Gears, Drift Mode', 'All-Wheel Drive', 'Electric', '546 km', 5, '5 Star (Euro NCAP)'),
        (('Toyota', 'Fortuner'), '2.7 Petrol 4x2 MT', '3343000', '2.7L 2TR-FE 4-Cylinder Petrol Dual VVT-i', 164, 245, 175, 12.0, 'Manual - 5 Gears', 'Rear Wheel Drive', 'Petrol', '10.3 km/l', 7, '5 Star (ANCAP)'),
        (('Toyota', 'Fortuner'), '2.8 Diesel 4x2 AT', '3821000', '2.8L 1GD-FTV Turbo Diesel', 201, 500, 180, 10.2, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Rear Wheel Drive', 'Diesel', '14.4 km/l', 7, '5 Star (ANCAP)'),
        (('Toyota', 'Fortuner'), 'Legender 2.8 4x4 AT', '4764000', '2.8L 1GD-FTV Turbocharged Diesel', 201, 500, 180, 9.8, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Four-Wheel Drive', 'Diesel', '14.2 km/l', 7, '5 Star (ANCAP)'),
        (('Toyota', 'Innova Hycross'), 'GX 2.0 Petrol AT 7-Str', '1977000', '2.0L TNGA 4-Cylinder M20A-FKS Petrol', 172, 209, 170, 10.5, 'Automatic (CVT)', 'Front Wheel Drive', 'Petrol', '16.13 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Innova Hycross'), 'VX Hybrid 8-Str', '2597000', '2.0L TNGA 4-Cylinder Petrol Hybrid (e-Drive)', 184, 206, 170, 9.5, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '23.24 km/l', 8, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Innova Hycross'), 'VX(O) Hybrid 7-Str', '2799000', '2.0L TNGA 4-Cylinder Petrol Hybrid (e-Drive)', 184, 206, 170, 9.5, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '23.24 km/l', 7, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Urban Cruiser Hyryder'), 'S NeoDrive AT', '1388000', '1.5L K15C Mild Hybrid Petrol', 102, 137, 170, 12.5, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '20.58 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Urban Cruiser Hyryder'), 'G Strong Hybrid e-CVT', '1869000', '1.5L TNGA 3-Cylinder Strong Hybrid', 114, 141, 170, 11.2, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '27.97 km/l', 5, '5 Star (Bharat NCAP)'),
        (('Toyota', 'Urban Cruiser Hyryder'), 'V AWD AllGrip MT', '1734000', '1.5L K15C Mild Hybrid Petrol', 102, 137, 168, 12.9, 'Manual - 5 Gears, AllGrip Select AWD', 'All-Wheel Drive', 'Petrol', '19.38 km/l', 5, '5 Star (Bharat NCAP)'),
        (('MG Motor', 'Hector'), 'Shine Pro 1.5 MT', '1600000', '1.5L Turbocharged Petrol', 141, 250, 170, 11.8, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '13.8 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('MG Motor', 'Hector'), 'Select Pro 2.0 Diesel MT', '1870000', '2.0L Multijet II Turbo Diesel', 168, 350, 180, 10.2, 'Manual - 6 Gears', 'Front Wheel Drive', 'Diesel', '15.6 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('MG Motor', 'Hector'), 'Savvy Pro Blackstorm CVT', '2250000', '1.5L Turbocharged Petrol', 141, 250, 170, 11.5, 'Automatic (CVT) - 8-Step Mode', 'Front Wheel Drive', 'Petrol', '13.8 km/l', 5, '5 Star (ASEAN NCAP)'),
        (('MG Motor', 'ZS EV'), 'Excite Executive 50.3 kWh', '1898000', '50.3 kWh Prismatic Battery', 174, 280, 175, 8.5, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '461 km', 5, '5 Star (Euro NCAP)'),
        (('MG Motor', 'ZS EV'), 'Exclusive Plus 50.3 kWh', '2410000', '50.3 kWh Prismatic Battery', 174, 280, 175, 8.5, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '461 km', 5, '5 Star (Euro NCAP)'),
        (('Volkswagen', 'Virtus'), 'Comfortline 1.0 TSI MT', '1156000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 190, 10.4, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '20.8 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Virtus'), 'Highline 1.0 TSI AT', '1488000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 190, 10.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.45 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Virtus'), 'Topline 1.0 TSI AT', '1668000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 190, 10.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.45 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Virtus'), 'GT Edge Limited Edition 1.5 DSG', '1940000', '1.5L TSI EVO Turbo Petrol with ACT', 148, 250, 190, 8.7, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.62 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Taigun'), 'Comfortline 1.0 TSI MT', '1170000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 185, 10.6, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '19.87 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Taigun'), 'Highline 1.0 TSI AT', '1520000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 185, 11.1, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.15 km/l', 5, '5 Star (Global NCAP)'),
        (('Volkswagen', 'Taigun'), 'GT Plus Edge Chrome 1.5 DSG', '1970000', '1.5L TSI EVO Turbo Petrol with ACT', 148, 250, 185, 8.9, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.41 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Slavia'), 'Active 1.0 TSI MT', '1163000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 190, 10.4, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '20.32 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Slavia'), 'Ambition 1.0 TSI AT', '1429000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 190, 10.9, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.73 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Slavia'), 'Monte Carlo 1.5 TSI DSG', '1913000', '1.5L TSI Turbo Petrol with ACT', 148, 250, 190, 8.8, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '19.36 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Kushaq'), 'Active 1.0 TSI MT', '1189000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 185, 10.6, 'Manual - 6 Gears', 'Front Wheel Drive', 'Petrol', '19.76 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Kushaq'), 'Ambition 1.0 TSI AT', '1549000', '1.0L TSI 3-Cylinder Turbo Petrol', 114, 178, 185, 11.1, 'Automatic (TC) - 6 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.09 km/l', 5, '5 Star (Global NCAP)'),
        (('Skoda', 'Kushaq'), 'Monte Carlo 1.5 TSI DSG', '2049000', '1.5L TSI Turbo Petrol with ACT', 148, 250, 185, 8.9, 'Automatic (DSG) - 7 Gears, Paddle Shift', 'Front Wheel Drive', 'Petrol', '18.86 km/l', 5, '5 Star (Global NCAP)'),
        (('Jeep', 'Compass'), 'Sport 2.0 Diesel MT', '2069000', '2.0L Multijet II Turbo Diesel', 168, 350, 190, 10.5, 'Manual - 6 Gears', 'Front Wheel Drive', 'Diesel', '17.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jeep', 'Compass'), 'Longitude 2.0 Diesel AT', '2479000', '2.0L Multijet II Turbo Diesel', 168, 350, 190, 10.2, 'Automatic (TC) - 9 Gears', 'Front Wheel Drive', 'Diesel', '15.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jeep', 'Compass'), 'Night Eagle 2.0 Diesel AT', '2619000', '2.0L Multijet II Turbo Diesel', 168, 350, 190, 10.2, 'Automatic (TC) - 9 Gears', 'Front Wheel Drive', 'Diesel', '15.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jeep', 'Wrangler'), 'Unlimited Sahara 2.0 Turbo AT', '6765000', '2.0L GME T4 Turbocharged Inline-4 Petrol', 268, 400, 160, 8.1, 'Automatic (TC) - 8 Gears, Command-Trac 4x4', 'Four-Wheel Drive', 'Petrol', '11.4 km/l', 5, '4 Star (Euro NCAP)'),
        (('BYD', 'Atto 3'), 'Dynamic 49.92 kWh', '2499000', '49.92 kWh Blade Battery', 201, 310, 160, 7.9, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '468 km', 5, '5 Star (Euro NCAP)'),
        (('BYD', 'Atto 3'), 'Premium 60.48 kWh', '2985000', '60.48 kWh Blade Battery', 201, 310, 160, 7.3, 'Automatic - 1 Gears', 'Front Wheel Drive', 'Electric', '521 km', 5, '5 Star (Euro NCAP)'),
        (('BYD', 'Seal'), 'Dynamic RWD 61.44 kWh', '4100000', '61.44 kWh Blade Battery', 201, 310, 180, 7.5, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '510 km', 5, '5 Star (Euro NCAP)'),
        (('BYD', 'Seal'), 'Premium RWD 82.56 kWh', '4555000', '82.56 kWh Blade Battery', 308, 360, 180, 5.9, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '650 km', 5, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Defender'), '90 SE 2.0 Petrol', '9700000', '2.0L P300 Turbocharged Inline-4 Petrol', 296, 400, 191, 7.1, 'Automatic (TC) - 8 Gears, All-Terrain AWD', 'All-Wheel Drive', 'Petrol', '10.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Defender'), '110 X-Dynamic HSE 3.0 Petrol', '14000000', '3.0L P400 Inline-6 Turbo Petrol MHEV', 395, 550, 191, 6.1, 'Automatic (TC) - 8 Gears, Terrain Response 2', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '9.8 km/l', 7, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Defender'), '130 Outbound 3.0 Diesel', '14600000', '3.0L D300 Inline-6 Twin Turbo Diesel', 296, 650, 191, 7.5, 'Automatic (TC) - 8 Gears, Electronic Air Suspension', 'All-Wheel Drive', 'Diesel', '10.9 km/l', 8, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Range Rover'), 'SE 3.0 Diesel LWB', '27000000', '3.0L D350 Inline-6 Turbocharged Diesel MHEV', 346, 700, 234, 6.3, 'Automatic (TC) - 8 Gears, All-Wheel Steering', 'All-Wheel Drive', 'Mild Hybrid(Electric + Diesel)', '11.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Land Rover', 'Range Rover'), 'SV 4.4 V8 Petrol', '44000000', '4.4L Twin-Turbo V8 Petrol (BMW N63 based)', 523, 750, 261, 4.6, 'Automatic (TC) - 8 Gears, Paddle Shift', 'All-Wheel Drive', 'Petrol', '8.5 km/l', 4, '5 Star (Euro NCAP)'),
        (('Porsche', '911'), 'Carrera Base', '18600000', '3.0L Twin-Turbo Flat-6 Boxer Petrol', 388, 450, 294, 4.0, 'Automatic (PDK) - 8 Gears, Paddle Shift', 'Rear Wheel Drive', 'Petrol', '9.4 km/l', 4, '5 Star (Euro NCAP)'),
        (('Porsche', '911'), 'Carrera 4 GTS', '27500000', '3.6L T-Hybrid Single Turbo Flat-6 Boxer', 534, 610, 312, 3.0, 'Automatic (PDK) - 8 Gears, Launch Control', 'All-Wheel Drive', 'Hybrid (Electric + Petrol)', '9.2 km/l', 4, '5 Star (Euro NCAP)'),
        (('Porsche', '911'), 'GT3 RS', '35000000', '4.0L Naturally Aspirated Flat-6 Boxer', 518, 465, 296, 3.2, 'Automatic (PDK) - 7 Gears, DRS Aero', 'Rear Wheel Drive', 'Petrol', '7.5 km/l', 2, 'Not Tested'),
        (('Porsche', '911'), 'Turbo S', '33500000', '3.8L Twin-Turbo Flat-6 Boxer Petrol', 641, 800, 330, 2.7, 'Automatic (PDK) - 8 Gears, Sport Chrono', 'All-Wheel Drive', 'Petrol', '8.3 km/l', 4, '5 Star (Euro NCAP)'),
        (('Porsche', 'Macan'), 'Macan Base 2.0', '8800000', '2.0L Turbocharged Inline-4 Petrol', 261, 400, 232, 6.2, 'Automatic (PDK) - 7 Gears, Paddle Shift', 'All-Wheel Drive', 'Petrol', '11.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Porsche', 'Macan'), 'Macan GTS', '15300000', '2.9L Twin-Turbo V6 Petrol', 434, 550, 272, 4.3, 'Automatic (PDK) - 7 Gears, Air Suspension', 'All-Wheel Drive', 'Petrol', '9.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Porsche', 'Macan'), 'Macan EV Turbo', '16900000', 'Dual PMSM Motor + 100 kWh Battery', 630, 1130, 260, 3.3, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '591 km', 5, '5 Star (Euro NCAP)'),
        (('Porsche', 'Taycan'), 'Taycan Base RWD', '18900000', 'Rear PMSM Motor + 89 kWh Battery', 402, 410, 230, 4.8, 'Automatic - 2-Speed Rear Transmission', 'Rear Wheel Drive', 'Electric', '590 km', 4, '5 Star (Euro NCAP)'),
        (('Porsche', 'Taycan'), 'Taycan 4S', '21500000', 'Dual PMSM Motor + 105 kWh Battery Plus', 536, 710, 250, 3.7, 'Automatic - 2-Speed Rear Transmission', 'All-Wheel Drive', 'Electric', '642 km', 4, '5 Star (Euro NCAP)'),
        (('Porsche', 'Taycan'), 'Taycan GTS', '24500000', 'Dual PMSM Motor + 93.4 kWh Battery', 590, 850, 250, 3.5, 'Automatic - 2-Speed Rear Transmission', 'All-Wheel Drive', 'Electric', '504 km', 4, '5 Star (Euro NCAP)'),
        (('Lexus', 'RX'), '500h F-Sport Performance', '11800000', '2.4L Turbo Petrol Hybrid + Direct4 eAxle', 366, 460, 210, 6.2, 'Automatic (TC) - 6 Gears, Direct4 AWD', 'All-Wheel Drive', 'Hybrid (Electric + Petrol)', '14.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Lexus', 'ES'), '300h Exquisite', '6315000', '2.5L 4-Cylinder Petrol Hybrid (A25A-FXS)', 215, 221, 180, 8.9, 'Automatic (e-CVT)', 'Front Wheel Drive', 'Hybrid (Electric + Petrol)', '22.58 km/l', 5, '5 Star (Euro NCAP)'),
        (('Ferrari', 'Roma'), 'Spider', '42000000', '3.9L Twin-Turbocharged V8 Petrol', 612, 760, 320, 3.4, 'Automatic (DCT) - 8 Gears, F1 Dual-Clutch', 'Rear Wheel Drive', 'Petrol', '8.6 km/l', 2, 'Not Tested'),
        (('Ferrari', '296 GTB'), '296 GTS Spider', '62400000', '3.0L 120° Twin-Turbo V6 + Electric Motor (PHEV)', 819, 740, 330, 2.9, 'Automatic (DCT) - 8 Gears, Retractable Hard Top', 'Rear Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '13.2 km/l', 2, 'Not Tested'),
        (('Lamborghini', 'Urus'), 'Urus S', '41800000', '4.0L Twin-Turbo V8 Petrol', 657, 850, 305, 3.5, 'Automatic (TC) - 8 Gears, Adaptive Air Suspension', 'All-Wheel Drive', 'Petrol', '7.1 km/l', 5, 'Not Tested'),
        (('Lamborghini', 'Urus'), 'Urus SE Hybrid', '45700000', '4.0L Twin-Turbo V8 + Electric Motor (PHEV)', 789, 950, 312, 3.4, 'Automatic (TC) - 8 Gears, 25.9 kWh Battery', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '12.0 km/l', 5, 'Not Tested'),
        (('BMW', '3 Series'), '330i M Sport', '6920000', '2.0L 4-Cylinder TwinPower Turbo Petrol', 255, 400, 250, 5.8, '8-Speed Steptronic Automatic (Torque Converter)', 'Rear Wheel Drive', 'Petrol', '16.1 km/l', 5, '5 Star (Euro NCAP)'),
        (('BMW', '5 Series'), '520d M Sport', '8990000', '2.0L 4-Cylinder TwinPower Turbo Diesel', 194, 400, 235, 7.3, '8-Speed Steptronic Automatic (Torque Converter)', 'Rear Wheel Drive', 'Diesel', '20.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('BMW', '7 Series'), '735i Pure Excellence', '18500000', '3.0L Inline-6 Turbo Petrol MHEV', 282, 425, 250, 6.7, '8-Speed Steptronic Sport Automatic', 'Rear Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '13.4 km/l', 5, 'Not Tested'),
        (('BMW', 'M4'), 'Competition Convertible xDrive', '19200000', '3.0L Twin-Turbo Inline-6 (S58)', 523, 650, 250, 3.7, '8-Speed M Steptronic with Drivelogic', 'All-Wheel Drive', 'Petrol', '9.8 km/l', 4, '5 Star (Euro NCAP)'),
        (('BMW', 'M2'), 'Manual 3.0 Petrol', '11800000', '3.0L Twin Turbo Inline-6 (S58)', 453, 550, 250, 4.2, '6-Speed Manual Gearbox', 'Rear Wheel Drive', 'Petrol', '9.8 km/l', 4, 'Not Tested'),
        (('BMW', 'X1'), 'sDrive18i xLine', '4950000', '1.5L 3-Cylinder TwinPower Turbo', 134, 230, 208, 9.2, '7-Speed Dual-Clutch Automatic', 'Front Wheel Drive', 'Petrol', '16.35 km/l', 5, '5 Star (Euro NCAP)'),
        (('BMW', 'X3'), 'xDrive30d M Sport', '7990000', '3.0L 6-Cylinder TwinPower Turbo Diesel', 282, 650, 245, 5.8, '8-Speed Steptronic Sport Automatic', 'All-Wheel Drive', 'Diesel', '15.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('BMW', 'X5'), 'xDrive50e M Sport PHEV', '12500000', '3.0L Inline-6 Turbo + Electric Motor (PHEV)', 483, 700, 250, 4.8, '8-Speed Steptronic Automatic, 25.7 kWh Battery', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '42.0 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'A4'), '35 TDI Premium', '4450000', '2.0L TDI Turbo Diesel', 148, 320, 219, 8.7, 'Automatic (DCT) - 7 Gears, S tronic', 'Front Wheel Drive', 'Diesel', '18.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'A4'), '45 TFSI Quattro Technology', '5850000', '2.0L TFSI Turbocharged Petrol', 248, 370, 250, 5.8, 'Automatic (DCT) - 7 Gears, Quattro AWD', 'All Wheel Drive', 'Petrol', '14.5 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'A6'), '40 TDI Premium Plus', '7950000', '2.0L TDI Turbo Diesel', 201, 400, 246, 7.6, 'Automatic (DCT) - 7 Gears, S tronic', 'Front Wheel Drive', 'Diesel', '17.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'A6'), '55 TFSI Quattro Technology', '9850000', '3.0L V6 TFSI Turbocharged Petrol MHEV', 335, 500, 250, 5.1, 'Automatic (DCT) - 7 Gears, Quattro AWD', 'All Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q3'), 'Sportback 40 TFSI Quattro S line', '7250000', '2.0L 4-Cylinder TFSI Petrol', 188, 320, 220, 7.3, 'Automatic (DCT) - 7 Gears, Quattro AWD', 'All Wheel Drive', 'Petrol', '14.93 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q5'), 'Sportback 45 TFSI Quattro S line', '9550000', '2.0L TFSI Turbocharged I4', 261, 370, 240, 6.1, 'Automatic (DCT) - 7 Gears, Quattro AWD', 'All Wheel Drive', 'Petrol', '13.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q7'), 'Bold Edition 55 TFSI Quattro', '12900000', '3.0L TFSI V6 + 48V Mild-Hybrid', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Quattro AWD', 'All Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11.2 km/l', 7, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8'), '55 TFSI Quattro Black Edition', '16800000', '3.0L V6 TFSI Twin-Scroll Turbo Petrol', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Quattro AWD', 'All Wheel Drive', 'Petrol', '9.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'A Class'), 'A 200d Progressive Line', '4800000', '2.0L OM654 Turbo Diesel', 148, 320, 227, 8.2, 'Automatic (DCT) - 8 Gears', 'Front Wheel Drive', 'Diesel', '20.5 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class'), 'C 220d AMG Line', '6250000', '2.0L OM654M Turbo Diesel with ISG', 197, 440, 245, 7.3, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'Rear Wheel Drive', 'Diesel', '17.6 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class'), 'C 300 AMG Line Night Edition', '6900000', '2.0L M254 Turbo Petrol with ISG', 255, 400, 250, 6.0, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'Rear Wheel Drive', 'Petrol', '14.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'E Class'), 'E 200 Exclusive', '7850000', '2.0L M254 Turbo Petrol with ISG', 201, 320, 240, 7.5, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'Rear Wheel Drive', 'Petrol', '14.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'E Class'), 'E 220d AMG Line', '8150000', '2.0L OM654M Turbo Diesel with ISG', 197, 440, 238, 7.4, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'Rear Wheel Drive', 'Diesel', '18.1 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'E Class'), 'E 450 4MATIC AMG Line LWB', '9250000', '3.0L M256 Inline-6 Turbo Petrol MHEV', 375, 500, 250, 4.5, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.0 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'S Class'), 'S 350d', '17700000', '3.0L OM656 Inline-6 Turbo Diesel', 282, 600, 250, 6.4, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'Rear Wheel Drive', 'Diesel', '15.6 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'S Class'), 'S 450 4MATIC', '18600000', '3.0L M256 Inline-6 Turbo Petrol MHEV', 362, 500, 250, 5.1, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.8 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'S Class'), 'Maybach S 580 4MATIC', '27200000', '4.0L V8 Biturbo Petrol with EQ Boost', 496, 700, 250, 4.8, 'Automatic (TC) - 9 Gears 9G-TRONIC', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '9.8 km/l', 4, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'G Class'), 'G 400d AMG Line', '25500000', '2.9L OM656 Inline-6 Turbo Diesel', 326, 700, 210, 6.4, 'Automatic (TC) - 9 Gears 9G-TRONIC, 3 Diff Locks', 'All-Wheel Drive', 'Diesel', '11.2 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC60'), 'B6 AWD Ultimate', '8990000', '2.0L Turbo + Electric Supercharger Petrol MHEV', 295, 420, 180, 6.2, 'Automatic (TC) - 8 Gears Geartronic', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.5 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC90'), 'Recharge T8 Plug-in Hybrid', '14000000', '2.0L Turbo Petrol + Electric Motor (PHEV)', 455, 709, 180, 5.3, 'Automatic (TC) - 8 Gears, 18.8 kWh Battery', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '41.6 km/l', 7, '5 Star (Euro NCAP)')
    ]


    # Strict Foreign Key Crosscheck: Verify Brand and Model combination exists before inserting Variant
    cur.execute("""
        SELECT b.brand_name, m.model_name, m.model_id
        FROM models m
        JOIN brands b ON m.brand_id = b.brand_id
    """)
    valid_models = {(r[0], r[1]): r[2] for r in cur.fetchall()}

    for v in variants:
        brand_name, model_name = v[0]
        variant_name = v[1]

        if (brand_name, model_name) not in valid_models:
            print(f"[DATA INTEGRITY WARNING] Variant skipped: Model '{model_name}' under Brand '{brand_name}' not found in database. Variant '{variant_name}' cannot be inserted.")
            continue

        model_id = valid_models[(brand_name, model_name)]
        try:
            cur.execute("""
                SELECT variant_id FROM variants 
                WHERE model_id = %s AND variant_name = %s LIMIT 1
            """, (model_id, variant_name))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO variants (model_id, variant_name, price_inr, engine, power_bhp, torque_nm,
                                          top_speed_kmh, acceleration_0_100, transmission, drivetrain, fuel_type,
                                          mileage_range, seating_capacity, safety_rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    model_id, variant_name, v[2], v[3], v[4], v[5], v[6], v[7],
                    v[8], v[9], v[10], v[11], v[12], v[13]
                ))
        except Exception as e:
            if "Duplicate entry" not in str(e):
                print(f"[DATA INTEGRITY ERROR] Failed to insert variant '{variant_name}' for '{brand_name} {model_name}': {e}")

    conn.commit()
        # Enrich newly added variants with standard equipment and factory finishes if missing
    cur.execute("""
        SELECT v.variant_id FROM variants v
        LEFT JOIN features f ON v.variant_id = f.variant_id
        WHERE f.feature_id IS NULL
    """)
    unfeatured = [row[0] for row in cur.fetchall()]
    for vid in unfeatured:
        for fcat, fdesc in [
            ("Safety", "Multi-Stage Airbags, ABS with EBD, Electronic Stability Program (ESP), Hill Hold Control, ISOFIX Child Seat Mounts, Tyre Pressure Monitoring"),
            ("Infotainment", "High-Definition Touchscreen, Wireless Apple CarPlay & Android Auto, Connected Car Telematics, Premium Multi-Speaker Acoustic System"),
            ("Comfort", "Multi-Zone Automatic Climate Control, Wireless Smartphone Charger, Cruise Control, Electrically Foldable ORVMs, Keyless Entry & Push-Button Start"),
            ("Performance", "Drive Modes (Eco / Normal / Sport), Adaptive Electric Power Steering, Precision Disc Brakes Front & Rear")
        ]:
            cur.execute("INSERT INTO features (variant_id, feature_category, feature_description) VALUES (%s, %s, %s)", (vid, fcat, fdesc))
        for cname, ctype in [
            ("Onyx Black, Glacier White, Titan Grey, Carbon Metallic", "Exterior"),
            ("Perforated Leatherette / Charcoal Fabric with Contrast Stitching", "Interior")
        ]:
            cur.execute("INSERT INTO colors (variant_id, color_name, color_type) VALUES (%s, %s, %s)", (vid, cname, ctype))
    conn.commit()
    print("✓ All variants inserted successfully!")

    # ===================== Features =====================
    car_features = [
        (('Mercedes-Benz','A Class', 'A200'),'Features','10.25" Digital Instrument Cluster, 10.25" MBUX Touchscreen Infotainment, Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System'),
        (('Mercedes-Benz','A Class', 'A200'),'Interior','Dual Tone (Black with Carbon Fibre Trim, Macchiato Beige / Black with Walnut Wood Trim)'),
        (('Mercedes-Benz','A Class', 'A200'),'Alloy_Wheels','17" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C200'),'Features','12.3" Digital Instrument Cluster, 11.9" MBUX Touchscreen Infotainment,Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System'),
        (('Mercedes-Benz','C Class', 'C200'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C200'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C220d'),'Features','12.3" Digital Instrument Cluster, 11.9" MBUX Touchscreen Infotainment, Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Diesel Optimised Engine Tuning'),
        (('Mercedes-Benz','C Class', 'C220d'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C220d'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C300'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, AMG Performance Seats, Adaptive Suspension, Quad Exhausts, AMG Night Package, Sport Steering, 15-speaker Burmester Audio'),
        (('Mercedes-Benz','C Class', 'C300'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C300'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Features','AMG-specific grille, 11.9-inch MBUX screen, sport seats, Burmester® 3D audio, adaptive suspension, track telemetry, and advanced driver aids.'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Interior','Single Tone (Black with Yellow Contrast and Aluminium Trim)'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Alloy_Wheels','20" AMG Light Alloy Wheels 4 fold 5-Double Spoke'),
        (('Mercedes-Benz','C Class AMG', 'C 63 SE Performance'),'Features','AMG hybrid powertrain with F1-derived tech, performance steering, 11.9-inch MBUX, AMG Track Pace, premium Burmester® audio, adaptive suspension, and driver assist suite.'),
        (('Mercedes-Benz','C Class AMG', 'C 63 SE Performance'),'Interior','Single Tone (Black)'),
        (('Mercedes-Benz','C Class AMG', 'C 63 SE Performance'),'Alloy_Wheels','20" AMG Light Alloy Wheels 4 fold 5-Double Spoke'),
        (('Mercedes-Benz','E Class', 'E200'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor. Premium interiors with 15-speaker Burmester audio, powered memory seats, adaptive cruise, AMG-style accents.'),
        (('Mercedes-Benz','E Class', 'E200'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E200'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Black with High Sheen'),
        (('Mercedes-Benz','E Class', 'E200d'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor. Premium interiors with 16-speaker Burmester audio, powered memory seats, adaptive cruise, AMG-style accents,Diesel Optimised Engine Tuning'),
        (('Mercedes-Benz','E Class', 'E200d'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E200d'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Black with High Sheen'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, enhanced engine, ventilated/heated seats, AMG-style accents, upgraded suspension, Petrol Optimised Enhanced Engine Tuning'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Tantalite Grey'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Features','AMG Night Package, Exterior Chrome Accents, Wheel Options, Sport Styling Package, 12.3" Digital Cluster, 12.8" OLED MBUX Touchscreen, 4-zone Climate, Ambient Lighting with 64 Colours, Reverse Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, Premium Burmester 3D Audio, Ventilated & Heated Seats, AMG-style Accents, Panoramic Sunroof, Executive Rear Seat Package, MBUX AR Navigation.'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Interior','Dual Tone (Sienna Black / Black with High-gloss Black Poplar Wood Trim, Beige / Black with High-gloss Black Poplar Wood Trim)'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Alloy_Wheels','20" AMG multi-spoke alloys'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Features','AMG V8 hybrid with E-Performance boost, Executive rear package, 12.8-inch OLED MBUX, Burmester® 4D surround, AMG ride control+, and comprehensive luxury driver aids.'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Interior','Dual Tone, High-gloss Black Poplar Wood Trim, High-gloss Brown Burr Walnut Wood Trim, MANUFAKTUR Black Piano Lacquer with Flowing Lines, MANUFAKTUR Brown Open-Pore Walnut with Aluminium Lines, AMG Carbon-Fibre/Black Piano Lacquer Trim'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Alloy_Wheels','20-inch AMG 10-spoke light-alloy wheels, 21-inch AMG multi-spoke forged wheels (Silver), 21-inch AMG multi-spoke forged wheels (Black), 21-inch AMG cross-spoke forged wheels'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats,  Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Interior','Dual Tone (Rose gold titanium grey), Star Pattern Trim'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Interior','Dual Tone (Rose Gold/Titanium Grey Pearl), Star Pattern Trim'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Interior','Dual Tone (Rose Gold/Titanium Grey Pearl), Star Pattern Trim'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats,Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Interior','Dual Tone (Black / Balao Brown/Neva Gray / Balao Brown), Brown Open-Pore Magnolia Wood Trim Elements With Mercedes-Benz Pattern In Aluminium'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Alloy_Wheels','20" 5-Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Interior','Dual Tone (Neva Gray/Balao Brown/Macchiato Beige / Space Gray), Trim Elements-Wood Fineline Anthracite'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Alloy_Wheels','21" 5-Spoke Light Alloy AllRound'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Interior','Dual Tone (Neva Gray/Balao Brown/Macchiato Beige / Space Gray)'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Alloy_Wheels','Data Missing'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Features','12.3" Driver Display, 17.7" OLED Infotainment, 12.3" Passenger Display, Rear 11.6" Displays, 7" Rear Tablet, MBUX AR Navigation, Rear Seat Comfort Package with 38° Recline & Massage, 4-Zone Climate, Wireless Phone Charging, Panoramic Sunroof, Ambient Lighting, Premium Burmester Audio.'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Interior','Dual Tone (Neva Grey/ Balao Brown, Macchiato Beige / Space Grey), Trim Elements-Wood Vinterio Walnut'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Alloy_Wheels','LM-Wheel 5-Spoke 20" All Round'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Features','10.25" Digital Display, Wireless Apple CarPlay & Android Auto, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, Panoramic Sunroof'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Interior','Dual Tone (Black, Macchiato Beige / Black with optional Walnut Brown Wood Trim),Progressive/exterior chrome accent pack'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Features','10.25" Digital Display, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, AMG Styling Package, AMG Performance Steering Wheel, AMG Sports Pedals, AMG Floor Mats, AMG Night Package'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Interior','Single Tone (Black with Contrast Red Stitching, optional Light Aluminium Trim), AMG Line exterior'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Alloy_Wheels','19" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLA AMG', '220d AMG Line 4Matic'),'Features','10.25" Digital Display, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, AMG Styling Package, AMG Performance Steering Wheel, AMG Sports Pedals, AMG Floor Mats, AMG Night Package, AMG Performance Exhaust System, AMG Illuminated Door Sills, AMG Sports Seats, AMG Sport Suspension'),
        (('Mercedes-Benz','GLA AMG', '220d AMG Line 4Matic'),'Interior','Single Tone (Black with Contrast Red Stitching, optional Light Aluminium Trim), Full AMG body kit'),
        (('Mercedes-Benz','GLA AMG', '220d AMG Line 4Matic'),'Alloy_Wheels','19" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Features','12.3" Digital Cluster, 10.25" MBUX touchscreen, Dual-zone climate, Ambient lighting; Reverse camera, Keyless Go, LED headlamps, 7 airbags, Active Brake Assist, Hill Start Assist.'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Interior','Dual Tone (Black/ Macchiato Beige and Sienna brown), AMG Line exterior, Night Package, chrome surround options.'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Alloy_Wheels','19" 5-Double Spoke Alloy Wheel'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Features','12.3" Digital Cluster, 11.9"/10.25" MBUX display, Dual-zone climate, Ambient lighting, Reverse camera, Keyless Go, LED headlamps; 9 airbags, Active Brake Assist, ATTENTION ASSIST.'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Interior','Dual Tone (Black/ Macchiato Beige and Sienna brown), Chrome/Gloss exterior packs, roof-rail finish options, AMG Line/Night Pack'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Alloy_Wheels','19" 5-Double Spoke Alloy Wheel'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Features','12.3" digital cluster, 11-12" MBUX touchscreen, Dual-zone/4-zone climate (LWB), Ambient lighting, 360° camera, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist.\nAdaptive cruise, Park Assist, panoramic sunroof, Burmester audio (pack)'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Black), Anthracite Open-Pore Oak Wood Trim Elements, Trim Element- Wood Socket Wrench Bit Tree'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Features','12.3" digital cluster, 10.25-11.9" MBUX, Dual-zone climate, Ambient lighting, Reverse cam, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist.\nHigh torque diesel performance, 360° camera, adaptive cruise, Park Assist; panoramic roof optional.'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Black), Anthracite Open-Pore Oak Wood Trim Elements, Trim Element- Wood Socket Wrench Bit Tree'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Features','12.3" digital cluster, 10.25/11.9" MBUX, Dual-zone climate, Ambient lighting, Reverse cam, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist, ATTENTION ASSIST, Rain-sensing wipers, Hill Start Assist, TPM, Panoramic sunroof, 360° camera, adaptive cruise & ADAS suite; optional Burmester audio'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Black), High-Gloss Brown Linestructure Lime Wood Trim'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, AMG body kit & LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, AMG body kit & LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Features','Dual 12.3" displays (instrument & MBUX), 360° camera, BURMESTER 18-speaker Dolbly Atmos sound; G-Turn (rotate on spot), G-Steering, G-Crawl, adaptive off-road modes, water-wading 850 mm'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Interior','Dual Tone (Nappa leather silver pearl/black), AMG carbon-fibre trim elements, MANUFAKTUR trim in black flamed open-pore ash wood, Metal structure trim element, MANUFAKTUR open-pore grey oak wood trim element, Black piano lacquer trim element, Open-pore natural walnut wood trim element, High-gloss light brown sen wood trim element'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Alloy_Wheels','20" AMG Silver/Black 10-Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','G Class AMG', 'G 63'),'Features','Off-road modes, G-turn, 360° cam, massaging seats, adaptive anti-roll suspension, dual displays, ADAS'),
        (('Mercedes-Benz','G Class AMG', 'G 63'),'Interior','Dual Tone (Macchiato beige/black/Truffle brown/black), Boxy body, ladder frame, optional Collector\'s Edition, Night pack'),
        (('Mercedes-Benz','G Class AMG', 'G 63'),'Alloy_Wheels','20" std, optional 21"/22" AMG'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Features','Widescreen MBUX cockpit, double rear airbags, AIRCAP, AIRSCARF, 360° parking assist, ambient lighting, Burmester 3D audio, elegant open-air luxury'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Interior','Dual Tone (Tonka brown / black/Power red / black), Metal Structure Trim Element'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Alloy_Wheels','19" AMG Multi-Spoke Alloys'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Features', 'Gloss Black R-Dynamic exterior styling pack, Matrix LED headlights w/ DRL, 11.4-inch Pivi Pro infotainment, Meridian Sound System, powered tailgate, 12-way electric front seats w/ heating, adaptive cruise control, 3D surround camera, lane keep assist, dual-zone climate control, keyless entry, ambient lighting'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Interior', 'Single Tone (Black)'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Alloy_Wheels', '19-inch Diamond Turned Finish'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Features', 'Gloss Black R-Dynamic exterior styling pack, Matrix LED headlights w/ DRL, 11.4-inch Pivi Pro infotainment, Meridian Sound System, powered tailgate, 12-way electric front seats w/ heating, adaptive cruise control, 3D surround camera, lane keep assist, dual-zone climate control, keyless entry, ambient lighting'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Interior', 'Single Tone (Black)'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Alloy_Wheels', '19-inch Diamond Turned Finish'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Features', '12.3″ Touchscreen w/ Google Built-in, Wireless CarPlay, Harman Kardon Soundbar, 360° Camera, Pilot Assist ADAS, Adaptive Cruise, Panoramic Roof, OTA Updates, One-Pedal Drive'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Interior', 'Breeze interior,Pine interior,Mist interior'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Alloy_Wheels', '19″ 5-spoke glossy black diamond cut'),
        (('Volvo', 'EX40', 'Plus'), 'Features', '12.3" Touchscreen w/ Google Built-in, Harman Kardon Sound, 360° Camera, Pilot Assist ADAS, Adaptive Cruise, Panoramic Roof, OTA Updates, Wireless CarPlay'),
        (('Volvo', 'EX40', 'Plus'), 'Interior', 'Single Tone (Charcoal)'),
        (('Volvo', 'EX40', 'Plus'), 'Alloy_Wheels', '19"/20" Aero & Diamond Cut'), 
        (('Volvo', 'EC40', 'Ultra'), 'Features', 'Google Built-in 12.3" Display, Harman Kardon Audio, 360° Camera, Pilot Assist ADAS, Panoramic Roof, Ambient Lighting, Wireless CarPlay, OTA updates'),
        (('Volvo', 'EC40', 'Ultra'), 'Interior', 'Dual Tone (Charcoal Insert/Sky Blue Insert)'),
        (('Volvo', 'EC40', 'Ultra'), 'Alloy_Wheels', '19"/20" Aero & Diamond Cut'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Features', 'Google Built-in 9" Touchscreen, 15-speaker Bowers & Wilkins Audio, Panoramic Roof, Pilot Assist ADAS, 360° Camera, Adaptive Cruise, Wireless CarPlay, Ambient Lighting, 4-zone Climate'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Interior', 'Dual Tone (Amber / Charcoal, Maroon Brown / Charcoal)'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Alloy_Wheels', '19" Diamond Cut, optional 20"'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Features', '12.3" Digital Cockpit, 19-speaker Bowers & Wilkins Audio, Panoramic Roof, Pilot Assist ADAS, 360° Camera, Adaptive Cruise, Wireless CarPlay, Four-zone Climate, Soft-close Doors, Hands-free Tailgate'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Interior', 'Dual Tone (Grey Ash / Brown Ash/ Charcoal)'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Alloy_Wheels', '20" Diamond Cut, optional 21"'),
        (('BMW', 'X1', 'sDrive18i M Sport'),'Features', 'LED headlights w/ DRLs, Curved Display (10.25" + 10.7"), Wireless CarPlay & Android Auto, Wireless Charging, iDrive Controller w/ Voice Command, Navigation w/ Rear View Camera, Park Distance Control, 6 Airbags, Dynamic Stability Control, Crash Sensor, Dual-zone climate.'),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Interior', "Veganza Perforated Mocha/Veganza Perforated Oyster, Interior trim finishers Aluminium ‘Mesheffect’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Alloy_Wheels', '18" M light alloy wheels Double-spoke style 838 M Bicolour'),
        (('BMW', 'X1', 'sDrive18d M Sport'),'Features', 'LED headlights w/ DRLs, Curved Display (10.25" + 10.7"), Wireless CarPlay & Android Auto, Wireless Charging, iDrive Controller w/ Voice Command, Navigation w/ Rear View Camera, Park Distance Control, 6 Airbags, Dynamic Stability Control, Crash Sensor, Dual-zone climate.'),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Interior', "Veganza Perforated Mocha/Veganza Perforated Oyster, Interior trim finishers Aluminium ‘Mesheffect’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Alloy_Wheels', '18" M light alloy wheels Double-spoke style 838 M Bicolour'),
        (('BMW', 'X3', 'xDrive20i M Sport'),'Features', 'Parking Assistant, Reversing Assistant, 360° Camera, Wireless Apple CarPlay & Android Auto, Harman Kardon Surround Sound System, BMW Curved Display (12.3" Instrument + 14.9" Control Display), Panoramic Glass Sunroof, 6 Airbags, Tyre Pressure Indicator, Driving Assistant, Cruise Control with Braking Function'),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Interior', "Veganza Perforated Espresso Brown, Veganza Perforated Calm Beige, Interior trim finishers Aluminium ‘Rhombicle’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Alloy_Wheels', '19" M Light Alloy Wheels Y-Spoke Bicolour'),
        (('BMW', 'X3', 'xDrive20d M Sport'),'Features', 'Parking Assistant, Reversing Assistant, 360° Camera, Wireless Apple CarPlay & Android Auto, Harman Kardon Surround Sound System, BMW Curved Display (12.3" Instrument + 14.9" Control Display), Panoramic Glass Sunroof, 6 Airbags, Tyre Pressure Indicator, Driving Assistant, Cruise Control with Braking Function'),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Interior', "Veganza Perforated Espresso Brown, Veganza Perforated Calm Beige, Interior trim finishers Aluminium ‘Rhombicle’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Alloy_Wheels', '19" M Light Alloy Wheels Y-Spoke Bicolour'),
        (('BMW', 'X5', 'xDrive40i'),'Features', '360° Camera w/ Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Wireless CarPlay & Android Auto, Harman Kardon Sound, Panoramic Sunroof, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate, Electric Seats w/ Memory, Comfort Access, Welcome Light.'),
        (('BMW', 'X5', 'xDrive40i'), 'Interior', "Sensafin Decor Stitching / Cognac, Fine-Wood Trim 'Fineline Stripe' Brown High-Gloss"),
        (('BMW', 'X5', 'xDrive40i'), 'Alloy_Wheels', '21" Light Alloy Wheels Y-Spoke Style 744 Bicolour'),
        (('BMW', 'X5', 'xDrive30d'),'Features', '360° Camera w/ Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Wireless CarPlay & Android Auto, Harman Kardon Sound, Panoramic Sunroof, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate, Electric Seats w/ Memory, Comfort Access, Welcome Light.'),
        (('BMW', 'X5', 'xDrive30d'), 'Interior', "Sensafin Decor Stitching / Cognac, Fine-Wood Trim 'Fineline Stripe' Brown High-Gloss"),
        (('BMW', 'X5', 'xDrive30d'), 'Alloy_Wheels', '21" Light Alloy Wheels Y-Spoke Style 744 Bicolour'),
        (('BMW', 'X7', 'xDrive40i M Sport'),'Features', '360° Camera, Curved Display (12.3" + 14.9"), Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Air Suspension, Gesture Control, Laserlight, Comfort Seats w/ Memory, Welcome Light, Comfort Access, Rear Seat Entertainment, 5-Zone Climate, Soft-Close Doors, Sky Lounge Glass Roof, Heated & Ventilated Seats, Rear Comfort Package, Remote Functions via My BMW App.'),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Interior', "Individual Extended Leather Trim Merino | Tartufo, Fine-Wood Trim 'Fineline' Black With Metal Effect High-Gloss"),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Alloy_Wheels', '21" Inches M Light Alloy Wheels Double-Spoke Style 754 M Bicolour Orbit Grey, Gloss-Lathed'),
        (('BMW', 'X7', 'xDrive40d M Sport'),'Features', '360° Camera, Curved Display (12.3" + 14.9"), Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Air Suspension, Gesture Control, Laserlight, Comfort Seats w/ Memory, Welcome Light, Comfort Access, Rear Seat Entertainment, 5-Zone Climate, Soft-Close Doors, Sky Lounge Glass Roof, Heated & Ventilated Seats, Rear Comfort Package, Remote Functions via My BMW App.'),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Interior', "Individual Extended Leather Trim Merino | Tartufo, Fine-Wood Trim 'Fineline' Black With Metal Effect High-Gloss"),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Alloy_Wheels', '21" Inches M Light Alloy Wheels Double-Spoke Style 754 M Bicolour Orbit Grey, Gloss-Lathed'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'),'Features', 'Crystal LED headlights, Curved Display (12.3" + 14.9"), Sky Lounge Panoramic Roof, Ambient Air Package, Rear Alcantara Cushions, Rear Captain Seats, Harman Kardon 16-Speaker Sound, Heads-Up Display, Ambient Light Bar, Comfort Access, Remote via My BMW App.'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Interior', "BMW Individual Extended Leather Trim Merino | Tartufo', Fine-wood trim 'Fineline Stripe' brown high gloss"),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Alloy_Wheels', '53.4 cm (21") DPE light alloy wheels Y-spoke style 753 bicolour (9.5J x 21 with 285/45 R21 tyres)'),
        (('BMW', 'XM', 'Plug-in Hybrid'),'Features', '360° Camera, BMW Curved Display (12.3" + 14.9"), Bowers & Wilkins Diamond Surround Sound, Adaptive Cruise Control, M Adaptive Suspension, BMW Laserlight, Electric Comfort Seats w/ Massage & Memory, M Lounge Rear Seats, 4-Zone Climate Control, Soft-Close Doors, Heated & Ventilated Seats, Gesture Control, Ambient Lighting, Remote Functions via My BMW App'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Interior', 'Dual Tone (Deep Lagoon / Walknappa Vintage Coffee , Silverstone / Walknappa Vintage Coffee, Sakhir Orange / Walknappa Vintage Coffee , Black / Walknappa Vintage Coffee), M-specific trims'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Alloy_Wheels', '21" / 22" / 23" M Light-Alloy (optional)'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'),'Features', '360° Camera, BMW Curved Display (10.25" + 10.7"), Harman Kardon Sound, Driving Assistant Plus (Lane Keep, Blind Spot, Cross Traffic Alert), Adaptive Cruise Control, Electric Seats w/ Memory, 6 Airbags, Tyre Pressure Monitor, Ambient Lighting, Dual-Zone Climate, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Interior', 'Veganza Perforated Mocha, Interior trim finishers Aluminium Hexacube'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Alloy_Wheels', 'M Sport 18-inch alloy wheels'),
        (('BMW', 'iX', 'xDrive 50'),'Features', 'Adaptive air suspension with Dynamic Handling, premium Harman Kardon surround sound, BMW Intelligent Personal Assistant, gesture control, optional 5G connectivity, extended ambient lighting with customizable themes'),
        (('BMW', 'iX', 'xDrive 50'), 'Interior', 'Dual Tone (Interior design Suite Leather Castanea), M-specific trims'),
        (('BMW', 'iX', 'xDrive 50'), 'Alloy_Wheels', '21" or 22" multi-spoke alloy wheels'),
        (('BMW', '2 Series', '218 M Sport'),'Features', '360° Camera with Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Harman Kardon Sound, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate Control, Electric Seats with Memory, Comfort Access, Welcome Light'),
        (('BMW', '2 Series', '218 M Sport'), 'Interior', 'Veganza Perforated Mocha, Veganza Perforated Oyster, Interior Decors Illuminated Aluminium Graphite'),
        (('BMW', '2 Series', '218 M Sport'), 'Alloy_Wheels', '18" M Law Y-Spoke 975M Bicolour'),
        (('BMW', '2 Series', '218 M Sport Pro'),'Features', '360° Camera with Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Harman Kardon Sound, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate Control, Electric Seats with Memory, Comfort Access, Welcome Light'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Interior', 'Veganza Perforated Mocha, Veganza Perforated Oyster, M Illuminated Decor Hexacube Matte'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Alloy_Wheels', '18" M Law Y-Spoke 975M Bicolour'),
        (('BMW', 'M2', '3.0 Petrol'),'Features', 'BMW Curved Display (12.3-inch instrument cluster + 14.9-inch control display), iDrive 8.5, Harman Kardon Surround Sound System, M Sport Seats, Adaptive M Suspension, M Traction Control, Gear Shift Assistant, Matrix LED Headlights, 3-Zone Climate Control, Ambient Lighting, Lane Departure Warning, Blind Spot Monitoring, Rear Cross Traffic Alert, Parking Assistant, M Drift Analyzer'),
        (('BMW', 'M2', '3.0 Petrol'), 'Interior', "Leather 'Vernasca' Black/Exclusive Highlight, Leather 'Vernasca' Black/Contrast Stitching, Lthr Vernasca Black/Accent Red, Interior Trim Finishers 'Aluminum Rhombicle’, Interior Trim Finishers 'Carbon Fibre'"),
        (('BMW', 'M2', '3.0 Petrol'), 'Alloy_Wheels', '19"/ 20" M Light Alloy Wheels Double-Spoke Style 930 M Jet Black With Mixed Tyres, 19"/ 20" M Light Alloy Wheels Double-Spoke Style 930 M Bicolour With Mixed Tyres, 19"/20" M Law Do.Sp. 930M Silver'),
        (('BMW', '3 Series LWB', '330 Li M Sport'),'Features', 'Curved Display (14.9" + 12.3"), Panoramic Sunroof, 3-Zone Climate Control, Ambient Lighting, Driving Assistant (ADAS), Park Assistant Plus w/ Surround View, Comfort Access, Remote 3D View via My BMW App'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Interior', 'Leather Vernasca Cognac Decor Stitching, M Aerodynamics Package with satin aluminium accents, Pearl Chrome grille slats'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Alloy_Wheels', '18" Light Alloy Wheels 848 M Double Spoke'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'),'Features', 'Curved Display (14.9" + 12.3"), Panoramic Sunroof, 3-Zone Climate Control, Ambient Lighting, Driving Assistant (ADAS), Park Assistant Plus w/ Surround View, Comfort Access, Remote 3D View via My BMW App'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Interior', 'Leather Vernasca Cognac Decor Stitching, M Aerodynamics Package with satin aluminium accents, Pearl Chrome grille slats'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Alloy_Wheels', '18" Light Alloy Wheels 848 M Double Spoke'),
        # --- BMW High-End Models ---
        (('BMW', '3 Series', 'M340i'), 'Features', '14.9" Curved Display, M Sport Differential, M Sport Brakes, Adaptive M Suspension, Harman Kardon Sound, Wireless CarPlay, Ambient Lighting, 6 Airbags'),
        (('BMW', '3 Series', 'M340i'), 'Interior', 'Dual Tone (Alcantara / Sensatec Black with Blue Contrast Stitching)'),
        (('BMW', '3 Series', 'M340i'), 'Alloy_Wheels', '18" M Light Alloy Wheels 790 M Bicolour'),
        (('BMW', 'M4', 'Competition'), 'Features', 'M Curved Display, M Drive Professional with Drift Analyser, M Carbon Bucket Seats, Adaptive M Suspension, Harman Kardon Sound, Head-Up Display'),
        (('BMW', 'M4', 'Competition'), 'Interior', 'Dual Tone (Black / Yas Marina Blue Full Merino Leather)'),
        (('BMW', 'M4', 'Competition'), 'Alloy_Wheels', '19"/20" M Forged Wheels Double-Spoke 826 M'),
        (('BMW', 'M4', 'CS'), 'Features', 'M Carbon ceramic brakes, Lightweight Carbon bonnet & roof, Titanium rear silencer, M Drive Professional with 10-stage traction control'),
        (('BMW', 'M4', 'CS'), 'Interior', 'Dual Tone (Anthracite Alcantara / Merino Black with Mugello Red accents)'),
        (('BMW', 'M4', 'CS'), 'Alloy_Wheels', '19"/20" M Light Alloy Wheels Star-spoke style 827 M in Bronze Gold'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Features', '14.9" Curved Touchscreen, BMW Live Cockpit Plus, Ambient Lighting, Reversing Assistant, Harman Kardon Surround Audio, Glass Sunroof, 6 Airbags'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Interior', 'Dual Tone (Perforated Sensatec Tacora Red / Black)'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Alloy_Wheels', '18" M Aerodynamic Wheels 858 M Bicolour'),
        (('BMW', '5 Series', '530Li M Sport'), 'Features', 'BMW Interaction Bar with Ambient Lighting, 14.9" Curved Display, Bowers & Wilkins Surround Sound, Panoramic Glass Roof, Driving Assistant, Parking Assistant Plus'),
        (('BMW', '5 Series', '530Li M Sport'), 'Interior', 'Dual Tone (Veganza Perforated Copper Brown / Atlas Grey)'),
        (('BMW', '5 Series', '530Li M Sport'), 'Alloy_Wheels', '19" M Light Alloy Wheels Double-Spoke 935 M'),
        (('BMW', 'M5', 'Competition'), 'Features', 'M Hybrid Drive System, Curved Display, Bowers & Wilkins Diamond Surround Sound, M Carbon Ceramic Brakes, Active M Differential, 4-Zone Climate'),
        (('BMW', 'M5', 'Competition'), 'Interior', 'Dual Tone (Merino Full Leather Silverstone / Black with Carbon Trim)'),
        (('BMW', 'M5', 'Competition'), 'Alloy_Wheels', '20"/21" M Double-Spoke 951 M Bicolour'),
        (('BMW', 'i5', 'M60 xDrive'), 'Features', 'Adaptive M Suspension Professional, BMW Interaction Bar, Bowers & Wilkins Sound, Active Roll Stabilization, M Sport Brakes with Red Calipers, Panoramic Roof'),
        (('BMW', 'i5', 'M60 xDrive'), 'Interior', 'Dual Tone (Black / Smoke White Veganza with Carbon Inlays)'),
        (('BMW', 'i5', 'M60 xDrive'), 'Alloy_Wheels', '20" M Aerodynamic Wheels 940 M Bicolour Jet Black'),
        (('BMW', '7 Series', '740i M Sport'), 'Features', '31.3" 8K BMW Theatre Screen in Rear, Interaction Bar, Bowers & Wilkins Diamond 4D Sound, Sky Lounge Panoramic Glass Roof, Executive Lounge Seating, Automatic Doors'),
        (('BMW', '7 Series', '740i M Sport'), 'Interior', 'Dual Tone (BMW Individual Merino Leather Amarone / Black with Open-Pore Oak Wood Trim)'),
        (('BMW', '7 Series', '740i M Sport'), 'Alloy_Wheels', '20" M Aerodynamic Wheels 907 M Bicolour'),
        (('BMW', '7 Series', '740d M Sport'), 'Features', '31.3" 8K BMW Theatre Screen in Rear, Interaction Bar, Bowers & Wilkins Diamond 4D Sound, Sky Lounge Panoramic Glass Roof, Executive Lounge Seating, Automatic Doors'),
        (('BMW', '7 Series', '740d M Sport'), 'Interior', 'Dual Tone (BMW Individual Merino Leather Amarone / Black with Open-Pore Oak Wood Trim)'),
        (('BMW', '7 Series', '740d M Sport'), 'Alloy_Wheels', '20" M Aerodynamic Wheels 907 M Bicolour'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Features', '31.3" 8K BMW Theatre Screen, Executive Lounge Rear Console, Bowers & Wilkins 4D Diamond Audio, Adaptive Air Suspension, Integral Active Steering, Level 2 ADAS'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Interior', 'Dual Tone (BMW Individual Leather Merino Tartufo / Black)'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Alloy_Wheels', '21" M Aerodynamic Wheels 908 M Bicolour'),
        (('BMW', 'i7', 'M70 xDrive'), 'Features', 'Dual electric motors, M sport boost, 31.3" 8K Theatre Screen, Executive Lounge seating, Bowers & Wilkins Diamond 4D Audio, Executive Drive Pro air suspension'),
        (('BMW', 'i7', 'M70 xDrive'), 'Interior', 'Dual Tone (BMW Individual Merino Leather Smoke White / Black with Carbon Fibre Trim)'),
        (('BMW', 'i7', 'M70 xDrive'), 'Alloy_Wheels', '21" M Light Alloy Wheels Star-spoke style 908 M Jet Black'),
        (('BMW', 'M8', 'Competition Coupé'), 'Features', 'M Setup with Track Mode, M Carbon Ceramic Brakes, Bowers & Wilkins Diamond Surround Sound, Driving Assistant Professional, M Carbon Roof, 360° Camera'),
        (('BMW', 'M8', 'Competition Coupé'), 'Interior', 'Dual Tone (Full Merino Leather Sakhir Orange / Black)'),
        (('BMW', 'M8', 'Competition Coupé'), 'Alloy_Wheels', '20" M Star-Spoke 813 M Bicolour'),
        (('BMW', 'Z4', 'M40i'), 'Features', 'M Sport Differential, Adaptive M Suspension, BMW Live Cockpit Professional, Harman Kardon Sound, Electrically Operated Softtop, Wind Deflector, M Sport Brakes'),
        (('BMW', 'Z4', 'M40i'), 'Interior', 'Dual Tone (Leather Vernasca Cognac with Contrast Stitching)'),
        (('BMW', 'Z4', 'M40i'), 'Alloy_Wheels', '19" M Light Alloy Wheels Double-Spoke 799 M Bicolour'),

        # --- Audi Models ---
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Features', '10.1" MMI Touch Infotainment, Audi Virtual Cockpit Plus, 3-Zone Deluxe Climate Control, Audi Sound System, Sunroof, 8 Airbags, Audi Drive Select'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Interior', 'Dual Tone (Okapi Brown / Black Leatherette with Piano Black Inlays)'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Alloy_Wheels', '17" 5-Arm Dynamic Style Alloy Wheels'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Features', '10.1" MMI Touchscreen, Audi Virtual Cockpit Plus, Ambient Lighting Package Plus, Sunroof, Audi Drive Select, Wireless Phone Charger'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Interior', 'Dual Tone (Atlas Beige / Black Leatherette with Aluminum Ellipse Inlays)'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Alloy_Wheels', '17" 5-Arm Dynamic Style Alloy Wheels'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Features', '10.1" MMI Navigation Plus, Bang & Olufsen 3D Sound (19 speakers), Audi Virtual Cockpit Plus, Comfort Keyless Entry, Park Assist, Matrix LED Headlamps'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Interior', 'Dual Tone (Okapi Brown / Black with Natural Gray Oak Wood Inlays)'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Alloy_Wheels', '17" 5-Spoke V-Style Alloy Wheels'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Features', 'Dual MMI Touchscreens (10.1" + 8.6"), Audi Virtual Cockpit Plus, Matrix LED Headlights, Audi Sound System, Panoramic Sunroof, 4-Zone Climate'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Interior', 'Dual Tone (Mother-of-Pearl Beige / Black with Walnut Brown Inlays)'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Alloy_Wheels', '18" 5-Arm Design Alloy Wheels'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Features', 'Dual MMI Touchscreens, Audi Virtual Cockpit Plus, Bang & Olufsen Premium 3D Sound, Panoramic Sunroof, 4-Zone Climate, Audi Wireless Phone Box'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Interior', 'Dual Tone (Mother-of-Pearl Beige / Black with Aluminum Fragment Inlays)'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Alloy_Wheels', '18" 5-Arm Multi-Spoke Alloy Wheels'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Features', 'HD Matrix LED Headlights with Dynamic Indicators, Bang & Olufsen Premium 3D Sound, Park Assist Plus with 360° Cameras, Audi Virtual Cockpit Plus, 4-Zone AC'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Interior', 'Dual Tone (Valcona Okapi Brown / Black Leather with Fine Grain Birch Wood Trim)'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Alloy_Wheels', '18" 5-Arm Star Design Alloy Wheels'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Features', '10.1" MMI Touch Display, Audi Virtual Cockpit Plus, Panoramic Glass Sunroof, 2-Zone Climate, Audi Sound System, 6 Airbags, Quattro All-Wheel Drive'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Interior', 'Dual Tone (Okapi Brown / Black with Aluminium Dimension Inlays)'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Alloy_Wheels', '18" 5-Arm Style Alloy Wheels'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Features', '10.1" MMI Navigation Plus, Audi Virtual Cockpit Plus, Audi Sound System (10 speakers), Gesture-controlled Electric Tailgate, Wireless Charging'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Interior', 'Dual Tone (Okapi Brown / Black Leather with Matte Brushed Aluminium Trim)'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Alloy_Wheels', '18" 5-Arm V-Style Alloy Wheels'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Features', '10.1" MMI Touch Screen, Audi Virtual Cockpit Plus, Panoramic Sunroof, 3-Zone Climate, Audi Drive Select with Offroad mode, 8 Airbags'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Interior', 'Dual Tone (Cricket Leather Beige / Black with Micrometallic Silver Inlays)'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Alloy_Wheels', '19" 5-Arm Pylon Design Alloys'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Features', 'Bang & Olufsen 3D Sound System (19 speakers), Matrix LED Headlamps, Comfort Key with Sensor-controlled Tailgate, Adaptive Suspension with Damping Control'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Interior', 'Dual Tone (Okapi Brown / Black Leather with Inlays in Walnut Brown)'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Alloy_Wheels', '19" 5-Double-Spoke Dynamic Contrast Grey Alloys'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Features', 'Dual Central Displays (10.1" + 8.6"), Audi Virtual Cockpit Plus, Matrix LED Headlights, Audi Sound System, Adaptive Air Suspension, 4-Zone Climate Control, 8 Airbags'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Saiga Beige / Black with Gray Oak High-Gloss Inlays)'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Alloy_Wheels', '19" 5-Arm Star Design Alloy Wheels'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Features', 'Bang & Olufsen 3D Premium Sound, Matrix LED with Audi Laser Light, Adaptive Air Suspension, Power-assisted Door Closure, 360° Surround Cameras'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Cricket Leather Cedar Brown / Black with Eucalyptus Natural Wood Inlays)'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Alloy_Wheels', '19" 5-Arm V-Spoke Design Alloys'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Features', 'Frameless Doors, Dual Touchscreens, HD Matrix LED Headlamps, B&O 3D Sound, Adaptive Air Suspension, Valcona Leather Seats with Massage, 8 Airbags'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Pando Gray / Black with Fine Grain Ash Wood Trim)'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Alloy_Wheels', '21" 5-Segment Spoke Design Alloy Wheels'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Features', 'Twin-turbo V8, RS Adaptive Air Suspension Sport, All-wheel Steering, Ceramic Brakes, Bang & Olufsen Advanced 3D Sound System (23 speakers)'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Interior', 'Dual Tone (Valcona Leather Black with Express Red Honeycomb Stitching)'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Alloy_Wheels', '23" 5-Y-Spoke Rotor Design Cast Alloys'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Features', 'Audi Virtual Cockpit Plus with Sport Display, B&O 3D Sound, S Sport Suspension with Damper Control, Matrix LED Headlamps with Audi Laser Light, Panoramic Sunroof'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Interior', 'Dual Tone (Magma Red / Black Fine Nappa Leather with Carbon Atlas Inlays)'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Alloy_Wheels', '19" 5-Double-Arm S-Design Alloys'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Features', 'Dual MMI Screens, Virtual Mirrors, Adaptive Air Suspension, Bang & Olufsen 3D Sound, Panoramic Sunroof, Matrix LED Headlamps, 8 Airbags'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Interior', 'Dual Tone (Pearl Beige / Black Valcona Leather)'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Alloy_Wheels', '20" 5-Arm Dynamic Aero Alloys'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Features', '114 kWh high-capacity battery, Adaptive Air Suspension, B&O 3D Sound, Digital Matrix LED Headlights, Head-up Display, 4-Zone AC'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Interior', 'Dual Tone (Okapi Brown / Black Valcona Leather with Volcano Gray Inlays)'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Alloy_Wheels', '20" 5-Arm Aero Style Contrast Gray Alloys'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Features', 'Coupe SUV aerodynamic silhouette, Dual MMI Touchscreens, Adaptive Air Suspension, Audi Pre-Sense Front, 360° Cameras'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Interior', 'Dual Tone (Pearl Beige / Black Leatherette with Aluminium Inlays)'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Alloy_Wheels', '20" 5-Arm Aero Contrast Gray Alloys'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Features', '114 kWh battery, Digital Matrix LED with projection functions, B&O 3D Audio, Panoramic Glass Sunroof, Soft-close doors'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Interior', 'Dual Tone (Black / Rotor Gray with Orange Contrast Stitching)'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Alloy_Wheels', '21" Aero Structure Black Diamond Turned Alloys'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Features', '800-Volt Architecture, Electric Quattro with Torque Vectoring, Matrix LED with Audi Laser Light, Bang & Olufsen 3D Sound, Adaptive 3-Chamber Air Suspension, Carbon Roof'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Interior', 'Dual Tone (Black Leather-Free Interior with Express Red Honeycomb Stitching)'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Alloy_Wheels', '21" 5-Twin-Spoke Concept Car Aerodynamic Alloys'),

        # --- Indian Market Additions Features ---
        # Ford
        (('Ford', 'Endeavour', 'Titanium+ 2.0 4x4 AT'), 'Features', '8.0" SYNC 3 Touchscreen, Panoramic Sunroof, Semi-Autonomous Parallel Park Assist, Terrain Management System, 7 Airbags, Hands-free Tailgate, Dual-zone Climate Control, Active Noise Cancellation'),
        (('Ford', 'Endeavour', 'Titanium+ 2.0 4x4 AT'), 'Interior', 'Dual Tone (Ebony Black / Cognac Brown Leather)'),
        (('Ford', 'Endeavour', 'Titanium+ 2.0 4x4 AT'), 'Alloy_Wheels', '18" Diamond Cut 6-Spoke Alloy Wheels'),
        (('Ford', 'Mustang', 'GT V8'), 'Features', '12" Digital LCD Cluster, 8" SYNC 3 Touchscreen, B&O 12-Speaker Audio, Track Apps with Line Lock & Launch Control, 8 Airbags, Active Exhaust Modes, Selectable Drive Modes'),
        (('Ford', 'Mustang', 'GT V8'), 'Interior', 'Single Tone (Ebony Black Leather with Contrast Stitching)'),
        (('Ford', 'Mustang', 'GT V8'), 'Alloy_Wheels', '19" Ebony Black Painted Aluminum Wheels'),

        # Mahindra
        (('Mahindra', 'XUV700', 'AX7 Diesel AT Luxury Pack AWD'), 'Features', 'Dual 10.25" Superscreen (Infotainment + Cluster), AdrenoX AI Connected Car Tech, Level 2 ADAS Suite, Sony 3D 12-Speaker Sound, Skyroof Panoramic Glass, Wireless Android Auto & Apple CarPlay, 7 Airbags, 360° Surround View'),
        (('Mahindra', 'XUV700', 'AX7 Diesel AT Luxury Pack AWD'), 'Interior', 'Dual Tone (Ivory & Dark Blue Nappa Leatherette)'),
        (('Mahindra', 'XUV700', 'AX7 Diesel AT Luxury Pack AWD'), 'Alloy_Wheels', '18" Diamond Cut Multi-Spoke Alloys'),
        (('Mahindra', 'Scorpio-N', 'Z8L Diesel 4x4 AT'), 'Features', '8.0" Touchscreen with AdrenoX Connect, Sony 12-Speaker 3D Audio, Dual-Zone Climate Control, 4XPLOR Intelligent Terrain Mode, Electric Sunroof, Wireless Phone Charger, 6 Airbags, Driver Drowsiness Detection'),
        (('Mahindra', 'Scorpio-N', 'Z8L Diesel 4x4 AT'), 'Interior', 'Dual Tone (Coffee Black & Rich Leatherette)'),
        (('Mahindra', 'Scorpio-N', 'Z8L Diesel 4x4 AT'), 'Alloy_Wheels', '18" Diamond Cut Machined Alloy Wheels'),
        (('Mahindra', 'Thar', 'LX 4-Str Hard Top Diesel AT 4WD'), 'Features', '7.0" Touchscreen Infotainment with Adventure Statistics, Drizzle Resistant Controls, Roof Mounted Speakers, Electric Shift-on-Fly 4WD Transfer Case, ESP with Rollover Mitigation, Rear Parking Sensors'),
        (('Mahindra', 'Thar', 'LX 4-Str Hard Top Diesel AT 4WD'), 'Interior', 'Single Tone (Sporty Black Water-Resistant Dashboard)'),
        (('Mahindra', 'Thar', 'LX 4-Str Hard Top Diesel AT 4WD'), 'Alloy_Wheels', '18" Deep Silver Alloy Wheels with All-Terrain Tyres'),

        # Hyundai
        (('Hyundai', 'Creta', 'SX (O) 1.5 Diesel AT'), 'Features', 'Seamless 10.25" Dual Curved Screens, Bose Premium 8-Speaker Audio, Level 2 ADAS with 19 Safety Features, Voice Controlled Panoramic Sunroof, Front Ventilated Seats, 360° Camera, 6 Airbags standard, Bluelink Connected Tech'),
        (('Hyundai', 'Creta', 'SX (O) 1.5 Diesel AT'), 'Interior', 'Dual Tone (Grey & Dark Chrome with Honeycomb Emboss)'),
        (('Hyundai', 'Creta', 'SX (O) 1.5 Diesel AT'), 'Alloy_Wheels', '17" Diamond Cut Aerodynamic Alloy Wheels'),
        (('Hyundai', 'Venue', 'SX (O) 1.0 Turbo DCT'), 'Features', '8.0" HD Infotainment, 2-Step Rear Reclining Seats, Electric Sunroof, Ambient Lighting, 6 Airbags standard, Drive Modes (Eco, Normal, Sport), Bluelink Over-The-Air Updates, Paddle Shifters'),
        (('Hyundai', 'Venue', 'SX (O) 1.0 Turbo DCT'), 'Interior', 'Dual Tone (Black & Greige Fabric/Leatherette Combination)'),
        (('Hyundai', 'Venue', 'SX (O) 1.0 Turbo DCT'), 'Alloy_Wheels', '16" Diamond Cut Sport Alloy Wheels'),
        (('Hyundai', 'Verna', 'SX (O) 1.5 Turbo DCT'), 'Features', 'Dual 10.25" Integrated Screen Setup, Heated & Ventilated Front Seats, Bose 8-Speaker Audio, 64-Color Ambient Light linked to drive modes, Level 2 ADAS Suite, Smart Electric Trunk, 6 Airbags'),
        (('Hyundai', 'Verna', 'SX (O) 1.5 Turbo DCT'), 'Interior', 'Dual Tone (Black & Soft Beige with Piano Red Accents)'),
        (('Hyundai', 'Verna', 'SX (O) 1.5 Turbo DCT'), 'Alloy_Wheels', '16" Satin Black Diamond Cut Alloy Wheels'),
        (('Hyundai', 'Bayon', '1.5 NA MT'), 'Features', '10.25" Digital Cluster, 10.25" Infotainment Display, Hyundai SmartSense ADAS Suite, Wireless Phone Charging, Bose Sound System, LED Ambient Lighting, Automatic Air Conditioning'),
        (('Hyundai', 'Bayon', '1.5 NA MT'), 'Interior', 'Single Tone (Black with Subtle Turquoise Stitching)'),
        (('Hyundai', 'Bayon', '1.5 NA MT'), 'Alloy_Wheels', '16" Turbine-Style Alloy Wheels'),

        # Honda
        (('Honda', 'City', 'ZX CVT'), 'Features', '8.0" Touchscreen Infotainment, Honda SENSING Level 2 ADAS Suite, LaneWatch Camera, One-Touch Electric Sunroof, 8-Speaker Sound, Walk Away Auto Lock, 6 Airbags, Remote Engine Start'),
        (('Honda', 'City', 'ZX CVT'), 'Interior', 'Dual Tone (Premium Beige & Black with Piano Black Accents)'),
        (('Honda', 'City', 'ZX CVT'), 'Alloy_Wheels', '16" Multi-Spoke Two-Tone Diamond Cut Alloys'),
        (('Honda', 'Elevate', 'ZX CVT'), 'Features', '10.25" Advanced HD Touchscreen, Honda SENSING Suite, LaneWatch Blind-Spot Monitor, Wireless Apple CarPlay/Android Auto, Electric Sunroof, Automatic Climate Control, 6 Airbags, 458L Boot'),
        (('Honda', 'Elevate', 'ZX CVT'), 'Interior', 'Dual Tone (Rich Mocha Brown Leatherette & Black)'),
        (('Honda', 'Elevate', 'ZX CVT'), 'Alloy_Wheels', '17" Dual-Tone Diamond Cut Multi-Spoke Alloys'),

        # Maruti Suzuki
        (('Maruti Suzuki', 'Swift', 'ZXi Plus AMT'), 'Features', '9.0" SmartPlay Pro+ Touchscreen, Arkamys Surround Sense Audio, Wireless Phone Charger, Cruise Control, 6 Airbags standard, LED Projector Headlamps with DRLs, Rear AC Vents, Suzuki Connect'),
        (('Maruti Suzuki', 'Swift', 'ZXi Plus AMT'), 'Interior', 'Dual Tone (Black and Off-White Satin Chrome Trim)'),
        (('Maruti Suzuki', 'Swift', 'ZXi Plus AMT'), 'Alloy_Wheels', '15" Precision Cut Two-Tone Alloy Wheels'),
        (('Maruti Suzuki', 'Brezza', 'ZXi Plus AT'), 'Features', '9.0" SmartPlay Pro+ Touchscreen, 360° View Camera, Head-Up Display (HUD), Electric Sunroof, Arkamys Audio, Wireless Charging, 6 Airbags, Paddle Shifters, Rear AC Vents'),
        (('Maruti Suzuki', 'Brezza', 'ZXi Plus AT'), 'Interior', 'Dual Tone (Black & Rich Brown with Silver Accents)'),
        (('Maruti Suzuki', 'Brezza', 'ZXi Plus AT'), 'Alloy_Wheels', '16" Geometric Dual-Tone Alloy Wheels'),
        (('Maruti Suzuki', 'Grand Vitara', 'Alpha+ Strong Hybrid e-CVT'), 'Features', 'Panoramic Sunroof, 9.0" SmartPlay Pro+ Display, Head-Up Display, 360° Surround Camera, Ventilated Front Seats, EV Mode Drive Switch, Qi Wireless Charger, 6 Airbags, Suzuki Connect'),
        (('Maruti Suzuki', 'Grand Vitara', 'Alpha+ Strong Hybrid e-CVT'), 'Interior', 'Dual Tone (Bordeaux Faux Leather & Black with Champagne Gold Trim)'),
        (('Maruti Suzuki', 'Grand Vitara', 'Alpha+ Strong Hybrid e-CVT'), 'Alloy_Wheels', '17" Precision Cut Multi-Spoke Alloy Wheels'),

        # Tata Motors
        (('Tata Motors', 'Nexon', 'Fearless Plus S 1.2 DCA'), 'Features', '10.25" Floating Infotainment, 10.25" Full Digital Instrument Cluster with Nav View, JBL 9-Speaker Cinematic Sound, 360° HD Camera, Ventilated Seats, Voice-assisted Panoramic Sunroof, 6 Airbags standard'),
        (('Tata Motors', 'Nexon', 'Fearless Plus S 1.2 DCA'), 'Interior', 'Dual Tone (Benecke-Kaliko Tri-tone with Royal Blue / Slate Grey Trim)'),
        (('Tata Motors', 'Nexon', 'Fearless Plus S 1.2 DCA'), 'Alloy_Wheels', '16" Aero Disc Diamond Cut Alloy Wheels'),
        (('Tata Motors', 'Harrier', 'Fearless+ Dark Edition AT'), 'Features', '12.3" Cinemax Touchscreen, 10.25" Digital Cluster, Level 2 ADAS with 11 Functions, JBL 10-Speaker Audio with Subwoofer, 360° Surround Camera, Panoramic Sunroof with Mood Lighting, Dual-Zone Fully Automatic AC, 7 Airbags'),
        (('Tata Motors', 'Harrier', 'Fearless+ Dark Edition AT'), 'Interior', 'Single Tone (#DARK Oberon Black Nappa Leather with Piano Black Inlays)'),
        (('Tata Motors', 'Harrier', 'Fearless+ Dark Edition AT'), 'Alloy_Wheels', '19" Spider-Spoke R19 Diamond Cut Satin Alloys'),
        (('Tata Motors', 'Safari', 'Accomplished+ Dark Edition AT'), 'Features', '12.3" Harman Touchscreen, Memory & Ventilated Front Seats + Ventilated Rear Captain Seats, Level 2 ADAS Suite, JBL 10-Speaker Audio, Gesture Controlled Powered Tailgate, Ambient Light Bar, 7 Airbags'),
        (('Tata Motors', 'Safari', 'Accomplished+ Dark Edition AT'), 'Interior', 'Single Tone (#DARK Theme Black Leatherette with Signature Embroidery)'),
        (('Tata Motors', 'Safari', 'Accomplished+ Dark Edition AT'), 'Alloy_Wheels', '19" Satin Black Spider Alloy Wheels'),
        (('Tata Motors', 'Punch', 'Creative AMT'), 'Features', '7.0" Harman Touchscreen, 7.0" TFT Digital Instrument Cluster, Auto Headlamps & Rain Sensing Wipers, Cruise Control, Electric Sunroof, Cooled Glovebox, Dual Airbags with 5-Star Safety'),
        (('Tata Motors', 'Punch', 'Creative AMT'), 'Interior', 'Dual Tone (Off-White & Granite Black with Tri-Arrow Motif)'),
        (('Tata Motors', 'Punch', 'Creative AMT'), 'Alloy_Wheels', '16" Diamond Cut Two-Tone Alloy Wheels'),
        (('Tata Motors', 'Sierra', 'EV Empowered AWD'), 'Features', 'Lounge Seating Experience, Continuous Glass Canopy Roof, Dual 12.3" Panoramic Displays, Level 2+ Autonomous Driving, V2L & V2V Bi-directional Charging, Connected Car 2.0, 7 Airbags'),
        (('Tata Motors', 'Sierra', 'EV Empowered AWD'), 'Interior', 'Dual Tone (Oatmeal Fabric & Moss Wood Eco Leatherette)'),
        (('Tata Motors', 'Sierra', 'EV Empowered AWD'), 'Alloy_Wheels', '19" Aerodynamic Optimized EV Alloy Wheels'),
        (('Tata Motors', 'Curvv', 'Creative 1.5 Diesel AT'), 'Features', '12.3" Floating Touchscreen, Level 2 ADAS Suite, Voice Assisted Panoramic Sunroof with Mood Light, Gesture Powered Tailgate, Ventilated Seats, 9-Speaker JBL Sound, 360° Camera, 6 Airbags'),
        (('Tata Motors', 'Curvv', 'Creative 1.5 Diesel AT'), 'Interior', 'Dual Tone (Burgundy Leatherette & Obsidian Black Inlays)'),
        (('Tata Motors', 'Curvv', 'Creative 1.5 Diesel AT'), 'Alloy_Wheels', '18" Machined Two-Tone Alloy Wheels'),
        (('Tata Motors', 'Aeris', 'Smart EV'), 'Features', '10.25" Touchscreen, ZConnect Connected App Suite, Multi-Mode Regenerative Braking, Smart Auto AC, Reverse Camera with Guidelines, ESP with Hill Hold, 6 Airbags'),
        (('Tata Motors', 'Aeris', 'Smart EV'), 'Interior', 'Dual Tone (Frost White & Dark Ocean Blue Accents)'),
        (('Tata Motors', 'Aeris', 'Smart EV'), 'Alloy_Wheels', '16" Aerodynamic Energy-Saving Alloy Wheels'),

        # Kia
        (('Kia', 'Seltos', 'X-Line 1.5 Diesel AT'), 'Features', 'Dual 10.25" Panoramic Screen Display, Level 2 ADAS with 17 Autonomous Features, Dual-Zone Fully Automatic AC, Bose Premium 8-Speaker Audio, Panoramic Dual-Pane Sunroof, 360° Camera with Blind View Monitor, 6 Airbags'),
        (('Kia', 'Seltos', 'X-Line 1.5 Diesel AT'), 'Interior', 'Single Tone (Exclusive X-Line Sage Green Leatherette with Orange Stitching)'),
        (('Kia', 'Seltos', 'X-Line 1.5 Diesel AT'), 'Alloy_Wheels', '18" Gloss Black Crystal Cut Alloy Wheels'),
        (('Kia', 'Sonet', 'X-Line 1.0 Turbo DCT'), 'Features', '10.25" HD Touchscreen + 10.25" Digital Cluster, Level 1 ADAS (10 features), Bose 7-Speaker Premium Sound with LED Sound Mood Lights, 360° Camera, Ventilated Front Seats, Sunroof, 6 Airbags standard'),
        (('Kia', 'Sonet', 'X-Line 1.0 Turbo DCT'), 'Interior', 'Single Tone (Exclusive X-Line Sage Green & Carbon Fiber Trim)'),
        (('Kia', 'Sonet', 'X-Line 1.0 Turbo DCT'), 'Alloy_Wheels', '16" Crystal Cut Glossy Black Alloy Wheels'),
        (('Kia', 'EV6', 'GT-Line AWD'), 'Features', 'Dual 12.3" Curved Displays, Meridian 14-Speaker Audio, Augmented Reality Head-Up Display (AR-HUD), Ultra-Fast 800V Multi-Charging (10-80% in 18 min), Level 2 ADAS Suite, V2L Power Supply, 8 Airbags'),
        (('Kia', 'EV6', 'GT-Line AWD'), 'Interior', 'Dual Tone (Black Suede & Vegan Leather with Neon Accents)'),
        (('Kia', 'EV6', 'GT-Line AWD'), 'Alloy_Wheels', '19" Aerodynamic Alloy Wheels with Diamond Finish'),

        # Toyota
        (('Toyota', 'Fortuner', 'GR-S 2.8 Diesel 4x4 AT'), 'Features', '8.0" Touchscreen with Android Auto & Apple CarPlay, JBL 11-Speaker Audio with Subwoofer, GR-S Sport-Tuned Suspension, Auto Limited Slip Differential (Auto LSD), 360° Camera, Dual Zone AC, 7 Airbags, GR Badging'),
        (('Toyota', 'Fortuner', 'GR-S 2.8 Diesel 4x4 AT'), 'Interior', 'Single Tone (Sport Black Leather with GR Red Stitching and Suede Inserts)'),
        (('Toyota', 'Fortuner', 'GR-S 2.8 Diesel 4x4 AT'), 'Alloy_Wheels', '18" GR-S All-Black Machined Alloy Wheels'),
        (('Toyota', 'Innova Hycross', 'ZX(O) Hybrid'), 'Features', '10.1" Touchscreen Infotainment, Toyota Safety Sense (ADAS Level 2), Powered Ottoman Captain Seats with Leg Support, Panoramic Sunroof with Mood Lighting, 9-Speaker JBL Audio, 360° Camera, 6 Airbags'),
        (('Toyota', 'Innova Hycross', 'ZX(O) Hybrid'), 'Interior', 'Dual Tone (Dark Chestnut & Black Leather with Silver Accents)'),
        (('Toyota', 'Innova Hycross', 'ZX(O) Hybrid'), 'Alloy_Wheels', '18" Super Chrome Multi-Spoke Metallic Alloys'),
        (('Toyota', 'Urban Cruiser Hyryder', 'V Hybrid'), 'Features', 'Panoramic Sunroof, 9.0" Smart Playcast Audio, Head-Up Display, 360° View Camera, Ventilated Front Seats, Wireless Phone Charging, EV Drive Mode, 6 Airbags, Drive Mode Select'),
        (('Toyota', 'Urban Cruiser Hyryder', 'V Hybrid'), 'Interior', 'Dual Tone (Rich Black & Bordeaux Leatherette with Brushed Silver Inlays)'),
        (('Toyota', 'Urban Cruiser Hyryder', 'V Hybrid'), 'Alloy_Wheels', '17" Dual-Tone Precision Cut Alloy Wheels'),

        # MG Motor
        (('MG Motor', 'Hector', 'Savvy Pro 1.5 CVT'), 'Features', 'Segment Largest 14.0" HD Portrait Infotainment Screen, Level 2 ADAS (11 features) including Traffic Jam Assist, Infinity 8-Speaker Sound with Subwoofer, Dual-Pane Panoramic Sunroof, 360° View HD Camera, 6 Airbags'),
        (('MG Motor', 'Hector', 'Savvy Pro 1.5 CVT'), 'Interior', 'Dual Tone (Argil Brown & Lush Black with Wood Pattern Accents)'),
        (('MG Motor', 'Hector', 'Savvy Pro 1.5 CVT'), 'Alloy_Wheels', '18" Dual-Tone Machined Alloy Wheels'),
        (('MG Motor', 'ZS EV', 'Exclusive Pro'), 'Features', '10.1" HD Infotainment Screen, Level 2 ADAS Suite, Dual-Pane Panoramic Skyroof, 360° Camera with Transparent Chassis, i-SMART 75+ Connected Features, PM 2.5 Air Filter, 6 Airbags, Wireless Charging'),
        (('MG Motor', 'ZS EV', 'Exclusive Pro'), 'Interior', 'Single Tone (Dark Luxe Leatherette with Contrast Grey Stitching)'),
        (('MG Motor', 'ZS EV', 'Exclusive Pro'), 'Alloy_Wheels', '17" Tomahawk Diamond Cut Aerodynamic Alloy Wheels'),

        # Volkswagen
        (('Volkswagen', 'Virtus', 'GT Plus 1.5 TSI DSG'), 'Features', '10.1" VW Play Touchscreen, 8.0" Digital Cockpit, Active Cylinder Technology (ACT), 8-Speaker Sound, Ventilated Front Seats, Wireless App-Connect, Electric Sunroof, 6 Airbags standard, ESC, Hill Hold Control'),
        (('Volkswagen', 'Virtus', 'GT Plus 1.5 TSI DSG'), 'Interior', 'Dual Tone (Titan Black & Ceramic Leatherette with Red Ambient Illumination)'),
        (('Volkswagen', 'Virtus', 'GT Plus 1.5 TSI DSG'), 'Alloy_Wheels', '16" Razor Diamond Cut Gloss Black Alloys with Red Calipers'),
        (('Volkswagen', 'Taigun', 'GT Plus 1.5 TSI DSG'), 'Features', '10.1" VW Play Infotainment, 8.0" Digital Virtual Cockpit, Active Cylinder Technology (ACT), Electric Sunroof, Wireless Charging, 6 Airbags standard, Ventilated Front Seats, ESC, Multi-Collision Brakes'),
        (('Volkswagen', 'Taigun', 'GT Plus 1.5 TSI DSG'), 'Interior', 'Dual Tone (Titan Black & Grey Faux Leather with Carbon Fiber Texture)'),
        (('Volkswagen', 'Taigun', 'GT Plus 1.5 TSI DSG'), 'Alloy_Wheels', '17" Manila Gloss Black Alloy Wheels with Red Brake Calipers'),

        # Skoda
        (('Skoda', 'Slavia', 'Style 1.5 TSI DSG'), 'Features', '10.0" Skoda Infotainment System, 8.0" Digital Virtual Cockpit, Active Cylinder Deactivation (ACT), Subwoofer & 8 Speakers, Ventilated Leather Seats, Electric Sunroof, 6 Airbags standard, Electronic Differential Lock'),
        (('Skoda', 'Slavia', 'Style 1.5 TSI DSG'), 'Interior', 'Dual Tone (Black & Soft Beige with Piano Black Slat Deco)'),
        (('Skoda', 'Slavia', 'Style 1.5 TSI DSG'), 'Alloy_Wheels', '16" Ving Machined Two-Tone Alloy Wheels'),
        (('Skoda', 'Kushaq', 'Style 1.5 TSI DSG'), 'Features', '10.0" Skoda Touchscreen with Wireless SmartLink, 8.0" Digital Cluster, Subwoofer Sound System, Electric Sunroof, Ventilated Front Seats, 6 Airbags standard, Ambient Lighting, Tyre Pressure Monitoring'),
        (('Skoda', 'Kushaq', 'Style 1.5 TSI DSG'), 'Interior', 'Dual Tone (Black & Grey Perforated Leather with Brushed Chrome Accents)'),
        (('Skoda', 'Kushaq', 'Style 1.5 TSI DSG'), 'Alloy_Wheels', '17" Atlas Two-Tone Machined Alloy Wheels'),

        # Jeep
        (('Jeep', 'Compass', 'Model S 4x4 Diesel AT'), 'Features', '10.1" Uconnect 5 Touchscreen, 10.25" Frameless Digital Cluster, 360° Surround Camera, Alpine 9-Speaker Audio with Subwoofer, Dual-Pane Panoramic Sunroof, Selec-Terrain 4x4 Modes, Powered Tailgate, 6 Airbags'),
        (('Jeep', 'Compass', 'Model S 4x4 Diesel AT'), 'Interior', 'Single Tone (Imperial Black Leather with Tungsten Accent Stitching)'),
        (('Jeep', 'Compass', 'Model S 4x4 Diesel AT'), 'Alloy_Wheels', '18" Gloss Grey Diamond Cut Alloy Wheels'),
        (('Jeep', 'Wrangler', 'Rubicon'), 'Features', '12.3" Uconnect 5 Touchscreen with Off-Road Pages, Rock-Trac 4x4 with 4:1 Low Ratio & Tru-Lok Locking Differentials, Electronic Front Sway-Bar Disconnect, Removable Freedom Top Doors/Roof, Alpine 9-Speaker Sound'),
        (('Jeep', 'Wrangler', 'Rubicon'), 'Interior', 'Single Tone (Black Nappa Leather with Rubicon Red Stitching)'),
        (('Jeep', 'Wrangler', 'Rubicon'), 'Alloy_Wheels', '17" Machined Face with Black Pockets & 33" BFGoodrich KO2 Tyres'),

        # BYD
        (('BYD', 'Atto 3', 'Extended Range'), 'Features', '12.8" Rotating Intelligent Touchscreen, Level 2 ADAS Suite, Panoramic Sunroof with Anti-Pinch, DiLink 4.0 Connected System, 360° Holographic Transparent Camera, Dirac 8-Speaker Audio, VTOL Mobile Power Station, 7 Airbags'),
        (('BYD', 'Atto 3', 'Extended Range'), 'Interior', 'Dual Tone (Eclipse Blue & Synth Leather White with Red Strings)'),
        (('BYD', 'Atto 3', 'Extended Range'), 'Alloy_Wheels', '18" Windmill Dynamic Aerodynamic Alloy Wheels'),
        (('BYD', 'Seal', 'Performance AWD'), 'Features', '15.6" Rotating Multimedia Screen, Cell-to-Body (CTB) Battery Architecture, Dynaudio 12-Speaker Sound, Head-Up Display, Frequency Selective Damping (FSD), Level 2 ADAS Suite, Panoramic Canopy, 9 Airbags'),
        (('BYD', 'Seal', 'Performance AWD'), 'Interior', 'Dual Tone (Thaumas Black & Mist White Nappa Leather)'),
        (('BYD', 'Seal', 'Performance AWD'), 'Alloy_Wheels', '19" Precision Machined Dual-Tone Blade Alloys'),

        # Land Rover
        (('Land Rover', 'Range Rover', 'Autobiography 3.0 LWB'), 'Features', '13.1" Curved Pivi Pro Touchscreen, 13.7" Interactive Driver Display, Meridian Signature 35-Speaker 1600W Sound with Active Noise Cancellation, Electronic Air Suspension with Dynamic Response Pro, All-Wheel Steering, Executive Class Comfort Plus Rear Seats, Digital LED Headlamps with Image Projection, 3D Surround Camera'),
        (('Land Rover', 'Range Rover', 'Autobiography 3.0 LWB'), 'Interior', 'Dual Tone (Caraway & Perlino Semi-Aniline Leather with Natural Black Birch Veneer)'),
        (('Land Rover', 'Range Rover', 'Autobiography 3.0 LWB'), 'Alloy_Wheels', '22" 10-Spoke Gloss Dark Grey Diamond Turned Alloys'),
        (('Land Rover', 'Defender', '110 HSE 3.0 Diesel'), 'Features', '11.4" Pivi Pro Screen, ClearSight Ground View & Rear Camera Mirror, Electronic Air Suspension with Adaptive Dynamics, Meridian 14-Speaker Sound, Terrain Response 2 with Configurable Modes, 3D Surround Camera, Matrix LED Headlights, Wade Sensing up to 900mm'),
        (('Land Rover', 'Defender', '110 HSE 3.0 Diesel'), 'Interior', 'Dual Tone (Ebony Windsor Leather & Robustec with Light Oyster Headlining)'),
        (('Land Rover', 'Defender', '110 HSE 3.0 Diesel'), 'Alloy_Wheels', '20" Style 5098 5-Spoke Gloss Sparkle Silver Alloys'),

        # Porsche
        (('Porsche', '911', 'Carrera S'), 'Features', 'Porsche Communication Management (PCM) 10.9" Display, 8-Speaker Sound Package Plus, Porsche Active Suspension Management (PASM), Sport Chrono Package with Mode Switch, Launch Control, Dynamic Engine Mounts, Porsche Torque Vectoring Plus (PTV Plus), Matrix LED Headlights'),
        (('Porsche', '911', 'Carrera S'), 'Interior', 'Dual Tone (Black & Bordeaux Red Full Leather with Carbon Fiber Trim)'),
        (('Porsche', '911', 'Carrera S'), 'Alloy_Wheels', '20"/21" Carrera Classic Forged Alloy Wheels'),
        (('Porsche', 'Macan', 'Macan S'), 'Features', '10.9" Full HD Touchscreen PCM, Sport Chrono Package, Porsche Active Suspension Management (PASM), BOSE Surround Sound System (14 speakers), Panoramic Roof System, Multi-Function GT Sports Steering, ParkAssist with Surround View, Power 14-Way Comfort Seats'),
        (('Porsche', 'Macan', 'Macan S'), 'Interior', 'Dual Tone (Black & Mojave Beige Extended Leather Package)'),
        (('Porsche', 'Macan', 'Macan S'), 'Alloy_Wheels', '20" Macan S Wheels in Dark Titanium'),
        (('Porsche', 'Taycan', 'Turbo S'), 'Features', 'Curved 16.8" Driver Cockpit Display, 10.9" Central PCM + Optional Passenger Display, Porsche 4D Chassis Control, Adaptive Air Suspension with Smart Lift, Burmester 3D High-End Surround Sound, Performance Battery Plus 800-Volt Architecture, Electric Sport Sound, Ceramic Composite Brakes (PCCB)'),
        (('Porsche', 'Taycan', 'Turbo S'), 'Interior', 'Dual Tone (Black & Chalk Olea Club Leather with Dark Matt Neodyme Trim)'),
        (('Porsche', 'Taycan', 'Turbo S'), 'Alloy_Wheels', '21" Mission E Design Forged Aerodynamic Wheels'),

        # Lexus
        (('Lexus', 'RX', '350h Luxury'), 'Features', '14.0" Touchscreen Display with Lexus Interface, Mark Levinson 21-Speaker Premium Surround Sound, Lexus Safety System+ 3.0 (ADAS), Head-Up Display, E-Latch Electronic Door Release, Panoramic Glass Roof, 360° Panoramic View Monitor, Adaptive Variable Suspension'),
        (('Lexus', 'RX', '350h Luxury'), 'Interior', 'Dual Tone (Saddle Tan & Black Semi-Aniline Leather with Medium Brown Bamboo Trim)'),
        (('Lexus', 'RX', '350h Luxury'), 'Alloy_Wheels', '21" 20-Spoke Metallic Dark Grey Premium Alloys'),
        (('Lexus', 'ES', '300h Luxury'), 'Features', '12.3" Touchscreen Multimedia Display, Mark Levinson 17-Speaker PurePlay Audio, Power Reclining Rear Seats with Center Armrest Controls, Hands-Free Kick Sensor Tailgate, Bi-LED Triple Beam Headlamps, 10 Airbags, Blind Spot Monitor'),
        (('Lexus', 'ES', '300h Luxury'), 'Interior', 'Dual Tone (Hazel & Black Smooth Leather with Shimamoku Wood Trim)'),
        (('Lexus', 'ES', '300h Luxury'), 'Alloy_Wheels', '18" Multi-Spoke Noise-Reducing Alloy Wheels'),

        # Ferrari
        (('Ferrari', 'Roma', 'Coupe'), 'Features', '16.0" Curved Digital Instrument Cluster, 8.4" Central Display, 8.8" Passenger Display, F1-Trac Traction Control, Side Slip Control (SSC 6.0), Dynamic Enhancer (FDE), Matrix LED Headlights, Carbon Ceramic Brakes (CCM3), Dual-zone Climate, Advanced ADAS Pack'),
        (('Ferrari', 'Roma', 'Coupe'), 'Interior', 'Dual Tone (Cuoio Leather & Charcoal Alcantara with Carbon Fiber Driver Zone)'),
        (('Ferrari', 'Roma', 'Coupe'), 'Alloy_Wheels', '20" Forged Grigio Corsa Diamond-Cut Wheels'),
        (('Ferrari', '296 GTB', 'Coupe'), 'Features', 'Digital Cockpit with HMI Capacitive Touch Steering, Head-Up Display, 6-way Chassis Dynamic Sensor (6w-CDS), ABS Evo Brake-by-Wire, eManettino with 4 driving modes (eDrive, Hybrid, Performance, Qualify), Titanium Exhaust Pipes, Carbon Ceramic Brakes'),
        (('Ferrari', '296 GTB', 'Coupe'), 'Interior', 'Dual Tone (Nero Leather & Rosso Corsa Accents with Carbon Racing Seats)'),
        (('Ferrari', '296 GTB', 'Coupe'), 'Alloy_Wheels', '20" Forged Diamond-Polished Lightweight Wheels'),

        # Lamborghini
        (('Lamborghini', 'Urus', 'Performante'), 'Features', 'Lamborghini Infotainment System III with Dual Touchscreens, Bang & Olufsen 3D Advanced Sound (21 speakers), ANIMA Drive Selector with RALLY Mode, Akrapovic Titanium Exhaust, Carbon-Fiber Bonnet & Roof, Carbon Ceramic Brakes (CCB), Adaptive Air Suspension'),
        (('Lamborghini', 'Urus', 'Performante'), 'Interior', 'Dual Tone (Nero Cosmus Alcantara & Giallo Taurus Accents with Dark Chrome Trim)'),
        (('Lamborghini', 'Urus', 'Performante'), 'Alloy_Wheels', '22" Pelope Shiny Black Lightweight Alloys with Titanium Bolts'),
        (('Lamborghini', 'Revuelto', 'Coupe'), 'Features', '12.3" Instrument Cluster, 8.4" Central Display, 9.1" Passenger Display, Carbon-Fiber Monofuselage Chassis, 13 Drive Modes including Citta, Strada, Sport, Corsa, Torque Vectoring via front e-axle, Carbon Ceramic Brakes Plus (CCB Plus), Matrix LED Lights'),
        (('Lamborghini', 'Revuelto', 'Coupe'), 'Interior', 'Dual Tone (Nero Ade & Arancio Apodis Leather/Dinamica Corsa Package)'),
        (('Lamborghini', 'Revuelto', 'Coupe'), 'Alloy_Wheels', '21" Front / 22" Rear Altanero Forged Shiny Black Alloy Wheels')
    ]

    # Strict Foreign Key Crosscheck: Verify Variant exists before inserting Features
    cur.execute("""
        SELECT b.brand_name, m.model_name, v.variant_name, v.variant_id
        FROM variants v
        JOIN models m ON v.model_id = m.model_id
        JOIN brands b ON m.brand_id = b.brand_id
    """)
    valid_variants = {(r[0], r[1], r[2]): r[3] for r in cur.fetchall()}

    for item in car_features:
        brand, model, variant_name = item[0]
        cat, desc = item[1], item[2]

        if (brand, model, variant_name) not in valid_variants:
            print(f"[DATA INTEGRITY WARNING] Feature skipped: Variant '{variant_name}' for '{brand} {model}' not found in database.")
            continue

        variant_id = valid_variants[(brand, model, variant_name)]
        try:
            cur.execute("SELECT feature_id FROM features WHERE variant_id = %s AND feature_category = %s LIMIT 1", (variant_id, cat))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO features (variant_id, feature_category, feature_description)
                    VALUES (%s, %s, %s)
                """, (variant_id, cat, desc))
        except Exception as e:
            if "Duplicate entry" not in str(e):
                print(f"[DATA INTEGRITY ERROR] Error inserting feature for '{brand} {model} {variant_name}': {e}")

    conn.commit()
    print("✓ All Features inserted successfully!")


    # ===================== Colors =====================
    car_colors = [
        (('Mercedes-Benz','A Class', 'A200'), 'Cosmos Black, Mountain Grey,Polar White,Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C200'), 'Obsidian Black, Mojave Silver,Selenite Grey,Sodalite Blue, Opalith White, Hi-Tech Silver', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C220d'), 'Obsidian Black, Mojave Silver,Selenite Grey,Sodalite Blue, Opalith White, Hi-Tech Silver', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C300'), 'Obsidian Black,Sodalite Blue, Patagonia red bright, Opalith White', 'Metallic'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'), 'Polar White, Selenite Grey Metallic, Sodalite Blue Metallic, Hi Tech Silver, Spectral Blue,  Graphite Grey, Opalite White Bright, Patagonia Red Bright, Graphite Grey Magno', 'Metallic'),
        (('Mercedes-Benz','C Class AMG', 'C 63 SE Performance'), 'Polar White, Selenite Grey Metallic, Sodalite Blue Metallic, Hi Tech Silver, Spectral Blue,  Graphite Grey, Opalith white metallic, Patagonia red metallic bright, Graphite Grey Magno', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E200'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E200d'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'), 'Diamond White Bright,Onyx Black, Nautic Blue, High Tech Silver', 'Metallic'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'), 'Black, Nautic blue, Salenite Grey, High-Tech Silver, Emerald Green, Obsidian black, Graphite Grey, Verde Silver,Velvet Brown, Opalite White Bright, Rubellite Red Metallic, Kalahari Gold Metallic, Graphite Grey Magno, Opalite White Magno', 'Metallic'),
        (('Mercedes-Benz','EQA', '250 Plus'), 'Polar White,High Tech Silver, Patagonia red, Mountain Grey, Spectral Blue, Cosmos Black', 'Metallic'),
        (('Mercedes-Benz','EQB', '250 Plus'), 'Cosmos Black, Rose Gold, Digital White, Mountain Grey, Iridium Silver', 'Metallic'),
        (('Mercedes-Benz','EQB', '350 4Matic'), 'Cosmos Black, Rose Gold, Digital White, Mountain Grey, Iridium Silver', 'Metallic'),
        (('Mercedes-Benz','EQE', '500 4Matic'), 'Obsidian Black Metallic, Sodalite Blue Metallic, Emerald Green Metallic, Velvet Brown Metallic, High-Tech Silver Metallic, Selenite Grey Metallic, Polar White, Alpine Grey, Diamond White', 'Metallic'),
        (('Mercedes-Benz','EQS', '450 5 Seater'), 'Black Lacquer, Sodalite Blue, Velvet Brown, Polar White, Obsidian Black, Opalite White Bright Metallic, Alpine Grey, Emerald Green', 'Metallic'),
        (('Mercedes-Benz','EQS', '580 4Matic'), 'Black Lacquer, Sodalite Blue, Selenite Grey Metallic, Velvet Brown, Polar White, Obsidian Black, High-Tech Silver, Opalite White Bright Metallic, Alpine Grey, Emerald Green', 'Metallic'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'), 'Obsidian Black,Graphite Grey', 'Metallic'),
        (('Mercedes-Benz','GLA', 'GLA200'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLA', '220d 4Matic'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLA AMG', '220d AMG Line 4Matic'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLC', '200d 4Matic'), 'Nautic Blue, Mojave Silver, Graphite Grey, Polar White, Obsidian Black', 'Metallic'),
        (('Mercedes-Benz','GLC', '300 4Matic'), 'Nautic Blue, Mojave Silver, Graphite Grey, Polar White, Obsidian Black', 'Metallic'),
        (('Mercedes-Benz','GLE', '450 4MATIC'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLS', '450 4MATIC'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'), 'Obsidian Black, Opalite White Bright, Classic Grey, Opalite White Magno, South Seas Blue Magno', 'Metallic'),
        (('Mercedes-Benz','G Class AMG', 'G 63'), 'Classic G shades + Manufaktur options', 'Metallic'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'), 'Obsidian Black, Graphite Grey, Hi-Tech Silver, Spectral Blue', 'Metallic'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Fuji White, Santorini Black, Firenze Red, Eiger Grey, Portofino Blue', 'Solid'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Fuji White, Santorini Black, Firenze Red, Eiger Grey, Portofino Blue', 'Solid'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Cloud Blue,Crystal White,Onyx Black,Vapour Grey,Sand Dune', 'Metallic'),
        (('Volvo', 'EX40', 'Plus'), 'Crystal White,Fjord Blue, Onyx Black, Sage Green, Cloud Blue', 'Metallic'),
        (('Volvo', 'EC40', 'Ultra'), 'Crystal White,Fjord Blue, Onyx Black, Sage Green, Cloud Blue,Fusion Red', 'Metallic'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Onyx Black, Crystal White, Denim Blue, Fusion Red, Bright Dusk', 'Metallic'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Onyx Black, Denim Blue, Crystal White, Bright Dusk, Mulberry Red, Vapour Grey', 'Metallic'),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Alpine White (Non-Metallic)/Black Sapphire (Metallic)/M Portimao Blue (Metallic)/Space Silver (Metallic)/Storm Bay (Metallic)', 'Metallic'),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Alpine White (Non-Metallic)/Black Sapphire (Metallic)/M Portimao Blue (Metallic)/Space Silver (Metallic)/Storm Bay (Metallic)', 'Metallic'),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Dune Grey Metallic, Alpine White, Individual Tanzanite Blue, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Dune Grey Metallic, Alpine White, Individual Tanzanite Blue, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X5', 'xDrive40i'), 'Mineral White Metallic, SkyScraper Grey Metallic, Black, Sapphire Metallic', 'Metallic'),
        (('BMW', 'X5', 'xDrive30d'), 'Mineral White Metallic, SkyScraper Grey Metallic, Black, Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Mineral White Metallic, Tanzanite Blue Metallic, Skyscraper Grey Metallic, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Mineral White Metallic, Tanzanite Blue Metallic, Skyscraper Grey Metallic, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Mineral White (Metallic),  Black Sapphire (Metallic), Sparkling Copper Grey (Metallic)', 'Metallic'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Black Sapphire metallic,  Mineral White metallic,  Cape York Green metallic,  Dravit Grey metallic,  M Carbon Black metallic,  M Marina Bay Blue metallic,  M Toronto Red metallic', 'Metallic'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Portimao Blue Metallic,  Mineral White Metallic,  Skyscraper Grey Metallic,  Carbon Black Metallic,  Sparkling Cooper Grey Metallic', 'Metallic'),
        (('BMW', 'iX', 'xDrive 50'), 'Black Sapphire Metallic, Sophisto Grey (metallic), Mineral White Metallic,  Phytonic Blue Metallic,  Aventurin Red metallic,  Oxide Grey Metallic,  Storm Bay Metallic', 'Metallic'),
        (('BMW', '2 Series', '218 M Sport'), 'Black Sapphire Metallic, Alpine White, Portimao Blue Metallic, Brooklyn Grey', 'Metallic'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Black Sapphire Metallic, Alpine White, Portimao Blue Metallic, Brooklyn Grey', 'Metallic'),
        (('BMW', 'M2', '3.0 Petrol'), 'Brooklyn Grey Metallic, Skyscraper Grey Metallic, Dragon Fire Red Metallic, Black Sapphire, Portimao Blue Metallic, Sao Paulo Yellow, M Zandvoort Blue, Alpine White 3', 'Metallic'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Mineral White Metallic, Carbon Black Metallic, Skyscraper Grey Metallic, Arctic Race Blue Metallic', 'Metallic'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Mineral White Metallic, Carbon Black Metallic, Skyscraper Grey Metallic, Arctic Race Blue Metallic', 'Metallic'),
        (('BMW', '3 Series', 'M340i'), 'Tanzanite Blue Metallic,  Dravit Grey Metallic,  Black Sapphire Metallic, Fire Red,  Arctic Race Blue', 'Metallic'),
        (('BMW', 'M4', 'Competition'), 'Black Sapphire Metallic, Toronto Red Metallic, Skyscraper Grey Metallic, Portimao Blue Metallic, Sao Paulo Yellow Metallic, Isle of Man Green Metallic, Dravit Gey Metallic, Tanzanite Blue Metallic, Aventurine Red Metallic, Brooklyn Grey Metallic', 'Metallic'),
        (('BMW', 'M4', 'CS'), 'Black Sapphire Metallic, Isle of Man Green Metallic, Brooklyn Grey Metallic', 'Metallic'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Black Sapphire metallic, Skyscraper Grey metallic, Mineral White metallic', 'Metallic'),
        (('BMW', '5 Series', '530Li M Sport'), 'Carbon Black, Sparkling Cooper Grey', 'Metallic'),
        (('BMW', 'M5', 'Competition'), 'M Carbon Black metallic, Black Sapphire metallic, Sophisto Grey brilliant effect metallic, M Marina Bay Blue metallic, M Isle of Man Green metallic, M Brooklyn Grey metallic, Fire Red metallic', 'Metallic'),
        (('BMW', 'i5', 'M60 xDrive'), 'Alpine White Solid, M Carbon Black Metallic, Black Sapphire Metallic, Sophisto Grey brilliant effect metallic, Mineral White metallic, Phytonic Blue metallic, Oxide Grey metallic, M Brooklyn Grey metallic, Cape York Green metallic, Fire Red metallic, Tanzanite Blue, Frozen Deep Grey metallic, Frozen Pure Grey metallic, Frozen Portimao Blue metallic', 'Metallic'),
        (('BMW', '7 Series', '740i M Sport'), 'Black Sapphire Metallic, Individual Dravit Grey Metallic, Individual Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', '7 Series', '740d M Sport'), 'Black Sapphire Metallic, Individual Dravit Grey Metallic, Individual Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Black Sapphire Metallic, Dravit Grey Metallic, Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'i7', 'M70 xDrive'), 'Black Sapphire Metallic, Dravit Grey Metallic, Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'M8', 'Competition Coupé'), 'Black Sapphire metallic, Marina Bay Blue metallic, Isle of Man Green metallic, Brooklyn Grey metallic, Skyscraper Grey metallic, Aventurine Red metallic, Tanzanite Blue metallic, Daytona Beach Blue, Dravit Grey metallic', 'Metallic'),
        (('BMW', 'Z4', 'M40i'), 'Alpine White, Black Sapphire metallic, M Portimao Blau metallic, San francisco red metallic, Skyscraper grey metallic, Thundernight metallic', 'Metallic'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Navarra Blue, Mythos Black, Glacier White', 'Solid'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Navarra Blue, Mythos Black, Glacier White', 'Solid'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Mythos Black, Glacier White, Navarra Blue, Tango Red, Manhattan Grey', 'Solid'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Glacier White, Firmament Blue Metallic, Mythos Black Metallic, Madeira Brown Metallic, Manhattan Grey Metallic', 'Metallic'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Glacier White, Firmament Blue Metallic, Mythos Black Metallic, Madeira Brown Metallic, Manhattan Grey Metallic', 'Metallic'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Manhattan Grey, Mythos Black, Madeira Brown, Firmament Blue, Glacier White', 'Metallic'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Pulse Orange, Nano Grey Metallic, Glacier White Metallic, Mythos Black Metallic, Navarra Blue Metallic', 'Metallic'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Pulse Orange, Nano Grey Metallic, Glacier White Metallic, Mythos Black Metallic, Navarra Blue Metallic', 'Metallic'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Navarra Blue Metallic, Glacier White, Mythos Black Metallic, Manhattan Gray Metallic', 'Metallic'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Navarra Blue Metallic, Glacier White, Mythos Black Metallic, Manhattan Gray Metallic', 'Metallic'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Sakhir Gold, Waitomo Blue, Glacier White, Mythos Black, Samurai Grey', 'Metallic'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Sakhir Gold, Waitomo Blue, Glacier White, Mythos Black, Samurai Grey', 'Metallic'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Glacier White Metallic, Mythos Black Metallic, Sakhir Gold Metallic, Samurai Gray Metallic, Satellite Silver Metallic, Tamarind Brown Metallic, Vicuna Beige Metallic, Waitomo Blue Metallic', 'Metallic'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Mythos Black Metallic, Glacier White Metallic, Chili Red Metallic, Sakhir Gold Metallic, Satellite Silver Metallic, Waitomo Blue Metallic, Ascari Blue Metallic', 'Metallic'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Tango Red Metallic, Mythos Black Metallic, Ibis White Solid, Navara Blue Metallic, District Green Metallic, Daytona Grey Pearl', 'Metallic'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Ibis White, Ascari Blue Metallic, Floret Silver Metallic, Kemora Grey Metallic, Mythos Black Metallic, Suzuka Grey Metallic, Tactics Green Metallic, Tango Red Metallic, Daytona Gray Pearl Effect', 'Metallic'),
        # --- Indian Market Additions Colors ---
        (('Ford', 'Endeavour', 'Titanium+ 2.0 4x4 AT'), 'Diffused Silver, Absolute Black, Diamond White, Moondust Silver', 'Metallic'),
        (('Ford', 'Mustang', 'GT V8'), 'Race Red, Oxford White, Shadow Black, Magnetic Metallic, Triple Yellow', 'Metallic'),
        (('Mahindra', 'XUV700', 'AX7 Diesel AT Luxury Pack AWD'), 'Everest White, Midnight Black, Electric Blue, Dazzling Silver, Red Rage', 'Metallic'),
        (('Mahindra', 'Scorpio-N', 'Z8L Diesel 4x4 AT'), 'Dazzling Silver, Deep Forest, Grand Canyon, Napoli Black, Everest White', 'Metallic'),
        (('Mahindra', 'Thar', 'LX 4-Str Hard Top Diesel AT 4WD'), 'Napoli Black, Galaxy Grey, Aquamarine, Red Rage, Everest White', 'Metallic'),
        (('Hyundai', 'Creta', 'SX (O) 1.5 Diesel AT'), 'Abyss Black, Atlas White, Ranger Khaki, Titan Grey, Robust Emerald Pearl, Fiery Red', 'Metallic'),
        (('Hyundai', 'Venue', 'SX (O) 1.0 Turbo DCT'), 'Typhoon Silver, Titan Grey, Denim Blue, Abyss Black, Atlas White, Fiery Red', 'Metallic'),
        (('Hyundai', 'Verna', 'SX (O) 1.5 Turbo DCT'), 'Titan Grey, Tellurian Brown, Atlas White, Abyss Black, Starry Night, Fiery Red', 'Metallic'),
        (('Hyundai', 'Bayon', '1.5 NA MT'), 'Polar White, Intense Blue, Dragon Red, Mangrove Green, Phantom Black', 'Metallic'),
        (('Honda', 'City', 'ZX CVT'), 'Platinum White Pearl, Lunar Silver Metallic, Meteoroid Grey Metallic, Golden Brown Metallic, Radiant Red Metallic', 'Metallic'),
        (('Honda', 'Elevate', 'ZX CVT'), 'Phoenix Orange Pearl, Obsidian Blue Pearl, Platinum White Pearl, Golden Brown Metallic, Meteoroid Grey Metallic, Lunar Silver Metallic', 'Metallic'),
        (('Maruti Suzuki', 'Swift', 'ZXi Plus AMT'), 'Luster Blue, Novel Orange, Sizzling Red, Pearl Arctic White, Magma Grey, Splendid Silver', 'Metallic'),
        (('Maruti Suzuki', 'Brezza', 'ZXi Plus AT'), 'Brave Khaki, Magma Grey, Sizzling Red, Splendid Silver, Exuberant Blue, Pearl Arctic White', 'Metallic'),
        (('Maruti Suzuki', 'Grand Vitara', 'Alpha+ Strong Hybrid e-CVT'), 'Nexa Blue, Arctic White, Splendid Silver, Grandeur Grey, Chestnut Brown, Opulent Red', 'Metallic'),
        (('Tata Motors', 'Nexon', 'Fearless Plus S 1.2 DCA'), 'Fearless Purple, Creative Ocean, Pure Grey, Flame Red, Daytona Grey, Pristine White', 'Metallic'),
        (('Tata Motors', 'Harrier', 'Fearless+ Dark Edition AT'), 'Oberon Black, Sunlit Yellow, Pebble Grey, Lunar White, Coral Red', 'Metallic'),
        (('Tata Motors', 'Safari', 'Accomplished+ Dark Edition AT'), 'Oberon Black, Cosmic Gold, Supernova Copper, Stardust Ash, Galactic Sapphire, Pristine White', 'Metallic'),
        (('Tata Motors', 'Punch', 'Creative AMT'), 'Tornado Blue, Calypso Red, Atomic Orange, Meteor Bronze, Daytona Grey, Tropical Mist, Orcus White', 'Metallic'),
        (('Tata Motors', 'Sierra', 'EV Empowered AWD'), 'Jade Green, Arctic Glacier White, Obsidian Black, Starlight Silver', 'Metallic'),
        (('Tata Motors', 'Curvv', 'Creative 1.5 Diesel AT'), 'Gold Essence, Cosmic Gold, Flame Red, Pristine White, Pure Grey, Daytona Grey', 'Metallic'),
        (('Tata Motors', 'Aeris', 'Smart EV'), 'Teal Blue, Daytona Grey, Pristine White, Tropical Mist', 'Metallic'),
        (('Kia', 'Seltos', 'X-Line 1.5 Diesel AT'), 'Matte Graphite, Imperial Blue, Intense Red, Gravity Grey, Aurora Black Pearl, Glacier White Pearl, Pewter Olive', 'Matte'),
        (('Kia', 'Sonet', 'X-Line 1.0 Turbo DCT'), 'Matte Graphite, Pewter Olive, Imperial Blue, Intense Red, Gravity Grey, Aurora Black Pearl, Glacier White Pearl', 'Matte'),
        (('Kia', 'EV6', 'GT-Line AWD'), 'Moonscape Matte, Yacht Blue, Runway Red, Snow White Pearl, Aurora Black Pearl', 'Matte'),
        (('Toyota', 'Fortuner', 'GR-S 2.8 Diesel 4x4 AT'), 'Attitude Black, Sparkling Black, Platinum White Pearl, Super White, Silver Metallic', 'Metallic'),
        (('Toyota', 'Innova Hycross', 'ZX(O) Hybrid'), 'Blackish Ageha Glass Flake, Platinum White Pearl, Attitude Black Mica, Silver Metallic, Super White', 'Metallic'),
        (('Toyota', 'Urban Cruiser Hyryder', 'V Hybrid'), 'Cafe White, Enticing Silver, Gaming Grey, Sporting Red, Midnight Black, Cave Black, Speedy Blue', 'Metallic'),
        (('MG Motor', 'Hector', 'Savvy Pro 1.5 CVT'), 'Havana Grey, Candy White, Starry Black, Aurora Silver, Glaze Red, Dune Brown', 'Metallic'),
        (('MG Motor', 'ZS EV', 'Exclusive Pro'), 'Candy White, Starry Black, Aurora Silver, Currant Red', 'Metallic'),
        (('Volkswagen', 'Virtus', 'GT Plus 1.5 TSI DSG'), 'Wild Cherry Red, Candy White, Carbon Steel Grey, Curcuma Yellow, Reflex Silver, Rising Blue Metallic, Lava Blue', 'Metallic'),
        (('Volkswagen', 'Taigun', 'GT Plus 1.5 TSI DSG'), 'Wild Cherry Red, Candy White, Carbon Steel Grey, Curcuma Yellow, Reflex Silver, Lava Blue Metallic', 'Metallic'),
        (('Skoda', 'Slavia', 'Style 1.5 TSI DSG'), 'Crystal Blue, Tornado Red, Candy White, Brilliant Silver, Carbon Steel, Deep Black', 'Metallic'),
        (('Skoda', 'Kushaq', 'Style 1.5 TSI DSG'), 'Honey Orange, Tornado Red, Candy White, Brilliant Silver, Carbon Steel, Deep Black', 'Metallic'),
        (('Jeep', 'Compass', 'Model S 4x4 Diesel AT'), 'Galaxy Blue, Brilliant Black, Exotica Red, Techno Metallic Green, Silvery Moon, Pearl White', 'Metallic'),
        (('Jeep', 'Wrangler', 'Rubicon'), 'Firecracker Red, Bright White, Black Clearcoat, Sarge Green, Granite Crystal Metallic, Hydro Blue', 'Solid'),
        (('BYD', 'Atto 3', 'Extended Range'), 'Surf Blue, Parkour Red, Boulder Grey, Ski White, Cosmos Black', 'Metallic'),
        (('BYD', 'Seal', 'Performance AWD'), 'Arctic Blue, Atlantis Grey, Aurora White, Cosmos Black', 'Metallic'),
        (('Land Rover', 'Range Rover', 'Autobiography 3.0 LWB'), 'Santorini Black, Fuji White, Batumi Gold, Belgravia Green, Charente Grey, Portofino Blue, Hakuba Silver, Eiger Grey', 'Metallic'),
        (('Land Rover', 'Defender', '110 HSE 3.0 Diesel'), 'Pangea Green, Gondwana Stone, Tasman Blue, Santorini Black, Fuji White, Eiger Grey, Hakuba Silver, Silicon Silver', 'Metallic'),
        (('Porsche', '911', 'Carrera S'), 'Guards Red, Racing Yellow, White, Black, GT Silver Metallic, Gentian Blue Metallic, Aventurine Green Metallic, Chalk, Python Green', 'Metallic'),
        (('Porsche', 'Macan', 'Macan S'), 'Papaya Metallic, Gentian Blue Metallic, Carrara White Metallic, Volcano Grey Metallic, Jet Black Metallic, Copper Ruby Metallic, Carmine Red', 'Metallic'),
        (('Porsche', 'Taycan', 'Turbo S'), 'Frozen Blue Metallic, Mamba Green Metallic, Carmine Red, Neptune Blue, Carrara White Metallic, Jet Black Metallic, Crayon, Ice Grey Metallic', 'Metallic'),
        (('Lexus', 'RX', '350h Luxury'), 'Sonic Quartz, Sonic Titanium, Sonic Chrome, Sonic Iridium, Graphite Black, Red Mica Crystal Shine, Deep Blue Mica', 'Metallic'),
        (('Lexus', 'ES', '300h Luxury'), 'Sonic Quartz, Sonic Titanium, Sonic Chrome, Sonic Iridium, Black, Deep Blue Mica', 'Metallic'),
        (('Ferrari', 'Roma', 'Coupe'), 'Rosso Corsa, Bianco Avus, Nero Daytona, Blu Pozzi, Grigio Silverstone, Giallo Modena, Grigio Titanio', 'Metallic'),
        (('Ferrari', '296 GTB', 'Coupe'), 'Rosso Corsa, Rosso Scuderia, Blu Tour de France, Giallo Modena, Bianco Cervino, Nero Daytona, Grigio Scuro', 'Metallic'),
        (('Lamborghini', 'Urus', 'Performante'), 'Giallo Auge, Arancio Borealis, Bianco Monocerus, Nero Noctis, Verde Mantis, Grigio Keres, Blu Astraeus, Rosso Mars', 'Metallic'),
        (('Lamborghini', 'Revuelto', 'Coupe'), 'Arancio Apodis, Giallo Inti, Verde Scandal, Bianco Icarus, Nero Pegaso, Blu Eleos, Grigio Telesto, Rosso Bia', 'Metallic')
    ]


    # Strict Foreign Key Crosscheck: Verify Variant exists before inserting Colors
    for color in car_colors:
        brand, model, variant_name = color[0]
        color_name, color_type = color[1], color[2]

        if (brand, model, variant_name) not in valid_variants:
            print(f"[DATA INTEGRITY WARNING] Color skipped: Variant '{variant_name}' for '{brand} {model}' not found in database.")
            continue

        variant_id = valid_variants[(brand, model, variant_name)]
        try:
            cur.execute("SELECT color_id FROM colors WHERE variant_id = %s AND color_name = %s LIMIT 1", (variant_id, color_name))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO colors (variant_id, color_name, color_type)
                    VALUES (%s, %s, %s)
                """, (variant_id, color_name, color_type))
        except Exception as e:
            if "Duplicate entry" not in str(e):
                print(f"[DATA INTEGRITY ERROR] Error inserting color for '{brand} {model} {variant_name}': {e}")

    conn.commit()
    print("✓ All Colors inserted successfully!")

def generate_booking_id():
    """Generates unique alphanumeric reference ID formatted as BK-XXXXXX."""
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    numbers = ''.join(random.choices(string.digits, k=2))
    return f"BK-{letters}{numbers}"



# ---------- Web App UI Setup (STRICTLY NATIVE PYTHON) ----------
db_cfg, db_source = get_db_config()

# Sidebar: Navigation Console & System Telemetry
st.sidebar.title("AutoSpec Web")
st.sidebar.caption("Automotive Intelligence Platform")

conn = get_db_connection(db_cfg)
if not conn:
    st.error("Fatal: Database connection could not be established. Check server configuration.")
    st.stop()

cursor = conn.cursor(buffered=True)

# Auto-seed database if brands < 23 (seamless initial or expanded deployment)
try:
    cursor.execute("SELECT COUNT(*) FROM brands")
    brand_cnt = cursor.fetchone()
    if not brand_cnt or brand_cnt[0] < 23:
        insert_sample_data(cursor, conn)
except Exception as e:
    print(f"[DATA INTEGRITY ERROR] Auto-seed check failed: {e}")

# ----------------- SIDEBAR NAVIGATION -----------------
with st.sidebar.container(border=True):
    st.caption("NAVIGATION CONSOLE")
    mode = st.radio(
        "Operational Mode",
        ["User Mode", "Admin Mode"],
        index=0,
        help="Select User Mode for vehicle discovery, comparison, and booking, or Admin Mode for management analytics and database control."
    )

with st.sidebar.container(border=True):
    st.caption("THEME SWITCHER (7 PALETTES)")
    theme_names_list = list(THEMES.keys())
    current_th = st.session_state.get("app_theme", "Dark Mode")
    cur_idx = theme_names_list.index(current_th) if current_th in theme_names_list else 0

    def on_theme_change():
        st.session_state["app_theme"] = st.session_state["app_theme_selector"]

    chosen_theme = st.selectbox(
        "Visual Palette",
        theme_names_list,
        index=cur_idx,
        key="app_theme_selector",
        on_change=on_theme_change,
        help="Select any theme to transform colors across the site."
    )
    st.caption(f"Active Theme: **{chosen_theme}**")

# Helper function for vehicle image lookup
def get_car_image(brand, model):
    safe_b = brand.replace(" ", "_")
    safe_m = model.replace(" ", "_")
    p = os.path.join("images", f"{safe_b}_{safe_m}.jpg")
    if os.path.exists(p):
        return p
    return f"https://placehold.co/800x450/161B22/E63946/png?text={safe_b}+{safe_m}"

# Helper function for Indian currency formatting
def format_inr(val):
    if not val or val == 0:
        return "Price on Request"
    val = float(val)
    if val >= 10000000:
        return f"₹ {val / 10000000:.2f} Cr"
    elif val >= 100000:
        return f"₹ {val / 100000:.2f} Lakh"
    return f"₹ {val:,.2f}"

def format_rupees(val):
    try:
        return f"₹ {int(val):,}"
    except Exception:
        return str(val)

# ==============================================================================
# USER MODE
# ==============================================================================
if mode == "User Mode":
    st.title("AutoSpec Web")
    st.caption("Comprehensive vehicle specifications, performance benchmarking, dynamic financial calculation, and reservations.")
    st.divider()

    tab1, tab2, tab3, tab_emi, tab4, tab5 = st.tabs([
        "Explore Brands",
        "Search & Filter",
        "Car Details",
        "EMI Calculator",
        "Compare Cars",
        "Book a Car"
    ])

    # ------------------ TAB 1: EXPLORE BRANDS ------------------
    with tab1:
        st.subheader("Automotive Manufacturers")
        st.caption("Browse prestige manufacturers across global automotive markets.")

        cursor.execute("""
            SELECT b.brand_name, b.country_of_origin, b.year_founded,
                   COUNT(DISTINCT m.model_id) as total_models,
                   COUNT(DISTINCT v.variant_id) as total_variants
            FROM brands b
            LEFT JOIN models m ON b.brand_id = m.brand_id
            LEFT JOIN variants v ON m.model_id = v.model_id
            GROUP BY b.brand_id, b.brand_name, b.country_of_origin, b.year_founded
            ORDER BY b.brand_name
        """)
        brand_data = cursor.fetchall()

        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.metric("Total Manufacturers", len(brand_data))
        with c2:
            total_m = sum(row[3] for row in brand_data)
            with st.container(border=True):
                st.metric("Cataloged Models", total_m)
        with c3:
            total_v = sum(row[4] for row in brand_data)
            with st.container(border=True):
                st.metric("Production Variants", total_v)

        st.divider()

        all_countries = sorted(list(set(b[1] for b in brand_data if b[1])))
        selected_country = st.selectbox("Filter by Country of Origin", ["All Countries"] + all_countries, key="mfg_country")

        filtered_brands = brand_data
        if selected_country != "All Countries":
            filtered_brands = [b for b in brand_data if b[1] == selected_country]

        df_brands = pd.DataFrame(
            filtered_brands,
            columns=["Manufacturer", "Country of Origin", "Year Founded", "Models Count", "Variants Count"]
        )
        st.dataframe(df_brands, use_container_width=True, hide_index=True)

    # ------------------ TAB 2: SEARCH & FILTER (NATIVE DATAFRAME ENHANCEMENTS) ------------------
    with tab2:
        st.subheader("Search & Filter Vehicles")
        st.caption("Find vehicles matching your powertrain, body style, and pricing parameters.")

        with st.container(border=True):
            col_f1, col_f2, col_f3, col_f4 = st.columns([1, 1, 1.2, 0.8])
            with col_f1:
                fuel_filter = st.selectbox("Powertrain", ["All", "Petrol", "Diesel", "Electric", "Hybrid"], key="sr_fuel")
            with col_f2:
                body_filter = st.selectbox("Body Architecture", ["All", "SUV", "Sedan", "Coupé", "Gran Coupé", "SportBack", "Convertible", "Roadster"], key="sr_body")
            with col_f3:
                max_price = st.slider("Max Price (INR)", min_value=500000, max_value=50000000, value=50000000, step=500000, format="₹%d", key="sr_price")
            with col_f4:
                curr_view = st.radio("Display View", ["Data Table", "Grid Cards"], index=0, horizontal=True, key="sr_view")

        t_start = time.time()
        query = """
            SELECT b.brand_name, m.model_name, m.body_type, v.variant_name, v.price_inr,
                   v.fuel_type, v.power_bhp, v.torque_nm, v.acceleration_0_100, v.top_speed_kmh, v.transmission
            FROM variants v
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE v.price_inr <= %s
        """
        params = [max_price]

        if fuel_filter != "All":
            query += " AND v.fuel_type LIKE %s"
            params.append(f"%{fuel_filter}%")
        if body_filter != "All":
            query += " AND m.body_type LIKE %s"
            params.append(f"%{body_filter}%")

        query += " ORDER BY v.price_inr ASC"
        cursor.execute(query, params)
        catalog_results = cursor.fetchall()

        st.caption(f"Displaying {len(catalog_results)} matching vehicles.")

        if catalog_results:
            if curr_view == "Data Table":
                df_cat = pd.DataFrame(catalog_results, columns=[
                    "Brand", "Model", "Body Architecture", "Trim Variant", "Price (INR)",
                    "Powertrain", "Power (BHP)", "Torque (Nm)", "0-100 km/h (s)", "Top Speed (km/h)", "Transmission"
                ])

                # Objective 2: Pandas .style to format Price (INR) in Indian Rupees and highlight lowest price in green
                styler = df_cat.style.format({
                    "Price (INR)": format_rupees
                }).highlight_min(subset=["Price (INR)"], color="#2E7D32")

                # Objective 2: st.column_config with ProgressColumn bars for stats
                col_config = {
                    "Top Speed (km/h)": st.column_config.ProgressColumn(
                        "Top Speed (km/h)",
                        help="Maximum achievable speed",
                        format="%d km/h",
                        min_value=0,
                        max_value=350,
                    ),
                    "0-100 km/h (s)": st.column_config.ProgressColumn(
                        "0-100 km/h (s)",
                        help="Acceleration sprint 0 to 100 km/h",
                        format="%.1f s",
                        min_value=0,
                        max_value=15,
                    ),
                    "Power (BHP)": st.column_config.ProgressColumn(
                        "Power (BHP)",
                        help="Peak engine power output",
                        format="%d BHP",
                        min_value=0,
                        max_value=1050,
                    )
                }

                st.dataframe(
                    styler,
                    column_config=col_config,
                    hide_index=True,
                    use_container_width=True
                )
            else:
                for row_idx in range(0, len(catalog_results), 3):
                    cols = st.columns(3)
                    for col_idx, item_idx in enumerate(range(row_idx, min(row_idx + 3, len(catalog_results)))):
                        c_b, c_m, c_body, c_v, c_p, c_fuel, c_bhp, c_tq, c_acc, c_top, c_tr = catalog_results[item_idx]
                        img_path = get_car_image(c_b, c_m)
                        formatted_p = format_inr(c_p)

                        with cols[col_idx]:
                            with st.container(border=True):
                                st.image(img_path, use_container_width=True)
                                st.subheader(f"{c_b} {c_m}")
                                st.caption(f"Trim: {c_v}")
                                st.write(f"**Price:** {formatted_p}")
                                st.write(f"**Specs:** {c_fuel} | {c_bhp} BHP | {c_acc}s 0-100")
                                if st.button("Inspect Details", key=f"cat_btn_{item_idx}", use_container_width=True):
                                    st.session_state["spec_brand"] = c_b
                                    st.session_state["spec_model"] = c_m
                                    st.session_state["spec_variant"] = c_v
                                    st.info(f"Loaded {c_b} {c_m}: {c_v}. Navigate to the 'Car Details' tab.")
        else:
            st.info("No vehicles match the selected criteria. Adjust maximum price or powertrain filters.")

    # ------------------ TAB 3: CAR DETAILS (WITH DYNAMIC EMI CALCULATOR) ------------------
    with tab3:
        st.subheader("Car Details & Engineering Specifications")
        st.caption("Deep vehicle inspection, performance metrics, dynamic EMI calculator, and equipment list.")

        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brand_list = [b[0] for b in cursor.fetchall()]

        with st.container(border=True):
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if "spec_brand" not in st.session_state or st.session_state["spec_brand"] not in brand_list:
                    st.session_state["spec_brand"] = brand_list[0] if brand_list else None
                selected_brand = st.selectbox("Manufacturer", brand_list, key="spec_brand")

            cursor.execute("""
                SELECT model_name FROM models m
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s ORDER BY model_name
            """, (selected_brand,))
            model_list = [m[0] for m in cursor.fetchall()]

            with col_s2:
                if "spec_model" not in st.session_state or st.session_state["spec_model"] not in model_list:
                    st.session_state["spec_model"] = model_list[0] if model_list else None
                selected_model = st.selectbox("Model Line", model_list, key="spec_model")

            cursor.execute("""
                SELECT v.variant_id, v.variant_name, v.price_inr, v.engine, v.power_bhp, v.torque_nm,
                       v.top_speed_kmh, v.acceleration_0_100, v.transmission, v.drivetrain,
                       v.fuel_type, v.mileage_range, v.seating_capacity, v.safety_rating
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s
                ORDER BY v.variant_name
            """, (selected_brand, selected_model))
            variant_rows = cursor.fetchall()

            variant_names = [v[1] for v in variant_rows]
            with col_s3:
                if "spec_variant" not in st.session_state or st.session_state["spec_variant"] not in variant_names:
                    st.session_state["spec_variant"] = variant_names[0] if variant_names else None
                selected_variant = st.selectbox("Trim Variant", variant_names, key="spec_variant")

        selected_row = next((v for v in variant_rows if v[1] == selected_variant), None)

        if selected_row:
            v_id, v_name, v_price, v_engine, v_bhp, v_torque, v_top_speed, v_accel, v_trans, v_drive, v_fuel, v_mileage, v_seats, v_safety = selected_row
            raw_car_price = float(v_price or 0)
            price_str = f"₹ {raw_car_price:,.2f}" if raw_car_price else "Price on Request"

            with st.container(border=True):
                col_img, col_hero = st.columns([1.2, 1])
                with col_img:
                    img_path = get_car_image(selected_brand, selected_model)
                    st.image(img_path, caption=f"{selected_brand} {selected_model}", use_container_width=True)
                with col_hero:
                    st.subheader(f"{selected_brand} {selected_model}")
                    st.caption(f"Trim: {v_name}")
                    st.write(f"### {price_str}")
                    st.write(f"**Engine Configuration:** {v_engine}")
                    st.write(f"**Transmission:** {v_trans}")
                    st.write(f"**Drivetrain:** {v_drive}")
                    st.write(f"**Powertrain:** {v_fuel}")

                    if st.button("Proceed to Book This Vehicle", type="primary", use_container_width=True):
                        st.session_state["book_brand"] = selected_brand
                        st.session_state["book_model"] = selected_model
                        st.session_state["book_variant"] = selected_variant
                        st.session_state["prefill_brand"] = selected_brand
                        st.session_state["prefill_model"] = selected_model
                        st.session_state["prefill_variant"] = selected_variant
                        st.success(f"Vehicle selected: {selected_brand} {selected_model} ({selected_variant}). Navigate to 'Book a Car' tab.")

            st.divider()

            # Performance Specifications
            st.subheader("Performance Specifications")
            with st.container(border=True):
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric(label="Power", value=f"{v_bhp} BHP")
                with m2:
                    st.metric(label="Torque", value=f"{v_torque} Nm")
                with m3:
                    st.metric(label="0 to 100 km/h", value=f"{v_accel} s")
                with m4:
                    st.metric(label="Top Speed", value=f"{v_top_speed} km/h")

            st.subheader("Vehicle Engineering Details")
            with st.container(border=True):
                sp1, sp2, sp3, sp4 = st.columns(4)
                with sp1:
                    st.metric(label="Efficiency / Range", value=str(v_mileage))
                with sp2:
                    st.metric(label="Seating Capacity", value=f"{v_seats} Seats")
                with sp3:
                    st.metric(label="Safety Rating", value=str(v_safety))
                with sp4:
                    st.metric(label="Drivetrain", value=str(v_drive))

            st.divider()

            # Feature 3: Dynamic EMI Calculator (User Mode)
            st.subheader("Dynamic Loan EMI Calculator")
            st.caption("Calculate estimated monthly installments based on selected vehicle ex-showroom price.")
            with st.container(border=True):
                col_e1, col_e2, col_e3 = st.columns(3)
                with col_e1:
                    down_pay_pct = st.slider("Down Payment (%)", min_value=10, max_value=80, value=20, step=5, key="emi_dp_pct")
                    down_pay_val = raw_car_price * (down_pay_pct / 100.0)
                    st.caption(f"Down Payment Amount: ₹ {down_pay_val:,.2f}")
                with col_e2:
                    tenure_years = st.slider("Loan Tenure (Years)", min_value=1, max_value=7, value=5, step=1, key="emi_tenure_yrs")
                    st.caption(f"Tenure Duration: {tenure_years * 12} Months")
                with col_e3:
                    interest_rate_pct = st.slider("Interest Rate (%)", min_value=7.0, max_value=15.0, value=8.5, step=0.25, key="emi_rate_pct")
                    st.caption(f"Annual Percentage Rate (APR): {interest_rate_pct:.2f}%")

                # Mathematical logic for EMI calculation: EMI = [P x r x (1+r)^n] / [(1+r)^n - 1]
                loan_principal = raw_car_price - down_pay_val
                tenure_months = tenure_years * 12
                monthly_rate = (interest_rate_pct / 100.0) / 12.0

                if monthly_rate > 0 and tenure_months > 0:
                    monthly_emi = loan_principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
                else:
                    monthly_emi = loan_principal / tenure_months if tenure_months else 0

                total_repayment = monthly_emi * tenure_months
                total_interest = total_repayment - loan_principal

                # Prominent st.metric display
                st.metric(
                    label="Estimated Monthly EMI",
                    value=f"₹ {monthly_emi:,.2f} / month",
                    delta=f"Principal Debt: ₹ {loan_principal:,.2f} | Total Interest: ₹ {total_interest:,.2f}",
                    delta_color="off"
                )

                df_emi_chart = pd.DataFrame({
                    "Capital Component": ["Down Payment", "Principal Loan", "Total Interest Payable"],
                    "Amount (INR)": [down_pay_val, loan_principal, total_interest]
                }).set_index("Capital Component")
                st.bar_chart(df_emi_chart)

            st.divider()

            # Expanders for secondary information
            cursor.execute("SELECT feature_category, feature_description FROM features WHERE variant_id = %s", (v_id,))
            features = cursor.fetchall()

            with st.expander("Full Equipment & Features List", expanded=False):
                if features:
                    f_col1, f_col2 = st.columns(2)
                    mid = (len(features) + 1) // 2
                    with f_col1:
                        for f in features[:mid]:
                            st.write(f"**{f[0]}:** {f[1]}")
                    with f_col2:
                        for f in features[mid:]:
                            st.write(f"**{f[0]}:** {f[1]}")
                else:
                    st.write("Standard factory specifications apply.")

            cursor.execute("SELECT color_name, color_type FROM colors WHERE variant_id = %s", (v_id,))
            colors_data = cursor.fetchall()

            with st.expander("Available Color Options", expanded=False):
                if colors_data:
                    for c_name, c_type in colors_data:
                        st.write(f"• **{c_type}:** {c_name}")
                else:
                    st.write("Standard factory exterior and interior finishes.")

            with st.expander("Technical Specification Data Sheet", expanded=False):
                spec_items = [
                    {"Parameter": "Manufacturer", "Specification": selected_brand},
                    {"Parameter": "Model Line", "Specification": selected_model},
                    {"Parameter": "Variant Trim", "Specification": v_name},
                    {"Parameter": "Ex-Showroom Price", "Specification": price_str},
                    {"Parameter": "Engine Configuration", "Specification": v_engine},
                    {"Parameter": "Peak Power Output", "Specification": f"{v_bhp} BHP"},
                    {"Parameter": "Peak Torque Output", "Specification": f"{v_torque} Nm"},
                    {"Parameter": "0-100 km/h Sprint", "Specification": f"{v_accel} s"},
                    {"Parameter": "Top Speed", "Specification": f"{v_top_speed} km/h"},
                    {"Parameter": "Transmission", "Specification": v_trans},
                    {"Parameter": "Drivetrain", "Specification": v_drive},
                    {"Parameter": "Powertrain Fuel", "Specification": v_fuel},
                    {"Parameter": "Efficiency / Range", "Specification": v_mileage},
                    {"Parameter": "Seating Capacity", "Specification": f"{v_seats} Passengers"},
                    {"Parameter": "Safety Rating", "Specification": v_safety}
                ]
                st.dataframe(pd.DataFrame(spec_items), use_container_width=True, hide_index=True)
        else:
            st.info("Select a Manufacturer, Model Line, and Trim Variant above to inspect vehicle engineering specifications.")

    # ------------------ TAB: DEDICATED EMI CALCULATOR ------------------
    with tab_emi:
        st.subheader("Dynamic Automotive Loan EMI Calculator")
        st.caption("Interactively calculate loan installments, amortisation schedules, and financing requirements.")

        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        all_calc_brands = [b[0] for b in cursor.fetchall()]

        with st.container(border=True):
            st.subheader("Select Vehicle to Finance")
            col_eb1, col_eb2, col_eb3 = st.columns(3)
            with col_eb1:
                if "ded_emi_brand" not in st.session_state or st.session_state["ded_emi_brand"] not in all_calc_brands:
                    prefill_b = st.session_state.get("spec_brand")
                    st.session_state["ded_emi_brand"] = prefill_b if (prefill_b and prefill_b in all_calc_brands) else (all_calc_brands[0] if all_calc_brands else None)
                sel_eb_brand = st.selectbox("Manufacturer", all_calc_brands, key="ded_emi_brand")

            cursor.execute("""
                SELECT model_name FROM models m
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s ORDER BY model_name
            """, (sel_eb_brand,))
            all_calc_models = [m[0] for m in cursor.fetchall()]

            with col_eb2:
                if "ded_emi_model" not in st.session_state or st.session_state["ded_emi_model"] not in all_calc_models:
                    prefill_m = st.session_state.get("spec_model")
                    st.session_state["ded_emi_model"] = prefill_m if (prefill_m and prefill_m in all_calc_models) else (all_calc_models[0] if all_calc_models else None)
                sel_eb_model = st.selectbox("Model Line", all_calc_models, key="ded_emi_model")

            cursor.execute("""
                SELECT v.variant_id, v.variant_name, v.price_inr
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s
                ORDER BY v.variant_name
            """, (sel_eb_brand, sel_eb_model))
            all_calc_variants = cursor.fetchall()
            calc_var_dict = {v[1]: float(v[2] or 0) for v in all_calc_variants}
            calc_var_names = list(calc_var_dict.keys())

            with col_eb3:
                if "ded_emi_variant" not in st.session_state or st.session_state["ded_emi_variant"] not in calc_var_names:
                    prefill_v = st.session_state.get("spec_variant")
                    st.session_state["ded_emi_variant"] = prefill_v if (prefill_v and prefill_v in calc_var_names) else (calc_var_names[0] if calc_var_names else None)
                sel_eb_variant = st.selectbox("Trim Variant", calc_var_names, key="ded_emi_variant")

        car_calc_price = calc_var_dict.get(sel_eb_variant, 5000000.0)

        col_fin1, col_fin2 = st.columns([1.1, 1])
        with col_fin1:
            with st.container(border=True):
                st.subheader("Financing Controls")
                st.write(f"**Selected Vehicle:** {sel_eb_brand} {sel_eb_model} ({sel_eb_variant})")
                st.write(f"**Ex-Showroom Price:** ₹ {car_calc_price:,.2f}")

                dp_pct = st.slider("Down Payment Percentage (%)", min_value=10, max_value=80, value=20, step=5, key="ded_calc_dp_pct")
                dp_val = car_calc_price * (dp_pct / 100.0)
                st.write(f"**Down Payment Capital:** ₹ {dp_val:,.2f}")

                loan_years = st.slider("Loan Tenure (Years)", min_value=1, max_value=7, value=5, step=1, key="ded_calc_tenure_yrs")
                st.write(f"**Tenure Duration:** {loan_years * 12} Monthly Installments")

                apr_rate = st.slider("Annual Interest Rate (%)", min_value=7.0, max_value=15.0, value=8.5, step=0.25, key="ded_calc_apr_rate")
                st.write(f"**Annual Interest Rate:** {apr_rate:.2f}% APR")

        # EMI Math
        net_principal = car_calc_price - dp_val
        total_months = loan_years * 12
        r_mo = (apr_rate / 100.0) / 12.0

        if r_mo > 0 and total_months > 0:
            emi_result = net_principal * r_mo * ((1 + r_mo) ** total_months) / (((1 + r_mo) ** total_months) - 1)
        else:
            emi_result = net_principal / total_months if total_months else 0

        gross_repay = emi_result * total_months
        total_interest_cost = gross_repay - net_principal

        with col_fin2:
            with st.container(border=True):
                st.subheader("Amortisation & Monthly EMI")
                st.metric(
                    label="Estimated Monthly EMI",
                    value=f"₹ {emi_result:,.2f} / month",
                    delta=f"Principal: ₹ {net_principal:,.2f} | Total Interest: ₹ {total_interest_cost:,.2f}",
                    delta_color="off"
                )
                st.divider()
                st.write(f"**Net Financed Principal:** ₹ {net_principal:,.2f}")
                st.write(f"**Total Interest Payable:** ₹ {total_interest_cost:,.2f}")
                st.write(f"**Gross Total Repayment:** ₹ {gross_repay:,.2f}")

                df_ded_chart = pd.DataFrame({
                    "Capital Component": ["Down Payment", "Principal Loan", "Total Interest"],
                    "Amount (INR)": [dp_val, net_principal, total_interest_cost]
                }).set_index("Capital Component")
                st.bar_chart(df_ded_chart)

    # ------------------ TAB 4: COMPARE CARS (FEATURE 1) ------------------
    with tab4:
        st.subheader("Compare Cars")
        st.caption("Select two different vehicles to compare side-by-side specs, visual profiles, and performance differentials.")

        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brand_list = [b[0] for b in cursor.fetchall()]

        with st.container(border=True):
            col_ca1, col_ca2 = st.columns(2)
            with col_ca1:
                st.write("#### Car A (Reference Vehicle)")
                if "cmp_tab_a_brand" not in st.session_state or st.session_state["cmp_tab_a_brand"] not in brand_list:
                    st.session_state["cmp_tab_a_brand"] = brand_list[0] if brand_list else None
                c_a_brand = st.selectbox("Brand (A)", brand_list, key="cmp_tab_a_brand")
                cursor.execute("""
                    SELECT model_name FROM models m
                    JOIN brands b ON m.brand_id = b.brand_id
                    WHERE b.brand_name = %s ORDER BY model_name
                """, (c_a_brand,))
                models_a = [m[0] for m in cursor.fetchall()]
                if "cmp_tab_a_model" not in st.session_state or st.session_state["cmp_tab_a_model"] not in models_a:
                    st.session_state["cmp_tab_a_model"] = models_a[0] if models_a else None
                c_a_model = st.selectbox("Model (A)", models_a, key="cmp_tab_a_model")

                cursor.execute("""
                    SELECT v.variant_name, v.price_inr, v.engine, v.power_bhp, v.torque_nm,
                           v.top_speed_kmh, v.acceleration_0_100, v.transmission, v.drivetrain,
                           v.fuel_type, v.mileage_range, v.seating_capacity, v.safety_rating
                    FROM variants v
                    JOIN models m ON v.model_id = m.model_id
                    JOIN brands b ON m.brand_id = b.brand_id
                    WHERE b.brand_name = %s AND m.model_name = %s
                    ORDER BY v.variant_name
                """, (c_a_brand, c_a_model))
                vars_a = cursor.fetchall()
                v_a_names = [v[0] for v in vars_a]
                if "cmp_tab_a_variant" not in st.session_state or st.session_state["cmp_tab_a_variant"] not in v_a_names:
                    st.session_state["cmp_tab_a_variant"] = v_a_names[0] if v_a_names else None
                c_a_var = st.selectbox("Variant (A)", v_a_names, key="cmp_tab_a_variant")
                car_a_data = next((v for v in vars_a if v[0] == c_a_var), None)

            with col_ca2:
                st.write("#### Car B (Comparison Vehicle)")
                b_default_idx = min(1, len(brand_list) - 1)
                if "cmp_tab_b_brand" not in st.session_state or st.session_state["cmp_tab_b_brand"] not in brand_list:
                    st.session_state["cmp_tab_b_brand"] = brand_list[b_default_idx] if brand_list else None
                c_b_brand = st.selectbox("Brand (B)", brand_list, key="cmp_tab_b_brand")
                cursor.execute("""
                    SELECT model_name FROM models m
                    JOIN brands b ON m.brand_id = b.brand_id
                    WHERE b.brand_name = %s ORDER BY model_name
                """, (c_b_brand,))
                models_b = [m[0] for m in cursor.fetchall()]
                if "cmp_tab_b_model" not in st.session_state or st.session_state["cmp_tab_b_model"] not in models_b:
                    st.session_state["cmp_tab_b_model"] = models_b[0] if models_b else None
                c_b_model = st.selectbox("Model (B)", models_b, key="cmp_tab_b_model")

                cursor.execute("""
                    SELECT v.variant_name, v.price_inr, v.engine, v.power_bhp, v.torque_nm,
                       v.top_speed_kmh, v.acceleration_0_100, v.transmission, v.drivetrain,
                       v.fuel_type, v.mileage_range, v.seating_capacity, v.safety_rating
                    FROM variants v
                    JOIN models m ON v.model_id = m.model_id
                    JOIN brands b ON m.brand_id = b.brand_id
                    WHERE b.brand_name = %s AND m.model_name = %s
                    ORDER BY v.variant_name
                """, (c_b_brand, c_b_model))
                vars_b = cursor.fetchall()
                v_b_names = [v[0] for v in vars_b]
                if "cmp_tab_b_variant" not in st.session_state or st.session_state["cmp_tab_b_variant"] not in v_b_names:
                    st.session_state["cmp_tab_b_variant"] = v_b_names[0] if v_b_names else None
                c_b_var = st.selectbox("Variant (B)", v_b_names, key="cmp_tab_b_variant")
                car_b_data = next((v for v in vars_b if v[0] == c_b_var), None)

        if car_a_data and car_b_data:
            st.divider()

            # Side-by-side images using st.columns(2)
            col_img_a, col_img_b = st.columns(2)
            with col_img_a:
                with st.container(border=True):
                    img_a = get_car_image(c_a_brand, c_a_model)
                    st.image(img_a, caption=f"Car A: {c_a_brand} {c_a_model} ({c_a_var})", use_container_width=True)
                    st.subheader(f"{c_a_brand} {c_a_model}")
                    st.caption(f"Trim: {c_a_var}")
                    st.write(f"### ₹ {car_a_data[1]:,.2f}")
                    st.write(f"**Powertrain:** {car_a_data[9]} | {car_a_data[7]}")

            with col_img_b:
                with st.container(border=True):
                    img_b = get_car_image(c_b_brand, c_b_model)
                    st.image(img_b, caption=f"Car B: {c_b_brand} {c_b_model} ({c_b_var})", use_container_width=True)
                    st.subheader(f"{c_b_brand} {c_b_model}")
                    st.caption(f"Trim: {c_b_var}")
                    st.write(f"### ₹ {car_b_data[1]:,.2f}")
                    st.write(f"**Powertrain:** {car_b_data[9]} | {car_b_data[7]}")

            st.divider()
            st.subheader("Performance Specification Differentials (Car B vs Car A)")

            # Objective 3 Feature 1: Use st.metric() with delta parameter to compare specs visually
            # E.g. If Car A has 500 BHP and Car B has 400 BHP, show Car B's power with red "-100 BHP" delta
            delta_bhp = (car_b_data[3] or 0) - (car_a_data[3] or 0)
            delta_torque = (car_b_data[4] or 0) - (car_a_data[4] or 0)
            delta_accel = (car_b_data[6] or 0) - (car_a_data[6] or 0)
            delta_top = (car_b_data[5] or 0) - (car_a_data[5] or 0)
            delta_price = (car_b_data[1] or 0) - (car_a_data[1] or 0)

            with st.container(border=True):
                m_c1, m_c2, m_c3, m_c4, m_c5 = st.columns(5)
                with m_c1:
                    st.metric(
                        label="Power Output",
                        value=f"{car_b_data[3]} BHP",
                        delta=f"{delta_bhp:+d} BHP" if delta_bhp != 0 else "Equal to Car A"
                    )
                with m_c2:
                    st.metric(
                        label="Peak Torque",
                        value=f"{car_b_data[4]} Nm",
                        delta=f"{delta_torque:+d} Nm" if delta_torque != 0 else "Equal to Car A"
                    )
                with m_c3:
                    st.metric(
                        label="0-100 km/h Sprint",
                        value=f"{car_b_data[6]} s",
                        delta=f"{delta_accel:+.2f} s" if delta_accel != 0 else "Equal to Car A",
                        delta_color="inverse"
                    )
                with m_c4:
                    st.metric(
                        label="Top Speed",
                        value=f"{car_b_data[5]} km/h",
                        delta=f"{delta_top:+d} km/h" if delta_top != 0 else "Equal to Car A"
                    )
                with m_c5:
                    st.metric(
                        label="Ex-Showroom Price",
                        value=f"₹ {car_b_data[1]:,.0f}",
                        delta=f"₹ {delta_price:+,.0f}",
                        delta_color="off"
                    )

            st.subheader("Side-by-Side Detailed Technical Matrix")
            cmp_matrix = [
                {"Parameter": "Manufacturer", f"Car A: {c_a_brand} {c_a_model}": c_a_brand, f"Car B: {c_b_brand} {c_b_model}": c_b_brand},
                {"Parameter": "Trim Variant", f"Car A: {c_a_brand} {c_a_model}": c_a_var, f"Car B: {c_b_brand} {c_b_model}": c_b_var},
                {"Parameter": "Ex-Showroom Price", f"Car A: {c_a_brand} {c_a_model}": f"₹ {car_a_data[1]:,.2f}", f"Car B: {c_b_brand} {c_b_model}": f"₹ {car_b_data[1]:,.2f}"},
                {"Parameter": "Engine Configuration", f"Car A: {c_a_brand} {c_a_model}": car_a_data[2], f"Car B: {c_b_brand} {c_b_model}": car_b_data[2]},
                {"Parameter": "Peak Power Output", f"Car A: {c_a_brand} {c_a_model}": f"{car_a_data[3]} BHP", f"Car B: {c_b_brand} {c_b_model}": f"{car_b_data[3]} BHP"},
                {"Parameter": "Peak Torque Output", f"Car A: {c_a_brand} {c_a_model}": f"{car_a_data[4]} Nm", f"Car B: {c_b_brand} {c_b_model}": f"{car_b_data[4]} Nm"},
                {"Parameter": "Top Speed", f"Car A: {c_a_brand} {c_a_model}": f"{car_a_data[5]} km/h", f"Car B: {c_b_brand} {c_b_model}": f"{car_b_data[5]} km/h"},
                {"Parameter": "0-100 km/h Sprint", f"Car A: {c_a_brand} {c_a_model}": f"{car_a_data[6]} s", f"Car B: {c_b_brand} {c_b_model}": f"{car_b_data[6]} s"},
                {"Parameter": "Transmission", f"Car A: {c_a_brand} {c_a_model}": car_a_data[7], f"Car B: {c_b_brand} {c_b_model}": car_b_data[7]},
                {"Parameter": "Drivetrain", f"Car A: {c_a_brand} {c_a_model}": car_a_data[8], f"Car B: {c_b_brand} {c_b_model}": car_b_data[8]},
                {"Parameter": "Powertrain Fuel", f"Car A: {c_a_brand} {c_a_model}": car_a_data[9], f"Car B: {c_b_brand} {c_b_model}": car_b_data[9]},
                {"Parameter": "Efficiency / Range", f"Car A: {c_a_brand} {c_a_model}": str(car_a_data[10]), f"Car B: {c_b_brand} {c_b_model}": str(car_b_data[10])},
                {"Parameter": "Seating Capacity", f"Car A: {c_a_brand} {c_a_model}": f"{car_a_data[11]} Seats", f"Car B: {c_b_brand} {c_b_model}": f"{car_b_data[11]} Seats"},
                {"Parameter": "Safety Rating", f"Car A: {c_a_brand} {c_a_model}": str(car_a_data[12]), f"Car B: {c_b_brand} {c_b_model}": str(car_b_data[12])}
            ]
            st.dataframe(pd.DataFrame(cmp_matrix), use_container_width=True, hide_index=True)

    # ------------------ TAB 5: BOOK A CAR ------------------
    with tab5:
        st.subheader("Vehicle Reservation & On-Road Calculator")
        st.caption("Calculate accurate on-road capital requirements, loan EMI schedules, and book directly.")

        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        all_brands = [b[0] for b in cursor.fetchall()]

        with st.container(border=True):
            col_b1, col_b2, col_b3 = st.columns(3)

            with col_b1:
                if "book_brand" not in st.session_state or st.session_state["book_brand"] not in all_brands:
                    prefill_b = st.session_state.get("prefill_brand")
                    st.session_state["book_brand"] = prefill_b if (prefill_b and prefill_b in all_brands) else (all_brands[0] if all_brands else None)
                booking_brand = st.selectbox("1. Manufacturer *", all_brands, key="book_brand")

            cursor.execute("""
                SELECT model_name FROM models m
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s ORDER BY model_name
            """, (booking_brand,))
            model_options = [m[0] for m in cursor.fetchall()]

            with col_b2:
                if "book_model" not in st.session_state or st.session_state["book_model"] not in model_options:
                    prefill_m = st.session_state.get("prefill_model")
                    st.session_state["book_model"] = prefill_m if (prefill_m and prefill_m in model_options) else (model_options[0] if model_options else None)
                booking_model = st.selectbox("2. Model Line *", model_options, key="book_model")

            cursor.execute("""
                SELECT v.variant_id, v.variant_name, v.price_inr, v.engine, v.power_bhp, v.fuel_type, v.transmission
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s
                ORDER BY v.variant_name
            """, (booking_brand, booking_model))
            variant_records = cursor.fetchall()
            variant_dict = {v[1]: v for v in variant_records}
            variant_options = list(variant_dict.keys())

            with col_b3:
                if "book_variant" not in st.session_state or st.session_state["book_variant"] not in variant_options:
                    prefill_v = st.session_state.get("prefill_variant")
                    st.session_state["book_variant"] = prefill_v if (prefill_v and prefill_v in variant_options) else (variant_options[0] if variant_options else None)
                booking_variant = st.selectbox("3. Trim Variant *", variant_options, key="book_variant")

        selected_variant_record = variant_dict.get(booking_variant)

        if selected_variant_record:
            b_variant_id, _, b_price, b_engine, b_power, b_fuel, b_trans = selected_variant_record
            raw_price = float(b_price or 0)

            # Indian tax breakdown
            rto_tax = raw_price * 0.10
            insurance = raw_price * 0.035
            tcs = (raw_price * 0.01) if raw_price > 1000000 else 0
            on_road_total = raw_price + rto_tax + insurance + tcs

            st.divider()
            col_calc, col_form = st.columns([1.1, 1.2])

            with col_calc:
                with st.container(border=True):
                    st.subheader("On-Road Cost Breakdown")
                    st.write(f"**Base Ex-Showroom:** ₹ {raw_price:,.2f}")
                    st.write(f"**RTO Registration (10.0%):** ₹ {rto_tax:,.2f}")
                    st.write(f"**Comprehensive Insurance (3.5%):** ₹ {insurance:,.2f}")
                    if tcs > 0:
                        st.write(f"**TCS Section 206C (1.0%):** ₹ {tcs:,.2f}")
                    st.metric("Estimated On-Road Total", f"₹ {on_road_total:,.2f}")

                    st.divider()
                    st.subheader("Loan EMI Calculator")
                    book_dp_pct = st.slider("Down Payment (%)", min_value=10, max_value=80, value=20, step=5, key="book_calc_dp_pct")
                    book_dp_amt = on_road_total * (book_dp_pct / 100.0)
                    book_loan_principal = on_road_total - book_dp_amt

                    book_tenure_yrs = st.selectbox("Tenure Duration", [1, 2, 3, 4, 5, 6, 7], index=4, format_func=lambda y: f"{y} Years ({y*12} Months)", key="book_calc_tenure")
                    book_tenure_months = book_tenure_yrs * 12
                    book_apr_rate = st.slider("Annual Interest Rate (%)", min_value=7.0, max_value=15.0, value=8.5, step=0.25, key="book_calc_apr")

                    book_mo_r = (book_apr_rate / 100.0) / 12.0
                    if book_mo_r > 0 and book_tenure_months > 0:
                        book_monthly_emi = book_loan_principal * book_mo_r * ((1 + book_mo_r) ** book_tenure_months) / (((1 + book_mo_r) ** book_tenure_months) - 1)
                    else:
                        book_monthly_emi = book_loan_principal / book_tenure_months if book_tenure_months else 0

                    book_total_payment = book_monthly_emi * book_tenure_months
                    book_total_interest = book_total_payment - book_loan_principal

                    st.metric(
                        label="Estimated Monthly EMI",
                        value=f"₹ {book_monthly_emi:,.2f} / mo",
                        delta=f"Total Interest: ₹ {book_total_interest:,.2f}",
                        delta_color="off"
                    )

                    df_book_emi = pd.DataFrame({
                        "Component": ["Principal Debt", "Total Interest"],
                        "Amount (INR)": [book_loan_principal, book_total_interest]
                    }).set_index("Component")
                    st.bar_chart(df_book_emi)

            with col_form:
                with st.container(border=True):
                    with st.form("customer_reservation_form"):
                        st.subheader("Customer Contact Information")
                        c_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
                        c_contact = st.text_input("Phone Number *", placeholder="e.g. +91 98765 43210")
                        c_email = st.text_input("Email Address *", placeholder="e.g. rahul.sharma@example.com")
                        c_city = st.selectbox("Preferred Dealership Location", [
                            "Mumbai Flagship Centre",
                            "Delhi NCR Hub",
                            "Bengaluru Tech City Showroom",
                            "Hyderabad Jubilee Hills",
                            "Chennai Mount Road",
                            "Pune Koregaon Park",
                            "Kolkata Park Street",
                            "Ahmedabad SG Highway"
                        ])
                        c_date = st.date_input("Preferred Delivery Date")
                        c_notes = st.text_area("Special Requests / Delivery Notes", placeholder="e.g. Requesting carbon package", height=70)

                        submit_booking = st.form_submit_button("Confirm Booking", type="primary", use_container_width=True)

                        if submit_booking:
                            if not c_name or len(c_name.strip()) < 2:
                                st.error("Validation Error: Full Name must contain at least 2 characters.")
                            elif not c_contact or len(c_contact.strip()) < 7:
                                st.error("Validation Error: Phone Number is malformed.")
                            elif not c_email or "@" not in c_email or "." not in c_email:
                                st.error("Validation Error: Email address format is invalid.")
                            else:
                                booking_id = generate_booking_id()
                                tx_uuid = str(uuid.uuid4())
                                contact_combined = f"{c_contact.strip()} ({c_city})"
                                email_combined = f"{c_email.strip()} | Date: {c_date}"
                                if c_notes.strip():
                                    email_combined += f" | Notes: {c_notes.strip()}"

                                checksum = hashlib.sha256(f"{booking_id}_{b_variant_id}_{c_email.strip()}".encode()).hexdigest()

                                try:
                                    cursor.execute("""
                                        INSERT INTO bookings (booking_id, variant_id, customer_name, customer_contact, customer_email, status)
                                        VALUES (%s, %s, %s, %s, %s, 'Active')
                                    """, (booking_id, b_variant_id, c_name.strip(), contact_combined, email_combined))
                                    conn.commit()

                                    st.session_state["confirmed_voucher"] = {
                                        "id": booking_id,
                                        "uuid": tx_uuid,
                                        "checksum": checksum,
                                        "name": c_name.strip(),
                                        "contact": c_contact.strip(),
                                        "email": c_email.strip(),
                                        "city": c_city,
                                        "date": str(c_date),
                                        "brand": booking_brand,
                                        "model": booking_model,
                                        "variant": booking_variant,
                                        "price": b_price,
                                        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                                    }
                                    st.success(f"Booking Confirmed. Reference: {booking_id}")
                                except Exception as e:
                                    st.error(f"Database Write Failure: {e}")

            if "confirmed_voucher" in st.session_state:
                vch = st.session_state["confirmed_voucher"]
                with st.container(border=True):
                    st.subheader("Vehicle Reservation Confirmation")
                    st.caption(f"Reference ID: {vch['id']} | Status: Active | Timestamp: {vch['timestamp_utc']}")
                    st.divider()
                    vc1, vc2 = st.columns(2)
                    with vc1:
                        st.write("**Vehicle Reserved:**")
                        st.write(f"### {vch['brand']} {vch['model']}")
                        st.write(f"**Trim:** {vch['variant']}")
                        st.write(f"**Ex-Showroom Price:** ₹ {vch['price']:,.2f}")
                    with vc2:
                        st.write("**Customer Information:**")
                        st.write(f"**Name:** {vch['name']}")
                        st.write(f"**Contact:** {vch['contact']}")
                        st.write(f"**Email:** {vch['email']}")
                        st.write(f"**Dealership Centre:** {vch['city']}")
                    st.caption(f"UUID: {vch['uuid']} | SHA256: {vch['checksum']}")


# ==============================================================================
# ADMIN MODE (WITH ADMIN ANALYTICS DASHBOARD - FEATURE 2)
# ==============================================================================
elif mode == "Admin Mode":
    st.title("AutoSpec Administration Console")
    st.caption("Manage customer bookings, review visual analytics, audit database records, and monitor cloud architecture.")
    st.divider()

    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        col_l1, col_l2 = st.columns([1, 1])
        with col_l1:
            with st.container(border=True):
                st.subheader("Administrative Authentication")
                st.caption("Enter administrative master password to access records.")
                admin_pw = st.text_input("Master Password", type="password")
                if st.button("Unlock Dashboard", type="primary", use_container_width=True):
                    if admin_pw == ADMIN_PASSWORD:
                        st.session_state["admin_logged_in"] = True
                        st.rerun()
                    else:
                        st.error("Authentication Error: Invalid Master Password. Access Denied.")
    else:
        col_t1, col_t2 = st.columns([4, 1])
        with col_t2:
            if st.button("Log Out", type="secondary", use_container_width=True):
                st.session_state["admin_logged_in"] = False
                st.rerun()

        cursor.execute("SELECT COUNT(*) FROM bookings")
        total_bookings = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM brands")
        total_brands = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM models")
        total_models = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM variants")
        total_variants = cursor.fetchone()[0]

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            with st.container(border=True):
                st.metric("Total Reservations", total_bookings)
        with kpi2:
            with st.container(border=True):
                st.metric("Active Brands", total_brands)
        with kpi3:
            with st.container(border=True):
                st.metric("Vehicle Models", total_models)
        with kpi4:
            with st.container(border=True):
                st.metric("Variants Registered", total_variants)

        st.divider()

        admin_tab1, admin_tab2, admin_tab3 = st.tabs([
            "Customer Bookings",
            "Database Operations",
            "Cloud Deployment & Export"
        ])

        with admin_tab1:
            st.subheader("Customer Vehicle Bookings Audit")
            st.caption("Review active records, filter by transaction status, or export CSV audit files.")

            # Feature 2: Admin Analytics Dashboard (Admin Mode)
            # Above the booking DataFrame, add visual analytics section using native st.bar_chart() or st.line_chart()
            cursor.execute("""
                SELECT b.brand_name, COUNT(bk.booking_id) as booking_count
                FROM brands b
                JOIN models m ON b.brand_id = m.brand_id
                JOIN variants v ON m.model_id = v.model_id
                JOIN bookings bk ON v.variant_id = bk.variant_id
                GROUP BY b.brand_name
                ORDER BY booking_count DESC
            """)
            brand_analytics_rows = cursor.fetchall()

            cursor.execute("""
                SELECT DATE(bk.booking_date) as b_date, COUNT(*) as daily_count
                FROM bookings bk
                GROUP BY DATE(bk.booking_date)
                ORDER BY b_date ASC
            """)
            time_analytics_rows = cursor.fetchall()

            with st.container(border=True):
                st.subheader("Admin Visual Analytics Dashboard")
                st.caption("Executive overview of booking distribution across manufacturers and demand volume over time.")

                col_an1, col_an2 = st.columns(2)
                with col_an1:
                    st.write("#### Total Bookings per Brand")
                    if brand_analytics_rows:
                        df_brand_chart = pd.DataFrame(brand_analytics_rows, columns=["Brand", "Total Bookings"]).set_index("Brand")
                        st.bar_chart(df_brand_chart)
                    else:
                        st.info("No bookings recorded yet to populate brand chart.")

                with col_an2:
                    st.write("#### Bookings Timeline (Daily Volume)")
                    if time_analytics_rows:
                        df_time_chart = pd.DataFrame(time_analytics_rows, columns=["Date", "Bookings"]).set_index("Date")
                        st.line_chart(df_time_chart)
                    else:
                        st.info("No chronological transaction data available.")

            st.divider()

            # Booking DataFrame & Controls
            cursor.execute("""
                SELECT bk.booking_id, b.brand_name, m.model_name, v.variant_name,
                       bk.customer_name, bk.customer_contact, bk.customer_email,
                       bk.booking_date, bk.status
                FROM bookings bk
                JOIN variants v ON bk.variant_id = v.variant_id
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                ORDER BY bk.booking_date DESC
            """)
            books = cursor.fetchall()

            if books:
                df_books = pd.DataFrame(books, columns=[
                    "Booking ID", "Brand", "Model", "Variant",
                    "Customer Name", "Contact", "Email / Notes", "Date", "Status"
                ])

                col_f1, col_f2 = st.columns([1, 2])
                with col_f1:
                    status_filter = st.selectbox("Filter Status", ["All", "Active", "Confirmed", "Delivered", "Cancelled"])
                with col_f2:
                    search_cust = st.text_input("Search (Customer Name / Booking ID)", placeholder="Search customer name or reference ID...")

                filtered_df = df_books
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df["Status"] == status_filter]
                if search_cust.strip():
                    term = search_cust.strip().lower()
                    filtered_df = filtered_df[
                        filtered_df["Customer Name"].str.lower().str.contains(term) |
                        filtered_df["Booking ID"].str.lower().str.contains(term)
                    ]

                st.dataframe(filtered_df, use_container_width=True, hide_index=True)

                col_down, col_upd = st.columns([1, 1])
                with col_down:
                    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Export Bookings (CSV)",
                        data=csv_data,
                        file_name=f"autospec_bookings_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )

                with col_upd:
                    with st.expander("Update Transaction State"):
                        all_ids = df_books["Booking ID"].tolist()
                        sel_id = st.selectbox("Select Target ID", all_ids)
                        new_st = st.selectbox("Transition To", ["Active", "Confirmed", "Delivered", "Cancelled"])
                        if st.button("Commit State Change"):
                            cursor.execute("UPDATE bookings SET status = %s WHERE booking_id = %s", (new_st, sel_id))
                            conn.commit()
                            st.success(f"State transitioned for {sel_id} to {new_st}.")
                            st.rerun()
            else:
                st.info("No booking records currently committed. Create a test transaction in User Mode.")

        with admin_tab2:
            st.subheader("Database Operations & Integrity")
            st.caption("Administrative reset routine to purge existing tables and reload curated production datasets with strict crosschecking.")

            with st.container(border=True):
                st.warning("Warning: Resetting the database drops all booking logs and repopulates the factory dataset.")
                confirm_reset = st.checkbox("Acknowledge permanent table reset and re-seed.")
                if st.button("Execute Factory Reset", disabled=not confirm_reset):
                    try:
                        cursor.execute("DELETE FROM bookings")
                        cursor.execute("DELETE FROM features")
                        cursor.execute("DELETE FROM colors")
                        cursor.execute("DELETE FROM variants")
                        cursor.execute("DELETE FROM models")
                        cursor.execute("DELETE FROM brands")
                        conn.commit()
                        insert_sample_data(cursor, conn)
                        st.success("Database Purged and Re-seeded with Full Crosschecking Successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Execution Error: {e}")

        with admin_tab3:
            st.subheader("Cloud Infrastructure & Migration")
            st.caption("Deployment parameters, live socket benchmarks, and full relational export.")

            col_inf1, col_inf2 = st.columns(2)
            with col_inf1:
                with st.container(border=True):
                    st.subheader("Active Socket Telemetry")
                    st.write(f"**Connection Mode:** `{db_source}`")
                    st.write(f"**Host Endpoint:** `{db_cfg.get('host')}`")
                    st.write(f"**Port:** `{db_cfg.get('port')}`")
                    st.write(f"**Database Schema:** `{db_cfg.get('database')}`")
                    st.write(f"**Authenticated User:** `{db_cfg.get('user')}`")

                    if st.button("Benchmark Socket Ping"):
                        t_ping = time.time()
                        cursor.execute("SELECT 1")
                        cursor.fetchall()
                        ping_ms = (time.time() - t_ping) * 1000
                        st.success(f"Socket healthy: {ping_ms:.2f} ms roundtrip.")

            with col_inf2:
                with st.container(border=True):
                    st.subheader("Database SQL Backup")
                    st.write("Generate a deterministic SQL file containing DDL schema definitions and complete INSERT rows.")

                    sql_dump = generate_sql_dump(cursor)
                    st.download_button(
                        label="Download Relational Dump (.sql)",
                        data=sql_dump,
                        file_name=f"autospec_relational_backup_{datetime.now().strftime('%Y%m%d')}.sql",
                        mime="application/sql",
                        type="primary",
                        use_container_width=True
                    )
                    st.caption("Compatible with MySQL 8.0, TiDB Serverless, and AWS RDS.")

            st.divider()
            st.subheader("Cloud Migration Specification")
            st.markdown("""
            1. **Provision MySQL Cluster**: Deploy serverless instance on TiDB Cloud or AWS RDS.
            2. **Apply DDL & Seed**: Execute the downloaded `.sql` file in the database console.
            3. **Bind Secrets**: Update `.streamlit/secrets.toml` or Streamlit Community Cloud environment:
            ```toml
            [mysql]
            host = "your-cluster-endpoint.com"
            port = 4000
            user = "your_user"
            password = "your_password"
            database = "AutoSpec_Database_System"
            ssl_verify_cert = true
            ```
            4. **Production Deploy**: Link GitHub repository to share.streamlit.io.
            """)

# Gracefully close connections
try:
    cursor.close()
    conn.close()
except Exception:
    pass
