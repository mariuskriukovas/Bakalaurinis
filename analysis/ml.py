# import matplotlib.pyplot as plt
# import numpy as np
# from sklearn import datasets, linear_model
#
#
# #Define the problem
# problem = [75, 104, 147, -3, 204, 275]
#
# #create x and y for the problem
#
# x=[]
# y=[]
#
# for (xi, yi) in enumerate(problem):
#   features=[]
#   for i in range(3):
#     features.append(pow(xi,i))
#   x.append(features)
#   y.append(yi)
# print(x)
# print(y)
# x=np.array(x)
# y=np.array(y)
# # Create linear regression object
# regr = linear_model.LinearRegression()
# regr.fit(x, y)
#
# #create the testing set
# x_test_range=range(len(x),3+len(x))
# x_test=[]
# for xi in x_test_range:
#   features=[]
#   for i in range(3):
#     features.append(pow(xi,i))
#   x_test.append(features)
# print (x_test)
# # The coefficients
# print('Coefficients: \n', regr.coef_)
# print('Intercept: \n', regr.intercept_)
# # The mean squared error
# print("Mean squared error: %.2f"
#               % np.mean((regr.predict(x) - y) ** 2))
# # Explained variance score: 1 is perfect prediction
# print('Variance score: %.2f' % regr.score(x,y))
#
# #Do predictions
# y_predicted = regr.predict(x_test)
#
# print ("Next few numbers in the series are")
# for pred in y_predicted:
#   print (pred)
#
# plt.scatter(range(len(problem)), problem, color='black')
# plt.scatter(x_test_range, y_predicted,  color='red')
# #plt.plot(x_test, regr.predict(x_test), color='blue',
# #                 linewidth=3)
#
# plt.show()


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD