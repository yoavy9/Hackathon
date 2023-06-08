from preprocess import *
from utils import *
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import make_scorer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
import joblib


def decision_trees(X_train, X_test, y_train, y_test):
    # Initialize the Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=4)

    # Fit the data to the model
    dt.fit(X_train, y_train)

    # Predict the values for the test set
    y_pred = dt.predict(X_test)

    # Printing the accuracy of the model
    f1 = f1_score(y_test, y_pred, average='macro')
    print('Decision Tree Accuracy: ', f1)


def perform_cross_validation(X, y, depths, cv=5):
    """
    Perform cross-validation for hyperparameter tuning using a decision tree classifier.

    Parameters:
        X (array-like): The input features.
        y (array-like): The target variable.
        param_grid (dict): Dictionary specifying the hyperparameter grid to search.
        cv (int, optional): Number of cross-validation folds. Default is 5.

    Returns:
        float: The average accuracy score across cross-validation folds.
    """
    scores_by_depth = {}  # Dictionary to store scores for each depth

    # Define F1 scorer
    f1_scorer = make_scorer(f1_score)

    for depth in depths:
        dt_classifier = DecisionTreeClassifier(max_depth=depth)
        scores = cross_val_score(dt_classifier, X, y, cv=cv, scoring=f1_scorer)
        scores_by_depth[depth] = scores.mean()

    return scores_by_depth


def random_forrest(X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier(n_estimators=100)

    # Fit the model to the data
    rf.fit(X_train, y_train)

    # Get feature importances
    importances = rf.feature_importances_

    # Create a list of feature names
    feature_names = X_train.columns

    # Sort feature importances in descending order
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for i, index in enumerate(indices):
        print(f"{i + 1}. {feature_names[index]} ({importances[index]:.4f})")
    # Predict the values for the test set
    y_pred = rf.predict(X_test)

    # Compute and print the F1 score
    f1 = f1_score(y_test, y_pred, average='macro')
    print('F1 Score: ', f1)
    return y_pred, rf


def main():
    data = load_data('train_data.csv', parse_dates=['booking_datetime', 'checkin_date', 'checkout_date',
                                              'hotel_live_date'])
    X, y = preprocess_Q2(data)
    # Split the data into a training set and a test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    id = X_test['h_booking_id'].reset_index(drop=True)
    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test, flag_train=False)
    X_train = X_train.drop(['h_booking_id'], axis=1)
    X_test = X_test.drop(['h_booking_id'], axis=1)
    """return Q1"""
    y_pred, rf = random_forrest(X_train, X_test, y_train, y_test)

    result = pd.concat([id, pd.Series(y_pred)], axis=1)
    result.columns = ['id', 'cancellation']
    result.to_csv('agoda_cancellation_prediction.csv', index=False)
    joblib.dump(rf, 'model.pkl')



    ####### load #########
    # loaded_model = joblib.load('model.pkl')
    # X = preprocess_data(X, flag_train=False)
    # X = X.drop(['h_booking_id'], axis=1)
    # y_pred = loaded_model.predict(X)
    # result = pd.concat([data['h_booking_id'], pd.Series(y_pred)], axis=1)
    # result.columns = ['id', 'cancellation']
    # result.to_csv('agoda_cancellation_prediction.csv', index=False)


if __name__ == '__main__':
    np.random.seed(0)
    main()

