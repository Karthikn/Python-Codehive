def check_password_strength(password: str) -> tuple[bool, list]:
    # Initialize list to track failed criteria
    failed_criteria = []
    
    # Flags to check character requirements
    has_upper, has_lower, has_digit, has_special = False, False, False, False
    special_chars = "!@#$%^&*(),.?\":{}|<>"
    
    # Check if password meets minimum length
    if len(password) < 8:
        failed_criteria.append("Password must be at least 8 characters long")
    
    # Iterate over each character to check for required conditions
    for char in password:
        if char.isupper(): has_upper = True
        if char.islower(): has_lower = True
        if char.isdigit(): has_digit = True
        if char in special_chars: has_special = True
        
        # Exit early if all criteria are met
        if has_upper and has_lower and has_digit and has_special:
            break

    # Append failed criteria to the list
    if not has_upper: failed_criteria.append("Password must contain at least one uppercase letter")
    if not has_lower: failed_criteria.append("Password must contain at least one lowercase letter")
    if not has_digit: failed_criteria.append("Password must contain at least one digit")
    if not has_special: failed_criteria.append("Password must contain at least one special character")

    # Return boolean indicating if all criteria are met, along with any failed criteria
    return len(failed_criteria) == 0, failed_criteria


def main():
    # Display password requirements to the user
    print("Password Strength Checker")
    print("------------------------")
    print("Password must meet the following criteria:")
    print("- At least 8 characters long")
    print("- Contains uppercase and lowercase letters")
    print("- Contains at least one digit")
    print("- Contains at least one special character")
    print("------------------------")

    # Continuously ask for a password until 'q' is entered
    while True:
        password = input("\nEnter a password to check (or 'q' to quit): ")

        # Exit condition
        if password.lower() == 'q':
            print("Exiting Password Strength Checker.")
            break

        # Validate password strength
        is_strong, failed_criteria = check_password_strength(password)

        # Provide feedback based on password strength
        if is_strong:
            print("\n✅ Password is strong! It meets all security criteria.")
        else:
            print("\n❌ Password is weak. Please address the following:")
            for criteria in failed_criteria:
                print(f"  - {criteria}")


if __name__ == "__main__":
    # Start the password strength validation
    main()
