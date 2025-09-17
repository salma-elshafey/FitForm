"""
User Profile Module for FitForm
Simple class to handle user data and format inputs for workout and meal plan prompts
"""

from datetime import date
from typing import List, Optional, Dict


class UserProfile:
    """
    User Profile class to store user data and format inputs for prompts
    """
    
    def __init__(self):
        # Personal Information
        self.first_name: str = ""
        self.last_name: str = ""
        self.email: str = ""
        self.date_of_birth: Optional[date] = None
        self.gender: str = ""  # "Male", "Female", "Other"
        
        # Physical Data
        self.height: Optional[float] = None  # in cm
        self.weight: Optional[float] = None  # in kg
        
        # Fitness Goals
        self.fitness_goals: str = ""  # "Weight Loss", "Muscle Building", etc.
        self.sub_goals: List[str] = []
        self.activity_level: str = ""  # "Sedentary", "Lightly Active", etc.
        self.experience_level: str = ""  # "Beginner", "Intermediate", "Advanced"
        
        # Training Preferences
        self.training_days: Optional[int] = None  # days per week
        self.time_per_session: Optional[int] = None  # minutes
        self.workout_location: str = ""  # "Gym", "Home", "Outdoors"
        self.available_equipment: List[str] = []
        
        # Health Information
        self.special_conditions: List[str] = []
        self.allergies: List[str] = []
        self.diseases: List[str] = []
        
        # Nutrition Preferences
        self.dietary_preferences: List[str] = []  # "Vegetarian", "Vegan", etc.
        self.cooking_time: Optional[int] = None  # minutes per day
        
        # Background
        self.user_background: str = ""
    
    def get_age(self) -> Optional[int]:
        """Calculate age from date of birth"""
        if not self.date_of_birth:
            return None
        
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age
    
    def get_bmi(self) -> Optional[float]:
        """Calculate BMI"""
        if not self.height or not self.weight:
            return None
        
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 1)
    
    def validate_data(self) -> Dict[str, List[str]]:
        """Validate user profile data"""
        errors = {}
        
        # Personal info validation
        if not self.first_name:
            errors.setdefault('personal', []).append("First name is required")
        
        if not self.last_name:
            errors.setdefault('personal', []).append("Last name is required")
        
        if self.email and '@' not in self.email:
            errors.setdefault('personal', []).append("Invalid email format")
        
        # Physical data validation
        if self.height and (self.height < 50 or self.height > 300):
            errors.setdefault('physical', []).append("Height must be between 50-300 cm")
        
        if self.weight and (self.weight < 20 or self.weight > 500):
            errors.setdefault('physical', []).append("Weight must be between 20-500 kg")
        
        # Age validation
        age = self.get_age()
        if age and (age < 13 or age > 120):
            errors.setdefault('personal', []).append("Age must be between 13-120 years")
        
        # Training validation
        if self.training_days and (self.training_days < 1 or self.training_days > 7):
            errors.setdefault('training', []).append("Training days must be between 1-7")
        
        if self.time_per_session and (self.time_per_session < 15 or self.time_per_session > 180):
            errors.setdefault('training', []).append("Session time must be between 15-180 minutes")
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if profile data is valid"""
        return len(self.validate_data()) == 0
    
    def get_workout_program_inputs(self) -> Dict[str, str]:
        """
        Format user data for workout_program.prompty inputs
        """
        return {
            "training_days": str(self.training_days or 3),
            "fitness_goals": self.fitness_goals or "General Fitness",
            "special_conditions": ", ".join(self.special_conditions) if self.special_conditions else "None",
            "height": str(self.height or ""),
            "weight": str(self.weight or ""),
            "age": str(self.get_age() or ""),
            "gender": self.gender or "",
            "user_background": self.user_background or "",
            "time_per_session": f"{self.time_per_session or 45} minutes",
            "workout_location": self.workout_location or "Home",
            "available_equipment": ", ".join(self.available_equipment) if self.available_equipment else "Bodyweight only",
            "experience_level": self.experience_level or "Beginner"
        }
    
    def get_meal_plan_inputs(self) -> Dict[str, str]:
        """
        Format user data for meal_prep.prompty inputs
        """
        return {
            "goal": self.fitness_goals or "General Fitness",
            "sub_goals": ", ".join(self.sub_goals) if self.sub_goals else "",
            "height": str(self.height or ""),
            "weight": str(self.weight or ""),
            "age": str(self.get_age() or ""),
            "gender": self.gender or "",
            "activity_level": self.activity_level or "Moderately Active",
            "allergies": ", ".join(self.allergies) if self.allergies else "None",
            "preferences": ", ".join(self.dietary_preferences) if self.dietary_preferences else "",
            "diseases": ", ".join(self.diseases) if self.diseases else "None",
            "cooking_time": f"{self.cooking_time or 30} minutes per day"
        }
    
    def get_profile_summary(self) -> Dict:
        """Get a summary of the user profile"""
        return {
            "name": f"{self.first_name} {self.last_name}".strip(),
            "age": self.get_age(),
            "bmi": self.get_bmi(),
            "fitness_goal": self.fitness_goals,
            "activity_level": self.activity_level,
            "experience_level": self.experience_level,
            "is_valid": self.is_valid()
        }
    
    def update_from_dict(self, data: Dict):
        """Update profile from dictionary data"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "fitness_goals": self.fitness_goals,
            "sub_goals": self.sub_goals,
            "activity_level": self.activity_level,
            "experience_level": self.experience_level,
            "training_days": self.training_days,
            "time_per_session": self.time_per_session,
            "workout_location": self.workout_location,
            "available_equipment": self.available_equipment,
            "special_conditions": self.special_conditions,
            "allergies": self.allergies,
            "diseases": self.diseases,
            "dietary_preferences": self.dietary_preferences,
            "cooking_time": self.cooking_time,
            "user_background": self.user_background
        }
# TODO: Add WorkoutHistory and MealPlanChecklist models below