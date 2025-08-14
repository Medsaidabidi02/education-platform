'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import toast from 'react-hot-toast';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  requiredRole?: 'student' | 'instructor' | 'admin';
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requireAuth = true,
  requiredRole 
}) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (requireAuth && !user) {
        toast.error('Please sign in to access this page');
        router.push('/login');
        return;
      }

      if (user && !user.is_approved) {
        toast.error('Your account is pending approval');
        router.push('/');
        return;
      }

      if (requiredRole && user && user.role !== requiredRole) {
        toast.error('You do not have permission to access this page');
        router.push('/');
        return;
      }
    }
  }, [user, loading, requireAuth, requiredRole, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (requireAuth && !user) {
    return null;
  }

  if (user && !user.is_approved) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Account Pending Approval
          </h1>
          <p className="text-gray-600">
            Your account is currently being reviewed by our administrators. 
            You will receive an email once your account is approved.
          </p>
        </div>
      </div>
    );
  }

  if (requiredRole && user && user.role !== requiredRole) {
    return null;
  }

  return <>{children}</>;
};

export default ProtectedRoute;