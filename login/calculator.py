class Calculator():

    def __init__(self, grades: list[str], weights: list[str]) -> None:
        self.grades = [float(grade) for grade in grades]
        self.weights = [float(weight) for weight in weights]

    def avg_grade(self) -> float:
        # Check if the lengths of grades and weights are the same
        if len(self.grades) != len(self.weights):
            raise ValueError("Lengths of grades and weights must be the same")
        elif len(self.grades) == 0:
            return 0

        # Calculate the weighted sum
        weighted_sum = sum(grade * weight for grade, weight in zip(self.grades, self.weights))

        # Calculate the total weight
        total_weight = sum(self.weights)

        # Calculate the weighted average grade
        average_grade = weighted_sum / total_weight

        return round(average_grade, 2)