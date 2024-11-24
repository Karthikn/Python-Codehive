
# Configuration Manager and API 

This project provides a comprehensive solution for managing application configurations. It parses configuration files, stores them in a SQLite database, and serves them via a RESTful Flask API. The implementation ensures secure handling of sensitive data, supports multiple configuration sections, and enables retrieval of the latest configurations.

## Features

1. **Configuration Parsing**
   - Reads configurations from an INI file using `ConfigParser`.
   - Converts configurations into a dictionary format for processing.

2. **Database Management**
   - Stores configurations in a SQLite database.
   - Automatically handles database setup with schema creation.

3. **Flask REST API**
   - Provides endpoints for retrieving the latest configurations.
   - Supports querying specific sections of the configuration.

4. **Secure Data Handling**
   - Masks sensitive fields like passwords when displaying configurations.

## File Structure

- **`config.ini`**: Input configuration file in INI format (to be created by the user).
- **`config.db`**: SQLite database file for storing configurations.
- **`app.py`**: Main application file containing the Configuration Manager and API logic.

## Usage

### Prerequisites
- Python 3.7 or above
- Required libraries: `flask`, `configparser` (standard library), `sqlite3` (standard library)

### Installation
1. Clone the repository or copy the code.
2. Install dependencies by running:
   ```bash
   pip install flask
   ```

### Configuration File
Create a `config.ini` file in the root directory. Example:
```ini
[database]
host = localhost
port = 5432
user = admin
password = secret

[app]
debug = true
port = 5000
```

### Running the Application
Run the application using:
```bash
python app.py
```

### API Endpoint
- **GET /config**: Retrieve the latest configuration.
  - Query Parameters: `section` (optional) to fetch a specific configuration section.

#### Example Requests
1. Retrieve all configurations:
   ```bash
   curl http://localhost:5000/config
   ```

2. Retrieve a specific section:
   ```bash
   curl http://localhost:5000/config?section=database
   ```

### Console Output
The application masks sensitive fields (like passwords) in the console logs for security purposes.

### Database Schema
The SQLite database uses the following schema:
- **`configurations`**
  - `id`: Auto-increment primary key.
  - `section`: Configuration section name (e.g., "database").
  - `config_data`: JSON-encoded configuration values.
  - `timestamp`: Timestamp of the configuration entry.

## Error Handling
- Handles missing configuration files with appropriate error messages.
- Provides detailed error responses via the API.

## Extensibility
- Additional endpoints can be added to the Flask app for enhanced functionality.
- Supports multiple configuration files by extending the `ConfigurationManager` class.

## Security Considerations
- Avoid exposing sensitive configurations like passwords in logs or API responses.
- Use a secure storage mechanism for production-grade applications.

## License
This project is open-source and can be freely modified or distributed under the MIT License.

---

### Author
This script was developed to provide an efficient way to manage and serve application configurations. Feedback and contributions are welcome.