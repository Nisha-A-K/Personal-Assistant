# Personal Health & Schedule Assistant

A dynamic, web-based personal assistant designed to help users manage their daily schedule while proactively promoting mental and physical well-being. This application generates an intelligent daily schedule based on a user's profile and allows for real-time updates and conflict resolution with custom events.


---

## ✨ Core Features

-   **Personalized User Profiles:** Users can register a profile including their name, height, weight, and job type.
-   **Automated Daily Schedule Generation:** Creates a holistic daily schedule template with timings for:
    -   Morning and evening routines (wake up, meals, wind down).
    -   Work blocks based on user-defined office hours.
    -   Health reminders like drinking water.
    -   Job-specific activities (e.g., post-work recovery for active jobs, exercise for sedentary jobs).
    -   Meditation and family/relaxation time.
-   **Dynamic Conflict Resolution:** When a user adds a custom engagement with a specific duration (e.g., a meeting from 10:00 AM to 11:30 AM), the application automatically removes any generated template items that fall within that time block.
-   **Interactive Timeline UI:** The daily schedule is presented in a clean, modern, and easy-to-read timeline format with icons and color-coding for different activity types.
-   **In-Memory Data:** Simple and fast data handling for user profiles and events (data is reset on server restart).

## 🛠️ Technology Stack

-   **Backend:** Python 3 with the **Flask** micro-framework to create a RESTful API.
-   **Frontend:** Vanilla **HTML**, **CSS**, and **JavaScript (ES6+)**. No external frameworks are required.
-   **Communication:** The frontend communicates with the backend via asynchronous `fetch` API requests.

## 🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

### Prerequisites

-   Python 3.6 or higher
-   `pip` (Python package installer)
-   A web browser (Chrome, Firefox, Edge, etc.)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/personal-health-assistant.git
    cd personal-health-assistant
    ```

2.  **Install the required Python package (Flask):**
    ```bash
    pip install Flask
    ```
    This is the only dependency required for the backend.

## 🏃‍♀️ How to Run the Application

The application consists of two parts that must be running simultaneously: the backend server and the frontend in your browser.

1.  **Start the Backend Server:**
    Navigate to the project's root directory in your terminal and run the following command:
    ```bash
    python app.py
    ```
    You should see output indicating that the server is running on `http://127.0.0.1:5000`. Keep this terminal window open.

2.  **Open the Frontend:**
    Open your web browser and navigate to the following URL:
    ```
    http://1227.0.0.1:5000
    ```
    The Personal Health Assistant application should now be visible and fully interactive.

## 📋 How to Use the Application

1.  **Create Your Profile:** Fill in your name, height, weight, select a job type, and set your daily office start and end times.
2.  **Generate Your Schedule:** Click the **"Update Profile & Get Schedule"** button. Your personalized daily schedule will instantly appear in the timeline view.
3.  **Add a Custom Engagement:** If you have a specific meeting or appointment, add it using the "Add a Custom Engagement" form. Provide an event name and a "From" and "To" time.
4.  **Watch the Schedule Update:** After adding your engagement, the timeline will automatically refresh. Any generated health reminders that conflicted with your custom event will be removed to make space for it.
5.  **Delete Your Profile:** To clear all your data, enter your username and click the **"Delete Profile"** button.

## 🔮 Future Enhancements

This project has a solid foundation that can be extended with more features:

-   **Database Integration:** Replace the in-memory dictionaries with a persistent database like **SQLite** or **PostgreSQL** to save user data permanently.
-   **User Authentication:** Add a proper login and registration system so multiple users can securely save their own schedules.
-   **Browser Notifications:** Implement push notifications to remind users of upcoming schedule items (e.g., "Time to drink water!").
-   **Advanced Health Metrics:** Automatically calculate and display metrics like BMI in the user profile.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
