"""This file serves as an example how to use MPIPoolEngine
to optimize across nodes and also as a test for the
MPIPoolEngine."""
import pypesto
import numpy as np
import scipy as sp
import pypesto.optimize as optimize
# you need to manually import the MPIPoolEninge
from pypesto.engine.mpi_pool import MPIPoolEngine
# the below is needed for testing purposes.
from numpy.testing import assert_almost_equal

def setup_rosen_problem(n_starts: int = 10):
    """sets up the rosenbrock problem and return
    a pypesto.Problem"""
    objective = pypesto.Objective(fun=sp.optimize.rosen,
                                   grad=sp.optimize.rosen_der,
                                   hess=sp.optimize.rosen_hess)

    dim_full = 10
    lb = -5 * np.ones((dim_full, 1))
    ub = 5 * np.ones((dim_full, 1))

    # fixing startpoints
    startpoints = pypesto.startpoint.latin_hypercube(n_starts=n_starts,
                                                     lb=lb,
                                                     ub=ub)
    problem = pypesto.Problem(objective=objective, lb=lb, ub=ub,
                               x_guesses=startpoints)
    return problem

# set all your code into this if condition.
# This way only one core performs the code
# and distributes the work of the optimization.
if __name__ == '__main__':
    # set number of starts
    n_starts = 2
    #create problem
    problem = setup_rosen_problem()
    # create optimizer
    optimizer = optimize.FidesOptimizer()

    # result2 is the way to call the optimization with MPIPoolEngine.
    result1 = optimize.minimize(
            problem=problem, optimizer=optimizer,
            n_starts=n_starts, engine=pypesto.engine.MultiProcessEngine())
    result2 = optimize.minimize(
            problem=problem, optimizer=optimizer,
            n_starts=n_starts, engine=MPIPoolEngine())


    # starting here are the tests (not needed in your code)
    if(result1.optimize_result.list[0]['id'] ==
            result2.optimize_result.list[0]['id']):
        assert_almost_equal(result1.optimize_result.list[0]['x'],
                            result2.optimize_result.list[0]['x'],
                            err_msg='The final parameter values '
                                    'do not agree for the engines.')
        assert_almost_equal(result1.optimize_result.list[1]['x'],
                            result2.optimize_result.list[1]['x'],
                            err_msg='The final parameter values '
                                    'do not agree for the engines.')
    else:
        assert_almost_equal(result1.optimize_result.list[0]['x'],
                            result2.optimize_result.list[1]['x'],
                            err_msg='The final parameter values '
                                    'do not agree for the engines.')
        assert_almost_equal(result1.optimize_result.list[1]['x'],
                            result2.optimize_result.list[0]['x'],
                            err_msg='The final parameter values '
                                    'do not agree for the engines.')