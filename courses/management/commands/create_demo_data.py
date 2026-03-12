from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Count
from courses.models import Category, Course
from lessons.models import Module, Lesson
from reviews.models import Review
from enrollments.models import Enrollment
from payments.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo data for the learning platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')
        
        # Create instructors
        instructor1, created = User.objects.get_or_create(
            username='john_instructor',
            defaults={
                'email': 'john@learnhub.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'instructor',
                'is_verified_instructor': True,
                'bio': 'Senior Software Engineer with 10+ years of experience in web development.'
            }
        )
        if created:
            instructor1.set_password('demo1234')
            instructor1.save()
        
        instructor2, created = User.objects.get_or_create(
            username='sarah_instructor',
            defaults={
                'email': 'sarah@learnhub.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'instructor',
                'is_verified_instructor': True,
                'bio': 'Data Science Expert and AI Researcher.'
            }
        )
        if created:
            instructor2.set_password('demo1234')
            instructor2.save()
        
        instructor3, created = User.objects.get_or_create(
            username='mike_instructor',
            defaults={
                'email': 'mike@learnhub.com',
                'first_name': 'Mike',
                'last_name': 'Davis',
                'role': 'instructor',
                'is_verified_instructor': True,
                'bio': 'Full-stack developer and mobile app specialist.'
            }
        )
        if created:
            instructor3.set_password('demo1234')
            instructor3.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created instructors'))
        
        # Create categories
        categories_data = [
            {'name': 'Web Development', 'icon': 'fa-code', 'description': 'Learn HTML, CSS, JavaScript and modern frameworks'},
            {'name': 'Data Science', 'icon': 'fa-chart-line', 'description': 'Master Python, ML and data analysis'},
            {'name': 'Mobile Development', 'icon': 'fa-mobile-alt', 'description': 'Build iOS and Android apps'},
            {'name': 'Machine Learning', 'icon': 'fa-brain', 'description': 'Deep learning and AI fundamentals'},
            {'name': 'DevOps', 'icon': 'fa-server', 'description': 'Cloud computing and automation'},
            {'name': 'UI/UX Design', 'icon': 'fa-palette', 'description': 'Design beautiful user interfaces'},
            {'name': 'Cybersecurity', 'icon': 'fa-shield-alt', 'description': 'Protect systems and networks'},
            {'name': 'Cloud Computing', 'icon': 'fa-cloud', 'description': 'AWS, Azure and Google Cloud'}
        ]
        
        categories = []
        for cat_data in categories_data:
            import re
            slug = re.sub(r'[^a-z0-9\-]', '', cat_data['name'].lower().replace(' ', '-'))
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slug,
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            categories.append(cat)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        
        # Create courses
        courses_data = [
            {
                'title': 'Complete Web Development Bootcamp 2024',
                'description': 'Learn HTML, CSS, JavaScript, React, Node.js and more. This comprehensive course takes you from beginner to professional web developer.',
                'category': categories[0],
                'instructor': instructor1,
                'price': 49.99,
                'discount_price': 19.99,
                'level': 'beginner',
                'requirements': 'Basic computer skills\nNo programming experience needed\nA computer with internet access',
                'outcomes': 'Build responsive websites\nCreate full-stack web applications\nMaster JavaScript fundamentals\nDeploy applications to production'
            },
            {
                'title': 'Python for Data Science and Machine Learning',
                'description': 'Master Python programming for data analysis, visualization, and machine learning. Includes pandas, numpy, scikit-learn and TensorFlow.',
                'category': categories[1],
                'instructor': instructor2,
                'price': 79.99,
                'discount_price': 29.99,
                'level': 'intermediate',
                'requirements': 'Basic Python knowledge\nUnderstanding of math concepts\nComputer with Python installed',
                'outcomes': 'Analyze data with pandas\nCreate visualizations\nBuild ML models\nDeploy ML solutions'
            },
            {
                'title': 'iOS App Development with Swift',
                'description': 'Build beautiful iOS apps from scratch using Swift and SwiftUI. Learn to create apps for iPhone and iPad.',
                'category': categories[2],
                'instructor': instructor3,
                'price': 69.99,
                'discount_price': 24.99,
                'level': 'beginner',
                'requirements': 'Mac computer\nNo prior iOS experience\nWillingness to learn',
                'outcomes': 'Build iOS apps with Swift\nCreate SwiftUI interfaces\nPublish apps to App Store\nUnderstand iOS architecture'
            },
            {
                'title': 'Deep Learning with TensorFlow',
                'description': 'Learn neural networks, CNNs, RNNs and build AI models. This course covers everything from basics to advanced deep learning.',
                'category': categories[3],
                'instructor': instructor2,
                'price': 99.99,
                'discount_price': 39.99,
                'level': 'advanced',
                'requirements': 'Python experience\nBasic ML knowledge\nGPU recommended',
                'outcomes': 'Build neural networks\nCreate image classifiers\nImplement NLP models\nDeploy AI solutions'
            },
            {
                'title': 'AWS Cloud Practitioner Certification',
                'description': 'Prepare for AWS certification. Learn cloud fundamentals, AWS services, and best practices.',
                'category': categories[4],
                'instructor': instructor1,
                'price': 39.99,
                'discount_price': 14.99,
                'level': 'beginner',
                'requirements': 'Basic IT knowledge\nInternet connection\nDesire to learn cloud',
                'outcomes': 'Understand cloud concepts\nNavigate AWS console\nPrepare for certification\nDeploy cloud solutions'
            },
            {
                'title': 'UI/UX Design Masterclass',
                'description': 'Learn to design beautiful user interfaces and experiences. Master Figma, design principles, and user research.',
                'category': categories[5],
                'instructor': instructor3,
                'price': 59.99,
                'discount_price': 22.99,
                'level': 'beginner',
                'requirements': 'No design experience needed\nFigma (free) installed\nCreative mindset',
                'outcomes': 'Design interfaces in Figma\nApply design principles\nConduct user research\nBuild design portfolios'
            },
            {
                'title': 'React - The Complete Guide',
                'description': 'Master React including hooks, Redux, React Router, and Next.js. Build modern single-page applications.',
                'category': categories[0],
                'instructor': instructor1,
                'price': 54.99,
                'discount_price': 21.99,
                'level': 'intermediate',
                'requirements': 'JavaScript knowledge\nHTML/CSS basics\nUnderstanding of JS ES6',
                'outcomes': 'Build React apps\nMaster React hooks\nImplement Redux\nCreate SSR apps with Next.js'
            },
            {
                'title': 'Cybersecurity Fundamentals',
                'description': 'Learn ethical hacking, network security, and cyber defense. Prepare for a career in cybersecurity.',
                'category': categories[6],
                'instructor': instructor2,
                'price': 74.99,
                'discount_price': 29.99,
                'level': 'beginner',
                'requirements': 'Basic computer skills\nUnderstanding of networks\nLegal mindset',
                'outcomes': 'Understand cyber threats\nPerform penetration testing\nSecure networks\nRespond to incidents'
            },
        ]
        
        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                instructor=course_data['instructor'],
                defaults={
                    'description': course_data['description'],
                    'category': course_data['category'],
                    'price': course_data['price'],
                    'discount_price': course_data['discount_price'],
                    'level': course_data['level'],
                    'requirements': course_data['requirements'],
                    'outcomes': course_data['outcomes'],
                    'is_published': True,
                    'is_approved': True,
                    'total_lessons': 0,
                    'total_duration': 1200
                }
            )
            courses.append(course)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))
        
        # Create modules and lessons for each course
        lesson_titles = [
            'Introduction and Setup',
            'Core Concepts',
            'Building Your First Project',
            'Advanced Techniques',
            'Best Practices',
            'Real-world Applications',
            'Testing and Debugging',
            'Deployment',
            'Final Project',
            'Course Summary'
        ]
        
        for course in courses:
            if not course.modules.exists():
                for i, title in enumerate(lesson_titles[:5]):
                    module, created = Module.objects.get_or_create(
                        course=course,
                        title=f'Module {i+1}: {title}',
                        defaults={'order': i}
                    )
                    for j in range(3):
                        Lesson.objects.get_or_create(
                            module=module,
                            title=f'Lesson {j+1}: {title} - Part {j+1}',
                            defaults={
                                'order': j,
                                'duration': 15 + (j * 5),
                                'video_id': 'dQw4w9WgXcQ',
                                'is_preview': j == 0
                            }
                        )
                # Update course stats
                from django.db.models import Count
                course.total_lessons = course.modules.aggregate(
                    total=Count('lessons')
                )['total'] or 0
                course.total_duration = sum(
                    m.get_total_duration() for m in course.modules.all()
                )
                course.save()
        
        self.stdout.write(self.style.SUCCESS('Created modules and lessons'))
        
        # Create students
        students = []
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@example.com',
                    'first_name': f'Student',
                    'last_name': f'User{i}',
                    'role': 'student'
                }
            )
            if created:
                student.set_password('demo1234')
                student.save()
            students.append(student)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} students'))
        
        # Create enrollments and reviews
        enrollment_count = 0
        for course in courses[:6]:
            for student in students[:3]:
                enrollment, created = Enrollment.objects.get_or_create(
                    user=student,
                    course=course,
                    defaults={
                        'progress_percentage': 20.0 + (hash(student.username + course.title) % 60),
                        'completed': False
                    }
                )
                
                if created:
                    payment = Payment.objects.create(
                        user=student,
                        course=course,
                        amount=course.discount_price or course.price,
                        transaction_id=f'TXN-{student.id}-{course.id}-{enrollment_count}',
                        status='completed'
                    )
                    enrollment.payment = payment
                    enrollment.save()
                    enrollment_count += 1
                
                # Add reviews
                if not Review.objects.filter(user=student, course=course).exists():
                    Review.objects.create(
                        user=student,
                        course=course,
                        rating=4 + (hash(student.username) % 2),
                        comment=f'Great course! Learned a lot from {course.instructor.first_name}. Highly recommended!'
                    )
        
        self.stdout.write(self.style.SUCCESS('Created enrollments and reviews'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Demo data created successfully!'))
        self.stdout.write('\n📋 Login credentials:')
        self.stdout.write('   Admin: admin / admin123')
        self.stdout.write('   Instructor: john_instructor / demo1234')
        self.stdout.write('   Student: student1 / demo1234')
