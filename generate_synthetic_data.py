import json
import random
import argparse

# --- Reasoning Puzzle Generation ---

NAMES = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
COLORS = ["Red", "Green", "Blue", "Yellow", "White", "Black", "Brown", "Orange", "Purple", "Gray"]
PETS = ["Dog", "Cat", "Bird", "Fish", "Horse", "Rabbit", "Turtle", "Snake", "Lizard", "Hamster"]
PROFESSIONS = ["Doctor", "Lawyer", "Teacher", "Engineer", "Artist", "Chef", "Pilot", "Musician", "Writer", "Scientist"]

def generate_reasoning_puzzle():
    # A simple logic puzzle template
    num_entities = random.randint(3, 5)
    
    shuffled_names = random.sample(NAMES, num_entities)
    shuffled_professions = random.sample(PROFESSIONS, num_entities)
    
    solution = {name: prof for name, prof in zip(shuffled_names, shuffled_professions)}
    
    clues = []
    # Generate non-contradictory clues
    for i in range(num_entities):
        if random.random() > 0.5:
            # Direct clue
            clues.append(f"{shuffled_names[i]} is the {solution[shuffled_names[i]]}.")
        else:
            # Negative clue
            wrong_profession = random.choice([p for p in shuffled_professions if p != solution[shuffled_names[i]]])
            clues.append(f"{shuffled_names[i]} is not the {wrong_profession}.")

    random.shuffle(clues)

    problem = f"There are {num_entities} people: {', '.join(shuffled_names)}. They each have a different profession: {', '.join(shuffled_professions)}. Find out who has which profession based on the following clues:\n\n" + "\n".join(clues)
    
    return {"type": "reasoning_puzzle", "problem": problem, "solution": json.dumps(solution)}

# --- Mathematical Problem Generation ---

def generate_math_problem():
    # A word problem generator with more variety
    
    op_type = random.choice(["add", "subtract", "multiply", "divide", "percentage", "fraction", "speed-distance-time"])
    
    if op_type == "add":
        num1 = random.randint(1, 1000)
        num2 = random.randint(1, 1000)
        problem = f"A company has {num1} employees. They hire {num2} more. How many employees do they have now?"
        solution = num1 + num2
    elif op_type == "subtract":
        num1 = random.randint(500, 1000)
        num2 = random.randint(1, 500)
        problem = f"A library has {num1} books. {num2} books are checked out. How many books are left in the library?"
        solution = num1 - num2
    elif op_type == "multiply":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        problem = f"A factory produces {num1} widgets per day. How many widgets does it produce in {num2} days?"
        solution = num1 * num2
    elif op_type == "divide":
        divisor = random.randint(2, 20)
        dividend = divisor * random.randint(10, 50)
        problem = f"There are {dividend} cookies to be shared equally among {divisor} people. How many cookies does each person get?"
        solution = dividend // divisor
    elif op_type == "percentage":
        price = random.randint(10, 500)
        discount = random.randint(5, 50)
        problem = f"A shirt costs ${price}. It is on sale for {discount}% off. What is the final price?"
        solution = price * (1 - discount / 100)
    elif op_type == "fraction":
        numerator = random.randint(1, 5)
        denominator = random.randint(numerator + 1, 10)
        multiplier = random.randint(2, 5)
        problem = f"A recipe calls for {numerator}/{denominator} cups of flour. You want to make {multiplier} times the recipe. How much flour do you need in cups?"
        solution = f"{numerator * multiplier}/{denominator}"
    elif op_type == "speed-distance-time":
        speed = random.randint(40, 120)
        time = random.randint(1, 5)
        problem = f"A car travels at a constant speed of {speed} km/h. How far will it travel in {time} hours?"
        solution = speed * time
        
    return {"type": "math_problem", "problem": problem, "solution": str(solution)}

# --- Obscure Code Generation ---

def generate_obscure_code():
    # A template for a confusing code snippet
    
    choice = random.choice(["list_comprehension", "lambda_factorial"])
    
    if choice == "list_comprehension":
        n = random.randint(10, 30)
        code = f"[x**2 for x in range({n}) if x % {random.randint(2,4)} == 0 and (x % {random.randint(5,7)} != 0 or x % {random.randint(8,10)} == 0)]"
        analysis = f"This is a list comprehension in Python that generates a list of squared numbers up to {n} based on a complex condition.\n\n"
        analysis += "**How it works:**\n"
        analysis += f"It iterates through numbers from 0 to {n-1}.\n"
        analysis += "The condition is evaluated for each number, and if it's true, the square of the number is added to the list.\n\n"
        analysis += "**Why it's obscure:**\n"
        analysis += "*   **Complex Condition:** The nested boolean logic with `and` and `or` can be hard to reason about.\n"
        analysis += "*   **Readability:** A standard loop with `if` statements would be more readable."
    else: # lambda_factorial
        code = "Y = lambda f: (lambda x: f(lambda *args: x(x)(*args)))(lambda x: f(lambda *args: x(x)(*args)))\nfactorial = Y(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))"
        analysis = "This code defines the factorial function using the Y combinator in a single line of code (conceptually). It is a classic example of implementing recursion with anonymous functions."

    return {"type": "obscure_code", "code": code, "analysis": analysis}


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic data.")
    parser.add_argument("num_problems", type=int, help="The total number of problems to generate.")
    parser.add_argument("output_file", type=str, help="The output file to write the data to.")
    args = parser.parse_args()
    
    with open(args.output_file, "w") as f:
        for i in range(args.num_problems):
            problem_type = random.choice(["reasoning", "math", "code"])
            
            if problem_type == "reasoning":
                problem = generate_reasoning_puzzle()
            elif problem_type == "math":
                problem = generate_math_problem()
            else: # code
                problem = generate_obscure_code()
                
            f.write(json.dumps(problem) + "\n")
            
    print(f"Successfully generated {args.num_problems} problems and saved them to {args.output_file}")

if __name__ == "__main__":
    main()
