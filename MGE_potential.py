import numpy as np
from astropy import units as un
from scipy import constants as cs
import sys

class MGE_potential: 
    def __init__(self, counts = None, sigma = None, inputfilename = None):
        """
        NAME:
            __init__
        PURPOSE:
            initialize a MGE object
        INPUT:
            counts: sol[0, : ] of MGE of density profile
            sigma: sol[1, : ] of MGE of density profile
            inputfilename: file containing mge.sol results
        OUTPUT:
            instance
        HISTORY:
            2016-08-22 - Written (Milanov, MPIA)
        """
        if inputfilename is not None:
            data = np.loadtxt(inputfilename)        
            self._counts = data[0,:]     #[M_sun / pc^2]
            self._sigma = data[1,:]     #[pc]
        elif counts is None or sigma is None:
            sys.exit("Error in MGE_potential.__init__(): Specify input file or counts and sigma.")
        else:
            self._counts = counts       #[M_sun / pc²]
            self._sigma = sigma     #[pc]

        self._G = (un.m ** 3 / (un.kg * un.s ** 2)).to(un.pc ** 3/(un.solMass * un.s ** 2), cs.G) #[pc³ / M_sun * s²]
        self._mass = self._counts * 2. * cs.pi * self._sigma ** 2 #[M_sun]
        self._counts3d = self._counts / (np.sqrt(2. * cs.pi) self._sigma) #[M_sun / pc³]
        return None

    def _H_j(u, R, sigma = self._sigma):
        """
        NAME:
            _H_j
        PURPOSE:
            auxiliary function to calculate potential (see Cappellari 2008, (17))
        INPUT:
            u: integration parameter
            R: distance from centre (only input in potential function)
            sigma: sigma given from MGE 
        OUTPUT:
            one factor of integrand
        HISTORY:
            2016-08-22 - Written (Milanov, MPIA)
        """
        return np.exp(- u ** 2 * R ** 2 / (2. * sigma ** 2))

    def _integrand (u, R, sigma = self._sigma, M = self._mass):
        """
        NAME:
            _integrand
        PURPOSE:
            gives integrand for potential
        INPUT:
            u: integration parameter
            R: distance from centre (only input in potential function)
            sigma: sigma given from MGE
            M: mass calculated from counts given from MGE
        OUTPUT:
            integrand
        HISTORY
            2016-08-22 - Written (Milanov, MPIA)
        """
        H = np.zeros(len(sigma))
        for i in range(len(sigma)): # try with numpy arrays to have H function returning an array already
            H[i] = H_j(u, R, sigma[i])
        return np.sum(M * H / sigma)

    def Potential (R):
        """
        NAME:
            Potential
        PURPOSE:
            calculates potential at distance R
        INPUT:
            R: distance from centre
        OUTPUT:
            Potential
        HISTORY
            2016-08-22 - Written (Milanov, MPIA)
        """
        a = - np.sqrt( 2. / cs.pi) * self._G    #[pc^3/M_sol*s^2]
        b = intg.quad(integrand, 0., 1., args = (R))
        return a * b

    



