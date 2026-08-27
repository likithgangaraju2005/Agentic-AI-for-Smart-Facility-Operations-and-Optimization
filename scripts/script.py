from function import get_name, calculate_marks, check_result

name = get_name("Lily")

total, average = calculate_marks(85, 90, 78)

result = check_result(average)

print("Name:", name)
print("Total Marks:", total)
print("Average Marks:", average)
print("Result:", result)