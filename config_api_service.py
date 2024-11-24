from configparser import ConfigParser
import json
from flask import Flask, jsonify, request
from pathlib import Path
import sqlite3
from typing import Dict, Optional


class ConfigurationManager:
    def __init__(self, config_file: str, db_file: str = "config.db"):
        self.config_file = config_file
        self.db_file = db_file
        self._setup_database()

    def _setup_database(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL,
                config_data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def parse_config(self) -> Dict:
        """Parse configuration file and return as dictionary."""
        if not Path(self.config_file).exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        config = ConfigParser()
        config.read(self.config_file)

        config_dict = {section: dict(config[section]) for section in config.sections()}
        return config_dict

    def save_to_database(self, config_data: Dict):
        """Save configuration data to SQLite database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        for section, data in config_data.items():
            cursor.execute(
                "INSERT INTO configurations (section, config_data) VALUES (?, ?)",
                (section, json.dumps(data))
            )

        conn.commit()
        conn.close()

    def get_latest_config(self, section: Optional[str] = None) -> Dict:
        """Retrieve the latest configuration from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        query = '''
            SELECT section, config_data
            FROM configurations c1
            WHERE timestamp = (
                SELECT MAX(timestamp)
                FROM configurations c2
                WHERE c2.section = c1.section
            )
        '''
        if section:
            query += " AND section = ?"
            cursor.execute(query, (section,))
        else:
            cursor.execute(query)

        result = {row[0]: json.loads(row[1]) for row in cursor.fetchall()}
        conn.close()
        return result


# Flask API
app = Flask(__name__)
config_manager = None


@app.route('/config', methods=['GET'])
def get_config():
    try:
        section = request.args.get('section')  # Optional query parameter
        config = config_manager.get_latest_config(section)
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    global config_manager
    config_file = "config.ini"

    try:
        # Initialize configuration manager
        config_manager = ConfigurationManager(config_file)

        # Parse and save configuration
        config_data = config_manager.parse_config()
        config_manager.save_to_database(config_data)

        # Display results in console
        print("Configuration File Parser Results:")
        for section, values in config_data.items():
            print(f"\n{section}:")
            for key, value in values.items():
                # Mask sensitive fields
                if key.lower() in ["password"]:
                    value = "******"
                print(f"- {key}: {value}")

        # Start API
        app.run(port=5000)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
