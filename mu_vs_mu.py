import numpy as np

import phaseplot
from pylab import *
from scipy.constants import codata

def get_phase_data(S, nsurfaces):
    ''' get_phase_data - Determines which surface composition is most stable
        Parameters
        ----------
            S : 1D numpy array of surface energies
            nsurfaces : int, Total number of surfaces
        Returns
        -------
            X : value
    '''
    S = np.split(S, nsurfaces)
    S = np.column_stack(S)
    x = np.argmin(S, axis=1) + 1
    return x

def get_labels(ticks, data):
    '''Accesses and returns the labels that correspond to the phases displayed on the phase diagram
       Parameters
       ----------
            ticks : list, Phases that are displayed
            data  : list of dictionaries
       Returns
       -------
            labels : list strings
    '''
    labels = []
    for i in range(0, ticks.size):
        val = ticks[i] - 1
        val = int(val)
        l = data[val]['Label']
        labels.append(l)
    
    return labels

def transform_numbers(Z, ticks):
    ''' transform numbers - Takes the phase diagram array and converts the numbers to numbers scaled 0, 1, 2, etc in order to make plotting easier
        Parameters
        ----------
            Z : numpy array - surface stabilities
            ticks : list - unique phases appearing in above array
        Returns
        -------
            Z : numpy array - new array
    '''
    counter = 0
    y = np.arange(ticks.size)
    for i in range(0, ticks.size):
        for j in range(0, Z.size):
            if Z[j] == ticks[i]:
                Z[j] = y[i]
    
    return Z

def pressure(X, T):
    ''' pressure - Calculate the pressure for chemical potential values
        Parameters
        ----------
            X : numpy array - delta mu values
            T : int - temperature
        Returns
        -------
            pressure : numpy array - pressure values
    '''
    k = codata.value('Boltzmann constant in eV/K')
    pressure = X / (k * T * 2.203)

    return pressure

def constants(data, bulk):
    '''constants - calculate the surface energy irrespective of chemical potential
       Parameters
       ----------
            data : list of dictionaries containg info on each surface
            bulk : bulk dictionary
       Returns
       -------
            Yexcess : Excess for the Y species
            Xexcess : Excess for the X species
    '''
    Yexcess = data['Y'] / (data['Area'] * 2.0)
    Xexcess = data['X'] / (2.0 * data['Area'])
    B = (data['Energy'] - data['M']  * (bulk['Energy'] / bulk['F-Units'])) / (2.0 * data['Area'])
    
    return Yexcess, Xexcess, B

def scale(X, Xscale):
    
    return X * Xscale

def calculate_surface_energy(Ux, Uy, yshiftval, xshiftval, Yexcess, Xexcess, B):
    ''' This function calculates the surface for a given chemical potential of
        oxygen and hydrogen
        Parameters
        ----------
            Ux   : Chemical potential of Hmim
            Uy   : Chemical potential of H2O
            yshiftval : shift value for y axis
            xshiftval : shift value for x axis
            Yexcess : Excess Y
            Xexcess : Excess X
            Returns
        -------
            SE  : Surface Energy
    '''
    yshiftval = scale(yshiftval, Yexcess)
    xshiftval = scale(xshiftval, Xexcess)
    C = scale(Xexcess, Ux)
    D = scale(Yexcess, Uy)
    SE = B - C - D - yshiftval - xshiftval

    return SE

def surface_energy_array(data, bulk, X, Y, nsurfaces, xshiftval=None, yshiftval=None):
    ''' This function calculates and returns a 2D numpy array of surface energes
        for a range of chemical potential values
        Parameters
        ----------
            data      : List containing the dictionary data for each phase
            bulk      : dictionary containing data for bulk
            Hmim      : X axis chemical potential values
            H2O       : Y axis chemical potential values
            nsurfaces : Number of phases
            xshiftval : shift value for x axis
            yshiftval : shift value for y axis
        Returns
        -------
            SE_array  : array of surface energies matching chemcial potential values
     '''
    if xshiftval is None:
        xshiftval = 0
    if yshiftval is None:
        yshiftval = 0
    
    Xnew = np.tile(X, Y.size)
    Xnew = np.reshape(Xnew, (Y.size, X.size))
    Ynew = np.tile(Y, X.size)
    Ynew = np.split(Ynew, X.size)
    Ynew = np.column_stack(Ynew)

    S = np.array([])
    for k in range(0, nsurfaces):
        Yexcess, Xexcess, B = constants(data[k], bulk)
        SE = calculate_surface_energy(Xnew, Ynew, yshiftval, xshiftval, Yexcess, Xexcess, B)
        S = np.append(S, SE)
    SE_array = get_phase_data(S, nsurfaces)
    return SE_array

def read_nist(File):
    data = np.genfromtxt(File, skip_header=2)
    return data

def calculate_gibbs(data):
    temperature = data[:,0]
    deltas = data[:,1]
    H = data[:,5]

    DeltaS = (deltas * 0.01036) / 1000
    H = H + H[0]
    H_HT = H * 0.01036
    mu = H_HT - temperature * DeltaS
    data = {'Temperature': temperature, 'Shift': mu}
    return data


def calculate(data, bulk, deltaX, deltaY, xshiftval=None, yshiftval=None, temperature=None, convert_pressure=False, output=None):
    '''Function that runs the calcualtion
       Parameters
       ----------
        data      : List containing the dictionary data for each phase
        bulk      : dictionary containing data for bulk
        Hmim      : X axis chemical potential values
        H2O       : Y axis chemical potential values
        nsurfaces : Number of phases
    '''
    if yshiftval is None:
        yshiftval = 0
        yshift = False
    else:
        yshift = True

    if xshiftval is None:
        xshiftval = 0
        xshift = False
    else:
        xshift = True

    if temperature is None:
        temperature = 0

    if output is None:
        output = "Phase.png"

    data = sorted(data, key=lambda k: (k['X']))
    nsurfaces = len(data)
    X = np.arange(deltaX['Range'][0], deltaX['Range'][1], 0.025, dtype="float")
    Y = np.arange(deltaY['Range'][0], deltaY['Range'][1], 0.025, dtype="float")

    if xshift == True:
        X = X - xshiftval

    if yshift == True:
        Y = Y - yshiftval

    SE_array = surface_energy_array(data, bulk, X, Y, nsurfaces, xshiftval, yshiftval)
    ticks = np.unique([SE_array])
    SE_array = transform_numbers(SE_array, ticks)
    Z = np.reshape(SE_array, (Y.size, X.size))
    labels = get_labels(ticks, data)
                 
    if xshift == False and yshift == False:
        phaseplot.plot_phase(X, Y, Z, ticks, labels, deltaX['Label'], deltaY['Label'], temperature, output)

    elif convert_pressure == False:
        phaseplot.plot_phase(X, Y, Z, ticks, labels, deltaX['Label'], deltaY['Label'], temperature, output)

    elif convert_pressure == True:
        p1 = pressure(X, temperature)
        p2 = pressure(Y, temperature)
        phaseplot.plot_mu_p(X, Y, Z, p1, p2, ticks, labels, deltaX['Label'], deltaY['Label'], temperature, output)
        phaseplot.plot_pressure(p1, p2, Z, ticks, labels, deltaX['Label'], deltaY['Label'], temperature, output="pressure.png")
