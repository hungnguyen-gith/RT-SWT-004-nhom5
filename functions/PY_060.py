def grade_exam(score, attendance_pct, has_late_penalty, extra_credit, is_makeup_exam, has_disability_accommodation):
    adjusted = score
    if has_late_penalty:
        if has_disability_accommodation:
            adjusted -= 2
        else:
            adjusted -= 5
    adjusted += extra_credit
    if attendance_pct < 50:
        if has_disability_accommodation:
            adjusted -= 5
        else:
            adjusted -= 10
    elif attendance_pct < 75:
        adjusted -= 5
    if is_makeup_exam:
        adjusted = min(adjusted, 80)
    if adjusted >= 90:
        grade = "A"
    elif adjusted >= 80:
        grade = "B"
    elif adjusted >= 70:
        grade = "C"
    elif adjusted >= 60:
        grade = "D"
    else:
        grade = "F"
    if grade == "F" and attendance_pct >= 90:
        grade = "D"
    return grade