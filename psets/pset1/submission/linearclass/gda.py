import numpy as np
import util

def main(train_path, valid_path, save_path):
    """Problem: Gaussian discriminant analysis (GDA)

    Args:
        train_path: Path to CSV file containing dataset for training.
        valid_path: Path to CSV file containing dataset for validation.
        save_path: Path to save predicted probabilities using np.savetxt().
    """
    # Load dataset
    x_train, y_train = util.load_dataset(train_path, add_intercept=False)

    # *** START CODE HERE ***
    x_valid, y_valid = util.load_dataset(valid_path, add_intercept=False)

    # Train a GDA classifier
    clf = GDA()
    clf.fit(x_train, y_train)

    # Plot decision boundary on validation set
    util.plot(x_valid, y_valid, clf.theta, 'barro/Desktop')

    # Use np.savetxt to save outputs from validation set to save_path
    np.savetxt(save_path, clf.predict(x_valid))
    # *** END CODE HERE ***

class GDA:
    """Gaussian Discriminant Analysis.

    Example usage:
        > clf = GDA()
        > clf.fit(x_train, y_train)
        > clf.predict(x_eval)
    """
    def __init__(self, step_size=1, max_iter=10000, eps=1e-5,
                 theta_0=None, verbose=True):
        """
        Args:
            step_size: Step size for iterative solvers only.
            max_iter: Maximum number of iterations for the solver.
            eps: Threshold for determining convergence.
            theta_0: Initial guess for theta. If None, use the zero vector.
            verbose: Print loss values during training.
        """
        self.theta = theta_0
        self.step_size = step_size
        self.max_iter = max_iter
        self.eps = eps
        self.verbose = verbose

    def fit(self, x, y):
        """Fit a GDA model to training set given by x and y by updating
        self.theta.

        Args:
            x: Training example inputs. Shape (n_examples, dim).
            y: Training example labels. Shape (n_examples,).
        """
        # *** START CODE HERE ***
        # Find phi, mu_0, mu_1, and sigma
        self.phi = np.mean(y)
        self.mu_0 = np.sum((1 - y)[:, None] * x, axis = 0) / np.sum(1 - y)
        self.mu_1 = np.sum(y[:, None] * x, axis = 0) / np.sum(y)
        self.sigma = ((x - self.mu_0).T @ np.diag((1 - y)) @ (x - self.mu_0) + (x - self.mu_1).T @ np.diag((1 - y)) @ (x - self.mu_1))/x.shape

        # Write theta in terms of the parameters
        sigma_inverse = np.linalg.inv(self.sigma)
        self.theta = sigma_inverse @ (self.mu_1 - self.mu_0)
        self.theta_0 = 1 / 2 * self.mu_0.T @ sigma_inverse @ self.mu_0 - 1 / 2 * self.mu_1.T @ sigma_inverse @ self.mu_1 + np.log(
        self.phi / (1 - self.phi))
        self.theta = np.insert(self.theta, 0, self.theta_0)
        # *** END CODE HERE ***

    def predict(self, x):
        """Make a prediction given new inputs x.

        Args:
            x: Inputs of shape (n_examples, dim).

        Returns:
            Outputs of shape (n_examples,).
        """
        # *** START CODE HERE ***
        def sigmoid(z):
            return 1 / (1 + np.exp(-z))

        return sigmoid(x @ self.theta) >= 0.5
        # *** END CODE HERE

if __name__ == '__main__':
    main(train_path='ds1_train.csv',
         valid_path='ds1_valid.csv',
         save_path='gda_pred_1.txt')

    main(train_path='ds2_train.csv',
         valid_path='ds2_valid.csv',
         save_path='gda_pred_2.txt')