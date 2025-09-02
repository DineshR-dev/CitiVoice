# CitiVoice - Citizen Feedback & Complaint Management System

CitiVoice is a Django-based web application designed to help citizens submit feedback and complaints to local authorities, track their status, and promote transparency in public issue resolution. This project was built to explore practical Django modeling, form handling, AJAX, and real-world web development concepts. The application follows a super simple, minimalist design without complex or overwhelming elements, making it easy for users to understand and use effectively.

## Features

- **User Registration & Login:** Citizens can sign up, log in, and manage their profiles.
- **Complaint Submission:** Users can submit complaints with title, description, and location.
- **Voting System:** Users can vote on complaints to highlight important issues.
- **Complaint Assignment:** Admins can take complaints and update their status (pending, active, completed).
- **Filtering & Pagination:** Complaints can be filtered by status and location; lists are paginated for usability.
- **AJAX Interactions:** Most actions (add, vote, update status) use AJAX for a smooth user experience.
- **Role-Based Access:** Admins have special permissions to manage complaints and locations.
- **Responsive UI:** Built with Bootstrap for mobile-friendly design.

## Technologies Used

- **Backend:** Django, Django ORM
- **Frontend:** HTML, CSS (Bootstrap), JavaScript (jQuery, AJAX)
- **Database:** SQLite (default, can be changed)
- **Other:** Font Awesome, Bootstrap Icons, jQuery UI (via CDN)

## How It Works

- **Citizens:** Register, log in, submit complaints, vote on issues, and track complaint status.
- **Admins:** Assign themselves to complaints, update status, and manage locations.
- **Transparency:** All users can view complaint records and see which issues are being addressed.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DineshR-dev/CitiVoice.git
   cd citizen_feedback
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the app:**  
   Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Folder Structure

- `citizen_feedback/` - Django project settings and configuration
- `frontend/` - Templates, static files, and user-facing views
- `complaints/` - Models, forms, and logic for complaints
- `core/` - Location and admin mapping models
- `users/` - User profile and authentication logic

## Screenshots

![Home Page](https://github.com/user-attachments/assets/4e9ce2a8-fb02-4187-9d5c-1f18f05652b0)
*Example of the CitiVoice's Home page contains all complaints of current month* 

![Profile Page](https://github.com/user-attachments/assets/8057b903-d61f-4f13-8c64-e6226aab88cc)
*Example of the CitiVoice's profile page*

![Complaint Page](https://github.com/user-attachments/assets/69c6704d-f83f-4353-a2f5-4d247e7ce6ff)
*Example of the CitiVoice's Complaint Page we can see full deatils of complaint*

![Complaint record Page](https://github.com/user-attachments/assets/ac0d9a93-0e22-477d-b253-2a03537fc951)
*Example of the CitiVoice's Complaint record page contains all taken Complaints*

## License

This project is for educational and demonstration purposes.

---

**Built for learning Django and practical web development.**
