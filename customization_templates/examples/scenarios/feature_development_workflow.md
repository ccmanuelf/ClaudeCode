# Feature Development Workflow Example

## Scenario Overview
**Objective:** Complete end-to-end development of a user profile management feature
**Duration:** 2-3 days (16-24 hours of development)
**Complexity:** Intermediate
**Team Size:** 1-2 developers

## Prerequisites
- ClaudeCode setup complete
- Basic project structure in place
- Database access configured
- Testing framework installed

## Phase 1: Feature Planning & Specification

### Step 1: Initialize Feature Planning
```bash
# Start ClaudeCode session
python resume.py

# Create planning document
cp agent-config/command_templates/planning_template.md planning/user_profile_feature.md
```

### Step 2: Define Feature Specification
```bash
# Create detailed specification
cp agent-config/templates/spec_template.json specs/user_profile_spec.json
```

**Fill in key specification details:**
```json
{
  "name": "User Profile Management Specification",
  "version": "1.0.0",
  "status": "draft",
  "authors": ["Your Name"],
  "overview": {
    "purpose": "Allow users to view, edit, and manage their profile information",
    "scope": "User profile CRUD operations with validation and security"
  },
  "requirements": {
    "functional": [
      {
        "id": "FR001",
        "title": "View Profile",
        "description": "Users can view their current profile information",
        "priority": "must-have"
      },
      {
        "id": "FR002", 
        "title": "Edit Profile",
        "description": "Users can update their profile information",
        "priority": "must-have"
      },
      {
        "id": "FR003",
        "title": "Profile Validation",
        "description": "System validates profile data before saving",
        "priority": "must-have"
      }
    ]
  }
}
```

### Step 3: Create Feature Task
```bash
# Create task document
cp agent-config/command_templates/do_task_template.md tasks/user_profile_implementation.md
```

**Task Configuration:**
- Task ID: FEAT-UP-001
- Task Name: User Profile Management Feature
- Priority: High
- Estimated Effort: 16-20 hours
- Dependencies: User authentication system

### Step 4: Initial Checkpoint
```bash
# Create planning checkpoint
python resume.py
# Choose option 2: Create checkpoint
# Description: "User profile feature - planning complete, ready for implementation"
```

## Phase 2: Database & Backend Implementation

### Step 5: Database Schema Design
```bash
# Create migration file
mkdir -p migrations
touch migrations/003_add_user_profiles.sql
```

**Sample Migration:**
```sql
-- migrations/003_add_user_profiles.sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    bio TEXT,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_email ON user_profiles(email);
```

### Step 6: Backend API Implementation
```bash
# Create backend files
mkdir -p src/api/profiles
touch src/api/profiles/__init__.py
touch src/api/profiles/models.py
touch src/api/profiles/views.py
touch src/api/profiles/serializers.py
```

**Sample Model (models.py):**
```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### Step 7: Database Checkpoint
```bash
# Run migration
python manage.py migrate  # or your migration command

# Create checkpoint
python resume.py
# Choose option 2: Create checkpoint
# Description: "User profiles - database schema implemented and migrated"
```

## Phase 3: API Endpoints Development

### Step 8: Implement API Views
**Sample Views (views.py):**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['put'])
    def update_me(self, request):
        """Update current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
```

### Step 9: API Checkpoint
```bash
# Test API endpoints
curl -X GET http://localhost:8000/api/profiles/me/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create checkpoint
python resume.py
# Choose option 2: Create checkpoint  
# Description: "User profiles - API endpoints implemented, basic testing complete"
```

## Phase 4: Frontend Implementation

### Step 10: Create Frontend Components
```bash
# Create frontend structure
mkdir -p src/components/profiles
touch src/components/profiles/ProfileView.jsx
touch src/components/profiles/ProfileEdit.jsx
touch src/components/profiles/ProfileForm.jsx
```

**Sample ProfileView Component:**
```javascript
import React, { useState, useEffect } from 'react';
import { profileAPI } from '../api/profiles';

const ProfileView = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileAPI.getMe();
      setProfile(data);
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading profile...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>No profile found</div>;

  return (
    <div className="profile-view">
      <h2>My Profile</h2>
      <div className="profile-info">
        <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Phone:</strong> {profile.phone || 'Not provided'}</p>
        <p><strong>Bio:</strong> {profile.bio || 'No bio available'}</p>
      </div>
      <button onClick={() => window.location.href = '/profile/edit'}>
        Edit Profile
      </button>
    </div>
  );
};

export default ProfileView;
```

### Step 11: Frontend Checkpoint
```bash
# Test frontend components
npm start  # or your dev server command

# Create checkpoint
python resume.py
# Choose option 2: Create checkpoint
# Description: "User profiles - frontend components implemented, basic UI working"
```

## Phase 5: Testing & Validation

### Step 12: Write Tests
```bash
# Create test files
mkdir -p tests/api/profiles
touch tests/api/profiles/test_models.py
touch tests/api/profiles/test_views.py
touch tests/frontend/profiles/ProfileView.test.jsx
```

**Sample Backend Tests (test_views.py):**
```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.profiles.models import UserProfile

class UserProfileViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile_me(self):
        """Test retrieving current user's profile"""
        response = self.client.get('/api/profiles/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')

    def test_update_profile_me(self):
        """Test updating current user's profile"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.put('/api/profiles/update_me/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
```

### Step 13: Run Test Suite
```bash
# Run backend tests
python manage.py test tests.api.profiles

# Run frontend tests  
npm test -- --testPathPattern=profiles

# Check coverage
pytest --cov=src/api/profiles tests/api/profiles/
```

### Step 14: Testing Checkpoint
```bash
# Create checkpoint after testing
python resume.py
# Choose option 2: Create checkpoint
# Description: "User profiles - comprehensive test suite implemented, all tests passing"
```

## Phase 6: Integration & Deployment Preparation

### Step 15: Integration Testing
```bash
# Test full workflow
curl -X GET http://localhost:8000/api/profiles/me/ \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X PUT http://localhost:8000/api/profiles/update_me/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Updated", "last_name": "User"}'
```

### Step 16: Documentation Update
```bash
# Update API documentation
echo "## User Profile Endpoints

### GET /api/profiles/me/
Get current user's profile

### PUT /api/profiles/update_me/  
Update current user's profile

**Request Body:**
\`\`\`json
{
  \"first_name\": \"string\",
  \"last_name\": \"string\",
  \"email\": \"string\",
  \"phone\": \"string\",
  \"bio\": \"string\"
}
\`\`\`" >> docs/API.md
```

### Step 17: Final Feature Checkpoint
```bash
# Create completion checkpoint
python resume.py
# Choose option 2: Create checkpoint
# Description: "User profiles feature COMPLETE - ready for code review and deployment"
```

## Phase 7: Code Review & Deployment

### Step 18: Prepare for Review
```bash
# Create pull request
git checkout -b feature/user-profiles
git add .
git commit -m "Add user profile management feature

- Database schema for user profiles
- REST API endpoints for CRUD operations
- Frontend components for viewing/editing
- Comprehensive test suite
- API documentation updates"

git push origin feature/user-profiles
```

### Step 19: Create GitHub Issue for Review
```bash
# Use GitHub issue template
cp agent-config/templates/github_issue_template.json .github/issues/user_profiles_review.json
```

### Step 20: Session Summary
```bash
# Generate comprehensive session summary
cp agent-config/command_templates/session_summary_template.md sessions/user_profiles_completion.md
```

**Key Session Summary Points:**
- **Completed Items:** All functional requirements implemented
- **Files Modified:** 15 new files, 3 updated files
- **Test Coverage:** 95% for backend, 85% for frontend
- **Performance:** All API endpoints < 200ms response time
- **Next Steps:** Code review, QA testing, production deployment

## Success Metrics

### Technical Metrics
- ✅ All functional requirements (FR001-FR003) implemented
- ✅ 95%+ test coverage achieved
- ✅ API response times < 200ms
- ✅ Frontend components fully functional
- ✅ Database migration successful

### Process Metrics
- ✅ 8 checkpoints created throughout development
- ✅ No work lost during development
- ✅ Clear handoff documentation prepared
- ✅ Feature completed within estimated timeframe

## Lessons Learned

### What Went Well
1. **Checkpoint Strategy:** Regular checkpoints prevented any work loss
2. **Specification First:** Having clear specs accelerated development
3. **Test-Driven Approach:** Writing tests early caught integration issues
4. **Documentation:** Real-time documentation updates saved time

### Challenges Encountered
1. **Database Schema:** Initial design needed refinement for performance
2. **API Validation:** Edge cases required additional validation logic
3. **Frontend State:** Complex state management needed refactoring

### Recommendations for Future Features
1. **Start with API Design:** Define API contracts before implementation
2. **Parallel Development:** Frontend and backend can be developed simultaneously
3. **Early Testing:** Integration tests should run continuously
4. **Performance Baseline:** Establish performance requirements upfront

## Next Steps

After completing this feature:
1. **Code Review:** Submit for peer review
2. **QA Testing:** Hand off to QA team
3. **Performance Testing:** Load test the new endpoints
4. **Security Review:** Validate data protection measures
5. **Deployment:** Deploy to staging, then production
6. **Monitoring:** Set up monitoring for new endpoints
7. **User Feedback:** Collect initial user feedback

## Reusable Patterns

This workflow demonstrates several reusable patterns:
- **Checkpoint-Driven Development:** Regular progress saves
- **Specification-First Approach:** Clear requirements before coding
- **Parallel Testing:** Tests written alongside implementation
- **Documentation Automation:** Real-time doc updates
- **Integration Validation:** End-to-end testing throughout

These patterns can be applied to any feature development workflow in ClaudeCode.