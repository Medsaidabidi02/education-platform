# Education Platform

A comprehensive education platform with secure video streaming, user authentication, plan-based access control, and admin approval system.

## 🚀 Features

### Security & Authentication
- **JWT Authentication** with device tracking
- **Session Management** with single-device enforcement
- **Admin Approval System** for new user accounts
- **Device Fingerprinting** for enhanced security
- **Protected Video Streaming** with signed URLs

### Course Management
- **Plan-based Access Control** for premium content
- **Video Progress Tracking** with completion status
- **Course Reviews & Ratings** with moderation system
- **Multi-level Course Difficulty** (Beginner, Intermediate, Advanced)
- **Course Categories** and tagging system

### Video Security
- **Encrypted Video URLs** with expiration
- **Download Protection** with configurable settings
- **Quality Control** (480p, 720p, 1080p, 4K)
- **Access Logging** for security auditing

### User Experience
- **Responsive Design** with Tailwind CSS
- **Real-time Notifications** using React Hot Toast
- **Progress Analytics** and completion certificates
- **Review System** with helpfulness voting

## 🛠 Tech Stack

### Backend
- **Django 5.2.5** with Django REST Framework
- **PostgreSQL** database
- **JWT Authentication** with Simple JWT
- **CORS** enabled for frontend integration
- **Python Decouple** for environment management

### Frontend
- **Next.js 15** with TypeScript
- **Tailwind CSS** for styling
- **Axios** for API communication
- **React Hook Form** for form validation
- **Lucide React** for icons

### DevOps
- **Docker & Docker Compose** for containerization
- **PostgreSQL 15** in Alpine container
- **Multi-stage Docker builds** for optimization

## 📁 Project Structure

```
education-platform/
├── backend/                    # Django backend
│   ├── education_backend/      # Main Django project
│   ├── users/                  # User management app
│   ├── courses/                # Course management app
│   ├── videos/                 # Video streaming app
│   ├── reviews/                # Review system app
│   ├── plans/                  # Subscription plans app
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment template
│   ├── Dockerfile             # Backend container config
│   └── manage.py              # Django management script
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js app router pages
│   │   ├── components/        # Reusable React components
│   │   ├── contexts/          # React context providers
│   │   ├── lib/               # Utility libraries
│   │   └── types/             # TypeScript type definitions
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── .env.local.example     # Frontend environment template
│   ├── Dockerfile             # Frontend container config
│   └── next.config.ts         # Next.js configuration
├── docker-compose.yml         # Multi-container setup
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚦 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Medsaidabidi02/education-platform.git
   cd education-platform
   ```

2. **Set up environment variables**
   ```bash
   # Backend environment
   cp backend/.env.example backend/.env
   
   # Frontend environment  
   cp frontend/.env.local.example frontend/.env.local
   ```

3. **Update environment variables**
   Edit `backend/.env` and `frontend/.env.local` with your configuration.

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin

### Manual Setup (Without Docker)

#### Backend Setup

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb education_platform
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/profile/` | Get user profile |
| PATCH | `/api/auth/profile/` | Update user profile |
| POST | `/api/auth/password/change/` | Change password |
| GET | `/api/auth/sessions/` | List user sessions |
| POST | `/api/auth/sessions/{id}/terminate/` | Terminate session |

### Course Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | List courses |
| GET | `/api/courses/{id}/` | Course details |
| POST | `/api/courses/{id}/enroll/` | Enroll in course |
| GET | `/api/courses/{id}/videos/` | Course videos |

### Video Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/videos/{id}/stream/` | Secure video stream |
| POST | `/api/videos/{id}/progress/` | Update progress |
| GET | `/api/videos/{id}/progress/` | Get progress |

### Review Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviews/` | List reviews |
| POST | `/api/reviews/` | Create review |
| PATCH | `/api/reviews/{id}/` | Update review |
| DELETE | `/api/reviews/{id}/` | Delete review |

### Plan Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/plans/` | List subscription plans |
| GET | `/api/plans/{id}/` | Plan details |
| POST | `/api/plans/{id}/subscribe/` | Subscribe to plan |

## 🔐 Security Features

### Device Management
- Maximum device limits per user
- Device fingerprinting for identification
- Session termination on device conflicts

### Video Protection
- Signed URLs with expiration
- IP-based access control
- Download prevention measures
- Encrypted video streaming

### User Security
- Admin approval for new accounts
- Password validation and hashing
- Session timeout management
- Role-based access control

## 🎯 Admin Features

### User Management
- Approve/reject new user accounts
- Monitor user sessions and devices
- Role assignment (Student, Instructor, Admin)
- Activity tracking and analytics

### Content Moderation
- Review approval/rejection system
- Course content management
- Video upload and processing
- Quality control and monitoring

## 📱 Frontend Pages

### Public Pages
- **Landing Page** - Hero section with platform features
- **Login Page** - User authentication
- **Register Page** - Account creation
- **Plans Page** - Subscription plan selection

### Protected Pages
- **Dashboard** - User overview and progress
- **Courses** - Course browsing and enrollment
- **Course Detail** - Video player and course content
- **Profile** - User settings and information
- **Reviews** - Course feedback system

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 🚀 Deployment

### Production Environment Variables

Update your production environment files:

**Backend (.env)**
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DB_HOST=your-production-db-host
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_APP_NAME=Education Platform
```

### Docker Production Deployment
```bash
# Build and run in production mode
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial release with core features
  - User authentication and device management
  - Course and video management
  - Review system with moderation
  - Plan-based access control
  - Secure video streaming

---

**Built with ❤️ for education**