from scipy.stats import norm, multivariate_normal

class Sombrerito:

    def __init__ (self, mu_x, mu_y, theta_x, theta_y, theta_xy=0, theta_yx=0):
        # Guardar parametros
        self.mean = [mu_x, mu_y]
        self.cov =[
            [theta_x, theta_xy],
            [theta_yx, theta_y]
        ]

        self.hat = multivariate_normal (self.mean, self.cov)

    def pdf (self, x, y):
        return self.hat.pdf ([x, y])
    
    def rvs (self, size=1):
        # Draw random samples from multivariante normal distribution
        return self.hat.rvs (size=size)
    
if __name__ == "__main__":
    # mean = [5, 2]
    # theta = [
    #     [1, 0],
    #     [0, 1]
    # ]
    # density = Sombrerito (5, 2, 1, 1)

    # print (density.pdf (5, 2))
    # print (multivariate_normal.pdf (mean, mean=mean, cov=theta))

    # hat_x = norm (loc=mean[0], scale=theta[0][0])
    # hat_y = norm (loc=mean[1], scale=theta[1][1])

    # prob_x = hat_x.pdf (mean[0])
    # prob_y = hat_y.pdf (mean[1])

    step_robot = Sombrerito (mu_x=1, mu_y=0, theta_x=0.5, theta_y=0.5)
    while input() == 'q':
        print(step_robot.rvs ())
