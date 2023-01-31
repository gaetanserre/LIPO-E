import numpy as np
from statistical_analysis import LIPO_Statistics

def Uniform(X: np.array):
  """
  This function generates a random point in the feasible region X. We assume that X is a subset of R^n 
  described by the inequalities X = {x in R^n | a_i <= x_i <= b_i, i = 0, ..., m-1} where a_i, b_i are given
  such that X[i,j] = [a_i, b_i] for i = 0, ..., m-1 and j = 0, 1.
  For simplicity, we assume that X C Rectangle given by an infinite norm (i.e. X = {x in R^n | -M <= x_i <= M, i = 1, ..., n}).
  X: feasible region (numpy array)
  """

  theta = np.zeros(X.shape[0])
  for i in range(X.shape[0]):
    theta[i] = np.random.uniform(X[i,0], X[i,1])
  return theta
        

def LIPO(f, n: int, fig_path: str, delta=0.05, max_slope=1000.0):
  """
  f: class of the function to maximize (class)
  n: number of function evaluations (int)
  fig_path: path to save the statistics figures (str)
  max_slope: maximum slope for the nb_samples vs nb_evaluations curve (float)
  """
  
  # Initialization
  t = 1

  X_1 = Uniform(f.bounds)
  nb_samples = 1
  last_nb_samples = [0] * n
  last_nb_samples[t-1] = nb_samples

  points = X_1.reshape(1, -1)
  value = f(X_1)
  values = np.array([value])

  # Statistics
  stats = LIPO_Statistics(f, fig_path, delta=delta)

  def slope_stop_condition():
    if last_nb_samples[2] > 0: # Compute the slope of the last 3 points
      slope = (last_nb_samples[t-1] - last_nb_samples[t-3]) / 2

      return slope > max_slope
    else:
      return False

  def condition(x, values, k, points):
    """
    Subfunction to check the condition in the loop, depending on the set of values we already have.
    values: set of values of the function we explored (numpy array)
    x: point to check (numpy array)
    k: Lipschitz constant (float)
    points: set of points we have explored (numpy array)
    """
    max_val = np.max(values)

    left_min = np.min(values.reshape(-1) + k * np.linalg.norm(x - points, ord=2, axis=1))

    return left_min >= max_val
          
  # Main loop
  while t < n:
    X_tp1 = Uniform(f.bounds)
    nb_samples += 1
    last_nb_samples[t-1] = nb_samples
    if condition(X_tp1, values, f.k, points):
      points = np.concatenate((points, X_tp1.reshape(1, -1)))

      value = f(X_tp1)
      values = np.concatenate((values, np.array([value])))
      
      # Statistical analysis
      stats.update(np.max(values), nb_samples)

      t += 1
    
    elif slope_stop_condition():
      print(f"Exponential growth of the number of samples. Stopping the algorithm at iteration {t}.")
      stats.plot()
      return points, values, nb_samples

    if nb_samples >= 500*n:
      ValueError("LIPO has likely explored every possible \
        region in which the maximum can be, but did not \
        finish the main loop. Please reduce the number \
        of function evaluations.")


  stats.plot()
          
  # Output
  return points, values, nb_samples