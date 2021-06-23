#!/usr/bin/env python
# coding: utf-8


import numpy


# Trying to determine the power required during cruise only (for now) with no wind (for now).


## Inputs

F_d = input("Enter the flight distance in kilometers: ") #Flight Distance [kilometers] #default is 50
alpha = input("Enter the angles of attack in degrees: ") #Angle of attack [degrees] # default is half of 6 which is what is specified as maximum in the energy efficent arrival paper


## Givens

V_cruise = 50.41 #Cruise speed [m/s]
R = 4.0 #Radius of the rotor [m]
A_rotor = 50.26 #Rotor disk area [m^2]
m = 2940 #Mass [kg]
sigma = 0.055 #Thrust weighted solidity ratio
Cd_mean = 0.0089 #Mean blade drag coeffcient
Fp = 0.97 #Accounts for increasein blade section velocity with rotor edgewise and axial speed
k = 1.75 #Induced power factor
Omega = 30.12 #Rotational velocity of the rotor blades [rad/s]
P_max = 494.25 #Total deliverable power [kW]
rho = 1.225 #Air density in [kg/m^3]  ******Check for different heights
g = 9.81 #Acceleration due to gravity [9.81 m/s^2]
Thee = 0 #Rotor tip-path-plane roll angle [degrees]
Theta = alpha #Rotor tip-path-plane pitch angle   ###Theta = Alpha for level flight

## Flight Time

#Assuming constant V_cruise for the duration of the flight
Tf = (F_d*1000)/V_cruise #Time of flight [seconds]
print("The total time of flight is", round(Tf, 2), "seconds, or", numpy.round(Tf/60, 2), "minutes")

## Thrust

T = m*g/(numpy.cos(Thee*numpy.pi/180)*numpy.cos(Theta*numpy.pi/180)) #Total eVTOL thrust [N]
T_rotor = T/4

print("The thrust on each rotor is", round(T_rotor/1000,2), "kN")
print("The total thrust required is", round(T/1000, 2), "kN")

## Induced Velocity (Vi) and Hover Induced Velocity (Vh)

Vh = numpy.sqrt(T_rotor/(2*rho*A_rotor))  #Hover induced velocity

#Induced Velocity
coefficients = [1, 2*V_cruise*numpy.sin(alpha*numpy.pi/180), (V_cruise**2), 0, -Vh**4] #Defining the coefficients of the polynomial

x = numpy.roots(coefficients) #Solves for the roots of the polynomial

#Finding the real positive value that is lower than Vh
for i in range(len(x)):
    if x[i].real > 0 and x[i] < Vh:
        Vi = x[i].real #Induced velocity
        
#Checking the solution for Vi based on Equation 10
y = (Vh**2)/(numpy.sqrt((V_cruise*numpy.cos(alpha*numpy.pi/180))**2+(V_cruise*numpy.sin(alpha*numpy.pi/180)+Vi)**2))

if y-Vi < 0.001:
    print("Vi is good")
else:
    print("***Check Vi***")

## Power

#Induced Power
P_ind_rot = k*T_rotor*Vi

#Parasite Power
P_parasite = T*V_cruise*numpy.sin(alpha*numpy.pi/180) #[W]

#Profile Power ------- is this needed???
P_prof = (rho*A_rotor*((Omega*R)**3)*sigma*Cd_mean*Fp)/8 #[W]

#Total power required
P_required = (P_ind_rot*4+P_parasite+P_prof) #[W]

print("The power required for the flight is", round(P_required/1000, 2), "kW")

## Energy (Performance Index)

E_total = (P_required*Tf)/1E6 #[MJ]
print("The total energy consumption during the flight is", round(E_total, 2), "MJ")

## Summary

print('Alpha = {}°'.format(alpha))
print("Flight Distance =", round(F_d), "km")
print("Flight Time =", round(Tf, 2), "seconds, or", round(Tf/60, 2), "minutes")
print("Total Thurst =", round(T/1000, 2), "kN")
print("Thrust Per Rotor =", round(T_rotor/1000, 2), "kN")
print("---")
print("Power:")
print("  Induced Power =", round(P_ind_rot*4/1000, 2), "kW")
print("  Parasite Power =", round(P_parasite/1000, 2), "kW")
print("  Profile Power =", round(P_prof/1000, 2), "kW")
print("     --> Total Power =", round(P_required/1000, 2), "kW <--")
print("---")
print("Energy:")
print("     --> Total Energy =", round(E_total, 2), "MJ <--")






