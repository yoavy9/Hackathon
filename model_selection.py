import math

from preprocess import *
from utils import *

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt



def decision_trees(X_train, X_test, y_train, y_test):
    f1_scores = []
    max_depths = [1, 2, 3, 4, 5, 6, 7, 8]
    for max_depth in max_depths:
        # Initialize the Decision Tree Classifier with varying max_depth
        dt = DecisionTreeClassifier(max_depth=max_depth)

        # Fit the data to the model
        dt.fit(X_train, y_train)

        # Predict the values for the test set
        y_pred = dt.predict(X_test)

        # Calculate F1 score
        f1 = f1_score(y_test, y_pred, average='macro')
        f1_scores.append(f1)

    # Create a DataFrame for visualization
    df = pd.DataFrame({'Max Depth': max_depths, 'F1 Score': f1_scores})

    # Plotting using Plotly
    fig = px.line(df, x='Max Depth', y='F1 Score', title='Decision Tree Performance')
    fig.show()


def linear_regression(X_train, X_test, y_train, y_test):
    import pandas as pd
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import StandardScaler
    from math import sqrt

    # Assuming X_train, y_train, X_test, y_test are already defined

    # Standardize the features to have mean=0 and variance=1 for PCA
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply PCA
    pca = PCA(n_components=0.95)  # retain 95% of the variance
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    print("finish pca")
    # Initialize the model
    model = LinearRegression()

    # Fit the model on the PCA-transformed data
    model.fit(X_train_pca, y_train)

    # Predict the selling amount for the test set
    predictions = model.predict(X_test_pca)
    print("finish predict")
    # Calculate the RMSE
    print(predictions)
    rmse = sqrt(mean_squared_error(y_test, predictions))
    print(f"RMSE: {rmse}")


def SVR(X_train, X_test, y_train, y_test):
    from sklearn.decomposition import PCA
    from sklearn.svm import SVR
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import StandardScaler
    from math import sqrt

    # Assuming X_train, y_train, X_test, y_test are already defined

    # Standardize the features to have mean=0 and variance=1 for PCA
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply PCA
    pca = PCA(n_components=0.95)  # retain 95% of the variance
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)

    # Initialize the model
    model = SVR()

    # Fit the model on the PCA-transformed data
    model.fit(X_train_pca, y_train)

    # Predict the selling amount for the test set
    predictions = model.predict(X_test_pca)

    # Calculate the RMSE
    rmse = sqrt(mean_squared_error(y_test, predictions))
    print(f"RMSE: {rmse}")


def lasso_regression(X_train, X_test, y_train, y_test):
    import pandas as pd
    from sklearn.linear_model import Lasso
    from sklearn.metrics import mean_squared_error
    from math import sqrt

    # Assuming X_train, y_train, X_test, y_test are already defined

    # Initialize the model
    model = Lasso(alpha=0.1)  # the alpha parameter controls the degree of regularization

    # Fit the model
    model.fit(X_train, y_train)

    # Predict the selling amount for the test set
    predictions = model.predict(X_test)

    # Calculate the RMSE
    rmse = sqrt(mean_squared_error(y_test, predictions))
    print(f"RMSE: {rmse}")


def elastic_net_regression(X_train, X_test, y_train, y_test):
    import pandas as pd
    from sklearn.linear_model import ElasticNet
    from sklearn.metrics import mean_squared_error
    from math import sqrt

    # Assuming X_train, y_train, X_test, y_test are already defined

    # Initialize the model
    model = ElasticNet(alpha=0.1, l1_ratio=0.5)
    # the alpha parameter controls the degree of regularization (0 means no penalty, default is 1)
    # the l1_ratio parameter corresponds to the mix between L1 and L2 regularization (0 for L2, 1 for L1, 0.5 for equal mix)

    # Fit the model
    model.fit(X_train, y_train)

    # Predict the selling amount for the test set
    predictions = model.predict(X_test)

    # Calculate the RMSE
    rmse = sqrt(mean_squared_error(y_test, predictions))
    print(f"RMSE: {rmse}")


def choose_alpha_for_elastic_net(X_train, y_train, X_test, y_test):
    import pandas as pd
    from sklearn.linear_model import ElasticNet
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import mean_squared_error
    from math import sqrt

    # Assuming X_train, y_train, X_test, y_test are already defined

    # Define the model
    model = ElasticNet()

    # Define the grid of hyperparameters to search
    hyperparameter_grid = {
        'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
        'l1_ratio': np.linspace(0, 1, 10)
    }

    # Set up the grid search with 5-fold cross validation
    grid_cv = GridSearchCV(
        model,
        param_grid=hyperparameter_grid,
        cv=5,
        scoring='neg_root_mean_squared_error',  # RMSE
    )

    # Fit the model and find the best hyperparameters
    print("finished_grid_cv")
    grid_cv.fit(X_train, y_train)

    print(f"Best parameters: {grid_cv.best_params_}")
    print(f"Best RMSE: {-grid_cv.best_score_}")

    # Get the best model
    best_model = grid_cv.best_estimator_

    # Predict the selling amount for the test set using the best model
    predictions = best_model.predict(X_test)

    # Calculate the RMSE for the test set
    rmse = sqrt(mean_squared_error(y_test, predictions))
    print(f"Test RMSE: {rmse}")


def predict_and_save(X, y, X_cancel, y_cancel):
    # Train a classifier to predict if an order will be cancelled
    X_train_cancel, X_test_cancel, y_train_cancel, y_test_cancel = train_test_split(X_cancel, y_cancel, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_cancel, y_train_cancel)

    # Predict cancellations on the entire dataset
    cancel_predictions = clf.predict(X)

    # Train a regressor to predict the cost of cancellation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = rf.predict(X_test)

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"RMSE: {rmse}")

    # Make predictions on the entire dataset
    all_predictions = rf.predict(X)

    # If the order is unlikely to be cancelled, make the prediction -1
    all_predictions[cancel_predictions == 0] = -1

    # Create a dataframe with the ids and predicted selling amount
    output = pd.DataFrame({'id': X.index, 'predicted_selling_amount': all_predictions})

    # Write to csv
    output.to_csv('agoda_cost_of_cancellation.csv', index=False)


def ada_boost(X, y):

    # Create the AdaBoost classifier
    adaboost = AdaBoostClassifier(n_estimators=100, random_state=42)

    # Perform k-fold cross-validation with F1 score using macro averaging
    k = 5  # Number of folds
    scores = cross_val_score(adaboost, X, y, cv=k, scoring='f1_macro')

    # Print the average F1 score across all folds
    print("Average F1 Score (Macro):", scores.mean())


def random_forrest_k_cross(X, y):
    # Create the Random Forest classifier

    rf = RandomForestClassifier(n_estimators=100)

    # Perform k-fold cross-validation with F1 score using macro averaging
    k = 5  # Number of folds
    scores = cross_val_score(rf, X, y, cv=k, scoring='f1_macro')

    # Print the average F1 score across all folds
    print("Average F1 Score (Macro):", scores.mean())


def random_forrest_by_k(X_train, X_test, y_train, y_test):
    # Define a range of n_estimators values to try
    n_estimators_range = range(1, 150, 20)

    # Initialize a list to store the F1 scores
    f1_scores = []

    # Loop over the n_estimators values
    for n_estimators in n_estimators_range:
        print(n_estimators)
        # Initialize the Random Forest classifier with the current number of estimators
        rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)

        # Fit the data to the model
        rf.fit(X_train, y_train)

        # Predict the values for the test set
        y_pred = rf.predict(X_test)

        # Compute the F1 score and append it to the list of F1 scores
        f1 = f1_score(y_test, y_pred, average='macro')
        f1_scores.append(f1)

    # Create a DataFrame with the F1 scores
    df = pd.DataFrame({
        'n_estimators': n_estimators_range,
        'F1 Score': f1_scores
    })

    # Create a line plot of the F1 scores
    fig = px.line(df, x='n_estimators', y='F1 Score', title='F1 Score as a Function of n_estimators')
    fig.show()


def ridge_regression(X_train, X_test, y_train, y_test):
    # Create the Ridge Classifier
    ridge_classifier = RidgeClassifier()

    # Define the alpha values to search
    alphas = [0.1, 1.0, 10.0]

    # Perform grid search
    param_grid = {'alpha': alphas}
    grid_search = GridSearchCV(ridge_classifier, param_grid, cv=5, scoring='f1_macro')
    grid_search.fit(X_train, y_train)

    # Get the alpha values and corresponding mean test scores
    alphas = grid_search.cv_results_['param_alpha'].data.astype(float)
    mean_test_scores = grid_search.cv_results_['mean_test_score']

    # Plot the results
    fig = go.Figure(data=go.Scatter(x=alphas, y=mean_test_scores, mode='markers'))
    fig.update_layout(
        xaxis_type='log',
        xaxis_title='Alpha',
        yaxis_title='Mean F1 Score (Macro)',
        title='Grid Search: Alpha vs. Mean F1 Score'
    )
    fig.show()

    # Get the best alpha value
    best_alpha = grid_search.best_params_['alpha']

    # Fit the data to the model with the best alpha
    ridge_classifier_best = RidgeClassifier(alpha=best_alpha)
    ridge_classifier_best.fit(X_train, y_train)

    # Predict the target variable for the test set
    y_pred = ridge_classifier_best.predict(X_test)

    # Calculate and print the F1 score
    f1 = f1_score(y_test, y_pred, average='macro')
    print('Best Alpha:', best_alpha)
    print('F1 Score (Macro):', f1)



def logistic_regression(X_train, X_test, y_train, y_test):
    # Initializing the logistic regression model
    lr = LogisticRegression()

    # Fitting the data to the model
    lr.fit(X_train, y_train)

    # Predicting the values for the test set
    y_pred = lr.predict(X_test)

    # Printing the accuracy of the model
    f1 = f1_score(y_test, y_pred, average='macro')
    print('Decision Tree Accuracy: ', f1)


def knn(X_train, X_test, y_train, y_test):

    knn = KNeighborsClassifier(n_neighbors=5)

    # Fit the data to the model
    knn.fit(X_train, y_train)

    # Predict the values for the test set
    y_pred = knn.predict(X_test)

    # Compute and print the F1 score
    f1 = f1_score(y_test, y_pred, average='weighted')
    print('F1 Score: ', f1)




from sklearn.metrics import mean_squared_error
from math import sqrt

def decision_tree_loss(X_train, X_test, y_train, y_test):
    train_loss = []
    test_loss = []

    max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for depth in max_depths:
        print(depth)
        # Initialize the model
        model = DecisionTreeRegressor(max_depth=depth)

        # Fit the model
        model.fit(X_train, y_train)

        # Predict the target variable for the train set
        train_predictions = model.predict(X_train)

        # Predict the target variable for the test set
        test_predictions = model.predict(X_test)

        # Calculate the RMSE for train and test sets
        train_rmse = sqrt(mean_squared_error(y_train, train_predictions))
        test_rmse = sqrt(mean_squared_error(y_test, test_predictions))

        # Append the loss values to the lists
        train_loss.append(train_rmse)
        test_loss.append(test_rmse)

    # Create a DataFrame for visualization
    df = pd.DataFrame({'Max Depth': max_depths, 'Train Loss': train_loss, 'Test Loss': test_loss})

    # Plotting using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Max Depth'], y=df['Train Loss'], mode='lines+markers', name='Train Loss'))
    fig.add_trace(go.Scatter(x=df['Max Depth'], y=df['Test Loss'], mode='lines+markers', name='Test Loss'))
    fig.update_layout(title='Loss Over Train and Test Sets',
                      xaxis_title='Max Depth',
                      yaxis_title='Loss',
                      legend=dict(x=0.7, y=0.95),
                      )
    fig.show()


def lasso_regression_graph(X_train, X_test, y_train, y_test):
    rmse_scores = []
    alphas = [0.1, 0.5, 1, 2, 5, 10]
    for alpha in alphas:
        print(alpha)
        # Initialize the model
        model = Lasso(alpha=alpha)

        # Fit the model
        model.fit(X_train, y_train)

        # Predict the selling amount for the test set
        predictions = model.predict(X_test)

        # Calculate the RMSE
        rmse = math.sqrt(mean_squared_error(y_test, predictions))
        rmse_scores.append(rmse)

    # Create a DataFrame for visualization
    df = pd.DataFrame({'Alpha': alphas, 'RMSE': rmse_scores})

    # Plotting using Plotly
    fig = px.line(df, x='Alpha', y='RMSE', title='Lasso Regression Performance')
    fig.show()


def main():
    data = load_data('train_data.csv', parse_dates=['booking_datetime', 'checkin_date', 'checkout_date',
                                                    'hotel_live_date'])
    data = preprocess_data(data)
    X, y = preprocess_Q1(data)
    # predict_and_save(X,y)
    # Split the data into a training set and a test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # y_train = y_train[y_train < 8000]
    # X_train = X_train.loc[y_train.index]
    # random_forrest_by_k(X_train, X_test, y_train, y_test)
    # decision_trees(X_train, X_test, y_train, y_test)
    # lasso_regression_graph(X_train, X_test, y_train, y_test)
    # decision_tree_loss(X_train, X_test, y_train, y_test)
    # random_forest_loss(X_train, X_test, y_train, y_test)
    lasso_loss(X_train, X_test, y_train, y_test)


def random_forest_loss(X_train, X_test, y_train, y_test):
    train_loss = []
    test_loss = []
    sizes = [1, 21, 41, 61, 81, 101]
    for size in sizes:
        # Initialize the model
        print(size)
        model = RandomForestRegressor(n_estimators=size)

        # Fit the model
        model.fit(X_train, y_train)

        # Predict the target variable for the train set
        train_predictions = model.predict(X_train)

        # Predict the target variable for the test set
        test_predictions = model.predict(X_test)

        # Calculate the RMSE for train and test sets
        train_rmse = sqrt(mean_squared_error(y_train, train_predictions))
        test_rmse = sqrt(mean_squared_error(y_test, test_predictions))

        # Append the loss values to the lists
        train_loss.append(train_rmse)
        test_loss.append(test_rmse)

    # Create a DataFrame for visualization
    df = pd.DataFrame({'Ensemble Size': sizes, 'Train Loss': train_loss, 'Test Loss': test_loss})

    # Plotting using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Ensemble Size'], y=df['Train Loss'], mode='lines+markers', name='Train Loss'))
    fig.add_trace(go.Scatter(x=df['Ensemble Size'], y=df['Test Loss'], mode='lines+markers', name='Test Loss'))
    fig.update_layout(title='Loss Over Train and Test Sets',
                      xaxis_title='Ensemble Size',
                      yaxis_title='Loss',
                      legend=dict(x=0.7, y=0.95),
                      )
    fig.show()


def lasso_loss(X_train, X_test, y_train, y_test):
    train_loss = []
    test_loss = []
    alphas = [0.1, 0.5, 1, 2, 5, 10]
    for alpha in alphas:
        print(alpha)
        # Initialize the model
        model = Lasso(alpha=alpha)

        # Fit the model
        model.fit(X_train, y_train)

        # Predict the target variable for the train set
        train_predictions = model.predict(X_train)

        # Predict the target variable for the test set
        test_predictions = model.predict(X_test)

        # Calculate the RMSE for train and test sets
        train_rmse = sqrt(mean_squared_error(y_train, train_predictions))
        test_rmse = sqrt(mean_squared_error(y_test, test_predictions))

        # Append the loss values to the lists
        train_loss.append(train_rmse)
        test_loss.append(test_rmse)

    # Create a DataFrame for visualization
    df = pd.DataFrame({'Alpha': alphas, 'Train Loss': train_loss, 'Test Loss': test_loss})

    # Plotting using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Alpha'], y=df['Train Loss'], mode='lines+markers', name='Train Loss'))
    fig.add_trace(go.Scatter(x=df['Alpha'], y=df['Test Loss'], mode='lines+markers', name='Test Loss'))
    fig.update_layout(title='Loss Over Train and Test Sets',
                      xaxis_title='Alpha',
                      yaxis_title='Loss',
                      legend=dict(x=0.7, y=0.95),
                      )
    fig.show()

if __name__ == '__main__':
    np.random.seed(0)
    main()
