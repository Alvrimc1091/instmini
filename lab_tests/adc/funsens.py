# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Create the DataFrame
# df_freqs = pd.DataFrame({'f':[40, 45, 50, 55, 60],
#                          'p':[1993, 1902, 2256, 2076, 1876]})

# # Extract the data
# x = df_freqs['f']
# y = df_freqs['p']

# # Fit a fourth-degree polynomial to the data
# coefficients = np.polyfit(x, y, 4)

# # Print the coefficients
# print("Coefficients of the fitted polynomial:")
# for i, coeff in enumerate(reversed(coefficients)):
#     print(f"  Coefficient {i}: {coeff}")

# # Create a polynomial function based on the coefficients
# poly = np.poly1d(coefficients)

# # Generate a range of x values for the fitted curve
# x_fit = np.linspace(min(x), max(x), 100)

# # Calculate the corresponding y values for the fitted curve
# y_fit = poly(x_fit)

# # Create a plot
# plt.figure(figsize=(8, 6))
# plt.scatter(x, y, label='Data', color='blue')
# plt.plot(x_fit, y_fit, label='Fitted Polynomial', color='red')
# plt.xlabel('f')
# plt.ylabel('p')
# plt.legend()
# plt.title('Polynomial Fit to Data')
# plt.grid(True)
# plt.show()




plt.savefig('sensitiviy_function.png')
print('Gráfico guardado como sensitivity_function.png')