# Architecture Design Document for Flask Application in `app.py`

1. **Application Framework:**
   - **Framework Used:** Flask
   - **Description:** A lightweight WSGI web application framework.

2. **Database:**
   - **Database Used:** SQLite
   - **ORM:** SQLAlchemy
   - **Description:** A lightweight disk-based database that doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language.

3. **Security:**
   - **Password Hashing:** Flask-Bcrypt
   - **Rate Limiting:** Flask-Limiter
   - **Authentication:** JWT (JSON Web Tokens) with Flask-JWT-Extended
   - **Description:** Security measures include password hashing for secure password storage, rate limiting to prevent abuse of the APIs, and JWT for secure and scalable user authentication.

4. **API and Functionality:**
   - **Endpoints:** Endpoint Description
- **/register/** This endpoint should accept a username and password and create a new user
- **/login/** This endpoint should allow a user to exchange their credentials for an API key
- **/logout/** This endpoint should expire the API key
- **/shorten/** This endpoint should shorten a URI and accept an optional TTL
- **/x/{...}** This endpoint should expand a shortcode by serving a redirect to the original URI
  
- **Main Functionalities:** The application might include functionalities related to user authentication, data processing, and interactions with the SQLite database.

5. **Configuration:**
   - **Configuration Management:** Managed within the application, likely through Flask's app.config.

6. **Dependencies:**
   - Flask
   - Flask-SQLAlchemy
   - Flask-Bcrypt
   - Flask-Limiter
   - Flask-JWT-Extended
   - Others (based on the full contents of the file Requirements.txt)

7. **Data Flow:**
   - **Client-Server Interaction:** Clients interact with the server through API endpoints.
   - **Database Interaction:** The server interacts with the SQLite database using SQLAlchemy ORM for data storage and retrieval.

8. **Scalability and Performance:**
   - **Rate Limiting:** Helps to manage the load on the server.
   - **Stateless Authentication:** JWTs are stateless, which can help in scaling the application.

9. **Error Handling and Logging:**
   - Uses built in Docker logs
