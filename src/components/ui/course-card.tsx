"use client";

import Image from "next/image";
import { Star, Clock, Users, BookOpen } from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "./button";
import { cn, formatPrice, formatDuration } from "@/lib/utils";
import type { Course } from "@/types";

interface CourseCardProps {
  course: Course;
  className?: string;
}

export function CourseCard({ course, className }: CourseCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "group bg-card rounded-xl border border-border overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300",
        className
      )}
    >
      <div className="relative overflow-hidden">
        <Image
          src={course.thumbnail}
          alt={course.title}
          width={400}
          height={200}
          className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <div className="absolute top-3 left-3">
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-accent text-accent-foreground">
            {course.level}
          </span>
        </div>
        <div className="absolute top-3 right-3">
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary text-primary-foreground">
            {course.category}
          </span>
        </div>
      </div>

      <div className="p-4 space-y-3">
        <div>
          <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors">
            {course.title}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
            {course.shortDescription}
          </p>
        </div>

        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-1">
            <Image
              src={course.instructor.avatar || '/avatar-placeholder.png'}
              alt={course.instructor.name}
              width={20}
              height={20}
              className="rounded-full"
            />
            <span>{course.instructor.name}</span>
          </div>
        </div>

        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span className="font-medium">{course.rating}</span>
              <span>({course.reviewCount})</span>
            </div>
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              <span>{course.studentCount}</span>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            <span>{formatDuration(course.duration)}</span>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-border">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-primary">
              {formatPrice(course.price)}
            </span>
            {course.originalPrice && course.originalPrice > course.price && (
              <span className="text-sm text-muted-foreground line-through">
                {formatPrice(course.originalPrice)}
              </span>
            )}
          </div>
          <Button size="sm" className="group-hover:bg-primary/90">
            <BookOpen className="w-4 h-4 mr-2" />
            Enroll Now
          </Button>
        </div>
      </div>
    </motion.div>
  );
}