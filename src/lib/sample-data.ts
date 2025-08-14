import type { Course } from "@/types";

export const sampleCourses: Course[] = [
  {
    id: "1",
    title: "Complete React Developer Course",
    description: "Master React from basics to advanced concepts including hooks, context, and modern patterns",
    shortDescription: "Master React from basics to advanced concepts with hands-on projects",
    thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400&h=300&fit=crop",
    instructor: {
      id: "1",
      name: "Sarah Johnson",
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b593?w=100&h=100&fit=crop&crop=face"
    },
    price: 89.99,
    originalPrice: 129.99,
    duration: 720, // 12 hours
    level: "intermediate",
    category: "Frontend",
    tags: ["React", "JavaScript", "Web Development"],
    rating: 4.8,
    reviewCount: 2340,
    studentCount: 15420,
    lessons: [
      {
        id: "1",
        title: "Introduction to React",
        description: "Learn the basics of React and why it's so popular",
        duration: 30,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-01-15"),
    updatedAt: new Date("2024-08-01")
  },
  {
    id: "2",
    title: "Advanced Python Programming",
    description: "Deep dive into Python with advanced topics like decorators, metaclasses, and async programming",
    shortDescription: "Deep dive into advanced Python concepts and best practices",
    thumbnail: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=300&fit=crop",
    instructor: {
      id: "2",
      name: "Michael Chen",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face"
    },
    price: 79.99,
    duration: 960, // 16 hours
    level: "advanced",
    category: "Backend",
    tags: ["Python", "Programming", "Backend"],
    rating: 4.9,
    reviewCount: 1850,
    studentCount: 8920,
    lessons: [
      {
        id: "2",
        title: "Python Decorators Explained",
        description: "Understanding and implementing Python decorators",
        duration: 45,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-02-10"),
    updatedAt: new Date("2024-07-20")
  },
  {
    id: "3",
    title: "UI/UX Design Fundamentals",
    description: "Learn the principles of user interface and user experience design",
    shortDescription: "Master the fundamentals of modern UI/UX design",
    thumbnail: "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&h=300&fit=crop",
    instructor: {
      id: "3",
      name: "Emma Rodriguez",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face"
    },
    price: 69.99,
    originalPrice: 99.99,
    duration: 540, // 9 hours
    level: "beginner",
    category: "Design",
    tags: ["UI/UX", "Design", "Figma"],
    rating: 4.7,
    reviewCount: 3210,
    studentCount: 12340,
    lessons: [
      {
        id: "3",
        title: "Design Thinking Process",
        description: "Introduction to the design thinking methodology",
        duration: 25,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-03-05"),
    updatedAt: new Date("2024-08-10")
  },
  {
    id: "4",
    title: "Machine Learning with TensorFlow",
    description: "Build and deploy machine learning models using TensorFlow and Python",
    shortDescription: "Build ML models with TensorFlow from scratch to deployment",
    thumbnail: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400&h=300&fit=crop",
    instructor: {
      id: "4",
      name: "Dr. Alex Kumar",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face"
    },
    price: 149.99,
    duration: 1440, // 24 hours
    level: "advanced",
    category: "Data Science",
    tags: ["Machine Learning", "TensorFlow", "Python", "AI"],
    rating: 4.9,
    reviewCount: 980,
    studentCount: 4560,
    lessons: [
      {
        id: "4",
        title: "Introduction to Neural Networks",
        description: "Understanding the basics of neural networks",
        duration: 60,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-01-20"),
    updatedAt: new Date("2024-08-05")
  },
  {
    id: "5",
    title: "Digital Marketing Mastery",
    description: "Complete guide to digital marketing including SEO, social media, and paid advertising",
    shortDescription: "Complete digital marketing course covering all major channels",
    thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop",
    instructor: {
      id: "5",
      name: "Lisa Thompson",
      avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&h=100&fit=crop&crop=face"
    },
    price: 59.99,
    duration: 600, // 10 hours
    level: "beginner",
    category: "Marketing",
    tags: ["Digital Marketing", "SEO", "Social Media"],
    rating: 4.6,
    reviewCount: 2100,
    studentCount: 18750,
    lessons: [
      {
        id: "5",
        title: "Digital Marketing Fundamentals",
        description: "Overview of digital marketing landscape",
        duration: 35,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-02-28"),
    updatedAt: new Date("2024-07-15")
  },
  {
    id: "6",
    title: "Node.js Backend Development",
    description: "Build scalable backend applications with Node.js, Express, and MongoDB",
    shortDescription: "Build scalable backend APIs with Node.js and Express",
    thumbnail: "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400&h=300&fit=crop",
    instructor: {
      id: "6",
      name: "James Wilson",
      avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&h=100&fit=crop&crop=face"
    },
    price: 94.99,
    originalPrice: 119.99,
    duration: 840, // 14 hours
    level: "intermediate",
    category: "Backend",
    tags: ["Node.js", "Express", "MongoDB", "API"],
    rating: 4.8,
    reviewCount: 1640,
    studentCount: 9830,
    lessons: [
      {
        id: "6",
        title: "Setting up Node.js Environment",
        description: "Installing and configuring Node.js for development",
        duration: 20,
        type: "video",
        order: 1,
        isPreview: true
      }
    ],
    createdAt: new Date("2024-03-12"),
    updatedAt: new Date("2024-08-08")
  }
];