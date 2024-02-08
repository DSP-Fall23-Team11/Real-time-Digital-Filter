import sympy as sp

class AllPassFilter:
    def __init__(self, a):
        self.a = a

    def find_zeros_poles(self):
        # Define the variable and transfer function
        omega = sp.symbols('omega', real=True)
        Hap = (sp.exp(-1j * omega) - sp.conjugate(self.a)) / (1 - self.a * sp.exp(-1j * omega))

        # Find the zeros and poles by solving the equations
        zeros = sp.solve(sp.Eq(Hap, 0), omega)
        poles = sp.solve(sp.Eq(1 - self.a * sp.exp(-1j * omega), 0), omega)

        # Return the calculated zeros and poles
        return zeros, poles

# Example usage:
# Replace 'your_a_value' with the actual 'a' value you want to use
a_value = complex(0.5, 0.5)
all_pass_filter = AllPassFilter(a_value)

zeros, poles = all_pass_filter.find_zeros_poles()

# Print the zeros and poles
print("Zeros:", zeros)
print("Poles:", poles)