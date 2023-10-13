import math

from state import State
import constants

from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-poster')


class Individual:
    """
    stores Gray code representation of a control history
    """

    t = np.linspace(0, constants.duration, constants.num_optimization_parameters)
    t_new = np.linspace(0, constants.duration, constants.num_high_resolution_parameters)

    def __init__(self):
        self.controls = []

    def add_control(self, control):
        self.controls.append(control)

    def get_actual_gammas(self):
        actual_gammas = []
        for control in self.controls:
            actual_gammas.append(control.get_actual_gamma())
        return actual_gammas

    def get_actual_betas(self):
        actual_betas = []
        for control in self.controls:
            actual_betas.append(control.get_actual_beta())
        return actual_betas

    def get_high_resolution_gammas(self):
        optimization_gammas = self.get_actual_gammas()

        f = CubicSpline(Individual.t, optimization_gammas, bc_type='natural')
        high_resolution_gammas = f(Individual.t_new)

        return high_resolution_gammas

    def get_high_resolution_betas(self):
        optimization_betas = self.get_actual_betas()

        f = CubicSpline(Individual.t, optimization_betas, bc_type='natural')
        high_resolution_betas = f(Individual.t_new)

        return high_resolution_betas

    def plot_control_history(self):
        optimization_gammas = self.get_actual_gammas()
        high_resolution_gammas = self.get_high_resolution_gammas()

        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, high_resolution_gammas, 'b')
        plt.plot(Individual.t, optimization_gammas, 'ro')
        plt.title('Gamma Control History')
        plt.xlabel('Time (s)')
        plt.ylabel('Heading Angle Rate (rad/s)')
        plt.grid()
        plt.show()

        optimization_betas = self.get_actual_betas()
        high_resolution_betas = self.get_high_resolution_betas()

        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, high_resolution_betas, 'b')
        plt.plot(Individual.t, optimization_betas, 'ro')
        plt.title('Beta Control History')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (ft/s^2)')
        plt.grid()
        plt.show()

    def get_state_history(self):
        high_resolution_gammas = self.get_high_resolution_gammas()
        high_resolution_betas = self.get_high_resolution_betas()

        h = constants.duration / (constants.num_high_resolution_parameters - 1)
        s0 = State(0, 8, 0, 0)

        s = np.zeros(len(Individual.t_new), dtype=State)
        s[0] = s0

        for i in range(constants.num_high_resolution_parameters - 1):
            s[i + 1] = s[i].next_state(high_resolution_gammas[i], high_resolution_betas[i], h)
            if not s[i + 1].is_feasible():
                return None

        return s

    def plot_state_history(self):
        state_history = self.get_state_history()

        if state_history is None:
            return

        x = []
        for state in state_history:
            x.append(state.x)
        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, x, 'b')
        plt.title('x State History')
        plt.xlabel('Time (s)')
        plt.ylabel('x Position (ft)')
        plt.grid()
        plt.show()

        y = []
        for state in state_history:
            y.append(state.y)
        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, y, 'b')
        plt.title('y State History')
        plt.xlabel('Time (s)')
        plt.ylabel('y Position (ft)')
        plt.grid()
        plt.show()

        alpha = []
        for state in state_history:
            alpha.append(state.alpha)
        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, alpha, 'b')
        plt.title('alpha State History')
        plt.xlabel('Time (s)')
        plt.ylabel('Heading Angle (rad)')
        plt.grid()
        plt.show()

        v = []
        for state in state_history:
            v.append(state.v)
        plt.figure(figsize=(12, 8))
        plt.plot(Individual.t_new, v, 'b')
        plt.title('v State History')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (ft/s)')
        plt.grid()
        plt.show()

        # trajectory
        plt.figure(figsize=(12, 8))
        plt.plot(x, y, 'b')
        plt.axhline(y=3, xmin=-15, xmax=-4, color='k')
        plt.axvline(x=-4, ymin=-1, ymax=3, color='k')
        plt.axhline(y=-1, xmin=-4, xmax=4, color='k')
        plt.axvline(x=4, ymin=-1, ymax=3, color='k')
        plt.axhline(y=3, xmin=4, xmax=15, color='k')
        plt.title('Trajectory')
        plt.xlabel('x (ft)')
        plt.ylabel('y (ft)')
        plt.grid()
        plt.show()

    def print_final_state(self):
        state_history = self.get_state_history()

        if state_history is None:
            print('No feasible solution found')

        sf = state_history[-1]
        print('Final state values:')
        print('x_f =', sf.x)
        print('y_f =', sf.y)
        print('alpha_f =', sf.alpha)
        print('v_f =', sf.v)

    def get_cost(self):
        state_history = self.get_state_history()

        if state_history is None:
            return constants.infeasibility_constant

        sf = state_history[-1]
        sf_required = State(0, 0, 0, 0)

        return math.sqrt((sf_required.x - sf.x) ** 2 + (sf_required.y - sf.y) ** 2 +
                         (sf_required.alpha - sf.alpha) ** 2 + (sf_required.v - sf.v) ** 2)

    def get_fitness(self):
        return 1 / (self.get_cost() + 1)
