# User Profile Module

This module handles user profile data for the FitForm application. It provides:

### Features
- User data validation
- Format data for workout program prompts
- Format data for meal plan prompts
- Profile completeness tracking
- BMI calculation

### Usage

```python
from app.models.user import UserProfile
from datetime import date

# Create user profile
user = UserProfile()
user.first_name = "أحمد"
user.last_name = "محمد"
user.height = 175
user.weight = 80
user.fitness_goals = "Weight Loss"

# Get inputs for workout program
workout_inputs = user.get_workout_program_inputs()

# Get inputs for meal plan
meal_inputs = user.get_meal_plan_inputs()

# Validate data
if user.is_valid():
    print("Profile is valid!")
```

### Integration with Prompts

The User Profile module formats data specifically for:
- `workout_program.prompty` - Gets training preferences and physical data
- `meal_prep.prompty` - Gets nutrition preferences and health data